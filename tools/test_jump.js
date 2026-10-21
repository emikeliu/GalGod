#!/usr/bin/env node
/**
 * tools/test_jump.js
 * 验证「跳转后黑屏」是否修好。
 *
 * 场景：
 *   1. 先跑 scene_1_1，停在某句对白上（VM 处于挂起态，_running = true）
 *   2. 中途跳到 scene_3_4
 *   3. 断言：新链能继续推进对白、旧链不会抢帧栈
 *
 * 用法：node tools/test_jump.js
 */

'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const WEB = path.join(ROOT, 'web');

/* --------------------------------------------------------------------------
   DOM 桩（与 test_vm.js 同构，精简版）
   -------------------------------------------------------------------------- */
const noop = () => {};
const store = {};

function makeEl() {
  return {
    style: {}, dataset: {}, children: [], hidden: false, innerHTML: '', textContent: '',
    classList: { add: noop, remove: noop, toggle: noop, contains: () => false },
    appendChild(c) { this.children.push(c); return c; },
    removeChild(c) { const i = this.children.indexOf(c); if (i >= 0) this.children.splice(i, 1); return c; },
    remove: noop, querySelector: () => null, querySelectorAll: () => [],
    addEventListener: noop, removeEventListener: noop,
    setAttribute: noop, removeAttribute: noop, getAttribute: () => null,
    closest: () => null, getBoundingClientRect: () => ({ width: 0, height: 0 }),
    get firstChild() { return this.children[0] || null; },
    focus: noop, click: noop, play: () => Promise.resolve(), pause: noop
  };
}

function createAudioEl() {
  return {
    play: () => Promise.resolve(), pause: noop, load: noop,
    volume: 1, loop: false, currentTime: 0, preload: '', readyState: 0,
    addEventListener: noop, removeAttribute: noop,
    setAttribute: noop, getAttribute: () => '',
    set onended(v) {}, get ended() { return false; }, get paused() { return true; }
  };
}

