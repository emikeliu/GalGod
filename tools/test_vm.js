#!/usr/bin/env node
/**
 * tools/test_vm.js
 * 无头 VM 冒烟测试：用桩对象替代 DOM/音频/舞台，
 * 驱动真实剧本执行，验证：
 *   - label / call / return 帧栈
 *   - $ actor.show(...) 的参数绑定
 *   - if / menu 分支走向
 *   - scene / show / hide / play 指令分发
 *
 * 用法：node tools/test_vm.js [label]
 */

'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const WEB = path.join(ROOT, 'web');

/* --------------------------------------------------------------------------
   最小 window + DOM 桩
   -------------------------------------------------------------------------- */
const noop = () => {};
const store = {};

function makeEl() {
  return {
    style: {},
    dataset: {},
    classList: { add: noop, remove: noop, toggle: noop, contains: () => false },
    children: [],
    hidden: false,
    innerHTML: '',
    textContent: '',
    appendChild(c) { this.children.push(c); return c; },
    removeChild(c) {
      const i = this.children.indexOf(c);
      if (i >= 0) this.children.splice(i, 1);
      return c;
    },
    remove: noop,
    querySelector: () => null,
    querySelectorAll: () => [],
    addEventListener: noop,
    removeEventListener: noop,
    setAttribute: noop,
    removeAttribute: noop,
    getAttribute: () => null,
    closest: () => null,
    getBoundingClientRect: () => ({ width: 0, height: 0 }),
    get firstChild() { return this.children[0] || null; },
    focus: noop,
    click: noop,
    play: () => Promise.resolve(),
    pause: noop
  };
}

const els = {};
function getEl(id) {
  if (!els[id]) els[id] = makeEl();
  return els[id];
}

const sandbox = {
  console,
  Math,
  JSON,
  Date,
  Promise,
  setTimeout,
  clearTimeout,
  setInterval,
  clearInterval,
  performance: { now: () => Date.now() },
  /* 无头测试：所有定时器立即触发，避免 5 秒 hard pause 拖死测试 */
  setTimeout: (fn) => setImmediate(fn),
  setInterval: (fn) => setImmediate(fn),
  clearTimeout: () => {},
  clearInterval: () => {},
  encodeURIComponent,
  decodeURIComponent,
  localStorage: {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; }
  },
  document: {
    readyState: 'complete',
    getElementById: getEl,
    createElement: () => makeEl(),
    addEventListener: noop,
    removeEventListener: noop,
    querySelector: () => null,
    querySelectorAll: () => [],
    documentElement: makeEl(),
    fullscreenElement: null
  },
  addEventListener: noop,
  removeEventListener: noop,
  innerWidth: 1920,
  innerHeight: 1080,
  location: { search: '' },
  Image: function () { return { set src(v) {}, get src() { return ''; } }; },
  Audio: function () {
    return {
      play: () => Promise.resolve(),
      pause: noop,
      load: noop,
      volume: 1,
      loop: false,
      currentTime: 0,
      preload: '',
      addEventListener: noop,
      removeAttribute: noop,
      set onended(v) {},
      get ended() { return false; },
      get paused() { return true; }
    };
  },
  fetch: () => Promise.reject(new Error('no fetch in headless'))
};
sandbox.window = sandbox;
sandbox.global = sandbox;
vm.createContext(sandbox);

/* --------------------------------------------------------------------------
   加载所需模块（跳过依赖 DOM 的 ui/stage）
   -------------------------------------------------------------------------- */
['js/rpy/strings.js', 'js/rpy/lexer.js', 'js/rpy/parser.js',
 'js/rpy/expr.js', 'js/rpy/compiler.js',
 'js/engine/state.js', 'js/engine/images.js', 'js/engine/actors.js'].forEach((f) => {
  vm.runInContext(fs.readFileSync(path.join(WEB, f), 'utf8'), sandbox, { filename: f });
});

const { RPYCompiler, RPYState, RPYImages, RPYActors, RPYExpr } = sandbox;

/* --------------------------------------------------------------------------
   编译
   -------------------------------------------------------------------------- */
const manifest = JSON.parse(fs.readFileSync(path.join(WEB, 'assets', 'manifest.json'), 'utf8'));
const overrides = JSON.parse(fs.readFileSync(path.join(WEB, 'assets', 'overrides.json'), 'utf8'));

const files = manifest.script_files.map((rel) => ({
  path: rel,
  source: fs.readFileSync(path.join(ROOT, rel), 'utf8')
}));

