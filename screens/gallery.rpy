## 画廊 #####################################################################
##
## 使用 Ren'Py 内置画廊系统的画廊屏幕基本设置。
## 更多信息请见：
## https://www.renpy.org/doc/html/rooms.html#image-gallery
##
init python:


    
    gallery_thumb_size = (400, 225)
    ## 为方便起见：列出我们将在此画廊中使用的
    ## 所有画廊图像名称
    gallery_buttons = [
        'sdcg_002','ashwin_cg_1', 'xia_cg_1', 'zoran_cg_1','cg_004','cg_005', 'sdcg_009', 'sdcg_001', 'sdcg_003'
    ]
    gallery_button_alts = {
        "sdcg_002": _("政客短插图"),
        "ashwin_cg_1": _("林曦班级短插图"),
        "xia_cg_1": _("小涟插图"),
        "zoran_cg_1": _("男主打球短插图"),
        "cg_004": _("林曦吃冰激凌短插图"),
        "cg_005": _("林曦推倒插图"),
        "sdcg_009": _("江晚晴淋雨插图"),
        "sdcg_001": _("林曦告白插图"),
        "sdcg_003": _("诺提拉插图"),
    }
    ## 设置画廊
    g = Gallery()
    g.locked_button = Transform("gui/CG_box_idle.png", xysize=gallery_thumb_size)
    g.transition = dissolve
    ## 并声明各种画廊图像
    ## 此文件不假定存在任何 GUI 文件，所以我
    ## 只是使用下面声明为图像的基本方块，但你需要
    ## 用实际图像替换这些。
    ## 这些使用在 gallery_buttons 列表中声明的名称

    g.button("sdcg_002")#政客sdcg
    g.condition("renpy.seen_image('sdcg 001')") #sdcg用这个判断条件，当看到这张图片时，解锁这个按钮
    g.display(Transform("sdcg 001", xysize=(1920, 1080))) #下面放差分
    g.display(Transform("sdcg 002", xysize=(1920, 1080)))

    g.button("ashwin_cg_1")#林曦班级内sdcg
    g.condition("renpy.seen_image('sdcg 004')")
    g.display(Transform("sdcg 004", xysize=(1920, 1080)))
    g.display(Transform("sdcg 005", xysize=(1920, 1080)))
    g.display(Transform("sdcg 006", xysize=(1920, 1080)))
    g.display(Transform("sdcg 007", xysize=(1920, 1080)))
    g.display(Transform("sdcg 008", xysize=(1920, 1080)))
    g.display(Transform("sdcg 009", xysize=(1920, 1080)))
    g.display(Transform("sdcg 010", xysize=(1920, 1080)))
    g.display(Transform("sdcg 011", xysize=(1920, 1080)))
    g.display(Transform("sdcg 012", xysize=(1920, 1080)))
    g.display(Transform("sdcg 013", xysize=(1920, 1080)))

    g.button("xia_cg_1")#小涟cg
    g.condition("renpy.seen_image('cg 001')")
    g.display(Transform("cg 001", xysize=(1920, 1080)))
    g.display(Transform("cg 002", xysize=(1920, 1080)))
    g.display(Transform("cg 003", xysize=(1920, 1080)))

    g.button("zoran_cg_1")#男主打球sdcg
    g.condition("renpy.seen_image('sdcg 019')")
    g.display(Transform("sdcg 019", xysize=(1920, 1080)))

    g.button("cg_004")#林曦吃冰激凌sdcg
    g.condition("renpy.seen_image('sdcg 014')")
    g.display(Transform("sdcg 014", xysize=(1920, 1080)))
    g.display(Transform("sdcg 015", xysize=(1920, 1080)))
    g.display(Transform("sdcg 016", xysize=(1920, 1080)))
    g.display(Transform("sdcg 017", xysize=(1920, 1080)))
    g.display(Transform("sdcg 018", xysize=(1920, 1080)))

    g.button("cg_005")#林曦推倒cg
    g.condition("renpy.seen_image('cg 004')")
    g.display(Transform("cg 004", xysize=(1920, 1080)))
    g.display(Transform("cg 005", xysize=(1920, 1080)))

    g.button("sdcg_009")#江晚晴淋雨
    g.condition("renpy.seen_image('cg 006')")
    g.display(Transform("cg 006", xysize=(1920, 1080)))
    
    g.button("sdcg_001")#林曦告白
    g.condition("renpy.seen_image('cg 007')") #sdcg用这个判断条件，当看到这张图片时，解锁这个按钮
    g.display(Transform("cg 007", xysize=(1920, 1080))) #下面放差分
    g.display(Transform("cg 008", xysize=(1920, 1080)))
    g.display(Transform("cg 009", xysize=(1920, 1080)))
    g.display(Transform("cg 010", xysize=(1920, 1080)))
    g.display(Transform("cg 011", xysize=(1920, 1080)))
    g.display(Transform("cg 012", xysize=(1920, 1080)))
    g.display(Transform("cg 013", xysize=(1920, 1080)))

    g.button("sdcg_003")#诺提拉cg
    g.condition("renpy.seen_image('cg noctella_descend')")
    g.display(Transform("cg noctella_descend", xysize=(1920, 1080)))
    #g.display(Transform("sdcg 004", xysize=(1920, 1080)))
    #g.display(Transform("sdcg 005", xysize=(1920, 1080)))
    #g.display(Transform("sdcg 006", xysize=(1920, 1080)))
    #g.display(Transform("sdcg 007", xysize=(1920, 1080)))
    #g.display(Transform("sdcg 008", xysize=(1920, 1080)))
    #g.display(Transform("sdcg 009", xysize=(1920, 1080)))
    #g.display(Transform("sdcg 010", xysize=(1920, 1080)))

    

