/* ==========================================================================
   rpy/parser.js
   把缩进树转换成语句 AST。覆盖本工程实际使用的 Ren'Py 语法子集。
   未知语句不抛异常，产出 {type:'ignore'} 并记录诊断。
   ========================================================================== */
(function (global) {
  'use strict';

  var S = global.RPYStrings;

  /* --------------------------------------------------------------------------
     基础工具
     -------------------------------------------------------------------------- */

  /** 按顶层分隔符切分（忽略括号内与引号内的分隔符） */
  function splitTopLevel(str, sep) {
    var out = [];
    var buf = '';
    var depth = 0;
    var inS = false, inD = false, esc = false;
    for (var i = 0; i < str.length; i++) {
      var c = str[i];
      if (esc) { buf += c; esc = false; continue; }
      if (c === '\\') { buf += c; esc = true; continue; }
      if (inS) { buf += c; if (c === "'") inS = false; continue; }
      if (inD) { buf += c; if (c === '"') inD = false; continue; }
      if (c === "'") { inS = true; buf += c; continue; }
      if (c === '"') { inD = true; buf += c; continue; }
      if (c === '(' || c === '[' || c === '{') { depth++; buf += c; continue; }
      if (c === ')' || c === ']' || c === '}') { depth--; buf += c; continue; }
      if (depth === 0 && c === sep) { out.push(buf); buf = ''; continue; }
      buf += c;
    }
    if (buf.trim() !== '' || out.length) out.push(buf);
    return out;
  }

  /** 找到顶层第一个关键字位置（前后需为空白） */
  function findKeyword(str, kw) {
    var depth = 0;
    var inS = false, inD = false, esc = false;
    for (var i = 0; i < str.length; i++) {
      var c = str[i];
      if (esc) { esc = false; continue; }
      if (c === '\\') { esc = true; continue; }
      if (inS) { if (c === "'") inS = false; continue; }
      if (inD) { if (c === '"') inD = false; continue; }
      if (c === "'") { inS = true; continue; }
      if (c === '"') { inD = true; continue; }
      if (c === '(' || c === '[' || c === '{') { depth++; continue; }
      if (c === ')' || c === ']' || c === '}') { depth--; continue; }
      if (depth !== 0) continue;
      if (str.substr(i, kw.length) === kw) {
        var before = i === 0 ? ' ' : str[i - 1];
        var after = str[i + kw.length] || ' ';
        if (/\s/.test(before) && /\s/.test(after)) return i;
      }
    }
    return -1;
  }

  /** 解析 NAME(args) 形式，返回 {name, args:[...], raw} */
  function parseCall(expr) {
    var s = String(expr).trim();
    var m = /^([A-Za-z_][\w.]*)\s*\(([\s\S]*)\)$/.exec(s);
    if (!m) return { name: s, args: [], raw: s, isCall: false };
    var argStr = m[2].trim();
    var args = argStr ? splitTopLevel(argStr, ',').map(function (a) { return a.trim(); })
                      : [];
    return { name: m[1], args: args, raw: s, isCall: true };
  }

  /** 解析参数列表 "a, b=1" -> {positional:[], kwargs:{}} */
  function parseArgs(argStr) {
    var pos = [];
    var kw = {};
    if (!argStr || !argStr.trim()) return { positional: pos, kwargs: kw };
    splitTopLevel(argStr, ',').forEach(function (piece) {
      var p = piece.trim();
      if (!p) return;
      var idx = -1, depth = 0, inS = false, inD = false, esc = false;
      for (var i = 0; i < p.length; i++) {
        var c = p[i];
        if (esc) { esc = false; continue; }
        if (c === '\\') { esc = true; continue; }
        if (inS) { if (c === "'") inS = false; continue; }
        if (inD) { if (c === '"') inD = false; continue; }
        if (c === "'") { inS = true; continue; }
        if (c === '"') { inD = true; continue; }
        if ('([{'.indexOf(c) >= 0) depth++;
        else if (')]}'.indexOf(c) >= 0) depth--;
        else if (c === '=' && depth === 0) { idx = i; break; }
      }
      if (idx > 0) {
        kw[p.slice(0, idx).trim()] = p.slice(idx + 1).trim();
      } else {
        pos.push(p);
      }
    });
    return { positional: pos, kwargs: kw };
  }

  /** 是否为字符串字面量，返回内容或 null */
  function asString(token) {
    var t = String(token).trim();
    if (t.length >= 2 && t[0] === '"' && t[t.length - 1] === '"') {
      return S.unescapeRpy(t.slice(1, -1));
    }
    if (t.length >= 2 && t[0] === "'" && t[t.length - 1] === "'") {
      return S.unescapeRpy(t.slice(1, -1));
    }
    return null;
  }

  /* --------------------------------------------------------------------------
     转场解析：dissolve / Dissolve(2.0) / flash / vpunch / None
     -------------------------------------------------------------------------- */
  function parseTransition(token) {
    if (!token) return null;
    var t = String(token).trim();
    if (!t || t === 'None') return null;
    var call = parseCall(t);
    var name = call.name.split('.').pop();
    var lower = name.toLowerCase();
    var duration = null;
    if (call.args.length) {
      var d = parseFloat(call.args[0]);
      if (!isNaN(d)) duration = d;
    }
    var map = {
      dissolve: { kind: 'dissolve', duration: duration == null ? 0.5 : duration },
      fade: { kind: 'fade', duration: duration == null ? 0.5 : duration },
      flash: { kind: 'flash', duration: 0.6 },
      vpunch: { kind: 'vpunch', duration: 0.32 },
      hpunch: { kind: 'hpunch', duration: 0.32 },
      pixellate: { kind: 'pixellate', duration: 0.9 },
      fadein: { kind: 'fadein', duration: duration == null ? 0.5 : duration },
      fadeout: { kind: 'fadeout', duration: duration == null ? 0.5 : duration },
      forced_dissolve: { kind: 'forced_dissolve', duration: duration == null ? 1 : duration },
      memory_filter: { kind: 'filter', filter: 'memory' },
      gray_filter: { kind: 'filter', filter: 'gray' },
      reset_filter: { kind: 'filter', filter: 'reset' }
    };
    if (map[lower]) {
      var r = {};
      for (var k in map[lower]) r[k] = map[lower][k];
      r.name = name;
      return r;
    }
    return { kind: 'dissolve', duration: 0.5, name: name, unknown: true };
  }

  /* --------------------------------------------------------------------------
     say 语句识别
     "文本"                       -> 旁白
     cz "文本"                    -> 角色
     cz "文本" (who_color="#fff")  -> 带参数
     -------------------------------------------------------------------------- */
  var STR_LIT = '("(?:[^"\\\\]|\\\\.)*"|\'(?:[^\'\\\\]|\\\\.)*\')';

  function parseSay(text) {
    /* 形式 1：cz "台词"  —— who 是标识符 */
    var m = new RegExp('^([A-Za-z_][\\w.]*)\\s+' + STR_LIT + '\\s*(\\([\\s\\S]*\\))?$').exec(text);
    if (m) {
      var str = asString(m[2]);
      if (str === null) return null;
      return {
        who: m[1],
        text: str,
        args: m[3] ? parseArgs(m[3].slice(1, -1)) : { positional: [], kwargs: {} }
      };
    }

    /* 形式 2："同学A" "台词"  —— who 是字符串字面量
       对应 scenes/1_2.rpy 里未定义角色时的写法 */
    m = new RegExp('^' + STR_LIT + '\\s+' + STR_LIT + '\\s*(\\([\\s\\S]*\\))?$').exec(text);
    if (m) {
      var whoStr = asString(m[1]);
      var whatStr = asString(m[2]);
      if (whoStr === null || whatStr === null) return null;
      return {
        who: whoStr,
        whoIsLiteral: true,
        text: whatStr,
        args: m[3] ? parseArgs(m[3].slice(1, -1)) : { positional: [], kwargs: {} }
      };
    }

    /* 形式 3："台词"  —— 旁白 */
    var only = asString(text);
    if (only !== null) {
      return { who: null, text: only, args: { positional: [], kwargs: {} } };
    }
    return null;
  }

  /* --------------------------------------------------------------------------
     主解析
     -------------------------------------------------------------------------- */
  function Parser(file, diagnostics) {
    this.file = file;
    this.diags = diagnostics || [];
  }

  Parser.prototype.diag = function (node, kind, msg) {
    this.diags.push({
      kind: kind,
      file: this.file,
      line: node ? node.line : 0,
      text: node ? node.text : '',
      message: msg
    });
  };

  Parser.prototype.parseBlock = function (children) {
    var out = [];
    for (var i = 0; i < children.length; i++) {
      var stmts = this.parseStatement(children[i]);
      if (!stmts) continue;
      if (Array.isArray(stmts)) {
        for (var j = 0; j < stmts.length; j++) out.push(stmts[j]);
      } else {
        out.push(stmts);
      }
    }
    return out;
  };

  Parser.prototype.parseStatement = function (node) {
    var text = node.text;
    var self = this;

    /* ---- label ---- */
    var m = /^label\s+([A-Za-z_][\w.]*)\s*(\([^)]*\))?\s*:$/.exec(text);
    if (m) {
      return {
        type: 'label',
        name: m[1],
        params: m[2] ? m[2].slice(1, -1) : '',
        body: self.parseBlock(node.children),
        line: node.line,
        file: self.file
      };
    }

    /* ---- init / python / screen / style / transform 等：跳过整块 ---- */
    if (/^(init\b|screen\s|style\s|python\s*:|init\s+python\s*:|layeredimage\s|translate\s|testcase\s)/.test(text)) {
      return self.handleDeclarative(node);
    }

    /* ---- define ---- */
    m = /^define\s+([\w.]+)\s*=\s*([\s\S]+)$/.exec(text);
    if (m) {
      return { type: 'define', name: m[1], value: m[2].trim(), line: node.line, file: self.file };
    }

    /* ---- default ---- */
    m = /^default\s+([\w.]+)\s*=\s*([\s\S]+)$/.exec(text);
    if (m) {
      return { type: 'default', name: m[1], value: m[2].trim(), line: node.line, file: self.file };
    }

    /* ---- image ---- */
    m = /^image\s+([^\s=]+(?:\s+[^\s=]+)*)\s*=\s*([\s\S]+)$/.exec(text);
    if (m) {
      return {
        type: 'image',
        name: m[1].trim(),
        expr: m[2].trim(),
        line: node.line,
        file: self.file
      };
    }
    m = /^image\s+([^\s=]+(?:\s+[^\s=]+)*)\s*:$/.exec(text);
    if (m) {
      return {
        type: 'image',
        name: m[1].trim(),
        expr: null,
        block: node.children.length ? '(block)' : null,
        line: node.line,
        file: self.file
      };
    }

    /* ---- transform ---- */
    m = /^transform\s+([\w.]+)\s*(\([^)]*\))?\s*:$/.exec(text);
    if (m) {
      return {
        type: 'transform',
        name: m[1],
        params: m[2] ? m[2].slice(1, -1) : '',
        body: node.children.map(function (c) { return c.text; }),
        line: node.line,
        file: self.file
      };
    }

    /* ---- scene ---- */
    if (/^scene(\s|$)/.test(text)) return self.parseScene(node);

    /* ---- show ---- */
    if (/^show(\s|$)/.test(text)) return self.parseShow(node);

    /* ---- hide ---- */
    if (/^hide(\s|$)/.test(text)) return self.parseHide(node);

    /* ---- play / stop / queue ---- */
    m = /^(play|stop|queue)\s+(music|sound|voice|movie|menu_music|audio|ambient)\b([\s\S]*)$/.exec(text);
    if (m) return self.parseAudio(node, m[1], m[2], m[3]);

    /* ---- voice ---- */
    m = /^voice\s+([\s\S]+)$/.exec(text);
    if (m) {
      /* 注意：键名必须是 path，file 已被占用为「源文件路径」 */
      var voiceArg = m[1].trim();
      var voicePath = asString(voiceArg);
      return {
        type: 'voice',
        path: voicePath === null ? voiceArg : voicePath,
        line: node.line,
        file: self.file
      };
    }

    /* ---- pause ---- */
    m = /^pause\s+([\d.]+)?([\s\S]*)$/.exec(text);
    if (m) {
      return {
        type: 'pause',
        seconds: m[1] ? parseFloat(m[1]) : null,
        hard: /hard\s*=\s*True/.test(text),
        line: node.line,
        file: self.file
      };
    }

    /* ---- with ---- */
    m = /^with\s+([\s\S]+)$/.exec(text);
    if (m) {
      return {
        type: 'with',
        transition: parseTransition(m[1]),
        line: node.line,
        file: self.file
      };
    }

    /* ---- window ---- */
    m = /^window\s+(hide|show|auto)([\s\S]*)$/.exec(text);
    if (m) {
      return {
        type: 'window',
        mode: m[1],
        transition: /with\s+(\w+)/.test(m[2])
          ? parseTransition(/with\s+([\w.]+)/.exec(m[2])[1])
          : null,
        line: node.line,
        file: self.file
      };
    }

    /* ---- $ 语句 ---- */
      m = /^\$\s*([\s\S]+)$/.exec(text);
      if (m) {
        return { type: 'py', code: m[1].trim(), line: node.line, file: self.file };
      }
  
      /* ---- if / elif / else ---- */
      if (/^if\s+/.test(text)) return self.parseIf(node);
  
      m = /^elif\s+([\s\S]+):\s*$/.exec(text);
      if (m) {
        return {
          type: 'elif',
          __pendingElif: m[1].trim(),
          body: self.parseBlock(node.children),
          line: node.line,
          file: self.file
        };
      }
  
      if (/^else\s*:\s*$/.test(text)) {
        return {
          type: 'else',
          __pendingElse: true,
          body: self.parseBlock(node.children),
          line: node.line,
          file: self.file
        };
      }

    /* ---- menu ---- */
    if (/^menu\s*(\([^)]*\))?\s*:$/.test(text)) return self.parseMenu(node);

    /* ---- jump ---- */
    m = /^jump\s+([\w.]+)/.exec(text);
    if (m) {
      return { type: 'jump', target: m[1], line: node.line, file: self.file };
    }

    /* ---- call ---- */
    m = /^call\s+screen\s+([\w.]+)\s*(\([\s\S]*\))?\s*$/.exec(text);
    if (m) {
      return {
        type: 'callScreen',
        screen: m[1],
        args: m[2] ? parseArgs(m[2].slice(1, -1)) : { positional: [], kwargs: {} },
        rawArgs: m[2] || '',
        line: node.line,
        file: self.file
      };
    }
    m = /^call\s+([\w.]+)\s*(\([\s\S]*\))?\s*(?:from\s+[\w.]+)?\s*$/.exec(text);
    if (m) {
      return {
        type: 'call',
        target: m[1],
        args: m[2] ? parseArgs(m[2].slice(1, -1)) : { positional: [], kwargs: {} },
        line: node.line,
        file: self.file
      };
    }

    /* ---- return ---- */
    if (/^return(\s|$)/.test(text)) {
      m = /^return\s+([\s\S]+)$/.exec(text);
      return {
        type: 'return',
        value: m ? m[1].trim() : null,
        line: node.line,
        file: self.file
      };
    }

    /* ---- centered ---- */
    m = /^centered\s+([\s\S]+)$/.exec(text);
    if (m) {
      var centeredText = asString(m[1]);
      if (centeredText !== null) {
        return { type: 'centered', text: centeredText, line: node.line, file: self.file };
      }
    }

    /* ---- pass ---- */
    if (/^pass\s*$/.test(text)) {
      return { type: 'ignore', reason: 'pass', line: node.line, file: self.file };
    }

    /* ---- camera master / camera master at T / camera: (ATL 块) ---- */
    if (/^camera(\s|:|$)/.test(text)) {
      var camRaw = text.replace(/^camera\s*/, '');

      /* camera: 后面跟 ATL 块（zoom / xpos / ypos / ease ...） */
      if (/^camera\s*:\s*$/.test(text) || /^camera\s*:\s*$/.test(text.trim())) {
        return {
          type: 'camera',
          layer: 'master',
          atl: node.children.map(function (c) { return c.text; }),
          transition: null,
          line: node.line,
          file: self.file
        };
      }

      var camAt = null;
      var camAtIdx = findKeyword(camRaw, 'at');
      if (camAtIdx >= 0) {
        camAt = parseTransition(camRaw.slice(camAtIdx + 2).trim());
        camRaw = camRaw.slice(0, camAtIdx);
      }
      return {
        type: 'camera',
        layer: camRaw.trim() || 'master',
        atl: node.children.length
          ? node.children.map(function (c) { return c.text; })
          : null,
        transition: camAt,
        line: node.line,
        file: self.file
      };
    }

    /* ---- show screen / hide screen 已在 show/hide 中处理 ---- */

    /* ---- 其他 screen-language 语句：整体跳过 ---- */
    if (/^(nvl\s|window\s|key\s|timer\s|add\s|text\s|fixed\s|vbox\s|hbox\s|frame\s|button\s|imagebutton\s|use\s|for\s|while\s|if\s|layeredimage\s|imagebutton\s|bar\s|side\s|grid\s|viewport\s|transclude\s|on\s|at\s|contains\s|parallel\s|repeat\s|block\s|ease\w*\s|linear\s|pause\s|function\s|showif\s|hotspot\s|imagemap\s|label\s)/.test(text)) {
      return { type: 'ignore', reason: 'screen-language', line: node.line, file: self.file };
    }

    /* ---- 字典/结构残留（跨行字典被合并后的残余） ---- */
    if (/^[}\]),]/.test(text) || /^["'][^"']*["']\s*:/.test(text)) {
      return { type: 'ignore', reason: 'structural', line: node.line, file: self.file };
    }

    /* ---- say ---- */
    var say = parseSay(text);
    if (say) {
      say.type = 'say';
      say.line = node.line;
      say.file = self.file;
      return say;
    }

    self.diag(node, 'UNKNOWN_STATEMENT', '无法识别的语句，已跳过');
    return { type: 'ignore', reason: 'unknown', line: node.line, file: self.file, text: text };
  };

  /* ---- init python / screen 等声明式语句 ---- */
  Parser.prototype.handleDeclarative = function (node) {
    var text = node.text;

    /* init python: 里的 default/define 仍然要收集（如 global_actor_settings） */
    if (/^init\b/.test(text) && /python/.test(text)) {
      return { type: 'ignore', reason: 'init-python', line: node.line, file: this.file };
    }
    if (/^init\b/.test(text)) {
      return { type: 'ignore', reason: 'init', line: node.line, file: this.file };
    }
    if (/^screen\s+([\w.]+)/.test(text)) {
      var mm = /^screen\s+([\w.]+)/.exec(text);
      return {
        type: 'screen',
        name: mm[1],
        body: node.children.map(function (c) { return c.text; }),
        line: node.line,
        file: this.file
      };
    }
    if (/^style\s/.test(text)) {
      return { type: 'ignore', reason: 'style', line: node.line, file: this.file };
    }
    return { type: 'ignore', reason: 'declarative', line: node.line, file: this.file };
  };

  /* ---- scene ---- */
  Parser.prototype.parseScene = function (node) {
    var text = node.text.replace(/^scene\s*/, '');
    var transition = null;
    var wi = findKeyword(text, 'with');
    if (wi >= 0) {
      transition = parseTransition(text.slice(wi + 4));
      text = text.slice(0, wi);
    }
    var name = text.trim();
    if (!name) {
      return {
        type: 'scene',
        image: null,
        transition: transition,
        line: node.line,
        file: this.file
      };
    }
    return {
      type: 'scene',
      image: name,
      transition: transition,
      line: node.line,
      file: this.file
    };
  };

  /* ---- show ---- */
  Parser.prototype.parseShow = function (node) {
    var raw = node.text.replace(/^show\s*/, '');

    /* show screen NAME(args) */
    var m = /^screen\s+([\w.]+)\s*(\([\s\S]*\))?\s*$/.exec(raw);
    if (m) {
      return {
        type: 'showScreen',
        screen: m[1],
        args: m[2] ? parseArgs(m[2].slice(1, -1)) : { positional: [], kwargs: {} },
        line: node.line,
        file: this.file
      };
    }

    /* show layer master at T */
    m = /^layer\s+([\w.]+)([\s\S]*)$/.exec(raw);
    if (m) {
      var at = null;
      var ai = findKeyword(m[2], 'at');
      if (ai >= 0) at = parseTransition(m[2].slice(ai + 2).trim());
      return {
        type: 'showLayer',
        layer: m[1],
        transition: at,
        line: node.line,
        file: this.file
      };
    }

    var transition = null;
    var atList = [];

    var withIdx = findKeyword(raw, 'with');
    if (withIdx >= 0) {
      transition = parseTransition(raw.slice(withIdx + 4));
      raw = raw.slice(0, withIdx);
    }
    var atIdx = findKeyword(raw, 'at');
    if (atIdx >= 0) {
      var atPart = raw.slice(atIdx + 2).trim();
      raw = raw.slice(0, atIdx);
      atList = splitTopLevel(atPart, ',').map(function (a) { return a.trim(); }).filter(Boolean);
    }
    ['behind', 'onlayer', 'as', 'zorder'].forEach(function (kw) {
      var i = findKeyword(raw, kw);
      if (i >= 0) raw = raw.slice(0, i);
    });

    return {
      type: 'show',
      image: raw.trim(),
      at: atList,
      transition: transition,
      line: node.line,
      file: this.file
    };
  };

  /* ---- hide ---- */
  Parser.prototype.parseHide = function (node) {
    var raw = node.text.replace(/^hide\s*/, '');
    var m = /^screen\s+([\w.]+)/.exec(raw);
    if (m) {
      return { type: 'hideScreen', screen: m[1], line: node.line, file: this.file };
    }
    var transition = null;
    var wi = findKeyword(raw, 'with');
    if (wi >= 0) {
      transition = parseTransition(raw.slice(wi + 4));
      raw = raw.slice(0, wi);
    }
    return {
      type: 'hide',
      image: raw.trim(),
      transition: transition,
      line: node.line,
      file: this.file
    };
  };

  /* ---- play / stop / queue ---- */
  Parser.prototype.parseAudio = function (node, verb, channel, rest) {
    var opts = { loop: false, fadein: 0, fadeout: 0, volume: null, ifChanged: false };
    var file = null;
    var r = rest.trim();

    if (/^loop\b/.test(r)) { opts.loop = true; r = r.replace(/^loop\s*/, ''); }
    if (/^noloop\b/.test(r)) { r = r.replace(/^noloop\s*/, ''); }

    /* fadein / fadeout / volume / if_changed 是「键 值」形式 */
    r = r.replace(/\bfadein\s+([\d.]+)/g, function (_, v) { opts.fadein = parseFloat(v); return ''; });
    r = r.replace(/\bfadeout\s+([\d.]+)/g, function (_, v) { opts.fadeout = parseFloat(v); return ''; });
    r = r.replace(/\bvolume\s+([\d.]+)/g, function (_, v) { opts.volume = parseFloat(v); return ''; });
    r = r.replace(/\bif_changed\b/g, function () { opts.ifChanged = true; return ''; });
    r = r.replace(/\bloop\b/g, function () { opts.loop = true; return ''; });

    /* 关键：路径要去掉引号。r 形如 `"audio/bgm/BGM_月幕.ogg"  ` */
    var tail = r.trim();
    var tailStr = asString(tail);
    file = (tailStr !== null ? tailStr : tail) || null;

    return {
      type: verb === 'play' ? 'play' : (verb === 'stop' ? 'stop' : 'queue'),
      channel: channel,
      path: file,
      opts: opts,
      line: node.line,
      srcFile: this.file
    };
  };

  /* ---- if / elif / else ---- */
  Parser.prototype.parseIf = function (node) {
    var branches = [];
    var elseBody = null;

    var cond = node.text.replace(/^if\s+/, '').replace(/:\s*$/, '');
    var current = { cond: cond.trim(), body: this.parseBlock(node.children) };
    branches.push(current);

    /* 兄弟节点在 lexer 里是同级，需要由上层把 elif/else 交给我 */
    return {
      type: 'if',
      branches: branches,
      elseBody: elseBody,
      line: node.line,
      file: this.file
    };
  };

  /* ---- menu ---- */
  Parser.prototype.parseMenu = function (node) {
    var caption = null;
    var who = null;
    var items = [];

    for (var i = 0; i < node.children.length; i++) {
      var child = node.children[i];
      var t = child.text;

      if (/:\s*$/.test(t)) {
        /* 选项："文本": */
        var label = asString(t.replace(/:\s*$/, '').trim());
        if (label === null) {
          /* 可能是 "who" "text": 形式 */
          var parts = splitTopLevel(t.replace(/:\s*$/, ''), ' ');
          label = asString(t.replace(/:\s*$/, '').trim());
        }
        items.push({
          text: label === null ? t.replace(/:\s*$/, '').trim() : label,
          body: this.parseBlock(child.children),
          line: child.line
        });
        continue;
      }

      var say = parseSay(t);
      if (say) {
        /* menu 的题面 */
        who = say.who;
        caption = say.text;
        continue;
      }
      this.diag(child, 'MENU_UNEXPECTED', 'menu 中无法识别的语句');
    }

    return {
      type: 'menu',
      who: who,
      caption: caption,
      items: items,
      line: node.line,
      file: this.file
    };
  };

  /* --------------------------------------------------------------------------
     对 if/elif/else 的兄弟节点做后处理
     -------------------------------------------------------------------------- */
  function foldConditionals(stmts, diag) {
    var out = [];
    for (var i = 0; i < stmts.length; i++) {
      var s = stmts[i];
      if (s.type === 'if') {
        /* 收集紧随其后的 elif / else（解析阶段它们会作为独立 ignore 或节点出现） */
        var j = i + 1;
        while (j < stmts.length) {
          var n = stmts[j];
          if (n && n.__pendingElif !== undefined) {
            s.branches.push({ cond: n.__pendingElif, body: n.body });
            j++;
            continue;
          }
          if (n && n.__pendingElse) {
            s.elseBody = n.body;
            j++;
            continue;
          }
          break;
        }
        i = j - 1;
      }
      out.push(s);
    }
    return out;
  }

  global.RPYParser = {
    parse: function (root, file) {
      var diagnostics = [];
      var p = new Parser(file, diagnostics);
      var body = p.parseBlock(root.children);
      body = foldConditionals(body, diagnostics);
      return { body: body, diagnostics: diagnostics };
    },
    /* 导出给编译器/测试使用 */
    splitTopLevel: splitTopLevel,
    findKeyword: findKeyword,
    parseCall: parseCall,
    parseArgs: parseArgs,
    asString: asString,
    parseTransition: parseTransition,
    parseSay: parseSay,
    Parser: Parser
  };
})(window);