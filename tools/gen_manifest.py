#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 Ren'Py 工程目录，生成纯前端加载器所需的静态清单。

用法:
    python3 tools/gen_manifest.py            # 从脚本所在位置推断工程根目录
    python3 tools/gen_manifest.py --root .   # 显式指定工程根目录

输出:
    web/assets/manifest.json   运行时清单（脚本文件 / 资源列表 / 缺失项）
    web/assets/missing.txt     人类可读的缺失资源报告
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# 需要跳过的目录（运行时用不到，且会拖慢扫描）
# ---------------------------------------------------------------------------
SKIP_DIRS = {
    "web",
    "tools",
    "plans",
    "cache",
    "saves",
    "tl",
    "optional files",
    "__pycache__",
    ".git",
    ".vscode",
}

# 资源类型 -> 扩展名
ASSET_EXTS = {
    ".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".bmp", ".svg",
    ".ogg", ".mp3", ".wav", ".opus", ".flac", ".m4a",
    ".webm", ".mp4", ".ogv",
    ".ttf", ".otf", ".woff", ".woff2",
}

SCRIPT_EXTS = {".rpy"}

# 剧本入口顺序（start 所在的 script.rpy 必须最先编译）
SCRIPT_ORDER = [
    "script.rpy",
    "resources.rpy",
    "options.rpy",
    "gui.rpy",
    "styles.rpy",
    "history_screen.rpy",
    "privacy polacy.rpy",
    "config/options.rpy",
    "config/character_config.rpy",
    "config/character_core.rpy",
    "config/performances_config.rpy",
    "effects/raineffect.rpy",
]

# 只作为「全局配置扫描」使用、不进入剧本执行的屏幕文件
SCREEN_PREFIX = "screens/"

# 资源引用提取：抓取 .rpy 里带扩展名的字符串字面量。
# 注意不能要求扩展名后紧跟引号 —— 形如 Image("gui/对话框.png", xalign=0.5) 的参数后面是逗号。
QUOTED_ASSET_RE = re.compile(
    r'"((?:[^"\\\n]|\\.)*?\.(?:png|jpg|jpeg|webp|avif|gif|bmp|svg'
    r'|ogg|mp3|wav|opus|flac|m4a|webm|mp4|ogv|ttf|otf|woff2?))'
    r'(?:"|\s*,|\s*\)|\s*\])',
    re.IGNORECASE,
)

# 语音路径前缀补全规则：剧本写 "cv/linxi/x.ogg"，实际文件在 "audio/cv/linxi/x.ogg"
VOICE_PREFIXES = ("cv/", "cv2/", "cv3/", "bgm/", "fx/")

# Ren'Py 的「动态图像名」占位符：auto "gui/mm_start_%s.png"、Frame("gui/x_[prefix_]y.png")
# 这些不是真实文件，必须从缺失检测里排除，否则报告会被噪声淹没。
DYNAMIC_MARKERS = ("%s", "%d", "[prefix_]", "[prefix]", "*", "**", "{")

# 剧本里用变量拼接出来的路径（如 raineffect 的 RainFiles + "/_rain-long.png"）。
# 这里手工补上它们的真实位置。
PATH_REMAP = {
    "/_rain-long.png": "effects/_rain-long.png",
    "/_rain-medium.png": "effects/_rain-medium.png",
    "/_rain-short.png": "effects/_rain-short.png",
}


def is_asset(name: str) -> bool:
    return os.path.splitext(name)[1].lower() in ASSET_EXTS


def walk(root: str):
    """遍历工程目录，产出 (相对路径, 绝对路径)。"""
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in SKIP_DIRS and not d.startswith(".")
        )
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == ".":
            rel_dir = ""
        for fn in sorted(filenames):
            if fn.startswith("."):
                continue
            rel = os.path.join(rel_dir, fn).replace(os.sep, "/")
            yield rel, os.path.join(dirpath, fn)


def is_dynamic(path: str) -> bool:
    """判断是否为 Ren'Py 的模板/通配路径，这类不是真实文件。"""
    return any(m in path for m in DYNAMIC_MARKERS)


def resolve_candidates(path: str):
    """把剧本里的资源路径转换成可能存在的真实路径（按优先级排序）。"""
    raw = path.strip().replace("\\", "/")
    out = []

    if raw in PATH_REMAP:
        out.append(PATH_REMAP[raw])

    path = raw.lstrip("/")
    out.append(path)

    # 语音/音频前缀补全：cv/... -> audio/cv/...
    for p in VOICE_PREFIXES:
        if path.startswith(p):
            out.append("audio/" + path)
            break

    # effects/ 相对补齐（雨效图片）
    if path.startswith("_rain"):
        out.append("effects/" + path)

    # Ren'Py 允许省略扩展名 —— 精确匹配失败时由运行时兜底，这里不盲猜
    return out


