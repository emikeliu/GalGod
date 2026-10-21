init -1 python:
    gui.main_menu_font = "JCYT500W.ttf"

# 按钮本身
style main_menu_button:
    background None                  # 不显示背景
    hover_background None            # hover 也不显示背景
    insensitive_background None      # 不可点击时背景
    xpadding 10
    ypadding 4
    hover_sound None                 # 不加声音也行

# 按钮文字
style main_menu_button_text:
    font gui.main_menu_font
    size 28                          # 字号稍小
    color "#FFFFFF"
    hover_color "#FFDDAA"            # hover 时颜色变化
    outlines [(3, "#00000066", 0, 0)]  # 黑色柔光阴影
    xalign 0.5

style say_dialogue:
    line_leading 10 # 行上方的间距，避免描边显示
    line_spacing 10 # 行与行之间增加 10 像素