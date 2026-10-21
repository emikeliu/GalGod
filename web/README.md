# GalGod · 纯前端 Ren'Py 加载器

在浏览器里直接读取工程目录下的 `.rpy` 源码与素材，复刻 Ren'Py 的运行效果。
**零依赖、零构建、不引入任何第三方引擎。**

---

## 快速开始

```bash
# 1. 在工程根目录（archive/）启动静态服务
cd /run/media/mikeliu/Linux/GalGod-1.0.0-win/game/archive
python3 -m http.server 8080

# 2. 浏览器打开
#    http://127.0.0.1:8080/web/
```

> **必须通过 HTTP 打开。** `file://` 下浏览器会拦截 `fetch`，无法读取 `.rpy`。

改了 `.rpy` 之后需要重新生成清单：

```bash
python3 tools/gen_manifest.py
```

---

## 操作说明

| 操作 | 功能 |
|---|---|
| 左键 / 空格 / 回车 | 推进对话；打字中点击立即补全 |
| 滚轮上滑 | 回滚到上一句 |
| 滚轮下滑 | 打开历史记录 |
| Esc | 打开游戏菜单 |
| Ctrl（按住） | 快进 |
| Tab | 切换快进 |
| V | 切换自动播放 |
| H | 隐藏对话框 |
| F1 | 操作说明 |
| **F9** 或 **`** | **调试面板**（诊断 / 章节跳转 / 变量 / 指令追踪） |

### 调试面板（F9）

四个页签，不占用游戏 UI，只在需要时打开：

| 页签 | 内容 |
|---|---|
| 诊断 | 解析 / 资源 / 运行时问题，按类型分组，带文件:行号 |
| 章节跳转 | 对应 `screens/dev_jump_menu.rpy`，任意时刻直接跳 label（**不需要先点开始游戏**） |
| 变量 | store 变量、persistent 关键项、成就、当前舞台状态 |
| 指令追踪 | 当前 label 的指令流，高亮当前 PC，自动滚到执行位置 |

底部常驻显示当前 `label #pc` 与运行状态（运行中/等待/自动/快进/回滚点数）。

### URL 参数

| 参数 | 作用 |
|---|---|
| `?strict=1` | 启动后自动展开调试面板 |
| `?label=scene_2_4` | 启动时提示该章节，按 F9 可直接跳转 |
| `?label=scene_2_4&play=1` | 跳过主菜单，**直接开始**该章节 |

例：`http://127.0.0.1:8080/web/?label=scene_3_4&play=1`

---

## 目录结构

```
web/
  index.html            入口
  README.md             本文件
  css/
    stage.css           1920×1080 舞台、图层、加载遮罩、诊断面板
    textbox.css         对话框 / 名字框 / 居中文本 / 选项
    menu.css            主菜单 / 存读档 / 设置 / 画廊 / 作者的话
    effects.css         转场、震动、滤镜
  js/
    boot.js             应用主控：加载 → 编译 → 组装 → 启动
    manifest.js         清单与 .rpy 拉取（统一加 ../ 根前缀）
    fs-utils.js         小工具：Toast / 确认框 / 章节名
    rpy/
      strings.js        BOM、转义、文本标签 → HTML、去 Python 注释
      lexer.js          缩进建树 + 跨行括号/三引号合并
      parser.js         语句识别 → AST
      expr.js           安全表达式求值（无 eval / new Function）
      compiler.js       AST → 线性指令流（if/menu 展开、camera ATL）
    engine/
      state.js          变量表、舞台快照、历史、持久化
      actors.js         CHARACTERS_CONFIG → Actor，立绘变换
      images.js         image 定义解析、bg_fit / bg_focus、资源回退
      stage.js          图层、scene/show/hide、雨、滤镜、镜头
      transitions.js    dissolve / fade / flash / vpunch / pixellate
      audio.js          music / sound / voice 三通道
      save.js           3 页 × 6 槽 + auto / quick
      movie.js          ED 视频
      vm.js             帧栈、yield 挂起、回滚、存读档
    ui/
      say.js            打字机对白
      centered_text.js  centered 与 centered_left_text
      choice.js         选项菜单
      history.js        历史记录 + 回滚跳转
      main_menu.js      主菜单
      save_load.js      存读档界面
      config.js         系统设置
      gallery.js        附加鉴赏
      about.js          作者的话
      diag.js           F9 诊断面板
  assets/
    manifest.json       生成物：脚本清单 + 资源索引 + 缺失项
    overrides.json      缺失资源回退表
    missing.txt         缺失资源人类可读报告
```

---

## 工具

