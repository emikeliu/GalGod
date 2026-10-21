
label scene_1_1:
    $ quick_menu = False
    $ custom_ui = False

    # 初始黑屏
    scene black
    play music "audio/bgm/BGM_月幕.ogg" loop fadein 1.0 volume 1.0

    # 隐藏对话框并显示开场文本
    window hide

    # 使用 at 调用变换，图片会花 5 秒从透明变不透明
    show bg moon at forced_dissolve(5.0)
    
    # 配合硬暂停锁定玩家操作
    $ renpy.pause(5.0, hard=True)

    # 开场
    call screen centered_left_text("月幕下，清辉洒落。")
    call screen centered_left_text("我躺倒在硬石地面上，感受不到冰凉。")
    call screen centered_left_text("覆于天穹的满月，带着分外神秘的魔力，将我吸引。")
    call screen centered_left_text("人的气息，车的声响，十分嘈杂。")
    call screen centered_left_text("但我却不可思议地，感受不到。")
    call screen centered_left_text("相反，能感受到的，唯有寂静。")
    call screen centered_left_text("宛如身处没有琴键敲响的音乐教室一般，无边的寂静。")
    call screen centered_left_text("遗世独立的天空分外从容，全然不见欲与他者比高的俗念，\n今晚依旧如故，清丽，澄澈。")
    call screen centered_left_text("我，为什么会倒在这里呢？")
    call screen centered_left_text("玉盘向我压下。")
    call screen centered_left_text("坠落……坠落着，向我靠近。")
    call screen centered_left_text("有种被吸了起来的错觉。")
    call screen centered_left_text("想要伸出双手，但是，手也好，脚也好，都不存在。")
    call screen centered_left_text("人，生而四肢俱在……\n不过，如果是月亮的决定，那么就没办法了。")
    call screen centered_left_text("过去的回忆，未来的事情，寻常人为之困扰的，我正在思虑的……")
    call screen centered_left_text("在这月光下，通通被净化、洗涤。")
    call screen centered_left_text("我……感受到了灵魂层面的，颤栗。")
    call screen centered_left_text("——那是一轮金镜。")
    call screen centered_left_text("十分，美丽。")
    call screen centered_left_text("正如今天的日子一般，想来，今天是个重要的日子。")
    call screen centered_left_text("啊啊，那一定是，神明的居所吧。")
    call screen centered_left_text("因为，我也将要前往神明之处。")
    call screen centered_left_text("天选试……")
    call screen centered_left_text("我要去那里，")
    call screen centered_left_text("——直面，")
    call screen centered_left_text("神明。")

    # 开场结束，开始渐隐效果
    scene black with Dissolve(2.0)
    stop music fadeout 2.0
    
    # 黑屏保持一秒
    pause 1.0

    window auto

    $ quick_menu = True
    $ custom_ui = True
    scene bg street1_1 with dissolve

    # （快乐的BGM）
    play music "audio/bgm/BGM_日常2.ogg" loop fadein 1.0

    "早晨，空气清爽，阳光美好，完美的上学好天气。"
    "虽然我并不想上学就是了，嗐……谁又会想呢。"
    "感觉不如玩Galgame。"

    # 林曦进场，根据语境是打招呼，用开心或微笑
    # 第一次显示指定位置 center
    $ lx.show("微笑", pos=center)

    voice "cv/linxi/linxi_0001.ogg"
    lx "哟，舟子，早上好~"

    cz "嘿？巧哈曦曦，说吧，你是不是在跟踪我，我们又不住一起，怎么天天能遇到你。"

    "林曦，我的好哥们，要说的话，我肯定比她妈更熟悉她。"
    "……当然，反过来估计也是。"

    # 林曦吐槽，切换表情：无语
    $ lx.show("无语")
    
    voice "cv/linxi/linxi_0002.ogg"
    lx "哎，孩子脑子被撞傻了。"
    voice "cv/linxi/linxi_0003.ogg"
    lx "连这种莫名其妙的话都说得出来，我们读的是一个学校，能碰到不是很正常吗。"

    cz "……无言以对。"
    cz "话说，我虽然被大运撞了，但是你懂的吧？我以前是体育生，所以我现在很正常，包括脑子。"

    # 欲言又止，对应配置里的 key
    $ lx.show("欲言又止")
    voice "cv/linxi/linxi_0004.ogg"
    lx "额——"

    "她一脸欲言又止的神情，像是在憋着什么，不得不说真是有点意思。"

    cz "啊哈哈哈哈哈！我的身体倍儿棒，头脑也是精神得很呐，今年天选试的身体健康项目，肯定没问题了！"

    # （白眼） -> 对应 key "白眼"
    $ lx.show("白眼")
    voice "cv/linxi/linxi_0005.ogg"
    lx "本来还是在和你开开玩笑，怎么说呢，额，现在，你的表现，已经让我深深地怀疑了。"
    voice "cv/linxi/linxi_0006.ogg"
    lx "陈舟啊，说句不好听的，你，脑子没问题吧……"

    cz "哼哼~"
    "我摆出一个自信且低调的微笑，单手托着下巴，摩挲了一番。"

    cz "唔唔……"
    "我犹豫了。"
    cz "大概？"

    # 再次白眼，或者保持
    $ lx.act(anim_shake) # 增加一个小动作表示无语的震动
    "她明显地白了我一眼。"

    voice "cv/linxi/linxi_0007.ogg"
    lx "好了好了，别给我在这整蛊了。"

    # 恢复笑容
    $ lx.show("开心")
    "只不过，在白了我一眼后她还是露出那一如既往的健康笑容。"
    "作为回应，我也对她扯了扯嘴角，心照不宣。"
    "在二人之间的微表情交流中，似乎一切都得到了充分沟通。"
    "果然啊，只有和曦曦在一起时，是最放松的。"

    $ lx.show("平静")
    voice "cv/linxi/linxi_0008.ogg"
    lx "哎，算了，我也早就释怀了。"

    cz "释怀什么？"

    voice "cv/linxi/linxi_0009.ogg"
    lx "你的……女友啊，嗯，你嘴巴里那个，最爱的人，小涟。"

    cz "哦~你在说她啊。"
    cz "小涟怎么了，怎么就释怀了，她可是很爱我的，我也是很爱她的，我们郎才女貌天生一对，还有谁能来反对？"

    # 皱着脸 -> 对应 key "鼓嘴气气" 或 "萌怒"
    $ lx.show("鼓嘴气气")
    voice "cv/linxi/linxi_0010.ogg"
    lx "……这不是反不反对的问题，而是…而是……"

    "少女皱着脸，总算是憋出来了想说的话。"

    # （>_<） -> 情绪激动，用 "萌怒" 并配合跳跃动作
    $ lx.show("萌怒")
    $ lx.act(anim_jump)
    voice "cv/linxi/linxi_0011.ogg"
    lx "而是……以Galgame里的女主作为女朋友，还交往什么的，太离谱了啦！！！"

    voice "cv/linxi/linxi_0012.ogg"
    lx "我都不知道该怎么吐槽了，啊，啊啊啊，不对不对，是我特喵的早就吐槽一百遍了，无槽可吐了！"
    
    # 稍微平复一点，或者是苦恼，这里用 "哭哭" 或者 "叹气" 来表现无力感
    $ lx.show("叹气")
    voice "cv/linxi/linxi_0013.ogg"
    lx "如果是别人，我真的可以和解的……但是，但是但是，你这样子，和Galgame里的女主谈恋爱，我可是过了好几年了，才和解，才释怀呀！"

    cz "有、有这么离谱么……"
    "话说，我的曦曦啊，你这不是在张嘴说胡话吗，我看你这可完全不像释怀的样子！！"

    voice "cv/linxi/linxi_0014.ogg"
    lx "哈——呼、呼呼。"
    
    # 脸红气喘 -> 对应 "害羞" (因为没有专门的累表情，害羞通常带红晕)
    $ lx.show("害羞")
    "林曦深呼吸了几口，这样子气喘吁吁的、红红的脸，平时可不怎么见得到。"
    "我都想拍个照了，放在以后拿出来给她看，偷袭一番，肯定又能创造出难得的回忆。"
    "啧啧，可惜了，要是现在提出这一茬，八成得被她打。"

    cz "额，咳咳，我的目标，可是成为Galgame领域大神。"

    # （白眼）
    $ lx.show("白眼")
    voice "cv/linxi/linxi_0015.ogg"
    lx "………………"

    cz "所以——把Galgame中的女主角当做相伴一生的伴侣，有什么可疑惑的？其他人做得到吗！"
    "我理直气壮！"

    # （无奈） -> 对应 "无语"
    $ lx.show("无语")
    voice "cv/linxi/linxi_0016.ogg"
    lx "信了，我真的信了。"
    voice "cv/linxi/linxi_0017.ogg"
    lx "饶了我吧，别在我面前，提你的脑内女友了……"

    cz "什么脑内女友，我不许你侮辱我的爱人，我们之间，可是真心相爱的……而且，她也很可爱，就是你不理解而已……"
    
    $ lx.show("平静")
    voice "cv/linxi/linxi_0018.ogg"
    lx "好好好，你说什么都是。"

    "我嘟嘟囔囔，同她一起行走于脚下再平凡不过的上学路。"
    "哼，什么脑内女友不脑内女友的……"
    "你们懂什么，就算是虚幻角色，也是可以去爱的，也是有爱人的能力的。"
    "在一路的打闹中，就这样，我们靠近了学校。"
    
    
    # 切换到 street2 模拟走到另一条街
    scene bg street2_1 with dissolve

    "……"
    
    # （音效：吵吵闹闹）
    play sound fx.crowd loop 

    "在我们走到离学校只剩一条街的地方，人群涌动。"
    "好像是在做什么展出？演讲？"

    cz "那边好热闹，什么情况？"

    "我们天天上学，基本上很少在早晨见到这种场景，不但有人群，还有一些布置起来的台面、警戒线、保安之类的。"

    $ lx.show("惊讶")
    voice "cv/linxi/linxi_0019.ogg"
    lx "哎？不是吧，你这都不知道？"

    cz "你了解我的……我在家里，一直在准备。"

    "见我这么说，她很明显地叹了一口气。"
    
    # 严肃话题开始，准备切BGM
    # 叹气 -> 忧伤
    $ lx.show("叹气")
    voice "cv/linxi/linxi_0020.ogg"
    lx "该怎么说你呢，舟子，我也不想打击你，而是真的，真的……我不想看到你…浪费宝贵的生命。"

    # （嘈杂声渐隐）
    stop sound fadeout 1.0

    # 切换忧伤BGM
    play music "audio/bgm/BGM_忧郁.ogg" loop fadein 2.0

    # （低沉） -> 忧伤
    $ lx.show("忧伤")
    voice "cv/linxi/linxi_0021.ogg"
    lx "更不想看到你，事后痛苦……"

    "她的声音不知何时起，从朋友间的玩闹，变为了十分温柔的磁性声音，那是我最好的朋友……林曦的真正声音。"
    "正因如此，我才绝不能打着哈哈，逃避这个对话。"
    "沉默了一会儿，我回答道。"

    cz "是，我这些年，一直都在准备，在准备……天选试。"
    cz "之前也说过无数遍了，况且，你去我家的次数不少吧？应该见过的，我努力的样子。"
    cz "对吧，你应是最清楚不过的。"

    voice "cv/linxi/linxi_0022.ogg"
    lx "嗯，我很清楚。"
    "她轻轻地咬了咬嘴唇，脸上划过一丝不安。"

    $ lx.show("欲言又止")
    voice "cv/linxi/linxi_0023.ogg"
    lx "真的，真的真的，不放弃吗？"

    # （摇头嗯嗯） -> 动作：act(anim_shake) + 表情：平静带怒(或严肃)
    # 这里用 "平静" 比较合适，因为她在认真思考
    $ lx.show("平静")
    $ lx.act(anim_shake) 
    
    voice "cv/linxi/linxi_0024.ogg"
    lx "……不，不对，不是这个意思，我其实想说，正是因为，是天选试……我才想说的，你，陈舟，你真的，要去做那件事，没有任何回旋余地了？"
    voice "cv/linxi/linxi_0025.ogg"
    lx "连高考都不考了？"

    cz "嗯，我不高考了。"

    "高考？开什么玩笑？！"
    "我提起音量，大叫出声。"

    # （嘈杂声出来）
    play sound fx.crowd loop fadein 1.0
    play music "audio/bgm/BGM_欢快.ogg" loop

    with vpunch
    play sound fx.deng
    $ lx.show("惊讶")
    cz "高考哪里有玩Galgame重要！！"

    "身边走过的路人惊恐看来！"

    cz "我啊，我天天回家就是玩Galgame，事到如今，已经回不了头了！"

    "像是被我的气势慑住了，曦曦她，听到我的觉悟只是喉头滚动，没能说出话来。"

    cz "你知道的吧？肯定清楚，毕竟这可是常识，要玩Galgame，才能成为人上人！"

    "少女皱着眉，咬着牙看了我几眼后，她这才像是放弃了一般，散去了眉间的褶皱。"

    # （有点不服） -> 鼓嘴气气 -> 然后转为 平静
    $ lx.show("鼓嘴气气")
    voice "cv/linxi/linxi_0026.ogg"
    lx "唔……"
    
    $ lx.show("平静")
    voice "cv/linxi/linxi_0027.ogg"
    lx "嗯……好啦好啦，我会支持你的啦。"
    voice "cv/linxi/linxi_0028.ogg"
    lx "也只有我会管你了，唉，怎么就做了你这猪头的青梅，真是天杀的孽缘……"

    cz "谢谢你，我最好的兄弟。"

    $ lx.show("忧伤")
    voice "cv/linxi/linxi_0029.ogg"
    lx "……"
    "她的眼底晦暗了一阵，可能是我的错觉。"

    voice "cv/linxi/linxi_0030.ogg"
    lx "天选试，可是很残酷的哦，你要做好心理准备。"
    voice "cv/linxi/linxi_0031.ogg"
    lx "毕竟，那可是Galgame啊，你比我更了解，那是多么高级……多么，上流的，贵族的文化……"

    cz "啊啊，毕竟是第一艺术，我心里门清呢，早就做好思想建设了。"
    
    # 严肃的讨论
    $ lx.show("平静")
    voice "cv/linxi/linxi_0032.ogg"
    lx "区分一个文盲最简单的方式，就是看他了不了解Galgame。"
    "她的声音带着一丝苦涩，对于Galgame……她既没有兴趣，也没有才能。"

    voice "cv/linxi/linxi_0033.1.ogg"
    lx "擅长的，必是人中龙凤。"
    voice "cv/linxi/linxi_0033.ogg"
    lx "能从Galgame玩家中脱颖而出的人，既有人文情怀也有雷霆手段，温柔如歌，雷霆如刀……在商业中纵横睥睨，在政治上叱咤四方。"
    voice "cv/linxi/linxi_0034.ogg"
    lx "教科书里都是这么说的，大家都懂得呀……"

    cz "当然，我懂，所以我才去玩Galgame。"
    cz "权利、财富、人脉、名声，在你玩Galgame，脱颖而出的那一刻起，就向你涌来了，我从未见过，擅长Galgame却活在底层的人。"

    voice "cv/linxi/linxi_0035.ogg"
    lx "我们九年义务教育，都在教学Galgame的知识，天选试……可是那个，挑选出最擅长Galgame之人的舞台。"
    voice "cv/linxi/linxi_0036.ogg"
    lx "不玩Galgame的，做普通职业，平凡一生；玩Galgame的，升官发财，当企业高管，这个世界不就是这样的么。"
    voice "cv/linxi/linxi_0037.ogg"
    lx "你面对的竞争，可比高考严重多了。"
    voice "cv/linxi/linxi_0038.ogg"
    lx "那是…属于天之骄子的世界。"

    "她嘴里说出的话，我心中无比了然，也深感认同。"
    "国家自古以来，就建立了“天选试”制度，旨在由中央直接挑选能担任政治大任的高级人才，每3年一次，一次1000人。"
    "天选试中，全都是Galgame相关考核。"
    "通过者们，掌握的是制定规则、影响国运的权力。"
    "万般皆下品，惟有旮旯高。一个亿万富翁，在一个20来岁的、擅长Galgame的“天选之子”面前，也会自觉矮上一头！"
    "这哪怕放在整个世界上，也是最为神圣、最为残酷的测试！"
    "初试，统一命题，全国只有几万人能通过。"
    "省级考核，是综合素质评估，由真正的天选之子进行面试，这一道后，只会剩下3000~5000人。"
    "而殿试……则是天才与精英之间的较量。"
    "1000人，残酷，血腥。"
    cz "三年一次么……"
    "——这个目标，我，要实现。"
    "一定。"

    cz "再说，我也不是为了什么金钱，权利。"
    cz "我是为了爱……爱！而爱的力量是无穷的，Galgame里都是这么说的！"

    # （长叹） -> 叹气 + 摇头(shake)
    $ lx.show("叹气")
    $ lx.act(anim_shake)
    voice "cv/linxi/linxi_0039.ogg"
    lx "哎——"
    voice "cv/linxi/linxi_0040.ogg"
    lx "我说啊，要是你是为了升官发财倒还好了。"
    voice "cv/linxi/linxi_0041.ogg"
    lx "偏偏为了那个小涟，我估计往前推个两三百年，也没有什么人是抱着这么奇怪的目的，去参加天选试……"
    voice "cv/linxi/linxi_0042.ogg"
    lx "该说你是深情呢，还是该说你病得不轻呢。"

    "她摇了摇头，拿出一副放不下我的样子，再度向我展现笑颜。"

    # （轻快） -> 微笑
    $ lx.show("微笑")
    play music "audio/bgm/BGM_日常6.ogg" loop fadeout 1.0 fadein 1.0

    voice "cv/linxi/linxi_0043.ogg"
    lx "算了，当我没说，论起魔怔，你是一等一的。"
    voice "cv/linxi/linxi_0044.ogg"
    lx "你放心，我会一直陪着你的……一直。"

    cz "那是自然，你看着就是了，我一定会让小涟……"

    # === 政客演讲场景 ===
    $ lx.hide()

    show sdcg 001 with dissolve

    voice "cv/zhengke/zhengke_0001.ogg"
    zhengke "在这里，我想和大家说一件事！"

    "唉？我们聊着说着，之前看到的吵吵嚷嚷的地方好像开始了，有人在演讲。"

    show sdcg 002 with dissolve
    voice "cv/zhengke/zhengke_0002.ogg"
    zhengke "我作为省里干部的一员，对于现在省里的情况，十分痛心！"

    
    cz "……原来是当官的，没意思，曦曦，我们走吧。"
    "估计又是要讲一些无关痛痒的车轱辘话。"

    voice "cv/linxi/linxi_0045.ogg"
    lx "你不知道吗？他很出名的，毕竟，他是Galgame领域大神。"

    # 演出：主角立刻回头，可以使用一个 震动屏幕 或者 快速切换
    with vpunch # 简单的原生震动
    "我噌噌两步马上退了回来。"

    cz "是Galgame领域大神？这下不得不听了。"

    "只有顺利通过省级考核的天才人物，才能成为Galgame领域大神！"
    "哪怕他们没有斩获最终的殿试，也已经能站在无数人的头顶，获得巨大的能量。"
    "果然，他和那些普通官员的气质不同，眼前的人，十分年轻。"
    "身上肌肉的轮廓宛如雕塑，能透出正装，呈现出美丽的线条。"
    "能在这种年龄就当上实权高官，还具备如此的龙虎姿容，毫无疑问，是玩Galgame的功劳，我相信他的话语值得一听。"

    voice "cv/zhengke/zhengke_0003.ogg"
    zhengke "每三年一度的天选试，马上就要开始了！"
    
    # 模拟闪光灯
    play sound fx.camera
    with flash
    pause 0.15
    "记者们的长枪短炮咔咔闪烁。"

    show sdcg 001 with dissolve
    voice "cv/zhengke/zhengke_0004.ogg"
    zhengke "大家心里清楚，我们作为中部省份，去年，在最终选定的名额上，还是落后于那些经济大省。"

    "他停顿了一下，目光扫过全场，让这句话在每一个听众心中沉淀，空气中弥漫着一种熟悉的不甘。"

    show sdcg 002 with dissolve
    voice "cv/zhengke/zhengke_0005.ogg"
    zhengke "为什么会这样？"
    voice "cv/zhengke/zhengke_0006.ogg"
    zhengke "我们输了吗？我们输了吗？{size=+10}不，我们没有！{/size}我们输掉的，只是几个冰冷冷的数字！但我们没有输掉我们的志气，更没有输掉我们的才华与汗水！"
    voice "cv/zhengke/zhengke_0007.ogg"
    zhengke "我们的孩子，玩的旮旯Game，不比任何人少！"
    voice "cv/zhengke/zhengke_0008.ogg"
    zhengke "可是，为什么？为什么我们贡献了这么多的粮食，给沿海城市贡献了最庞大的劳动力，守护着整个国家的「天下之中」，可我们的孩子在「天选」这条起跑线上，却好像天生就比别人矮了一头？！"

    play sound fx.camera
    with flash
    pause 0.15

    play sound fx.camera
    with flash
    pause 0.15
    "闪光灯疯狂开闭！"
    "人群随之涌动起来……我的胸中，也荡起了阵阵涟漪。"
    "3年前的遗憾，今年，我，想要弥补。"
    "每个省份的名额，是重中之重，所谓的终极名额，会关联到更前面的测试通过率，能多一个，我就多一份机会。"
    "今年的具体分配，应该还没下来吧，再过不久，天选试就要开始了。"
    "到底会如何……"

    show sdcg 001 with dissolve
    voice "cv/zhengke/zhengke_0009.ogg"
    zhengke "我们不是要抢别人的饭碗，我们是要争一个更公平的机会！\n我们要求，在天选试的名额分配上，必须充分考虑历史贡献与战略定力，而不仅仅是经济增速！"
    "他侧过身，仿佛在指向无形的对手，又像是在向全场的民众和媒体勾勒一幅蓝图。"
    hide sdcg with dissolve


    # 切回林曦，表情：平静
    $ lx.show("平静")
    voice "cv/linxi/linxi_0046.ogg"
    lx "果然啊，今年的前奏已经开始了。"
    voice "cv/linxi/linxi_0047.ogg"
    lx "虽然这和我们……和我们绝大多数人没有关系就是了。"

    "几乎没有哪个孩子的父母，会在孩子出生时，就考虑到，说，要让自己的子女获得诺贝尔奖，或者奥运冠军。"
    "天选试亦同。"
    "它和绝大多数人没有任何关系，通常不作为家长、教师们会考虑到的目标。"
    "可就算如此，它的机制还是会在媒体、在高天、在日常的方方面面中渗透而入。"
    "只有那些拥有顶级资源、天生智商超群，Galgame感受力拔尖的存在，方可一窥门径。"
    "平凡人们，只要高考，上大学，然后工作，娶妻生子即可。"

    voice "cv/zhengke/zhengke_0010.ogg"

    zhengke "我将亲自带队，赴京陈情！把我们的诉求，把我们孩子的优秀，把我们全省的决心，直接摆在决策者的案头！请大家前往我们政府官网，留下你们宝贵的名字！"

    "林曦望着那边，瞳中覆着半层疏离，她看着那位演讲者，像是在看天上的星。"
    "但是，我发现了……"
    "作为她从小玩到大的好兄弟，我可以窥见到，寄宿于她眼底的神圣、追求、认命……还有一丝解脱。"

    cz "我们走吧。"

    voice "cv/linxi/linxi_0048.ogg"
    lx "嗯。"

    cz "对了，还得麻烦你帮个忙，和我一起，到时候去官网给他签个字。"

    # 恢复笑容
    $ lx.show("微笑")
    voice "cv/linxi/linxi_0049.ogg"
    lx "嘿嘿，小事一桩。"

    cz "还有点时间，咱们慢慢走。"

    "我们很快整理好了心情，无论什么事情发生……都无法，动摇我的决意。"
    "天选试，势在必得。"
    "一切……都是为了小涟。"

    $ achievement.grant("ACH_01")
    $ achievement.sync()
    # 本场结束，大幕关闭
    stop music fadeout 2.0

    show cinematic_black_overlay
    
    # 这里的硬暂停时间必须等于上面 linear 的时间
    $ renpy.pause(2.0, hard=True)
    
    # 此时已经彻底黑屏了
    scene black # 清理掉背景和刚才的覆盖层
    
    $ renpy.pause(1.0, hard=True) # 黑屏后再额外多等 1 秒（也是强制的）
    
    # 结束本章
    return