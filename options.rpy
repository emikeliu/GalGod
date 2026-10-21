## 此文件包含可以更改以自定义游戏的选项。
##
## 以两个'#'标记开头的行是注释，您不应取消注释它们。以单个'#'标记开头的行是被注
## 释掉的代码，您可能希望在适当的时候取消注释它们。

## TODO: 将这三个顶部值（config.name、build.name 和 config.save_directory）更改
## 为您项目独有的内容！

## 基础 ##########################################################################

## 游戏的人类可读名称。这用于设置默认窗口标题，并显示在界面和错误报告中。
##
## 字符串周围的 _() 将其标记为可翻译。

define config.name = _("GalGod")
define config.steam_appid = 4262610

## 用于可执行文件和已构建发行版中目录的游戏短名称。这必须仅包含 ASCII 字符，并且
## 不得包含空格、冒号或分号。

define build.name = "GalGod"

## 保存目录 ########################################################################
##
## 控制 Ren'Py 将此游戏的保存文件放置在特定于平台的位置。保存文件将放置在：
##
## Windows：%APPDATA\RenPy\<config.save_directory>
##
## Macintosh：$HOME/Library/RenPy/<config.save_directory>
##
## Linux：$HOME/.renpy/<config.save_directory>
##
## 通常不应更改此项，如果更改，应始终是字面字符串，而不是表达式。

## 注意：典型的 save_directory 值看起来像"FreshProject-1671818013"
define config.save_directory = "NoctellaObservatory-GalGod"


## 游戏的版本。

define config.version = "1.0.0"


## 声音和音乐 #######################################################################

## 这三个变量控制默认情况下向玩家显示哪些混音器等内容。将其中一个设置为 False 将
## 隐藏相应的混音器。

define config.has_sound = True
define config.has_music = True
define config.has_voice = True


## 要允许用户在声音或语音频道上播放测试声音，请取消注释下面的一行并使用它来设置
## 要播放的示例声音。

# define config.sample_sound = "sample-sound.ogg"
# define config.sample_voice = "sample-voice.ogg"


## 取消注释以下行以设置玩家在主菜单时将播放的音频文件。此文件将继续播放到游戏
## 中，直到它被停止或播放另一个文件。

# define config.main_menu_music = "main-menu-theme.ogg"


## 转场 ##########################################################################
##
## 这些变量设置在发生某些事件时使用的转场。每个变量都应设置为转场，或 None 表示
## 不应使用转场。

## 进入或退出游戏菜单。

define config.enter_transition = dissolve
define config.exit_transition = dissolve


## 游戏菜单的屏幕之间。

define config.intra_transition = dissolve


## 加载游戏后使用的转场。

define config.after_load_transition = None


## 游戏结束后进入主菜单时使用。

define config.end_game_transition = None

## 窗口管理 ########################################################################
##
## 这控制何时显示对话窗口。如果是"show"，则始终显示。如果是"hide"，则仅在存在对
## 话时显示。如果是"auto"，则窗口在场景语句之前隐藏，并在显示对话后再次显示。
##
## 游戏开始后，可以使用"window show"、"window hide"和"window auto"语句更改此设
## 置。

define config.window = "auto"


## 用于显示和隐藏对话窗口的转场

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


## 首选项默认值 ######################################################################

## 控制默认文本速度。默认值 0 表示无限，而任何其他数字是每秒打出的字符数。

default preferences.text_cps =30

## 默认的自动前进延迟。数字越大，等待时间越长，有效范围为 0 到 30。
default preferences.afm_time = 15

# 语音结束后留一点呼吸感
define config.afm_voice_delay = 0.5

## 图标 ##########################################################################
##
## 显示在任务栏或 dock 上的图标。

define config.window_icon = "gui/window_icon.png"

## 自定义选项 #######################################################################
##
## 我喜欢设置的配置变量。

## 为没有足够项目的网格不崩溃提供便利 https://www.renpy.org/doc/html/
## config.html#var-config.allow_underfull_grids 在现代 Ren'Py 中，这已经是默认设
## 置。
define config.allow_underfull_grids = True

