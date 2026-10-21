/* ==========================================================================
   rpy/lexer.js
   把 .rpy 源码切成「带缩进的逻辑行」并构建缩进树。
   Ren'Py 用 4 空格缩进表达块，必须按缩进建树，不能逐行正则硬解。
   ========================================================================== */
(function (global) {
  'use strict';

  var S = global.RPYStrings;

  /**
   * 去掉行尾注释，尊重引号内的 #。
   */
  function stripComment(line) {
    var inS = false, inD = false, esc = false;
    for (var i = 0; i < line.length; i++) {
      var c = line[i];
      if (esc) { esc = false; continue; }
      if (c === '\\') { esc = true; continue; }
      if (inS) { if (c === "'") inS = false; continue; }
      if (inD) { if (c === '"') inD = false; continue; }
      if (c === "'") { inS = true; continue; }
      if (c === '"') { inD = true; continue; }
      if (c === '#') return line.slice(0, i);
    }
    return line;
  }

  /**
   * 合并跨行结构：
   *  1. 三引号字符串（define gui.about = _("""...""")）
   *  2. 未闭合的括号（image X = im.Scale(\n ...,\n ...)）
   *  3. 未闭合的花括号字典（define bubble.properties = {\n "a": 1,\n }）
   * 返回逻辑行数组，每项 {text, line}。
   */
  function joinTripleQuotes(rawLines) {
    var out = [];
    var i = 0;
    while (i < rawLines.length) {
      var line = rawLines[i];
      var startLine = i + 1;

      /* ---- 1) 三引号 ---- */
      if ((line.match(/"""/g) || []).length % 2 === 1) {
        var buf = line;
        var j = i + 1;
        var closed = false;
        while (j < rawLines.length) {
          buf += '\\n' + rawLines[j];
          if ((rawLines[j].match(/"""/g) || []).length % 2 === 1) {
            closed = true;
            break;
          }
          j++;
        }
        if (closed) {
          out.push({ text: buf, line: startLine });
          i = j + 1;
          continue;
        }
        /* 未闭合：按普通行处理，交给解析器报诊断 */
        out.push({ text: line, line: startLine });
        i++;
        continue;
      }

      /* ---- 2) 未闭合括号 / 花括号 ---- */
      var depth = bracketDelta(line);
      if (depth > 0) {
        var joined = line;
        var k = i + 1;
        var ok = false;
        while (k < rawLines.length) {
          var next = rawLines[k];
          /* 跨行字典的每个成员单独一行，用空格连接即可保持可解析 */
          joined += ' ' + next.trim();
          depth += bracketDelta(next);
          if (depth <= 0) { ok = true; break; }
          k++;
        }
        if (ok) {
          out.push({ text: joined, line: startLine });
          i = k + 1;
          continue;
        }
      }

      out.push({ text: line, line: startLine });
      i++;
    }
    return out;
  }

  /**
   * 统计一行里括号的净增量（忽略字符串与注释内的括号）。
   */
  function bracketDelta(line) {
    var d = 0;
    var inS = false, inD = false, inTriple = false, esc = false;
    for (var i = 0; i < line.length; i++) {
      var c = line[i];
      if (esc) { esc = false; continue; }
      if (c === '\\') { esc = true; continue; }
      if (inTriple) {
        if (line.substr(i, 3) === '"""') { inTriple = false; i += 2; }
        continue;
      }
      if (inS) { if (c === "'") inS = false; continue; }
      if (inD) { if (c === '"') inD = false; continue; }
      if (line.substr(i, 3) === '"""') { inTriple = true; i += 2; continue; }
      if (c === "'") { inS = true; continue; }
      if (c === '"') { inD = true; continue; }
      if (c === '#') break;
      if (c === '(' || c === '[' || c === '{') d++;
      else if (c === ')' || c === ']' || c === '}') d--;
    }
    return d;
  }

  function countIndent(line) {
    var n = 0;
    for (var i = 0; i < line.length; i++) {
      var c = line[i];
      if (c === ' ') n++;
      else if (c === '\t') n += 4;
      else break;
    }
    return n;
  }

  /**
   * 词法分析：返回根节点。
   * 节点结构：{ text, indent, line, children: [] }
   */
  function lex(source, file) {
    var src = S.stripBom(source).replace(/\r\n?/g, '\n');
    var rawLines = src.split('\n');
    var logical = joinTripleQuotes(rawLines);

    var root = { text: '', indent: -1, line: 0, children: [], file: file };
    var stack = [root];
    var diagnostics = [];

    for (var i = 0; i < logical.length; i++) {
      var item = logical[i];
      var raw = item.text.replace(/\t/g, '    ');
      var indent = countIndent(raw);
      var body = stripComment(raw.slice(indent)).replace(/\s+$/, '');
      if (!body) continue;

      /* 缩进必须严格增长或回退到已有的层级 */
      var parent = stack[stack.length - 1];
      while (stack.length > 1 && indent <= parent.indent) {
        stack.pop();
        parent = stack[stack.length - 1];
      }
      if (indent <= parent.indent) {
        /* 顶层 */
        parent = root;
        stack = [root];
      }

      var node = {
        text: body,
        indent: indent,
        line: item.line,
        children: [],
        file: file
      };
      parent.children.push(node);

      /* 以 : 结尾的语句开启新块 */
      if (/:\s*$/.test(body)) {
        stack.push(node);
      }
    }

    return { root: root, diagnostics: diagnostics };
  }

  global.RPYLexer = {
    lex: lex,
    stripComment: stripComment,
    countIndent: countIndent,
    bracketDelta: bracketDelta,
    joinTripleQuotes: joinTripleQuotes
  };
})(window);