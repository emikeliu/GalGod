## 载入和保存界面 #######################################################
##
## 这些界面负责让玩家保存游戏并再次载入。
## 由于它们几乎所有内容都相同，两者都是通过第三个界面 file_slots 来实现的。
##
## https://www.renpy.org/doc/html/screen_special.html#save
## https://www.renpy.org/doc/html/screen_special.html#load
init python:
    def save_dialogue_callback(d):
        current_text = getattr(store, "_last_say_what", "")

        if current_text:
            current_text = renpy.filter_text_tags(current_text, allow=[])
            
            # 如果字数超过 12 个字，我们在中间强行加一个换行符 \n
            if len(current_text) > 8:
                # 第一行：截取前 12 个字
                line1 = current_text[:8]
                # 第二行：截取第 13 到第 24 个字
                line2 = current_text[8:16]
                
                # 如果超过 24 个字，加上省略号
                if len(current_text) > 15:
                    line2 += "..."
                    
                # 将两行用换行符连起来
                current_text = line1 + "\n" + line2
        else:
            current_text = "（无对话）"

        d["dialogue_text"] = current_text

    config.save_json_callbacks.append(save_dialogue_callback)

    # 统一生成存档槽位的可见摘要与无障碍朗读文案。
    def build_slot_accessibility_text(display_prefix_str, spoken_prefix_str, dialogue_text, slot_time):
        if dialogue_text:
            full_content = display_prefix_str + dialogue_text.replace("\n", "")

            line1 = full_content[:8]
            line2 = full_content[8:16]

            if len(full_content) > 16:
                line2 = full_content[8:15] + "..."

            if line2:
                display_text = line1 + "\n" + line2
            else:
                display_text = line1

            spoken_text = spoken_prefix_str + dialogue_text.replace("\n", "")
            extra_alt = __("时间 [slot_time]。摘要 [spoken_text]")
            return display_text, renpy.substitutions.substitute(extra_alt, scope={
                "slot_time": slot_time,
                "spoken_text": spoken_text,
            })[0]

        extra_alt = __("时间 [slot_time]。空槽位。")
        return "", renpy.substitutions.substitute(extra_alt, scope={
            "slot_time": slot_time,
        })[0]


## 保存槽使用的缩略图的宽度和高度。
define config.thumbnail_width = 384
define config.thumbnail_height = 216


screen save():

    tag menu

    add "gui/load_menu.png" # 背景；可以是任何内容
    text "":
        # 页面级说明放在独立简单节点上，避免影响存档槽和复合容器。
        extra_alt _("保存页面。这里可以浏览分页并保存到槽位。按方向键切换控件。")
    imagebutton:
        idle "gui/cancel_idle.png"
        hover "gui/cancel_hover.png"
        xalign 0.98
        yalign 0.02
        action Return()
        alt _("关闭保存界面")
    add "gui/title_savemenu.png":
        xalign 0.01
        yalign 0.01

    use file_slots(_("Save"))


