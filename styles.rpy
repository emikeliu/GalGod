################################################################################
## Initialization
################################################################################

## init offset 语句使此文件中的初始化语句在任何其他文件中的 init 语句之前运行
init offset = -2

## 调用 gui.init 将样式重置为合理的默认值，并设置游戏的宽度和高度
init python:
    gui.init(1920, 1080)

define config.check_conflicting_properties = True

################################################################################
## GUI 配置变量
################################################################################
## 一些可选的 gui 值已被保留，以便更容易地针对无障碍目的进行调整，例如允许玩家通过重建 gui 来更改默认文本字体或大小。
## 如果您需要调整它们，可以添加更多，或者在直接使用它们的任何实例中查找并替换为它们的值。

# 对话和选择菜单的文本字体
define gui.text_font = gui.preference("font", "JCYT500W.ttf")
# 按钮的文本字体
define gui.interface_text_font = gui.preference("interface_font", "JCYT500W.ttf")
# 角色名称的字体
define gui.name_text_font = gui.preference("name_font", "JCYT500W.ttf")

# define gui.text_font = "JCYT500W.ttf"
# define gui.interface_text_font = "JCYT500W.ttf"
# define gui.name_text_font = "JCYT500W.ttf"

# 游戏内文本的默认大小
define gui.text_size = gui.preference("size", 33)
# 角色名称的大小
define gui.name_text_size = gui.preference("name_size", 45)

## 本地化 ################################################################

## 这控制在哪里允许换行。默认值适用于大多数语言。可用值列表可以在以下位置找到
## https://www.renpy.org/doc/html/style_properties.html#style-property-language

define gui.language = "unicode"

define gui.text_outlines =  [(2, "#000000", 0, 0)]


################################################################################
## Style Initialization
################################################################################

init offset = -1

################################################################################
## Styles
################################################################################

style default:
    font gui.text_font
    size gui.text_size
    language gui.language

style input:
    adjust_spacing False

style hyperlink_text:
    hover_underline True
    color "#fff"

style gui_text:
    color '#ffffff'
    size gui.text_size
    font gui.interface_text_font
    outlines [(3, "#000000", 0, 0)]

style button:
    xysize (None, None)
    padding (0, 0)

style button_text:
    is gui_text
    yalign 0.5
    xalign 0.0
    ## 文本按钮在既未被选中也未被悬停时使用的颜色
    idle_color '#888888'
    ## 用于被悬停的按钮和条的颜色
    hover_color '#ff8335'
    ## 文本按钮在被选中但未获得焦点时使用的颜色。如果按钮是当前屏幕或首选项值，则该按钮被选中。
    selected_color '#ffffff'
    ## 文本按钮在无法被选中时使用的颜色
    insensitive_color '#8888887f'

style label_text:
    is gui_text
    size 36
    color '#fff'


style bar:
    ysize 38
    left_bar Frame("gui/bar/left.png", 6, 6, 6, 6, tile=False)
    right_bar Frame("gui/bar/right.png", 6, 6, 6, 6, tile=False)

style vbar:
    xsize 38
    top_bar Frame("gui/bar/top.png", 6, 6, 6, 6, tile=False)
    bottom_bar Frame("gui/bar/bottom.png", 6, 6, 6, 6, tile=False)

style scrollbar:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", 6, 6, 6, 6, tile=False)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", 6, 6, 6, 6, tile=False)
    unscrollable 'hide'

style vscrollbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", 6, 6, 6, 6, tile=False)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", 6, 6, 6, 6, tile=False)
    unscrollable 'hide'

style slider:
    ysize 38
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", 6, 6, 6, 6, tile=False)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize 38
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", 6, 6, 6, 6, tile=False)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding (6, 6, 6, 6)
    background Frame("gui/frame.png", 6, 6, 6, 6, tile=False)
