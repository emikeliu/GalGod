#!/usr/bin/env node
/**
 * tools/test_diag.js
 * 无头验证 F9 调试台四个页签都能渲染出内容。
 * 用轻量 DOM 桩，检查每个页签渲染后的 innerHTML 长度与关键文本。
 */

'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const WEB = path.join(ROOT, 'web');

/* --------------------------------------------------------------------------
   极简 DOM 桩：只实现 diag.js 用到的 API
   -------------------------------------------------------------------------- */
function makeEl(tag) {
  const el = {
    tagName: (tag || 'div').toUpperCase(),
    children: [],
    style: {},
    dataset: {},
    attrs: {},
    _html: '',
    hidden: false,
    className: '',
    id: '',
    scrollTop: 0,
    offsetTop: 0,
    clientHeight: 400,
    textContent: '',
    classList: {
      add() {}, remove() {}, toggle() {}, contains: () => false
    },
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    appendChild(c) { this.children.push(c); c.parentNode = this; return c; },
    removeChild(c) {
      const i = this.children.indexOf(c);
      if (i >= 0) this.children.splice(i, 1);
      return c;
    },
    remove() {},
    setAttribute(k, v) { this.attrs[k] = v; if (k === 'hidden') this.hidden = true; },
    getAttribute(k) { return this.attrs[k]; },
    removeAttribute(k) { delete this.attrs[k]; if (k === 'hidden') this.hidden = false; },
    addEventListener() {},
    removeEventListener() {},
    querySelector() { return null; },
    querySelectorAll() { return []; },
    closest() { return null; },
    focus() {},
    click() {}
  };
  return el;
}

const REG = {};
function getEl(id) {
  if (!REG[id]) { REG[id] = makeEl('div'); REG[id].id = id; }
  return REG[id];
}

const sandbox = {
  console, Math, JSON, Date, String, Number, Object, Array, Promise,
  setTimeout: (f) => setImmediate(f),
  setInterval: () => 0,
  clearInterval: () => {},
  clearTimeout: () => {},
  encodeURIComponent,
  document: {
    readyState: 'complete',
    body: makeEl('body'),
    getElementById: getEl,
    createElement: (t) => makeEl(t),
    addEventListener() {},
    removeEventListener() {},
    querySelector() { return null; },
    querySelectorAll() { return []; }
  },
  localStorage: {
    _d: {},
    getItem(k) { return this._d[k] == null ? null : this._d[k]; },
    setItem(k, v) { this._d[k] = String(v); },
    removeItem(k) { delete this._d[k]; }
  }
};
sandbox.window = sandbox;
sandbox.global = sandbox;
vm.createContext(sandbox);

/* --------------------------------------------------------------------------
   加载依赖
   -------------------------------------------------------------------------- */
['js/rpy/strings.js', 'js/rpy/lexer.js', 'js/rpy/parser.js',
 'js/rpy/expr.js', 'js/rpy/compiler.js',
 'js/engine/state.js', 'js/engine/images.js', 'js/ui/diag.js'].forEach((f) => {
  vm.runInContext(fs.readFileSync(path.join(WEB, f), 'utf8'), sandbox, { filename: f });
});

const { RPYCompiler, RPYState, RPYImages, RPYDiag, RPYStrings } = sandbox;

/* --------------------------------------------------------------------------
   构造最小 App
   -------------------------------------------------------------------------- */
const manifest = JSON.parse(fs.readFileSync(path.join(WEB, 'assets/manifest.json'), 'utf8'));
const overrides = JSON.parse(fs.readFileSync(path.join(WEB, 'assets/overrides.json'), 'utf8'));
const files = manifest.script_files.map((rel) => ({
  path: rel, source: fs.readFileSync(path.join(ROOT, rel), 'utf8')
}));
const program = RPYCompiler.compileAll(files);

const state = new RPYState.State();
state.vars.quick_menu = true;
state.vars.bad_end_flag = 2;
state.bg = { name: 'bg street1_1' };
state.sprites.lx = { expr: '微笑', pos: 'center', zoom: 0.6, xOffset: 0, yOffset: 1250, visible: true };
state.music = { path: 'audio/bgm/BGM_日常2.ogg', loop: true };

const images = new RPYImages.Images(manifest, overrides);
images.load(program);

