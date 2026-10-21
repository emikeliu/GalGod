/* ==========================================================================
   engine/images.js
   把 resources.rpy 里的 image 定义解析成浏览器可用的资源描述。
   支持：
     image X = "path"
     image X = bg_fit("path")
     image X = bg_focus("path", zoom=1.5, x=0.2, y=0.3)
     image X = Solid("#fff")
     image X = Transform("path", xysize=(w,h))
     image X = im.Scale("path", w, h)
     image X = At(Image("path"), style)
     image X:  (ATL 块，按名称 + 首帧静态图处理)
   ========================================================================== */
(function (global) {
  'use strict';

  var P = global.RPYParser;

  var IMAGE_EXTS = ['.webp', '.avif', '.png', '.jpg', '.jpeg', '.gif', '.bmp'];

  function Images(manifest, overrides) {
    this.manifest = manifest || { assets: [] };
    this.overrides = overrides || {};
    this.assetSet = Object.create(null);
    var assets = this.manifest.assets || [];
    for (var i = 0; i < assets.length; i++) {
      this.assetSet[assets[i]] = true;
      this.assetSet[assets[i].toLowerCase()] = assets[i];
    }
    this.defs = Object.create(null);     /* name -> descriptor */
    this.diagnostics = [];
  }

  /* --------------------------------------------------------------------------
     资源存在性 / 路径修复
     -------------------------------------------------------------------------- */
  Images.prototype.exists = function (path) {
    return !!(this.assetSet[path] || this.assetSet[String(path).toLowerCase()]);
  };

  Images.prototype.canonical = function (path) {
    if (this.assetSet[path]) return path;
    return this.assetSet[String(path).toLowerCase()] || path;
  };

  /**
   * 把剧本里的路径转换成实际可请求的 URL。
   * 处理：overrides 回退、语音 audio/ 前缀、缺扩展名兜底、中文编码。
   */
  /**
   * 注册 define 别名，例如 resources.rpy 里的
   *   define fx.crowd = "audio/fx/FX_嘈杂声.ogg"
   * 之后 `play sound fx.crowd` 就能解析到真实文件。
   */
  Images.prototype.setAliases = function (aliases) {
    this.aliases = aliases || Object.create(null);
    return this;
  };

  Images.prototype.resolve = function (path, kind) {
    if (!path) return null;
    var raw = String(path).trim().replace(/\\/g, '/');

    /* define 别名（fx.crowd / fx.camera ...） */
    if (this.aliases && this.aliases[raw]) {
      raw = this.aliases[raw];
    }

    /* 已经是 URL / data URI */
    if (/^(https?:|data:|blob:)/.test(raw)) return raw;

    var ov = (this.overrides[kind || 'image'] || {})[raw];
    if (ov === null) return null;             /* 明确标记为「不存在，静默跳过」 */
    if (typeof ov === 'string') raw = ov;

    var candidates = [raw];

    /* 语音/音效前缀补全 */
    if (/^(cv|cv2|cv3|bgm|fx)\//.test(raw)) candidates.push('audio/' + raw);

    /* 缺扩展名：尝试常见后缀 */
    if (!/\.[a-z0-9]{2,5}$/i.test(raw)) {
      for (var i = 0; i < IMAGE_EXTS.length; i++) candidates.push(raw + IMAGE_EXTS[i]);
    }

    /* effects 目录下的雨图 */
    if (raw.charAt(0) === '_') candidates.push('effects/' + raw);

    for (var c = 0; c < candidates.length; c++) {
      if (this.exists(candidates[c])) {
        return this.canonical(candidates[c]);
      }
    }

    /* 找不到也不中断播放，返回原路径让浏览器 404，由诊断面板记录 */
    this.diagnostics.push({
      kind: 'MISSING_ASSET',
      path: raw,
      message: '资源不存在: ' + raw
    });
    return raw;
  };

  /**
   * 工程根目录前缀。
   * 本页面位于 /web/index.html，而 .rpy、images/、audio/、gui/、movies/
   * 都在上一级（工程根）。所以所有资源 URL 都要以 '../' 开头。
   */
  Images.ROOT = '../';

  Images.prototype.url = function (path, kind) {
    var p = this.resolve(path, kind);
    if (!p) return null;

    /* 已经是绝对 URL / data URI：原样返回 */
    if (/^(https?:|data:|blob:|\/\/)/.test(p)) return p;

    /* 已经是带 ../ 的相对路径：避免重复加前缀 */
    var prefix = p.indexOf('../') === 0 ? '' : Images.ROOT;

    /* 中文文件名必须逐段编码，否则部分静态服务器会 404 */
    return prefix + p.split('/').map(function (seg) {
      if (seg === '..' || seg === '.' || seg === '') return seg;
      return encodeURIComponent(seg);
    }).join('/');
  };

  /* --------------------------------------------------------------------------
     解析 image 表达式
     -------------------------------------------------------------------------- */
  Images.prototype.parseExpr = function (expr) {
    var s = String(expr || '').trim();
    if (!s) return { type: 'none' };

    /* 纯字符串 */
    var str = P.asString(s);
    if (str !== null) {
      return { type: 'image', path: str, fit: 'none' };
    }

    var call = P.parseCall(s);
    var name = String(call.name || '').split('.').pop();
    var args = call.args || [];
    var kw = P.parseArgs(args.join(',')).kwargs;

    /* bg_fit(path) */
    if (name === 'bg_fit') {
      var p1 = P.asString(args[0] || '');
      return { type: 'image', path: p1, fit: 'cover', zoom: 1, xalign: 0.5, yalign: 0.5 };
    }

    /* bg_focus(path, zoom=, x=, y=) */
    if (name === 'bg_focus') {
      var p2 = P.asString(args[0] || '');
      return {
        type: 'image',
        path: p2,
        fit: 'cover',
        zoom: num(kw.zoom, 1.3),
        xalign: num(kw.x, 0.5),
        yalign: num(kw.y, 0.5)
      };
    }

    /* Solid("#fff") */
    if (name === 'Solid') {
      var color = P.asString(args[0] || '');
      return { type: 'solid', color: color || '#000' };
    }

    /* Transform(path, zoom=..., xysize=(w,h)) */
    if (name === 'Transform') {
      var tp = P.asString(args[0] || '');
      var out = { type: 'image', path: tp, fit: 'none' };
      if (kw.zoom !== undefined) out.zoom = num(kw.zoom, 1);
      if (kw.xysize) {
        var m = /\(?\s*([\d.]+)\s*,\s*([\d.]+)\s*\)?/.exec(kw.xysize);
        if (m) { out.width = parseFloat(m[1]); out.height = parseFloat(m[2]); }
      }
      return out;
    }

    /* im.Scale(path, w, h) / Image(path) / At(Image(path), style) */
    if (name === 'Scale' || name === 'Image' || name === 'At') {
      var inner = args[0] || '';
      var innerStr = P.asString(inner);
      if (innerStr === null) {
        var ic = P.parseCall(inner);
        innerStr = P.asString((ic.args || [])[0] || '');
      }
      var o2 = { type: 'image', path: innerStr, fit: name === 'Scale' ? 'stretch' : 'none' };
      if (name === 'Scale' && args.length >= 3) {
        o2.width = num(args[1]);
        o2.height = num(args[2]);
      }
      return o2;
    }

    /* 直接是另一张图片的名字（极少见） */
    if (!call.isCall && /^[A-Za-z_]/.test(s)) {
      return { type: 'ref', name: s };
    }

    return { type: 'none', raw: s };
  };

  function num(v, dflt) {
    if (v === undefined || v === null || v === '') return dflt;
    var n = parseFloat(v);
    return isNaN(n) ? dflt : n;
  }

  /* --------------------------------------------------------------------------
     装载 image 定义
     -------------------------------------------------------------------------- */
  Images.prototype.load = function (program) {
    var defs = program.images || {};
    for (var name in defs) {
      var d = defs[name];
      var desc = this.parseExpr(d.expr);
      desc.name = name;
      desc.file = d.file;
      desc.line = d.line;
      this.defs[name] = desc;
    }

    /* Ren'Py 内置色块：scene black / scene white 依赖它们 */
    var BUILTINS = {
      'black': '#000',
      'white': '#fff',
      'bg black': '#000',
      'bg white': '#fff'
    };
    Object.keys(BUILTINS).forEach(function (n) {
      if (!this.defs[n]) {
        this.defs[n] = {
          name: n,
          type: 'solid',
          color: BUILTINS[n],
          file: '(builtin)',
          line: 0
        };
      }
    }, this);

    return this;
  };

  /**
   * 给定 Ren'Py 的 show 名称（如 "bg street1_1" / "cg 001" / "lx 微笑"），
   * 返回图像描述。多段名称优先匹配完整名，再退化到最长前缀。
   */
  Images.prototype.get = function (name) {
    var n = String(name || '').trim().replace(/\s+/g, ' ');
    if (!n) return null;
    if (this.defs[n]) return this.defs[n];

    /* 尝试去掉末尾属性（show lx 微笑 时可能带额外 tag） */
    var parts = n.split(' ');
    for (var len = parts.length - 1; len >= 1; len--) {
      var key = parts.slice(0, len).join(' ');
      if (this.defs[key]) {
        var base = Object.assign({}, this.defs[key]);
        base.extraAttrs = parts.slice(len);
        return base;
      }
    }
    return null;
  };

  /** 该名称是否是一个已定义的 image */
  Images.prototype.has = function (name) {
    return !!this.defs[String(name || '').trim().replace(/\s+/g, ' ')];
  };

  /* --------------------------------------------------------------------------
     预加载
     -------------------------------------------------------------------------- */
  Images.prototype.preload = function (paths, onProgress) {
    var self = this;
    var total = paths.length;
    var done = 0;
    if (!total) return Promise.resolve();

    return new Promise(function (resolve) {
      var pending = total;
      paths.forEach(function (p) {
        var url = self.url(p, 'image');
        if (!url) { tick(); return; }
        var img = new Image();
        img.onload = tick;
        img.onerror = tick;
        img.src = url;
      });
      function tick() {
        done++;
        if (onProgress) onProgress(done, total);
        if (--pending <= 0) resolve();
      }
    });
  };

  global.RPYImages = {
    Images: Images
  };
})(window);