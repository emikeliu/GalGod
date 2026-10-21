#!/usr/bin/env node
/**
 * tools/test_hud.js
 * 验证 HUD（screens/ui.rpy 的 custom_ui）：
 *   - 5 个按钮 + 3 个按钮都建出来了，图片路径正确
 *   - custom_ui = False 时整层隐藏，= True 时显示
 *   - 快进 / 自动 的选中态能正确切换
 *   - 快存 / 快读 走 quick 槽
 */

'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const WEB = path.join(ROOT, 'web');

/* --------------------------------------------------------------------------
   DOM 桩（可查询 class，足够验证 HUD 结构）
   -------------------------------------------------------------------------- */
const noop = () => {};

function makeEl(tag) {
  const el = {
    tagName: (tag || 'div').toUpperCase(),
    id: '', className: '', style: {}, dataset: {}, attrs: {},
    children: [], parentNode: null,
    hidden: false, textContent: '', _html: '',
    _classes: new Set(),
    classList: {
      add(c) { el._classes.add(c); },
      remove(c) { el._classes.delete(c); },
      toggle(c, on) { if (on === undefined) { el._classes.has(c) ? el._classes.delete(c) : el._classes.add(c); } else if (on) el._classes.add(c); else el._classes.delete(c); },
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
    focus() {},
    get innerHTML() { return el._html; },
    set innerHTML(v) { el._html = String(v); if (!v) el.children.length = 0; }
  };
  return el;
}

const REG = {};
function getEl(id) {
  if (!REG[id]) { REG[id] = makeEl('div'); REG[id].id = id; }
  return REG[id];
}

const store = {};
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
    documentElement: makeEl('html'), fullscreenElement: null
  },
  addEventListener: noop, removeEventListener: noop,
  innerWidth: 1920, innerHeight: 1080,
  location: { search: '' },
  Image: function () { return { set src(v) {}, get src() { return ''; } }; },
  fetch: () => Promise.reject(new Error('no fetch'))
};
sandbox.window = sandbox;
sandbox.global = sandbox;
vm.createContext(sandbox);

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
   加载依赖
   -------------------------------------------------------------------------- */
['js/rpy/strings.js', 'js/rpy/lexer.js', 'js/rpy/parser.js',
 'js/rpy/expr.js', 'js/rpy/compiler.js',
 'js/engine/state.js', 'js/engine/images.js'].forEach((f) => {
  vm.runInContext(fs.readFileSync(path.join(WEB, f), 'utf8'), sandbox, { filename: f });
});

const { RPYCompiler, RPYState, RPYImages } = sandbox;

const manifest = JSON.parse(fs.readFileSync(path.join(WEB, 'assets/manifest.json'), 'utf8'));
const overrides = JSON.parse(fs.readFileSync(path.join(WEB, 'assets/overrides.json'), 'utf8'));
const files = manifest.script_files.map((rel) => ({
  path: rel, source: fs.readFileSync(path.join(ROOT, rel), 'utf8')
}));
const program = RPYCompiler.compileAll(files);

const state = new RPYState.State();
const images = new RPYImages.Images(manifest, overrides);
images.load(program);

/* --------------------------------------------------------------------------
   取出 boot.js 里的 buildQuickMenu / syncHud / refreshQuickMenu 逻辑
   通过加载整份 boot.js 拿到 App 原型（需要先补齐其它全局依赖）
   -------------------------------------------------------------------------- */
['js/fs-utils.js', 'js/manifest.js',
 'js/engine/actors.js', 'js/engine/audio.js', 'js/engine/transitions.js',
 'js/engine/stage.js', 'js/engine/save.js', 'js/engine/movie.js',
 'js/engine/vm.js',
 'js/ui/say.js', 'js/ui/centered_text.js', 'js/ui/choice.js',
 'js/ui/history.js', 'js/ui/diag.js',
 'js/ui/main_menu.js', 'js/ui/save_load.js', 'js/ui/config.js',
 'js/ui/gallery.js', 'js/ui/about.js',
 'js/boot.js'].forEach((f) => {
  try {
    vm.runInContext(fs.readFileSync(path.join(WEB, f), 'utf8'), sandbox, { filename: f });
  } catch (e) {
    /* 部分 UI 依赖真实 DOM 细节，加载失败不影响 HUD 验证 */
  }
});

/* --------------------------------------------------------------------------
   构造 App 并只调用 HUD 相关方法
   -------------------------------------------------------------------------- */
const App = sandbox.GalGod ? sandbox.GalGod.constructor : null;
const app = new App();

app.program = program;
app.manifest = manifest;
app.images = images;
app.state = state;
app.overrides = overrides;
app.runtimeDiagnostics = [];

app.vm = {
  running: true,
  skipMode: false,
  autoMode: false,
  state: state,
  setSkip(on) { this.skipMode = on; },
  setAuto(on) { this.autoMode = on; }
};

