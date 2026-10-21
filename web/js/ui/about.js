/* ==========================================================================
   ui/about.js
   作者的话。对应 screens/other_screens.rpy 的 about 屏幕。
   未通关 True End 时显示解锁提示（与原作逻辑一致）。
   ========================================================================== */
(function (global) {
  'use strict';

  function AboutUI(app) {
    this.app = app;
    this.el = null;
  }

  AboutUI.prototype.isOpen = function () {
    return !!this.el;
  };

  AboutUI.prototype.open = function () {
    if (this.el) return;
    var self = this;
    var app = this.app;

    var root = document.createElement('div');
    root.className = 'menu-screen dim';
    root.id = 'menu-about';

    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'menu-close';
    close.textContent = '返回';
    close.style.cssText =
      'height:48px;padding:0 26px;border:1px solid rgba(255,255,255,.3);' +
      'border-radius:4px;background:rgba(0,0,0,.5);color:#ddd;' +
      'font-family:inherit;font-size:18px;cursor:pointer;';
    close.addEventListener('click', function () { self.close(); });

    var body = document.createElement('div');
    body.className = 'ab-body';

    var card = document.createElement('div');
    card.className = 'ab-card';

    var cleared = !!app.state.persistent.get('game_cleared');

    if (cleared) {
      var text = document.createElement('div');
      text.className = 'ab-text';
      text.textContent = app.aboutText();
      card.appendChild(text);
    } else {
      var locked = document.createElement('div');
      locked.className = 'ab-locked';
      locked.textContent = '通关 True End，解锁 ED、尾声，与《作者的话》';
      card.appendChild(locked);
    }

    body.appendChild(card);
    root.appendChild(close);
    root.appendChild(body);

    this.el = root;
    this._esc = function (e) {
      if (e.key === 'Escape') { e.preventDefault(); self.close(); }
    };
    document.addEventListener('keydown', this._esc);

    app.stage.menusLayer.appendChild(root);
  };

  AboutUI.prototype.close = function () {
    if (!this.el) return;
    this.el.parentNode.removeChild(this.el);
    this.el = null;
    if (this._esc) {
      document.removeEventListener('keydown', this._esc);
      this._esc = null;
    }
  };

  global.RPYAboutUI = {
    AboutUI: AboutUI
  };
})(window);