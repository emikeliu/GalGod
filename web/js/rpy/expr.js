/* ==========================================================================
   rpy/expr.js
   受限表达式求值器。
   不使用 eval / new Function —— 手写 tokenizer + Pratt parser，
   只支持本工程剧本实际出现的语法：
     字面量、变量、属性/索引、调用、算术、比较、布尔、三元、in、not in
   所有函数调用走白名单（ctx.call），未知名字返回 undefined 并记诊断。
   ========================================================================== */
(function (global) {
  'use strict';

  /* --------------------------------------------------------------------------
     Tokenizer
     -------------------------------------------------------------------------- */
  var T_NUM = 'num', T_STR = 'str', T_ID = 'id', T_OP = 'op',
      T_EOF = 'eof';

  var OPS = [
    '**', '//', '==', '!=', '<=', '>=', '+=', '-=', '*=', '/=', '<<', '>>',
    '+', '-', '*', '/', '%', '<', '>', '=', '(', ')', '[', ']', '{', '}',
    ',', ':', '.', '?', '!', '&', '|', '^', '~'
  ];

  function tokenize(src, diag) {
    var toks = [];
    var i = 0;
    var n = src.length;
    var inS = false, inD = false, esc = false;
    while (i < n) {
      var c = src[i];
      if (c === ' ' || c === '\t' || c === '\n' || c === '\r') { i++; continue; }

      /* 字符串 */
      if (c === '"' || c === "'") {
        var quote = c;
        var start = i;
        i++;
        var buf = '';
        var closed = false;
        while (i < n) {
          var ch = src[i];
          if (ch === '\\') { buf += ch + (src[i + 1] || ''); i += 2; continue; }
          if (ch === quote) {
            /* 相邻字符串字面量拼接：'a' 'b' */
            i++;
            closed = true;
            break;
          }
          buf += ch;
          i++;
        }
        if (!closed && diag) diag('UNTERMINATED_STRING', start, '字符串未闭合');
        toks.push({ t: T_STR, v: buf, start: start });
        continue;
      }

      /* 数字 */
      if (/[0-9]/.test(c) || (c === '.' && /[0-9]/.test(src[i + 1] || ''))) {
        var s = i;
        while (i < n && /[0-9.eE]/.test(src[i])) {
          if ((src[i] === 'e' || src[i] === 'E') && /[+-]/.test(src[i + 1] || '')) i++;
          i++;
        }
        toks.push({ t: T_NUM, v: parseFloat(src.slice(s, i)), start: s });
        continue;
      }

      /* 标识符 */
      if (/[A-Za-z_\u4e00-\u9fff]/.test(c)) {
        var is = i;
        while (i < n && /[A-Za-z0-9_\u4e00-\u9fff]/.test(src[i])) i++;
        toks.push({ t: T_ID, v: src.slice(is, i), start: is });
        continue;
      }

      /* 运算符 */
      var matched = null;
      for (var k = 0; k < OPS.length; k++) {
        if (src.substr(i, OPS[k].length) === OPS[k]) { matched = OPS[k]; break; }
      }
      if (matched) {
        toks.push({ t: T_OP, v: matched, start: i });
        i += matched.length;
        continue;
      }

      /* 未知字符：跳过并记录 */
      if (diag) diag('UNKNOWN_CHAR', i, '无法识别的字符: ' + c);
      i++;
    }
    toks.push({ t: T_EOF, v: null, start: n });
    return toks;
  }

  /* --------------------------------------------------------------------------
     Parser (Pratt)
     -------------------------------------------------------------------------- */
  var BP = {
    '?': 5,
    'or': 10,
    'and': 20,
    '|': 25,
    '^': 27,
    '&': 30,
    '==': 40, '!=': 40, '<': 40, '>': 40, '<=': 40, '>=': 40,
    'in': 40, 'not in': 40, 'is': 40, 'is not': 40,
    '<<': 50, '>>': 50,
    '+': 60, '-': 60,
    '*': 70, '/': 70, '//': 70, '%': 70,
    '**': 80
  };

  function ExprParser(toks) {
    this.toks = toks;
    this.pos = 0;
  }

  ExprParser.prototype.peek = function (offset) {
    return this.toks[this.pos + (offset || 0)];
  };
  ExprParser.prototype.next = function () {
    return this.toks[this.pos++];
  };
  ExprParser.prototype.expect = function (t, v) {
    var tok = this.peek();
    if (tok.t !== t || (v !== undefined && tok.v !== v)) {
      throw new Error('期望 ' + v + '，得到 ' + (tok.v === null ? 'EOF' : tok.v));
    }
    return this.next();
  };

  ExprParser.prototype.parseExpr = function (minBp) {
    minBp = minBp || 0;
    var left = this.parsePrefix();

    for (;;) {
      var tok = this.peek();
      if (tok.t === T_EOF) break;

      /* 后缀：调用 / 索引 / 属性 */
      if (tok.t === T_OP && tok.v === '(') { left = this.parseCallTail(left); continue; }
      if (tok.t === T_OP && tok.v === '[') { left = this.parseIndexTail(left); continue; }
      if (tok.t === T_OP && tok.v === '.') {
        this.next();
        var name = this.next();
        left = { k: 'attr', obj: left, name: name.v };
        continue;
      }

      /* 中缀 */
      var op = tok.v;
      if (tok.t === T_ID && (op === 'and' || op === 'or' || op === 'in' || op === 'is')) {
        /* not in / is not */
        if (op === 'in' || op === 'is') {
          var nx = this.peek(1);
          if (nx && nx.t === T_ID && nx.v === 'not') op = op + ' not';
        }
      } else if (tok.t === T_ID && op === 'not') {
        var nx2 = this.peek(1);
        if (nx2 && nx2.t === T_ID && nx2.v === 'in') op = 'not in';
        else break;
      } else if (tok.t !== T_OP) {
        break;
      }

      var bp = BP[op];
      if (bp === undefined) break;
      if (bp < minBp) break;

      this.next();
      if (op === 'not in') this.next();
      if (op === 'in not') this.next();      /* 兼容写错的顺序 */
      if (op === 'is not') this.next();

      var right = this.parseExpr(bp + 1);
      left = { k: 'bin', op: op, l: left, r: right };
    }
    return left;
  };

  ExprParser.prototype.parsePrefix = function () {
    var tok = this.next();

    if (tok.t === T_NUM) return { k: 'lit', v: tok.v };
    if (tok.t === T_STR) {
      /* 相邻字符串自动拼接 */
      var str = tok.v;
      while (this.peek().t === T_STR) str += this.next().v;
      return { k: 'lit', v: global.RPYStrings.unescapeRpy(str) };
    }
    if (tok.t === T_ID) {
      if (tok.v === 'True')  return { k: 'lit', v: true };
      if (tok.v === 'False') return { k: 'lit', v: false };
      if (tok.v === 'None')  return { k: 'lit', v: null };
      if (tok.v === 'not') {
        return { k: 'unary', op: 'not', e: this.parseExpr(BP['and']) };
      }
      return { k: 'name', v: tok.v };
    }
    if (tok.t === T_OP) {
      if (tok.v === '-') return { k: 'unary', op: '-', e: this.parseExpr(75) };
      if (tok.v === '+') return this.parseExpr(75);
      if (tok.v === '(') {
        /* 括号表达式或元组 */
        var items = [];
        if (this.peek().v !== ')') {
          items.push(this.parseExpr(0));
          while (this.peek().v === ',') {
            this.next();
            if (this.peek().v === ')') break;
            items.push(this.parseExpr(0));
          }
        }
        this.expect(T_OP, ')');
        return items.length === 1 ? items[0] : { k: 'tuple', items: items };
      }
      if (tok.v === '[') {
        var arr = [];
        if (this.peek().v !== ']') {
          arr.push(this.parseExpr(0));
          while (this.peek().v === ',') {
            this.next();
            if (this.peek().v === ']') break;
            arr.push(this.parseExpr(0));
          }
        }
        this.expect(T_OP, ']');
        return { k: 'list', items: arr };
      }
      if (tok.v === '{') {
        var pairs = [];
        if (this.peek().v !== '}') {
          pairs.push([this.parseExpr(0), (function () {
            this.expect(T_OP, ':');
            return this.parseExpr(0);
          }).call(this)]);
          while (this.peek().v === ',') {
            this.next();
            if (this.peek().v === '}') break;
            var key = this.parseExpr(0);
            this.expect(T_OP, ':');
            pairs.push([key, this.parseExpr(0)]);
          }
        }
        this.expect(T_OP, '}');
        return { k: 'dict', pairs: pairs };
      }
    }
    throw new Error('无法解析的表达式片段: ' + (tok.v === null ? 'EOF' : tok.v));
  };

  ExprParser.prototype.parseCallTail = function (callee) {
    this.expect(T_OP, '(');
    var args = [];
    var kwargs = {};
    if (this.peek().v !== ')') {
      for (;;) {
        /* 关键字参数 name=value */
        var a = this.peek();
        var b = this.peek(1);
        if (a.t === T_ID && b && b.t === T_OP && b.v === '=') {
          this.next(); this.next();
          kwargs[a.v] = this.parseExpr(0);
        } else {
          args.push(this.parseExpr(0));
        }
        if (this.peek().v === ',') { this.next(); continue; }
        break;
      }
    }
    this.expect(T_OP, ')');
    return { k: 'call', callee: callee, args: args, kwargs: kwargs };
  };

  ExprParser.prototype.parseIndexTail = function (obj) {
    this.expect(T_OP, '[');
    var idx = this.parseExpr(0);
    this.expect(T_OP, ']');
    return { k: 'index', obj: obj, idx: idx };
  };

  /* --------------------------------------------------------------------------
     求值
     -------------------------------------------------------------------------- */

  function isThenable(v) {
    return v && typeof v.then === 'function';
  }

  /**
   * 同步求值。若遇到异步调用则返回 Promise。
   * @param {object} ast
   * @param {object} ctx  { get(name), call(calleeAst, argsValue, kwargsValue), diag() }
   */
  function evaluate(ast, ctx) {
    var v = evalNode(ast, ctx);
    return v;
  }

  function evalNode(node, ctx) {
    switch (node.k) {
      case 'lit': return node.v;

      case 'list':
        return node.items.map(function (x) { return evalNode(x, ctx); });

      case 'tuple':
        return node.items.map(function (x) { return evalNode(x, ctx); });

      case 'dict': {
        var o = {};
        node.pairs.forEach(function (p) {
          var key = evalNode(p[0], ctx);
          o[key] = evalNode(p[1], ctx);
        });
        return o;
      }

      case 'name':
        return ctx.get(node.v);

      case 'attr': {
        var base = evalNode(node.obj, ctx);
        if (base === null || base === undefined) return undefined;
        return base[node.name];
      }

      case 'index': {
        var b = evalNode(node.obj, ctx);
        var i = evalNode(node.idx, ctx);
        if (b === null || b === undefined) return undefined;
        return b[i];
      }

      case 'unary': {
        var e = evalNode(node.e, ctx);
        if (node.op === 'not') return !e;
        if (node.op === '-') return -e;
        return e;
      }

      case 'bin': {
        var l = evalNode(node.l, ctx);
        var r = evalNode(node.r, ctx);
        return applyBin(node.op, l, r);
      }

      case 'call': {
        var argsV = node.args.map(function (a) { return evalNode(a, ctx); });
        var kwV = {};
        Object.keys(node.kwargs).forEach(function (k) {
          kwV[k] = evalNode(node.kwargs[k], ctx);
        });
        return ctx.call(node.callee, argsV, kwV);
      }

      default:
        ctx.diag && ctx.diag('EVAL_UNKNOWN_NODE', 0, '未知 AST 节点: ' + node.k);
        return undefined;
    }
  }

  function applyBin(op, l, r) {
    switch (op) {
      case '+': return l + r;
      case '-': return l - r;
      case '*': return l * r;
      case '/': return l / r;
      case '//': return Math.floor(l / r);
      case '%': return l % r;
      case '**': return Math.pow(l, r);
      case '==': return l === r;
      case '!=': return l !== r;
      case '<': return l < r;
      case '>': return l > r;
      case '<=': return l <= r;
      case '>=': return l >= r;
      case 'and': return l && r;
      case 'or': return l || r;
      case 'in': return l in Object(r);
      case 'not in': return !(l in Object(r));
      case 'is': return l === r;
      case 'is not': return l !== r;
      case '&': return l & r;
      case '|': return l | r;
      case '^': return l ^ r;
      case '<<': return l << r;
      case '>>': return l >> r;
      default: return undefined;
    }
  }

  /* --------------------------------------------------------------------------
     解析缓存
     -------------------------------------------------------------------------- */
  var cache = Object.create(null);

  function parse(src, diag) {
    var key = String(src);
    if (cache[key]) return cache[key];
    var toks = tokenize(key, diag);
    var p = new ExprParser(toks);
    var ast;
    try {
      ast = p.parseExpr(0);
      if (p.peek().t !== T_EOF) {
        /* 尾巴有残留：可能是赋值语句，交给调用方处理 */
        ast = { k: 'partial', first: ast, rest: key.slice(p.peek().start) };
      }
    } catch (err) {
      if (diag) diag('EXPR_PARSE_ERROR', 0, err.message + ' :: ' + key);
      ast = { k: 'lit', v: undefined };
    }
    cache[key] = ast;
    return ast;
  }

  /* --------------------------------------------------------------------------
     语句级执行：赋值 / 自增 / 方法调用
     覆盖剧本里的全部 $ 语句形态
     -------------------------------------------------------------------------- */

  /**
   * 判断并执行一条 $"..." 语句。返回 {handled, kind, ...}
   * 支持的形态：
   *   a = expr            a += expr          a -= expr
   *   obj.attr = expr     obj.method(...)
   *   renpy.pause(...)    achievement.grant(...)
   */
  function execStatement(code, ctx) {
    var src = String(code).trim();
    if (!src) return { handled: true, kind: 'noop' };

    /* 复合赋值： +=  -=  *=  /= */
    var aug = /^([A-Za-z_][\w.\[\]'"]*)\s*(\+=|-=|\*=|\/=)\s*([\s\S]+)$/.exec(src);
    if (aug) {
      var target = aug[1];
      var op = aug[2][0];
      var rhsAst = parse(aug[3], ctx.diag);
      var rhs = evaluate(rhsAst, ctx);
      var cur = ctx.getPath ? ctx.getPath(target) : ctx.get(target);
      var newVal = applyBin(op, cur === undefined ? 0 : cur, rhs);
      ctx.setPath ? ctx.setPath(target, newVal) : ctx.set(target, newVal);
      return { handled: true, kind: 'assign', target: target, value: newVal };
    }

    /* 普通赋值（排除 ==） */
    var eq = findAssignEq(src);
    if (eq > 0) {
      var lhs = src.slice(0, eq).trim();
      var rhsSrc = src.slice(eq + 1).trim();
      var ast = parse(rhsSrc, ctx.diag);
      var val = evaluate(ast, ctx);
      if (ctx.setPath) ctx.setPath(lhs, val);
      else ctx.set(lhs, val);
      return { handled: true, kind: 'assign', target: lhs, value: val };
    }

    /* 纯表达式：方法调用 / 函数调用 */
    var ast2 = parse(src, ctx.diag);
    if (ast2.k === 'partial') {
      ctx.diag && ctx.diag('EXPR_TRAILING', 0, '表达式后有多余内容: ' + ast2.rest);
      ast2 = ast2.first;
    }
    var result = evaluate(ast2, ctx);
    return { handled: true, kind: 'expr', value: result, ast: ast2 };
  }

  /** 找到顶层赋值等号（排除 ==、!=、<=、>=、+= 等） */
  function findAssignEq(src) {
    var depth = 0;
    var inS = false, inD = false, esc = false;
    for (var i = 0; i < src.length; i++) {
      var c = src[i];
      if (esc) { esc = false; continue; }
      if (c === '\\') { esc = true; continue; }
      if (inS) { if (c === "'") inS = false; continue; }
      if (inD) { if (c === '"') inD = false; continue; }
      if (c === "'") { inS = true; continue; }
      if (c === '"') { inD = true; continue; }
      if ('([{'.indexOf(c) >= 0) { depth++; continue; }
      if (')]}'.indexOf(c) >= 0) { depth--; continue; }
      if (depth !== 0) continue;
      if (c !== '=') continue;
      var prev = src[i - 1] || '';
      var next = src[i + 1] || '';
      if ('=!<>+-*/%&|^'.indexOf(prev) >= 0) continue;
      if (next === '=') continue;
      return i;
    }
    return -1;
  }

  global.RPYExpr = {
    tokenize: tokenize,
    parse: parse,
    evaluate: evaluate,
    execStatement: execStatement,
    applyBin: applyBin,
    findAssignEq: findAssignEq,
    isThenable: isThenable,
    /* 供调试 */
    _cache: cache
  };
})(window);