## 选项屏幕 ###############################################################
##
## 此屏幕用于显示由menu语句呈现的游戏内选项。唯一的参数items是一个对象列表，
## 每个对象都有caption和action字段。
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5
    spacing 33

style choice_button:
    is default
    xysize (699, 107)
    # 确保 background 的 150 是正确的边角数值
    background Frame("gui/choice_[prefix_]background.png", 150, 25, 150, 25, tile=False)
    padding (40, 5, 40, 5) # 增加左右间距，防止文字撞边

style choice_button_text:
    is default
    xalign 0.5 yalign 0.5
    text_align 0.5
    idle_color "#ffffff"
    hover_color "#ffffff"
    
    outlines [(2, "#000", 0, 0)] 