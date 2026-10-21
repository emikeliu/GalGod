/* ==========================================================================
   ui/history.js
   历史记录界面。对应 screens/history_screen.rpy 与 history_screen.rpy。
   支持点击回滚到某一句。
   ========================================================================== */
(function (global) {
  'use strict';

  function HistoryUI(app) {
    this.app = app;
    this.el = null;
  }

  HistoryUI.prototype.isOpen = function () {
    return !!this.el;
  };

  HistoryUI.prototype.open = function () {
    if (this.el) return;

    var self = this;
    var root = document.createElement('div');
    root.className = 'menu-screen dim';
    root.id = 'menu-history';

    var body = document.createElement('div');
    body.className = 'sl-body';
    body.style.cssText = 'padding:50px 120px 40px;display:flex;flex-direction:column;';

    var head = document.createElement('div');
    head.className = 'sl-head';
    var title = document.createElement('div');
    title.className = 'menu-title';
    title.textContent = '历史记录';
    var close = document.createElement('button');
    close.type = 'button';
    close.textContent = '返回';
    close.style.cssText =
      'height:46px;padding:0 26px;border:1px solid rgba(255,255,255,.3);' +
      'border-radius:4px;background:rgba(255,255,255,.08);color:#ddd;' +
      'font-family:inherit;font-size:17px;cursor:pointer;';
    close.addEventListener('click', function () { self.close(); });
    head.appendChild(title);
    head.appendChild(close);

    var list = document.createElement('div');
    list.className = 'history-list';
    list.style.cssText =
      'flex:1;overflow-y:auto;padding:10px 24px 10px 0;' +
      'display:flex;flex-direction:column;gap:16px;';

    var history = this.app.state.history;
    if (!history.length) {
      var empty = document.createElement('div');
      empty.style.cssText = 'color:rgba(255,255,255,.45);font-size:19px;';
      empty.textContent = '还没有任何对话记录。';
      list.appendChild(empty);
    } else {
      history.forEach(function (h, idx) {
        var row = document.createElement('div');
        row.style.cssText =
          'display:flex;gap:26px;align-items:flex-start;padding:10px 14px;' +
          'border-radius:6px;cursor:pointer;transition:background .15s ease;';
        row.addEventListener('mouseenter', function () {
          row.style.background = 'rgba(255,255,255,.06)';
        });
        row.addEventListener('mouseleave', function () {
          row.style.background = 'transparent';
        });
        row.addEventListener('click', function () {
          self.jumpTo(idx);
        });

        var name = document.createElement('div');
        name.style.cssText =
          'width:180px;flex:0 0 180px;font-size:21px;color:#9ad;' +
          'text-shadow:2px 0 0 rgba(0,0,0,.6);';
        name.textContent = h.who || '　';

        var text = document.createElement('div');
        text.style.cssText =
          'flex:1;font-size:21px;line-height:1.72;color:#eee;' +
          'white-space:pre-wrap;text-shadow:2px 0 0 rgba(0,0,0,.6);';
        text.textContent = h.what;

        row.appendChild(name);
        row.appendChild(text);
        list.appendChild(row);
      });
    }

    body.appendChild(head);
    body.appendChild(list);
    root.appendChild(body);
    this.app.stage.menusLayer.appendChild(root);
    this.el = root;

    /* 滚到底部 */
    list.scrollTop = list.scrollHeight;

    /* Esc 关闭 */
    this._esc = function (e) {
      if (e.key === 'Escape') { e.preventDefault(); self.close(); }
    };
    document.addEventListener('keydown', this._esc);
  };

  HistoryUI.prototype.close = function () {
    if (!this.el) return;
    this.el.parentNode.removeChild(this.el);
    this.el = null;
    if (this._esc) {
      document.removeEventListener('keydown', this._esc);
      this._esc = null;
    }
  };

  /**
   * 回滚到历史记录中的某一句。
   * 由于回滚栈只保留最近的快照，这里按「向后回滚 N 步」逼近目标。
   */
  HistoryUI.prototype.jumpTo = function (index) {
    var vm = this.app.vm;
    var hist = this.app.state.history;
    var target = hist[index];
    if (!target) return;

    /* 找到对应快照 */
    var steps = hist.length - index;
    var ok = false;
    for (var i = 0; i < steps + 4; i++) {
      if (!vm.canRollback()) break;
      vm.rollback();
      var last = this.app.state.history[this.app.state.history.length - 1];
      if (last && last.what === target.what && last.who === target.who) {
        ok = true;
        break;
      }
    }

    if (!ok) {
      this.app.toast('该记录超出回滚范围');
    }
    this.close();
  };

  global.RPYHistoryUI = {
    HistoryUI: HistoryUI
  };
})(window);