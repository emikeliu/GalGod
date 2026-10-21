/* ==========================================================================
   rpy/strings.js
   字符串工具：BOM 剥离、转义还原、Ren'Py 文本标签 -> HTML
   ========================================================================== */
(function (global) {
  'use strict';

  var BOM = 0xFEFF;

  function stripBom(s) {
    if (typeof s !== 'string') return '';
    return s.charCodeAt(0) === BOM ? s.slice(1) : s;
  }

  /* Ren'Py 字符串字面量里的转义序列 */
  function unescapeRpy(s) {
    if (typeof s !== 'string') return '';
    var out = '';
    for (var i = 0; i < s.length; i++) {
      var c = s[i];
      if (c !== '\\') { out += c; continue; }
      var n = s[++i];
      switch (n) {
        case 'n': out += '\n'; break;
        case 't': out += '\t'; break;
        case '"': out += '"'; break;
        case "'": out += "'"; break;
        case '\\': out += '\\'; break;
        case ' ': out += ' '; break;
        case '\n': out += ''; break;   /* 行尾续行 */
        default: out += (n === undefined ? '\\' : n);
      }
    }
    return out;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&')
      .replace(/</g, '<')
      .replace(/>/g, '>')
      .replace(/"/g, '"');
  }

  /* ------------------------------------------------------------------
     文本标签解析
     支持本工程实际用到的：{size=} {/size} {space=} {b} {i} {color=}
     以及常见的 {w} {p} {nw} {cps=} {font=} {u} {s} {a=} {alt=}
     未知标签原样丢弃（Ren'Py 里它们也不产生可见字符）
     ------------------------------------------------------------------ */
  var SIZE_RE = /^size=([+-]?\d+(?:\.\d+)?)$/;
  var SPACE_RE = /^space=([+-]?\d+(?:\.\d+)?)$/;
  var VSPACE_RE = /^vspace=([+-]?\d+(?:\.\d+)?)$/;
  var COLOR_RE = /^color=(.+)$/;
  var FONT_RE = /^font=(.+)$/;
  var ALPHA_RE = /^alpha=([\d.]+)$/;
  var CPS_RE = /^cps=([\d.]+)$/;

  /**
   * 把 Ren'Py 文本转换为 HTML。
   * @param {string} text  已经 unescape 过的文本
   * @param {number} baseSize 基准字号，用于 {size=+N}
   * @returns {string} HTML
   */
  function renderText(text, baseSize) {
    baseSize = baseSize || 33;
    if (!text) return '';

    var out = '';
    var sizeStack = [];
    var curSize = baseSize;
    var i = 0;
    var plain = false;

    function emit(str) {
      if (plain) {
        out += escapeHtml(str);
        return;
      }
      /* 保留换行，其余走 HTML 转义 */
      out += escapeHtml(str).replace(/\n/g, '<br>');
    }

    while (i < text.length) {
      var ch = text[i];
      if (ch === '{') {
        var end = text.indexOf('}', i + 1);
        if (end < 0) { emit(text.slice(i)); break; }
        var tag = text.slice(i + 1, end);
        i = end + 1;

        if (tag === 'plain') { plain = true; continue; }
        if (tag === 'nw') { continue; }
        if (tag === 'p' || tag === 'w' || /^w=/.test(tag) || CPS_RE.test(tag)) {
          /* 等待/暂停类标签在浏览器端不产生视觉字符 */
          continue;
        }
        if (tag === 'b') { out += '<b>'; continue; }
        if (tag === '/b') { out += '</b>'; continue; }
        if (tag === 'i') { out += '<i>'; continue; }
        if (tag === '/i') { out += '</i>'; continue; }
        if (tag === 'u') { out += '<u>'; continue; }
        if (tag === '/u') { out += '</u>'; continue; }
        if (tag === 's') { out += '<s>'; continue; }
        if (tag === '/s') { out += '</s>'; continue; }
        if (tag === '/size') {
          curSize = sizeStack.length ? sizeStack.pop() : baseSize;
          out += '</span>';
          continue;
        }
        if (tag === '/color') { out += '</span>'; continue; }
        if (tag === '/font') { out += '</span>'; continue; }
        if (tag === '/a') { out += '</span>'; continue; }
        if (tag === 'alt' || tag === 'noalt' || tag === 'rt' || tag === 'rb' ||
            tag === 'art') {
          continue;
        }

        var m = SIZE_RE.exec(tag);
        if (m) {
          sizeStack.push(curSize);
          var raw = m[1];
          if (raw[0] === '+' || raw[0] === '-') {
            curSize = curSize + parseFloat(raw);
          } else {
            curSize = parseFloat(raw);
          }
          out += '<span class="t-size" style="font-size:' + curSize + 'px">';
          continue;
        }

        m = SPACE_RE.exec(tag);
        if (m) {
          out += '<span style="display:inline-block;width:' + parseFloat(m[1]) + 'px"></span>';
          continue;
        }

        m = VSPACE_RE.exec(tag);
        if (m) {
          out += '<span style="display:inline-block;height:' + parseFloat(m[1]) + 'px"></span><br>';
          continue;
        }

        m = COLOR_RE.exec(tag);
        if (m) {
          out += '<span style="color:' + escapeHtml(m[1]) + '">';
          continue;
        }

        m = FONT_RE.exec(tag);
        if (m) {
          out += '<span style="font-family:\'' + escapeHtml(m[1].replace(/'/g, '')) + '\'">';
          continue;
        }

        m = ALPHA_RE.exec(tag);
        if (m) {
          out += '<span style="opacity:' + m[1] + '">';
          continue;
        }

        /* 形如 {a=...} 的超链接、{image=...} 等：忽略标签本身 */
        continue;
      }
      emit(ch);
      i++;
    }
    return out;
  }

  /**
   * 去掉 Python 表达式里的 # 注释（尊重字符串），并压掉空行。
   * 用于解析 CHARACTERS_CONFIG / global_actor_settings 这类跨行字典。
   */
  function stripPythonComments(src) {
    var text = String(src || '').replace(/\r\n?/g, '\n');
    var out = '';
    var inS = false, inD = false, inTriple = false, esc = false;

    for (var i = 0; i < text.length; i++) {
      var c = text[i];

      if (esc) { out += c; esc = false; continue; }
      if (c === '\\') { out += c; esc = true; continue; }

      if (inTriple) {
        if (text.substr(i, 3) === '"""') { inTriple = false; out += '"""'; i += 2; continue; }
        out += c;
        continue;
      }
      if (inS) { out += c; if (c === "'") inS = false; continue; }
      if (inD) { out += c; if (c === '"') inD = false; continue; }

      if (text.substr(i, 3) === '"""') { inTriple = true; out += '"""'; i += 2; continue; }
      if (c === "'") { inS = true; out += c; continue; }
      if (c === '"') { inD = true; out += c; continue; }

      if (c === '#') {
        while (i < text.length && text[i] !== '\n') i++;
        out += '\n';
        continue;
      }
      out += c;
    }

    return out
      .split('\n')
      .map(function (l) { return l.replace(/\s+$/, ''); })
      .filter(function (l) { return l.trim() !== ''; })
      .join('\n');
  }

  /** 去掉所有标签，得到纯文本（用于存读档摘要、历史记录） */
  function stripTags(text) {
    return String(text || '')
      .replace(/\{[^{}]*\}/g, '')
      .replace(/\\n/g, ' ');
  }

  global.RPYStrings = {
    stripBom: stripBom,
    unescapeRpy: unescapeRpy,
    escapeHtml: escapeHtml,
    renderText: renderText,
    stripTags: stripTags,
    stripPythonComments: stripPythonComments
  };
})(window);