screen load():

    tag menu

    add "gui/load_menu.png" # 背景；可以是任何内容
    text "":
        # 页面级说明放在独立简单节点上，避免影响读档槽和复合容器。
        extra_alt _("读档页面。这里可以浏览分页并读取已有存档。按方向键切换控件。")
    imagebutton:
        idle "gui/cancel_idle.png"
        hover "gui/cancel_hover.png"
        xalign 0.98
        yalign 0.02
        action Return()
        alt _("关闭读取界面")
    add "gui/titlle_lloadmenu.png":
        xalign 0.01
        yalign 0.01

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(
        pattern=_("Page {}"), auto=_("Automatic saves"),
        quick=_("Quick saves"))
    # 获取当前所在页面（返回值为 "auto", "quick", "1", "2"...）
    use game_menu(title)
    $ current_pg = FileCurrentPage()

    # 1. 判断需要加什么前缀
    $ prefix_str = ""
    $ spoken_prefix_str = ""
    if current_pg == "auto":
        $ prefix_str = "[自动]"
        $ spoken_prefix_str = "自动存档。"
    elif current_pg == "quick":
        $ prefix_str = "[快速]"
        $ spoken_prefix_str = "快速存档。"

    # 2. 定义页面的先后顺序，用来处理 < 和 > 按钮
    $ page_order =[]
    if config.has_autosave:
        $ page_order.append("auto")
    if config.has_quicksave:
        $ page_order.append("quick")
    $ page_order.extend(["1", "2", "3"])

    # 找到当前页面在列表中的位置，计算出上一页和下一页的目标
    $ current_index = page_order.index(current_pg) if current_pg in page_order else 0
    $ prev_page = page_order[current_index - 1] if current_index > 0 else None
    $ next_page = page_order[current_index + 1] if current_index < len(page_order) - 1 else None

    # 统一生成分页按钮朗读文本，避免 alt 在焦点切换时再访问局部变量导致报错。
    $ page_name_map = {
        "auto": _("自动存档页"),
        "quick": _("快速存档页"),
        "1": _("第 1 页"),
        "2": _("第 2 页"),
        "3": _("第 3 页"),
    }
    $ current_page_message_map = {
        "auto": _("当前页：自动存档页"),
        "quick": _("当前页：快速存档页"),
        "1": _("当前页：第 1 页"),
        "2": _("当前页：第 2 页"),
        "3": _("当前页：第 3 页"),
    }
    

    fixed:
        xsize 1500 xalign 0.5
        ## 这确保输入框会在任何按钮之前获得回车事件。
        order_reverse True

        ## 页面名称，可以通过点击来编辑。
        ## 如果你想要的话，这可以很容易地被移除。
        ## 如果移除的话，别忘了同时移除顶部的 `default`。
        #button:
            #style "page_label"
            #key_events True
            #action page_name_value.Toggle()

            #input:
                #style "page_label_text"
                #value page_name_value

        ## 文件槽的网格。
        grid 2 3:
            style_prefix "slot"

            for i in range(2*3):
                $ slot = i + 1
                $ d_text = FileJson(slot, key="dialogue_text", empty="", missing="")
                $ slot_time = FileTime(slot, format=_("%Y/%m/%d %H:%M:%S"), empty=_("空槽位"))
                $ display_text, slot_extra_alt = build_slot_accessibility_text(prefix_str, spoken_prefix_str, d_text, slot_time)
                $ slot_alt = _("[title]槽位 [slot]。[slot_extra_alt]")

                button:
                    action FileAction(slot)
                    alt renpy.substitutions.substitute(slot_alt, scope={
                        "title": title,
                        "slot": slot,
                        "slot_extra_alt": slot_extra_alt,
                    })[0]
                    has vbox

                    hbox:
                        add FileScreenshot(slot):
                            xysize(160,90)
                            xalign 0.5
                            yalign 0.5
                            yoffset 23
                            xoffset 10
                            zoom 1.7
                            crop (42, 24, 300, 168)

                    ## https://www.fabriziomusacchio.com/blog/2021-08-15-strftime_Cheat_Sheet/
                    text FileTime(slot,
                            format=_("{#file_time}%Y/%m/%d , %H:%M:%S"),
                            empty=_("empty slot")):
                        style "slot_time_text"

                    text FileSaveName(slot):
                        style "slot_name_text" 
                        size 10
                    if d_text != "": 
                        # 如果不是空档位，则显示 前缀 + 文本
                        text "[display_text]":
                            style "slot_name_text" 
                            color "#ffffff"        
                    else:
                        # 空档位时什么都不显示（防止只出现一个【自动】）
                        text "":
                            style "slot_name_text"
                    #text FileJson(slot, key="dialogue_text", empty="", missing=""):
                            #style "slot_name_text" # 你可以自定义样式，例如 slot_dialogue_text
                            #color "#ffffff"        # 举例：设置灰色字体
                            #size 40               # 举例：设置较小的字号

                    # 这意味着玩家可以悬停在这个保存槽上
                    # 并按下删除键来删除它
                    key "save_delete" action FileDelete(slot)

        ## 访问其他页面的按钮。
        vbox:
            style_prefix "page"
            hbox:
                $ current_pg = FileCurrentPage()

                textbutton _("<") action ([FilePage(prev_page), Function(announce_accessibility_status, current_page_message_map.get(str(prev_page), _("当前页：未知页")))] if prev_page else None) style "page_text" sensitive (prev_page != None) alt (renpy.substitutions.substitute(_("上一页，前往[target_page]"), scope={"target_page": page_name_map.get(str(prev_page), _("未知页"))})[0] if prev_page else _("当前已经是第一页"))

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action [FilePage("auto"), Function(announce_accessibility_status, current_page_message_map["auto"])] style "page_text" alt _("自动存档页")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action [FilePage("quick"), Function(announce_accessibility_status, current_page_message_map["quick"])] style "page_text" alt _("快速存档页")

                ## range(1, 10) 给出从 1 到 9 的数字。
                for page in range(1, 4):
                    $ page_alt = renpy.substitutions.substitute(_("第 [page_number] 页"), scope={"page_number": page})[0]
                    $ page_action = [FilePage(page), Function(announce_accessibility_status, current_page_message_map[str(page)])]
                    textbutton "[page]" :
                        action page_action
                        style "page_text"
                        alt page_alt

                       
                textbutton _(">") action ([FilePage(next_page), Function(announce_accessibility_status, current_page_message_map.get(str(next_page), _("当前页：未知页")))] if next_page else None) style "page_text" sensitive (next_page != None) alt (renpy.substitutions.substitute(_("下一页，前往[target_page]"), scope={"target_page": page_name_map.get(str(next_page), _("未知页"))})[0] if next_page else _("当前已经是最后一页"))
                #spacing 20
                #textbutton _("<") action FilePagePrevious() style "page_text" sensitive (current_pg in ["2", "3"])

                #if config.has_autosave:
                    
                    #textbutton _("{#auto_page}A") action FilePage("auto") style "page_text"

                #if config.has_quicksave:
                    #textbutton _("{#quick_page}Q") action FilePage("quick") style "page_text"

                ## range(1, 10) 给出从 1 到 9 的数字。
                #for page in range(1, 4):
                    #textbutton "[page]" :
                        #action FilePage(page)
                        #style "page_text"

                #textbutton _(">") action FilePageNext() style "page_text" sensitive (current_pg in ["1", "2"])

            # if config.has_sync:
                # if CurrentScreenName() == "save":
                    # textbutton _("Upload Sync"):
                        # action UploadSync()
                # else:
                    # textbutton _("Download Sync"):
                        # action DownloadSync()


