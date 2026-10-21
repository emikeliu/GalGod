## 游戏菜单屏幕 ############################################################
##
## 这布局了游戏菜单屏幕的基本通用结构。它通过屏幕标题调用，
## 并显示标题和导航。
##
## 此屏幕不再包含背景，也不再嵌入其内容。它旨在易于从任何给定的菜单屏幕中移除，
## 因此你需要自己完成一些繁重的工作来设置菜单屏幕内容的容器。
##

screen game_menu(title):

    style_prefix "game_menu"

    vbox:
        xpos 60 yalign 0.5
        spacing 6

        #if main_menu:

            #textbutton _("开始游戏") action Start()

        #else:

            #textbutton _("历史记录") action ShowMenu("history_screen")

            #textbutton _("保存") action ShowMenu("save")

        #textbutton _("读取") action ShowMenu("load")

        #textbutton _("配置") action ShowMenu("my_settings_ui")

        #if _in_replay:

            # textbutton _("End Replay") action EndReplay(confirm=True)
            #textbutton _("结束回放") action EndReplay(confirm=True)

        #elif not main_menu:

            #textbutton _("主菜单") action MainMenu()

        #textbutton _("关于本作") action ShowMenu("about")

        # if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## 帮助对移动设备来说不是必需的或相关的。
            # textbutton _("Help") action ShowMenu("help")

        #if renpy.variant("pc"):

            ## 退出按钮在iOS上被禁止，在Android和Web上不需要。
            #textbutton _("退出") action Quit(confirm=not main_menu)

    #textbutton _("返回"):
        #style "return_button"
        #action Return()

    ## 如果你不想将屏幕标题文本显示为标签，请删除此行
    ## （例如，如果它已经嵌入到背景图像中。）
    #label title

    #if main_menu:
        #key "game_menu" action ShowMenu("main_menu")

style return_button:
    xpos 60
    yalign 1.0
    yoffset -45

style game_menu_viewport:
    xsize config.screen_width-420
    ysize config.screen_height-200
    align (0.5, 0.5)

style game_menu_side:
    yfill True
    align (1.0, 0.5)

style game_menu_vscrollbar:
    unscrollable "hide"

style game_menu_label:
    padding (10, 10)
style game_menu_label_text:
    size 45