const program = RPYCompiler.compileAll(files);

/* --------------------------------------------------------------------------
   角色配置（复用 boot 的抽取逻辑，这里简化：直接 eval CHARACTERS_CONFIG）
   -------------------------------------------------------------------------- */
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
    if (c === '{' || c === '(' || c === '[') depth++;
    else if (c === '}' || c === ')' || c === ']') { depth--; if (depth === 0) { i++; break; } }
    else if (c === '\n' && depth === 0) break;
    i++;
  }
  /* 去掉跨行字典里的 # 注释 */
  return sandbox.RPYStrings.stripPythonComments(source.slice(start, i).trim());
}

const cfgSrc = fs.readFileSync(path.join(ROOT, 'config/character_config.rpy'), 'utf8');
const cfgExpr = extractAssignment(cfgSrc, 'CHARACTERS_CONFIG');
const charConfig = RPYExpr.evaluate(RPYExpr.parse(cfgExpr, null), {
  get: () => undefined, call: () => undefined, diag: () => {}
});

const globSrc = fs.readFileSync(path.join(ROOT, 'config/options.rpy'), 'utf8');
const globExpr = extractAssignment(globSrc, 'global_actor_settings');
const globCfg = RPYExpr.evaluate(RPYExpr.parse(globExpr, null), {
  get: () => undefined, call: () => undefined, diag: () => {}
});
RPYActors.GLOBAL.zoom = globCfg.zoom;
RPYActors.GLOBAL.y_offset = globCfg.y_offset;

console.log('角色配置: ' + Object.keys(charConfig).join(', '));
console.log('全局立绘: zoom=' + globCfg.zoom + ' y_offset=' + globCfg.y_offset);

/* --------------------------------------------------------------------------
   桩：Stage / Audio / Transition / UI
   -------------------------------------------------------------------------- */
const log = [];
const state = new RPYState.State();
const images = new RPYImages.Images(manifest, overrides);
images.load(program);

const stubStage = {
  spriteEls: {},
  showSprite(code, path, st) { log.push(['sprite', code, st.expr, st.pos]); },
  hideSprite(code) { log.push(['spriteHide', code]); },
  updateSprite() {},
  playSpriteAction(code, a) { log.push(['act', code, a]); },
  setBackground(name) { log.push(['bg', name]); },
  clearBackground() {},
  showCG(name) { log.push(['cg', name]); },
  hideCG() {},
  clearCG() {},
  showRain(w) { log.push(['rain', w]); },
  hideRain() {},
  showOverlay(n) { log.push(['overlay', n]); },
  clearOverlay() {},
  setFilter(f) { log.push(['filter', f]); },
  setCamera(z) { log.push(['camera', z]); },
  resetCamera() {},
  rebuild() {}
};

const stubAudio = {
  play(ch, p) { log.push(['play', ch, p]); },
  stop(ch) { log.push(['stop', ch]); },
  playVoice(p) { log.push(['voice', p]); },
  stopVoice() {},
  isVoicePlaying: () => false,
  onVoiceEnded: noop,
  applyVolumes: noop
};

const actors = new RPYActors.Actors(charConfig, stubStage, images, state);

/* UI 桩：say / centered / choice 由测试脚本控制"点击" */
let sayQueue = [];
let choicePicker = null;
const stubSay = {
  isWaiting: false,
  lastSay: null,
  show(op) {
    sayQueue.push({ who: op.who, text: op.text });
    log.push(['say', op.who, op.text.slice(0, 20)]);
    stubSay.isWaiting = true;
    return new Promise((resolve) => {
      stubSay._resolve = () => { stubSay.isWaiting = false; resolve(); };
    });
  },
  advance() { if (stubSay._resolve) { const r = stubSay._resolve; stubSay._resolve = null; r(); } },
  hideImmediate() {},
  hideBox() {},
  setWindowMode() {},
  applyAlpha() {}
};

const stubCentered = {
  show(text) {
    log.push(['centered', text]);
    return new Promise((resolve) => { stubCentered._resolve = resolve; });
  },
  hide() {}
};

const stubChoice = {
  show(caption, who, options) {
    log.push(['menu', caption, options.map((o) => o.text)]);
    return new Promise((resolve) => {
      choicePicker = (idx) => resolve(idx);
    });
  }
};

const stubMovie = { show: () => Promise.resolve(), hide: noop };

const stubTransitions = {
  apply(container, mutate, spec) { mutate(); return Promise.resolve(); },
  linearFadeIn() { return Promise.resolve(); }
};

