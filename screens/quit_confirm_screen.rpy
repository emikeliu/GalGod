screen quit_confirm():
    
    modal True
    
    
    zorder 200

    #底层图片
    add "gui/YES_save.png"

    
    hbox:
        
        xalign 0.5      
        yalign 0.54      
        spacing 100     # 两个按钮之间的间距
        
       
        imagebutton:
            idle "gui/YES_idle.png"   
            hover "gui/YES_hover.png" 
            action Quit(confirm=False)
            alt _("确认退出游戏")

        
        imagebutton:
            idle "gui/NO_idle.png"
            hover "gui/NO_hover.png"
            action [ Hide("quit_confirm"), Return() ]
            alt _("取消退出")

    #ESC退出这个screen
    key "game_menu" action [ Hide("quit_confirm"), Return() ]
