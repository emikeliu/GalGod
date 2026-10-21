/* ==========================================================================
   ui/save_load.js
   存档 / 读档界面。对应 screens/save_load.rpy：
   3 列 × 2 行，页签 auto / quick / 1 / 2 / 3。
   ========================================================================== */
(function (global) {
  'use strict';

  function SaveLoadUI(app) {
    this.app = app;
    this.el = null;
    this.mode = 'save';   /* 'save' | 'load' */
    this.page = '1';
  }

  SaveLoadUI.prototype.isOpen = function () {
    return !!this.el;
  };

  SaveLoadUI.prototype.open = function (mode, page) {
    this.mode = mode || 'save';
    this.page = page || (this.app.save.hasAny() ? '1' : '1');
    if (this.el) this.render();
    else this.build();
  };

  SaveLoadUI.prototype.build = function () {
    var self = this;
    var root = document.createElement('div');
    root.className = 'menu-screen dim';
    root.id = this.mode === 'save' ? 'menu-save' : 'menu-load';

    var body = document.createElement('div');
    body.className = 'sl-body';

    var head = document.createElement('div');
    head.className = 'sl-head';

    var title = document.createElement('div');
    title.className = 'menu-title';
    title.textContent = this.mode === 'save' ? '保存游戏' : '读取游戏';

    var right = document.createElement('div');
    right.style.cssText = 'display:flex;align-items:center;gap:24px;';

    var pages = document.createElement('div');
    pages.className = 'sl-pages';

    var close = document.createElement('button');
    close.type = 'button';
    close.textContent = '返回';
    close.style.cssText =
      'height:44px;padding:0 24px;border:1px solid rgba(255,255,255,.3);' +
      'border-radius:4px;background:rgba(255,255,255,.08);color:#ddd;' +
      'font-family:inherit;font-size:17px;cursor:pointer;';
    close.addEventListener('click', function () { self.close(); });

    right.appendChild(pages);
    right.appendChild(close);
    head.appendChild(title);
    head.appendChild(right);

    var grid = document.createElement('div');
    grid.className = 'sl-grid';

    body.appendChild(head);
    body.appendChild(grid);
    root.appendChild(body);

    this.root = root;
    this.grid = grid;
    this.pagesEl = pages;
    this.el = root;

    root.addEventListener('click', function (e) {
      if (e.target === root) self.close();
    });

    this._esc = function (e) {
      if (e.key === 'Escape') { e.preventDefault(); self.close(); }
    };
    document.addEventListener('keydown', this._esc);

    this.app.stage.menusLayer.appendChild(root);
    this.render();
  };

  SaveLoadUI.prototype.render = function () {
    var self = this;

    /* 页签 */
    this.pagesEl.innerHTML = '';
    global.RPYSave.PAGES.forEach(function (p) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = pageLabel(p);
      if (p === self.page) btn.classList.add('active');
      btn.addEventListener('click', function () {
        self.page = p;
        self.render();
      });
      self.pagesEl.appendChild(btn);
    });

    /* 槽位 */
    this.grid.innerHTML = '';
    var slots = this.app.save.list(this.page);

    slots.forEach(function (slotInfo) {
      var cell = document.createElement('div');
      cell.className = 'slot' + (slotInfo.empty ? ' empty' : '');

      var label = document.createElement('div');
      label.className = 'slot-label';
      label.textContent = pageLabel(self.page) + ' · ' + slotInfo.slot;
      cell.appendChild(label);

      var text = document.createElement('div');
      text.className = 'slot-text';
      text.textContent = slotInfo.empty
        ? '— 空槽位 —'
        : (slotInfo.info.text || '（无对白）');
      cell.appendChild(text);

      var time = document.createElement('div');
      time.className = 'slot-time';
      time.textContent = slotInfo.empty ? '' : (slotInfo.info.timeText || '');
      cell.appendChild(time);

      cell.addEventListener('click', function () {
        if (self.mode === 'save') {
          self.doSave(slotInfo.slot);
        } else {
          if (slotInfo.empty) {
            self.app.toast('该槽位为空');
            return;
          }
          self.doLoad(slotInfo.slot);
        }
      });

      if (!slotInfo.empty) {
        var del = document.createElement('button');
        del.type = 'button';
        del.className = 'slot-del';
        del.textContent = '×';
        del.title = '删除该存档';
        del.addEventListener('click', function (e) {
          e.stopPropagation();
          self.app.ui.confirm.ask('删除第 ' + slotInfo.slot + ' 号存档？').then(function (yes) {
            if (!yes) return;
            self.app.save.remove(self.page, slotInfo.slot);
            self.render();
          });
        });
        cell.appendChild(del);
      }

      self.grid.appendChild(cell);
    });
  };

  SaveLoadUI.prototype.doSave = function (slot) {
    var ok = this.app.save.save(this.page, slot);
    if (ok) {
      this.app.toast('已保存到 ' + pageLabel(this.page) + ' · ' + slot);
      this.render();
    }
  };

  SaveLoadUI.prototype.doLoad = function (slot) {
    this.close();
    this.app.save.load(this.page, slot);
  };

  SaveLoadUI.prototype.close = function () {
    if (!this.el) return;
    this.el.parentNode.removeChild(this.el);
    this.el = null;
    if (this._esc) {
      document.removeEventListener('keydown', this._esc);
      this._esc = null;
    }
  };

  function pageLabel(p) {
    if (p === 'auto') return '自动';
    if (p === 'quick') return '快速';
    return String(p);
  }

  global.RPYSaveLoadUI = {
    SaveLoadUI: SaveLoadUI
  };
})(window);