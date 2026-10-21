## 确认屏幕 ##############################################################
##
## 当Ren'Py想要向玩家询问是或否的问题时，会调用确认屏幕。
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action=None):

    ## 确保在显示此屏幕时其他屏幕不会获得输入。
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/黑底.png" # 你可以用自己的覆盖图像替换它

    frame:
        has vbox

        label _(message) style "confirm_prompt"

        hbox:

            imagebutton  idle "gui/YES_idle.png" hover "gui/YES_hover.png" action yes_action alt _("确认")
            # 修改后你可以只显示一个确认提示
            if no_action is not None:
                imagebutton  idle "gui/NO_idle.png" hover "gui/NO_hover.png" action no_action alt _("取消")

    ## 右键单击和Escape键回答"否"。
    if no_action is not None:
        key "game_menu" action no_action
    else:
        key "game_menu" action yes_action

style confirm_frame:
    background Frame("gui/提示框.png", 60, 60, 60, 60, tile=False)
    padding (60, 60, 60, 60)
    xalign 0.5
    yalign 0.5

style confirm_vbox:
    align (0.5, 0.5)
    spacing 45

style confirm_prompt:
    xalign 0.5

style confirm_prompt_text:
    textalign 0.5
    align (0.5, 0.5)
    layout "subtitle"

style confirm_hbox:
    xalign 0.5
    spacing 150

style confirm_button:
    xalign 0.5

style confirm_button_text:
    textalign 0.5


## 跳过指示器屏幕 #######################################################
##
## skip_indicator屏幕用于显示正在进行跳过。
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:
        has hbox

        text _("Skipping")

        text "▷" at delayed_blink(0.0, 1.0) style "skip_triangle"
        text "▷" at delayed_blink(0.2, 1.0) style "skip_triangle"
        text "▷" at delayed_blink(0.4, 1.0) style "skip_triangle"


## 此变换用于使箭头逐个闪烁。
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat

style skip_hbox:
    spacing 9

style skip_frame:
    is empty
    ypos 15
    background Frame("gui/skip.png", 24, 8, 75, 8, tile=False)
    padding (24, 8, 75, 8)

style skip_text:
    size 24

style skip_triangle:
    is skip_text
    ## 我们必须使用包含"向右黑色小三角形"字形的字体。
    font "JCYT500W.ttf"

## 通知屏幕 ###############################################################
##
## notify屏幕用于向玩家显示消息。（例如，当游戏快速保存或截屏时。）
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen
screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame:
    is empty
    ypos 68

    background Frame("gui/notify.png", 24, 8, 60, 8, tile=False)
    padding (24, 8, 60, 8)

style notify_text:
    size 24



