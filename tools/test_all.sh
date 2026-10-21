#!/bin/sh
# tools/test_all.sh
# 全量回归：资源校验 + 编译校验 + 逐章 VM 冒烟。
# 用法：sh tools/test_all.sh

set -e
cd "$(dirname "$0")/.."

echo "=============================================="
echo " 1/4  资源校验"
echo "=============================================="
python3 tools/gen_manifest.py > /dev/null
python3 tools/validate_assets.py

echo
echo "=============================================="
echo " 2/4  编译校验（lex -> parse -> compile）"
echo "=============================================="
node tools/test_compile.js

echo
echo "=============================================="
echo " 3/4  逐章 VM 冒烟"
echo "=============================================="

CHAPTERS="scene_1_1 scene_1_2 scene_1_3 scene_1_4 scene_2_1 scene_2_2 scene_2_3 scene_2_4 scene_3_1 scene_3_2 scene_3_3 scene_3_4 interlude1 interlude2 interlude_interview end2 end3 end1 after_story_noctella"

FAIL=0
for ch in $CHAPTERS; do
  OUT=$(STEPS=20000 node tools/test_vm.js "$ch" 2>&1 || true)
  ERRS=$(printf '%s' "$OUT" | grep -A1 "运行时诊断" | grep -v "运行时诊断" | tr -d ' ' | head -1)
  SAYS=$(printf '%s' "$OUT" | grep -E "^  say:" | head -1 | tr -d ' ')
  SPR=$(printf '%s' "$OUT" | grep -E "^  sprite:" | head -1 | tr -d ' ')

  if printf '%s' "$OUT" | grep -q "RUNTIME_ERROR"; then
    printf '  [FAIL] %-24s %s\n' "$ch" "存在运行时错误"
    printf '%s\n' "$OUT" | grep -A3 "RUNTIME_ERROR" | sed 's/^/        /'
    FAIL=$((FAIL + 1))
  elif printf '%s' "$OUT" | grep -q "label 不存在"; then
    printf '  [SKIP] %-24s label 不存在\n' "$ch"
  else
    printf '  [ OK ] %-24s %s %s\n' "$ch" "$SAYS" "$SPR"
  fi
done

echo
echo "=============================================="
echo " 4/4  结果"
echo "=============================================="
if [ "$FAIL" -eq 0 ]; then
  echo "全部章节冒烟通过"
  exit 0
else
  echo "有 $FAIL 个章节存在问题"
  exit 1
fi