## 各种音量滑块的默认音量百分比 https://www.renpy.org/doc/html/
## preferences.html#audio-channel-defaults
define config.default_music_volume = 0.7
define config.default_sfx_volume = 0.7
define config.default_voice_volume = 1

## 可选；这将音量滑块的行为恢复到 8.1 之前的版本，因此静音游戏会显示所有音量滑块
## 都为 0
# define config.preserve_volume_when_muted = False

## Ren'Py 在开始覆盖第一个自动保存槽之前将保存到的自动保存槽数量
define config.autosave_slots = 6
## 同样的设置，但用于快速保存
define config.quicksave_slots = 6

## 构建配置 ########################################################################
##
## 本节控制 Ren'Py 如何将您的项目转换为发行文件。

init python:

    ## 以下函数采用文件模式。文件模式不区分大小写，并与相对于基目录的路径匹配，
    ## 有或没有前导 /。如果多个模式匹配，则使用第一个。
    ##
    ## 在模式中：
    ##
    ## / 是目录分隔符。
    ##
    ## * 匹配所有字符，除了目录分隔符。
    ##
    ## ** 匹配所有字符，包括目录分隔符。
    ##
    ## 例如，"*.txt" 匹配基目录中的 txt 文件，"game/**.ogg" 匹配 game 目录或其任
    ## 何子目录中的 ogg 文件，"**.psd" 匹配项目中任何位置的 psd 文件。

    ## 将文件分类为 None 以将它们从构建的发行版中排除。

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('**.psd', None)
    build.classify('game/cache/**', None)
    ## 注意：这会排除 markdown 和 txt 文件。如果您将这些格式用于 README 或说明，
    ## 您可能需要删除这些行。
    build.classify('**.txt', None)
    build.classify('**.md', None)
    build.classify("**/generate-rain.py", None)
    build.classify("**/pre-process.py", None)

    ## 要归档文件，请将它们分类为'archive'。

    build.classify("game/**.rpy", "archive")
    build.classify("game/**.rpym", "archive")

    build.classify("game/**.webp", "archive")
    build.classify("game/**.avif", "archive")
    build.classify("game/**.webm", "archive")
    build.classify("game/**.mp4", "archive")
    build.classify("game/**.png", "archive")
    build.classify("game/**.jpg", "archive")
    build.classify("game/**.ttf", "archive")
    build.classify("game/**.otf", "archive")
    build.classify("game/**.mp3", "archive")
    build.classify("game/**.wav", "archive")
    build.classify("game/**.ogg", "archive")
    build.classify("game/**.opus", "archive")
    build.classify("game/**.rpyc", "archive")
    build.classify("game/**.rpymc", "archive")

## 执行应用内购买需要 Google Play 许可密钥。可以在 Google Play 开发者控制台的"盈
## 利">"盈利设置">"许可"下找到。

# define build.google_play_key = "..."


## 与 itch.io 项目关联的用户名和项目名称，用斜杠分隔。

# define build.itch_project = "renpytom/test-project"

# 强制使用现代渲染路径
define config.gl2 = True

# mipmap 会在加载时自动生成多个小版本
define config.mipmap = True

# 最近邻采样（Nearest Neighbor Scaling）
define config.nearest_neighbor = False


init python:
    # 主菜单音量通道
    renpy.music.register_channel(
        "menu_music",
        loop=True
    )

    # 主菜单UI音量专用通道
    renpy.music.register_channel(
        "ui_sfx",
        mixer="ui",      # 自定义 mixer 名，玩家设置界面里不存在这个滑块
        loop=False,
        tight=False
    )
    renpy.music.set_volume(1.0, channel="ui_sfx")

    def play_ui_hover():
        renpy.play("audio/fx/btn_Move.ogg", channel="ui_sfx")

    def play_ui_click():
        renpy.play("audio/fx/btn_Click.ogg", channel="ui_sfx")

    def always_sustain_voice(event, **kwargs):
        if event == "begin":
            # 在底层，voice sustain 语句实际上就是把这个变量设为 True
            store._voice.sustain = True

    # 全局注册
    config.all_character_callbacks.append(always_sustain_voice)
    # 后续直接 stop voice fadeout 1.0  # 1秒淡出停止