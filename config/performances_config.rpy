# performances_config.rpy

init -1:
    # ------------------------------------------------------------
    # 1. 基础立绘修正配置 (读取全局配置)
    # ------------------------------------------------------------
    transform actor_base_style:
        xanchor 0.5
        yanchor 1.0
        # 动态读取配置
        zoom global_actor_settings["zoom"]
        yalign 1.0
        # 动态读取配置
        yoffset global_actor_settings["y_offset"]
        subpixel True
 
    # ------------------------------------------------------------
    # 2. 通用演出动画
    # ------------------------------------------------------------
    
    # 小跳跃
    transform anim_jump:
        subpixel True
        # 先设置初始偏移为 0（相对于当前位置）
        yoffset 0
        # 从当前位置向上偏移 30 像素
        easein 0.15 yoffset -30
        # 归位到 0 相对偏移（即动画前的位置）
        easeout 0.15 yoffset 0

    # 惊讶/震动 (X轴左右晃动，不受垂直偏移影响，所以写法不变)
    transform anim_shake:
        subpixel True
        # 先设置初始偏移为 0
        xoffset 0
        easein 0.05 xoffset 10
        easeout 0.05 xoffset -10
        easein 0.05 xoffset 10
        easeout 0.05 xoffset 0

    # 呼吸动画 - 使用相对缩放
    # 注意：呼吸动画需要知道角色的基础缩放值
    # 由于每个角色的基础 zoom 不同，这个 transform 应该动态创建
    # 或者使用相对缩放的方式
    transform anim_breathing:
        subpixel True
        # 使用相对缩放：在当前缩放基础上微调
        zoom 1.0  # 相对缩放的基准
        easein 2.0 zoom 1.005
        easeout 2.0 zoom 1.0
        repeat
    
    # ------------------------------------------------------------
    # 3. 位置预设（保持不变）
    # ------------------------------------------------------------
    
    # 如果你有位置预设，可以继续使用
    # transform left:
    #     xalign 0.25
    #     yalign 1.0
    
    # transform right:
    #     xalign 0.75
    #     yalign 1.0