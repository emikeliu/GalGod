/* ==========================================================================
   ui/centered_text.js
   两种居中文本：
   1. centered "..."        —— 黑底全屏居中，点击继续（对应 say 的 centered 变体）
   2. call screen centered_left_text("...")
      —— 左上区域，25 cps 打字机，点击先补全再返回（对应 resources.rpy 的 screen）
   ========================================================================== */
(function (global) {
  'use strict';

  var S = global.RPYStrings;

  function CenteredUI(app) {
    this.app = app;
    this.el = document.getElementById('centered-text');
    this.mode = null;
    this.typing = false;
    this.timer = null;
    this.fullText = '';
    this.shown = 0;
    this.onDone = null;
    this.resolve = null;
    this.isFinished = false;

    this.bind();
  }

  CenteredUI.prototype.bind = function () {
    var self = this;
    var layer = document.getElementById('layer-screens');

    layer.addEventListener('click', function (e) {
      if (self.el.hidden) return;
      if (e.target.closest('.choice-layer')) return;
      if (self.app.isDebugOpen && self.app.isDebugOpen()) return;
      self.advance();
    });

    document.addEventListener('keydown', function (e) {
      if (self.el.hidden) return;
      if (self.app.isDebugOpen && self.app.isDebugOpen()) return;
      if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        self.advance();
      }
    });
  };

  /**
   * @param {string} text
   * @param {object} opts {mode:'center'|'left', cps, onDone}
   */
  CenteredUI.prototype.show = function (text, opts) {
    var self = this;
    opts = opts || {};
    this.mode = opts.mode || (opts.centered ? 'center' : 'left');
    this.onDone = opts.onDone || null;
    this.fullText = text || '';
    this.shown = 0;
    this.isFinished = false;

    /* 样式：left 模式对应 centered_left_text 的位置 */
    if (this.mode === 'left') {
      this.el.style.left = '15%';
      this.el.style.top = '40%';
      this.el.style.width = '1200px';
      this.el.style.fontSize = '36px';
      this.el.style.textAlign = 'left';
      this.el.style.transform = 'none';
    } else {
      this.el.style.left = '50%';
      this.el.style.top = '50%';
      this.el.style.width = 'auto';
      this.el.style.maxWidth = '1600px';
      this.el.style.fontSize = '40px';
      this.el.style.textAlign = 'center';
      this.el.style.transform = 'translate(-50%, -50%)';
    }

    this.el.hidden = false;
    this.el.innerHTML = '';

    var cps = opts.cps;
    return new Promise(function (resolve) {
      self.resolve = resolve;
      if (!cps) {
        self.el.innerHTML = S.renderText(self.fullText, 36);
        self.isFinished = true;
        return;
      }
      self.typewrite(cps);
    });
  };

  CenteredUI.prototype.typewrite = function (cps) {
    var self = this;
    this.typing = true;
    clearInterval(this.timer);
    var delay = 1000 / cps;
    var total = this.fullText.length;

    if (!total) { this.finish(); return; }

    this.timer = setInterval(function () {
      if (self.shown >= total) { self.finish(); return; }
      self.shown++;
      self.el.innerHTML = S.renderText(self.fullText.slice(0, self.shown), 36);
      if (self.shown >= total) self.finish();
    }, delay);
  };

  CenteredUI.prototype.finish = function () {
    clearInterval(this.timer);
    this.timer = null;
    this.typing = false;
    this.shown = this.fullText.length;
    this.el.innerHTML = S.renderText(this.fullText, 36);
    this.isFinished = true;
  };

  CenteredUI.prototype.advance = function () {
    if (this.el.hidden) return false;

    /* 对应 resources.rpy：未打完 -> 立即补全；已打完 -> Return() */
    if (!this.isFinished) {
      this.finish();
      return true;
    }

    this.hide();
    if (this.onDone) {
      var fn = this.onDone;
      this.onDone = null;
      fn();
    }
    if (this.resolve) {
      var r = this.resolve;
      this.resolve = null;
      r();
    }
    return true;
  };

  CenteredUI.prototype.hide = function () {
    clearInterval(this.timer);
    this.timer = null;
    this.typing = false;
    this.el.hidden = true;
    this.el.innerHTML = '';
  };

  CenteredUI.prototype.isActive = function () {
    return !this.el.hidden;
  };

  global.RPYCenteredUI = {
    CenteredUI: CenteredUI
  };
})(window);