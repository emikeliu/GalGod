
#需修改：标题的hover和idle样式，快进速度和自动速度，文本框预览，角色音量控制
# 用于记录当前分页
default current_setting_page = "game"
define config.game_menu_action = ShowMenu("my_settings_ui")
define textbox_preview_repeat_time = 5.0
default countdown_time = 0.0
# 用于记录对话框透明度 (0.0 - 1.0)，默认 1.0 (不透明)
default persistent.dialogue_box_alpha = 0.7

default lx_vol_var =0
# 初始化一个持久化变量，默认值为 5
default persistent.skip_speed_var = 5

init python:
    # 每一帧都根据持久化变量更新快进延迟
    def update_skip_speed():
        config.skip_delay = int(persistent.skip_speed_var)

    # 将其加入循环（或者简单的在设置界面修改）
    config.periodic_callback = update_skip_speed
    config.afm_voice_delay = 0.5  # 语音结束后额外等待 0.5 秒再跳下一句
    preferences.wait_for_voice = True
    def reset_custom_settings():
        
        persistent.skip_speed_var = 5
        persistent.dialogue_box_alpha = 0.7
        #persistent.
        
        # 检查字典是否存在，避免报错
        if not hasattr(persistent, '_character_volume') or persistent._character_volume is None:
            persistent._character_volume = {}

        
        char_list = ["lx", "jwq", "xl"]
        
        for char_id in char_list:
            # 更新持久化变量（用于保存）
            persistent._character_volume[char_id] = 1.0
            
            
            try:
                renpy.voice.set_character_volume(char_id, 1.0)
            except AttributeError:
                
                pass
    