const app = {
  program,
  images,
  state,
  runtimeDiagnostics: [
    { kind: 'DEMO', file: 'scenes/1_1.rpy', line: 42, message: '示例诊断条目' }
  ],
  vm: {
    lastPc: { label: 'scene_1_1', pc: 12 },
    diagnostics: [],
    rollbackStack: [1, 2, 3],
    running: true,
    waiting: 'say',
    autoMode: false,
    skipMode: false
  },
  toast() {},
  closeAllMenus() {},
  ui: {
    say: { hideImmediate() {} },
    centered: { hide() {} },
    choice: { hide() {} }
  },
  audio: { stop() {}, stopVoice() {} },
  stage: {
    clearBackground() {}, clearCG() {}, clearOverlay() {},
    hideRain() {}, resetCamera() {}, setFilter() {},
    spriteEls: {}
  },
  stats() {
    let ops = 0;
    Object.keys(program.labels).forEach((k) => { ops += program.labels[k].ops.length; });
    return {
      scripts: program.files.length,
      labels: Object.keys(program.labels).length,
      ops,
      images: Object.keys(program.images).length,
      assets: manifest.assets.length
    };
  }
};

/* --------------------------------------------------------------------------
   渲染测试
   -------------------------------------------------------------------------- */
const diag = new RPYDiag.Diag(app);

const tabs = ['issues', 'jump', 'vars', 'trace'];
let fail = 0;

console.log('=== 诊断台渲染测试 ===\n');

tabs.forEach((tab) => {
  diag.tab = tab;
  diag.open = true;
  diag.render();

  const html = diag.body.innerHTML || '';
  const len = html.length;
  const hasError = html.indexOf('PANEL_ERROR') >= 0;

  console.log('[' + (hasError ? 'FAIL' : ' OK ') + '] ' + tab.padEnd(8) +
    ' html=' + String(len).padStart(6) + ' 字节');

  if (len < 40) {
    console.log('        内容过少，可能渲染失败');
    fail++;
  }
  if (hasError) {
    console.log('        ' + html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').slice(0, 300));
    fail++;
  }
});

/* 内容抽查 */
diag.tab = 'vars'; diag.render();
const varsHtml = diag.body.innerHTML;
const varChecks = ['quick_menu', 'bad_end_flag', 'persistent', '舞台', 'bg street1_1'];
console.log('\n变量页抽查:');
varChecks.forEach((k) => {
  const ok = varsHtml.indexOf(k) >= 0;
  console.log('  ' + (ok ? 'OK  ' : 'MISS') + ' ' + k);
  if (!ok) fail++;
});

diag.tab = 'trace'; diag.render();
const traceHtml = diag.body.innerHTML;
const traceChecks = ['scene_1_1', '#12', 'current'];
console.log('\n指令追踪抽查:');
traceChecks.forEach((k) => {
  const ok = traceHtml.indexOf(k) >= 0;
  console.log('  ' + (ok ? 'OK  ' : 'MISS') + ' ' + k);
  if (!ok) fail++;
});

diag.tab = 'jump'; diag.render();

/* 说明：跳转按钮由 innerHTML 生成的容器承载，DOM 桩不解析 HTML，
   所以这里校验 JUMP_LIST 常量与 HTML 中的 label 列表，
   而不是查按钮的 textContent。 */
const jumpHtml = diag.body.innerHTML || '';
const jumpChecks = [
  ['after_story_noctella', jumpHtml],
  ['end1', jumpHtml],
  ['Scene 1-1', RPYDiag.JUMP_LIST.map((x) => x.text).join('|')],
  ['interlude_interview', RPYDiag.JUMP_LIST.map((x) => x.label).join('|')]
];
console.log('\n章节跳转抽查:');
jumpChecks.forEach(([k, hay]) => {
  const ok = hay.indexOf(k) >= 0;
  console.log('  ' + (ok ? 'OK  ' : 'MISS') + ' ' + k);
  if (!ok) fail++;
});

/* 桩的 appendChild 不写入 innerHTML，这里递归收集子节点文本 */
function collectText(el) {
  let out = el.textContent || '';
  (el.children || []).forEach((c) => { out += collectText(c); });
  return out;
}

diag.tab = 'issues'; diag.render();
const issuesHtml = diag.body.innerHTML;
const issueChecks = ['DEMO', '示例诊断条目', 'label'];
console.log('\n诊断页抽查:');
issueChecks.forEach((k) => {
  const ok = issuesHtml.indexOf(k) >= 0;
  console.log('  ' + (ok ? 'OK  ' : 'MISS') + ' ' + k);
  if (!ok) fail++;
});

console.log('\n结果: ' + (fail === 0 ? '通过' : fail + ' 项失败'));
process.exit(fail === 0 ? 0 : 1);