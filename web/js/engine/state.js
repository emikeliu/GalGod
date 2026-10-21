/* ==========================================================================
   engine/state.js
   运行时状态：变量表、舞台快照、历史、成就、可持久化项。
   与 Ren'Py 的 store / persistent / _history_list 对应。
   ========================================================================== */
(function (global) {
  'use strict';

  var PERSIST_KEY = 'galgod.persistent.v1';

  function Persistent() {
    this.data = {
      game_cleared: false,
      dialogue_box_alpha: 0.7,
      skip_speed_var: 5,
      text_cps: 30,
      afm_time: 15,
      music_volume: 0.9,
      sound_volume: 0.9,
      voice_volume: 0.9,
      character_volume: { lx: 1.0, jwq: 1.0, xl: 1.0 },
      seen: {},
      achievements: {},
      gallery_unlocked: {},
      mobile_privacy_agreed: false
    };
    this.load();
  }

  Persistent.prototype.load = function () {
    try {
      var raw = global.localStorage.getItem(PERSIST_KEY);
      if (!raw) return;
      var obj = JSON.parse(raw);
      for (var k in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, k)) this.data[k] = obj[k];
      }
    } catch (e) {
      /* localStorage 不可用时静默降级为内存态 */
    }
  };

  Persistent.prototype.save = function () {
    try {
      global.localStorage.setItem(PERSIST_KEY, JSON.stringify(this.data));
    } catch (e) { /* ignore */ }
  };

  Persistent.prototype.get = function (key, dflt) {
    var parts = String(key).split('.');
    var cur = this.data;
    for (var i = 0; i < parts.length; i++) {
      if (cur == null) return dflt;
      cur = cur[parts[i]];
    }
    return cur === undefined ? dflt : cur;
  };

  Persistent.prototype.set = function (key, value) {
    var parts = String(key).split('.');
    var cur = this.data;
    for (var i = 0; i < parts.length - 1; i++) {
      if (cur[parts[i]] == null || typeof cur[parts[i]] !== 'object') cur[parts[i]] = {};
      cur = cur[parts[i]];
    }
    cur[parts[parts.length - 1]] = value;
    this.save();
  };

  /* --------------------------------------------------------------------------
     运行时 State
     -------------------------------------------------------------------------- */
  function State() {
    this.vars = Object.create(null);       /* store 变量 */
    this.persistent = new Persistent();
    this.history = [];                     /* {who, what, voice, rollbackPc} */
    this.achievements = Object.create(null);

    /* 舞台 */
    this.bg = null;                        /* {name, path, fit, zoom, x, y} */
    this.cg = [];                          /* [{name, path, ...}] */
    this.sprites = Object.create(null);    /* code -> {expr, pos, zoom, xOffset, yOffset} */
    this.layerFilters = Object.create(null); /* master -> 'memory' | 'gray' | null */
    this.overlays = [];                    /* cinematic_black_overlay 等 */

    /* 音频 */
    this.music = null;
    this.ambient = null;
    this.voice = null;

    /* UI */
    this.windowMode = 'auto';              /* auto | show | hide */
    this.quickMenu = true;
    this.customUi = true;
    this.scriptBoxAlpha = 1.0;
    this.sayVisible = false;
    this.skipMode = false;
    this.autoMode = false;
  }

  State.prototype.getVar = function (name) {
    if (name === 'persistent') return this.persistent.data;
    if (name.indexOf('persistent.') === 0) {
      return this.persistent.get(name.slice('persistent.'.length));
    }
    if (name === 'store') return this.vars;
    if (name.indexOf('store.') === 0) {
      return this.vars[name.slice('store.'.length)];
    }
    if (Object.prototype.hasOwnProperty.call(this.vars, name)) return this.vars[name];
    return undefined;
  };

  State.prototype.setVar = function (name, value) {
    if (name.indexOf('persistent.') === 0) {
      this.persistent.set(name.slice('persistent.'.length), value);
      return;
    }
    if (name.indexOf('store.') === 0) {
      this.vars[name.slice('store.'.length)] = value;
      return;
    }
    this.vars[name] = value;
  };

  /** 支持 a.b.c 与 a['k'] 形式的路径写入（供 $ 语句使用） */
  State.prototype.setPath = function (path, value) {
    var p = String(path).trim();

    /* 简单标识符 / 点号路径 */
    if (/^[A-Za-z_][\w]*(\.[A-Za-z_][\w]*)*$/.test(p)) {
      var parts = p.split('.');
      if (parts.length === 1) {
        this.setVar(parts[0], value);
        return;
      }
      /* persistent.x.y */
      if (parts[0] === 'persistent') {
        this.persistent.set(parts.slice(1).join('.'), value);
        return;
      }
      var root = this.getVar(parts[0]);
      if (root === undefined || root === null) return;
      var cur = root;
      for (var i = 1; i < parts.length - 1; i++) {
        if (cur[parts[i]] == null) cur[parts[i]] = {};
        cur = cur[parts[i]];
      }
      cur[parts[parts.length - 1]] = value;
      return;
    }

    /* a['k'] 或 a["k"] */
    var m = /^([A-Za-z_][\w]*)\[(['"])(.*?)\2\]$/.exec(p);
    if (m) {
      var obj = this.getVar(m[1]);
      if (obj && typeof obj === 'object') obj[m[3]] = value;
      return;
    }
    /* 其余形态：忽略，由调用方记诊断 */
  };

  State.prototype.getPath = function (path) {
    var p = String(path).trim();
    if (/^[A-Za-z_][\w]*(\.[A-Za-z_][\w]*)*$/.test(p)) {
      var parts = p.split('.');
      if (parts.length === 1) return this.getVar(parts[0]);
      if (parts[0] === 'persistent') {
        return this.persistent.get(parts.slice(1).join('.'));
      }
      var cur = this.getVar(parts[0]);
      for (var i = 1; i < parts.length; i++) {
        if (cur == null) return undefined;
        cur = cur[parts[i]];
      }
      return cur;
    }
    var m = /^([A-Za-z_][\w]*)\[(['"])(.*?)\2\]$/.exec(p);
    if (m) {
      var obj = this.getVar(m[1]);
      return obj ? obj[m[3]] : undefined;
    }
    return undefined;
  };

  /* ---- 历史 ---- */
  State.prototype.pushHistory = function (entry) {
    this.history.push(entry);
    var limit = 250;
    if (this.history.length > limit) this.history.shift();
  };

  /* ---- 成就 ---- */
  State.prototype.grantAchievement = function (id) {
    this.achievements[id] = true;
    this.persistent.set('achievements.' + id, true);
  };

  /* ---- 已读标记（用于「跳过未读文本」判断） ---- */
  State.prototype.markSeen = function (key) {
    this.persistent.set('seen.' + key, true);
  };
  State.prototype.hasSeen = function (key) {
    return !!this.persistent.get('seen.' + key);
  };

  /* --------------------------------------------------------------------------
     快照：用于存档与回滚
     -------------------------------------------------------------------------- */

  /**
   * 生成可序列化的舞台快照。
   *
   * 两个必须注意的点：
   *   1. 立绘必须保留 visible —— 之前漏了这个字段，读档后所有立绘都被
   *      rebuild() 的 `if (!s.visible) return` 跳过，表现为「读档后没有立绘」。
   *   2. cg 数组里存着 DOM 引用（el），不能直接 JSON 序列化，只取名字/path。
   */
  State.prototype.snapshot = function () {
    var sprites = {};
    for (var code in this.sprites) {
      var s = this.sprites[code];
      sprites[code] = {
        expr: s.expr,
        path: s.path || null,
        pos: s.pos,
        zoom: s.zoom,
        xOffset: s.xOffset,
        yOffset: s.yOffset,
        visible: !!s.visible
      };
    }

    var cg = (this.cg || []).map(function (item) {
      var o = { name: item.name };
      if (item.path) o.path = item.path;
      if (item.type) o.type = item.type;
      if (item.color) o.color = item.color;
      return o;
    });

    var overlays = (this.overlays || []).map(function (o) {
      return typeof o === 'string' ? o : { name: o.name };
    });

    return {
      vars: JSON.parse(JSON.stringify(this.vars)),
      bg: this.bg ? JSON.parse(JSON.stringify(this.bg)) : null,
      cg: cg,
      sprites: sprites,
      layerFilters: JSON.parse(JSON.stringify(this.layerFilters)),
      overlays: overlays,
      camera: this.camera ? JSON.parse(JSON.stringify(this.camera)) : null,
      music: this.music ? JSON.parse(JSON.stringify(this.music)) : null,
      ambient: this.ambient ? JSON.parse(JSON.stringify(this.ambient)) : null,
      windowMode: this.windowMode,
      quickMenu: this.quickMenu,
      customUi: this.customUi,
      scriptBoxAlpha: this.scriptBoxAlpha
    };
  };

  State.prototype.restore = function (snap) {
    if (!snap) return;
    this.vars = Object.assign(Object.create(null), snap.vars || {});
    this.bg = snap.bg || null;
    this.cg = snap.cg || [];
    this.sprites = Object.assign(Object.create(null), snap.sprites || {});
    this.layerFilters = Object.assign(Object.create(null), snap.layerFilters || {});
    this.overlays = (snap.overlays || []).slice();
    this.music = snap.music || null;
    this.ambient = snap.ambient || null;
    this.windowMode = snap.windowMode || 'auto';
    this.quickMenu = snap.quickMenu !== false;
    this.customUi = snap.customUi !== false;
    this.scriptBoxAlpha = snap.scriptBoxAlpha == null ? 1 : snap.scriptBoxAlpha;
  };

  global.RPYState = {
    State: State,
    Persistent: Persistent
  };
})(window);