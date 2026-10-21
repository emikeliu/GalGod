/* ==========================================================================
   ui/config.js
   系统设置。对应 screens/config.rpy（my_settings_ui）与 screens/preferences.rpy。
   原作是逐层图片 UI，这里做「功能等价 + 图片背景 + DOM 控件」。
   ========================================================================== */
(function (global) {
  'use strict';

  var TABS = [
    { id: 'audio', label: '声音设置', img: 'gui/sound_config_hover.png' },
    { id: 'game',  label: '游戏设置', img: 'gui/game_config_hover.png' },
    { id: 'screen',label: '显示设置', img: 'gui/full_screen_hover.png' }
  ];

  function ConfigUI(app) {
    this.app = app;
    this.el = null;
    this.tab = 'game';
    this.previewTimer = null;
  }

  ConfigUI.prototype.isOpen = function () {
    return !!this.el;
  };

  ConfigUI.prototype.open = function () {
    if (this.el) return;
    var self = this;
    var app = this.app;

    var root = document.createElement('div');
    root.className = 'menu-screen';
    root.id = 'menu-config';

    var closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'menu-close';
    closeBtn.textContent = '返回';
    closeBtn.style.cssText =
      'height:48px;padding:0 26px;border:1px solid rgba(255,255,255,.3);' +
      'border-radius:4px;background:rgba(0,0,0,.5);color:#ddd;' +
      'font-family:inherit;font-size:18px;cursor:pointer;';
    closeBtn.addEventListener('click', function () { self.close(); });

    var body = document.createElement('div');
    body.className = 'cf-body';

    var tabs = document.createElement('div');
    tabs.className = 'cf-tabs';

    TABS.forEach(function (t) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'cf-tab' + (self.tab === t.id ? ' active' : '');
      btn.dataset.tab = t.id;
      btn.title = t.label;

      var url = app.images.url(t.img, 'image');
      if (url) {
        var im = document.createElement('img');
        im.src = url;
        im.alt = t.label;
        btn.appendChild(im);
      } else {
        btn.textContent = t.label;
      }
      btn.addEventListener('click', function () {
        self.tab = t.id;
        tabs.querySelectorAll('.cf-tab').forEach(function (b) {
          b.classList.toggle('active', b.dataset.tab === t.id);
        });
        self.renderPanel();
      });
      tabs.appendChild(btn);
    });

    var panel = document.createElement('div');
    panel.className = 'cf-panel';

    body.appendChild(tabs);
    body.appendChild(panel);
    root.appendChild(closeBtn);
    root.appendChild(body);

    this.root = root;
    this.panel = panel;
    this.el = root;

    this._esc = function (e) {
      if (e.key === 'Escape') { e.preventDefault(); self.close(); }
    };
    document.addEventListener('keydown', this._esc);

    app.stage.menusLayer.appendChild(root);
    this.renderPanel();
  };

  ConfigUI.prototype.close = function () {
    if (!this.el) return;
    if (this.previewTimer) { clearInterval(this.previewTimer); this.previewTimer = null; }
    this.el.parentNode.removeChild(this.el);
    this.el = null;
    if (this._esc) {
      document.removeEventListener('keydown', this._esc);
      this._esc = null;
    }
  };

  /* --------------------------------------------------------------------------
     面板渲染
     -------------------------------------------------------------------------- */
  ConfigUI.prototype.renderPanel = function () {
    var self = this;
    var p = this.panel;
    p.innerHTML = '';

    if (this.tab === 'audio') this.renderAudio(p);
    else if (this.tab === 'game') this.renderGame(p);
    else this.renderScreen(p);
  };

  ConfigUI.prototype.group = function (title) {
    var g = document.createElement('div');
    g.className = 'cf-group';
    var h = document.createElement('h3');
    h.textContent = title;
    g.appendChild(h);
    return g;
  };

  ConfigUI.prototype.row = function (label) {
    var r = document.createElement('div');
    r.className = 'cf-row';
    var l = document.createElement('div');
    l.className = 'cf-label';
    l.textContent = label;
    r.appendChild(l);
    return r;
  };

  /* ---- 声音 ---- */
  ConfigUI.prototype.renderAudio = function (p) {
    var self = this;
    var app = this.app;

    /* 主音量 */
    var g1 = this.group('音量');
    g1.appendChild(this.sliderRow('音乐音量', 'music_volume', 0, 1, 0.05, function (v) {
      app.state.persistent.set('music_volume', v);
      app.audio.applyVolumes();
    }));
    g1.appendChild(this.sliderRow('音效音量', 'sound_volume', 0, 1, 0.05, function (v) {
      app.state.persistent.set('sound_volume', v);
      app.audio.applyVolumes();
    }));
    g1.appendChild(this.sliderRow('语音音量', 'voice_volume', 0, 1, 0.05, function (v) {
      app.state.persistent.set('voice_volume', v);
      app.audio.applyVolumes();
    }));
    p.appendChild(g1);

    /* 角色独立音量 */
    var g2 = this.group('角色语音音量');
    var chars = [
      { code: 'lx', name: '林曦' },
      { code: 'jwq', name: '江晚晴' },
      { code: 'xl', name: '小涟' }
    ];
    chars.forEach(function (c) {
      g2.appendChild(self.sliderRow(c.name, 'char.' + c.code, 0, 1, 0.05, function (v) {
        var map = app.state.persistent.get('character_volume', {}) || {};
        map[c.code] = v;
        app.state.persistent.set('character_volume', map);
      }));
    });
    p.appendChild(g2);
  };

  /* ---- 游戏 ---- */
  ConfigUI.prototype.renderGame = function (p) {
    var self = this;
    var app = this.app;

    var g1 = this.group('文本');
    g1.appendChild(this.sliderRow('文本展示速度', 'text_cps', 0, 120, 1, function (v) {
      app.state.persistent.set('text_cps', v);
      self.updatePreviewSpeed(v);
    }, function (v) { return v === 0 ? '瞬间' : v + ' cps'; }));

    g1.appendChild(this.sliderRow('自动播放速度', 'afm_time', 1, 30, 1, function (v) {
      app.state.persistent.set('afm_time', v);
    }));

    g1.appendChild(this.sliderRow('对话框不透明度', 'dialogue_box_alpha', 0.2, 1, 0.05, function (v) {
      app.state.persistent.set('dialogue_box_alpha', v);
      app.ui.say.applyAlpha();
    }, function (v) { return Math.round(v * 100) + '%'; }));

    p.appendChild(g1);

    /* 文本框预览 */
    var g2 = this.group('文本框预览');
    var preview = document.createElement('div');
    preview.className = 'cf-preview';
    var pvText = document.createElement('div');
    pvText.className = 'pv-text';
    pvText.textContent = '如果能找寻到那真实的解脱，请告诉我';
    preview.appendChild(pvText);
    g2.appendChild(preview);

    var speeds = [30, 15, 60, 0];
    var si = 0;
    this.previewTimer = setInterval(function () {
      var cps = speeds[si++ % speeds.length];
      pvText.textContent = '';
      var full = '如果能找寻到那真实的解脱，请告诉我';
      var i = 0;
      var iv = setInterval(function () {
        if (i >= full.length || !pvText.isConnected) { clearInterval(iv); return; }
        pvText.textContent = full.slice(0, ++i);
      }, cps === 0 ? 1 : 1000 / cps);
    }, 5200);

    p.appendChild(g2);

    /* 快进 */
    var g3 = this.group('快进');
    g3.appendChild(this.sliderRow('快进速度', 'skip_speed_var', 1, 10, 1, function (v) {
      app.state.persistent.set('skip_speed_var', v);
    }, function (v) { return v + ' 级'; }));
    p.appendChild(g3);
  };

  /* ---- 显示 ---- */
  ConfigUI.prototype.renderScreen = function (p) {
    var self = this;
    var app = this.app;

    var g = this.group('显示模式');
    var r = this.row('窗口 / 全屏');
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'cf-toggle';
    btn.textContent = document.fullscreenElement ? '全屏' : '窗口';
    btn.classList.toggle('on', !!document.fullscreenElement);
    btn.addEventListener('click', function () {
      if (document.fullscreenElement) {
        document.exitFullscreen();
      } else {
        document.documentElement.requestFullscreen().catch(function () {
          app.toast('当前浏览器不允许全屏');
        });
      }
    });
    r.appendChild(btn);
    g.appendChild(r);
    p.appendChild(g);

    var g2 = this.group('舞台');
    var r2 = this.row('等比缩放');
    var info = document.createElement('span');
    info.style.color = '#aaa';
    info.textContent = '1920 × 1080 等比缩放，两侧自动留黑边';
    r2.appendChild(info);
    g2.appendChild(r2);
    p.appendChild(g2);

    var g3 = this.group('其他');
    var r3 = this.row('重新加载资源清单');
    var b3 = document.createElement('button');
    b3.type = 'button';
    b3.className = 'cf-toggle';
    b3.textContent = '刷新';
    b3.addEventListener('click', function () { global.location.reload(); });
    r3.appendChild(b3);
    g3.appendChild(r3);
    p.appendChild(g3);
  };

  /* --------------------------------------------------------------------------
     控件工厂
     -------------------------------------------------------------------------- */
  ConfigUI.prototype.sliderRow = function (label, key, min, max, step, onChange, fmt) {
    var app = this.app;
    var r = this.row(label);

    var input = document.createElement('input');
    input.type = 'range';
    input.className = 'cf-range';
    input.min = min;
    input.max = max;
    input.step = step;

    var cur = app.state.persistent.get(key.replace('char.', ''), app.state.persistent.data[key]);
    if (key.indexOf('char.') === 0) {
      var code = key.slice(5);
      var map = app.state.persistent.get('character_volume', {}) || {};
      cur = map[code] == null ? 1 : map[code];
    }
    input.value = cur == null ? min : cur;

    var val = document.createElement('span');
    val.className = 'cf-value';
    var show = function (v) { return fmt ? fmt(v) : Number(v).toFixed(2); };
    val.textContent = show(input.value);

    input.addEventListener('input', function () {
      var v = parseFloat(input.value);
      val.textContent = show(v);
      onChange(v);
    });

    r.appendChild(input);
    r.appendChild(val);
    return r;
  };

  ConfigUI.prototype.updatePreviewSpeed = function () {
    /* 预览速度由 renderGame 的定时器自动轮换，这里无需额外处理 */
  };

  global.RPYConfigUI = {
    ConfigUI: ConfigUI
  };
})(window);