# 保持缩放比例不变
transform hud_zoom:
    zoom 0.6

init python:
    # 统一处理模式切换后的视觉通知与无障碍朗读反馈。
    def announce_accessibility_status(message):
        renpy.notify(message)
        renpy.display.tts.speak(message)

    # 切换快进模式，并在状态变化后播报开启或关闭。
    def toggle_skip_accessibility():
        was_skipping = bool(config.skipping)
        Skip()()
        is_skipping = bool(config.skipping)

        if is_skipping != was_skipping:
            message = _("快进已开启") if is_skipping else _("快进已关闭")
            announce_accessibility_status(message)

    # 切换自动播放模式，并在状态变化后播报开启或关闭。
    def toggle_auto_forward_accessibility():
        was_enabled = bool(renpy.game.preferences.afm_enable)
        Preference("auto-forward", "toggle")()
        is_enabled = bool(renpy.game.preferences.afm_enable)

        if is_enabled != was_enabled:
            message = _("自动播放已开启") if is_enabled else _("自动播放已关闭")
            announce_accessibility_status(message)

screen custom_ui():
    zorder 100
    if custom_ui:
        $ skip_status = _("已开启") if config.skipping else _("已关闭")
        $ skip_alt = renpy.substitutions.substitute(_("快进，当前[status]"), scope={"status": skip_status})[0]
        fixed:
            
            # ==========================================
            # 区域 1：右上角功能条 (跳过 | 自动 | 菜单)
            # ==========================================
            # 使用 hbox 让这三个按钮横着排成一行
            hbox:
                xalign 0.98 
                yalign 0.02
                spacing 10 # 按钮之间的间距
                
                # 1. Skip (快进)
                imagebutton:
                    at hud_zoom
                    idle "gui/快进1.png"
                    hover "gui/快进2.png"
                    # 选中状态(正在快进时)高亮
                    selected_idle "gui/快进2.png" 
                    selected_hover "gui/快进1.png"
                    selected bool(config.skipping)
                    
                    action Function(toggle_skip_accessibility) # 核心功能：快进
                    tooltip "快进模式"
                    alt skip_alt
                    extra_alt _("按下后切换快进模式。")

                # 2. Auto (自动播放)
                imagebutton:
                    at hud_zoom
                    idle ("gui/自动2.png" if preferences.afm_enable else "gui/自动1.png")
                    hover ("gui/自动1.png" if preferences.afm_enable else "gui/自动2.png")
                    
                    action Function(toggle_auto_forward_accessibility)
                    tooltip "自动播放"
                    # 自动播放的开关状态改为只在点击切换时播报，避免常驻按钮在界面刷新时反复朗读。
                    alt _("自动播放")

                # 3. Menu (系统菜单/设置)
                imagebutton:
                    at hud_zoom
                    idle "gui/菜单1.png"
                    hover "gui/菜单2.png"
                    
                    # ShowMenu("preferences") 打开设置，也可以用 "save" 打开存档页
                    action ShowMenu("my_settings_ui") 
                    tooltip "系统菜单"
                    alt _("系统菜单")

            # ==========================================
            # 区域 2：右下角存档区 (保持之前的 Grid 布局)
            # ==========================================
            grid 5 1:
                at hud_zoom
                
                xalign 0.98
                yalign 0.98 
                
                spacing 25
                imagebutton:
                    idle "gui/LOG1.png"
                    hover "gui/LOG2.png"
                    action ShowMenu("history")
                    tooltip "快速存档"
                    alt _("历史记录")
                
                # 第一行
                imagebutton:
                    idle "gui/Q.S 1.png"
                    hover "gui/Q.S 2.png"
                    action [QuickSave(), Notify("⚡️ 已快速存档")]
                    tooltip "快速存档"
                    alt _("快速存档")

                imagebutton:
                    idle "gui/Q.L 1.png"
                    hover "gui/Q.L 2.png"
                    action QuickLoad()
                    tooltip "快速读取"
                    alt _("快速读取")

                # 第二行
                imagebutton:
                    yoffset -10
                    idle "gui/存档1.png"
                    hover "gui/存档2.png"
                    action ShowMenu("save")
                    tooltip "打开存档界面"
                    alt _("打开保存界面")

                imagebutton:
                    yoffset -10
                    idle "gui/读档1.png"
                    hover "gui/读档2.png"
                    action ShowMenu("load")
                    tooltip "打开读档界面"
                    alt _("打开读取界面")

init python:
    config.overlay_screens.append("custom_ui")

default custom_ui = True
