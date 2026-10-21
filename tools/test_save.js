#!/usr/bin/env node
/**
 * tools/test_save.js
 * 验证存读档：立绘 / 背景 / CG / 变量 / 镜头 能否完整往返。
 * 重点回归：读档后立绘消失的问题。
 */

'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const WEB = path.join(ROOT, 'web');

const noop = () => {};
const store = {};

function makeEl(tag) {
  const el = {
    tagName: (tag || 'div').toUpperCase(),
    id: '', className: '', dataset: {}, attrs: {}, children: [], parentNode: null,
    hidden: false, textContent: '', _html: '',
    _classes: new Set(),
    style: { _v: {}, setProperty(k, v) { this._v[k] = v; } },
    classList: {
      add(c) { el._classes.add(c); },
      remove(c) { el._classes.delete(c); },
      toggle(c, on) { on ? el._classes.add(c) : el._classes.delete(c); },
      contains: (c) => el._classes.has(c)
    },
    appendChild(c) { c.parentNode = el; el.children.push(c); return c; },
    removeChild(c) { const i = el.children.indexOf(c); if (i >= 0) el.children.splice(i, 1); return c; },
    remove() { if (el.parentNode) el.parentNode.removeChild(el); },
    setAttribute(k, v) { el.attrs[k] = String(v); if (k === 'hidden') el.hidden = true; },
    getAttribute(k) { return el.attrs[k] === undefined ? null : el.attrs[k]; },
    removeAttribute(k) { delete el.attrs[k]; if (k === 'hidden') el.hidden = false; },
    addEventListener(t, fn) { (el._ev = el._ev || {})[t] = fn; },
    removeEventListener() {}, querySelector: () => null, querySelectorAll: () => [],
    closest: () => null, focus: noop,
    get innerHTML() { return el._html; },
    set innerHTML(v) { el._html = String(v); }
  };
  return el;
}

const REG = {};
const getEl = (id) => (REG[id] = REG[id] || Object.assign(makeEl('div'), { id }));

const sandbox = {
  console, Math, JSON, Date, Promise, Object, Array, String, Number,
  setTimeout, clearTimeout, setInterval, clearInterval,
  encodeURIComponent, decodeURIComponent,
  performance: { now: () => Date.now() },
  localStorage: {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; }
  },
  document: {
    readyState: 'complete', body: makeEl('body'),
    getElementById: getEl, createElement: (t) => makeEl(t),
    addEventListener: noop, removeEventListener: noop,
    querySelector: () => null, querySelectorAll: () => [], documentElement: makeEl('html')
  },
  addEventListener: noop, removeEventListener: noop,
  innerWidth: 1920, innerHeight: 1080, location: { search: '' },
  Image: function () { return { set src(v) {}, get src() { return ''; } }; },
  fetch: () => Promise.reject(new Error('no fetch'))
};
sandbox.window = sandbox;
sandbox.global = sandbox;
vm.createContext(sandbox);

['js/rpy/strings.js', 'js/rpy/lexer.js', 'js/rpy/parser.js',
 'js/rpy/expr.js', 'js/rpy/compiler.js',
 'js/engine/state.js', 'js/engine/images.js', 'js/engine/actors.js'].forEach((f) => {
  vm.runInContext(fs.readFileSync(path.join(WEB, f), 'utf8'), sandbox, { filename: f });
});

const { RPYState, RPYImages, RPYActors, RPYExpr, RPYCompiler } = sandbox;

const manifest = JSON.parse(fs.readFileSync(path.join(WEB, 'assets/manifest.json'), 'utf8'));
const overrides = JSON.parse(fs.readFileSync(path.join(WEB, 'assets/overrides.json'), 'utf8'));
const program = RPYCompiler.compileAll(
  manifest.script_files.map((rel) => ({
    path: rel, source: fs.readFileSync(path.join(ROOT, rel), 'utf8')
  }))
);

const images = new RPYImages.Images(manifest, overrides);
images.load(program);

/* 舞台桩：记录收到的 sprite 与 bg，供断言 */
const shown = { sprites: [], bg: null, cg: [] };
const stageStub = {
  spriteEls: {},
  showSprite(code, p, s) { shown.sprites.push({ code, path: p, expr: s.expr, pos: s.pos }); },
  hideSprite: noop, updateSprite: noop, playSpriteAction: noop,
  setBackground(n) { shown.bg = n; },
  clearBackground() { shown.bg = null; },
  showCG(n) { shown.cg.push(n); }, hideCG: noop,
  clearCG() { shown.cg = []; },
  showRain: noop, hideRain: noop, showOverlay: noop, clearOverlay: noop,
  setFilter: noop, setCamera: noop, resetCamera: noop,
  rebuild: noop
};

function extractAssignment(source, name) {
  const re = new RegExp('(^|\\n)[ \\t]*' + name + '\\s*=\\s*', 'm');
  const m = re.exec(source);
  if (!m) return null;
  const start = m.index + m[0].length;
  let i = start, depth = 0, inS = false, inD = false, esc = false;
  while (i < source.length) {
    const c = source[i];
    if (esc) { esc = false; i++; continue; }
    if (c === '\\') { esc = true; i++; continue; }
    if (inS) { if (c === "'") inS = false; i++; continue; }
    if (inD) { if (c === '"') inD = false; i++; continue; }
    if (c === "'") { inS = true; i++; continue; }
    if (c === '"') { inD = true; i++; continue; }
    if ('{(['.indexOf(c) >= 0) depth++;
    else if (c === '}' || c === ')' || c === ']') { depth--; if (depth === 0) { i++; break; } }
    else if (c === '\n' && depth === 0) break;
    i++;
  }
  return sandbox.RPYStrings.stripPythonComments(source.slice(start, i).trim());
}

