## 偏好设置屏幕 ##########################################################
##
## 偏好设置屏幕允许玩家配置游戏以更好地适应自己。
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    add HBox(Transform("#292835", xsize=350), "#21212db2") # 背景；可以是任何内容

    text "":
        # 页面级说明放在简单显示对象上，避免挂到复杂根容器导致 group_alt/extra_alt 串到子节点。
        extra_alt _("系统设置页面。这里可以调整文本速度、音量和显示选项。按方向键切换控件。")

    use game_menu(_("Config"))

    viewport:
        style_prefix 'game_menu'
        mousewheel True draggable True pagekeys True
        scrollbars "vertical"
        has vbox

        hbox:
            box_wrap True

            if renpy.variant("pc") or renpy.variant("web"):
                # 只有桌面和网页版本才需要全屏/窗口模式

                vbox:
                    style_prefix "radio"
                    label _("显示")
                    textbutton _("窗口"):
                        # 确保在非全屏模式下选中此按钮。
                        selected not preferences.fullscreen
                        action Preference("display", "window")
                    textbutton _("全屏"):
                        action Preference("display", "fullscreen")

            vbox:
                style_prefix "check"
                label _("快进")
                textbutton _("跳过未读文本"):
                    action Preference("skip", "toggle")
                textbutton _("选项后继续跳过"):
                    action Preference("after choices", "toggle")
                textbutton _("跳过过渡动画"):
                    action InvertSelected(Preference("transitions", "toggle"))

            ## 可以在此处添加类型为"radio_pref"或"check_pref"的额外vbox，
            ## 以添加额外的创建者自定义偏好设置。

        null height 60

        hbox:
            style_prefix "slider"
            box_wrap True

            vbox:

                label _("文本展示速度")
                bar value Preference("text speed")

                label _("自动播放速度")
                bar value Preference("auto-forward time")

            vbox:

                if config.has_music:
                    label _("音乐音量")
                    hbox:
                        bar value Preference("music volume")

                if config.has_sound:
                    label _("音效音量")
                    hbox:
                        bar value Preference("sound volume")
                        if config.sample_sound:
                            textbutton _("Test") action Play("sound", config.sample_sound)


                if config.has_voice:
                    label _("语音音量")
                    hbox:
                        bar value Preference("voice volume")
                        if config.sample_voice:
                            textbutton _("Test") action Play("voice", config.sample_voice)

                if config.has_music or config.has_sound or config.has_voice:
                    null height 15
                    textbutton _("静音"):
                        style_prefix "check"
                        action Preference("all mute", "toggle")

### PREF
style pref_label:
    top_margin 15
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

## RADIO
style radio_label:
    is pref_label

style radio_label_text:
    is pref_label_text

style radio_vbox:
    is pref_vbox
    spacing 0

style radio_button:
    foreground "gui/button/radio_[prefix_]foreground.png"
    padding (35, 6, 6, 6)

## CHECK
style check_label:
    is pref_label
style check_label_text:
    is pref_label_text

style check_vbox:
    is pref_vbox
    spacing 0

style check_button:
    foreground "gui/button/check_[prefix_]foreground.png"
    padding (35, 6, 6, 6)

## SLIDER
style slider_label:
    is pref_label
style slider_label_text:
    is pref_label_text

style slider_slider:
    xsize 525

style slider_button:
    yalign 0.5
    left_margin 15

style slider_vbox:
    is pref_vbox
    xsize 675

