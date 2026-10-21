## Say屏幕 ##################################################################
##
## say屏幕用于向玩家显示对话。它接受两个参数，who和what，
## 分别是说话角色的名字和要显示的文本。（如果没有给出名字，who参数可以是None。）
##
## 此屏幕必须创建一个id为"what"的文本可显示对象，因为Ren'Py使用它来管理文本显示。
## 它还可以创建id为"who"和id为"window"的可显示对象来应用样式属性。
##
## https://www.renpy.org/doc/html/screen_special.html#say
default script_box_alpha = 1.0

screen say(who, what):
    style_prefix "say"

    window:
        id "window"
        background Transform(Image("gui/对话框.png", xalign=0.5, yalign=1.0),alpha=persistent.dialogue_box_alpha*script_box_alpha)
        

        

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"
                

        text what id "what"
            
        
    key "mousedown_4" action ShowMenu("history")

    # 如果你想保留原来的“滚轮向下继续对话”，可以加上这句（可选）
    key "mousedown_5" action Return() 

    ## 如果有侧边图像，将其显示在文本前面。
    add SideImage() xalign 0.0 yalign 1.0


## 使namebox可通过Character对象进行样式设置。
init python:
    config.character_id_prefixes.append('namebox')

# 对话窗口的样式
style window:
    xalign 0.5
    yalign 1.0
    xysize (1231, 277)
    padding (40, 10, 40, 40)
    background Image("gui/对话框.png", xalign=0.5, yalign=1.0)
    

# 对话的样式
style say_dialogue:
    adjust_spacing False
    ypos 70
    color "#f8f8f8"
    outlines [
        (2, "#333236", 0, 0),
    ]

# 旁白所说对话的样式
style say_thought:
    is say_dialogue

# 包含说话者名字的框的样式
style namebox:
    xpos -70
    ypos -20
    xysize (320, 77)
    background Frame("gui/姓名框.png", 5, 5, 5, 5, tile=False, xalign=0.0)
    padding (0, 5, 5, 5)

# 说话者名字文本的样式
style say_label:
    color '#ffffff'
    xalign 0.0
    yalign -0.2
    xpos 65
    size gui.name_text_size
    font gui.name_text_font
    outlines [ (2, "#333236", 0, 0), (0, "#3d3d3d", 0, 2) ]


## 快捷菜单屏幕 ###########################################################
##
## 快捷菜单在游戏中显示，以便轻松访问游戏外菜单。

screen quick_menu():

    ## 确保此屏幕显示在其他屏幕之上。
    #zorder 100

    if quick_menu and config.developer:

        hbox:
            style_prefix "quick"

            #textbutton _("Save") action ShowMenu('save')
            #textbutton _("Load") action ShowMenu('load')
            textbutton _("Back") action Rollback()
            #textbutton _("History") action ShowMenu('history')
            #textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            #textbutton _("Auto") action Preference("auto-forward", "toggle")
            #textbutton _("Config") action ShowMenu('preferences')


## 此代码确保quick_menu屏幕在游戏中显示，只要玩家没有明确隐藏界面。
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_hbox:
    xalign 0.5
    # yalign 1.0 yoffset -8
    yalign 0 yoffset 8
    spacing 8

style quick_button:
    background None
    hover_background None
    selected_background None
    focus_mask None
    padding (15, 6, 15, 0)

style quick_button_text:
    size 21
    idle_color "#000"
    hover_color "#ff97f6"
    selected_color "#ff97f6"

    outlines []          # ← 明确清空描边
    drop_shadow None     # ← 防止暗影

## NVL屏幕 ##################################################################
##
## 此屏幕用于NVL模式对话和菜单。
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox
        spacing 15

        key "mousedown_4" action ShowMenu("history")
        #key "mousedown_5" action Return()
        #key "mousedown_5" action If(GetFocusRect("history_text"), true=Return(), false=NullAction())
        use nvl_dialogue(dialogue)

        ## 如果提供了菜单，则显示菜单。如果config.narrator_menu设置为True，
        ## 菜单可能显示不正确。
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit True

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## 这控制一次可以显示的NVL模式条目的最大数量。
define config.nvl_list_length = 7

# NVL"文本框"的样式
style nvl_window:
    is default
    xfill True yfill True
    background "gui/nvl.png"
    padding (0, 150, 0, 150)

# 说话者名字文本的样式
style nvl_label:
    is say_label
    xpos 645 xanchor 1.0
    ypos 0 yanchor 0.0
    xsize 225
    min_width 225
    textalign 1.0

# NVL中对话的样式
style nvl_dialogue:
    is say_dialogue
    font "SourceHanSansCN-Medium.otf"
    xoffset -120
    xpos 675
    ypos 12
    xsize 885
    min_width 885
    outlines [
        (0, "#333236", 0, 0),
    ]

# NVL中旁白所说对话的样式
style nvl_thought:
    is nvl_dialogue

style nvl_button:
    xpos 675
    xanchor 0.0


## 气泡屏幕 ###############################################################
##
## 气泡屏幕用于在使用对话气泡时向玩家显示对话。气泡屏幕接受与say屏幕相同的参数，
## 必须创建一个id为"what"的可显示对象，并且可以创建id为"namebox"、"who"和"window"的可显示对象。
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window:
    is empty
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    is empty
    xalign 0.5

style bubble_who:
    is default
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    is default
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}
