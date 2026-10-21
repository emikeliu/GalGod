## 自动指示器屏幕 #######################################################
##
## 此屏幕用于指示自动前进模式正在进行中。
## 由我创建，Feniks。如果你不需要自动前进指示器屏幕，可以删除整个文件。
##

init python:
    def auto_indicator():
        """
        一个函数，当被调用时，判断是否应该在屏幕上显示自动指示器。
        """

        # 自动模式已开启
        if preferences.afm_enable and not renpy.get_screen('auto_indicator'):
            renpy.show_screen('auto_indicator')
        # 自动模式已关闭
        elif not preferences.afm_enable and renpy.get_screen('auto_indicator'):
            renpy.hide_screen('auto_indicator')

        return

    # 这会将自动指示器添加到覆盖函数列表中
    # 以便它可以自动显示自动指示器。
    if auto_indicator not in config.overlay_functions:
        config.overlay_functions.append(auto_indicator)

screen auto_indicator():

    zorder 100
    style_prefix "auto"

    frame:
        has hbox

        # 这里只保留视觉提示，不让自朗读在每次自动前进时重复播报这段固定文案。
        text _("Auto-Forward") alt ""

        text "▷" at auto_blink(1.0) style "skip_triangle" alt ""

## 此变换用于让箭头依次闪烁。
transform auto_blink(cycle):
    alpha 0.0
    linear 0.5 alpha 1.0
    pause 0.2
    linear 0.5 alpha 0.0
    pause (cycle - .4)
    repeat

style auto_hbox:
    spacing 9

style auto_frame:
    is empty
    ypos 15
    background Frame("#0008", 24, 8, 75, 8, tile=False)
    padding (24, 8, 75, 8)

style auto_text:
    size 24

style auto_triangle:
    is auto_text
    ## 我们必须使用包含 BLACK RIGHT-POINTING SMALL TRIANGLE
    ## 字形的字体。
    font "JCYT500W.ttf"
