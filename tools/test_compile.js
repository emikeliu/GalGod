#!/usr/bin/env node
/**
 * tools/test_compile.js
 * 无头验证：在 Node 里加载 rpy/lexer、rpy/parser、rpy/compiler，
 * 对工程内全部 .rpy 执行「lex -> parse -> compile」，输出诊断统计。
 *
 * 用法：node tools/test_compile.js
 */

'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const WEB = path.join(ROOT, 'web');

/* --------------------------------------------------------------------------
   构造一个最小 window 环境
   -------------------------------------------------------------------------- */
const sandbox = { console, encodeURIComponent, decodeURIComponent, Math, JSON, Date };
sandbox.window = sandbox;
sandbox.global = sandbox;
vm.createContext(sandbox);

function load(rel) {
  const file = path.join(WEB, rel);
  const code = fs.readFileSync(file, 'utf8');
  vm.runInContext(code, sandbox, { filename: rel });
}

['js/rpy/strings.js', 'js/rpy/lexer.js', 'js/rpy/parser.js',
 'js/rpy/expr.js', 'js/rpy/compiler.js'].forEach(load);

const { RPYCompiler, RPYLexer, RPYParser } = sandbox;

/* --------------------------------------------------------------------------
   收集文件
   -------------------------------------------------------------------------- */
const manifestPath = path.join(WEB, 'assets', 'manifest.json');
if (!fs.existsSync(manifestPath)) {
  console.error('缺少 web/assets/manifest.json，请先运行 python3 tools/gen_manifest.py');
  process.exit(1);
}
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

const files = manifest.script_files.map((rel) => ({
  path: rel,
  source: fs.readFileSync(path.join(ROOT, rel), 'utf8')
}));

console.log('脚本文件: ' + files.length);

/* --------------------------------------------------------------------------
   编译
   -------------------------------------------------------------------------- */
const t0 = Date.now();
const program = RPYCompiler.compileAll(files);
const ms = Date.now() - t0;

const labelNames = Object.keys(program.labels);
const realLabels = labelNames.filter((n) => !program.labels[n].synthetic);

let totalOps = 0;
labelNames.forEach((n) => { totalOps += program.labels[n].ops.length; });

console.log('耗时      : ' + ms + ' ms');
console.log('label     : ' + realLabels.length + ' 个');
console.log('指令      : ' + totalOps + ' 条');
console.log('image 定义: ' + Object.keys(program.images).length + ' 个');
console.log('define    : ' + program.defines.length + ' 条');
console.log('default   : ' + program.defaults.length + ' 条');
console.log('screen    : ' + Object.keys(program.screens).length + ' 个');
console.log('transform : ' + Object.keys(program.transforms).length + ' 个');

/* --------------------------------------------------------------------------
   诊断汇总
   -------------------------------------------------------------------------- */
const diags = program.diagnostics;
const byKind = {};
diags.forEach((d) => { (byKind[d.kind] = byKind[d.kind] || []).push(d); });

console.log('\n=== 诊断 ===');
const kinds = Object.keys(byKind).sort();
if (!kinds.length) {
  console.log('无问题');
} else {
  kinds.forEach((k) => {
    console.log(k + ': ' + byKind[k].length);
  });
}

/* 只打印严重问题详情 */
const SEVERE = ['MISSING_LABEL', 'DUPLICATE_LABEL', 'UNCOMPILED', 'MENU_UNEXPECTED', 'MISSING_START'];
let severeCount = 0;
SEVERE.forEach((k) => {
  if (!byKind[k]) return;
  severeCount += byKind[k].length;
  console.log('\n--- ' + k + ' ---');
  byKind[k].slice(0, 30).forEach((d) => {
    console.log('  ' + d.file + ':' + d.line + '  ' + d.message);
  });
});

/* 抽样展示若干真实 label 的首几条指令，确认编译正确 */
console.log('\n=== 抽样 ===');
/* 注意：scenes/end_te.rpy 里的 label 名是 end1（文件名与 label 名不一致） */
['start', 'scene_1_1', 'scene_3_4', 'end1'].forEach((name) => {
  const lab = program.labels[name];
  if (!lab) { console.log(name + ': 不存在'); return; }
  console.log('\n[' + name + '] ' + lab.ops.length + ' ops  (' + lab.file + ')');
  lab.ops.slice(0, 8).forEach((op, i) => {
    console.log('  #' + i + '  ' + RPYCompiler.describeOp(op));
  });
});

/* 验证 if/menu 展开的跳转目标合法 */
let badTarget = 0;
labelNames.forEach((n) => {
  const ops = program.labels[n].ops;
  ops.forEach((op) => {
    if (op.target !== undefined && op.target !== -1) {
      if (op.target < 0 || op.target > ops.length) badTarget++;
    }
  });
});
console.log('\n非法跳转目标: ' + badTarget);

/* menu 项目标校验 */
let badMenu = 0;
labelNames.forEach((n) => {
  const ops = program.labels[n].ops;
  ops.forEach((op) => {
    if (op.op === 'menu') {
      (op.items || []).forEach((it) => {
        if (it.target < 0 || it.target >= ops.length) badMenu++;
      });
    }
  });
});
console.log('非法 menu 目标: ' + badMenu);

const ok = severeCount === 0 && badTarget === 0 && badMenu === 0;
console.log('\n结果: ' + (ok ? '通过' : '存在问题'));
process.exit(ok ? 0 : 1);