const els = {};
const sandbox = {
  console, Math, JSON, Date, Promise, Object, Array, String, Number,
  setTimeout, clearTimeout, setInterval, clearInterval,
  performance: { now: () => Date.now() },
  encodeURIComponent, decodeURIComponent,
  localStorage: {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; }
  },
  document: {
    readyState: 'complete',
    getElementById: (id) => (els[id] = els[id] || makeEl()),
    createElement: (t) => (t === 'audio' ? createAudioEl() : makeEl()),
    addEventListener: noop, removeEventListener: noop,
    querySelector: () => null, querySelectorAll: () => [],
    documentElement: makeEl(), body: makeEl(), fullscreenElement: null
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

/* --------------------------------------------------------------------------
   加载模块
   -------------------------------------------------------------------------- */
['js/rpy/strings.js', 'js/rpy/lexer.js', 'js/rpy/parser.js',
 'js/rpy/expr.js', 'js/rpy/compiler.js',
 'js/engine/state.js', 'js/engine/images.js', 'js/engine/actors.js',
 'js/engine/vm.js'].forEach((f) => {
  vm.runInContext(fs.readFileSync(path.join(WEB, f), 'utf8'), sandbox, { filename: f });
});

const { RPYCompiler, RPYState, RPYImages, RPYActors, RPYExpr, RPYVM } = sandbox;

const manifest = JSON.parse(fs.readFileSync(path.join(WEB, 'assets/manifest.json'), 'utf8'));
const overrides = JSON.parse(fs.readFileSync(path.join(WEB, 'assets/overrides.json'), 'utf8'));

const files = manifest.script_files.map((rel) => ({
  path: rel, source: fs.readFileSync(path.join(ROOT, rel), 'utf8')
}));
const program = RPYCompiler.compileAll(files);

/* 角色配置 */
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
   桩
   -------------------------------------------------------------------------- */
const state = new RPYState.State();
const images = new RPYImages.Images(manifest, overrides);
images.load(program);

const said = [];       // 最近显示的对白
let waiting = false;
let resolveSay = null;

const stubSay = {
  isWaiting: false,
  lastSay: null,
  show(op) {
    said.push(op.text);
    stubSay.isWaiting = true;
    waiting = true;
    return new Promise((resolve) => { resolveSay = resolve; });
  },
  advance() {
    if (resolveSay) { const r = resolveSay; resolveSay = null; stubSay.isWaiting = false; waiting = false; r(); }
  },
  hideImmediate() {
    if (resolveSay) { const r = resolveSay; resolveSay = null; stubSay.isWaiting = false; waiting = false; r(); }
  },
  hideBox: noop, setWindowMode: noop, applyAlpha: noop
};

let centeredResolve = null;
const stubCentered = {
  show(text) { said.push('[C]' + text); return new Promise((r) => { centeredResolve = r; }); },
  hide() { if (centeredResolve) { const r = centeredResolve; centeredResolve = null; r(); } }
};

let choiceResolve = null;
const stubChoice = {
  show(cap, who, opts) { return new Promise((r) => { choiceResolve = (i) => r(i); }); },
  hide() { if (choiceResolve) { const r = choiceResolve; choiceResolve = null; r(-1); } }
};

const stubStage = {
  spriteEls: {},
  showSprite: noop, hideSprite: noop, updateSprite: noop, playSpriteAction: noop,
  setBackground: noop, clearBackground: noop, showCG: noop, hideCG: noop, clearCG: noop,
  showRain: noop, hideRain: noop, showOverlay: noop, clearOverlay: noop,
  setFilter: noop, setCamera: noop, resetCamera: noop, rebuild: noop
};

const stubAudio = {
  play: noop, stop: noop, playVoice: noop, stopVoice: noop,
  isVoicePlaying: () => false, onVoiceEnded: noop, applyVolumes: noop
};

const stubTransitions = {
  apply(c, mutate) { mutate(); return Promise.resolve(); },
  linearFadeIn() { return Promise.resolve(); }
};

const actors = new RPYActors.Actors(charConfig, stubStage, images, state);

const machine = new RPYVM.VM({
  program, state, images, actors,
  stage: stubStage, audio: stubAudio, transitions: stubTransitions,
  ui: { say: stubSay, centered: stubCentered, choice: stubChoice, movie: { show: () => Promise.resolve(), hide: noop }, toast: noop }
});

/* --------------------------------------------------------------------------
   驱动
   -------------------------------------------------------------------------- */
const tick = () => new Promise((r) => setTimeout(r, 0));

async function pump(n) {
  for (let i = 0; i < n; i++) {
    await tick();
    if (choiceResolve) { const f = choiceResolve; choiceResolve = null; f(0); continue; }
    if (centeredResolve) { const f = centeredResolve; centeredResolve = null; f(); continue; }
    if (waiting) { stubSay.advance(); continue; }
    if (machine.waiting === 'pause' && machine._pauseResolve) { machine._pauseResolve(); continue; }
    if (!machine.running) break;
  }
}

function snapshot() {
  const f = machine.currentFrame();
  return {
    running: machine.running,
    _running: !!machine._running,
    gen: machine.generation,
    frames: machine.frames.map((x) => x.label + '#' + x.pc),
    label: f ? f.label : null
  };
}

async function main() {
  let fail = 0;

  console.log('=== 场景 1：从主菜单直接跳转 ===');
  machine.jumpTo('scene_3_4');
  await pump(40);
  const s1 = snapshot();
  console.log('  状态:', JSON.stringify(s1));
  console.log('  最近对白:', said.slice(-2));
  if (!s1.running) { console.log('  [FAIL] 跳转后 VM 未运行'); fail++; }
  if (s1.label !== 'scene_3_4') { console.log('  [FAIL] 未停在 scene_3_4'); fail++; }
  if (said.length < 2) { console.log('  [FAIL] 跳转后没有推进任何对白（黑屏）'); fail++; }
  if (!fail) console.log('  [ OK ] 对白正常推进\n');

  console.log('=== 场景 2：播放中再跳转（旧链挂在 say 上） ===');
  const before = said.length;
  machine.jumpTo('scene_1_2');
  await pump(50);
  const s2 = snapshot();
  console.log('  状态:', JSON.stringify(s2));
  console.log('  新增对白:', said.slice(before, before + 3));
  if (s2.label !== 'scene_1_2') { console.log('  [FAIL] 未停在 scene_1_2'); fail++; }
  if (said.length <= before) { console.log('  [FAIL] 第二次跳转后没有推进（黑屏）'); fail++; }
  const dupCheck = said.slice(before).filter((t) => said.slice(0, before).indexOf(t) >= 0);
  console.log('  旧链残留检查: 重名对白 ' + dupCheck.length + ' 条');
  if (!fail) console.log('  [ OK ] 旧链已作废，新链接管\n');

  console.log('=== 场景 3：连续跳转 3 次（压力测试） ===');
  for (const lb of ['scene_2_1', 'end1', 'after_story_noctella']) {
    const n = said.length;
    machine.jumpTo(lb);
    await pump(30);
    const s = snapshot();
    const ok = s.running && s.label === lb && said.length > n;
    console.log('  ' + (ok ? '[ OK ]' : '[FAIL]') + ' -> ' + lb +
      '  running=' + s.running + ' 新对白=' + (said.length - n));
    if (!ok) fail++;
  }

  console.log('\n结果: ' + (fail === 0 ? '通过' : fail + ' 项失败'));
  process.exit(fail === 0 ? 0 : 1);
}

main().catch((e) => { console.error(e); process.exit(1); });