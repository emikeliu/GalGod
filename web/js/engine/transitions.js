/* ==========================================================================
   engine/transitions.js
   转场与特效实现。
   Ren'Py 的 dissolve 是对「整个 master 层」做交叉淡化，这里通过
   在同一容器内先放旧快照、再淡出新元素的方式近似，避免依赖 html2canvas。
   ========================================================================== */
(function (global) {
  'use strict';

  function Transition(stage) {
    this.stage = stage;
    this.timers = [];
  }

  Transition.prototype.clearTimers = function () {
    this.timers.forEach(function (t) { clearTimeout(t); });
    this.timers = [];
  };

  Transition.prototype.wait = function (ms) {
    var self = this;
    return new Promise(function (resolve) {
      var t = setTimeout(function () { resolve(); }, ms);
      self.timers.push(t);
    });
  };

  /* --------------------------------------------------------------------------
     主入口：对某个容器应用转场
     @param {HTMLElement} container  图层容器
     @param {Function} mutate      在旧内容之上执行的新内容变更
     @param {object} spec          {kind, duration, color}
     @returns {Promise}
     -------------------------------------------------------------------------- */
  Transition.prototype.apply = function (container, mutate, spec) {
    var kind = (spec && spec.kind) || 'none';
    var dur = (spec && spec.duration);

    if (!container) { mutate(); return Promise.resolve(); }

    switch (kind) {
      case 'none':
      case null:
      case undefined:
        mutate();
        return Promise.resolve();

      case 'dissolve':
      case 'fadein':
        return this.crossFade(container, mutate, dur == null ? 0.5 : dur);

      case 'fade':
        return this.fadeThroughBlack(container, mutate, dur == null ? 0.5 : dur);

      case 'flash':
        mutate();
        return this.flash();

      case 'pixellate':
        mutate();
        return this.pixellate();

      case 'vpunch':
        mutate();
        return this.punch('v');

      case 'hpunch':
        mutate();
        return this.punch('h');

      case 'filter':
        this.applyFilter(spec.filter);
        return Promise.resolve();

      case 'forced_dissolve':
        /* 元素自身从透明到不透明 */
        mutate();
        return Promise.resolve();

      default:
        mutate();
        return Promise.resolve();
    }
  };

  /* --------------------------------------------------------------------------
     交叉淡化：克隆旧节点快照，插入新内容，然后旧快照淡出
     -------------------------------------------------------------------------- */
  Transition.prototype.crossFade = function (container, mutate, seconds) {
    var ms = Math.max(0, seconds * 1000);
    if (ms === 0) { mutate(); return Promise.resolve(); }

    /* 旧内容快照：克隆子节点并绝对定位覆盖 */
    var snapshot = container.cloneNode(true);
    snapshot.removeAttribute('id');
    snapshot.className = 'xfade-snapshot';
    snapshot.setAttribute('aria-hidden', 'true');
    snapshot.style.cssText =
      'position:absolute;inset:0;width:100%;height:100%;pointer-events:none;' +
      'z-index:2;opacity:1;transition:opacity ' + seconds + 's linear;';
    container.appendChild(snapshot);

    /* 新内容在快照之下 */
    mutate();

    /* 强制回流后开始淡出 */
    void snapshot.offsetWidth;
    snapshot.style.opacity = '0';

    var self = this;
    return new Promise(function (resolve) {
      var t = setTimeout(function () {
        if (snapshot.parentNode) snapshot.parentNode.removeChild(snapshot);
        resolve();
      }, ms + 30);
      self.timers.push(t);
    });
  };

  /* --------------------------------------------------------------------------
     经黑场过渡：淡出到黑 -> 变更 -> 淡入
     -------------------------------------------------------------------------- */
  Transition.prototype.fadeThroughBlack = function (container, mutate, seconds) {
    var stage = this.stage;
    var half = Math.max(0.05, seconds);
    var black = document.createElement('div');
    black.className = 'overlay-solid';
    black.style.background = '#000';
    black.style.opacity = '0';
    black.style.transition = 'opacity ' + half + 's linear';
    black.style.zIndex = '999';
    stage.overlayLayer.appendChild(black);

    var self = this;
    return new Promise(function (resolve) {
      void black.offsetWidth;
      black.style.opacity = '1';
      var t1 = setTimeout(function () {
        mutate();
        void black.offsetWidth;
        black.style.opacity = '0';
        var t2 = setTimeout(function () {
          if (black.parentNode) black.parentNode.removeChild(black);
          resolve();
        }, half * 1000 + 30);
        self.timers.push(t2);
      }, half * 1000 + 20);
      self.timers.push(t1);
    });
  };

  /* --------------------------------------------------------------------------
     flash = Fade(0.1, 0.0, 0.5, color="#fff")
     -------------------------------------------------------------------------- */
  Transition.prototype.flash = function () {
    var el = document.createElement('div');
    el.className = 'fx-flash run';
    this.stage.overlayLayer.appendChild(el);
    var self = this;
    return new Promise(function (resolve) {
      var t = setTimeout(function () {
        if (el.parentNode) el.parentNode.removeChild(el);
        resolve();
      }, 620);
      self.timers.push(t);
    });
  };

  Transition.prototype.pixellate = function () {
    var el = document.createElement('div');
    el.className = 'fx-pixellate run';
    this.stage.overlayLayer.appendChild(el);
    var self = this;
    return new Promise(function (resolve) {
      var t = setTimeout(function () {
        if (el.parentNode) el.parentNode.removeChild(el);
        resolve();
      }, 920);
      self.timers.push(t);
    });
  };

  Transition.prototype.punch = function (dir) {
    var cls = dir === 'v' ? 'fx-vpunch' : 'fx-hpunch';
    this.stage.el.classList.remove('fx-vpunch', 'fx-hpunch');
    void this.stage.el.offsetWidth;
    this.stage.el.classList.add(cls);
    var self = this;
    return new Promise(function (resolve) {
      var t = setTimeout(function () {
        self.stage.el.classList.remove(cls);
        resolve();
      }, 340);
      self.timers.push(t);
    });
  };

  /* --------------------------------------------------------------------------
     记忆 / 灰度滤镜（作用于 master 层）
     -------------------------------------------------------------------------- */
  Transition.prototype.applyFilter = function (kind) {
    var el = this.stage.masterLayer;
    if (!el) return;
    el.classList.remove('filter-gray', 'filter-memory', 'filter-reset');
    if (kind === 'memory') el.classList.add('filter-memory');
    else if (kind === 'gray') el.classList.add('filter-gray');
    else el.classList.add('filter-reset');

    if (this.stage.state) {
      this.stage.state.layerFilters.master = (kind === 'reset' ? null : kind);
    }
  };

  /* --------------------------------------------------------------------------
     元素级线性淡入（forced_dissolve(t)）
     -------------------------------------------------------------------------- */
  Transition.prototype.linearFadeIn = function (el, seconds) {
    if (!el) return Promise.resolve();
    el.style.opacity = '0';
    el.style.transition = 'opacity ' + seconds + 's linear';
    void el.offsetWidth;
    el.style.opacity = '1';
    return Promise.resolve();
  };

  global.RPYTransitions = {
    Transition: Transition
  };
})(window);