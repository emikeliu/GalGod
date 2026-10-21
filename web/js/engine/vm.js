/* ==========================================================================
   engine/vm.js
   Ren'Py 脚本虚拟机。
   - 帧栈：call/return
   - 指令流：顺序执行 + 条件跳转
   - 等待：say / pause / menu / callScreen 会把 VM 挂起（yield）
   - 回滚：在每个 yield 点压入轻量快照
   ========================================================================== */
(function (global) {
  'use strict';

  var Expr = global.RPYExpr;

  /* --------------------------------------------------------------------------
     构造函数
     -------------------------------------------------------------------------- */
  function VM(deps) {
    this.program = deps.program;
    this.state = deps.state;
    this.images = deps.images;
    this.actors = deps.actors;
    this.stage = deps.stage;
    this.audio = deps.audio;
    this.transitions = deps.transitions;
    this.ui = deps.ui;               /* {say, centered, choice, movie} */
    this.transition = deps.transitions;

    this.waiting = null;             /* 'say' | 'pause' | 'menu' | 'screen' | 'movie' */
    this.paused = false;
    this.diagnostics = this.program.diagnostics;

    /* 执行链代际令牌：abort() 递增，旧链恢复时据此自行退出。
       必须在构造函数里初始化为数字，否则 run() 里
       `gen !== self.generation` 会因 undefined 而恒为真，链路一步都不跑。 */
    this.generation = 0;
    this._running = false;
    this._runningPromise = null;

    this.rollbackStack = [];
    this.rollbackLimit = 100;

    this.autoMode = false;
    this.skipMode = false;
    this.skipUnread = false;
    this.autoTimer = null;

    this.lastPc = { label: null, pc: 0 };

    /**
     * 挂起点：yield 型指令在执行前会把 frame.pc++ 提前推进，
     * 因此「存档位置」应该记录挂起的那条指令，而不是之后的下一条。
     * 这里保存 { label, pc } 作为读档的落点。
     */
    this.waitingAt = null;
  }

  /* --------------------------------------------------------------------------
     便捷访问
     -------------------------------------------------------------------------- */
  VM.prototype.label = function (name) {
    return this.program.labels[name] || null;
  };

  VM.prototype.currentFrame = function () {
    return this.frames[this.frames.length - 1] || null;
  };

  /**
   * 剧本里的 UI 开关变化后，通知外层刷新 HUD。
   * custom_ui / quick_menu 在 screens/ui.rpy 与 dialogue_screens.rpy 中控制显示。
   */
  VM.prototype.syncUiFlags = function () {
    if (this.onUiFlagChange) this.onUiFlagChange();
  };

  VM.prototype.diag = function (kind, op, msg) {
    this.diagnostics.push({
      kind: kind,
      file: op ? op.file : '',
      line: op ? op.line : 0,
      text: '',
      message: msg
    });
  };

  /* --------------------------------------------------------------------------
     启动 / 跳转
     -------------------------------------------------------------------------- */
  /**
   * 应用 script 里的 `default` 初始值。
   * 从主菜单直接跳章节时必须手动调用一次，否则 true_end_flag 这类
   * 用于 if 判断的变量是 undefined。
   */
  VM.prototype.applyDefaults = function () {
    var self = this;
    var defs = (this.program.defaults || []);

    defs.forEach(function (d) {
      if (self.state.getVar(d.name) !== undefined) return;

      var raw = String(d.value || '').trim();
      if (raw === 'True') { self.state.setVar(d.name, true); return; }
      if (raw === 'False') { self.state.setVar(d.name, false); return; }
      if (raw === 'None') { self.state.setVar(d.name, null); return; }
      if (/^-?\d+$/.test(raw)) { self.state.setVar(d.name, parseInt(raw, 10)); return; }
      if (/^-?\d*\.\d+$/.test(raw)) { self.state.setVar(d.name, parseFloat(raw)); return; }

      var s = global.RPYParser.asString(raw);
      if (s !== null) { self.state.setVar(d.name, s); return; }

      /* 其他表达式：尽力求值，失败就留空 */
      try {
        var ast = Expr.parse(raw, null);
        var v = Expr.evaluate(ast, self.exprContext({ file: d.file, line: d.line }));
        if (v !== undefined) self.state.setVar(d.name, v);
      } catch (e) { /* 忽略 */ }
    });
  };

  /**
   * 立即终止当前执行链（播放中 / 挂起中都可）。
   *
   * 关键：say / pause 等 yield 指令会让旧 Promise 一直悬着，
   * 此时 _running 仍为 true。若不显式作废旧链，新的 run() 会被
   * `if (this._running) return` 直接弹回 —— 表现就是跳转后黑屏。
   * 用 generation 令牌让旧链在恢复时自行退出。
   */
  VM.prototype.abort = function () {
    this.generation++;
    this._running = false;
    this._runningPromise = null;
    this.running = false;
    this.waiting = null;

    if (this._pauseTimer) {
      clearTimeout(this._pauseTimer);
      this._pauseTimer = null;
    }
    this._pauseResolve = null;

    if (this.autoTimer) {
      clearTimeout(this.autoTimer);
      this.autoTimer = null;
    }
  };

  VM.prototype.start = function (labelName) {
    this.abort();
    this.frames = [];
    this.applyDefaults();

    var name = labelName || 'start';
    if (!this.label(name)) {
      /* 退化到第一个非合成 label */
      var keys = Object.keys(this.program.labels).filter(function (k) {
        return !this.program.labels[k].synthetic;
      }, this);
      this.diag('MISSING_START', null, '找不到 label: ' + name + '，退化到 ' + keys[0]);
      name = keys[0];
      if (!name) return Promise.resolve();
    }
    this.frames.push({ label: name, pc: 0 });
    this.running = true;
    return this.run();
  };

  VM.prototype.jumpTo = function (labelName) {
    if (!this.label(labelName)) {
      this.diag('MISSING_LABEL', null, 'jump 目标不存在: ' + labelName);
      return Promise.resolve();
    }
    this.abort();
    this.frames = [{ label: labelName, pc: 0 }];
    this.rollbackStack = [];
    this.lastPc = { label: labelName, pc: 0 };
    this.applyDefaults();
    this.running = true;
    return this.run();
  };

  /* --------------------------------------------------------------------------
     主循环
     -------------------------------------------------------------------------- */
  /**
   * 主循环。
   *
   * 关键语义：一条 yield 型指令（say / pause / callScreen / menu）返回的
   * Promise 在「玩家推进」之前不会 resolve，这本身就是 VM 的挂起机制。
   * 因此这里不需要额外的 'wait' 返回值 —— Promise resolve 即代表继续执行。
   *
   * generation 令牌：abort() 会让旧链的 gen 失配，旧 Promise 一恢复就静默退出，
   * 不会与新链抢帧栈、也不会误把新链的 _running 复位。
   */
  VM.prototype.run = function () {
    if (!this.running) return Promise.resolve();
    /* 已有循环在跑：直接返回，避免重入把帧栈搅乱 */
    if (this._running) return this._runningPromise || Promise.resolve();

    var self = this;
    var gen = this.generation;
    this._running = true;

    this._runningPromise = (function loop() {
      /* 被 abort（跳转 / 重开 / 回主菜单）——旧链必须立刻退出 */
      if (gen !== self.generation) return Promise.resolve();
      if (!self.running) return Promise.resolve();

      var frame = self.currentFrame();
      if (!frame) { self.running = false; return Promise.resolve(); }

      var lab = self.label(frame.label);
      if (!lab) {
        self.diag('MISSING_LABEL', null, '帧指向不存在的 label: ' + frame.label);
        self.running = false;
        return Promise.resolve();
      }

      if (frame.pc >= lab.ops.length) {
        /* label 末尾：弹出帧 */
        self.frames.pop();
        if (!self.frames.length) {
          self.running = false;
          if (self.onEnd) self.onEnd();
        }
        return loop();
      }

      var op = lab.ops[frame.pc];
      self.lastPc = { label: frame.label, pc: frame.pc };

      var result;
      try {
        result = self.exec(op, frame);
        /* 每条指令后同步一次 UI 开关（custom_ui / quick_menu）。
           不能只依赖 onIdle —— yield 型指令会让 run() 长期挂起，
           onIdle 永远不会触发，HUD 就一直停在初始隐藏状态。 */
        self.syncUiFlags();
      } catch (err) {
        self.diag('RUNTIME_ERROR', op,
          '执行 ' + op.op + ' 出错: ' + (err && err.message ? err.message : err));
        frame.pc++;
        return loop();
      }

      /* 同步指令：继续下一条 */
      if (!Expr.isThenable(result)) return loop();

      /* 异步指令：等它 resolve（玩家推进 / 计时结束 / 选项被选）后继续 */
      return result.then(function () {
        /* 等待期间被 abort：这一条已作废，静默退出 */
        if (gen !== self.generation) return Promise.resolve();
        if (!self.running) return Promise.resolve();
        return loop();
      }, function (err) {
        if (gen !== self.generation) return Promise.resolve();
        self.diag('RUNTIME_ERROR', op,
          '异步指令失败: ' + (err && err.message ? err.message : err));
        frame.pc++;
        return loop();
      });
    })();

    var myPromise = this._runningPromise;

    return myPromise.then(function () {
      /* 只有「仍然属于自己这条链」时才清理标志位，
         否则会把新链的 _running / _runningPromise 误清掉 */
      if (self._runningPromise === myPromise) {
        self._running = false;
        self._runningPromise = null;
      }
      if (self.onIdle) self.onIdle();
    });
  };

  /* --------------------------------------------------------------------------
     resume：从 say / pause / menu 挂起处继续
     -------------------------------------------------------------------------- */
  VM.prototype.resume = function () {
    if (this.paused) return Promise.resolve();
    this.waiting = null;
    return this.run();
  };

  /* --------------------------------------------------------------------------
     单条指令执行
     返回：undefined 表示继续，Promise<'wait'> 表示挂起
     -------------------------------------------------------------------------- */
  VM.prototype.exec = function (op, frame) {
    var self = this;

    switch (op.op) {

      /* ---- 对白 ---- */
      case 'say':
        this.waitingAt = { label: frame.label, pc: frame.pc };
        frame.pc++;
        this.pushRollback('say');
        return this.ui.say.show(op, this);

      /* ---- 居中文本 ----
         该模式下不显示对话框，隐藏背景避免压住文字（对应原作 window hide） */
      case 'centered':
        this.waitingAt = { label: frame.label, pc: frame.pc };
        frame.pc++;
        this.pushRollback('centered');
        this.ui.say.hideBox();
        return this.ui.centered.show(op.text, { centered: true });

      /* ---- 场景 ---- */
      case 'scene':
        frame.pc++;
        return this.doScene(op);

      /* ---- show ---- */
      case 'show':
        frame.pc++;
        return this.doShow(op);

      /* ---- hide ---- */
      case 'hide':
        frame.pc++;
        return this.doHide(op);

      /* ---- show layer ---- */
      case 'showLayer':
        frame.pc++;
        if (op.transition && op.transition.kind === 'filter') {
          this.stage.setFilter(op.transition.filter);
        } else if (op.transition) {
          this.stage.setFilter('reset');
        }
        return undefined;

      /* ---- camera（ATL 镜头推拉） ---- */
      case 'camera':
        frame.pc++;
        this.stage.setCamera(op.zoom, op.xpos, op.ypos, op.duration);
        return undefined;

      /* ---- 屏幕 ---- */
      case 'showScreen':
        frame.pc++;
        return this.doShowScreen(op);

      case 'hideScreen':
        frame.pc++;
        if (op.screen === 'ed_player') return this.ui.movie.hide();
        return undefined;

      case 'callScreen':
        this.waitingAt = { label: frame.label, pc: frame.pc };
        frame.pc++;
        this.pushRollback('screen');
        /* centered_left_text 不需要对话框，隐藏底板 */
        if (op.screen === 'centered_left_text') this.ui.say.hideBox();
        return this.doCallScreen(op);

      /* ---- 音频 ---- */
      case 'play':
        frame.pc++;
        if (op.channel === 'movie') return undefined;
        this.audio.play(op.channel, op.path, op.opts);
        return undefined;

      case 'stop':
        frame.pc++;
        this.audio.stop(op.channel, op.opts);
        return undefined;

      case 'queue':
        frame.pc++;
        /* queue 简化处理：直接 play */
        this.audio.play(op.channel, op.path, op.opts);
        return undefined;

      case 'voice':
        frame.pc++;
        var tag = this.voiceTagFor(op.path);
        this.audio.playVoice(op.path, tag);
        return undefined;

      /* ---- 等待 ---- */
      case 'pause':
        frame.pc++;
        this.pushRollback('pause');
        return this.doPause(op);

      /* ---- 转场 ---- */
      case 'with':
        frame.pc++;
        return this.doWith(op);

      /* ---- 窗口 ---- */
      case 'window':
        frame.pc++;
        this.doWindow(op);
        return undefined;

      /* ---- $ 语句 ---- */
      case 'py':
        frame.pc++;
        /* $ 可能改动 custom_ui / quick_menu，HUD 需要立刻响应 */
        return this.doPython(op, frame);

      /* ---- 流程 ---- */
      case 'jump':
        if (op.targetLabel) {
          var lab = this.label(op.targetLabel);
          if (!lab) {
            this.diag('MISSING_LABEL', op, 'jump 目标不存在: ' + op.targetLabel);
            frame.pc++;
            return undefined;
          }
          this.frames = [{ label: op.targetLabel, pc: 0 }];
          return undefined;
        }
        frame.pc = op.target;
        return undefined;

      case 'jumpUnless':
        if (!this.evalCond(op.cond, op)) {
          frame.pc = op.target;
        } else {
          frame.pc++;
        }
        return undefined;

      case 'call':
        var callee = this.label(op.targetLabel);
        if (!callee) {
          this.diag('MISSING_LABEL', op, 'call 目标不存在: ' + op.targetLabel);
          frame.pc++;
          return undefined;
        }
        frame.pc++;
        this.frames.push({ label: op.targetLabel, pc: 0 });
        return undefined;

      case 'return':
        this.frames.pop();
        if (!this.frames.length) {
          this.running = false;
          if (this.onEnd) this.onEnd();
        }
        return undefined;

      /* ---- 菜单 ---- */
      case 'menu':
        /* menu 不推进 pc：由 doMenu 内部跳到选中项 */
        this.waitingAt = { label: frame.label, pc: frame.pc };
        this.pushRollback('menu');
        return this.doMenu(op, frame);

      case 'labelMarker':
        frame.pc++;
        return undefined;

      default:
        this.diag('UNKNOWN_OP', op, '未知指令: ' + op.op);
        frame.pc++;
        return undefined;
    }
  };

  /* --------------------------------------------------------------------------
     scene / show / hide
     -------------------------------------------------------------------------- */
  VM.prototype.doScene = function (op) {
    var self = this;
    var transition = op.transition;

    var mutate = function () {
      self.stage.clearCG();
      self.state.cg = [];
      self.stage.clearOverlay();
      self.state.overlays = [];
      /* scene 会清空所有立绘 */
      Object.keys(self.state.sprites).forEach(function (code) {
        self.state.sprites[code].visible = false;
        self.state.sprites[code].expr = null;
      });
      var sprites = Object.keys(self.stage.spriteEls);
      sprites.forEach(function (code) {
        var el = self.stage.spriteEls[code];
        if (el.parentNode) el.parentNode.removeChild(el);
        delete self.stage.spriteEls[code];
      });

      if (op.image) self.stage.setBackground(op.image);
      else self.stage.setBackground(null);
    };

    /* 特写 CG 类背景（cg / sdcg）用 CG 图层而非背景图层 */
    if (op.image && /^(cg|sdcg)\b/.test(op.image)) {
      mutate = function () {
        self.stage.setBackground(null);
        self.stage.clearCG();
        self.state.cg = [];
        self.stage.showCG(op.image);
      };
    }

    if (!transition) { mutate(); return undefined; }

    if (transition.kind === 'forced_dissolve') {
      mutate();
      var bg = this.stage.bgEl;
      var cg = this.state.cg.length ? this.state.cg[this.state.cg.length - 1].el : null;
      var el = cg || bg;
      if (el) this.transitions.linearFadeIn(el, transition.duration);
      return undefined;
    }

    return this.transitions.apply(this.stage.masterLayer, mutate, transition);
  };

  VM.prototype.doShow = function (op) {
    var name = String(op.image || '').trim();
    if (!name) return undefined;

    /* 雨效 */
    if (/^rain(back|front)\b/.test(name)) {
      var which = /^rainback/.test(name) ? 'back' : 'front';
      var mode = /static/.test(name) ? 'static' : 'scroll';
      this.stage.showRain(which, mode);
      return undefined;
    }

    /* 覆盖层 */
    if (this.images.has(name) === false && /^cinematic_/.test(name)) {
      this.stage.showOverlay(name);
      return undefined;
    }

    /* 角色立绘：NAME 是 actor code，属性是表情 */
    var desc = this.images.get(name);
    var parts = name.split(' ');

    /* 先看是否是角色 + 表情 */
    if (this.actors.has(parts[0])) {
      var actor = this.actors.get(parts[0]);
      var expr = parts.slice(1).join(' ') || null;
      if (expr && actor.expressions[expr]) {
        var opts = { transition: op.transition };
        this.applyAtList(op.at, opts);
        actor.show(expr, opts);
        return undefined;
      }
    }

    if (!desc) {
      this.diag('UNKNOWN_IMAGE', op, '未定义的图像: ' + name);
      return undefined;
    }

    /* cinematic_black_overlay 等等 */
    if (/^cinematic_/.test(name)) {
      this.stage.showOverlay(name);
      return undefined;
    }

    var self = this;
    var mutate = function () {
      self.stage.showCG(name);
    };
    if (!op.transition) { mutate(); return undefined; }
    return this.transitions.apply(this.stage.masterLayer, mutate, op.transition);
  };

  VM.prototype.applyAtList = function (atList, opts) {
    if (!atList) return;
    atList.forEach(function (a) {
      if (/^left$/.test(a)) opts.pos = 'left';
      else if (/^right$/.test(a)) opts.pos = 'right';
      else if (/^center$/.test(a)) opts.pos = 'center';
      else if (/^truecenter$/.test(a)) opts.pos = 'center';
      else if (/^offscreenleft$/.test(a)) opts.pos = -0.2;
      else if (/^offscreenright$/.test(a)) opts.pos = 1.2;
      else if (/^forced_dissolve/.test(a)) {
        var m = /\(([\d.]+)\)/.exec(a);
        opts.transition = { kind: 'forced_dissolve', duration: m ? parseFloat(m[1]) : 1 };
      }
    });
  };

  VM.prototype.doHide = function (op) {
    var name = String(op.image || '').trim();
    if (!name) return undefined;

    if (/^rain/.test(name)) {
      this.stage.hideRain(/^rainback/.test(name) ? 'back' : 'front');
      return undefined;
    }

    var parts = name.split(' ');
    if (this.actors.has(parts[0])) {
      this.actors.get(parts[0]).hide({ transition: op.transition });
      return undefined;
    }

    var self = this;
    var mutate = function () { self.stage.hideCG(name); };
    if (!op.transition) { mutate(); return undefined; }
    return this.transitions.apply(this.stage.masterLayer, mutate, op.transition);
  };

  VM.prototype.doShowScreen = function (op) {
    if (op.screen === 'ed_player') {
      var path = (op.args.positional || [])[0];
      var p = global.RPYParser.asString(path || '') || 'movies/ed.webm';
      return this.ui.movie.show(p);
    }
    /* 其他 screen：目前只有 centered_left_text 在 call screen 中使用 */
    return undefined;
  };

  VM.prototype.doCallScreen = function (op) {
    var self = this;

    if (op.screen === 'centered_left_text') {
      var raw = (op.args.positional || [])[0] || '';
      var text = global.RPYParser.asString(raw);
      if (text === null) text = '';
      return this.ui.centered.show(text, {
        mode: 'left',
        cps: 25,
        onDone: function () { self.resume(); }
      });
    }

    /* 未知 screen：立即当作已完成，避免卡死 */
    this.diag('UNKNOWN_SCREEN', op, 'call screen 未实现: ' + op.screen);
    var f = this.currentFrame();
    if (f) f.pc++;
    return Promise.resolve();
  };

  /* --------------------------------------------------------------------------
     pause
     -------------------------------------------------------------------------- */
  VM.prototype.doPause = function (op) {
    var self = this;
    var seconds = op.seconds;

    /* pause 无参数：等待点击 */
    if (seconds === null || seconds === undefined) {
      return new Promise(function (resolve) {
        self.waiting = 'pause';
        self._pauseResolve = function () {
          self.waiting = null;
          self._pauseResolve = null;
          resolve();
        };
      });
    }

    /* 跳过模式下大幅缩短 */
    if (this.skipMode) seconds = Math.min(seconds, 0.05);

    return new Promise(function (resolve) {
      self.waiting = 'pause';
      var t = setTimeout(function () {
        self.waiting = null;
        resolve();
      }, seconds * 1000);
      self._pauseTimer = t;
      /* hard pause 期间忽略点击；非 hard 允许点击提前结束 */
      if (!op.hard) {
        self._pauseResolve = function () {
          clearTimeout(t);
          self.waiting = null;
          self._pauseResolve = null;
          resolve();
        };
      }
    });
  };

  /* --------------------------------------------------------------------------
     with
     -------------------------------------------------------------------------- */
  VM.prototype.doWith = function (op) {
    var tr = op.transition;
    if (!tr) return undefined;

    if (tr.kind === 'filter') {
      this.stage.setFilter(tr.filter);
      return undefined;
    }

    var self = this;
    return this.transitions.apply(this.stage.masterLayer, function () {}, tr)
      .then(function () { return undefined; });
  };

  /* --------------------------------------------------------------------------
     window
     -------------------------------------------------------------------------- */
  VM.prototype.doWindow = function (op) {
    if (op.mode === 'hide') {
      this.state.windowMode = 'hide';
    } else {
      this.state.windowMode = op.mode;
    }
    if (this.ui && this.ui.say) {
      this.ui.say.setWindowMode(this.state.windowMode);
    }
    this.state.sayVisible = op.mode !== 'hide';
  };

  /* --------------------------------------------------------------------------
     $ 语句
     -------------------------------------------------------------------------- */
  VM.prototype.doPython = function (op, frame) {
    var self = this;
    var code = String(op.code || '').trim();

    /* 常见 renpy.* 调用直接拦截 */
    if (/^renpy\.pause\s*\(/.test(code)) {
      var m = /^renpy\.pause\s*\(\s*([\d.]+)/.exec(code);
      var secs = m ? parseFloat(m[1]) : null;
      var hard = /hard\s*=\s*True/.test(code);
      return this.doPause({ seconds: secs, hard: hard, file: op.file, line: op.line });
    }
    if (/^renpy\.full_restart\s*\(/.test(code)) {
      this.running = false;
      if (this.onFullRestart) this.onFullRestart();
      return undefined;
    }

    var ctx = this.exprContext(op);
    var result;
    try {
      result = Expr.execStatement(code, ctx);
    } catch (err) {
      this.diag('PY_ERROR', op, '执行失败: ' + code + ' :: ' + (err && err.message));
      return undefined;
    }

    /* 结果可能是 Promise（少见），等它 */
    if (Expr.isThenable(result)) {
      return result.then(function () { return undefined; });
    }
    if (result && Expr.isThenable(result.value)) {
      return result.value.then(function () { return undefined; });
    }
    return undefined;
  };

  /* --------------------------------------------------------------------------
     表达式上下文：把 store 变量、actor、renpy API 暴露给求值器
     -------------------------------------------------------------------------- */
  VM.prototype.exprContext = function (op) {
    var self = this;

    return {
      get: function (name) {
        /* 别名：center/left/right 作为位置常量 */
        if (name === 'center' || name === 'left' || name === 'right' ||
            name === 'truecenter' || name === 'center_left' ||
            name === 'center_right') {
          return name;
        }
        if (name === 'anim_shake' || name === 'anim_jump') return name;
        if (name === 'dissolve') return { kind: 'dissolve', duration: 0.5 };
        if (name === 'None') return null;
        if (name === 'True') return true;
        if (name === 'False') return false;

        if (self.actors.has(name)) return self.makeActorProxy(name);

        var v = self.state.getVar(name);
        if (v !== undefined) return v;

        /* renpy / config / achievement / persistent 命名空间 */
        if (name === 'renpy') return self.renpyApi();
        if (name === 'config') return self.configApi();
        if (name === 'achievement') return self.achievementApi();
        if (name === 'persistent') return self.persistentProxy();
        if (name === 'store') return self.state.vars;
        if (name === 'gui') return self.guiApi();

        return undefined;
      },

      set: function (name, value) {
        self.state.setVar(name, value);
      },

      setPath: function (path, value) {
        self.state.setPath(path, value);
      },

      getPath: function (path) {
        return self.state.getPath(path);
      },

      call: function (calleeAst, args, kwargs) {
        return self.invoke(calleeAst, args, kwargs, op);
      },

      diag: function (kind, pos, msg) {
        self.diag(kind, op, msg);
      }
    };
  };

  VM.prototype.makeActorProxy = function (code) {
    var self = this;
    var actor = this.actors.get(code);
    if (!actor) return undefined;

    return {
      show: function (expr, opts) {
        return actor.show(expr, opts || {});
      },
      hide: function (opts) {
        return actor.hide(opts || {});
      },
      act: function (action) {
        return actor.act(action);
      },
      reset_position: function () {
        return actor.resetPosition();
      },
      set_position: function (pos) {
        return actor.setPosition(pos);
      }
    };
  };

  /* --------------------------------------------------------------------------
     白名单 API
     -------------------------------------------------------------------------- */
  VM.prototype.renpyApi = function () {
    var self = this;
    return {
      pause: function (seconds, opts) {
        opts = opts || {};
        return self.doPause({
          seconds: seconds,
          hard: opts.hard,
          file: '',
          line: 0
        });
      },
      full_restart: function () {
        self.running = false;
        if (self.onFullRestart) self.onFullRestart();
      },
      notify: function (msg) {
        if (self.ui && self.ui.toast) self.ui.toast(msg);
      },
      get_screen: function () { return null; },
      show_screen: function () { return undefined; },
      hide_screen: function () { return undefined; }
    };
  };

  VM.prototype.configApi = function () {
    var self = this;
    return {
      developer: false,
      allow_skipping: true,
      skipping: false,
      screen_width: 1920,
      screen_height: 1080,
      name: 'GalGod',
      version: '1.0.0'
    };
  };

  VM.prototype.achievementApi = function () {
    var self = this;
    return {
      grant: function (id) {
        self.state.grantAchievement(id);
      },
      sync: function () { return undefined; }
    };
  };

  VM.prototype.persistentProxy = function () {
    var self = this;
    return {
      get: function (k) { return self.state.persistent.get(k); },
      set: function (k, v) { self.state.persistent.set(k, v); }
    };
  };

  VM.prototype.guiApi = function () {
    return {
      about: this.program.guiAbout || ''
    };
  };

  /* --------------------------------------------------------------------------
     调用派发
     -------------------------------------------------------------------------- */
  VM.prototype.invoke = function (calleeAst, args, kwargs, op) {
    /* callee 可能是：
       1. name（"store.xxx" 里的函数名）
       2. attr（obj.method）
    */
    if (calleeAst.k === 'name') {
      var fnName = calleeAst.v;
      var builtin = this.builtinFunction(fnName);
      if (builtin) return builtin.apply(null, args);
      this.diag('UNKNOWN_FUNCTION', op, '未知函数: ' + fnName);
      return undefined;
    }

    if (calleeAst.k === 'attr') {
      var objAst = calleeAst.obj;
      var method = calleeAst.name;

      /* renpy.xxx / achievement.xxx / config.xxx */
      if (objAst.k === 'name') {
        var root = objAst.v;
        if (root === 'renpy') {
          var api = this.renpyApi();
          if (typeof api[method] === 'function') return api[method].apply(api, args);
        }
        if (root === 'achievement') {
          var aapi = this.achievementApi();
          if (typeof aapi[method] === 'function') return aapi[method].apply(aapi, args);
        }
        if (root === 'persistent') {
          var pap = this.persistentProxy();
          if (typeof pap[method] === 'function') return pap[method].apply(pap, args);
        }

        /* actor 方法 */
        if (this.actors.has(root)) {
          var actor = this.actors.get(root);
          return this.callActorMethod(actor, method, args, kwargs, op);
        }
      }

      /* 通用对象方法 */
      var obj = this.evalAst(objAst, op);
      if (obj && typeof obj[method] === 'function') {
        return obj[method].apply(obj, args);
      }
      this.diag('UNKNOWN_METHOD', op, '无法调用方法: ' + method);
      return undefined;
    }

    this.diag('BAD_CALL', op, '无法识别的调用形式');
    return undefined;
  };

  VM.prototype.callActorMethod = function (actor, method, args, kwargs, op) {
    switch (method) {
      case 'show':
        return actor.show(args[0], normalizeActorOpts(kwargs));
      case 'hide':
        return actor.hide(normalizeActorOpts(kwargs));
      case 'act':
        return actor.act(args[0]);
      case 'reset_position':
        return actor.resetPosition();
      case 'set_position':
        return actor.setPosition(args[0]);
      default:
        this.diag('UNKNOWN_ACTOR_METHOD', op, '角色方法未实现: ' + method);
        return undefined;
    }
  };

  function normalizeActorOpts(kw) {
    var out = {};
    if (kw.pos !== undefined) out.pos = kw.pos;
    if (kw.zoom !== undefined) out.zoom = kw.zoom;
    if (kw.y_offset !== undefined) out.yOffset = kw.y_offset;
    if (kw.x_offset !== undefined) out.xOffset = kw.x_offset;
    if (kw.transition !== undefined) {
      out.transition = kw.transition === null
        ? null
        : (typeof kw.transition === 'string'
            ? { kind: kw.transition, duration: 0.5 }
            : kw.transition);
    }
    return out;
  }

  VM.prototype.evalAst = function (ast, op) {
    var ctx = this.exprContext(op);
    return Expr.evaluate(ast, ctx);
  };

  VM.prototype.builtinFunction = function (name) {
    var self = this;
    var map = {
      Character: function () { return {}; },
      Solid: function (c) { return { type: 'solid', color: c }; },
      Transform: function (p) { return { type: 'image', path: p }; },
      Image: function (p) { return { type: 'image', path: p }; },
      At: function (p) { return p; },
      Fade: function () { return { kind: 'fade', duration: 0.5 }; },
      Dissolve: function (d) { return { kind: 'dissolve', duration: d || 0.5 }; },
      Pause: function () { return null; },
      Function: function () { return null; },
      Play: function () { return null; },
      Stop: function () { return null; },
      Show: function () { return null; },
      Hide: function () { return null; },
      ShowMenu: function () { return null; },
      SetVariable: function () { return null; },
      SetScreenVariable: function () { return null; },
      Preference: function () { return null; },
      _: function (s) { return s; },
      len: function (a) { return a ? a.length : 0; },
      str: function (v) { return String(v); },
      int: function (v) { return parseInt(v, 10) || 0; },
      float: function (v) { return parseFloat(v) || 0; },
      range: function (a, b) {
        var out = [];
        var start = b === undefined ? 0 : a;
        var end = b === undefined ? a : b;
        for (var i = start; i < end; i++) out.push(i);
        return out;
      },
      max: function () { return Math.max.apply(Math, arguments); },
      min: function () { return Math.min.apply(Math, arguments); },
      abs: function (v) { return Math.abs(v); }
    };
    return map[name] || null;
  };

  /* --------------------------------------------------------------------------
     条件求值
     -------------------------------------------------------------------------- */
  VM.prototype.evalCond = function (cond, op) {
    var ast = Expr.parse(String(cond), function (kind, pos, msg) {
      this.diag(kind, op, msg);
    }.bind(this));
    var ctx = this.exprContext(op);
    var v;
    try {
      v = Expr.evaluate(ast, ctx);
    } catch (err) {
      this.diag('COND_ERROR', op, '条件求值失败: ' + cond);
      return false;
    }
    return !!v;
  };

  /* --------------------------------------------------------------------------
     菜单
     -------------------------------------------------------------------------- */
  VM.prototype.doMenu = function (op, frame) {
    var self = this;

    var options = (op.items || []).map(function (item, idx) {
      return { text: item.text, index: idx, target: item.target };
    });

    return this.ui.choice.show(op.caption, op.who, options).then(function (picked) {
      var item = op.items[picked];
      if (!item) {
        /* 用户取消：跳过整个 menu */
        frame.pc = op.end;
      } else {
        frame.pc = item.target;
      }
      return 'wait';
    });
  };

  /* --------------------------------------------------------------------------
     回滚
     -------------------------------------------------------------------------- */
  VM.prototype.pushRollback = function (kind) {
    var frame = this.currentFrame();
    if (!frame) return;

    this.rollbackStack.push({
      kind: kind,
      label: frame.label,
      pc: frame.pc - 1,
      frames: this.frames.map(function (f) { return { label: f.label, pc: f.pc }; }),
      snapshot: this.state.snapshot()
    });
    if (this.rollbackStack.length > this.rollbackLimit) this.rollbackStack.shift();
  };

  VM.prototype.canRollback = function () {
    return this.rollbackStack.length > 0;
  };

  VM.prototype.rollback = function () {
    var entry = this.rollbackStack.pop();
    if (!entry) return false;

    this.running = true;
    this.waiting = null;
    this.ui.say.hideImmediate();

    this.frames = entry.frames.map(function (f) { return { label: f.label, pc: f.pc }; });
    this.state.restore(entry.snapshot);
    this.stage.rebuild();

    /* 恢复音频 */
    if (this.state.music) {
      this.audio.play('music', this.state.music.path, { loop: this.state.music.loop });
    }
    if (this.state.ambient) {
      this.audio.play('sound', this.state.ambient.path, { loop: this.state.ambient.loop });
    }

    this.run();
    return true;
  };

  /* --------------------------------------------------------------------------
     存档 / 读档
     -------------------------------------------------------------------------- */
  /**
   * 生成存档数据。
   *
   * 关键：yield 型指令（say / centered / menu / callScreen）在 exec 里
   * 会先 `frame.pc++` 再返回 Promise 挂起。若直接取 frame.pc，
   * 存档记录的是「下一句」，读档就会从下一句开始（差一句）。
   *
   * 因此优先使用 waitingAt —— 它在挂起时记录的是「当前这句」。
   */
  VM.prototype.saveState = function () {
    var frame = this.currentFrame();
    if (!frame) return null;

    var at = this.waitingAt;
    var label = at ? at.label : frame.label;
    var pc = at ? at.pc : frame.pc;

    /* 保留完整的调用栈，但栈顶用落点修正 */
    var frames = this.frames.map(function (f) {
      return { label: f.label, pc: f.pc };
    });
    if (frames.length) {
      frames[frames.length - 1] = { label: label, pc: pc };
    }

    var lab = this.label(label);
    var op = (lab && pc >= 0 && pc < lab.ops.length) ? lab.ops[pc] : null;

    return {
      label: label,
      pc: pc,
      frames: frames,
      snapshot: this.state.snapshot(),
      dialogue: op && op.op === 'say'
        ? { who: op.who, text: op.text }
        : (this.ui.say.lastSay || null),
      time: new Date().toISOString()
    };
  };


  VM.prototype.loadState = function (data) {
    if (!data) return Promise.resolve();

    /* 作废旧执行链：say 的 Promise 可能还挂着，不处理会继续跑旧进度 */
    this.abort();
    this.ui.say.hideImmediate();
    this.rollbackStack = [];
    this.waitingAt = null;

    /* 恢复状态与调用栈 */
    this.state.restore(data.snapshot);
    this.frames = (data.frames && data.frames.length)
      ? data.frames.map(function (f) { return { label: f.label, pc: f.pc }; })
      : [{ label: data.label, pc: data.pc }];

    this.stage.rebuild();

    /* 音频恢复 */
    this.audio.stop('music', {});
    if (this.state.music) {
      this.audio.play('music', this.state.music.path, { loop: this.state.music.loop });
    }
    this.audio.stop('sound', {});
    if (this.state.ambient) {
      this.audio.play('sound', this.state.ambient.path, { loop: this.state.ambient.loop });
    }

    this.running = true;
    return this.run();
  };

  /* --------------------------------------------------------------------------
     自动 / 快进
     -------------------------------------------------------------------------- */
  VM.prototype.setAuto = function (on) {
    this.autoMode = !!on;
    this.state.autoMode = !!on;
    if (!on) {
      clearTimeout(this.autoTimer);
      this.autoTimer = null;
    }
    if (on && this.ui.say.isWaiting) {
      this.scheduleAuto();
    }
  };

  VM.prototype.scheduleAuto = function () {
    var self = this;
    clearTimeout(this.autoTimer);
    if (!this.autoMode) return;

    var delay = (this.state.persistent.get('afm_time', 15) || 15) * 100;

    var tick = function () {
      if (!self.autoMode) return;
      /* 语音播放中则等待 */
      if (self.audio.isVoicePlaying()) {
        self.autoTimer = setTimeout(tick, 200);
        return;
      }
      self.ui.say.advance();
    };
    this.autoTimer = setTimeout(tick, delay);
  };

  VM.prototype.setSkip = function (on) {
    this.skipMode = !!on;
    this.state.skipMode = !!on;
    if (on && this.ui.say.isWaiting) {
      this.ui.say.advance();
    }
  };

  /* --------------------------------------------------------------------------
     语音标签推断（用于角色独立音量）
     -------------------------------------------------------------------------- */
  VM.prototype.voiceTagFor = function (path) {
    var p = String(path || '');
    for (var code in (this.actors.actors || {})) {
      var a = this.actors.actors[code];
      if (a.voiceTag && p.indexOf(a.voiceTag) >= 0) return a.voiceTag;
    }
    if (/linxi/.test(p)) return 'lx';
    if (/jiangwanqing/.test(p)) return 'jwq';
    if (/xiaolian/.test(p)) return 'xl';
    return null;
  };

  global.RPYVM = {
    VM: VM
  };
})(window);