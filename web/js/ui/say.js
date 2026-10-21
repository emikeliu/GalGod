/* ==========================================================================
   ui/say.js
   对白：打字机、点击推进、名字框、自动/快进、历史记录。
   对应 screens/dialogue_screens.rpy 的 say 屏幕。
   ========================================================================== */
(function (global) {
  'use strict';

  var S = global.RPYStrings;

  function SayUI(app) {
    this.app = app;
    this.box = document.getElementById('textbox');
    this.namebox = document.getElementById('namebox');
    this.whoEl = document.getElementById('who');
    this.whatEl = document.getElementById('what');
    this.nextEl = document.getElementById('next-indicator');

    this.isWaiting = false;
    this.typing = false;
    this.fullText = '';
    this.shownChars = 0;
    this.timer = null;
    this.lastSay = null;
    this.resolve = null;
    this.visible = false;

    this.bindEvents();
  }

  /* --------------------------------------------------------------------------
     输入
     -------------------------------------------------------------------------- */
  SayUI.prototype.bindEvents = function () {
    var self = this;

    /* 点击推进（在 screens 层，避免菜单误触） */
    document.getElementById('layer-screens').addEventListener('click', function (e) {
      /* 选项层自己处理点击 */
      if (e.target.closest('.choice-layer')) return;
      /* HUD / 菜单 自己处理点击 */
      if (e.target.closest('.hud')) return;
      /* 调试面板打开时不推进 */
      if (self.app.isDebugOpen && self.app.isDebugOpen()) return;
      self.advance();
    });

    /* 空格 / 回车推进；Esc 打开菜单 */
    document.addEventListener('keydown', function (e) {
      if (self.app.isMenuOpen()) return;
      /* 调试面板优先消费按键 */
      if (self.app.isDebugOpen && self.app.isDebugOpen()) return;
      if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        self.advance();
      } else if (e.key === 'Escape') {
        e.preventDefault();
        self.app.openGameMenu();
      } else if (e.key === 'Control') {
        self.app.vm.setSkip(true);
      } else if (e.key === 'Tab') {
        e.preventDefault();
        self.app.toggleSkip();
      } else if (e.key === 'h' || e.key === 'H') {
        self.toggleHidden();
      } else if (e.key === 'v' || e.key === 'V') {
        self.app.toggleAuto();
      } else if (e.key === 'F1') {
        e.preventDefault();
        self.app.showHelp();
      }
    });

    document.addEventListener('keyup', function (e) {
      if (e.key === 'Control') self.app.vm.setSkip(false);
    });

    /* 滚轮方向与原作一致（screens/dialogue_screens.rpy）：
       mousedown_4（上滑） -> ShowMenu("history")
       mousedown_5（下滑） -> Return() 推进对话 */
    document.getElementById('layer-screens').addEventListener('wheel', function (e) {
      if (self.app.isMenuOpen()) return;
      if (self.app.isDebugOpen && self.app.isDebugOpen()) return;

      if (e.deltaY < 0) {
        /* 上滑：历史记录 */
        e.preventDefault();
        self.app.openHistory();
      } else if (e.deltaY > 0) {
        /* 下滑：推进对话 */
        e.preventDefault();
        if (self.isWaiting) self.advance();
      }
    }, { passive: false });
  };

  /* --------------------------------------------------------------------------
     显示一句对白
     -------------------------------------------------------------------------- */
  SayUI.prototype.show = function (op, vm) {
    var self = this;
    var app = this.app;

    return new Promise(function (resolve) {
      self.resolve = resolve;
      self.isWaiting = true;
      self.lastSay = { who: op.who, text: op.text };

      /* 角色名：用 display 控制，避免 [hidden] 被 flex 覆盖 */
      var whoName = app.resolveWho(op.who);
      if (whoName) {
        self.namebox.removeAttribute('hidden');
        self.namebox.style.display = 'flex';
        self.whoEl.textContent = whoName;
        self.namebox.style.color = app.whoColor(op.who);
      } else {
        self.namebox.setAttribute('hidden', '');
        self.namebox.style.display = 'none';
      }

      /* 正文 */
      self.fullText = op.text || '';
      self.shownChars = 0;
      self.whatEl.innerHTML = '';

      /* window auto：只有真正有对白时才显示对话框底板。
         剧本里 `window hide` 会把 mode 置为 hide，此时不弹底板。 */
      if (app.state.windowMode !== 'hide') self.showBox();

      /* 历史记录 */
      app.state.pushHistory({
        who: whoName || '',
        what: S.stripTags(self.fullText),
        voice: app.state.voice ? app.state.voice.path : null,
        rollbackIndex: app.vm.rollbackStack.length - 1
      });
      app.state.markSeen(app.vm.lastPc.label + ':' + (app.vm.lastPc.pc));

      var cps = Number(app.state.persistent.get('text_cps', 30)) || 30;
      if (vm && vm.skipMode) {
        self.finishTyping();
        self.showNextIndicator(true);
        /* 跳过模式：短延迟后自动推进 */
        setTimeout(function () {
          if (self.isWaiting) self.advance();
        }, 20);
        return;
      }

      self.typewrite(cps);
    });
  };

  /* --------------------------------------------------------------------------
     打字机
     -------------------------------------------------------------------------- */
  SayUI.prototype.typewrite = function (cps) {
    var self = this;
    this.typing = true;
    this.showNextIndicator(false);
    clearInterval(this.timer);

    if (!cps || cps <= 0) {
      this.finishTyping();
      return;
    }

    var delay = 1000 / cps;
    var total = this.fullText.length;

    this.timer = setInterval(function () {
      if (self.shownChars >= total) {
        self.finishTyping();
        return;
      }
      /* 每次推进 1 字符，低帧率下按时间补偿 */
      self.shownChars += 1;
      self.renderPartial();
      if (self.shownChars >= total) self.finishTyping();
    }, delay);
  };

  SayUI.prototype.renderPartial = function () {
    var partial = this.fullText.slice(0, this.shownChars);
    /* 保留未闭合标签的视觉一致性：只在完整标签处截断 */
    this.whatEl.innerHTML = S.renderText(partial, 33);
  };

  SayUI.prototype.finishTyping = function () {
    clearInterval(this.timer);
    this.timer = null;
    this.typing = false;
    this.shownChars = this.fullText.length;
    this.whatEl.innerHTML = S.renderText(this.fullText, 33);
    this.showNextIndicator(true);

    /* 自动模式：安排下一句 */
    if (this.app.vm.autoMode) {
      this.app.vm.scheduleAuto();
    }
  };

  /* --------------------------------------------------------------------------
     推进：未打完 -> 补全；已打完 -> 下一句
     -------------------------------------------------------------------------- */
  SayUI.prototype.advance = function () {
    if (!this.isWaiting) return;

    if (this.typing) {
      this.finishTyping();
      return;
    }

    /* hard pause 期间不可推进 */
    var vm = this.app.vm;
    if (vm.waiting === 'pause' && vm._pauseResolve) {
      vm._pauseResolve();
      return;
    }

    this.isWaiting = false;
    this.showNextIndicator(false);
    var r = this.resolve;
    this.resolve = null;
    if (r) r();
  };

  /* --------------------------------------------------------------------------
     显示 / 隐藏
     -------------------------------------------------------------------------- */
  SayUI.prototype.showBox = function () {
    this.visible = true;
    this.box.classList.remove('hidden');
  };

  SayUI.prototype.hideBox = function () {
    this.visible = false;
    this.box.classList.add('hidden');
  };

  SayUI.prototype.setWindowMode = function (mode) {
    if (mode === 'hide') {
      this.hideBox();
    } else if (mode === 'show') {
      this.showBox();
    } else {
      /* auto：有对白时显示，由 show() 控制 */
      if (!this.isWaiting) this.hideBox();
    }
  };

  SayUI.prototype.hideImmediate = function () {
    this.isWaiting = false;
    this.typing = false;
    clearInterval(this.timer);
    this.timer = null;
    this.showNextIndicator(false);
    if (this.resolve) {
      var r = this.resolve;
      this.resolve = null;
      r();
    }
  };

  SayUI.prototype.showNextIndicator = function (on) {
    this.nextEl.hidden = !on;
  };

  SayUI.prototype.toggleHidden = function () {
    this.hidden = !this.hidden;
    this.box.style.visibility = this.hidden ? 'hidden' : 'visible';
  };

  /* --------------------------------------------------------------------------
     更新透明度（设置项 dialogue_box_alpha）
     -------------------------------------------------------------------------- */
  SayUI.prototype.applyAlpha = function () {
    var a = Number(this.app.state.persistent.get('dialogue_box_alpha', 0.7));
    this.box.style.opacity = a;
  };

  global.RPYSayUI = {
    SayUI: SayUI
  };
})(window);