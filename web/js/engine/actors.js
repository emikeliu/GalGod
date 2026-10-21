/* ==========================================================================
   engine/actors.js
   对应 config/character_config.rpy 的 CHARACTERS_CONFIG + character_core.rpy 的 Actor。
   立绘变换顺序（关键）：
     1. 以底部居中为锚点定位到 pos（left/center/right 或 0~1 数值）
     2. 施加 y_offset（1080 坐标系下的像素，不随 zoom 缩放）
     3. 施加 x_offset
     4. 施加 zoom（以 bottom center 为原点）
   CSS 实现为： left: 50% + translateX(-50% + xoffset) + translateY(...) 与 scale()
   为避免 translate/scale 顺序歧义，这里用嵌套两层元素分别承担。
   ========================================================================== */
(function (global) {
  'use strict';

  /* 全局默认（config/options.rpy 的 global_actor_settings） */
  var GLOBAL = { zoom: 0.6, y_offset: 1250 };

  var POS = {
    left: 0.25,
    center: 0.5,
    center_left: 0.33,
    center_right: 0.67,
    right: 0.75,
    offscreenleft: -0.2,
    offscreenright: 1.2,
    truecenter: 0.5
  };

  function Actors(characterConfig, stage, images, state) {
    this.config = characterConfig || {};
    this.stage = stage;
    this.images = images;
    this.state = state;
    this.actors = Object.create(null);
    this.build();
  }

  Actors.prototype.build = function () {
    for (var code in this.config) {
      var cfg = this.config[code];
      this.actors[code] = new Actor(code, cfg, this);
    }
    return this;
  };

  /* --------------------------------------------------------------------------
     Actor
     -------------------------------------------------------------------------- */
  function Actor(code, cfg, owner) {
    this.code = code;
    this.name = cfg.name || code;
    this.color = cfg.color || '#ffffff';
    this.voiceTag = cfg.voice_tag || null;
    this.expressions = cfg.expressions || {};
    this.styleConfig = cfg.style || {};
    this.defaultZoom = pick(this.styleConfig.zoom, GLOBAL.zoom);
    this.defaultYOffset = pick(this.styleConfig.y_offset, GLOBAL.y_offset);
    this.owner = owner;
  }

  function pick(v, dflt) {
    return (v === undefined || v === null) ? dflt : v;
  }

  /** 数值参数：undefined/null/NaN 时回落默认值 */
  function asNumber(v, dflt) {
    if (v === undefined || v === null || v === '') return dflt;
    var n = parseFloat(v);
    return isNaN(n) ? dflt : n;
  }

  Actor.prototype.stateOf = function () {
    var st = this.owner.state;
    if (!st.sprites[this.code]) {
      st.sprites[this.code] = {
        expr: null,
        pos: 'center',
        zoom: this.defaultZoom,
        xOffset: 0,
        yOffset: this.defaultYOffset,
        visible: false
      };
    }
    return st.sprites[this.code];
  };

  /**
   * show(expression, pos=..., zoom=..., y_offset=..., x_offset=..., transition=...)
   * 与 character_core.rpy 语义一致：pos 只在显式给出时更新并记忆。
   */
  Actor.prototype.show = function (expression, opts) {
    opts = opts || {};
    var s = this.stateOf();
    var self = this;

    s.expr = expression;
    if (opts.pos !== undefined && opts.pos !== null) {
      s.pos = opts.pos;
    }
    if (opts.zoom !== undefined && opts.zoom !== null) s.zoom = asNumber(opts.zoom, s.zoom);
    if (opts.yOffset !== undefined && opts.yOffset !== null) s.yOffset = asNumber(opts.yOffset, s.yOffset);
    if (opts.xOffset !== undefined && opts.xOffset !== null) s.xOffset = asNumber(opts.xOffset, s.xOffset);
    s.visible = true;

    var path = this.expressions[expression];
    if (!path) {
      this.owner.diag && this.owner.diag({
        kind: 'MISSING_EXPRESSION',
        message: '角色 ' + this.code + ' 没有表情: ' + expression
      });
      return;
    }

    /* 把真实图片路径一并记入状态，读档重建时不依赖表情表查找 */
    s.path = path;

    var transition = opts.transition === undefined ? { kind: 'dissolve', duration: 0.5 } : opts.transition;
    this.owner.stage.showSprite(this.code, path, s, transition);
    return self;
  };

  Actor.prototype.hide = function (opts) {
    opts = opts || {};
    var s = this.stateOf();
    s.visible = false;
    s.expr = null;
    var transition = opts.transition === undefined ? { kind: 'dissolve', duration: 0.5 } : opts.transition;
    this.owner.stage.hideSprite(this.code, transition);
  };

  /** reset_position()：清空位置/缩放/偏移回到默认 */
  Actor.prototype.resetPosition = function () {
    var s = this.stateOf();
    s.zoom = this.defaultZoom;
    s.yOffset = this.defaultYOffset;
    s.xOffset = 0;
    s.pos = 'center';
    if (s.visible && s.expr) {
      this.owner.stage.updateSprite(this.code, s, { kind: 'dissolve', duration: 0.35 });
    }
  };

  /** act(anim_shake | anim_jump)：在当前位置上叠加动画 */
  Actor.prototype.act = function (actionName) {
    var s = this.stateOf();
    if (!s.visible) return;
    if (actionName === 'anim_shake') {
      this.owner.stage.playSpriteAction(this.code, 'shake', 200);
    } else if (actionName === 'anim_jump') {
      this.owner.stage.playSpriteAction(this.code, 'jump', 300);
    }
  };

  Actor.prototype.setPosition = function (pos) {
    var s = this.stateOf();
    s.pos = pos;
  };

  /* --------------------------------------------------------------------------
     Actors 容器
     -------------------------------------------------------------------------- */
  Actors.prototype.get = function (code) {
    return this.actors[code] || null;
  };

  Actors.prototype.has = function (code) {
    return !!this.actors[code];
  };

  /** 把 pos 名字或数值转成 0~1 的 xalign */
  Actors.prototype.posToAlign = function (pos) {
    if (typeof pos === 'number') return pos;
    var key = String(pos || 'center').trim();
    if (POS[key] !== undefined) return POS[key];
    /* "center+250" 之类的表达式暂不支持，退化到 center */
    return 0.5;
  };

  /** reset_position 全体 */
  Actors.prototype.resetAll = function () {
    for (var code in this.actors) {
      this.actors[code].resetPosition();
    }
  };

  global.RPYActors = {
    Actors: Actors,
    Actor: Actor,
    GLOBAL: GLOBAL,
    POS: POS
  };
})(window);