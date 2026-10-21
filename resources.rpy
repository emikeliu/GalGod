screen centered_left_text(content):
    # 1. 定义一个屏幕变量，用来追踪文本是否显示完毕
    # False = 正在打字, True = 打字完成
    default is_finished = False

    zorder 100
    
    fixed:
        xpos 0.15
        ypos 0.4
        xsize 1200
        
        text content:
            xalign 0.0
            text_align 0.0
            color "#fff"
            outlines [(2, "#000000bd", 0, 0)]
            font "JCYT500W.ttf"
            size 36
            line_leading 10
            
            # 2. 动态控制速度：
            # 如果 is_finished 为 True（玩家点击了），速度变为 0（瞬间显示），否则保持 25 cps 的显示速度
            slow_cps (0 if is_finished else 25)
            
            # 3. 监听完成事件：
            # 当文字自然播放完毕时，自动将 is_finished 设为 True
            slow_done SetScreenVariable("is_finished", True)
    
    # 4. 智能交互逻辑
    # 逻辑：如果(If)打字完成了 -> 点击由于关闭屏幕(Return)
    #      否则(False) -> 点击设为完成状态(瞬间显示剩余文字)
    
    key "dismiss" action If(is_finished, Return(), SetScreenVariable("is_finished", True))
    
    button:
        xfill True
        yfill True
        background None
        action If(is_finished, Return(), SetScreenVariable("is_finished", True))



init -2 python:
    def bg_fit(path):
        # 获取当前画布（1k）的宽高
        sw, sh = config.screen_width, config.screen_height
        
        # 获取图片的原始宽高（自动识别 1k/4k/甚至奇葩分辨率）
        iw, ih = renpy.image_size(path)

        # 核心通用逻辑：计算覆盖全屏所需的比例
        # 如果是 4k 进 1k，scale 会是 0.5 左右（缩小显示，保留细节）
        # 如果是 1k 进 1k，scale 会是 1.0（原样显示）
        # 如果是小图进 1k，scale 会大于 1.0（放大填充）
        scale = max(float(sw) / iw, float(sh) / ih)

        # 4. 返回 Transform 而非静态图片
        return Transform(
            path,
            zoom=scale,       # 动态缩放，交给 GPU 采样，保住 4k 细节
            xalign=0.5,       # 居中显示
            yalign=0.5,
            subpixel=True     # 开启次像素渲染，让平移、缩放动画丝滑不抖动
        )


    def bg_focus(path, zoom=1.3, x=0.5, y=0.5):
        # 获取基础数据
        sw, sh = config.screen_width, config.screen_height
        iw, ih = renpy.image_size(path)

        # 计算 Cover 基础比例（让图至少填满 1k 屏幕）
        base_scale = max(float(sw) / iw, float(sh) / ih)
        
        # 最终缩放倍率
        # 直接作用于原始 4K 图像，不经过 im.Scale 损耗
        final_zoom = base_scale * zoom

        # 返回一个具备“次像素级别”清晰度的变换
        return Transform(
            path,
            zoom=final_zoom,
            # 使用 align 配合 zoom 能够自动锁定聚焦中心
            xalign=x,
            yalign=y,
            # 必须开启 subpixel，否则在放大后平移会有一格一格的锯齿感
            subpixel=True
        )

# 杂鱼们的立绘
image ty_a shadow = "images/characters/other/体育生.png"
image father shadow = "images/characters/other/男剪影.png"
image mother shadow = "images/characters/other/女剪影.png"
image other renchao = "images/characters/other/renchao.png"

# 定义背景图片
image bg moon        = bg_focus("images/bg/moon.avif", zoom=1.5, x=0.2, y=0.3)
image bg moon_all    = bg_fit("images/bg/moon.avif")
image bg street1_1   = bg_fit("images/bg/街道1_白天.avif")
image bg street1_2   = bg_fit("images/bg/街道1_傍晚.avif")
image bg street2_1   = bg_fit("images/bg/街道2_白天.avif")
image bg street2_2   = bg_fit("images/bg/街道2_傍晚.avif")
image bg street3_1   = bg_fit("images/bg/街道3_白天.avif")
image bg classroom1 = bg_fit("images/bg/教室_白天.avif")
image bg classroom2 = bg_fit("images/bg/教室_傍晚.avif")
image bg classroom3 = bg_fit("images/bg/教室_夜晚.avif")
image bg classroom_floor = bg_fit("images/bg/教室地板.webp")
image bg room1_4    = bg_fit("images/bg/小卧室_夜晚开灯.avif")
image bg elevator    = bg_fit("images/bg/电梯内.avif")
image bg school1    = bg_fit("images/bg/学校中庭1.webp")
image bg school2    = bg_fit("images/bg/教学楼前.webp")
image bg sportsroom    = bg_fit("images/bg/体育储藏室.webp")
image bg tearoom    = bg_fit("images/bg/茶餐厅.webp")
image bg riverside_road = bg_fit("images/bg/河边白天.webp")
image bg riverside_road2 = bg_fit("images/bg/河边夕阳.webp")
image bg stair_landing  = bg_fit("images/bg/楼道.webp")
image bg shopping_mall  = bg_fit("images/bg/商场.webp")
image bg box_seat  = bg_fit("images/bg/包厢.avif")
image bg neighborhood  = bg_fit("images/bg/小区道路_夜晚.webp")
image bg neighborhood_vague  = bg_fit("images/bg/小区道路_夜晚_模糊.webp")
image bg urban_skies = bg_fit("images/bg/都市天空.webp")
image bg hotel_entrance = bg_fit("images/bg/高级酒店_大门夜晚.webp")
image bg hotel_restaurant = bg_fit("images/bg/高级酒店_早餐厅夜晚.webp")
image bg hotel_livingroom = bg_fit("images/bg/高层客厅_白天.webp")
image bg hotel_corridor = bg_fit("images/bg/高级酒店走廊_白天.webp")
image bg test_paper = bg_fit("images/bg/test_paper.webp")

