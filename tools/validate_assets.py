#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校验 manifest.json 与 overrides.json 的一致性，并交叉检查剧本里 image 语句
引用的图片是否真实存在（gen_manifest 只按扩展名扫描字符串，这里补充
"image 名 -> 文件" 的语义检查）。

用法:
    python3 tools/validate_assets.py
退出码:
    0  无阻塞问题
    1  存在未在 overrides 中登记的缺失资源
"""

from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "web", "assets")

# image <name...> = <expr>   或   image <name...>:
IMAGE_DEF_RE = re.compile(r"^\s*image\s+([^\s=:]+(?:\s+[^\s=:]+)*)\s*[=:]")
# 表达式里出现的字符串字面量
STR_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    manifest = load_json(os.path.join(WEB, "manifest.json"))
    overrides = load_json(os.path.join(WEB, "overrides.json"), {}) or {}
    if manifest is None:
        print("ERROR: web/assets/manifest.json 不存在，请先运行 tools/gen_manifest.py")
        return 1

    assets = set(manifest["assets"])
    asset_lower = {a.lower(): a for a in assets}

    known_missing = set(manifest.get("missing", []))
    declared = set()
    for section in ("image", "audio"):
        declared |= set((overrides.get(section) or {}).keys())

    problems = []

    # 1) manifest 报缺失，但 overrides 未登记
    for m in sorted(known_missing - declared):
        problems.append(("UNDECLARED_MISSING", m, "manifest 缺失但 overrides.json 未登记"))

    # 2) overrides 指向的替代文件不存在
    for section in ("image", "audio"):
        for k, v in (overrides.get(section) or {}).items():
            if v is None:
                continue
            if v not in assets and v.lower() not in asset_lower:
                problems.append(("BAD_OVERRIDE", k, "替代文件不存在: %s" % v))

    # 3) overrides 登记了其实存在的文件（冗余）
    for k in declared:
        if k not in known_missing and (k in assets or k.lower() in asset_lower):
            problems.append(("REDUNDANT_OVERRIDE", k, "文件其实存在，回退表可以删除该条"))

    # 4) 语义检查：image 定义引用的图片
    image_defs = {}
    for rel in manifest["script_files"]:
        path = os.path.join(ROOT, rel)
        try:
            with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
                lines = f.readlines()
        except OSError:
            continue
        for lineno, line in enumerate(lines, 1):
            if line.lstrip().startswith("#"):
                continue
            m = IMAGE_DEF_RE.match(line)
            if not m:
                continue
            name = " ".join(m.group(1).split())
            # 只处理单行定义（= 形式）
            if "=" not in line:
                continue
            for s in STR_RE.findall(line.split("=", 1)[1]):
                if not re.search(r"\.(png|jpe?g|webp|avif|gif|bmp|svg)$", s, re.I):
                    continue
                image_defs.setdefault(name, []).append((rel, lineno, s))

    for name, refs in sorted(image_defs.items()):
        for rel, lineno, s in refs:
            if s in assets or s.lower() in asset_lower:
                continue
            ov = (overrides.get("image") or {}).get(s, "__none__")
            if ov == "__none__":
                problems.append(
                    ("IMAGE_MISSING", s, "image '%s' (%s:%d) 引用的文件不存在" % (name, rel, lineno))
                )

    # ---------------- 输出 ----------------
    if not problems:
        print("OK: 资源校验通过（%d 个资源，%d 条回退）" % (len(assets), len(declared)))
        return 0

    print("发现 %d 个问题:\n" % len(problems))
    fatal = 0
    for kind, path, msg in problems:
        print("[%s] %s\n    %s" % (kind, path, msg))
        if kind in ("UNDECLARED_MISSING", "BAD_OVERRIDE", "IMAGE_MISSING"):
            fatal += 1
    print("\n其中阻塞级问题: %d" % fatal)
    return 1 if fatal else 0


if __name__ == "__main__":
    raise SystemExit(main())