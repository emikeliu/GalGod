/* ==========================================================================
   engine/stage.js
   舞台渲染：等比缩放、图层管理、scene/show/hide、立绘变换、雨、覆盖层。
   ========================================================================== */
(function (global) {
  'use strict';

  var DESIGN_W = 1920;
  var DESIGN_H = 1080;

  function Stage(images, state) {
    this.images = images;
    this.state = state;

    this.el = document.getElementById('stage');
    this.outer = document.getElementById('stage-outer');
    this.masterLayer = document.getElementById('layer-master');
    this.bgLayer = document.getElementById('layer-bg');
    this.cgLayer = document.getElementById('layer-cg');
    this.rainbackLayer = document.getElementById('layer-rainback');
    this.rainfrontLayer = document.getElementById('layer-rainfront');
    this.spriteLayer = document.getElementById('layer-sprites');
    this.overlayLayer = document.getElementById('layer-overlay');
    this.screensLayer = document.getElementById('layer-screens');
    this.menusLayer = document.getElementById('layer-menus');
    this.movieLayer = document.getElementById('layer-movie');
    this.transitionLayer = document.getElementById('layer-transition');

    this.spriteEls = Object.create(null);
    this.bgEl = null;
    this.cgEls = Object.create(null);
    this.rainEls = Object.create(null);
    this.scale = 1;

    this.bindResize();
    this.bindMenuLayerPointerEvents();
  }

  /* --------------------------------------------------------------------------
     菜单层的点击穿透
     #layer-menus 是全屏层。若它恒定 pointer-events:auto，会盖住 HUD、
     吞掉按钮点击。这里用 MutationObserver 让 active 类跟随「有无菜单」自动切换，
     不必在每个菜单的 open/close 里手动维护。
     -------------------------------------------------------------------------- */
  Stage.prototype.bindMenuLayerPointerEvents = function () {
    if (!this.menusLayer) return;

    var sync = function () {
      var hasMenu = this.menusLayer.children.length > 0;
      this.menusLayer.classList.toggle('active', hasMenu);
    }.bind(this);

    sync();

    if (typeof global.MutationObserver === 'function') {
      this._menuObserver = new global.MutationObserver(sync);
      this._menuObserver.observe(this.menusLayer, { childList: true });
    }
  };

  /* --------------------------------------------------------------------------
     缩放
     -------------------------------------------------------------------------- */
  Stage.prototype.bindResize = function () {
    var self = this;
    this.resize = function () {
      var w = global.innerWidth;
      var h = global.innerHeight;
      var s = Math.min(w / DESIGN_W, h / DESIGN_H);
      self.scale = s;
      self.el.style.setProperty('--stage-transform',
        'translate(-50%, -50%) scale(' + s + ')');
      self.el.style.position = 'absolute';
      self.el.style.left = '50%';
      self.el.style.top = '50%';
      self.el.style.transform = 'translate(-50%, -50%) scale(' + s + ')';
      self.el.style.transformOrigin = 'center center';
    };
    global.addEventListener('resize', this.resize);
    this.resize();
  };

  /* --------------------------------------------------------------------------
     背景
     -------------------------------------------------------------------------- */
  Stage.prototype.setBackground = function (name) {
    var desc = name ? this.images.get(name) : null;
    this.clearBackground();

    if (!desc) {
      this.state.bg = null;
      return;
    }

    if (desc.type === 'solid') {
      var div = document.createElement('div');
      div.className = 'solid-bg';
      div.style.background = desc.color;
      this.bgLayer.appendChild(div);
      this.bgEl = div;
      this.state.bg = { name: name, type: 'solid', color: desc.color };
      return;
    }

    if (desc.type === 'ref') {
      return this.setBackground(desc.name);
    }

    var url = this.images.url(desc.path, 'image');
    if (!url) {
      this.state.bg = null;
      return;
    }

    var img = document.createElement('img');
    img.src = url;
    img.alt = '';
    img.draggable = false;
    img.className = 'bg-img';

    this.applyImageGeometry(img, desc);
    this.bgLayer.appendChild(img);
    this.bgEl = img;

    this.state.bg = {
      name: name,
      path: desc.path,
      fit: desc.fit || 'none',
      zoom: desc.zoom || 1,
      xalign: desc.xalign == null ? 0.5 : desc.xalign,
      yalign: desc.yalign == null ? 0.5 : desc.yalign
    };
  };

  Stage.prototype.clearBackground = function () {
    while (this.bgLayer.firstChild) this.bgLayer.removeChild(this.bgLayer.firstChild);
    this.bgEl = null;
  };

  /**
   * 图像几何：
   *   fit=cover  -> 等比放大到覆盖 1920x1080，再乘 zoom
   *   fit=stretch-> 拉满
   *   fit=none   -> 原始尺寸（可乘 zoom）
   * 变换原点与 Ren'Py 的 xalign/yalign 对齐。
   */
  Stage.prototype.applyImageGeometry = function (img, desc) {
    var zoom = desc.zoom || 1;
    var xa = desc.xalign == null ? 0.5 : desc.xalign;
    var ya = desc.yalign == null ? 0.5 : desc.yalign;

    img.style.position = 'absolute';
    img.style.left = (xa * 100) + '%';
    img.style.top = (ya * 100) + '%';
    img.style.transformOrigin = 'center center';
    img.style.maxWidth = 'none';
    img.style.maxHeight = 'none';

    if (desc.fit === 'stretch') {
      img.style.width = '100%';
      img.style.height = '100%';
      img.style.transform = 'translate(-50%, -50%)';
      return;
    }

    if (desc.fit === 'cover') {
      /* 用 object-fit 让浏览器负责 cover，再叠加 zoom 与对齐 */
      img.style.width = DESIGN_W + 'px';
      img.style.height = DESIGN_H + 'px';
      img.style.objectFit = 'cover';
      img.style.objectPosition = (xa * 100) + '% ' + (ya * 100) + '%';
      img.style.transform =
        'translate(-50%, -50%) scale(' + zoom + ')';
      return;
    }

    /* none / 原始尺寸 */
    if (desc.width && desc.height) {
      img.style.width = desc.width + 'px';
      img.style.height = desc.height + 'px';
    }
    img.style.transform =
      'translate(-50%, -50%) scale(' + zoom + ')';
  };

  /* --------------------------------------------------------------------------
     CG / 立绘 / 其他 master 层图像
     -------------------------------------------------------------------------- */
  Stage.prototype.showCG = function (name, descOverride) {
    var desc = descOverride || this.images.get(name);
    if (!desc) return;

    if (desc.type === 'ref') return this.showCG(desc.name);

    if (desc.type === 'solid') {
      var div = document.createElement('div');
      div.className = 'solid-bg';
      div.style.background = desc.color;
      this.cgLayer.appendChild(div);
      this.state.cg.push({ name: name, type: 'solid', color: desc.color });
      return;
    }

    var url = this.images.url(desc.path, 'image');
    if (!url) return;

    var img = document.createElement('img');
    img.src = url;
    img.alt = '';
    img.draggable = false;
    this.applyImageGeometry(img, desc);
    this.cgLayer.appendChild(img);

    this.state.cg.push({
      name: name,
      path: desc.path,
      el: img,
      desc: desc
    });
  };

  Stage.prototype.hideCG = function (name) {
    var key = String(name || '').trim();
    var keep = [];
    for (var i = 0; i < this.state.cg.length; i++) {
      var item = this.state.cg[i];
      var matches = !key || item.name === key || item.name.indexOf(key + ' ') === 0 ||
                    (item.name.split(' ')[0] === key.split(' ')[0]);
      if (matches) {
        if (item.el && item.el.parentNode) item.el.parentNode.removeChild(item.el);
      } else {
        keep.push(item);
      }
    }
    this.state.cg = keep;
  };

  Stage.prototype.clearCG = function () {
    while (this.cgLayer.firstChild) this.cgLayer.removeChild(this.cgLayer.firstChild);
    this.state.cg = [];
  };

  /* --------------------------------------------------------------------------
     立绘
     结构：<div class="sprite-wrap"><img class="sprite"></div>
     wrap 负责定位与 x/y 偏移，img 负责 zoom（origin: bottom center）
     -------------------------------------------------------------------------- */
  Stage.prototype.showSprite = function (code, path, st, transition) {
    var url = this.images.url(path, 'image');
    if (!url) return;

    var existing = this.spriteEls[code];
    var img;

    if (existing) {
      /* 换表情：直接替换 src，位置变化用过渡 */
      img = existing.querySelector('img');
      var target = url;
      if (img.getAttribute('src') !== target) {
        this.applySpriteState(existing, st, transition);
        img.src = target;
        img.style.opacity = '0';
        img.style.transition = 'opacity ' + ((transition && transition.duration) || 0.5) + 's linear';
        void img.offsetWidth;
        img.style.opacity = '1';
      } else {
        this.applySpriteState(existing, st, transition);
      }
      return;
    }

    var wrap = document.createElement('div');
    wrap.className = 'sprite';
    wrap.dataset.code = code;

    img = document.createElement('img');
    img.src = url;
    img.alt = '';
    img.draggable = false;
    img.style.display = 'block';
    img.style.transformOrigin = 'bottom center';
    img.style.opacity = '1';

    wrap.appendChild(img);
    this.spriteLayer.appendChild(wrap);
    this.spriteEls[code] = wrap;

    this.applySpriteState(wrap, st, transition, true);
  };

  /**
   * 应用立绘几何。
   * x = pos 的 0~1 比例（相对 1920 宽），再加上 xOffset 像素
   * y = 底部对齐 + yOffset 像素（正值向下）
   * zoom 作用在 img 上，origin 为 bottom center
   */
  Stage.prototype.applySpriteState = function (wrap, st, transition, initial) {
    var align = this.alignOf(st.pos);
    var x = align * DESIGN_W + (st.xOffset || 0);
    var yOffset = st.yOffset || 0;
    var zoom = st.zoom == null ? 1 : st.zoom;

    var dur = (transition && transition.duration) || (initial ? 0.35 : 0.35);
    var kind = (transition && transition.kind) || 'dissolve';

    wrap.style.left = '0px';
    wrap.style.top = '0px';
    wrap.style.bottom = 'auto';
    wrap.style.transformOrigin = '0 0';

    if (kind === 'none') {
      wrap.style.transition = 'none';
    } else {
      wrap.style.transition =
        'transform ' + dur + 's ease, opacity ' + dur + 's ease';
    }

    /* 位移到 (x, 1080 + yOffset)，然后以图片底部中心对齐 */
    wrap.style.transform =
      'translate(' + x + 'px, ' + (DESIGN_H + yOffset) + 'px) ' +
      'translate(-50%, -100%)';

    var img = wrap.querySelector('img');
    if (img) {
      img.style.transformOrigin = 'bottom center';
      img.style.transform = 'scale(' + zoom + ')';
    }

    if (initial && kind !== 'none') {
      wrap.style.opacity = '0';
      void wrap.offsetWidth;
      wrap.style.opacity = '1';
    } else {
      wrap.style.opacity = '1';
    }
  };

  Stage.prototype.updateSprite = function (code, st, transition) {
    var wrap = this.spriteEls[code];
    if (!wrap) return;
    this.applySpriteState(wrap, st, transition);
  };

  Stage.prototype.hideSprite = function (code, transition) {
    var wrap = this.spriteEls[code];
    if (!wrap) return;
    var dur = (transition && transition.duration) || 0.5;
    if (!transition || transition.kind === 'none') {
      if (wrap.parentNode) wrap.parentNode.removeChild(wrap);
      delete this.spriteEls[code];
      return;
    }
    wrap.style.transition = 'opacity ' + dur + 's linear';
    void wrap.offsetWidth;
    wrap.style.opacity = '0';
    setTimeout(function () {
      if (wrap.parentNode) wrap.parentNode.removeChild(wrap);
      delete this.spriteEls[code];
    }.bind(this), dur * 1000 + 30);
  };

  Stage.prototype.playSpriteAction = function (code, action, ms) {
    var wrap = this.spriteEls[code];
    if (!wrap) return;
    var cls = action === 'shake' ? 'act-shake' : 'act-jump';
    wrap.classList.remove('act-shake', 'act-jump');
    void wrap.offsetWidth;
    wrap.classList.add(cls);
    setTimeout(function () {
      wrap.classList.remove(cls);
    }, ms || 300);
  };

  Stage.prototype.alignOf = function (pos) {
    if (typeof pos === 'number') return pos;
    var map = {
      left: 0.25, center: 0.5, right: 0.75,
      center_left: 0.33, center_right: 0.67,
      truecenter: 0.5,
      offscreenleft: -0.2, offscreenright: 1.2
    };
    return map[String(pos || 'center')] != null ? map[String(pos || 'center')] : 0.5;
  };

  /* --------------------------------------------------------------------------
     雨（effects/raineffect.rpy）
     -------------------------------------------------------------------------- */
  Stage.prototype.showRain = function (which, mode) {
    var self = this;
    mode = mode || 'scroll';
    var layer = which === 'back' ? this.rainbackLayer : this.rainfrontLayer;
    var key = which + ':' + mode;
    if (this.rainEls[key]) return;

    var sheets = which === 'back'
      ? [{ img: '_rain-short.png', dur: 0.32, delay: 0 }, { img: '_rain-medium.png', dur: 0.16, delay: 0 }]
      : [{ img: '_rain-medium.png', dur: 0.32, delay: 0 }, { img: '_rain-long.png', dur: 0.16, delay: 0 }];

    var container = document.createElement('div');
    container.className = 'rain-container';
    container.style.cssText = 'position:absolute;inset:0;overflow:hidden;pointer-events:none;';

    sheets.forEach(function (sh) {
      var url = self.images.url(sh.img, 'image');
      if (!url) return;
      var el = document.createElement('div');
      el.className = 'rain-sheet';
      el.style.backgroundImage = 'url("' + url + '")';
      el.style.opacity = '0.25';
      if (mode === 'scroll') {
        el.style.animation = 'rain-fall-' +
          (sh.dur > 0.2 ? 'slow' : 'fast') + ' ' + sh.dur + 's linear infinite';
      }
      container.appendChild(el);
    });

    layer.appendChild(container);
    this.rainEls[key] = container;
  };

  Stage.prototype.hideRain = function (which) {
    var keys = Object.keys(this.rainEls);
    for (var i = 0; i < keys.length; i++) {
      if (keys[i].indexOf(which + ':') === 0) {
        var el = this.rainEls[keys[i]];
        if (el.parentNode) el.parentNode.removeChild(el);
        delete this.rainEls[keys[i]];
      }
    }
  };

  /* --------------------------------------------------------------------------
     覆盖层（cinematic_black_overlay 等）
     -------------------------------------------------------------------------- */
  Stage.prototype.showOverlay = function (name) {
    if (name === 'cinematic_black_overlay') {
      var el = document.createElement('div');
      el.className = 'overlay-solid';
      el.style.background = '#000';
      el.style.opacity = '0';
      el.style.transition = 'opacity 2s linear';
      this.overlayLayer.appendChild(el);
      void el.offsetWidth;
      el.style.opacity = '1';
      this.state.overlays.push({ name: name, el: el });
      return;
    }
    /* 其他未知覆盖层：当作纯色/图像 */
    var desc = this.images.get(name);
    if (desc && desc.type === 'image') {
      var img = document.createElement('img');
      img.src = this.images.url(desc.path, 'image');
      img.className = 'overlay-solid';
      img.style.objectFit = 'cover';
      this.overlayLayer.appendChild(img);
      this.state.overlays.push({ name: name, el: img });
    }
  };

  Stage.prototype.clearOverlay = function (name) {
    var keep = [];
    for (var i = 0; i < this.state.overlays.length; i++) {
      var o = this.state.overlays[i];
      if (!name || o.name === name) {
        if (o.el && o.el.parentNode) o.el.parentNode.removeChild(o.el);
      } else {
        keep.push(o);
      }
    }
    this.state.overlays = keep;
  };

  /* --------------------------------------------------------------------------
     镜头（camera: 的 zoom / xpos / ypos）
     作用在 master 层，与舞台整体缩放互不影响。
     -------------------------------------------------------------------------- */
  Stage.prototype.setCamera = function (zoom, xpos, ypos, duration) {
    zoom = zoom == null ? 1 : zoom;
    xpos = xpos == null ? 0.5 : xpos;
    ypos = ypos == null ? 0.5 : ypos;

    this.camera = { zoom: zoom, xpos: xpos, ypos: ypos };

    var secs = duration || 0;
    this.masterLayer.style.transformOrigin =
      (xpos * 100) + '% ' + (ypos * 100) + '%';
    this.masterLayer.style.transition = secs
      ? 'transform ' + secs + 's ease'
      : 'none';
    this.masterLayer.style.transform =
      'scale(' + zoom + ') translate(' +
      ((0.5 - xpos) * 100) + '%, ' + ((0.5 - ypos) * 100) + '%)';

    if (this.state) this.state.camera = this.camera;
  };

  Stage.prototype.resetCamera = function () {
    this.masterLayer.style.transition = 'none';
    this.masterLayer.style.transform = 'none';
    this.masterLayer.style.transformOrigin = 'center center';
    this.camera = null;
    if (this.state) this.state.camera = null;
  };

  /* --------------------------------------------------------------------------
     滤镜
     -------------------------------------------------------------------------- */
  Stage.prototype.setFilter = function (kind) {
    this.masterLayer.classList.remove('filter-gray', 'filter-memory', 'filter-reset');
    if (kind === 'memory') this.masterLayer.classList.add('filter-memory');
    else if (kind === 'gray') this.masterLayer.classList.add('filter-gray');
    else if (kind === 'reset') this.masterLayer.classList.add('filter-reset');
    this.state.layerFilters.master = kind === 'reset' ? null : kind;
  };

  /* --------------------------------------------------------------------------
     从状态重建整个舞台（读档 / 回滚用）
     -------------------------------------------------------------------------- */
  Stage.prototype.rebuild = function () {
    var self = this;

    this.clearBackground();
    this.clearCG();
    this.clearOverlay();
    Object.keys(this.spriteEls).forEach(function (code) {
      var el = self.spriteEls[code];
      if (el.parentNode) el.parentNode.removeChild(el);
    });
    this.spriteEls = Object.create(null);
    this.hideRain('back');
    this.hideRain('front');

    if (this.state.bg) this.setBackground(this.state.bg.name);

    (this.state.cg || []).forEach(function (item) {
      self.showCG(item.name);
    });

    var sprites = this.state.sprites || {};
    Object.keys(sprites).forEach(function (code) {
      var s = sprites[code];
      if (!s.visible || !s.expr) return;

      var path = s.path;
      if (!path) {
        var actor = self.actors && self.actors.get(code);
        if (!actor) return;
        path = actor.expressions[s.expr];
      }
      if (!path) return;

      self.showSprite(code, path, s, { kind: 'none' });
    });

    /* 恢复镜头（camera 推拉） */
    if (this.state.camera) {
      var cam = this.state.camera;
      this.setCamera(cam.zoom, cam.xpos, cam.ypos, 0);
    }

    /* 恢复 HUD / 窗口等界面开关 */
    if (this.state.windowMode === 'hide') {
      /* 由 UI 层处理，这里不动 */
    }

    (this.state.overlays || []).forEach(function (o) {
      self.showOverlay(o.name);
    });

    var f = this.state.layerFilters.master;
    if (f) this.setFilter(f);
  };

  global.RPYStage = {
    Stage: Stage,
    DESIGN_W: DESIGN_W,
    DESIGN_H: DESIGN_H
  };
})(window);