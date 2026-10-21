#!/usr/bin/env node
/**
 * tools/test_e2e.js
 * 端到端：用文件系统桩替代 fetch，真正跑一遍 app.boot() + vm.start()，
 * 逐步观察 HUD 的显隐，定位「HUD 看不到」的原因。
 *
 * 用法：node tools/test_e2e.js [label]
 */

'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const WEB = path.join(ROOT, 'web');

/* --------------------------------------------------------------------------
   DOM 桩
   -------------------------------------------------------------------------- */
const noop = () => {};

function makeEl(tag) {
  const el = {
    tagName: (tag || 'div').toUpperCase(),
    id: '', className: '', dataset: {}, attrs: {},
    style: {
      _v: {},
      setProperty(k, v) { this._v[k] = v; },
      getPropertyValue(k) { return this._v[k] || ''; }
    },
    children: [], parentNode: null,
    hidden: false, textContent: '', _html: '', src: '',
    _classes: new Set(),
    classList: {
      add(c) { el._classes.add(c); },
      remove(c) { el._classes.delete(c); },
      toggle(c, on) {
        if (on === undefined) { el._classes.has(c) ? el._classes.delete(c) : el._classes.add(c); }
        else if (on) el._classes.add(c); else el._classes.delete(c);
      },
      contains: (c) => el._classes.has(c)
    },
    appendChild(c) { c.parentNode = el; el.children.push(c); return c; },
    removeChild(c) { const i = el.children.indexOf(c); if (i >= 0) el.children.splice(i, 1); return c; },
    remove() { if (el.parentNode) el.parentNode.removeChild(el); },
    setAttribute(k, v) { el.attrs[k] = String(v); if (k === 'hidden') el.hidden = true; },
    getAttribute(k) { return el.attrs[k] === undefined ? null : el.attrs[k]; },
    removeAttribute(k) { delete el.attrs[k]; if (k === 'hidden') el.hidden = false; },
    addEventListener(t, fn) { (el._ev = el._ev || {})[t] = fn; },
    removeEventListener() {},
    querySelector() { return null; },
    querySelectorAll() { return []; },
    closest() { return null; },
    focus() {}, click() {}, play: () => Promise.resolve(), pause: noop,
    getBoundingClientRect: () => ({ width: 1920, height: 1080 }),
    get innerHTML() { return el._html; },
    set innerHTML(v) { el._html = String(v); if (!v) el.children.length = 0; },
    get offsetWidth() { return 1920; },
    get firstChild() { return el.children[0] || null; }
  };
  return el;
}

const REG = {};
function getEl(id) {
  if (!REG[id]) { REG[id] = makeEl('div'); REG[id].id = id; }
  return REG[id];
}

const store = {};

function audioEl() {
  return {
    play: () => Promise.resolve(), pause: noop, load: noop,
    volume: 1, loop: false, currentTime: 0, preload: '', readyState: 0,
    addEventListener: noop, removeAttribute: noop,
    setAttribute: noop, getAttribute: () => '',
    set onended(v) {}, get ended() { return false; }, get paused() { return true; }
  };
}

/* --------------------------------------------------------------------------
   fetch 桩：按路径读本地文件
   -------------------------------------------------------------------------- */
function fetchStub(url) {
  /* 相对 web/ 解析：../xxx -> 工程根；assets/xxx -> web/assets */
  let p = String(url).replace(/^\.\.\//, '');
  let abs;
  if (String(url).indexOf('../') === 0) abs = path.join(ROOT, p);
  else abs = path.join(WEB, p);

  try {
    abs = decodeURIComponent(abs);
  } catch (e) { /* ignore */ }

  const exists = fs.existsSync(abs) && fs.statSync(abs).isFile();
  if (!exists) {
    return Promise.resolve({
      ok: false, status: 404,
      json: () => Promise.reject(new Error('404 ' + url)),
      text: () => Promise.reject(new Error('404 ' + url))
    });
  }
  const buf = fs.readFileSync(abs);
  return Promise.resolve({
    ok: true, status: 200,
    json: () => Promise.resolve(JSON.parse(buf.toString('utf8'))),
    text: () => Promise.resolve(buf.toString('utf8'))
  });
}

const sandbox = {
  console, Math, JSON, Date, Promise, Object, Array, String, Number,
  setTimeout: (f) => setImmediate(f),
  clearTimeout: () => {},
  setInterval: () => 0,
  clearInterval: () => {},
  encodeURIComponent, decodeURIComponent,
  performance: { now: () => Date.now() },
  localStorage: {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; }
  },
  document: {
    readyState: 'complete',
    body: makeEl('body'),
    getElementById: getEl,
    createElement: (t) => (t === 'audio' ? audioEl() : makeEl(t)),
    addEventListener: noop, removeEventListener: noop,
    querySelector: () => null, querySelectorAll: () => [],
    documentElement: makeEl('html'), fullscreenElement: null,
    exitFullscreen: () => Promise.resolve()
  },
  addEventListener: noop, removeEventListener: noop,
  innerWidth: 1920, innerHeight: 1080,
  location: { search: '' },
  Image: function () {
    const o = { onload: null, onerror: null };
    Object.defineProperty(o, 'src', {
      set(v) { o._src = v; setImmediate(() => o.onload && o.onload()); },
      get() { return o._src || ''; }
    });
    return o;
  },
  fetch: fetchStub
};
sandbox.window = sandbox;
sandbox.global = sandbox;
vm.createContext(sandbox);

