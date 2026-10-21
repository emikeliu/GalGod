## 主菜单屏幕 ############################################################
##
## 在Ren'Py启动时用于显示主菜单。
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

## 如果你喜欢，可以用你的背景图像替换它
image main_menu_background = im.Scale(
    "images/cg/main_screen.avif",
    config.screen_width,
    config.screen_height
)


transform hover_move_down:
    on idle:
        yoffset 0
        xoffset 0          # 平时位置不变
    # on hover:
        # yoffset 20         # 悬停时向下偏移 20 像素 (数字越大越往下)
        # xoffset -8       # 如果想往右移，可以加这行

screen main_menu():
    on "show" action [
        Function(renpy.music.set_volume, 0.9, channel="menu_music"),
        Play("menu_music", "audio/bgm/BGM_主界面.ogg", loop=True)
    ]

    on "hide" action Stop("menu_music", fadeout=1.0)

    ## 这确保任何其他菜单屏幕都被替换。
    tag menu
    
    add "main_menu_background"

    vbox:
        xpos 60
        yalign 0.15
        spacing 6
        
        if config.developer:
            textbutton _("Debug Jump") action ShowMenu("dev_jump_menu") style "main_menu_button"
        
    hbox:
        xalign 0.5
        yalign 0.98
        spacing 10
        
        # at transform:
            # zoom 0.5

        # 继续游戏
        fixed:
            xysize (245, 98)
            imagebutton:
                auto "gui/mm_continunes_%s.png"
                align (0.5, 0.5)
                at hover_move_down
                hovered Function(play_ui_hover)
                action [Function(play_ui_click), Continue()]
                alt _("继续游戏")

        # 开始游戏
        fixed:
            xysize (245, 98)
            imagebutton:
                auto "gui/mm_start_%s.png"
                align (0.5, 0.5)
                at hover_move_down
                hovered Function(play_ui_hover)
                action [Function(play_ui_click), Start()]
                alt _("开始游戏")

        # 载入游戏
        fixed:
            xysize (245, 98)
            imagebutton:
                auto "gui/mm_load_%s.png"
                align (0.5, 0.5)
                at hover_move_down
                hovered Function(play_ui_hover)
                action [Function(play_ui_click), ShowMenu("load")]
                alt _("读取游戏")

        # 系统设置
        fixed:
            xysize (245, 98)
            imagebutton:
                auto "gui/mm_config_%s.png"
                align (0.5, 0.5)
                at hover_move_down
                hovered Function(play_ui_hover)
                action [Function(play_ui_click), ShowMenu("my_settings_ui")]
                alt _("系统设置")

        # 附加鉴赏
        fixed:
            xysize (245, 99)
            imagebutton:
                auto "gui/mm_gallery_%s.png"
                align (0.5, 0.5)
                at hover_move_down
                hovered Function(play_ui_hover)
                action [Function(play_ui_click), ShowMenu("gallery")]
                alt _("附加鉴赏")

        # 作者的话
        fixed:
            xysize (245, 98)
            imagebutton:
                auto "gui/mm_about_%s.png"
                align (0.5, 0.5)
                at hover_move_down
                hovered Function(play_ui_hover)
                action [Function(play_ui_click), ShowMenu("about")]
                alt _("作者的话")

        # 退出
        fixed:
            xysize (245, 98)
            imagebutton:
                auto "gui/mm_quit_%s.png"
                align (0.5, 0.5)
                at hover_move_down
                hovered Function(play_ui_hover)
                action [Function(play_ui_click), ShowMenu("quit_confirm")]
                alt _("退出游戏")
