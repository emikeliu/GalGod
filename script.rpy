default bad_end_flag = 0 # >=7 才能往下走
default true_end_flag = 0 # >=4 才能进真结局
default true_end_finish = False # 解锁后日谈
default persistent.game_cleared = False # 解锁作者的话

screen ed_player(vid_path):
    add Movie(play=vid_path, channel="movie", size=(1920, 1080), keep_last_frame=True)

    key "dismiss" action []       # 拦截左键点击/确认
    key "K_SPACE" action []       # 拦截空格
    key "skip" action []          # 拦截 Ctrl
    key "stop_skipping" action [] 
    key "toggle_skip" action []   # 拦截 Tab
    key "hide_windows" action []      # 拦截 H 键和关联的隐藏 UI 动作
    key "mousedown_3" action []       # 拦截鼠标右键按下
    key "mouseup_3" action []         # 拦截鼠标右键弹起
    key "game_menu" action []     # 拦截ESC和鼠标右键

label start:
    call scene_1_1 from _call_scene_1_1
    call scene_1_2 from _call_scene_1_2
    call scene_1_3 from _call_scene_1_3
    call scene_1_4 from _call_scene_1_4

    call scene_2_1 from _call_scene_2_1
    call interlude1 from _call_interlude_1
    call interlude2 from _call_interlude_2
    call scene_2_2 from _call_scene_2_2
    call scene_2_3 from _call_scene_2_3
    call scene_2_4 from _call_scene_2_4

    call scene_3_1 from _call_scene_3_1
    call scene_3_2 from _call_scene_3_2
    call scene_3_3 from _call_scene_3_3
    call scene_3_4 from _call_scene_3_4

    if true_end_finish:
        # ED
        # 禁用跳过功能
        $ config.allow_skipping = False

        show screen ed_player("movies/ed.webm")
        $ renpy.pause(86.0)

        hide screen ed_player
        $ config.allow_skipping = True
        
        call after_story_noctella from _call_after_story_noctella
        $ persistent.game_cleared = True
    return
