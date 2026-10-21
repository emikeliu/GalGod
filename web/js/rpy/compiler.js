/* ==========================================================================
   rpy/compiler.js
   把 AST 编译成线性指令流。
   - 每个 label 编译为 {name, ops:[...]}
   - if / menu 在编译期展开成条件跳转
   - 保留 sourceLine 供诊断与存档定位
   ========================================================================== */
(function (global) {
  'use strict';

  function Program(diagnostics) {
    this.labels = Object.create(null);   /* name -> {name, ops, file, line} */
    this.images = Object.create(null);   /* "bg street1_1" -> {expr, file, line} */
    this.defines = [];                   /* {name, value, file, line} */
    this.defaults = [];                  /* {name, value, file, line} */
    this.transforms = Object.create(null);
    this.screens = Object.create(null);  /* name -> {body, file, line} */
    this.diagnostics = diagnostics || [];
    this.files = [];
  }

  function Emitter(program, labelName, file) {
    this.program = program;
    this.labelName = labelName;
    this.file = file;
    this.ops = [];
  }

  /**
   * 解析 camera: 的 ATL 块，提取 zoom / xpos / ypos / ease 时长。
   */
  function parseCameraATL(lines) {
    var out = { zoom: 1, xpos: 0.5, ypos: 0.5, duration: 0 };
    lines.forEach(function (raw) {
      var l = String(raw).trim();
      var m = /^zoom\s+([\d.]+)/.exec(l);
      if (m) { out.zoom = parseFloat(m[1]); return; }
      m = /^xpos\s+([\d.]+)/.exec(l);
      if (m) { out.xpos = parseFloat(m[1]); return; }
      m = /^ypos\s+([\d.]+)/.exec(l);
      if (m) { out.ypos = parseFloat(m[1]); return; }
      m = /^(ease|easein|easeout|linear)\s+([\d.]+)([\s\S]*)$/.exec(l);
      if (m) {
        out.duration = parseFloat(m[2]);
        var rest = m[3] || '';
        var mz = /zoom\s+([\d.]+)/.exec(rest);
        if (mz) out.zoom = parseFloat(mz[1]);
        return;
      }
    });
    return out;
  }

  Emitter.prototype.emit = function (op) {
    op.file = op.file || this.file;
    this.ops.push(op);
    return this.ops.length - 1;
  };
  Emitter.prototype.here = function () {
    return this.ops.length;
  };
  Emitter.prototype.patch = function (idx, target) {
    this.ops[idx].target = target;
  };

  /* --------------------------------------------------------------------------
     编译一个语句列表
     -------------------------------------------------------------------------- */
  Emitter.prototype.compileBlock = function (stmts) {
    for (var i = 0; i < stmts.length; i++) {
      this.compileStatement(stmts[i]);
    }
  };

  Emitter.prototype.compileStatement = function (s) {
    switch (s.type) {

      case 'say':
        this.emit({
          op: 'say',
          who: s.who,
          text: s.text,
          args: s.args,
          line: s.line,
          file: s.file
        });
        break;

      case 'centered':
        this.emit({ op: 'centered', text: s.text, line: s.line, file: s.file });
        break;

      case 'scene':
        this.emit({
          op: 'scene',
          image: s.image,
          transition: s.transition,
          line: s.line,
          file: s.file
        });
        break;

      case 'show':
        this.emit({
          op: 'show',
          image: s.image,
          at: s.at,
          transition: s.transition,
          line: s.line,
          file: s.file
        });
        break;

      case 'hide':
        this.emit({
          op: 'hide',
          image: s.image,
          transition: s.transition,
          line: s.line,
          file: s.file
        });
        break;

      case 'showLayer':
        this.emit({
          op: 'showLayer',
          layer: s.layer,
          transition: s.transition,
          line: s.line,
          file: s.file
        });
        break;

      case 'camera':
        /* camera master at FILTER -> 滤镜；camera: ATL 块 -> 镜头 zoom */
        if (s.transition) {
          this.emit({
            op: 'showLayer',
            layer: s.layer || 'master',
            transition: s.transition,
            line: s.line,
            file: s.file
          });
        } else if (s.atl && s.atl.length) {
          var cam = parseCameraATL(s.atl);
          this.emit({
            op: 'camera',
            zoom: cam.zoom,
            xpos: cam.xpos,
            ypos: cam.ypos,
            duration: cam.duration,
            line: s.line,
            file: s.file
          });
        }
        break;

      case 'showScreen':
        this.emit({
          op: 'showScreen',
          screen: s.screen,
          args: s.args,
          line: s.line,
          file: s.file
        });
        break;

      case 'hideScreen':
        this.emit({ op: 'hideScreen', screen: s.screen, line: s.line, file: s.file });
        break;

      case 'play':
      case 'stop':
      case 'queue':
        this.emit({
          op: s.type,
          channel: s.channel,
          path: s.path,
          opts: s.opts,
          line: s.line,
          file: s.file
        });
        break;

      case 'voice':
        this.emit({ op: 'voice', path: s.path, line: s.line, file: s.file });
        break;

      case 'pause':
        this.emit({
          op: 'pause',
          seconds: s.seconds,
          hard: !!s.hard,
          line: s.line,
          file: s.file
        });
        break;

      case 'with':
        this.emit({
          op: 'with',
          transition: s.transition,
          line: s.line,
          file: s.file
        });
        break;

      case 'window':
        this.emit({
          op: 'window',
          mode: s.mode,
          transition: s.transition,
          line: s.line,
          file: s.file
        });
        break;

      case 'py':
        this.emit({ op: 'py', code: s.code, line: s.line, file: s.file });
        break;

      case 'jump':
        this.emit({ op: 'jump', targetLabel: s.target, line: s.line, file: s.file });
        break;

      case 'call':
        this.emit({
          op: 'call',
          targetLabel: s.target,
          args: s.args,
          line: s.line,
          file: s.file
        });
        break;

      case 'callScreen':
        this.emit({
          op: 'callScreen',
          screen: s.screen,
          args: s.args,
          rawArgs: s.rawArgs,
          line: s.line,
          file: s.file
        });
        break;

      case 'return':
        this.emit({ op: 'return', value: s.value, line: s.line, file: s.file });
        break;

      case 'if':
        this.compileIf(s);
        break;

      case 'menu':
        this.compileMenu(s);
        break;

      case 'define':
        this.program.defines.push({
          name: s.name, value: s.value, file: s.file, line: s.line
        });
        break;

      case 'default':
        this.program.defaults.push({
          name: s.name, value: s.value, file: s.file, line: s.line
        });
        break;

      case 'image':
        this.program.images[s.name] = {
          expr: s.expr, block: s.block, file: s.file, line: s.line
        };
        break;

      case 'transform':
        this.program.transforms[s.name] = {
          params: s.params, body: s.body, file: s.file, line: s.line
        };
        break;

      case 'screen':
        this.program.screens[s.name] = {
          body: s.body, file: s.file, line: s.line
        };
        break;

      case 'label':
        /* 嵌套 label（极少见）：交给顶层处理 */
        this.program.diagnostics.push({
          kind: 'NESTED_LABEL',
          file: s.file,
          line: s.line,
          text: s.name,
          message: '嵌套 label 已按顺序内联处理'
        });
        this.emit({ op: 'labelMarker', name: s.name, line: s.line, file: s.file });
        this.compileBlock(s.body);
        break;

      case 'elif':
      case 'else':
        /* 已被 foldConditionals 吸收，此处不应出现 */
        this.program.diagnostics.push({
          kind: 'ORPHAN_BRANCH',
          file: s.file,
          line: s.line,
          text: s.type,
          message: '孤立的 ' + s.type + '，已忽略'
        });
        break;

      case 'ignore':
        /* 静默跳过；init/style/screen 属预期行为 */
        if (s.reason === 'unknown') {
          this.program.diagnostics.push({
            kind: 'IGNORED_STATEMENT',
            file: s.file,
            line: s.line,
            text: s.text,
            message: '未实现的语句，运行时跳过'
          });
        }
        break;

      default:
        this.program.diagnostics.push({
          kind: 'UNCOMPILED',
          file: s.file,
          line: s.line,
          text: s.type,
          message: '编译器不支持的 AST 类型: ' + s.type
        });
    }
  };

  /* ---- if ---- */
  Emitter.prototype.compileIf = function (s) {
    var endJumps = [];

    for (var i = 0; i < s.branches.length; i++) {
      var br = s.branches[i];
      var jf = this.emit({
        op: 'jumpUnless',
        cond: br.cond,
        target: -1,
        line: s.line,
        file: s.file
      });
      this.compileBlock(br.body);
      if (i < s.branches.length - 1 || s.elseBody) {
        endJumps.push(this.emit({ op: 'jump', target: -1, line: s.line, file: s.file }));
      }
      this.patch(jf, this.here());
    }

    if (s.elseBody) {
      this.compileBlock(s.elseBody);
    }

    var end = this.here();
    for (var k = 0; k < endJumps.length; k++) this.patch(endJumps[k], end);
  };

  /* ---- menu ---- */
  Emitter.prototype.compileMenu = function (s) {
    var items = [];
    var indexOp = this.emit({
      op: 'menu',
      who: s.who,
      caption: s.caption,
      items: items,
      line: s.line,
      file: s.file
    });

    var endJumps = [];
    for (var i = 0; i < s.items.length; i++) {
      var item = s.items[i];
      var entry = {
        text: item.text,
        target: this.here(),
        line: item.line
      };
      items.push(entry);
      this.compileBlock(item.body);
      endJumps.push(this.emit({ op: 'jump', target: -1, line: s.line, file: s.file }));
    }

    var end = this.here();
    for (var k = 0; k < endJumps.length; k++) this.patch(endJumps[k], end);
    this.ops[indexOp].end = end;
  };

  /* --------------------------------------------------------------------------
     顶层编译
     -------------------------------------------------------------------------- */
  function compileFile(program, astBody, file) {
    program.files.push(file);

    /* 先收集非 label 的顶层声明 */
    var emitter = new Emitter(program, '__top__', file);
    var topOps = [];

    for (var i = 0; i < astBody.length; i++) {
      var s = astBody[i];
      if (s.type === 'label') continue;
      emitter.compileStatement(s);
      topOps.push(s);
    }

    /* 顶层可执行语句（如 splashscreen 之前的东西）挂到一个合成 label */
    if (emitter.ops.length) {
      var name = '__top__:' + file;
      program.labels[name] = {
        name: name,
        ops: emitter.ops,
        file: file,
        line: 1,
        synthetic: true
      };
    }

    /* 再编译 label */
    for (var j = 0; j < astBody.length; j++) {
      var lb = astBody[j];
      if (lb.type !== 'label') continue;
      if (program.labels[lb.name] && !program.labels[lb.name].synthetic) {
        program.diagnostics.push({
          kind: 'DUPLICATE_LABEL',
          file: file,
          line: lb.line,
          text: lb.name,
          message: 'label 重复定义，后者覆盖前者'
        });
      }
      var em = new Emitter(program, lb.name, file);
      em.compileBlock(lb.body);
      /* label 结尾隐式 return */
      em.emit({ op: 'return', value: null, line: lb.line, file: file });
      program.labels[lb.name] = {
        name: lb.name,
        ops: em.ops,
        file: file,
        line: lb.line
      };
    }
  }

  /**
   * 解析并编译一组源文件。
   * @param {Array<{path:string, source:string}>} files
   */
  function compileAll(files) {
    var diagnostics = [];
    var program = new Program(diagnostics);

    /* 1) 逐个文件 lex + parse */
    var perFile = [];
    for (var i = 0; i < files.length; i++) {
      var f = files[i];
      var lexed = global.RPYLexer.lex(f.source, f.path);
      var parsed = global.RPYParser.parse(lexed.root, f.path);
      for (var d = 0; d < parsed.diagnostics.length; d++) diagnostics.push(parsed.diagnostics[d]);
      perFile.push({ path: f.path, body: parsed.body });
    }

    /* 2) 按文件顺序生成程序 */
    for (var k = 0; k < perFile.length; k++) {
      compileFile(program, perFile[k].body, perFile[k].path);
    }

    /* 3) 校验 jump/call 目标 */
    var labels = program.labels;
    Object.keys(labels).forEach(function (name) {
      var ops = labels[name].ops;
      for (var i = 0; i < ops.length; i++) {
        var op = ops[i];
        if ((op.op === 'jump' || op.op === 'call') && op.targetLabel) {
          if (!labels[op.targetLabel]) {
            diagnostics.push({
              kind: 'MISSING_LABEL',
              file: op.file,
              line: op.line,
              text: op.targetLabel,
              message: '跳转目标不存在: ' + op.targetLabel
            });
          }
        }
      }
    });

    return program;
  }

  /* --------------------------------------------------------------------------
     反编译辅助：把 ops 转成可读文本（诊断面板用）
     -------------------------------------------------------------------------- */
  function describeOp(op) {
    switch (op.op) {
      case 'say':
        return 'say ' + (op.who ? op.who + ' ' : '') + '"' + op.text.slice(0, 24) + '"';
      case 'scene':   return 'scene ' + (op.image || '(none)');
      case 'show':    return 'show ' + op.image;
      case 'hide':    return 'hide ' + op.image;
      case 'play':    return 'play ' + op.channel + ' ' + (op.path || '');
      case 'stop':    return 'stop ' + op.channel;
      case 'voice':   return 'voice ' + op.path;
      case 'pause':   return 'pause ' + (op.seconds == null ? '(click)' : op.seconds);
      case 'jump':    return 'jump -> ' + (op.targetLabel || ('#' + op.target));
      case 'call':    return 'call -> ' + op.targetLabel;
      case 'menu':    return 'menu (' + (op.items ? op.items.length : 0) + ' 项)';
      case 'py':      return '$ ' + op.code;
      case 'return':  return 'return';
      default:        return op.op;
    }
  }

  global.RPYCompiler = {
    compileAll: compileAll,
    describeOp: describeOp,
    Program: Program
  };
})(window);