## 画廊中使用的图像的声明。如果你使用 Ren'Py 的
## 自动图像名称，可能需要也可能不需要。
#image cg 0001 = Transform("images/cg/001.avif", xysize=(config.screen_width, config.screen_height))
#image cg 0002 = Transform("images/cg/002.avif", xysize=(config.screen_width, config.screen_height))
#image cg 0003 = Transform("images/cg/003.avif", xysize=(config.screen_width, config.screen_height))
#image cg 0004 = Transform("images/cg/004.avif", xysize=(config.screen_width, config.screen_height))
#image cg 0005 = Transform("images/cg/005.avif", xysize=(config.screen_width, config.screen_height))
#image sdcg 0001 = Transform("images/sdcg/001.avif", xysize=(config.screen_width, config.screen_height))
#image sdcg 0002 = Transform("images/sdcg/002.avif", xysize=(config.screen_width, config.screen_height))
#image sdcg 0003 = Transform("images/sdcg/003.avif", xysize=(config.screen_width, config.screen_height))
#image sdcg 0004 = Transform("images/sdcg/004.avif", xysize=(config.screen_width, config.screen_height))
#image sdcg 0005 = Transform("images/sdcg/005.avif", xysize=(config.screen_width, config.screen_height))
#image sdcg 0006 = Transform("images/sdcg/006.avif", xysize=(config.screen_width, config.screen_height))
#image sdcg 0007 = Transform("images/sdcg/007.avif", xysize=(config.screen_width, config.screen_height))
#image sdcg 0008 = Transform("images/sdcg/008.avif", xysize=(config.screen_width, config.screen_height))
#image sdcg 0009 = Transform("images/sdcg/009.avif", xysize=(config.screen_width, config.screen_height))
#image sdcg 0010 = Transform("images/sdcg/010.avif", xysize=(config.screen_width, config.screen_height))


