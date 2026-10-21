/* ==========================================================================
   ui/main_menu.js
   主菜单。对应 screens/main_menu.rpy：
   背景 images/cg/main_screen.avif，底部一排 245x98 图标按钮。
   ========================================================================== */
(function (global) {
  'use strict';

  var S = global.RPYStrings;

  function MainMenu(app) {
    this.app = app;
    this.el = null;
  }

  MainMenu.prototype.isOpen = function () {
    return !!this.el;
  };

  MainMenu.prototype.show = function () {
    if (this.el) return;
    var self = this;
    var app = this.app;

    var root = document.createElement('div');
    root.className = 'menu-screen';
    root.id = 'menu-main';

    /* 背景 */
    var bgUrl = app.images.url('images/cg/main_screen.avif', 'image');
    if (bgUrl) {
      var img = document.createElement('img');
      img.className = 'mm-bg';
      img.src = bgUrl;
      img.alt = '';
      root.appendChild(img);
    }

    /* 按钮行 */
    var row = document.createElement('div');
    row.className = 'mm-row';

    var buttons = [
      { key: 'continue', label: '继续游戏', on: function () { self.onContinue(); }, disabled: !app.save.hasAny() },
      { key: 'start',    label: '开始游戏', on: function () { self.onStart(); } },
      { key: 'load',     label: '读取游戏', on: function () { app.ui.saveLoad.open('load'); } },
      { key: 'config',   label: '系统设置', on: function () { app.ui.config.open(); } },
      { key: 'gallery',  label: '附加鉴赏', on: function () { app.ui.gallery.open(); } },
      { key: 'about',    label: '作者的话', on: function () { app.ui.about.open(); } },
      { key: 'quit',     label: '退出游戏', on: function () { self.onQuit(); } }
    ];

    var FILE_KEY = {
      continue: 'mm_continunes',
      start: 'mm_start',
      load: 'mm_load',
      config: 'mm_config',
      gallery: 'mm_gallery',
      about: 'mm_about',
      quit: 'mm_quit'
    };

    buttons.forEach(function (b) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'mm-btn';
      btn.disabled = !!b.disabled;
      btn.title = b.label;
      btn.setAttribute('aria-label', b.label);

      var base = FILE_KEY[b.key];
      var idle = app.images.url('gui/' + base + '_idle.png', 'image');
      var hover = app.images.url('gui/' + base + '_hover.png', 'image');
      var insensitive = app.images.url('gui/' + base + '_insensitive.png', 'image');

      var im = document.createElement('img');
      im.src = idle || '';
      im.alt = b.label;
      im.onerror = function () {
        /* 缺图时退化为文字按钮 */
        im.remove();
        btn.textContent = b.label;
        btn.style.cssText =
          'width:245px;height:98px;font-size:20px;color:#fff;background:none;' +
          'border:1px solid rgba(255,255,255,.25);border-radius:6px;' +
          'font-family:inherit;cursor:pointer;';
      };

      if (hover) {
        btn.addEventListener('mouseenter', function () { im.src = hover; });
        btn.addEventListener('mouseleave', function () {
          im.src = btn.disabled && insensitive ? insensitive : idle;
        });
      }

      btn.addEventListener('click', function () {
        app.playUiClick();
        b.on();
      });
      btn.addEventListener('mouseenter', function () { app.playUiHover(); });

      btn.appendChild(im);
      row.appendChild(btn);
    });

    root.appendChild(row);

    var ver = document.createElement('div');
    ver.className = 'mm-version';
    ver.textContent = 'v' + (app.program.version || '1.0.0') + '  ·  Web RPY Loader';
    root.appendChild(ver);

    app.stage.menusLayer.appendChild(root);
    this.el = root;

    app.playMenuMusic();
  };

  MainMenu.prototype.hide = function () {
    if (!this.el) return;
    this.el.parentNode.removeChild(this.el);
    this.el = null;
  };

  MainMenu.prototype.onStart = function () {
    var app = this.app;
    this.hide();
    app.stopMenuMusic();
    app.vm.start('start');
  };

  MainMenu.prototype.onContinue = function () {
    var app = this.app;
    var best = app.save.latest();
    if (!best) {
      app.toast('没有可继续的存档');
      return;
    }
    var parts = best.key.split('.');
    this.hide();
    app.stopMenuMusic();
    app.save.load(parts[0], parseInt(parts[1], 10));
  };

  MainMenu.prototype.onQuit = function () {
    var app = this.app;
    app.ui.confirm.ask('确定要退出游戏吗？').then(function (yes) {
      if (!yes) return;
      app.hideAll();
      app.showQuitScreen();
    });
  };

  global.RPYMainMenu = {
    MainMenu: MainMenu
  };
})(window);