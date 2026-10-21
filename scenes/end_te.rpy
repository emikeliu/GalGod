label end1:
    
    cz "小涟，我的愿望是……请赋予小涟一次选择的权利。"

    "我感受到了，小涟的气息，小涟的味道。"

    cz "让她自己决定，是作为一个独立的意识存在于此世，还是作为我们共同回忆的结晶，安然逝去。"

    "大抵是我的错觉吧，我看到高悬于天的神明，微微笑了一下。"

    "然后，"

    scene bg noctella_background with pixellate
    "消失了身影。"

    "就像从未存在过一般。"

    "我只是望着仅存月华的虚空，"
    "望着，望着。"
    "直到听见外界的声音。"

    stop music fadeout 1.0
    "直到再一次，听不见外界的声音。"

    scene bg heavenly_altar_focus with Dissolve(1.5)

    play music "audio/bgm/BGM_悲伤慈爱.ogg" loop fadein 1.0

    $ xl.show("温柔", pos=center)
    voice "cv3/xiaolian/xiaolian_0046.ogg"
    xl "………………嗯……"

    "不知何时起，她站在了我的旁边。"

    voice "cv3/xiaolian/xiaolian_0047.ogg"
    xl "这样，真的好吗？"

    "她可爱地歪着头，有点踌躇，我也只能耸耸肩。"

    cz "好不好我觉得不重要。"

    cz "重要的是，你想怎么做呢？"

    $ xl.show("卖萌气气")
    voice "cv3/xiaolian/xiaolian_0048.ogg"
    xl "难道，不是你在自说自话？\n我或许，只会说出你想听的话哦。"

    "我摇了摇头。"

    cz "本来是这样想的。"

    cz "现在不这么认为了。"

    "三年前的清辉，穿透过来。"

    "小涟的身体渐渐融入温柔的月光之中，似乎可以看到和少女的微笑重叠在一起。"

    $ xl.show("卖萌叹气")
    voice "cv3/xiaolian/xiaolian_0049.ogg"
    xl "以前都是我去让你选择的，现在居然是我来吗，你好坏。"

    cz "好像坏一点才有人喜欢啊，网上都是这么说。"

    $ xl.show("温柔")
    voice "cv3/xiaolian/xiaolian_0050.ogg"
    xl "你真的成长了好多好多，我感觉，都不需要我了，我在与不在，对你也没有太大的区别。"

    $ xl.show("卖萌叹气")
    voice "cv3/xiaolian/xiaolian_0051.ogg"
    xl "干脆就这样，让我消失不也挺好么。"

    cz "不管是让你存在也好，还是让你消失也好，我觉得，那都不是我该说的。"

    $ xl.show("卖萌疑惑")
    voice "cv3/xiaolian/xiaolian_0052.ogg"
    xl "可是，我是你创造的呀？"

    cz "真的吗？"

    $ xl.show("卖萌叹气")
    voice "cv3/xiaolian/xiaolian_0053.ogg"
    xl "……大概。"

    "或许是吧，但很明显，她也没多少底气。"

    cz "说起来，你以前可是很相信神明的，我都是听了你的意见，所以才下了决心，要借神明的力量，让大家都看到你。"

    cz "你为什么会这么相信呢？要知道，连我都不信的。"

    $ xl.show("温柔")
    voice "cv3/xiaolian/xiaolian_0054.ogg"
    xl "我一定是，被月光所迷惑了吧。"

    "……原来，是这样啊。"
    "我理解了。"

    "——那么，绝对，这样更好。"

    cz "回到正题，你想……怎么样呢？"

    voice "cv3/xiaolian/xiaolian_0055.ogg"
    xl "我吗，我……"

    "轻轻地，轻轻地，风吹过。"
    "温柔的夜风，裹着少女的眼泪，抚平了一切思念。"

    $ xl.show("抽泣")
    voice "cv3/xiaolian/xiaolian_0056.ogg"
    xl "嘶——我，呜，我……"

    "我只是微笑看着她。"

    "终于有一天，我也可以给予他人支撑了——"

    $ xl.show("抽泣")
    voice "cv3/xiaolian/xiaolian_0057.ogg"
    xl "咿，阿舟，嘶……"

    $ xl.hide(transition=None)
    $ xl_l.show("抽泣", transition=None)
    "她扑了过来。"

    voice "cv3/xiaolian/xiaolian_0058.ogg"
    xl "我不要……离开你…………"

    "时隔多日，再度感受到的柔软，让我简直要落下眼泪。"

    "小涟……你当然是我，重要的人。"

    "我就这样，被小涟抱着，亦步亦趋，挪动到了天选台的边上。"

    $ xl_l.hide()
    show bg heavenly_altar with dissolve

    play sound fx.crowd loop fadein 1.0
    "台下，传来了惊呼。"
    "而后，便是带着各种情绪的目光，向这边涌来。"
    "我们默默承受着。"

    "我是一个人上的天选台。"
    "这是理所当然的。"

    "他们本应看不到小涟。"
    "这也是理所当然的。"

    play sound fx.camera
    with flash
    pause 0.15

    play sound fx.camera
    with flash
    pause 0.15
    "闪光灯咔嚓作响。"

    "有这样的结果，自然……也就不奇怪了。"

    "我身边忽然出现的纯白少女让他们感到好奇，我甚至可以看到，许多人的目光都亮了起来。"

    "清纯、美丽、乖巧的小涟。"

    "有多么完美，我再清楚不过。"

    "呵，可惜，看来是不能独自欣赏小涟的可爱了。"

    "这之后，日子定然不会平静。"

    "不过——"

    "那些都是后话。"

    "今日，我看到了诺提拉，我不再害怕。"

    cz "{size=60}————我！{/size}"

    "压榨出身体里每一个细胞的力量，鼓起勇气，对着全世界喊道。"

    with vpunch
    cz "{size=60}喜欢小涟！{/size}"

    voice "cv3/xiaolian/xiaolian_0059.ogg"
    xl "唉？"

    "她也没能想到，会在当下，得到我爱的告白吧。"

    # （立绘出现）
    $ jwq.show("挺好颜", pos=right, x_offset=-250)
    voice "cv3/jiangwanqing/jiangwanqing_0129.ogg"
    jwq "啊，是吗……"

    "晚晴露出了一副解脱似的表情，她们在台下，靠近了过来，所以当然听到了我的宣告。"

    $ lx.show("哭哭", pos=left, x_offset=250)
    voice "cv3/linxi/linxi_0155.ogg"
    lx "呜呜——我又成败犬了……"

    "她们……真是各方面都截然相反的两个人呀……\n或许只有我清楚她们相近的地方吧。"
    "曦曦和晚晴的表情，就像是对不上的拼图似的，完全不一致。"

    "可惜，不方便拍下来了……"
    "不过没关系，你们想不到的，还在更后面呢——"

    play music "audio/bgm/BGM_欢快.ogg" loop fadein 0.5

    cz "{size=60}——林曦！{/size}"

    $ lx.show("惊讶")
    voice "cv3/linxi/linxi_0156.ogg"
    lx "唉——？"

    "我久违地喊出了她的全名，这就代表着，我是有如此的认真吧。"

    "你总是照耀着我，对我伸出手来，我还没有答复你呢……"

    "哪怕全世界都在看着，也无所谓。"

    cz "{size=60}我也最喜欢你了！你的告白，我答应了！{/size}"

    $ lx.act(anim_jump)
    $ lx.show("萌怒")
    $ jwq.show("落寞")
    voice "cv3/jiangwanqing/jiangwanqing_0130.ogg"
    jwq "嗯额？！"

    "江晚晴。"

    "你——"

    cz "{size=60}江晚晴，我放不下你，\n我希望，你能永远和我在一起！{/size}"

    "——也别跑。"


    $ jwq.show("尴尬")
    voice "cv3/jiangwanqing/jiangwanqing_0131.ogg"
    jwq "欸………………？"

    $ lx.show("无语")
    voice "cv3/linxi/linxi_0157.ogg"
    lx "…………哈？"

    $ xl.show("温柔")
    voice "cv3/xiaolian/xiaolian_0060.ogg"
    xl "哎呀哎呀……"

    "已经不需要再踌躇了！"
    play sound fx.camera
    with flash
    pause 0.15

    play sound fx.camera
    with flash
    pause 0.15
    "闪光灯疯狂照耀着，就连台下她们的身边，也给围上了长枪短炮。"

    cz "我喜欢小涟。"

    cz "然后，也喜欢曦曦。"

    cz "不知不觉起，晚晴也变得喜欢起来了！"

    "我堂堂正正地看向她们三个的脸。"

    cz "虽然按常理来说，只能选择一个吧！"

    cz "但是，正如我所说的！\n我一直喜欢着你们！！！"

    "我将双手张开，拥抱着整个世界，就宛如隔着空气，拥抱着她们。"

    "宣言道。"

    cz "我可不会谁都不选，留下一个，莫名其妙的开放结局！"

    "那是剧情作的做法。"

    "而我，作为萌作高手，也是钦定的萌萌人大圣——"

    menu:
        "全选":
            pass
        "全都要":
            pass
        "三个都要":
            pass
        "要创造全员幸福的结局！":
            pass
        "我说我他妈要全选你耳朵聋吗？":
            pass
    
    $ achievement.grant("ACH_07")
    $ achievement.sync()

    with vpunch
    $ xl.show("卖萌惊讶")
    cz "我并不是谁都不选，而是三个人，我全都要选！"

    with vpunch
    cz "你们都是我的翅膀！"

    with vpunch
    cz "在萌作里，全选，也是选择！！！"

    "她们听完我说的话，在震惊中互相对视，满脸不可置信。"

    "记者们一个个眼神喷出了精光来，用摄像机锁定着我们。"

    "台下的杂音，耳边的风声，携着微微凉意，化为絮状包裹住我。"

    "在掌中，在脚下，在环绕我的强光深处，情绪在鼓动、脉涌，向四方奔流。"

    "这早已超越了立誓的单纯，如同将自己切得四分五裂，再熔进空气，化为风暴席卷全场。"

    "星夜下，头脑十分清醒。"

    "我，无比认真！！！"

    $ lx.hide()
    $ jwq.hide()
    "接着……还是小涟，率先牵了牵我的衣角。"

    $ xl.hide()
    $ xl_l.show("害羞", pos=center)
    voice "cv3/xiaolian/xiaolian_0061.ogg"
    xl "那，那个……"

    "她羞红着脸，犹犹豫豫……我们是什么关系，有什么好害羞的。"

    cz "嗯！"

    "我只能点头回应，而等来的，则是这么一句——"

    voice "cv3/xiaolian/xiaolian_0062.ogg"
    xl "……我，我能，争取一下正妻嘛？"

    "她自斜下方瞅着我，这副谨小慎微、羞答答的模样，让人哑然失笑。"

    "想不到，你居然还有这种心思，我还以为你怎么都无所谓呢。"

    "真是……够可爱的。"

    "自曦曦和晚晴那边，也传来了动静。"

    "我已经做好觉悟了。"

    "就算你们拒绝我，我也要死皮赖脸地，去追上你们。"

    "就像你们，拼尽了全力向我伸出手一样。"

    stop music fadeout 1.0
    "将来的路途，定是布满荆棘。"

    "但是……"

    $ xl_l.hide()
    window hide
    $ quick_menu = False
    $ custom_ui = False

    show bg moon with Dissolve(2.0)
    play music "audio/bgm/BGM_月幕.ogg" loop fadein 1.5

    call screen centered_left_text("明月指引着我。")
    call screen centered_left_text("仅是这样，便已完全足够。")
    call screen centered_left_text("啊啊。")
    call screen centered_left_text("真是……十分美丽。")
    call screen centered_left_text("刚刚我所说的，绝不是应付场面的台词。")
    call screen centered_left_text("我不会重蹈覆辙。")
    call screen centered_left_text("必须好好展现我的意志。")
    call screen centered_left_text("——前进，为了让她们相信我，而竭尽全力。")
    call screen centered_left_text("“（真漂亮……）”")
    call screen centered_left_text("夜风吹过，清辉洒下。")
    call screen centered_left_text("我看向先前祂凭空而立的虚空。")
    call screen centered_left_text("苍色的天幕，带着分外神秘的魔力，将我吸引。")
    call screen centered_left_text("人的气息，车的声响，十分嘈杂。")
    call screen centered_left_text("但我却不可思议地，感受不到。")
    call screen centered_left_text("相反，能感受到的，唯有寂静。")
    call screen centered_left_text("宛如身处没有琴键敲响的音乐教室一般，无边的寂静。")
    call screen centered_left_text("遗世独立的天空分外从容，全然不见欲与他者比高的俗念，今晚依旧如故，清丽，澄澈。")
    call screen centered_left_text("我，站在这里。")
    call screen centered_left_text("诺提拉……神明的显圣，会给我带来一切。")
    call screen centered_left_text("在Galgame至上的世界里，我已经……站在了至高之巅。")
    call screen centered_left_text("但那些，我并不关心。")
    call screen centered_left_text("过去的回忆，未来的事情，寻常人为之困扰的，我正在思虑的……")
    call screen centered_left_text("在这月光下，通通被净化、洗涤。")
    call screen centered_left_text("我……感受到了灵魂层面的，颤栗。")
    call screen centered_left_text("——那是一轮金镜。")
    call screen centered_left_text("十分，")
    call screen centered_left_text("美丽。")
    call screen centered_left_text("只有神明的居所，")
    call screen centered_left_text("才会如此优雅。")
    call screen centered_left_text("“（说起来，诺提拉好可爱……）”")
    call screen centered_left_text("现在，祂是否仍投下视线，看着这一方小小世界呢。")
    call screen centered_left_text("“（啊……）”")
    call screen centered_left_text("我会永远记得那个身影吧。")
    call screen centered_left_text("因为，")
    call screen centered_left_text("我喜欢上了——")
    call screen centered_left_text("——这片月幕。")
    
    # 通关标识
    $ true_end_finish = True

    stop music fadeout 2.0
    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene black
    $ renpy.pause(1.0, hard=True)

    return