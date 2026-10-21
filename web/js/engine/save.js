/* ==========================================================================
   engine/save.js
   存读档：3 页 × 6 槽 + 自动 / 快速。
   与 Ren'Py 的 FileSave / FileLoad 对应，数据存 localStorage。
   槽位展示「对白摘要 + 时间」，不需要截图。
   ========================================================================== */
(function (global) {
  'use strict';

  var KEY_PREFIX = 'galgod.save.';
  var INDEX_KEY = 'galgod.save.index';
  var PAGES = ['auto', 'quick', '1', '2', '3'];
  var SLOTS_PER_PAGE = 6;

  function SaveManager(app) {
    this.app = app;
  }

  SaveManager.prototype.keyFor = function (page, slot) {
    return KEY_PREFIX + page + '.' + slot;
  };

  SaveManager.prototype.readIndex = function () {
    try {
      var raw = global.localStorage.getItem(INDEX_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) { return {}; }
  };

  SaveManager.prototype.writeIndex = function (idx) {
    try {
      global.localStorage.setItem(INDEX_KEY, JSON.stringify(idx));
    } catch (e) { /* ignore */ }
  };

  /* --------------------------------------------------------------------------
     写档
     -------------------------------------------------------------------------- */
  SaveManager.prototype.save = function (page, slot) {
    var data = this.app.vm.saveState();
    if (!data) {
      this.app.toast('当前没有可保存的进度');
      return false;
    }

    data.version = 1;
    data.page = String(page);
    data.slot = slot;
    data.labelName = this.app.chapterTitle(data.label);

    /* 摘要文本：与 screens/save_load.rpy 一致，超过 8 字换行、超过 15 字省略 */
    var dlg = data.dialogue;
    var summary = dlg ? String(dlg.text || '') : '';
    summary = global.RPYStrings.stripTags(summary).replace(/\s+/g, ' ').trim();
    data.dialogue_text = summary.length > 15 ? summary.slice(0, 14) + '…' : summary;
    data.time_text = formatTime(new Date());

    try {
      global.localStorage.setItem(this.keyFor(page, slot), JSON.stringify(data));
    } catch (e) {
      this.app.toast('保存失败：本地存储空间不足');
      return false;
    }

    var idx = this.readIndex();
    idx[page + '.' + slot] = {
      time: data.time,
      timeText: data.time_text,
      text: data.dialogue_text,
      label: data.label,
      chapter: data.labelName
    };
    this.writeIndex(idx);
    return true;
  };

  /* --------------------------------------------------------------------------
     读档
     -------------------------------------------------------------------------- */
  SaveManager.prototype.load = function (page, slot) {
    var raw = null;
    try {
      raw = global.localStorage.getItem(this.keyFor(page, slot));
    } catch (e) { raw = null; }
    if (!raw) {
      this.app.toast('该槽位为空');
      return false;
    }
    var data;
    try {
      data = JSON.parse(raw);
    } catch (e) {
      this.app.toast('存档损坏');
      return false;
    }
    this.app.closeAllMenus();
    this.app.vm.loadState(data);
    return true;
  };

  SaveManager.prototype.remove = function (page, slot) {
    try {
      global.localStorage.removeItem(this.keyFor(page, slot));
    } catch (e) { /* ignore */ }
    var idx = this.readIndex();
    delete idx[page + '.' + slot];
    this.writeIndex(idx);
  };

  SaveManager.prototype.list = function (page) {
    var idx = this.readIndex();
    var out = [];
    for (var s = 1; s <= SLOTS_PER_PAGE; s++) {
      var info = idx[String(page) + '.' + s];
      out.push({
        slot: s,
        empty: !info,
        info: info || null
      });
    }
    return out;
  };

  SaveManager.prototype.hasAny = function () {
    var idx = this.readIndex();
    return Object.keys(idx).length > 0;
  };

  SaveManager.prototype.latest = function () {
    var idx = this.readIndex();
    var best = null;
    Object.keys(idx).forEach(function (k) {
      var v = idx[k];
      if (!best || v.time > best.time) best = { key: k, info: v };
    });
    return best;
  };

  function formatTime(d) {
    function p(n) { return n < 10 ? '0' + n : String(n); }
    return d.getFullYear() + '/' + p(d.getMonth() + 1) + '/' + p(d.getDate()) +
      ' ' + p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds());
  }

  global.RPYSave = {
    SaveManager: SaveManager,
    PAGES: PAGES,
    SLOTS_PER_PAGE: SLOTS_PER_PAGE,
    formatTime: formatTime
  };
})(window);