/* 记录调用 */
const calls = [];
app.playUiHover = () => calls.push('hover');
app.playUiClick = () => calls.push('click');
app.openHistory = () => calls.push('history');
app.openGameMenu = () => calls.push('menu');
app.toast = () => {};
app.hudFlash = (m) => calls.push('flash:' + m);
app.ui = {
  saveLoad: { open: (m) => calls.push('saveLoad:' + m), isOpen: () => false },
  config: { open: () => {}, isOpen: () => false },
  gallery: { isOpen: () => false },
  about: { isOpen: () => false },
  history: { isOpen: () => false },
  confirm: { isOpen: () => false }
};
app.save = {
  saved: [],
  save(page, slot) { this.saved.push(page + '.' + slot); return true; },
  list(page) { return [{ slot: 1, empty: false, info: {} }]; },
  load(page, slot) { calls.push('load:' + page + '.' + slot); }
};

/* --------------------------------------------------------------------------
   执行 & 断言
   -------------------------------------------------------------------------- */
let fail = 0;

function check(name, cond, extra) {
  console.log('  ' + (cond ? '[ OK ]' : '[FAIL]') + ' ' + name + (extra ? '  ' + extra : ''));
  if (!cond) fail++;
}

console.log('=== 构建 HUD ===');
app.buildQuickMenu();

const hud = getEl('hud');
const top = getEl('hud-top');
const bottom = getEl('hud-bottom');

check('hud 容器存在', !!app.hudEl);
check('右上角 3 个按钮', top.children.length === 3, '实际 ' + top.children.length);
check('右下角 5 个按钮', bottom.children.length === 5, '实际 ' + bottom.children.length);

function srcOf(btn) {
  const img = btn.children.find((c) => c.tagName === 'IMG');
  return img ? img.src : null;
}

const expectTop = ['快进1.png', '自动1.png', '菜单1.png'];
top.children.forEach((btn, i) => {
  const s = srcOf(btn);
  const ok = s && s.indexOf(expectTop[i]) >= 0;
  check('右上 #' + (i + 1) + ' -> ' + expectTop[i], ok, s || '');
});

const expectBottom = ['LOG1.png', 'Q.S 1.png', 'Q.L 1.png', '存档1.png', '读档1.png'];
bottom.children.forEach((btn, i) => {
  const s = srcOf(btn);
  const ok = s && s.indexOf(expectBottom[i]) >= 0;
  check('右下 #' + (i + 1) + ' -> ' + expectBottom[i], ok, s || '');
});

console.log('\n=== custom_ui 显隐 ===');
state.vars.custom_ui = false;
app.refreshQuickMenu();
check('custom_ui=False -> 隐藏', hud.hidden === true);

state.vars.custom_ui = true;
app.refreshQuickMenu();
check('custom_ui=True  -> 显示', hud.hidden === false);

state.vars.custom_ui = undefined;
app.refreshQuickMenu();
check('未定义时默认显示', hud.hidden === false);

console.log('\n=== 快进 / 自动 选中态 ===');
app.vm.skipMode = false;
app.vm.autoMode = false;
app.syncHud();
check('快进默认未选中', !app.hudButtons.skip.classList.contains('selected'));
check('自动默认未选中', !app.hudButtons.auto.classList.contains('selected'));

app.vm.skipMode = true;
app.syncHud();
check('开启快进 -> 选中', app.hudButtons.skip.classList.contains('selected'));
check('选中后换图 快进2', (srcOf(app.hudButtons.skip) || '').indexOf('快进2') >= 0,
  srcOf(app.hudButtons.skip) || '');

app.vm.autoMode = true;
app.syncHud();
check('开启自动 -> 选中', app.hudButtons.auto.classList.contains('selected'));

app.vm.skipMode = false;
app.vm.autoMode = false;
app.syncHud();
check('关闭后恢复 快进1', (srcOf(app.hudButtons.skip) || '').indexOf('快进1') >= 0);

console.log('\n=== 按钮功能 ===');
calls.length = 0;
bottom.children[0]._ev.click({ stopPropagation: noop });
check('历史按钮 -> openHistory', calls.indexOf('history') >= 0, calls.join(','));

calls.length = 0;
bottom.children[1]._ev.click({ stopPropagation: noop });
check('快存按钮 -> quick 槽', app.save.saved.indexOf('quick.1') >= 0, app.save.saved.join(','));

calls.length = 0;
bottom.children[2]._ev.click({ stopPropagation: noop });
check('快读按钮 -> 读 quick 槽', calls.indexOf('load:quick.1') >= 0, calls.join(','));

calls.length = 0;
bottom.children[3]._ev.click({ stopPropagation: noop });
check('存档按钮 -> save 页', calls.indexOf('saveLoad:save') >= 0, calls.join(','));

calls.length = 0;
bottom.children[4]._ev.click({ stopPropagation: noop });
check('读档按钮 -> load 页', calls.indexOf('saveLoad:load') >= 0, calls.join(','));

calls.length = 0;
top.children[2]._ev.click({ stopPropagation: noop });
check('菜单按钮 -> openGameMenu', calls.indexOf('menu') >= 0, calls.join(','));

console.log('\n结果: ' + (fail === 0 ? '通过' : fail + ' 项失败'));
process.exit(fail === 0 ? 0 : 1);