/* --------------------------------------------------------------------------
   VM（从 vm.js 加载，注入桩）
   -------------------------------------------------------------------------- */
vm.runInContext(fs.readFileSync(path.join(WEB, 'js/engine/vm.js'), 'utf8'),
  sandbox, { filename: 'js/engine/vm.js' });

/* 让 vm.js 内部能拿到 RPYState（它只用 global.RPYState？实际 vm 只用传入的 state） */
const machine = new sandbox.RPYVM.VM({
  program,
  state,
  images,
  actors,
  stage: stubStage,
  audio: stubAudio,
  transitions: stubTransitions,
  ui: {
    say: stubSay,
    centered: stubCentered,
    choice: stubChoice,
    movie: stubMovie,
    toast: noop
  }
});

/* --------------------------------------------------------------------------
   驱动：自动"点击"推进，直到跑完 N 步
   -------------------------------------------------------------------------- */
const TARGET_LABEL = process.argv[2] || 'scene_1_1';
const MAX_STEPS = parseInt(process.env.STEPS || '120', 10);

function tick() {
  return new Promise((r) => setTimeout(r, 0));
}

async function main() {
  console.log('\n=== 执行 ' + TARGET_LABEL + ' ===');
  const startLabel = process.argv[3] || TARGET_LABEL;

  if (!program.labels[startLabel]) {
    console.error('label 不存在: ' + startLabel);
    process.exit(1);
  }

  machine.start(startLabel);

  for (let i = 0; i < MAX_STEPS; i++) {
    await tick();

    /* 优先级：菜单 > 居中文本 > 对白 */
    if (choicePicker) {
      const pick = 0;
      log.push(['pick', pick]);
      const f = choicePicker;
      choicePicker = null;
      f(pick);
      continue;
    }
    if (stubCentered._resolve) {
      const r = stubCentered._resolve;
      stubCentered._resolve = null;
      log.push(['click-centered']);
      r();
      continue;
    }
    if (stubSay.isWaiting) {
      log.push(['click-say']);
      stubSay.advance();
      continue;
    }
    if (machine.waiting === 'pause' && machine._pauseResolve) {
      machine._pauseResolve();
      continue;
    }
    if (!machine.running) break;
  }

  /* ------------------------------------------------------------------------
     结果
     ------------------------------------------------------------------------ */
  console.log('执行日志 ' + log.length + ' 条，前 70 条：\n');
  log.slice(0, 70).forEach((e, i) => {
    console.log('  ' + String(i).padStart(3) + '  ' + formatEntry(e));
  });

  const counts = {};
  log.forEach((e) => { counts[e[0]] = (counts[e[0]] || 0) + 1; });
  console.log('\n=== 指令统计 ===');
  Object.keys(counts).sort().forEach((k) => {
    console.log('  ' + k + ': ' + counts[k]);
  });

  console.log('\n=== 运行时诊断 ===');
  const diags = machine.diagnostics.filter((d) =>
    !['IGNORED_STATEMENT'].includes(d.kind));
  if (!diags.length) {
    console.log('  无');
  } else {
    const byKind = {};
    diags.forEach((d) => { (byKind[d.kind] = byKind[d.kind] || []).push(d); });
    Object.keys(byKind).forEach((k) => {
      console.log('  ' + k + ': ' + byKind[k].length);
      byKind[k].slice(0, 6).forEach((d) => {
        console.log('    ' + d.file + ':' + d.line + '  ' + d.message);
      });
    });
  }

  console.log('\n=== 状态 ===');
  console.log('  vars: ' + JSON.stringify(state.vars));
  console.log('  立绘: ' + Object.keys(state.sprites).join(', '));
  console.log('  音乐: ' + (state.music ? state.music.path : '(none)'));
}

function formatEntry(e) {
  switch (e[0]) {
    case 'say': return 'say  ' + (e[1] || '旁白') + '  "' + e[2] + '"';
    case 'sprite': return 'sprite ' + e[1] + ' 表情=' + e[2] + ' pos=' + e[3];
    case 'bg': return 'bg   ' + e[1];
    case 'play': return 'play ' + e[1] + '  ' + e[2];
    case 'menu': return 'menu "' + (e[1] || '') + '" -> ' + JSON.stringify(e[2]);
    case 'centered': return 'centered "' + e[1].slice(0, 30) + '"';
    case 'camera': return 'camera zoom=' + e[1];
    case 'filter': return 'filter ' + e[1];
    default: return e.join(' ');
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});