screen my_settings_ui():
    tag menu
    
    default display_preview = True
    key "game_menu" action Return()

    #on "hide" action Function(restore_channel_volumes)
    #on "replace" action Function(restore_channel_volumes)
    modal True
    
    # 全屏背景图
    add "gui/config_menu.png"
    add "gui/system_config_titlle.png"

    #左侧标题（游戏设置，音量设置）
    vbox:
        xpos 50 
        ypos 50
        spacing 20 

        null height 80

        
        vbox:
            spacing 15

             
            imagebutton:
                auto "gui/game_config_%s.png"
                # 点击切换到 game 分页
                action SetScreenVariable("current_setting_page", "game") 
                # 选中状态检测
                selected (current_setting_page == "game")
                alt _("切换到游戏设置")

            imagebutton:
                auto "gui/sound_config_%s.png"
                action SetScreenVariable("current_setting_page", "audio")
                selected (current_setting_page == "audio")
                alt _("切换到音量设置")
    imagebutton:
        idle "gui/cancel_idle.png"
        hover "gui/cancel_hover.png"
        xalign 0.98
        yalign 0.02
        action Return()
        alt _("关闭设置")

    #右侧区域
    frame:
        background None
        xpos 500
        ypos 150
        xsize 800
        ysize 600
        
        #音效设置
        if current_setting_page == "audio":
            hbox:
                spacing 400
                vbox:
                    spacing 90
                
                    
                    vbox:
                        spacing 20
                        add "gui/main_voice.png" 
                        bar value Preference("main volume") style "custom_image_bar" alt _("主音量 [text]")
                    vbox:
                        spacing 20
                        add "gui/music_voice.png"
                        
                    
                        
                        bar value Preference("music volume") style "custom_image_bar" alt _("音乐音量 [text]")

                    
                    vbox:
                        spacing 20
                        add "gui/cv_voice.png"
                    
                        bar value  Preference("sound volume")  style "custom_image_bar" alt _("音效音量 [text]") 
                
                    
                    vbox:
                        spacing 20
                    
                        add "gui/character_voice.png"
                        bar value Preference("voice volume") style "custom_image_bar" alt _("语音总音量 [text]")
                vbox:
                    yoffset 100
                    spacing 100
                    
                    # --- 角色 1：男主 (对应 voice_hero 通道) ---
                    vbox:
                        spacing 50
                        # 这里可以用图片 add "gui/name_hero.png" 代替 text
                        #text "林曦" color "#ffffff" size 30
                        add "gui/text_lx.png"
                        #add "gui/lx_icon.jpg" xysize(109,109)
                        # 【关键】控制 "voice_hero" 通道的音量
                        bar value DictValue(dict=persistent._character_volume,key="lx",range=1.0,force_step=True) style "custom_image_bar" alt _("林曦语音音量 [text]")
                        #text "{:.0f}".format(persistent._character_volume["lx"]*10)

                    # --- 角色 2：系统音 (对应 voice_system 通道) ---
                    vbox:
                        spacing 50
                        #text "江晚晴" color "#ffffff" size 30
                        add "gui/text_jwq.png"
                        #add "gui/jwq_icon.jpg" xysize(109,109)
                        # 【关键】控制 "voice_system" 通道的音量
                        bar value DictValue(dict=persistent._character_volume,key="jwq",range=1.0) style "custom_image_bar" alt _("江晚晴语音音量 [text]")

                    # --- 角色 3：其他/预留 ---
                    vbox:
                        spacing 50
                        #text "小涟" color "#ffffff" size 30
                        add "gui/text_xl.png"
                        #add "gui/xl_icon.jpg" xysize(109,109)
                        # 如果没有专门的通道，可以用 Voice Volume "Tag"
                        # 或者在此处添加新的自定义通道
                        bar value DictValue(dict=persistent._character_volume,key="xl",range=1.0) style "custom_image_bar" alt _("小涟语音音量 [text]")

                    
        #游戏设置
        elif current_setting_page == "game":
            
            
            hbox:
                spacing 300

                
                vbox:
                    spacing 40 

                    
                    vbox:
                        spacing 20
                        add "gui/screen_mode_title.png" 
                        hbox:
                            spacing 20
                            xoffset 50
                            # 窗口模式按钮
                            imagebutton:
                                auto "gui/window_%s.png"
                                action Preference("display", "window") 
                                yoffset 10
                                selected_idle "gui/window_hover.png"
                                selected_hover "gui/window_hover.png"
                                alt _("窗口模式")
                            # 全屏模式按钮
                            imagebutton:
                                auto "gui/full_screen_%s.png"
                                action Preference("display", "fullscreen")
                                selected_idle "gui/full_screen_hover.png"
                                selected_hover "gui/full_screen_hover.png"
                                alt _("全屏模式")

                    
                    vbox:
                        spacing 80
                        add "gui/text_spped_title.png"
                        bar value FieldValue(preferences, "text_cps", range=200, max_is_zero=True) style "custom_image_bar" changed renpy.restart_interaction alt _("文本播放速度 [text]")

                    # 3. 自动模式速度
                    vbox:
                        spacing 80
                        add "gui/auto_spped_title.png"
                        bar value Preference("auto-forward time") style "custom_image_bar" alt _("自动播放速度 [text]")
                    
                    # 4. 快进速度
                    
                    vbox:
                        spacing 80
                        add "gui/skips_title.png"
                        # 暂时指向 auto-forward time
                        bar value VariableValue("persistent.skip_speed_var", range=10) style "custom_image_bar" alt _("快进速度 [text]") 

                
                vbox:
                    spacing 40

                    
                    
                        

                    
                    vbox:
                        spacing 70
                        add "gui/window_alpha_title.png"
                        # 控制 persistent.dialogue_box_alpha 变量，范围 0.0-1.0
                        bar value VariableValue("persistent.dialogue_box_alpha", range=1.0, step=0.05) style "custom_image_bar" alt _("文本框透明度 [text]")

                    
                    vbox:
                        spacing 20
                        yoffset -15
                        add "gui/skip_title.png"
                        hbox:
                            spacing 45
                            yalign 0.5
                            xoffset 50
                            
                            imagebutton:
                                auto "gui/skip_all_%s.png"  yoffset -6
                                action SetField(preferences, "skip_unseen", True)
                                # 当 skip_unseen 为 True 时，按钮高亮
                                selected (preferences.skip_unseen)
                                selected_idle "gui/skip_all_hover.png"
                                selected_hover "gui/skip_all_hover.png"
                                alt _("跳过全部文本")
                            
                            imagebutton:
                                idle Transform("gui/skip_read_idle.png"   ,yoffset=1)
                                hover Transform("gui/skip_read_hover.png",yoffset=2)
                                action SetField(preferences, "skip_unseen", False)
                                
                                selected (not preferences.skip_unseen)
                                selected_idle Transform("gui/skip_read_hover.png"   ,yoffset=2)
                                selected_hover Transform("gui/skip_read_hover.png",yoffset=2)
                                alt _("仅跳过已读文本")
                                
                    vbox:
                        spacing 10
                        
                        fixed:
                            frame:
                                # 1. 设置背景图片 (可以使用 Frame 缩放，防止边角拉伸)
                                # 如果没有图片，也可以用 "#000a" 代表半透明黑色
                                background Frame("gui/text_box.png") 
                                    
                                # 2. 设置内边距，让文字不要挨着背景边缘
                                
                                    
                                # 3. 设置位置
                                xalign 0.345
                                yalign 0.895
                                    
                                # 4. (可选) 设置最小/最大宽度，防止文字太长或太短
                                xysize(477,288)
                                yoffset 100
                                xoffset 50
                                if display_preview:

                                    text "调整文字播放速度":
                                        id "preview_text_[preferences.text_cps]" # 建议加上 ID 联动，拉动即播
                                        color "#F5f5f5" 
                                        outlines [(2, "#4f4f4f", absolute(0), absolute(0))]
                                        slow_cps preferences.text_cps
                                        
                        timer textbox_preview_repeat_time:
                            action [SetScreenVariable("display_preview",False)]
                        timer textbox_preview_repeat_time+1.0 repeat True action [Hide('my_settings_ui'),SetVariable("countdown_time",textbox_preview_repeat_time+1.0),Show("my_settings_ui")]   
                            
                            
                            
                            
                                
    #底部按钮
    imagebutton:
        auto "gui/Initial_%s.png"
        action Confirm(
            "确定要恢复默认设置吗？", 
            yes=[
                Preference("reset"), 
                Function(reset_custom_settings),
                Preference("music volume", 0.26),
                Preference("sfx volume", 0.26),
                Preference("voice volume", 1.0)
            ],
        confirm_selected=True
    )
        xalign 0.6 yalign 0.9 xoffset 100
        alt _("恢复默认设置")
        
    imagebutton:
        auto "gui/back_to_title_%s.png"
        action If(main_menu, Return(), MainMenu())
        xalign 0.5 yalign 0.9 xoffset -110
        alt _("返回标题")
        

