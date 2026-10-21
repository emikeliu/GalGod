## 历史记录屏幕 ##############################################################
##
## 这是一个向玩家显示对话历史记录的屏幕。虽然此屏幕没有什么特别之处，
## 但它必须访问存储在_history_list中的对话历史记录。
##
## https://www.renpy.org/doc/html/history.html

define config.history_length = 250



screen history():

    tag menu

    ## 避免预测此屏幕，因为它可能非常大。
    predict False
    # 另一种备选判断方式
    #key "mousedown_5" action If(history_adj.value > 0 and history_adj.value == history_adj.range, true=Return(), false=NullAction())
    #key "mousedown_5" action If(GetFocusRect("history_text"), true=Return(), false=NullAction())
    
    

    

    add "gui/load_menu.png" # 背景；可以是任何内容
    add "gui/titlle_history.png" xalign 0.02 yalign 0.02
    imagebutton:
        idle "gui/cancel_idle.png"
        hover "gui/cancel_hover.png"
        xalign 0.98
        yalign 0.02
        action Return()
        alt _("关闭历史记录")

    use game_menu(_("History"))

    viewport:
        #tyle_prefix 'game_menu'
        area (100, 150, 1720, 850)
        mousewheel True draggable True pagekeys True yinitial 1.0
        scrollbars "vertical" 
        style_prefix "history" 

        has vbox

        style_prefix "history"
        

        for h in _history_list[-100:]:

            frame:
                has hbox
                if h.who:
                    label h.who style 'history_name':
                        substitute False
                        ## 从角色中获取who文本的颜色（如果已设置）
                        if "color" in h.who_args:
                            text_color h.who_args["color"]
                        xsize 200   # 这个数字和null宽度数字应该相同
                        xoffset 50
                else:
                    null width 200
                if h.voice.filename is not None:
                    #text "路径: [h.voice.filename]" size 12
                    imagebutton:
                        
                        
                        idle "gui/voice_idle.png" 
                        hover "gui/voice_hover.png"
                        # 核心动作：播放该条目保存的语音
                        action Play("voice", h.voice.filename) 
                        yalign 0.5
                        alt _("播放这句语音")
                            
                else:
                    null width 45
                    #text "无语音数据"

                
                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                button:
                    alt _("历史记录条目")
                    extra_alt _("[h.who]：[what]")
                    text what:
                        substitute False
                    if h.rollback_identifier:
                        #action RollbackToIdentifier(h.rollback_identifier)
                        action Confirm("确定要跳转到这句对话吗？\n", yes=RollbackToIdentifier(h.rollback_identifier))
                    style "text_box"
                    padding (20, 20, 20, 20)
                    xfill True
                    ysize 243

                    
                xoffset 0
        if not _history_list:
            label _("The dialogue history is empty.")


## 这决定了哪些标签可以在历史记录屏幕上显示。

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_frame:
    xsize 1400
    ysize None
    background None

style history_hbox:
    spacing 20
    xoffset 200

style history_vbox:
    spacing 20

style history_name:
    xalign 0.2
    yalign 0.2
    yoffset 100
    background "gui/name.png"
    xoffset 500

style history_name_text:
    textalign 1.0
    align (0.2, 0.1)
    color '#fff'
   
    yoffset -45
    size 30
    xoffset 0

style history_text:
    textalign 0.0
    
    size 30
    yalign 0.02

style history_label:
    xfill True

style history_label_text:
    xalign 0.5

style text_box:
    background "gui/history_jump_[prefix_]background.png"
    padding (20, 30, 30, 20)
style history_vscrollbar is vscrollbar:
    # 1. 设置滚动条的宽度
    xsize 10

    # 2. 设置轨道 (Base Bar)
    # Frame("路径", 左边距, 上边距) - 确保两端圆角不被拉伸
    base_bar Frame("gui/滚轮底.png", 5, 5)

    # 3. 设置滑块 (Thumb)
    # 同样建议使用 Frame，这样滑块长度变化时不会变形
    thumb Frame("gui/滚轮.png", 5, 5)
    
    # (可选) 滑块悬停时的图片
    # thumb_hover Frame("gui/history_thumb_hover.png", 5, 5)

    # 4. 如果内容不足不需要滚动时，隐藏滚动条
    unscrollable "hide"