image bg heavenly_altar = bg_fit("images/bg/天坛.webp")
image bg heavenly_altar_focus = bg_focus("images/bg/天坛.webp", zoom=1.9, x=0.52, y=0.15)

image bg white = Solid("#fff")
image bg black = Solid("#000")

image bg noctella_background = bg_fit("images/cg/noctella_background.webp")


# 后日谈使用背景
image bg computer_desk  = bg_fit("images/bg/电脑桌_晚上关灯.webp")
image bg kitchen    = bg_fit("images/bg/小厨房_晚上开灯.webp")
image bg living_room1    = bg_fit("images/bg/小客厅_晚上关灯.webp")
image bg living_room2   = bg_fit("images/bg/小客厅_晚上开灯.webp")



# CG
image cg 001 = bg_fit("images/cg/001.avif")
image cg 002 = bg_fit("images/cg/002.avif")
image cg 003 = bg_fit("images/cg/003.avif")
image cg 004 = bg_fit("images/cg/004.avif")
image cg 005 = bg_fit("images/cg/005.avif")
image cg 006 = bg_fit("images/cg/006.avif")
image cg 007 = bg_fit("images/cg/007.avif")
image cg 008 = bg_fit("images/cg/008.avif")
image cg 009 = bg_fit("images/cg/009.avif")
image cg 010 = bg_fit("images/cg/010.avif")
image cg 011 = bg_fit("images/cg/011.avif")
image cg 012 = bg_fit("images/cg/012.avif")
image cg 013 = bg_fit("images/cg/013.avif")

image cg noctella_descend = "images/cg/noctella_descend.webp" # 这张图展示4k大图
# image cg noctella_descend_full = Transform("images/cg/noctella_descend.webp", xsize=1920, ysize=1080, fit="cover")
image cg noctella_descend_full = bg_fit("images/cg/noctella_descend.webp")


#SDCG
image sdcg 001 = bg_focus("images/sdcg/001.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 002 = bg_focus("images/sdcg/002.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 003 = bg_focus("images/sdcg/003.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 004 = bg_focus("images/sdcg/004.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 005 = bg_focus("images/sdcg/005.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 006 = bg_focus("images/sdcg/006.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 007 = bg_focus("images/sdcg/007.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 008 = bg_focus("images/sdcg/008.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 009 = bg_focus("images/sdcg/009.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 010 = bg_focus("images/sdcg/010.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 011 = bg_focus("images/sdcg/011.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 012 = bg_focus("images/sdcg/012.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 013 = bg_focus("images/sdcg/013.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 014 = bg_focus("images/sdcg/014.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 015 = bg_focus("images/sdcg/015.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 016 = bg_focus("images/sdcg/016.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 017 = bg_focus("images/sdcg/017.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 018 = bg_focus("images/sdcg/018.avif",zoom=0.5, x=0.5, y=0.35)
image sdcg 019 = bg_focus("images/sdcg/019.avif",zoom=0.5, x=0.5, y=0.35)



# 纯黑
image cinematic_black_overlay:
    Solid("#000")
    alpha 0.0          # 初始透明
    linear 2.0 alpha 1.0 # 在 2 秒内线性变为不透明

image pavilion  = bg_fit("images/bg/凉亭.avif")

# 音效
define fx.elevator = "audio/fx/FX_电梯运行.ogg"
define fx.door_open = "audio/fx/FX_电梯开门声.ogg"
define fx.deng = "audio/fx/FX_噔.mp3"
define fx.deng2 = "audio/fx/FX_噔2.mp3"
define fx.dingdong = "audio/fx/FX_叮咚.mp3"
define fx.crowd = "audio/fx/FX_嘈杂声.ogg"
define fx.camera = "audio/fx/FX_照相机.mp3"
define fx.slap = "audio/fx/FX_嗖.mp3"
define fx.pa = "audio/fx/FX_pa.mp3"
define fx.wind = "audio/fx/FX_风吹过.mp3"
define fx.play_basketball = "audio/fx/FX_篮球场.mp3"
define fx.shot = "audio/fx/FX_投篮.mp3"
define fx.heartbeat = "audio/fx/FX_心跳.mp3"
define fx.classbell = "audio/fx/FX_上课铃.mp3"
define fx.thunder = "audio/fx/FX_打雷.mp3"
define fx.thunder2 = "audio/fx/FX_打雷2.mp3"
define fx.light_rain = "audio/fx/FX_小雨滴答.mp3"
define fx.rainstorm = "audio/fx/FX_大雨.ogg"
define fx.kabe_don = "audio/fx/FX_壁咚.mp3"
define fx.fabric_collision = "audio/fx/FX_布料碰撞.mp3"
define fx.cans = "audio/fx/FX_罐子.ogg"
define fx.fry = "audio/fx/FX_煎.ogg"
define fx.boil = "audio/fx/FX_煮.ogg"


# 特效
define flash = Fade(0.1, 0.0, 0.5, color="#fff")


# 定义一个让图片从透明变不透明的变换
transform forced_dissolve(t):
    alpha 0.0
    linear t alpha 1.0

transform reset_filter:
    matrixcolor IdentityMatrix()

transform gray_filter:
    matrixcolor SaturationMatrix(0)

transform memory_filter:
    matrixcolor (
        TintMatrix("#f0deb0")
        * SaturationMatrix(0.5)
        * ContrastMatrix(0.9)
    )