## 输入屏幕 ################################################################
##
## 此屏幕用于显示renpy.input。prompt参数用于传递文本提示。
##
## 此屏幕必须创建一个id为"input"的输入可显示对象以接受各种输入参数。
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:
        # 这使背景与ADV对话框相同

        vbox:
            xanchor 0.0 ypos 20 spacing 10
            text prompt style "input_prompt"
            input id "input"

style input_prompt:
    xalign 0.0

style input:
    xalign 0.0
    xmaximum 1116