/* --------------------------------------------------------------------------
   加载全部脚本（顺序与 index.html 一致）
   -------------------------------------------------------------------------- */
const SCRIPTS = [
  'js/fs-utils.js', 'js/manifest.js',
  'js/rpy/strings.js', 'js/rpy/lexer.js', 'js/rpy/parser.js',
  'js/rpy/expr.js', 'js/rpy/compiler.js',
  'js/engine/state.js', 'js/engine/actors.js', 'js/engine/images.js',
  'js/engine/audio.js', 'js/engine/transitions.js', 'js/engine/stage.js',
  'js/engine/save.js', 'js/engine/movie.js',
  'js/ui/say.js', 'js/ui/centered_text.js', 'js/ui/choice.js',
  'js/ui/history.js', 'js/ui/diag.js',
  'js/engine/vm.js',
  'js/ui/main_menu.js', 'js/ui/save_load.js', 'js/ui/config.js',
  'js/ui/gallery.js', 'js/ui/about.js',
  'js/boot.js'
];

const loadErrors = [];
SCRIPTS.forEach((f) => {
  try {
    vm.runInContext(fs.readFileSync(path.join(WEB, f), 'utf8'), sandbox, { filename: f });
  } catch (e) {
    loadErrors.push(f + ': ' + e.message);
  }
});

if (loadErrors.length) {
  console.log('加载错误:');
  loadErrors.forEach((e) => console.log('  ' + e));
}

/* --------------------------------------------------------------------------
   驱动
   -------------------------------------------------------------------------- */
const tick = () => new Promise((r) => setImmediate(r));

async function main() {
  let fail = 0;
  const app = sandbox.GalGod;
  if (!app) {
    console.error('app 未创建');
    process.exit(1);
  }

  console.log('=== boot ===');
  await app.boot();
  await tick();

  const hud = getEl('hud');
  const top = getEl('hud-top');
  const bottom = getEl('hud-bottom');

  console.log('  hud 存在        :', !!app.hudEl);
  console.log('  右上按钮数      :', top.children.length);
  console.log('  右下按钮数      :', bottom.children.length);
  console.log('  主菜单已显示    :', !!(app.ui.mainMenu && app.ui.mainMenu.isOpen()));
  console.log('  HUD hidden(主菜单):', hud.hidden);

  if (!app.hudEl) { console.log('  [FAIL] hudEl 为空'); fail++; }
  if (top.children.length !== 3) { console.log('  [FAIL] 右上按钮数不是 3'); fail++; }
  if (bottom.children.length !== 5) { console.log('  [FAIL] 右下按钮数不是 5'); fail++; }

  /* 从主菜单开始游戏 */
  console.log('\n=== 开始游戏 ===');
  app.ui.mainMenu.onStart();
  await tick();
  for (let i = 0; i < 400; i++) {
    await tick();
    if (app.ui.say.isWaiting) {
      /* 只推进，不打断 */
      app.ui.say.advance();
    }
    if (app.ui.centered.isActive && app.ui.centered.isActive()) {
      app.ui.centered.advance();
    }
    if (i === 200) {
      const st = app.state;
      console.log('  中段 vm.running :', app.vm.running);
      console.log('  中段 label      :', app.vm.lastPc.label + '#' + app.vm.lastPc.pc);
      console.log('  中段 custom_ui  :', JSON.stringify(st.getVar('custom_ui')));
      console.log('  中段 HUD hidden :', hud.hidden);
    }
    if (!app.vm.running) break;
  }

  const flag = app.state.getVar('custom_ui');
  const customUiOn = flag === undefined ? true : !!flag;

  console.log('\n=== 最终状态 ===');
  console.log('  label        :', app.vm.lastPc.label + '#' + app.vm.lastPc.pc);
  console.log('  vm.running   :', app.vm.running);
  console.log('  custom_ui    :', JSON.stringify(flag), '-> 生效:', customUiOn);
  console.log('  HUD hidden   :', hud.hidden);
  console.log('  HUD 应有显示 :', !!(app.vm.running && customUiOn));

  const expectHidden = !(app.vm.running && customUiOn);
  if (hud.hidden !== expectHidden) {
    console.log('  [FAIL] HUD 显隐与预期不符');
    fail++;
  } else {
    console.log('  [ OK ] HUD 显隐正确');
  }

  console.log('\n结果: ' + (fail === 0 ? '通过' : fail + ' 项失败'));
  process.exit(fail === 0 ? 0 : 1);
}

main().catch((e) => { console.error(e); process.exit(1); });