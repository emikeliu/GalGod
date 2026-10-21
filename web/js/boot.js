/* ==========================================================================
   boot.js
   应用主控制器：加载清单 → 抽取配置 → 解析编译 → 组装运行时 → 启动。
   ========================================================================== */
(function (global) {
  'use strict';

  var U = global.RPYUtils;
  var S = global.RPYStrings;

  /* ==========================================================================
     App
     ========================================================================== */
  function App() {
    this.bootEl = document.getElementById('boot');
    this.bootStatus = document.getElementById('boot-status');
    this.bootBar = document.getElementById('boot-bar-fill');
    this.bootHint = document.getElementById('boot-hint');

    this.program = null;
    this.manifest = null;
    this.overrides = null;
    this.state = null;
    this.images = null;
    this.stage = null;
    this.actors = null;
    this.audio = null;
    this.transitions = null;
    this.vm = null;
    this.save = null;

    this.characters = Object.create(null);  /* code -> {name, color} */
    this.actorConfig = null;
    this.globalActor = { zoom: 0.6, y_offset: 1250 };
    this.runtimeDiagnostics = [];

    this.ui = Object.create(null);
    this._menuMusicStarted = false;
  }

  /* --------------------------------------------------------------------------
     启动
     -------------------------------------------------------------------------- */
  App.prototype.boot = function () {
    var self = this;

    return global.RPYManifest.loadManifest(function (msg) {
      self.setStatus(msg);
    }).then(function (manifest) {
      self.manifest = manifest;
      self.setProgress(0.08);
      return global.RPYManifest.loadOverrides();
    }).then(function (ov) {
      self.overrides = ov;
      self.setStatus('正在读取剧本…');
      self.setProgress(0.14);
      return global.RPYManifest.loadScripts(
        self.manifest.script_files,
        function (done, total, path) {
          self.setProgress(0.14 + 0.6 * (done / total));
          self.setStatus('读取 ' + path + '  (' + done + '/' + total + ')');
        }
      );
    }).then(function (sources) {
      self.setStatus('正在解析与编译…');
      self.setProgress(0.8);

      /* 记录读取失败的文件 */
      sources.forEach(function (s) {
        if (s.error) {
          self.runtimeDiagnostics.push({
            kind: 'SCRIPT_LOAD_ERROR',
            file: s.path,
            line: 0,
            message: s.error
          });
        }
      });

      var usable = sources.filter(function (s) { return !s.error; });
      self.program = global.RPYCompiler.compileAll(usable);
      self.program.version = (self.manifest.game && self.manifest.game.version) || '1.0.0';

      /* 从原始源码抽取 Python 配置块（字符表 / 立像参数 / 作者的话） */
      self.extractPythonConfig(usable);

      self.setProgress(0.9);
      return self.mount(usable);
    }).then(function () {
      self.setStatus('准备就绪');
      self.setProgress(1);
      /* 预热角色立绘（数量少，值得预加载） */
      return self.preloadCharacters();
    }).then(function () {
      self.hideBoot();

      /* 支持直接用 URL 跳章节：?label=scene_2_4&play=1
         play=1 表示跳过主菜单立即开跑 */
      var params = parseQuery(global.location.search);
      if (params.label && self.program.labels[params.label]) {
        if (params.play === '1') {
          self.vm.start(params.label);
        } else {
          self.showTitle();
          self.pendingJump = params.label;
          self.toast('已加载 ' + params.label + '，按 F9 打开调试面板可跳转进入', 3600);
        }
      } else {
        self.showTitle();
      }

      self.reportBootDiagnostics();
    }).catch(function (err) {
      self.setStatus('启动失败');
      self.bootHint.innerHTML =
        '<span style="color:#ff8a80">' + S.escapeHtml(String(err && err.message || err)) + '</span>' +
        '<br><br>请确认：<br>' +
        '1. 已在工程根目录运行 <code>python3 -m http.server 8000</code><br>' +
        '2. 通过 <code>http://localhost:8000/web/</code> 打开本页面<br>' +
        '3. 已运行 <code>python3 tools/gen_manifest.py</code> 生成清单';
      throw err;
    });
  };

  App.prototype.setStatus = function (msg) {
    if (this.bootStatus) this.bootStatus.textContent = msg;
  };

  App.prototype.setProgress = function (v) {
    if (this.bootBar) this.bootBar.style.width = Math.round(v * 100) + '%';
  };

  App.prototype.hideBoot = function () {
    if (!this.bootEl) return;
    this.bootEl.classList.add('hide');
    var self = this;
    setTimeout(function () {
      if (self.bootEl && self.bootEl.parentNode) self.bootEl.parentNode.removeChild(self.bootEl);
      self.bootEl = null;
    }, 520);
  };

  /* --------------------------------------------------------------------------
     组装运行时
     -------------------------------------------------------------------------- */
  App.prototype.mount = function (sources) {
    var self = this;

    this.state = new global.RPYState.State();
    this.images = new global.RPYImages.Images(this.manifest, this.overrides);
    this.images.load(this.program);

    this.stage = new global.RPYStage.Stage(this.images, this.state);
    this.actors = new global.RPYActors.Actors(
      this.actorConfig || {},
      this.stage,
      this.images,
      this.state
    );
    /* 让 stage 能访问 actors（rebuild 用） */
    this.stage.actors = this.actors;

    this.audio = new global.RPYAudio.Audio(this.images, this.state, this.state.persistent);
    this.transitions = new global.RPYTransitions.Transition(this.stage);

    this.save = new global.RPYSave.SaveManager(this);

    /* UI 组件 */
    this.ui.say = new global.RPYSayUI.SayUI(this);
    this.ui.centered = new global.RPYCenteredUI.CenteredUI(this);
    this.ui.choice = new global.RPYChoiceUI.ChoiceUI(this);
    this.ui.movie = new global.RPYMovie.Movie(this);
    this.ui.confirm = new U.Confirm(this);
    this.ui.toast = new U.Toast(this);
    this.ui.history = new global.RPYHistoryUI.HistoryUI(this);
    this.ui.saveLoad = new global.RPYSaveLoadUI.SaveLoadUI(this);
    this.ui.config = new global.RPYConfigUI.ConfigUI(this);
    this.ui.gallery = new global.RPYGalleryUI.GalleryUI(this);
    this.ui.about = new global.RPYAboutUI.AboutUI(this);
    this.ui.diag = new global.RPYDiag.Diag(this);

    /* VM */
    this.vm = new global.RPYVM.VM({
      program: this.program,
      state: this.state,
      images: this.images,
      actors: this.actors,
      stage: this.stage,
      audio: this.audio,
      transitions: this.transitions,
      ui: {
        say: this.ui.say,
        centered: this.ui.centered,
        choice: this.ui.choice,
        movie: this.ui.movie,
        toast: function (m) { self.toast(m); }
      }
    });

    var self2 = this;
    this.vm.onEnd = function () { self2.onStoryEnd(); };
    this.vm.onFullRestart = function () { self2.backToTitle(); };
    this.vm.onIdle = function () { self2.refreshQuickMenu(); };
    this.vm.onUiFlagChange = function () { self2.refreshQuickMenu(); };

    /* 语音结束回调（auto 模式） */
    this.audio.onVoiceEnded(function () {
      if (self2.vm.autoMode) self2.vm.scheduleAuto();
    });

    /* 注册 define 别名（如 define fx.crowd = "audio/fx/..."），
       VM 遇到 `play sound fx.crowd` 时据此解析真实路径 */
    this.registerDefines();

    /* 应用初始设置 */
    this.ui.say.applyAlpha();
    this.audio.applyVolumes();

    this.buildQuickMenu();
    return Promise.resolve();
  };

  /* --------------------------------------------------------------------------
     define 别名注册
     -------------------------------------------------------------------------- */
  App.prototype.registerDefines = function () {
    var self = this;
    var aliases = Object.create(null);

    (this.program.defines || []).forEach(function (d) {
      var name = d.name;
      var raw = String(d.value || '').trim();
      var str = global.RPYParser.asString(raw);
      if (str !== null) aliases[name] = str;
    });

    /* default 也收进来（布尔/数字等），供 if 条件使用 */
    (this.program.defaults || []).forEach(function (d) {
      if (self.state.getVar(d.name) !== undefined) return;
      var raw = String(d.value || '').trim();
      if (raw === 'True') self.state.setVar(d.name, true);
      else if (raw === 'False') self.state.setVar(d.name, false);
      else if (/^-?\d+(\.\d+)?$/.test(raw)) self.state.setVar(d.name, parseFloat(raw));
      else {
        var s = global.RPYParser.asString(raw);
        if (s !== null) self.state.setVar(d.name, s);
      }
    });

    this.aliases = aliases;
    this.vm.aliases = aliases;
    this.audio.aliases = aliases;
    if (this.images && this.images.setAliases) this.images.setAliases(aliases);
  };

  /* --------------------------------------------------------------------------
     从源码抽取 Python 配置块
     -------------------------------------------------------------------------- */
  App.prototype.extractPythonConfig = function (sources) {
    var self = this;

    /* 1) CHARACTERS_CONFIG（config/character_config.rpy） */
    var cc = this.findSource(sources, 'character_config.rpy');
    if (cc) {
      var block = this.extractAssignment(cc, 'CHARACTERS_CONFIG');
      if (block) {
        try {
          var ast = global.RPYExpr.parse(block, null);
          var val = global.RPYExpr.evaluate(ast, {
            get: function () { return undefined; },
            call: function () { return undefined; },
            diag: function () {}
          });
          if (val && typeof val === 'object') {
            this.actorConfig = val;
          }
        } catch (e) {
          this.runtimeDiagnostics.push({
            kind: 'CONFIG_PARSE_ERROR',
            file: cc.path,
            line: 0,
            message: 'CHARACTERS_CONFIG 解析失败: ' + e.message
          });
        }
      }
    }
    if (!this.actorConfig) this.actorConfig = {};
    this.state && (this.state.actorConfig = this.actorConfig);

    /* 2) global_actor_settings（config/options.rpy） */
    var co = this.findSource(sources, 'config/options.rpy');
    if (co) {
      var g = this.extractAssignment(co, 'global_actor_settings');
      if (g) {
        try {
          var ast2 = global.RPYExpr.parse(g, null);
          var v2 = global.RPYExpr.evaluate(ast2, {
            get: function () { return undefined; },
            call: function () { return undefined; },
            diag: function () {}
          });
          if (v2 && typeof v2 === 'object') this.globalActor = v2;
        } catch (e) { /* 用默认值 */ }
      }
    }
    global.RPYActors.GLOBAL.zoom = this.globalActor.zoom;
    global.RPYActors.GLOBAL.y_offset = this.globalActor.y_offset;

    /* 3) Character 定义：cz / zhengke / me / 以及各角色 */
    ['resources.rpy', 'config/character_core.rpy', 'scenes/3_1.rpy'].forEach(function (path) {
      var src = self.findSource(sources, path);
      if (!src) return;
      self.parseCharacterDefines(src.source);
    });

    /* 4) gui.about（screens/other_screens.rpy） */
    var about = this.findSource(sources, 'other_screens.rpy');
    if (about) {
      var m = /gui\.about\s*=\s*_\(\s*"""([\s\S]*?)"""\s*\)/.exec(about.source);
      if (m) {
        this.program.guiAbout = S.unescapeRpy(m[1]);
      }
    }

    /* 5) define config.name / config.version */
    var opt = this.findSource(sources, 'options.rpy');
    if (opt) {
      var nm = /define\s+config\.name\s*=\s*_\(\s*"([^"]*)"\s*\)/.exec(opt.source);
      if (nm) this.program.gameName = nm[1];
      var vr = /define\s+config\.version\s*=\s*"([^"]*)"/.exec(opt.source);
      if (vr) this.program.version = vr[1];
    }
  };

  App.prototype.findSource = function (sources, suffix) {
    for (var i = 0; i < sources.length; i++) {
      if (sources[i].path === suffix ||
          sources[i].path.slice(-suffix.length) === suffix) {
        return sources[i];
      }
    }
    return null;
  };

  /**
   * 从源码中抽取 `NAME = <expr>` 的右侧表达式（支持跨行的大括号块）。
   */
  App.prototype.extractAssignment = function (src, name) {
    var text = src.source;
    var re = new RegExp('(^|\\n)[ \\t]*' + name + '\\s*=\\s*', 'm');
    var m = re.exec(text);
    if (!m) return null;

    var start = m.index + m[0].length;
    var i = start;
    var depth = 0;
    var inS = false, inD = false, inTriple = false, esc = false;

    while (i < text.length) {
      var c = text[i];
      if (esc) { esc = false; i++; continue; }
      if (c === '\\') { esc = true; i++; continue; }

      if (inTriple) {
        if (text.substr(i, 3) === '"""') { inTriple = false; i += 3; continue; }
        i++; continue;
      }
      if (inS) { if (c === "'") inS = false; i++; continue; }
      if (inD) { if (c === '"') inD = false; i++; continue; }

      if (text.substr(i, 3) === '"""') { inTriple = true; i += 3; continue; }
      if (c === "'") { inS = true; i++; continue; }
      if (c === '"') { inD = true; i++; continue; }

      if (c === '{' || c === '(' || c === '[') depth++;
      else if (c === '}' || c === ')' || c === ']') {
        depth--;
        if (depth === 0) { i++; break; }
      } else if (c === '\n' && depth === 0) {
        /* 单行赋值结束 */
        break;
      } else if (c === '#' && depth === 0) {
        break;
      }
      i++;
    }

    var expr = text.slice(start, i).trim();
    /* 去掉所有 # 注释（跨行字典里有大量注释） */
    expr = S.stripPythonComments(expr);
    return expr || null;
  };

  /**
   * 解析 `define cz = Character("陈舟", color="#ffffff")`
   */
  App.prototype.parseCharacterDefines = function (source) {
    var re = /define\s+([A-Za-z_]\w*)\s*=\s*Character\s*\(([\s\S]*?)\)\s*(?:#.*)?$/gm;
    var m;
    while ((m = re.exec(source)) !== null) {
      var code = m[1];
      if (this.characters[code]) continue;
      var args = m[2];
      var nameM = /^\s*("(?:[^"\\]|\\.)*")/.exec(args);
      var name = nameM ? S.unescapeRpy(nameM[1].slice(1, -1)) : code;
      var colorM = /color\s*=\s*"([^"]*)"/.exec(args);
      this.characters[code] = {
        name: name,
        color: colorM ? colorM[1] : '#ffffff'
      };
    }
  };

  /* --------------------------------------------------------------------------
     角色名解析
     -------------------------------------------------------------------------- */
  App.prototype.resolveWho = function (who) {
    if (who === null || who === undefined || who === '') return '';
    var code = String(who).trim();

    /* 角色表（CHARACTERS_CONFIG） */
    if (this.actors && this.actors.has(code)) {
      return this.actors.get(code).name;
    }
    /* Character(...) 定义 */
    if (this.characters[code]) return this.characters[code].name;

    /* narrator */
    if (code === 'narrator') return '';

    /* 字符串字面量形式的 who（"同学A" / menu 题面 "???"）
       —— 已经是显示名，原样返回 */
    return code;
  };

  App.prototype.whoColor = function (who) {
    var code = String(who || '').trim();
    if (this.actors && this.actors.has(code)) return this.actors.get(code).color;
    if (this.characters[code]) return this.characters[code].color;
    return '#ffffff';
  };

  /* --------------------------------------------------------------------------
     HUD —— 对应 screens/ui.rpy 的 custom_ui
       右上角：快进 | 自动 | 菜单
       右下角：历史 | 快存 | 快读 | 存档 | 读档
     整层 zoom 0.6（hud_zoom），只在游戏中显示（custom_ui == True）
     -------------------------------------------------------------------------- */
  App.prototype.buildQuickMenu = function () {
    var self = this;

    this.hudEl = document.getElementById('hud');
    this.hudTopEl = document.getElementById('hud-top');
    this.hudBottomEl = document.getElementById('hud-bottom');
    if (!this.hudEl) return;

    /* 幂等：重复调用（boot 重跑 / 热重载）时先清空，避免按钮叠加 */
    this.hudTopEl.innerHTML = '';
    this.hudBottomEl.innerHTML = '';
    this.hudButtons = Object.create(null);

    /* ---- 按钮工厂 ---- */
    function makeBtn(opts) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'hud-btn' + (opts.offsetUp ? ' offset-up' : '');
      btn.setAttribute('aria-label', opts.tip);

      var img = document.createElement('img');
      img.alt = opts.tip;
      img.draggable = false;
      img.src = self.images.url('gui/' + opts.idle, 'image') || '';
      img.onerror = function () {
        /* 缺图退化：显示文字 */
        img.remove();
        btn.textContent = opts.tip;
        btn.style.cssText =
          'padding:10px 16px;border:1px solid rgba(255,255,255,.3);' +
          'border-radius:4px;background:rgba(0,0,0,.45);color:#fff;' +
          'font-family:inherit;font-size:26px;line-height:1;';
      };
      btn.appendChild(img);

      var tip = document.createElement('span');
      tip.className = 'hud-tip';
      tip.textContent = opts.tip;
      btn.appendChild(tip);

      btn._idle = img;
      btn._opts = opts;

      btn.addEventListener('mouseenter', function () {
        self.playUiHover();
        if (opts.hover && !btn.classList.contains('selected')) {
          img.src = self.images.url('gui/' + opts.hover, 'image') || img.src;
        }
      });
      btn.addEventListener('mouseleave', function () {
        img.src = self.images.url(
          'gui/' + (btn.classList.contains('selected') && opts.selectedIdle
            ? opts.selectedIdle
            : opts.idle), 'image') || img.src;
      });
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        self.playUiClick();
        opts.on();
        self.syncHud();
      });

      return btn;
    }

    /* ---- 右上角：快进 / 自动 / 菜单 ---- */
    var skipBtn = makeBtn({
      idle: '快进1.png',
      hover: '快进2.png',
      selectedIdle: '快进2.png',
      tip: '快进模式',
      on: function () { self.toggleSkip(); }
    });
    this.hudTopEl.appendChild(skipBtn);
    this.hudButtons.skip = skipBtn;

    var autoBtn = makeBtn({
      idle: '自动1.png',
      hover: '自动2.png',
      selectedIdle: '自动2.png',
      tip: '自动播放',
      on: function () { self.toggleAuto(); }
    });
    this.hudTopEl.appendChild(autoBtn);
    this.hudButtons.auto = autoBtn;

    var menuBtn = makeBtn({
      idle: '菜单1.png',
      hover: '菜单2.png',
      tip: '系统菜单',
      on: function () { self.openGameMenu(); }
    });
    this.hudTopEl.appendChild(menuBtn);
    this.hudButtons.menu = menuBtn;

    /* ---- 右下角：历史 / 快存 / 快读 / 存档 / 读档 ---- */
    var histBtn = makeBtn({
      idle: 'LOG1.png',
      hover: 'LOG2.png',
      tip: '历史记录',
      on: function () { self.openHistory(); }
    });
    this.hudBottomEl.appendChild(histBtn);

    var qsBtn = makeBtn({
      idle: 'Q.S 1.png',
      hover: 'Q.S 2.png',
      tip: '快速存档',
      on: function () { self.quickSave(); }
    });
    this.hudBottomEl.appendChild(qsBtn);

    var qlBtn = makeBtn({
      idle: 'Q.L 1.png',
      hover: 'Q.L 2.png',
      tip: '快速读取',
      on: function () { self.quickLoad(); }
    });
    this.hudBottomEl.appendChild(qlBtn);

    var sBtn = makeBtn({
      idle: '存档1.png',
      hover: '存档2.png',
      offsetUp: true,
      tip: '打开存档界面',
      on: function () { self.ui.saveLoad.open('save'); }
    });
    this.hudBottomEl.appendChild(sBtn);

    var lBtn = makeBtn({
      idle: '读档1.png',
      hover: '读档2.png',
      offsetUp: true,
      tip: '打开读档界面',
      on: function () { self.ui.saveLoad.open('load'); }
    });
    this.hudBottomEl.appendChild(lBtn);

    this.hudEl.hidden = true;
    this.refreshQuickMenu();

    /* 自检：结构是否齐全（控制台可见，便于排查“看不到 HUD”） */
    if (global.console && global.console.debug) {
      console.debug('[GalGod] HUD 就绪: 右上 ' + this.hudTopEl.children.length +
        ' 个 / 右下 ' + this.hudBottomEl.children.length + ' 个');
    }
  };

  /** 同步按钮的选中态（快进中 / 自动中） */
  App.prototype.syncHud = function () {
    if (!this.hudButtons) return;

    var skipOn = !!(this.vm && this.vm.skipMode);
    var autoOn = !!(this.vm && this.vm.autoMode);

    [['skip', skipOn], ['auto', autoOn]].forEach(function (pair) {
      var btn = this.hudButtons[pair[0]];
      if (!btn) return;
      var on = pair[1];
      btn.classList.toggle('selected', on);
      var opts = btn._opts;
      var file = on && opts.selectedIdle ? opts.selectedIdle : opts.idle;
      var url = this.images.url('gui/' + file, 'image');
      if (url && btn._idle) btn._idle.src = url;
    }, this);
  };

  App.prototype.refreshQuickMenu = function () {
    if (!this.hudEl) return;

    /* 对应 screens/ui.rpy：`if custom_ui:` 才显示整层 HUD。
       剧本里用 `$ custom_ui = False` 关闭（如开场黑白演出段）。 */
    var flag = this.state.getVar('custom_ui');
    var customUiOn = flag === undefined ? true : !!flag;

    /* 调试开关：?hud=1 或 ?hud=force 强制常显，用于排查显示问题 */
    var force = this._forceHud;
    if (force === undefined) {
      var q = parseQuery(global.location.search);
      force = (q.hud === '1' || q.hud === 'force');
      this._forceHud = force;
    }

    var playing = !!(this.vm && this.vm.running) && (customUiOn || force);
    this.hudEl.hidden = !playing;
    if (playing) this.syncHud();
  };

  /* --------------------------------------------------------------------------
     快速存 / 读（对应 QuickSave() / QuickLoad()）
     -------------------------------------------------------------------------- */
  App.prototype.quickSave = function () {
    var ok = this.save.save('quick', 1);
    if (ok) this.hudFlash('⚡ 已快速存档');
  };

  App.prototype.quickLoad = function () {
    var list = this.save.list('quick');
    if (!list.length || list[0].empty) {
      this.hudFlash('快速存档为空', true);
      return;
    }
    this.save.load('quick', 1);
  };

  /** HUD 上方的瞬时提示（对应 Notify） */
  App.prototype.hudFlash = function (msg, isError) {
    if (!this.hudBottomEl) { this.toast(msg); return; }

    var old = this.hudBottomEl.querySelector('.hud-flash');
    if (old) old.remove();

    var el = document.createElement('div');
    el.className = 'hud-flash';
    el.textContent = msg;
    if (isError) el.style.color = '#ffb4ab';
    this.hudBottomEl.appendChild(el);

    setTimeout(function () {
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 1700);
  };

  App.prototype.toggleAuto = function () {
    if (!this.vm) return;
    this.vm.setAuto(!this.vm.autoMode);
    this.toast('自动播放' + (this.vm.autoMode ? '已开启' : '已关闭'));
    this.syncHud();
  };

  App.prototype.toggleSkip = function () {
    if (!this.vm) return;
    this.vm.setSkip(!this.vm.skipMode);
    this.toast('快进' + (this.vm.skipMode ? '已开启' : '已关闭'));
    this.syncHud();
  };

  /* --------------------------------------------------------------------------
     菜单开合
     -------------------------------------------------------------------------- */
  App.prototype.isMenuOpen = function () {
    return !!(
      (this.ui.mainMenu && this.ui.mainMenu.isOpen()) ||
      this.ui.saveLoad.isOpen() ||
      this.ui.config.isOpen() ||
      this.ui.gallery.isOpen() ||
      this.ui.about.isOpen() ||
      this.ui.history.isOpen() ||
      this.ui.confirm.isOpen() ||
      this.gameMenuEl
    );
  };

  /** 调试面板是否打开（F9）。对话/居中文本的输入处理需要据此让路。 */
  App.prototype.isDebugOpen = function () {
    return !!(this.ui.diag && this.ui.diag.open);
  };

  App.prototype.openHistory = function () {
    if (this.ui.history.isOpen()) return;
    this.ui.history.open();
  };

  App.prototype.openGameMenu = function () {
    if (this.isMenuOpen()) return;
    var self = this;

    var root = document.createElement('div');
    root.className = 'menu-screen dim';
    root.id = 'menu-game';

    var wrap = document.createElement('div');
    wrap.style.cssText =
      'flex:1;display:flex;flex-direction:column;align-items:center;' +
      'justify-content:center;gap:22px;';

    var title = document.createElement('div');
    title.className = 'menu-title';
    title.textContent = this.program.gameName || 'GalGod';
    title.style.marginBottom = '26px';
    wrap.appendChild(title);

    var items = [
      { label: '返回游戏', on: function () { self.closeGameMenu(); } },
      { label: '保存游戏', on: function () { self.ui.saveLoad.open('save'); } },
      { label: '读取游戏', on: function () { self.ui.saveLoad.open('load'); } },
      { label: '历史记录', on: function () { self.openHistory(); } },
      { label: '系统设置', on: function () { self.ui.config.open(); } },
      { label: '回到主菜单', on: function () { self.confirmToTitle(); } }
    ];

    items.forEach(function (it) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = it.label;
      b.style.cssText =
        'min-width:300px;height:64px;font-size:23px;font-family:inherit;' +
        'color:#ddd;background:rgba(255,255,255,.06);' +
        'border:1px solid rgba(255,255,255,.18);border-radius:6px;' +
        'cursor:pointer;letter-spacing:2px;transition:all .15s ease;';
      b.addEventListener('mouseenter', function () {
        b.style.background = 'rgba(255,255,255,.16)';
        b.style.color = '#fff';
      });
      b.addEventListener('mouseleave', function () {
        b.style.background = 'rgba(255,255,255,.06)';
        b.style.color = '#ddd';
      });
      b.addEventListener('click', it.on);
      wrap.appendChild(b);
    });

    root.appendChild(wrap);
    this.stage.menusLayer.appendChild(root);
    this.gameMenuEl = root;

    this._gameMenuEsc = function (e) {
      if (e.key === 'Escape') { e.preventDefault(); self.closeGameMenu(); }
    };
    document.addEventListener('keydown', this._gameMenuEsc);
  };

  App.prototype.closeGameMenu = function () {
    if (!this.gameMenuEl) return;
    this.gameMenuEl.parentNode.removeChild(this.gameMenuEl);
    this.gameMenuEl = null;
    if (this._gameMenuEsc) {
      document.removeEventListener('keydown', this._gameMenuEsc);
      this._gameMenuEsc = null;
    }
  };

  App.prototype.closeAllMenus = function () {
    this.closeGameMenu();
    this.ui.saveLoad.close();
    this.ui.config.close();
    this.ui.gallery.close();
    this.ui.about.close();
    this.ui.history.close();
  };

  App.prototype.confirmToTitle = function () {
    var self = this;
    this.ui.confirm.ask('返回主菜单？未保存的进度将丢失。').then(function (yes) {
      if (yes) self.backToTitle();
    });
  };

  /* --------------------------------------------------------------------------
     主菜单 / 标题
     -------------------------------------------------------------------------- */
  App.prototype.showTitle = function () {
    var self = this;
    if (this.ui.mainMenu) return;

    this.vm.running = false;
    this.ui.say.hideBox();
    this.vm.setAuto(false);
    this.vm.setSkip(false);
    this.audio.stop('music', { fadeout: 0.6 });
    this.audio.stop('sound', { fadeout: 0.4 });
    this.audio.stopVoice();
    this.refreshQuickMenu();

    this.ui.mainMenu = new global.RPYMainMenu.MainMenu(this);
    this.ui.mainMenu.show();
  };

  App.prototype.backToTitle = function () {
    this.closeAllMenus();
    if (this.ui.mainMenu) {
      this.ui.mainMenu.hide();
      this.ui.mainMenu = null;
    }
    this.vm.running = false;
    this.vm.frames = [];
    this.state = new global.RPYState.State();
    this.vm.state = this.state;
    this.audio.state = this.state;
    this.stage.state = this.state;
    this.actors.state = this.state;
    this.stage.setBackground(null);
    this.stage.clearCG();
    this.stage.clearOverlay();
    Object.keys(this.stage.spriteEls).forEach(function (code) {
      var el = this.stage.spriteEls[code];
      if (el.parentNode) el.parentNode.removeChild(el);
    }, this);
    this.stage.spriteEls = Object.create(null);
    this.ui.say.hideBox();
    this.state.history = [];
    this.showTitle();
  };

  App.prototype.playMenuMusic = function () {
    if (this._menuMusicStarted) return;
    this._menuMusicStarted = true;

    var self = this;
    var ch = this.audio.menuMusic;
    var url = this.images.url('audio/bgm/BGM_主界面.ogg', 'audio');
    if (!url) return;

    /* images.url 已完成逐段编码，这里不要再编一次 */
    var start = function () {
      ch.play(url, { loop: true, fadein: 1.0 });
    };

    /* 浏览器自动播放策略：未交互前不强行 play，避免 NS_BINDING_ABORTED */
    if (this._userInteracted) {
      start();
    } else {
      this._menuMusicStart = start;
    }
  };

  /** 首次用户交互（点击/按键）：补播被策略拦截的音频与菜单 BGM */
  App.prototype.markUserInteraction = function () {
    if (this._userInteracted) return;
    this._userInteracted = true;

    var start = this._menuMusicStart;
    this._menuMusicStart = null;
    if (start && this.ui.mainMenu && this.ui.mainMenu.isOpen()) start();

    if (this.audio && this.audio.pendingAutoplay) {
      var fn = this.audio.pendingAutoplay;
      this.audio.pendingAutoplay = null;
      fn();
    }
  };

  App.prototype.stopMenuMusic = function () {
    this.audio.menuMusic.stop({ fadeout: 0.5 });
    this._menuMusicStarted = false;
  };

  App.prototype.onStoryEnd = function () {
    this.refreshQuickMenu();
    this.toast('本章结束');
  };

  /* --------------------------------------------------------------------------
     帮助浮层（F1）
     -------------------------------------------------------------------------- */
  App.prototype.showHelp = function () {
    if (this.helpEl) { this.closeHelp(); return; }
    var self = this;

    var root = document.createElement('div');
    root.className = 'menu-screen dim';
    root.style.cssText = 'align-items:center;justify-content:center;';

    var box = document.createElement('div');
    box.style.cssText =
      'min-width:740px;padding:44px 56px;background:rgba(12,12,14,.96);' +
      'border:1px solid rgba(255,255,255,.14);border-radius:10px;' +
      'font-size:17px;line-height:2.1;color:#ddd;';

    var rows = [
      ['左键 / 空格 / 回车', '推进对话；打字中点击立即补全'],
      ['滚轮上滑', '回滚到上一句'],
      ['滚轮下滑', '打开历史记录'],
      ['Esc', '打开游戏菜单'],
      ['Ctrl（按住）', '快进'],
      ['Tab', '切换快进'],
      ['V', '切换自动播放'],
      ['H', '隐藏对话框'],
      ['F1', '显示 / 关闭本帮助'],
      ['F9 或 `', '调试面板：诊断 / 章节跳转 / 变量 / 指令追踪'],
      ['F5', '刷新页面']
    ];

    var html = '<div style="font-size:26px;letter-spacing:4px;margin-bottom:26px">' +
      '操作说明</div><table style="border-collapse:collapse">';
    rows.forEach(function (r) {
      html += '<tr>' +
        '<td style="padding:4px 44px 4px 0;color:#79c0ff;white-space:nowrap">' +
        S.escapeHtml(r[0]) + '</td>' +
        '<td style="padding:4px 0;color:#ccc">' + S.escapeHtml(r[1]) + '</td>' +
        '</tr>';
    });
    html += '</table>' +
      '<div style="margin-top:24px;font-size:14px;color:#666">点击任意处关闭</div>';
    box.innerHTML = html;

    root.appendChild(box);
    this.stage.menusLayer.appendChild(root);
    this.helpEl = root;

    root.addEventListener('click', function () { self.closeHelp(); });
  };

  App.prototype.closeHelp = function () {
    if (!this.helpEl) return;
    if (this.helpEl.parentNode) this.helpEl.parentNode.removeChild(this.helpEl);
    this.helpEl = null;
  };

  /* --------------------------------------------------------------------------
     UI 音效
     -------------------------------------------------------------------------- */
  App.prototype.playUiHover = function () {
    this.playOneShot('audio/fx/btn_Move.ogg', 0.5);
  };

  App.prototype.playUiClick = function () {
    this.playOneShot('audio/fx/btn_Click.ogg', 0.7);
  };

  App.prototype.playOneShot = function (path, vol) {
    var url = this.images.url(path, 'audio');
    if (!url) return;
    url = url.split('/').map(function (s) { return encodeURIComponent(s); }).join('/');
    try {
      var a = global.RPYAudio.createAudioElement();
      a.volume = vol == null ? 0.6 : vol;
      a.play().catch(function () {});
    } catch (e) { /* ignore */ }
  };

  /* --------------------------------------------------------------------------
     工具
     -------------------------------------------------------------------------- */
  App.prototype.toast = function (msg, ms) {
    if (this.ui.toast) this.ui.toast.show(msg, ms);
  };

  App.prototype.chapterTitle = function (label) {
    if (!label) return '';
    return U.CHAPTER_NAMES[label] || label;
  };

  App.prototype.aboutText = function () {
    if (this.program.guiAbout) return this.program.guiAbout;
    return '感谢游玩《GalGod》。\n\n这是一份用浏览器运行的 Ren\'Py 脚本加载器，' +
      '所有剧本与素材均直接来自原作工程目录。';
  };

  App.prototype.stats = function () {
    var self = this;
    if (!self.program) return null;

    var labels = Object.keys(self.program.labels).filter(function (k) {
      return !self.program.labels[k].synthetic;
    });

    var ops = 0;
    Object.keys(self.program.labels).forEach(function (k) {
      ops += self.program.labels[k].ops.length;
    });
    return {
      scripts: self.program.files.length,
      labels: labels.length,
      ops: ops,
      images: Object.keys(self.program.images).length,
      assets: (self.manifest && self.manifest.assets ? self.manifest.assets : []).length
    };
  };

  App.prototype.hideAll = function () {
    this.closeAllMenus();
    if (this.ui.mainMenu) this.ui.mainMenu.hide();
    this.ui.say.hideBox();
    this.ui.centered.hide();
    this.audio.pauseAll();
  };

  App.prototype.showQuitScreen = function () {
    var self = this;
    var root = document.createElement('div');
    root.className = 'menu-screen';
    root.style.cssText =
      'align-items:center;justify-content:center;background:#000;';
    var txt = document.createElement('div');
    txt.style.cssText =
      'text-align:center;color:#888;font-size:22px;line-height:2.2;';
    txt.innerHTML =
      '已退出游戏。<br><br>' +
      '<span style="font-size:17px;color:#555">可以直接关闭此标签页，' +
      '或点击下方按钮重新开始。</span>';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = '重新载入';
    btn.style.cssText =
      'margin-top:36px;padding:14px 40px;font-size:18px;font-family:inherit;' +
      'color:#ddd;background:rgba(255,255,255,.08);' +
      'border:1px solid rgba(255,255,255,.2);border-radius:6px;cursor:pointer;';
    btn.addEventListener('click', function () { global.location.reload(); });

    var wrap = document.createElement('div');
    wrap.style.cssText = 'display:flex;flex-direction:column;align-items:center;';
    wrap.appendChild(txt);
    wrap.appendChild(btn);
    root.appendChild(wrap);
    this.stage.menusLayer.appendChild(root);
  };

  /* --------------------------------------------------------------------------
     查询参数
     -------------------------------------------------------------------------- */
  /** 解析 ?a=1&b=2 */
  function parseQuery(search) {
    var out = {};
    String(search || '').replace(/^\?/, '').split('&').forEach(function (kv) {
      if (!kv) return;
      var i = kv.indexOf('=');
      var k = i < 0 ? kv : kv.slice(0, i);
      var v = i < 0 ? '' : kv.slice(i + 1);
      try {
        out[decodeURIComponent(k)] = decodeURIComponent(v.replace(/\+/g, ' '));
      } catch (e) {
        out[k] = v;
      }
    });
    return out;
  }

  /* --------------------------------------------------------------------------
     预加载角色立绘
     -------------------------------------------------------------------------- */
  App.prototype.preloadCharacters = function () {
    var paths = [];
    var cfg = this.actorConfig || {};
    Object.keys(cfg).forEach(function (code) {
      var ex = cfg[code].expressions || {};
      Object.keys(ex).forEach(function (k) { paths.push(ex[k]); });
    });
    if (!paths.length) return Promise.resolve();
    return this.images.preload(paths);
  };

  /* --------------------------------------------------------------------------
     启动诊断汇总
     -------------------------------------------------------------------------- */
  App.prototype.reportBootDiagnostics = function () {
    var items = [].concat(
      this.program.diagnostics || [],
      this.images.diagnostics || [],
      this.runtimeDiagnostics
    );
    var byKind = Object.create(null);
    items.forEach(function (d) {
      byKind[d.kind] = (byKind[d.kind] || 0) + 1;
    });

    var keys = Object.keys(byKind);
    if (!keys.length) {
      console.log('[GalGod] 解析完成，无诊断问题。');
      return;
    }
    console.group('[GalGod] 启动诊断 ' + items.length + ' 条');
    keys.forEach(function (k) {
      console.log('  ' + k + ': ' + byKind[k]);
    });
    console.log('按 F9 查看详情。');
    console.groupEnd();

    /* 严重问题给一个可点击提示 */
    var serious = (byKind.MISSING_LABEL || 0) + (byKind.SCRIPT_LOAD_ERROR || 0);
    if (serious > 0) {
      this.toast('有 ' + serious + ' 个严重问题，按 F9 查看', 4200);
    }

    /* URL 带 ?strict=1 时直接展开面板 */
    if (/[?&]strict=1/.test(global.location.search)) {
      this.ui.diag.show();
    }
  };

  /* ==========================================================================
     入口
     ========================================================================== */
  function main() {
    var app = new App();
    global.GalGod = app;

    /* 让外部调试方便 */
    global.app = app;

    app.boot().then(function () {
      console.log('[GalGod] ready');
    }).catch(function (err) {
      console.error('[GalGod] boot failed', err);
    });
  }

  /**
   * 浏览器自动播放策略：首个交互前不强行 play()。
   * 交互发生后补播菜单 BGM 与被拦截的音频。
   */
  function bindInteractionUnlock() {
    var handler = function () {
      if (global.GalGod && global.GalGod.markUserInteraction) {
        global.GalGod.markUserInteraction();
      }
    };
    document.addEventListener('pointerdown', handler, { passive: true });
    document.addEventListener('keydown', handler);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      bindInteractionUnlock();
      main();
    });
  } else {
    bindInteractionUnlock();
    main();
  }
})(window);