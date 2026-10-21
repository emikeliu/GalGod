# 00_config.rpy

# 使用 init -2 确保这些变量最先被初始化，这样 transforms.rpy 才能读取到
init -2 python:
    # 【全局配置】在这里调整立绘的物理属性
    # 1. 处里空格键 (Space)
    # 先从 'dismiss' (继续对话) 和 'button_select' (点击按钮) 中移除空格
    # 这样按空格就不会跳过对话了
    keys_to_remove = ['K_SPACE']
    
    for k in keys_to_remove:
        if k in config.keymap['dismiss']:
            config.keymap['dismiss'].remove(k)
        if k in config.keymap['button_select']:
            config.keymap['button_select'].remove(k)

    # 将空格键添加到 'hide_windows' (隐藏对话框)
    # 注意：Ren'Py 默认是用鼠标中键或 'h' 键隐藏
    if 'K_SPACE' not in config.keymap['hide_windows']:
        config.keymap['hide_windows'].append('K_SPACE')

    # 2. 处理鼠标滚轮向上 (Mousedown_4)
    # 从默认的 'rollback' (回滚时光) 中移除滚轮向上
    # 这样我们才能在 screen say 中重新定义它的功能
    if 'mousedown_4' in config.keymap['rollback']:
        config.keymap['rollback'].remove('mousedown_4')
    global_actor_settings = {
        # 立绘缩放比例 (0.75 表示缩小到 75%)
        "zoom": 0.6,
        
        # 垂直偏移修正 (像素)
        # 正数 = 向下移 (藏起脚部)
        # 负数 = 向上移
        "y_offset": 1250
    }