| 命令 | 作用 |
|---|---|
| `python3 tools/gen_manifest.py` | 扫描工程，生成 `manifest.json` 与 `missing.txt` |
| `python3 tools/validate_assets.py` | 校验清单与回退表一致性、检查 image 引用 |
| `node tools/test_compile.js` | 无头跑 lex → parse → compile，输出诊断统计 |
| `node tools/test_vm.js <label>` | 无头驱动 VM 执行指定章节（桩替代 DOM） |
| `sh tools/test_all.sh` | **全量回归**：资源 + 编译 + 19 个章节冒烟 |

---

## 已支持语法

```
label / call / return / jump
say（旁白与角色）、centered
scene / show / hide（含 at、with、layer、screen）
play / stop / queue / voice
pause（含 hard=True）、$ renpy.pause(...)
with dissolve / Dissolve(t) / fade / flash / vpunch / hpunch / pixellate
window hide / show / auto
$ actor.show(...) / act(...) / hide() / reset_position()
$ 变量赋值与 += / -=
if / elif / else、menu（含题面形式）
camera master at FILTER、camera:（ATL 镜头推拉）
show layer master at memory_filter / gray_filter / reset_filter
define / default / image / transform（注册到运行时）
```

未实现的语句一律**静默跳过并记入诊断**，不会中断播放。

---

## 实现要点

### 立绘变换
`yoffset` 是 1080 坐标系下的像素偏移，不随 `zoom` 缩放。顺序固定为：
**定位 → y_offset → x_offset → scale(origin: bottom center)**。
默认取 `global_actor_settings = {zoom: 0.6, y_offset: 1250}`，角色级 `style` 覆盖。

### 舞台缩放
固定 1920×1080 逻辑尺寸，`transform: scale(min(w/1920, h/1080))`，居中留黑边。
所有内部坐标都按 Ren'Py 的 1080p 坐标系书写。

### 文字速度
`preferences.text_cps` 默认 30，`centered_left_text` 固定 25。
`{size=}` `{space=}` `{color=}` `{b}` `{i}` 等标签转为 HTML；未知标签静默丢弃。

### 语音路径
剧本写 `voice "cv/linxi/x.ogg"`，实际文件在 `audio/cv/linxi/x.ogg`。
`images.resolve()` 会自动补 `audio/` 前缀。

### 资源路径
页面在 `/web/`，素材在上一级，所以 JS 统一用 `../` 前缀（`Images.ROOT`），
CSS 用 `../../`。中文文件名逐段 `encodeURIComponent`。

---

## 已知取舍

1. **系统设置页**：原作是十余张图片逐层叠加的 UI，这里做「功能等价」——
   同样的字段（音乐/音效/语音/角色音量、文本速度、自动速度、对话框不透明度、
   快进速度、显示模式）以图片背景 + DOM 控件呈现，不做逐像素还原。
2. **存档不存截图**：槽位显示「对白摘要 + 时间」，与原作 UI 的信息量一致。
   因此 `config.thumbnail_*` 相关逻辑未实现。
3. **`.rpyc` 不反编译**：只读 `.rpy`，这也是「读取静态资源」的前提。
4. **Steam 成就**：`achievement.grant/sync` 落为 localStorage 记录，
   用于画廊解锁与「作者的话」的解锁判定。
5. **可选的 Ren'Py 高级特性**（`screen language` 的自定义布局、`layeredimage`、
   `ATL` 的复杂循环）不执行，涉及处仅作静态背景/空操作处理。

---

## 缺失资源

`web/assets/missing.txt` 会列出全部「被引用但找不到」的文件。当前只有 6 项：

| 资源 | 处理 |
|---|---|
| `audio/fx/FX_上课铃.mp3` | 实际是 `.ogg`，回退表已映射 |
| `cv/linxi/linxi_01220/01230/01240.ogg` | 原作刻意打错的编号（配合省略号演出），静默跳过 |
| `gui/history_jump_{hover,idle}.png` | 回退到同目录 `*_background.png` |

新增缺失时，在 `web/assets/overrides.json` 中登记即可，`validate_assets.py` 会校验一致性。

---

## 排查

1. **打开是黑屏 / 一直卡在「正在读取资源清单」**
   → 确认用的是 `http://` 而不是 `file://`；确认 `web/assets/manifest.json` 存在。

2. **大量 404 指向 `/web/screens/xxx.rpy`**
   → `manifest.js` 的 `ROOT` 前缀没生效，检查是否用了旧缓存（硬刷新）。

3. **某个表情/背景不显示**
   → 按 F9 看诊断面板，`MISSING_ASSET` / `MISSING_EXPRESSION` 会指出具体路径。

4. **播放到某句话卡住**
   → F9 看 `UNKNOWN_OP` / `RUNTIME_ERROR`，通常是新语法未覆盖。