#滚动条样式
style custom_image_bar:
    xsize 259
    ysize 20
    xoffset 100
    top_gutter 10      
    bottom_gutter 10
    
    left_bar Transform("gui/底.png", ysize=10)
    right_bar Transform("gui/底.png", ysize=10)
    bar_vertical False
    
    thumb Transform("gui/圆.png", yoffset=-20)
    
    # 调整滑块与槽的偏移量
    thumb_offset -10
screen textbox_preview():
 
    tag preview
 
 
    fixed:
        frame:
            background "gui/text_box.png"
            xysize(477,288)
            align(.7,.0)
            left_margin 20
            text "如果能找寻到那真实的解脱，请告诉我" color "#F5f5f5" outlines [(2, "#4f4f4f",absolute(0), absolute(0))] slow_cps preferences.text_cps xalign .1 yalign .9
init python:
    # 定义一个函数，接收滑动条传回的 value，并应用到角色音量
    def update_lx_volume(v):
        # 这里的 renpy.audio.voice.set_character_volume 是 SetCharacterVolume 的底层函数
        renpy.audio.voice.set_character_volume("lx", v)
init python:
    # 1. 从默认的游戏菜单动作中移除鼠标右键
    if 'mouseup_3' in config.keymap['game_menu']:
        config.keymap['game_menu'].remove('mouseup_3')

    # 2. 将鼠标右键绑定到隐藏界面动作 (HideInterface)
    # 在 Ren'Py 中，'hide_windows' 是负责隐藏 UI 的内置动作，默认键是 'h'
    config.keymap['hide_windows'].append('mouseup_3')
#sound_config
init python:
    if not hasattr(persistent, '_character_volume'):
        persistent._character_volume = {}  ##判断字典存不存在，不存在则创建
    
    if 'xl' not in persistent._character_volume:
        persistent._character_volume['xl'] = 1.0
    if 'lx' not in persistent._character_volume:
        persistent._character_volume['lx'] = 1.0
    if 'jwq' not in persistent._character_volume:
        persistent._character_volume['jwq'] = 1.0
