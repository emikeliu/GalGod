#需更改的地方：cancel的样式，增加跳转功能，增加语音功能
screen history_menu():
    tag menu

    ## 1. 全屏背景
    add "gui/history.png"

    ## 2. 左上角的“历史记录”标题
    add "gui/titlle_history.png":
        xalign 0.02
        yalign 0.02

    ## 3. 返回按钮
    imagebutton:
        idle "gui/cancel_idle.png"
        hover "gui/cancel_hover.png"
        action Return()
        xalign 0.98
        yalign 0.02

    ## 4. 历史记录内容区域 (Viewport)
    viewport:
        id "history_vp"
        draggable True      # 允许触屏拖动
        mousewheel True     # 允许鼠标滚轮滚动
        
        
        # scrollbars "vertical" 
        
        # 设定显示区域
        area (100, 150, 1720, 850)
        yinitial 1.0

        vbox:
            spacing 30 

            for h in _history_list:
                hbox:
                    spacing 20 

                    ## --- A. 姓名框 ---
                    if h.who:
                        fixed:
                            xsize 200
                            ysize 60 
                            yalign 0.5 
                            yoffset 20 

                            add "gui/name.png" yalign 0.5

                            text h.who:
                                style "history_name_text"
                                align (0.5, 0.5)
                                yoffset -20
                    else:
                        null width 200

                    ## --- B. 对话框 ---
                    button:
                        xsize 1229
                        ysize 243
                        yalign 0.5

                        background "gui/history_jump_idle.png"
                        hover_background "gui/history_jump_hover.png"
                        action NullAction()

                        padding (60, 50, 60, 50)

                        text h.what:
                            style "history_text"
                            text_align 0.0
                            yalign 0.5 
                            layout "subtitle"
                            xmaximum 1100

    ## 5. 垂直滚动条 (UI组件)
    
    vbar:
        # 1. 绑定逻辑：控制 id 为 "history_vp" 的垂直滚动
        value YScrollValue("history_vp")

        # 2. 位置与大小
        
        xpos 1600
        ypos 150
        
        # 高度
        ysize 769
        
        # 宽度
        xsize 8 

        # 3. 图片样式
        # thumb: 滑块图片
        thumb "gui/滚轮.png"
        
        # base_bar: 滑槽背景
        base_bar "gui/滚轮底.png"
        
        # 4. 微调 (可选)
        # 如果滑块到了顶端被切掉一半，或者到了底端出界，调整 thumb_offset
        # 通常设为滑块图片高度的一半
        #thumb_offset 20
        
        # 当内容不足以滚动时，隐藏滚动条
        unscrollable "hide"


## 样式定义
style history_name_text:
    size 30
    color "#ffffff"
    outlines [(2, "#000000", 0, 0)]

style history_text:
    size 30 
    color "#ffffff"