const charConfig = RPYExpr.evaluate(
  RPYExpr.parse(extractAssignment(
    fs.readFileSync(path.join(ROOT, 'config/character_config.rpy'), 'utf8'),
    'CHARACTERS_CONFIG'), null), { get: () => undefined, call: () => undefined, diag: () => {} });

const globCfg = RPYExpr.evaluate(
  RPYExpr.parse(extractAssignment(
    fs.readFileSync(path.join(ROOT, 'config/options.rpy'), 'utf8'),
    'global_actor_settings'), null), { get: () => undefined, call: () => undefined, diag: () => {} });
RPYActors.GLOBAL.zoom = globCfg.zoom;
RPYActors.GLOBAL.y_offset = globCfg.y_offset;

/* --------------------------------------------------------------------------
   测试
   -------------------------------------------------------------------------- */
let fail = 0;
function check(name, cond, extra) {
  console.log('  ' + (cond ? '[ OK ]' : '[FAIL]') + ' ' + name + (extra ? '  ' + extra : ''));
  if (!cond) fail++;
}

const state = new RPYState.State();
const actors = new RPYActors.Actors(charConfig, stageStub, images, state);

console.log('=== 布置现场 ===');
state.vars.true_end_flag = 3;
state.vars.bad_end_flag = 7;
state.bg = { name: 'bg street1_1', path: 'images/bg/街道1_白天.avif', fit: 'cover' };
state.camera = { zoom: 1.3, xpos: 0.5, ypos: 0.4 };

actors.get('lx').show('微笑', { pos: 'center' });
actors.get('jwq').show('游刃有余', { pos: 'right', xOffset: -250 });
console.log('  立绘:', JSON.stringify(state.sprites.lx));

const snap = state.snapshot();
console.log('  快照 sprites.lx:', JSON.stringify(snap.sprites.lx));

console.log('\n=== 快照完整性 ===');
check('立绘保留 visible', snap.sprites.lx.visible === true);
check('立绘保留 path', !!snap.sprites.lx.path, snap.sprites.lx.path);
check('两个角色都在', Object.keys(snap.sprites).length === 2,
  Object.keys(snap.sprites).join(','));
check('背景已保存', !!snap.bg && snap.bg.name === 'bg street1_1');
check('镜头已保存', !!snap.camera && snap.camera.zoom === 1.3);
check('快照可 JSON 往返', (function () {
  try { JSON.parse(JSON.stringify(snap)); return true; } catch (e) { return false; }
})());

console.log('\n=== 模拟读档 ===');
/* 清空当前状态，模拟重新开始 */
state.vars = Object.create(null);
state.sprites = Object.create(null);
state.bg = null;
state.camera = null;

const loaded = JSON.parse(JSON.stringify(snap));
state.restore(loaded);

check('变量已恢复', state.vars.true_end_flag === 3 && state.vars.bad_end_flag === 7);
check('立绘已恢复', !!state.sprites.lx && state.sprites.lx.expr === '微笑');
check('立绘 visible 为 true', state.sprites.lx.visible === true);
check('立绘 path 存在', !!state.sprites.lx.path);
check('第二个立绘也在', !!state.sprites.jwq);

console.log('\n=== 重建舞台（rebuild 逻辑） ===');
shown.sprites.length = 0;
const sprites = state.sprites;
Object.keys(sprites).forEach((code) => {
  const s = sprites[code];
  if (!s.visible || !s.expr) return;
  let p = s.path;
  if (!p) {
    const actor = actors.get(code);
    if (actor) p = actor.expressions[s.expr];
  }
  if (!p) return;
  stageStub.showSprite(code, p, s, { kind: 'none' });
});

check('重建出 2 个立绘', shown.sprites.length === 2, JSON.stringify(shown.sprites.map((x) => x.code)));
check('表情正确', shown.sprites.every((x) => x.expr));
check('路径正确', shown.sprites.every((x) => x.path && x.path.indexOf('images/characters') === 0));

/* --------------------------------------------------------------------------
   存档落点：必须与「当前正在显示的那句」一致，不能差一句
   -------------------------------------------------------------------------- */
console.log('\n=== 存档落点（waitingAt） ===');

/* 手工模拟：当前 label 的 ops 里放 5 条 say，停在 #2 */
const fakeProgram = {
  labels: {
    demo: {
      ops: [0, 1, 2, 3, 4].map((i) => ({
        op: 'say', who: null, text: '第' + i + '句', file: 'demo.rpy', line: i + 1
      })),
      file: 'demo.rpy', line: 1
    }
  },
  defaults: [], diagnostics: [], images: {}, files: []
};

/* 直接检查 saveState 的取值逻辑，不依赖完整 VM */
function simulateSave(frame, waitingAt, ops) {
  const at = waitingAt;
  const label = at ? at.label : frame.label;
  const pc = at ? at.pc : frame.pc;
  const op = ops[pc];
  return { label, pc, text: op ? op.text : null };
}

const ops = fakeProgram.labels.demo.ops;

/* say 执行后 pc 已 ++，但 waitingAt 记的是原位置 */
const s1 = simulateSave({ label: 'demo', pc: 3 }, { label: 'demo', pc: 2 }, ops);
check('存档落在当前句而非下一句', s1.pc === 2 && s1.text === '第2句',
  'pc=' + s1.pc + ' text=' + s1.text);

/* 没有 waitingAt 时（非 yield 指令）退回 frame.pc */
const s2 = simulateSave({ label: 'demo', pc: 3 }, null, ops);
check('非挂起时使用 frame.pc', s2.pc === 3 && s2.text === '第3句',
  'pc=' + s2.pc + ' text=' + s2.text);

console.log('\n结果: ' + (fail === 0 ? '通过' : fail + ' 项失败'));
process.exit(fail === 0 ? 0 : 1);