def script_sort_key(rel: str):
    if rel in SCRIPT_ORDER:
        return (0, SCRIPT_ORDER.index(rel), rel)
    return (1, 0, rel)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="Ren'Py 工程根目录")
    ap.add_argument("--out", default=None, help="输出目录，默认 <root>/web/assets")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(args.root or os.path.dirname(here))
    out_dir = os.path.abspath(args.out or os.path.join(root, "web", "assets"))
    os.makedirs(out_dir, exist_ok=True)

    scripts, assets = [], []
    for rel, abspath in walk(root):
        if rel.endswith(".rpyc") or rel.endswith(".rpymc"):
            continue
        if rel.endswith(".rpy"):
            scripts.append(rel)
        elif is_asset(rel):
            assets.append(rel)

    scripts.sort(key=script_sort_key)
    asset_set = set(assets)
    asset_set_lower = {a.lower(): a for a in assets}

    asset_dirs = sorted({a.rsplit("/", 1)[0] for a in assets if "/" in a})

    # ------------------------------------------------------------------
    # 缺失资源检测
    # ------------------------------------------------------------------
    referenced = {}   # 引用路径 -> 首次出现位置
    missing = {}      # 引用路径 -> {"file":..., "line":..., "candidates":[...]}

    rpy_files = [s for s in scripts]
    for rel in rpy_files:
        abspath = os.path.join(root, rel)
        try:
            with open(abspath, "r", encoding="utf-8-sig", errors="replace") as f:
                lines = f.readlines()
        except OSError as e:
            print("warn: cannot read %s (%s)" % (rel, e), file=sys.stderr)
            continue
        for lineno, line in enumerate(lines, 1):
            # 跳过整行注释，避免把注释里的示例路径算进缺失报告
            stripped = line.lstrip()
            if stripped.startswith("#"):
                continue
            for m in QUOTED_ASSET_RE.finditer(line):
                p = m.group(1).strip()
                if not p or ".." in p:
                    continue
                # 跳过 Ren'Py 的动态模板名与打包通配符，它们不是真实文件
                if is_dynamic(p):
                    continue
                referenced.setdefault(p, (rel, lineno))
                cands = resolve_candidates(p)
                if any(c in asset_set or c.lower() in asset_set_lower for c in cands):
                    continue
                missing[p] = {
                    "file": rel,
                    "line": lineno,
                    "candidates": cands,
                    # 同目录下「只差扩展名」的候选，方便人工判断是否可回退
                    "same_stem": sorted(
                        a for a in assets
                        if os.path.splitext(a)[0] == os.path.splitext(cands[-1])[0]
                    ),
                }

    # ------------------------------------------------------------------
    # 输出
    # ------------------------------------------------------------------
    manifest = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "game": {
            "name": "GalGod",
            "version": "1.0.0",
            "screen_width": 1920,
            "screen_height": 1080,
        },
        "script_files": scripts,
        "screen_files": [s for s in scripts if s.startswith(SCREEN_PREFIX)],
        "assets": assets,
        "asset_dirs": asset_dirs,
        "missing": sorted(missing.keys()),
        "missing_detail": missing,
        "stats": {
            "scripts": len(scripts),
            "assets": len(assets),
            "referenced": len(referenced),
            "missing": len(missing),
        },
    }

    manifest_path = os.path.join(out_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)

    missing_path = os.path.join(out_dir, "missing.txt")
    with open(missing_path, "w", encoding="utf-8") as f:
        f.write("# 缺失资源报告  %s\n\n" % manifest["generated_at"])
        f.write("# 共 %d 个被引用但未找到的文件\n\n" % len(missing))
        for p in sorted(missing):
            d = missing[p]
            f.write("%s\n" % p)
            f.write("    首次引用: %s:%d\n" % (d["file"], d["line"]))
            f.write("    尝试路径: %s\n" % ", ".join(d["candidates"]))
            if d.get("same_stem"):
                f.write("    同名候选: %s\n" % ", ".join(d["same_stem"]))
            f.write("\n")

    print("root      : %s" % root)
    print("scripts   : %d" % len(scripts))
    print("assets    : %d" % len(assets))
    print("referenced: %d" % len(referenced))
    print("missing   : %d  -> %s" % (len(missing), missing_path))
    print("manifest  -> %s" % manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())