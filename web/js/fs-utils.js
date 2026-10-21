/* ==========================================================================
   fs-utils.js
   小工具集合：DOM 便捷方法、Toast、确认框、章节名映射。
   注意：本文件在 index.html 中先于其他脚本加载。
   ========================================================================== */
(function (global) {
  'use strict';

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function qsa(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function delay(ms) {
    return new Promise(function (r) { setTimeout(r, ms); });
  }

  /* --------------------------------------------------------------------------
     确认框
     -------------------------------------------------------------------------- */
  function Confirm(app) {
    this.app = app;
    this.el = null;
    this.resolve = null;
  }

  Confirm.prototype.isOpen = function () {
    return !!this.el;
  };

  Confirm.prototype.ask = function (message) {
    var self = this;
    if (this.el) this.close(false);

    var root = el('div', 'menu-screen');
    root.id = 'menu-confirm';

    var box = el('div', 'cf-box');
    var msg = el('div', 'cf-msg', message);
    var actions = el('div', 'cf-actions');

    var yes = el('button');
    yes.type = 'button';
    var yesImg = el('img');
    yesImg.src = this.app.images.url('gui/YES_hover.png', 'image') || '';
    yesImg.alt = '确认';
    yesImg.onerror = function () { yes.textContent = '确认'; };
    yes.appendChild(yesImg);
    yes.addEventListener('click', function () { self.close(true); });

    var no = el('button');
    no.type = 'button';
    var noImg = el('img');
    noImg.src = this.app.images.url('gui/NO_hover.png', 'image') || '';
    noImg.alt = '取消';
    noImg.onerror = function () { no.textContent = '取消'; };
    no.appendChild(noImg);
    no.addEventListener('click', function () { self.close(false); });

    actions.appendChild(yes);
    actions.appendChild(no);
    box.appendChild(msg);
    box.appendChild(actions);
    root.appendChild(box);

    this.el = root;
    this.app.stage.menusLayer.appendChild(root);

    this._esc = function (e) {
      if (e.key === 'Escape') { e.preventDefault(); self.close(false); }
    };
    document.addEventListener('keydown', this._esc);

    return new Promise(function (resolve) {
      self.resolve = resolve;
    });
  };

  Confirm.prototype.close = function (answer) {
    if (!this.el) return;
    this.el.parentNode.removeChild(this.el);
    this.el = null;
    if (this._esc) {
      document.removeEventListener('keydown', this._esc);
      this._esc = null;
    }
    var r = this.resolve;
    this.resolve = null;
    if (r) r(!!answer);
  };

  /* --------------------------------------------------------------------------
     Toast
     -------------------------------------------------------------------------- */
  function Toast(app) {
    this.app = app;
    this.el = null;
    this.timer = null;
  }

  Toast.prototype.show = function (msg, ms) {
    if (this.el) this.el.parentNode.removeChild(this.el);
    clearTimeout(this.timer);

    var t = el('div', 'toast', msg);
    this.app.stage.screensLayer.appendChild(t);
    this.el = t;

    var self = this;
    this.timer = setTimeout(function () {
      if (self.el && self.el.parentNode) self.el.parentNode.removeChild(self.el);
      self.el = null;
    }, ms || 1800);
  };

  /* --------------------------------------------------------------------------
     章节名
     -------------------------------------------------------------------------- */
  var CHAPTER_NAMES = {
    scene_1_1: '第一章 · 早晨',
    scene_1_2: '第一章 · 教室',
    scene_1_3: '第一章 · 放学后',
    scene_1_4: '第一章 · 归家',
    scene_2_1: '第二章 · 三人行',
    interlude1: '第二章 · 插曲',
    interlude2: '第二章 · 插曲',
    interlude_interview: '第二章 · 面试',
    scene_2_2: '第二章 · 选择',
    scene_2_3: '第二章 · 体验馆',
    scene_2_4: '第二章 · 雨夜',
    scene_3_1: '第三章 · 日常',
    scene_3_2: '第三章',
    scene_3_3: '第三章',
    scene_3_4: '第三章 · 抉择',
    end2: '结局 · 让小涟诞生',
    end3: '结局 · 对小涟放手',
    end_te: '真结局',
    after_story_noctella: '尾声 · 诺提拉',
    start: '序章'
  };

  global.RPYUtils = {
    el: el,
    qs: qs,
    qsa: qsa,
    delay: delay,
    Confirm: Confirm,
    Toast: Toast,
    CHAPTER_NAMES: CHAPTER_NAMES
  };
})(window);