## 这只是按钮名称 + _thumb，以便更容易迭代
image xia_cg_1_thumb = Transform("images/cg/001.avif", xysize=gallery_thumb_size)
image ashwin_cg_1_thumb = Transform("images/sdcg/004.avif", xysize=gallery_thumb_size)
image zoran_cg_1_thumb = Transform("images/sdcg/019.avif", xysize=gallery_thumb_size)
image cg_004_thumb = Transform("images/sdcg/014.avif", xysize=gallery_thumb_size)
image cg_005_thumb = Transform("images/cg/004.avif", xysize=gallery_thumb_size)
image sdcg_001_thumb = Transform("images/cg/007.avif", xysize=gallery_thumb_size)
image sdcg_002_thumb = Transform("images/sdcg/002.avif", xysize=gallery_thumb_size)
image sdcg_003_thumb = Transform("images/cg/noctella_descend.webp", xysize=gallery_thumb_size)
image sdcg_004_thumb = Transform("images/sdcg/004.avif", xysize=gallery_thumb_size)
image sdcg_005_thumb = Transform("images/sdcg/005.avif", xysize=gallery_thumb_size)
#image sdcg_006_thumb = Transform("images/sdcg/006.avif", xysize=gallery_thumb_size)
image sdcg_007_thumb = Transform("images/sdcg/007.avif", xysize=gallery_thumb_size)
image sdcg_008_thumb = Transform("images/sdcg/008.avif", xysize=gallery_thumb_size)
image sdcg_009_thumb = Transform("images/cg/006.avif", xysize=gallery_thumb_size)
image sdcg_010_thumb = Transform("images/sdcg/010.avif", xysize=gallery_thumb_size)

screen gallery():

    tag menu

    add "gui/load_menu.png"
    add Transform("gui/title_gallery.png",align =(0.98,0.98))
    text "":
        # 页面级说明放在简单显示对象上，避免泄漏到画廊按钮和复合显示对象内部。
        extra_alt _("画廊页面。这里可以浏览已解锁和未解锁的鉴赏内容。按方向键切换控件。")
    default page = 0
    $ items_per_page = 9
    $ max_pages = (len(gallery_buttons) - 1) // items_per_page + 1
    $ start_index = page * items_per_page
    $ end_index = min(start_index + items_per_page, len(gallery_buttons))
    $ current_page_items = gallery_buttons[start_index:end_index]

    imagebutton:
        idle "gui/cancel_idle.png"
        hover "gui/cancel_hover.png"
        xalign 0.98
        yalign 0.02
        action Return()
        alt _("关闭鉴赏界面")

    use game_menu(_("Gallery"))
    key "mouseup_3" action Return() #右键返回


    fixed:
        style_prefix 'gal'
        ## 将画廊图像组织成网格
        grid 3 3:
            xoffset -220
            for btn in current_page_items:
                $ gallery_extra_alt = _("已解锁。") if g.buttons[btn].check_unlock() else _("未解锁。")
                $ gallery_alt = _("鉴赏项：[gallery_name]。[gallery_extra_alt]")
                add g.make_button(
                    btn,
                    "{}_thumb".format(btn),
                    alt=renpy.substitutions.substitute(gallery_alt, scope={
                        "gallery_name": gallery_button_alts.get(btn, btn),
                        "gallery_extra_alt": gallery_extra_alt,
                    })[0],
                )
            ## 如果你不使用循环，这将看起来像这样：
            # add g.make_button("button_name", "button_thumbnail.png")
            


    #hbox:
            #align (0.5, 0.95)
            #spacing 100

            #textbutton "< 上一页":
                #action SetScreenVariable("page", page - 1)
                #sensitive (page > 0) # 如果是第0页，按钮不可点

            #text "Page [page+1] / [max_pages]" yalign 0.5 color "#fff"

            #textbutton "下一页 >":
                #action SetScreenVariable("page", page + 1)
                #sensitive (page < max_pages - 1) # 如果是最后一页，按钮不可点
    hbox:
        align (0.5, 0.96) # 调整位置到屏幕底部中央
        spacing 150
        
        # 上一页
        textbutton "<":
            style "page_text" # 复用你之前的页码样式
            action SetScreenVariable("page", page - 1)
            sensitive (page > 0) 
            alt _("上一页")

        # 页码显示
        text "[page+1] / [max_pages]":
            yalign 0.5 
            color "#fff"
            size 20

        # 下一页
        textbutton ">":
            style "page_text"
            action SetScreenVariable("page", page + 1)
            sensitive (page < max_pages - 1)
            alt _("下一页")
transform cg_fullsize:
    xysize (1920, 1080) 
    anchor (0.5, 0.5)
    pos (0.5, 0.5)

style gal_fixed:
    yfill True
    xsize config.screen_width-420
    align (1.0, 0.5)

style gal_grid:
    align (0.5, 0.5)
    xsize config.screen_width-420
    ysize config.screen_height-200
    spacing 100

