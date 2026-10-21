/* ==========================================================================
   manifest.js
   资源清单加载。优先请求 web/assets/manifest.json；
   失败时使用内置兜底（仅用于本地直接打开 index.html 的极端情况）。
   ========================================================================== */
(function (global) {
  'use strict';

  var MANIFEST_URL = 'assets/manifest.json';
  var OVERRIDES_URL = 'assets/overrides.json';

  /**
   * 工程根目录相对于本页面的前缀。
   *
   * 目录结构：
   *   archive/                <- 工程根（.rpy / images / audio / gui / movies）
   *     web/index.html        <- 本页面
   *
   * 因此从 /web/ 访问根下的资源必须用 '../'。
   * manifest.json 与 overrides.json 在 web/assets/ 内，不需要前缀。
   */
  var ROOT = '../';

  /* 兜底清单：只包含保证可跑通 start 所需的最小集合 */
  var FALLBACK = {
    version: 0,
    game: { name: 'GalGod', version: '1.0.0', screen_width: 1920, screen_height: 1080 },
    script_files: [
      'script.rpy',
      'resources.rpy',
      'config/options.rpy',
      'config/character_config.rpy',
      'config/character_core.rpy',
      'scenes/1_1.rpy',
      'scenes/1_2.rpy',
      'scenes/1_3.rpy',
      'scenes/1_4.rpy',
      'scenes/2_1.rpy',
      'scenes/2_2.rpy',
      'scenes/2_3.rpy',
      'scenes/2_4.rpy',
      'scenes/3_1.rpy',
      'scenes/3_2.rpy',
      'scenes/3_3.rpy',
      'scenes/3_4.rpy',
      'scenes/end_ne1.rpy',
      'scenes/end_ne2.rpy',
      'scenes/end_te.rpy',
      'scenes/interlude1.rpy',
      'scenes/interlude2.rpy',
      'scenes/interlude-interview.rpy',
      'scenes/after_story_noctella.rpy'
    ],
    assets: [],
    missing: []
  };

  function fetchJSON(url) {
    return fetch(url, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error(url + ' -> HTTP ' + r.status);
      return r.json();
    });
  }

  function loadManifest(onStatus) {
    if (onStatus) onStatus('正在读取资源清单…');
    return fetchJSON(MANIFEST_URL).catch(function (err) {
      if (onStatus) onStatus('资源清单缺失，使用内置清单（请先运行 tools/gen_manifest.py）');
      return FALLBACK;
    });
  }

  function loadOverrides() {
    return fetchJSON(OVERRIDES_URL).catch(function () {
      return { image: {}, audio: {} };
    });
  }

  /**
   * 顺序拉取全部 .rpy 源码。
   * @param {Array<string>} files
   * @param {Function} onProgress (done, total, path)
   */
  function loadScripts(files, onProgress) {
    var results = [];
    var total = files.length;

    return files.reduce(function (chain, path) {
      return chain.then(function () {
        /* 剧本位于工程根目录，必须带 ROOT 前缀 */
        var url = ROOT + path.split('/').map(function (s) {
          return encodeURIComponent(s);
        }).join('/');
        return fetch(url, { cache: 'no-cache' })
          .then(function (r) {
            if (!r.ok) throw new Error(path + ' -> HTTP ' + r.status);
            return r.text();
          })
          .then(function (text) {
            results.push({ path: path, source: text });
            if (onProgress) onProgress(results.length, total, path);
          })
          .catch(function (err) {
            results.push({ path: path, source: '', error: String(err) });
            if (onProgress) onProgress(results.length, total, path);
          });
      });
    }, Promise.resolve()).then(function () {
      return results;
    });
  }

  global.RPYManifest = {
    loadManifest: loadManifest,
    loadOverrides: loadOverrides,
    loadScripts: loadScripts,
    FALLBACK: FALLBACK
  };
})(window);