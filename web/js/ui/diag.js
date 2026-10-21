/* ==========================================================================
   ui/diag.js
   F9 调试面板，四个页签：

     诊断      解析 / 资源 / 运行时问题汇总
     章节跳转  对应 screens/dev_jump_menu.rpy，直接跳任意 label
     变量      store 变量 + persistent 关键项实时快照
     指令追踪  当前 label 的指令流，高亮当前 PC

   设计原则：面板是「只读观察 + 唯一写操作（跳转）」，
   不参与游戏逻辑，关掉后不留任何副作用。
   ========================================================================== */
(function (global) {
  'use strict';

  var TAB_LABELS = {
    issues: '诊断',
    jump: '章节跳转',
    vars: '变量',
    trace: '指令追踪'
  };

  /* 与 screens/dev_jump_menu.rpy 对齐的跳转清单 */
  var JUMP_LIST = [
    { label: 'scene_1_1', text: 'Scene 1-1' },
    { label: 'scene_1_2', text: 'Scene 1-2' },
    { label: 'scene_1_3', text: 'Scene 1-3' },
    { label: 'scene_1_4', text: 'Scene 1-4' },
    { label: 'scene_2_1', text: 'Scene 2-1' },
    { label: 'interlude1', text: 'Interlude 1' },
    { label: 'interlude2', text: 'Interlude 2' },
    { label: 'scene_2_2', text: 'Scene 2-2' },
    { label: 'scene_2_3', text: 'Scene 2-3' },
    { label: 'scene_2_4', text: 'Scene 2-4' },
    { label: 'scene_3_1', text: 'Scene 3-1' },
    { label: 'scene_3_2', text: 'Scene 3-2' },
    { label: 'scene_3_3', text: 'Scene 3-3' },
    { label: 'scene_3_4', text: 'Scene 3-4' },
    { label: 'interlude_interview', text: '面试' },
    { label: 'end1', text: 'True End' },
    { label: 'end2', text: 'End 2' },
    { label: 'end3', text: 'End 3' },
    { label: 'after_story_noctella', text: 'After Story' }
  ];

  function Diag(app) {
    this.app = app;
    this.el = document.getElementById('diag');
    this.body = document.getElementById('diag-body');
    this.tabsEl = document.getElementById('diag-tabs');
    this.pcEl = document.getElementById('diag-pc');
    this.stateEl = document.getElementById('diag-state');

    this.open = false;
    this.tab = 'issues';
    this.traceCache = { label: null, ops: null };

    if (!this.el) {
      /* HTML 结构缺失（例如旧版本缓存）：构造一个最小面板，保证 F9 可用 */
      this.el = document.createElement('div');
      this.el.id = 'diag';
      this.el.className = 'diag';
      this.el.hidden = true;
      this.el.innerHTML =
        '<div class="diag-head"><span class="d-title">调试面板</span>' +
        '<button type="button" id="diag-close">关闭 (F9)</button></div>' +
        '<div class="diag-body" id="diag-body"></div>';
      document.body.appendChild(this.el);
      this.body = document.getElementById('diag-body');
      this.tabsEl = null;
    }

    this.bind();
  }

  /* --------------------------------------------------------------------------
     事件绑定
     -------------------------------------------------------------------------- */
  Diag.prototype.bind = function () {
    var self = this;

    /* F9 开关；反引号作为备用键（部分键盘布局 F9 被占用） */
    document.addEventListener('keydown', function (e) {
      if (e.key === 'F9' || e.key === '`' || e.code === 'Backquote') {
        e.preventDefault();
        e.stopPropagation();
        self.toggle();
        return;
      }
      if (e.key === 'Escape' && self.open) {
        e.preventDefault();
        self.hide();
      }
    }, true);

    var closeBtn = document.getElementById('diag-close');
    if (closeBtn) closeBtn.addEventListener('click', function () { self.hide(); });

    var refreshBtn = document.getElementById('diag-refresh');
    if (refreshBtn) refreshBtn.addEventListener('click', function () { self.render(); });

    if (this.tabsEl) {
      this.tabsEl.addEventListener('click', function (e) {
        var btn = e.target.closest('button[data-tab]');
        if (!btn) return;
        self.tab = btn.dataset.tab;
        self.render();
      });
    }

    /* 面板内滚动不触发游戏的回滚/历史 */
    if (this.el) {
      this.el.addEventListener('wheel', function (e) { e.stopPropagation(); });
      this.el.addEventListener('click', function (e) { e.stopPropagation(); });
    }
  };

  /* --------------------------------------------------------------------------
     显隐
     -------------------------------------------------------------------------- */
  Diag.prototype.toggle = function () {
    if (this.open) this.hide(); else this.show();
  };

  Diag.prototype.show = function () {
    this.open = true;
    /* 用属性选择器而非 .hidden，避免 display:flex 覆盖 */
    this.el.removeAttribute('hidden');
    this.el.style.display = 'flex';
    this.render();
    this.startPolling();
  };

  Diag.prototype.hide = function () {
    this.open = false;
    this.el.setAttribute('hidden', '');
    this.el.style.display = 'none';
    this.stopPolling();
  };

  /* 打开期间低频刷新（PC / 状态 / 变量会变） */
  Diag.prototype.startPolling = function () {
    var self = this;
    this.stopPolling();
    this._poll = setInterval(function () {
      if (!self.open) return;
      self.updateFooter();
      if (self.tab === 'vars' || self.tab === 'trace') self.render();
    }, 700);
  };

  Diag.prototype.stopPolling = function () {
    if (this._poll) { clearInterval(this._poll); this._poll = null; }
  };

  /* --------------------------------------------------------------------------
     渲染入口
     -------------------------------------------------------------------------- */
  Diag.prototype.render = function () {
    var self = this;

    if (!this.body) {
      /* 极端情况：连 body 容器都没有，直接重建 */
      this.el.innerHTML = '<div class="diag-body" id="diag-body"></div>';
      this.body = this.el.querySelector('#diag-body');
    }

    /* ---- 页签状态与角标 ---- */
    var count = 0;
    try {
      count = this.collectIssues().length;
    } catch (e) {
      count = 0;
    }

    if (this.tabsEl) {
      Array.prototype.forEach.call(
        this.tabsEl.querySelectorAll('button[data-tab]'),
        function (btn) {
          var t = btn.dataset.tab;
          btn.classList.toggle('active', t === self.tab);
          btn.textContent = TAB_LABELS[t] || t;
          if (t === 'issues' && count > 0) {
            var badge = document.createElement('span');
            badge.className = 'd-badge';
            badge.textContent = count > 999 ? '999+' : count;
            btn.appendChild(badge);
          }
        }
      );
    }

    /* ---- 内容：任何异常都必须在面板里可见，而不是留白 ---- */
    try {
      switch (this.tab) {
        case 'issues': this.renderIssues(); break;
        case 'jump':   this.renderJump(); break;
        case 'vars':   this.renderVars(); break;
        case 'trace':  this.renderTrace(); break;
        default:       this.renderIssues();
      }
    } catch (err) {
      this.body.innerHTML =
        '<div class="d-item"><div><span class="d-kind">[PANEL_ERROR]</span> ' +
        esc(this.tab) + '</div>' +
        '<div class="d-msg">渲染失败：' + esc(err && err.message ? err.message : err) +
        '</div><div class="d-msg" style="color:#666">' +
        esc(String(err && err.stack ? err.stack : '').split('\n').slice(0, 5).join('\n')) +
        '</div></div>';
      if (global.console) console.error('[GalGod] diag render failed', err);
    }

    this.updateFooter();
  };

  Diag.prototype.updateFooter = function () {
    var vm = this.app.vm;
    if (!this.pcEl || !this.pcEl.textContent !== undefined) { /* noop */ }

    if (this.pcEl) {
      if (vm && vm.lastPc && vm.lastPc.label) {
        this.pcEl.textContent = vm.lastPc.label + '  #' + vm.lastPc.pc;
      } else {
        this.pcEl.textContent = '未开始';
      }
    }
    if (this.stateEl) {
      var bits = [];
      if (vm) {
        bits.push(vm.running ? '运行中' : '已停止');
        if (vm.waiting) bits.push('等待:' + vm.waiting);
        if (vm.autoMode) bits.push('自动');
        if (vm.skipMode) bits.push('快进');
        bits.push('回滚点:' + vm.rollbackStack.length);
      }
      this.stateEl.textContent = bits.join(' · ') || '—';
    }
  };

  /* --------------------------------------------------------------------------
     页签：诊断
     -------------------------------------------------------------------------- */
  Diag.prototype.collectIssues = function () {
    var app = this.app;
    var items = [].concat(
      app.program && app.program.diagnostics ? app.program.diagnostics : [],
      app.images && app.images.diagnostics ? app.images.diagnostics : [],
      app.runtimeDiagnostics || [],
      app.vm && app.vm.diagnostics ? app.vm.diagnostics : []
    );

    /* 去重 */
    var seen = Object.create(null);
    var out = [];
    items.forEach(function (d) {
      var key = [d.kind, d.file, d.line, d.message].join('|');
      if (seen[key]) return;
      seen[key] = true;
      out.push(d);
    });
    return out;
  };

  Diag.prototype.renderIssues = function () {
    var stats = this.app.stats ? this.app.stats() : null;
    var issues = this.collectIssues();

    var html = '';

    if (stats) {
      html += '<div class="d-stats">' +
        '脚本 ' + stats.scripts + ' 个 · label ' + stats.labels + ' 个 · 指令 ' +
        stats.ops + ' 条<br>' +
        '图像定义 ' + stats.images + ' 个 · 资源 ' + stats.assets + ' 个' +
        '</div>';
    }

    if (!issues.length) {
      html += '<div class="d-ok">✓ 没有诊断问题。全部语句与资源均已正确解析。</div>';
      this.body.innerHTML = html;
      return;
    }

    /* 按 kind 分组统计 */
    var byKind = Object.create(null);
    issues.forEach(function (d) {
      (byKind[d.kind] = byKind[d.kind] || []).push(d);
    });

    html += '<div class="d-section">共 ' + issues.length + ' 条，按类型分组</div>';
    Object.keys(byKind).sort().forEach(function (k) {
      html += '<div class="d-item">' +
        '<div><span class="d-kind">[' + esc(k) + ']</span> ' +
        '× ' + byKind[k].length + '</div>';
      byKind[k].slice(0, 20).forEach(function (d) {
        html += '<div class="d-msg" style="padding-left:12px">' +
          '<span class="d-loc">' + esc(d.file || '?') + ':' + (d.line || 0) + '</span>  ' +
          esc(d.message || '') + '</div>';
      });
      if (byKind[k].length > 20) {
        html += '<div class="d-msg" style="padding-left:12px;color:#666">… 还有 ' +
          (byKind[k].length - 20) + ' 条</div>';
      }
      html += '</div>';
    });

    this.body.innerHTML = html;
  };

  /* --------------------------------------------------------------------------
     页签：章节跳转
     -------------------------------------------------------------------------- */
  Diag.prototype.renderJump = function () {
    var self = this;
    var vm = this.app.vm;

    var html = '<div class="d-section">点击直接跳转（对齐 dev_jump_menu）</div>' +
      '<div class="diag-jump" id="diag-jump-list"></div>';

    html += '<div class="d-section">全部 label</div>';
    html += '<div class="d-stats" style="line-height:2">';
    var labels = Object.keys(this.app.program.labels)
      .filter(function (n) { return !self.app.program.labels[n].synthetic; })
      .sort();
    html += labels.map(function (n) {
      var ops = self.app.program.labels[n].ops.length;
      return '<span style="color:#79c0ff">' + esc(n) + '</span>' +
        '<span style="color:#555">(' + ops + ')</span>';
    }).join(' &nbsp; ');
    html += '</div>';

    this.body.innerHTML = html;

    var list = document.getElementById('diag-jump-list');
    JUMP_LIST.forEach(function (item) {
      var btn = document.createElement('button');
      btn.type = 'button';
      var exists = !!self.app.program.labels[item.label];
      btn.textContent = item.text;
      btn.title = item.label + (exists ? '' : '（label 不存在）');
      if (!exists) {
        btn.disabled = true;
        btn.style.opacity = '0.4';
      }
      btn.addEventListener('click', function () {
        self.jumpTo(item.label);
      });
      list.appendChild(btn);
    });
  };

  /**
   * 从调试面板直接跳转。
   * 关键：主菜单阶段 VM 尚未运行、frames 为空，此时也能直接开跑，
   * 因此这里不依赖「已经点过开始游戏」。
   */
  Diag.prototype.jumpTo = function (label) {
    var app = this.app;
    if (!app.program.labels[label]) {
      app.toast('label 不存在: ' + label);
      return;
    }

    /* ---- 1. 第一步就作废旧执行链 ----
       必须早于任何 UI 清理：say.hideImmediate() 会 resolve 旧的对白 Promise，
       若此时还没 abort，旧链会立刻继续跑到下一条指令，抢帧栈。 */
    app.vm.abort();

    /* ---- 2. 关掉所有界面层 ---- */
    app.closeAllMenus();
    app.closeHelp();
    if (app.ui.mainMenu) {
      app.ui.mainMenu.hide();
      app.ui.mainMenu = null;
    }
    app.stopMenuMusic();

    app.ui.say.hideImmediate();
    app.ui.say.hideBox();
    app.ui.centered.hide();
    app.ui.choice.hide();
    app.ui.movie.hide();

    /* ---- 音频与舞台复位 ---- */
    app.audio.stop('music', {});
    app.audio.stop('sound', {});
    app.audio.stopVoice();
    app.stage.clearBackground();
    app.stage.clearCG();
    app.stage.clearOverlay();
    app.stage.hideRain('back');
    app.stage.hideRain('front');
    app.stage.resetCamera();
    app.stage.setFilter('reset');
    Object.keys(app.stage.spriteEls).forEach(function (code) {
      var el = app.stage.spriteEls[code];
      if (el.parentNode) el.parentNode.removeChild(el);
    });
    app.stage.spriteEls = Object.create(null);

    /* ---- 3. 重置运行时状态（保留 persistent） ---- */
    var persistent = app.state.persistent;
    var fresh = new global.RPYState.State();
    fresh.persistent = persistent;
    app.state = fresh;
    app.vm.state = fresh;
    app.audio.state = fresh;
    app.stage.state = fresh;
    app.actors.state = fresh;

    /* ---- 4. 清空进度相关结构 ---- */
    app.vm.rollbackStack = [];
    app.vm.frames = [];

    /* ---- 5. 起跑（jumpTo 内部 abort + applyDefaults + running=true） ---- */
    app.toast('跳转到 ' + label, 1200);
    app.vm.jumpTo(label);
    app.refreshQuickMenu();

    if (this.open) this.render();
  };

  /* --------------------------------------------------------------------------
     页签：变量
     -------------------------------------------------------------------------- */
  Diag.prototype.renderVars = function () {
    var app = this.app;
    var state = app.state;
    var html = '';

    /* store 变量 */
    var vars = state.vars || {};
    var keys = Object.keys(vars).sort();

    html += '<div class="d-section">store 变量（' + keys.length + '）</div>';
    if (!keys.length) {
      html += '<div class="d-msg" style="color:#666">（空）</div>';
    } else {
      html += '<div class="diag-vars">';
      keys.forEach(function (k) {
        html += '<div class="v-row"><span class="v-key">' + esc(k) + '</span>' +
          '<span class="v-val" title="' + esc(safeJSON(vars[k])) + '">' +
          esc(safeJSON(vars[k])) + '</span></div>';
      });
      html += '</div>';
    }

    /* persistent 关键项 */
    var p = state.persistent.data;
    var pKeys = ['game_cleared', 'text_cps', 'afm_time', 'dialogue_box_alpha',
                 'skip_speed_var', 'music_volume', 'sound_volume', 'voice_volume'];
    html += '<div class="d-section">persistent</div><div class="diag-vars">';
    pKeys.forEach(function (k) {
      html += '<div class="v-row"><span class="v-key">' + esc(k) + '</span>' +
        '<span class="v-val">' + esc(safeJSON(p[k])) + '</span></div>';
    });
    html += '</div>';

    /* 已解锁成就 */
    var ach = Object.keys(p.achievements || {}).filter(function (k) {
      return p.achievements[k];
    });
    html += '<div class="d-section">成就（' + ach.length + '）</div>' +
      '<div class="d-msg" style="color:#7ee787">' +
      (ach.length ? esc(ach.join(', ')) : '（无）') + '</div>';

    /* 舞台状态 */
    html += '<div class="d-section">舞台</div><div class="d-msg">' +
      '背景: ' + esc(state.bg ? state.bg.name : '（空）') + '<br>' +
      'CG: ' + esc((state.cg || []).map(function (c) { return c.name; }).join(', ') || '（空）') + '<br>' +
      '立绘: ' + esc(Object.keys(state.sprites).map(function (code) {
        var s = state.sprites[code];
        return code + (s.visible ? '=' + (s.expr || '?') : '(隐藏)');
      }).join(', ') || '（空）') + '<br>' +
      '滤镜: ' + esc(state.layerFilters.master || '（无）') + '<br>' +
      '音乐: ' + esc(state.music ? state.music.path : '（无）') +
      '</div>';

    this.body.innerHTML = html;
  };

  /* --------------------------------------------------------------------------
     页签：指令追踪
     -------------------------------------------------------------------------- */
  Diag.prototype.renderTrace = function () {
    var vm = this.app.vm;
    var label = vm.lastPc && vm.lastPc.label;
    var pc = vm.lastPc ? vm.lastPc.pc : 0;

    if (!label) {
      this.body.innerHTML = '<div class="d-msg" style="color:#666">' +
        '尚未开始执行。可从「章节跳转」进入任意章节。</div>';
      return;
    }

    var ops = null;
    if (this.traceCache.label === label) {
      ops = this.traceCache.ops;
    } else {
      var lab = this.app.program.labels[label];
      ops = lab ? lab.ops : [];
      this.traceCache = { label: label, ops: ops };
    }

    var html = '<div class="d-section">' + esc(label) + '（' + ops.length + ' 条，当前 #' + pc + '）</div>';
    html += '<div class="diag-trace">';

    /* 以当前 PC 为中心显示 ±60 行，避免超长章节卡住 */
    var start = Math.max(0, pc - 30);
    var end = Math.min(ops.length, pc + 60);

    if (start > 0) {
      html += '<div class="t-row"><span class="t-pc">…</span>' +
        '<span class="t-lab"></span><span class="t-op">（前面还有 ' + start + ' 条）</span></div>';
    }

    for (var i = start; i < end; i++) {
      var op = ops[i];
      html += '<div class="t-row' + (i === pc ? ' current' : '') + '">' +
        '<span class="t-pc">#' + i + '</span>' +
        '<span class="t-lab">' + esc(shortFile(op.file)) + ':' + (op.line || 0) + '</span>' +
        '<span class="t-op">' + esc(global.RPYCompiler.describeOp(op)) + '</span>' +
        '</div>';
    }

    if (end < ops.length) {
      html += '<div class="t-row"><span class="t-pc">…</span>' +
        '<span class="t-lab"></span><span class="t-op">（后面还有 ' +
        (ops.length - end) + ' 条）</span></div>';
    }

    html += '</div>';
    this.body.innerHTML = html;

    /* 自动滚到当前行 */
    var cur = this.body.querySelector('.t-row.current');
    if (cur) {
      var top = cur.offsetTop - this.body.clientHeight / 2;
      this.body.scrollTop = Math.max(0, top);
    }
  };

  /* --------------------------------------------------------------------------
     工具
     -------------------------------------------------------------------------- */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&')
      .replace(/</g, '<')
      .replace(/>/g, '>')
      .replace(/"/g, '"');
  }

  function safeJSON(v) {
    if (v === undefined) return 'undefined';
    if (typeof v === 'function') return 'fn';
    try {
      var s = JSON.stringify(v);
      if (s === undefined) return String(v);
      return s.length > 60 ? s.slice(0, 57) + '…' : s;
    } catch (e) {
      return String(v);
    }
  }

  function shortFile(f) {
    if (!f) return '(builtin)';
    var parts = String(f).split('/');
    return parts.length > 1 ? parts.slice(-2).join('/') : f;
  }

  global.RPYDiag = {
    Diag: Diag,
    JUMP_LIST: JUMP_LIST
  };
})(window);