style page_label:
    xpadding 75
    ypadding 5
    xalign 0.5



style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color '#ff8335'

style slot_grid:
    xalign 0.5
    yalign 0.5
    spacing 5

style slot_time_text:
    size 20
    xoffset 315
    yoffset -42

style slot_vbox:
    spacing 12

style slot_button:
    xysize (587, 236)
    padding (15, 15, 15, 15)
    background "gui/peel_[prefix_]background.png"
    yalign 0.5
    xalign 0.2
    

style slot_button_text:
    size 21
    xalign 0.5
    idle_color '#aaaaaa'
    hover_color '#ff8335'
    selected_idle_color '#ffffff'

style page_hbox:
    xalign 0.5
    spacing 20

style page_vbox:
    xalign 0.5
    yalign 0.9
    spacing 0

style page_button:
    padding (15, 6, 15, 6)
    xalign 0.1
    background "gui/page_box_[prefix_]background.png"

style slot_name_text:
    xalign 0.7
    yalign 0.2
    xoffset 262
    size 25
    yoffset -180
    line_spacing 5

style page_text:
    xysize (51, 51)      # 强制固定宽度 51，高度 51
    padding (0, 0)       # 清除之前的内边距，防止撑开按钮
    
    background "gui/page_box_idle_background.png" 
    
    
    # 选中状态时的背景（在此处替换为你想要的选中图）
    selected_background "gui/page_box_hover_background.png" 
    yoffset 0
    xoffset 0
    
    # 鼠标悬停时的背景（可选）
    hover_background "gui/page_box_hover_background.png"
    #padding (15, 5, 5, 6)
style page_text_text:    # 专门控制按钮内文字的样式
    size 25              # 字体大小，51的框建议18-22左右
    color "#ffffff"
    align (0.5, 0.5)     # 核心：让文字在 51x51 的方框内水平垂直绝对居中
    text_align 0.5       # 多行文本时的居中（虽然这里只有1个数字）

style page_text_Q:
    size 10
    color "#ffffff"
    xoffset 10
    yoffset 1
    background "gui/page_box_idle_background.png" 
    
    # 选中状态时的背景（在此处替换为你想要的选中图）
    selected_background "gui/page_box_hover_background.png" 
    
    # 鼠标悬停时的背景（可选）
    hover_background "gui/page_box_hover_background.png"
    padding (15, 6,15, 6)
style page_text_selected:
    size 15
    color "#ffffff" 
    xoffset 0
    yoffset 1
    background "gui/page_box_idle_background.png" 
    padding (15, 6, 15, 6)
