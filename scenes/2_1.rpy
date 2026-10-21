# 定义临时路人角色
define xy_a = Character("校友A")
define xy_b = Character("校友B")
define xy_c = Character("校友C")
define ty_a = Character("健壮男生")


label scene_2_1:

    # ================= 场景：街道-白天 =================
    scene bg street1_1 with dissolve
    play music "audio/bgm/BGM_日常5.ogg" fadein 1.0

    "我住的地方离学校没那么远，只需要步行20分钟就能到达。"
    "新的一天，阳光明媚，空气清新。"
    "很舒适安稳的一天……大概……"

    $ lx.show("萌怒", pos=left, x_offset=250)
    $ lx.act(anim_jump)
    voice "cv2/linxi/linxi_0001.ogg"
    lx "唔哇！啊！你为什么会在这里，不要打扰我们平时的上学时光啊——！"

    $ jwq.show("游刃有余", pos=right, x_offset=-250)
    voice "cv2/jiangwanqing/jiangwanqing_0001.ogg"
    jwq "哎呀哎呀，不过是偶然碰见了，所以同你们顺道而已，有必要这么大的反应么。"

    voice "cv2/linxi/linxi_0002.ogg"
    lx "偶然你个大头鬼！\n我可全都看到了，你明明是一大早就在必经之路上蹲点，一看到我们径直就往这儿走！"

    $ jwq.show("微笑")
    voice "cv2/jiangwanqing/jiangwanqing_0002.ogg"
    jwq "什么~原来在你看来是这样吗？在我的视角里可不是这样的哦。"

    cz "……"
    "好吵。"

    $ lx.show("平静带怒")
    voice "cv2/linxi/linxi_0003.ogg"
    lx "你该不会想，以后天天都来打扰我们吧！"

    voice "cv2/jiangwanqing/jiangwanqing_0003.ogg"
    jwq "呵呵呵，什么打扰不打扰的，说得真不好听。\n你为什么这么在意这个？难道我加入会有什么不方便的吗？"

    $ lx.show("鼓嘴气气")
    voice "cv2/linxi/linxi_0004.ogg"
    lx "………………咕咕咕。"

    voice "cv2/jiangwanqing/jiangwanqing_0004.ogg"
    jwq "阿舟应该也不介意吧？"
    voice "cv2/jiangwanqing/jiangwanqing_0005.ogg"
    jwq "毕竟……我看，你们也不是那种氛围啊，没有那种，打扰了你们二人世界的说法吧。"

    cz "哦，我是无所谓。"

    "见到同学，顺路一起走走又不是什么稀奇事，以前也不少，无所谓了，我觉得曦曦也犯不着这么抗拒。"

    $ lx.show("忧伤")
    voice "cv2/linxi/linxi_0005.ogg"
    lx "你以后……该不会每天都要……"

    $ jwq.show("游刃有余")
    voice "cv2/jiangwanqing/jiangwanqing_0006.ogg"
    jwq "谁知道呢，大家每天都要上学，偶尔碰到也是难免~"

    "真是难得，曦曦的表情变幻莫测，简直就是生动两个字的实体化身，看着感觉真好玩，好想给她记录下来。"
    "我在旁边看着是挺乐呵的。"
    "她们两个女孩子打打闹闹，我也不会觉得无聊，结果是，我们一行人不知不觉就走到了学校里。"

    # ================= 场景：校内-白天 =================
    scene bg school1 with fade
    play sound fx.crowd loop fadein 1.0

    voice "cv2/others/xiaoyoua_0001.ogg"
    xy_a "唉，那个，不是江晚晴吗。"
    voice "cv2/others/xiaoyoub_0001.ogg"
    xy_b "她怎么和……"
    voice "cv2/others/xiaoyoua_0002.ogg"
    xy_a "昨天的那个传闻，是真的！？一入学就表白什么的。"
    voice "cv2/others/xiaoyouc.ogg"
    xy_c "呜呜……什么鬼啊，怎么我校校花刚一入学，就已经贴到别人身上去了。"
    voice "cv2/others/xiaoyoub_0002.ogg"
    xy_b "看这情况，真的不能再真，一眼顶真了啊……"

    "窸窸窣窣的声音从四周传来。"

    $ jwq.show("微笑", pos=center, x_offset=0, zoom=2, transition=dissolve, y_offset=2100)
    voice "cv2/jiangwanqing/jiangwanqing_0007.ogg"
    jwq "~~~♪"

    "而少女却一副什么都没听见的样子，自顾自地就贴在我的身边走。"
    "喂，开什么玩笑，这不全是你的锅吗？怎么一点表示都没，好歹澄清一下，我上学可不是为了当观赏动物的。"

    cz "你是不是，贴得太近了……"
    "我时不时能感受到，两人衣服偶然碰到的纤维材质感，有点痒痒的。"

    $ jwq.show("平静")
    voice "cv2/jiangwanqing/jiangwanqing_0008.ogg"
    jwq "哦？是吗？那我靠远一点。"

    cz "……"
    cz "…………"
    "哎？靠远了么？这是靠远了么？还是因为我没注意，其实已经靠远了一些？"
    "就在我感到诧异之时，忽然间，自腰际又传来一种轻轻的拉扯触感，像是小动物在抚摸。"
    "我向旁边望去。"

    $ jwq.hide()
    $ lx.show("害羞", pos=center, x_offset=0, zoom=2, transition=dissolve,  y_offset=1900)
    voice "cv2/linxi/linxi_0006.ogg"
    lx "……"

    "她的脸红红的，而更令我在意的是她的行为。"
    "居然在牵着我的衣角？这又是在搞什么飞机？"

    cz "曦曦？"

    $ lx.show("忧伤")
    voice "cv2/linxi/linxi_0007.ogg"
    lx "……嗯。"

    "她抬着眼向上看来，带着点委屈，身子微微前倾，我仿佛能透过她的瞳孔看到自己的脸庞。"
    "被这样一双眼睛注视后，我甚至感觉自己脸上温度都高了不少，遂赶紧地转过身子去。"
    "……爱怎样怎样吧，这一大早，全都莫名其妙的。"

    cz "那个，江晚晴同学……"
    
    $ lx.hide()
    $ jwq.show("游刃有余", pos=center, x_offset=0, zoom=2, transition=dissolve, y_offset=2100)
    voice "cv2/jiangwanqing/jiangwanqing_0009.ogg"
    jwq "可以叫我晚晴哦，阿舟。"

    cz "不是不是不是，我们还没那么熟吧？？？话说你为什么这么自来熟的叫我阿舟啊！"

    $ jwq.show("微笑")
    voice "cv2/jiangwanqing/jiangwanqing_0010.ogg"
    jwq "哦这样啊，那就从现在开始变得熟起来吧，来，你先试试，叫我晚晴。"

    cz "额……敬谢不敏。"
    "这女人也太自来熟了吧！？？"
    "真这么叫的话，被人听见了，指不定我要被套进麻袋打。"
    
    $ jwq.show("计划通", zoom=1, pos=left, x_offset=150, y_offset=0)
    $ lx.show("白眼", zoom=1, pos=right, x_offset=-250, y_offset=0)

    voice "cv2/linxi/linxi_0008.ogg"
    lx "呿，呿，没看到人家很困扰吗？你靠得这么近，引过来这么多目光，已经耽误到陈舟的正常生活了，离远点离远点。"
    voice "cv2/jiangwanqing/jiangwanqing_0011.ogg"
    jwq "哎呀，我可不想被你这么说，幼儿园里不认路只能牵着别人衣角的小宝宝。"

    "我不由得加快了脚步。"

    # ================= 场景：切换场景（教学楼前） =================
    stop sound fadeout 1.0
    scene bg school2 with pushleft

    "这俩人亦步亦趋地跟着我，越靠近教学楼，周围的视线就越来越多，密密麻麻，四面八方。"
    "如果眼神能带有能量的话，我现在身上所聚集的能量毫无疑问能在一分钟内把手机的电充满，哪怕是我，都诞生出了些微的心慌慌之意。"
    "这，就是所谓“天选之子”的影响力么，哪怕是预备的……"

    cz "那个，江晚晴同学。你不是说，能辅导我天选试？具体需要我做什么？"
    "算了，别的想那么多也没用，我最关心的，果然还是这个。"

    $ jwq.show("游刃有余", pos=center, x_offset=0)
    voice "cv2/jiangwanqing/jiangwanqing_0012.ogg"
    jwq "什么都不需要做哦，我只要，能在这阵短暂的时光里，待在你身边就够了。"

    cz "嗯，在观察我研究我的意义上，我还是能够理解的……\n不过，我主要想问的是……那个，你什么时候辅导我。"
    "我也清楚这话有多不要脸，所以说出口也是说得结结巴巴的。"
    "明明我还什么都没干，就敢让这位高贵的少女，来莅临辅导……\n人家可是一秒钟几万元上下的存在，虽然我没亲眼见到她多有钱，但电视剧里都这么说的。"
    "而且本质上是我受恩于她，可我的身上却完全没有什么能够报答。"

    $ jwq.show("平静")
    voice "cv2/jiangwanqing/jiangwanqing_0013.ogg"
    jwq "辅导啊，我待会就准备告诉你……"

    "而就在我们好好走着，已经经过操场，靠近了教学楼时，一个意外之客打断了我们的交流。"
    stop music fadeout 1.0
    stop sound fadeout 1.0
    $ jwq.hide()
    
    show ty_a shadow:
        zoom 0.6
        xalign 0.5
        yalign -0.1
    voice "cv2/others/tiyushenga_0001.ogg"
    ty_a "陈舟？喂，兄弟，你就是陈舟吧。"

    "男人身姿挺拔，站在了我的前边，看相貌，应该是同龄人吧，是别的班的？我不由得停了下来。"

    cz "嗯？我是，有什么事。"

    "他的身材壮实，体格比我更高一点，一身运动装束，目光相当平静，并没有咄咄逼人的感觉，而是依着一种特别的轨迹打量，从我一左一右两个少女的脸上闪过，仅仅停留了一瞬，就滞留在了我的身上。"
    "在我观察着他的同时，他必然也在分析我，肌肉、体格、眼神、气质，综合成第一印象，这是雄性生物的动物性本能。"
    "我不卑不亢地对视了回去。"

    voice "cv2/others/tiyushenga_0002.ogg"
    ty_a "嗯……不错，我听说，我们学校有个了不得的人物，看来所言非虚。"

    cz "是在说我？可能是误会吧，我就是个普通人。"

    "他咧嘴一笑。"

    voice "cv2/others/tiyushenga_0003.ogg"
    ty_a "我看不像。"

    "好吧，那我也没办法，毕竟我的目标是天选试，比常规意义上的普通人要更优秀一点的自觉，当然是有的。"
    "我只能耸耸肩，不置可否。"

    voice "cv2/others/tiyushenga_0004.ogg"
    ty_a "能让那个江晚晴跟在身边的，我想绝对不是一般人，这么一见，果然如此，所以，我就开门见山的说了。"
    "奶奶的，江晚晴啊江晚晴，看看你惹的祸。"

    voice "cv2/others/tiyushenga_0005.ogg"
    ty_a "我会参加天选试。"

    cz "嗯……然后呢。"

    "居然是想参加天选试的？没想到我们学校里居然还有这种人。"

    play music "audio/bgm/BGM_欢快2.ogg" fadein 1.0
    voice "cv2/others/tiyushenga_0006.ogg"
    ty_a "你知道的，将参加天选试当做目标的人，都是寂寞的。"

    cz "……"
    cz "唉？是这样？"
    "震惊！"
    "我怎么完全没有这个感觉？"
    "明明一回家就有软软香香甜甜的小女友在等我，每天都动力拉满了，感觉前途一片光明，未来可期，怎么可能会寂寞。"

    voice "cv2/others/tiyushenga_0007.ogg"
    ty_a "我一直渴望着，同类之间有价值的交流…但是，这个学校里的人，太无聊了。"
    voice "cv2/others/tiyushenga_0008.ogg"
    ty_a "只是没想到，原来还有你这样一位高手。"
    voice "cv2/others/tiyushenga_0009.ogg"
    ty_a "所以，陈舟，我们来决斗吧。"

    cz "曦曦我们走。"

    $ lx.show("平静", pos=right, zoom=0.6, y_offset=-700)
    voice "cv2/linxi/linxi_0009.ogg"
    lx "哦，哦。"

    "我直接无视了他，什么破几把决斗，有我玩Galgame重要吗？"

    voice "cv2/others/tiyushenga_0010.ogg"
    ty_a "喂，喂！别走啊？？"

    "啊，今天的风儿，甚是喧嚣，阳光炽烈，真是明媚的一天。"
    "说起来，今天中午是吃食堂好呢，还是出去吃呢……"

    voice "cv2/others/tiyushenga_0011.ogg"
    ty_a "我们来打旮旯篮球吧！"

    play sound fx.slap
    "我噌噌两步退了回去。"
    with vpunch
    cz "什么！居然是那个，Galgame篮球？！"
    

    $ lx.show("惊讶")
    $ lx.act(anim_shake)
    voice "cv2/linxi/linxi_0010.ogg"
    lx "唉这什么东西你这个词语不是很奇怪吗这两个玩意怎么能组合到一起的——"

    "我直接一把子把林曦别到边上，别挡着我的视线。"

    $ lx.show("萌怒")
    voice "cv2/linxi/linxi_0011.ogg"
    lx "嘎——"

    $ lx.hide()

    cz "你说的是那个从国家数据库中随机出短篇Galgame，一边攻略一边进行单手篮球对抗，最后打完满场时加权计算Galgame完成度和篮球分数，还要在20分钟内喘着气写完一篇1000字感想交给AI评分的……"
    cz "——那个旮旯篮球？！"

    voice "cv2/others/tiyushenga_0012.ogg"
    ty_a "哈！果然，我没看错啊！你这逼居然如此熟悉！\n太对了，太对了，我真他妈是找对人了。"

    "没错，这是一个几乎只在小圈子内流传的高级运动，因为实在太难太难，总是不能被主流人群所接受。"
    "所以，当他说出这个名词的那一刻，我就知道，眼前的人，不好对付……"

    cz "居然有人想要用旮旯篮球来挑战我么，呵呵，呵呵呵呵呵呵——"

    
    hide ty_a
    stop music
    $ jwq.show("平静", pos=center)
    voice "cv2/jiangwanqing/jiangwanqing_0014.ogg"
    jwq "我说，能别挡道么。"

    play sound fx.wind
    "一股冷风吹过。"

    cz "………………欸？"

    "不知何时起，江晚晴幽灵一般地站到了我的面前。"
    "她身姿挺拔，用手自然地梳理着自己的修长黑发，就这么直直的面对我面前的男生。"
    "那真的是一种很放松的姿态，但却自内辐射出阵阵威压，仿佛她周身的空气和我身边的有着密度差，光线都在这里发生了轻微的折射。"

    $ jwq.show("嫌弃")
    voice "cv2/jiangwanqing/jiangwanqing_0015.ogg"
    jwq "让开。"

    voice "cv2/others/tiyushenga_0013.ogg"
    ty_a "哦，哦……"

    play music "audio/bgm/BGM_忧郁徘徊.ogg" fadein 1.0
    "他见到江晚晴，就像是僵尸见到了道长，只剩下沉默。"
    "宛如被法诀操控了似的，眼前的男子战战兢兢地往旁挪了两步，就这么让开了道路。"

    "我左右看了看，见着江晚晴向前走了，我也只能顶着周围的视线，硬着头皮跟着她走了几步。"
    "然后，她又像是想起了什么一样，顿住，回过头去。"

    $ jwq.show("平静")
    voice "cv2/jiangwanqing/jiangwanqing_0016.ogg"
    jwq "在我和阿舟相处的时候，少来打扰我，懂？"

    voice "cv2/others/tiyushenga_0014.ogg"
    ty_a "嗯嗯嗯嗯嗯。"

    "看到他疯狂点头的样子，我自己的背后都流下了几丝冷汗，有……有点恐怖。"
    "话说，我们平时上学时，有这么安静吗？"

    $ jwq.show("叹气")
    voice "cv2/jiangwanqing/jiangwanqing_0017.ogg"
    jwq "让你遇到麻烦了呢，早上也没时间了，辅导的事，放学后再说。"
    voice "cv2/jiangwanqing/jiangwanqing_0018.ogg"
    jwq "……只有这个时候，是真羡慕你旁边的这个家伙呀，哎。"

    voice "cv2/linxi/linxi_0012.ogg"
    lx "~~略。"

    $ jwq.show("尴尬")
    "看到曦曦吐了吐舌头，江晚晴那张精致的脸一下垮掉，抽搐了两下。"

    $ jwq.show("微笑")
    "不过很快她就深呼吸了一口，接着就对我绽放出了一个无比明媚的笑容。"

    $ jwq.hide()
    "在教学楼下，一路走来的我们终于是分开了，她向着不远处的另一个楼梯道走去，在她移动时，不像是行走，而像是在斩开人群，所有的人，甚至包括教师们，都在自觉地隔出一段距离来。"
    "阳光打在她的头上，为她加冕。"
    "看着她渐渐远去的身影，不得不让我再一次意识到，这个家伙……似乎，真的很厉害。"
    "如果能得到她的指点……"

    # ================= 场景：教室-白天 =================
    scene bg classroom1 with fade

    "……"
    "听课的时间很快过去。"
    "虽然下了课后很多人都来问我江晚晴的问题，但我并不算熟悉，所以也就没什么好说的。"
    "背后说人闲话更是不礼貌，我基本都是能糊弄就糊弄。"
    "估计江晚晴那边也有得忙吧，所以课间的那短暂空隙她没有到我教室里来，这实在是让我松了一口气。"
    "要是节节下课都往我这儿跑，那可不敢想该是怎样一副地狱绘卷。"
    "哪怕就是现在，我都已经在想……我的大名，该不会已经被全校都知道了吧？"
    "我是一个很怕麻烦的人，尤其是被迫施加于我身上的麻烦。"
    "本应如此的……"
    "奇妙的是，这样波澜起伏的日常，似乎没有想象中的让我烦闷。"
    "呵呵，或许我也没那么了解自己吧。"

    stop music fadeout 2.0
    "……"

    # ================= 场景：体育储藏室 (旮旯篮球对决) =================

    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene black
    $ renpy.pause(1.0, hard=True)

    scene bg sportsroom with fade
    play music "audio/bgm/BGM_欢快.ogg" loop

    "中午，午休时间。"
    play sound fx.play_basketball loop
    "灼热的体育馆内，此时赫然是一番不同的气象。"
    "四周许多人围观着，台下，台上，灼灼盯着场内两个飞速运动的男子。"
    "就在靠近体育馆储藏室的旁边，周围的人隔出了一段距离，那里是两位少女。"
    "隔开的人们，有部分估计是在一旁小心翼翼的侧耳偷听着，生怕错过了什么大新闻吧，听说，好像是什么争风吃醋，明争暗斗，两男一女，两女一男……反正校内的传言是这样说的……"

    $ jwq.show("平静", pos=right, x_offset=-200, y_offset=0, zoom=1)
    voice "cv2/jiangwanqing/jiangwanqing_0019.ogg"
    jwq "结果还是约上了，决斗什么的，男人真傻啊。"
    
    $ lx.show("平静", pos=left, x_offset=270, y_offset=0, zoom=1)
    voice "cv2/linxi/linxi_0013.ogg"
    lx "是吗？只要陈舟开心，怎样都好咯。"

    "江晚晴的双眼扫视了全场，她倒是看不出有什么遗憾的，只是表现出一副无奈的模样。"

    $ jwq.show("叹气")
    voice "cv2/jiangwanqing/jiangwanqing_0020.ogg"
    jwq "我倒是想多多珍惜和阿舟在一起的时光……你肯定不懂的，这就叫得之易，故不知惜，家宝不知贵。"

    $ lx.show("无语")
    voice "cv2/linxi/linxi_0014.ogg"
    lx "额，能别说这么肉麻的话嘛，我都要起鸡皮了。"

    $ lx.hide()
    $ jwq.hide()

    show sdcg 019 with dissolve
    "砰砰，咚咚——阵阵声音传来。"
    "场内那狂、野、劲、霸的对决，两个少女一直有在观察着，目前看来是要到尾声了。"

    voice "cv2/others/xiaoyoua_0003.ogg"
    xy_a "话说，这是什么行为艺术吗？"
    voice "cv2/others/xiaoyoub_0003.ogg"
    xy_b "不知道……但是，好……厉害啊，他们。"

    "陈舟一手拿着手机，在那里飞速的点击画面，另一只手控球，走位完全靠本能。"
    "——如果在一般人眼中，大概是这样的。"
    "但实际上，他之所以能如此流畅地走位，正是一种心象地图建模能力+一心三用+余光感知能力共同发挥作用的结果。"

    cz "跟得上我的speed吗！！"

    "他的对手也不甘示弱，一边用左右手疯狂交换着手机，然后用剩下一只手放在陈舟的胸前，做出死亡缠绕，他大叫着一些莫名其妙的话语，疯狂干扰陈舟记游戏剧情的思路……"

    with hpunch
    "就在这时！"
    "陈舟那边，突然一个犹豫步，肩膀向右一沉，让对手停顿了一下。"
    "而这个停顿他没有放过，陈舟放弃了在Galgame上的注意力，右手将球向前大力一运，噌噌加速，用肩膀卡住半个身位，一个强侧手就硬上了上去！"
    "对面也是反应极快，直接侧滑步跟上少年，利用身体进行对抗，右手高高举起，想要封盖。"
    "眼尖的同学甚至能够瞥到，对面的左手正牢牢地按着skip键，疯狂跳过中。"
    "两人同时跃起，在空中发生身体接触。"
    "陈舟在空中有一个极小的拉杆动作，右手手腕一抖，用一个类似跑投的方式，将球抛起——"

    "球在空中划出高高的弧线。"
    play sound fx.shot
    "然后，在篮筐上颠了两下，最终落入球网。"

    hide sdcg with dissolve
    "……"

    $ jwq.show("游刃有余")
    voice "cv2/jiangwanqing/jiangwanqing_0021.ogg"
    jwq "你说，阿舟，会赢吗？"

    $ lx.show("开心")
    voice "cv2/linxi/linxi_0015.ogg"
    lx "会赢的！"

    $ jwq.show("平静")
    voice "cv2/jiangwanqing/jiangwanqing_0022.ogg"
    jwq "……那你知道，旮旯篮球最恐怖的地方在哪么？"

    $ lx.show("平静")
    voice "cv2/linxi/linxi_0016.ogg"
    lx "你别问我呀，我对Galgame，真不熟。"

    $ jwq.show("游刃有余")
    voice "cv2/jiangwanqing/jiangwanqing_0023.ogg"
    jwq "一边阅读，一边对抗……通常来说，这是不可能做到的。"
    voice "cv2/jiangwanqing/jiangwanqing_0024.ogg"
    jwq "体能、专注力、动态决策、神经募集，玩游戏时，同时还会涉及到理解文本的前额叶、触发情感的杏仁核……这是对一个人综合能力的全面考量。"

    "只见场上的陈舟突然用手机屏幕对着防守方晃了晃。"

    voice "cv2/jiangwanqing/jiangwanqing_0025.ogg"
    jwq "看吧，还有认知战，虽然这里看不清楚，但我估计是泳装吧……或者是更过激的，泡芙之类的……对面猛地一下就会被干扰到。"

    "此时，趁着对方刹那间的愣神，陈舟突然把手机抛到空中，完成转身跳投后又精准接住。"

    $ lx.show("微笑")
    voice "cv2/linxi/linxi_0017.ogg"
    lx "……好厉害……他，居然如此努力……"

    $ jwq.show("坚定")
    voice "cv2/jiangwanqing/jiangwanqing_0026.ogg"
    jwq "这就代表，他对天选试就是有这么执着吧。"
    voice "cv2/jiangwanqing/jiangwanqing_0027.ogg"
    jwq "对了，再说回来，其实这一些，还只是开胃菜而已。\n旮旯篮球真正难的地方……"

    voice "cv2/linxi/linxi_0018.ogg"
    lx "是什么？"

    $ jwq.show("平静")
    voice "cv2/jiangwanqing/jiangwanqing_0028.ogg"
    jwq "是后面的，限时感想环节，20分钟，一千字，AI评审……加权分值为，整整一半。"

    $ lx.show("萌怒")
    $ lx.act(anim_shake)
    voice "cv2/linxi/linxi_0019.ogg"
    lx "这到底有什么意义啊！"

    $ jwq.show("游刃有余")
    voice "cv2/jiangwanqing/jiangwanqing_0029.ogg"
    jwq "当然有意义，毕竟，Galgame才是最重要的。"

    $ lx.show("平静")
    voice "cv2/linxi/linxi_0020.ogg"
    lx "那你的意思是……？觉得我提早开香槟了？"

    "江晚晴只是摇了摇头，嘴角微扬，露出了常挂在脸上的自信表情。"

    voice "cv2/jiangwanqing/jiangwanqing_0030.ogg"
    jwq "会赢的，我是这么相信。"

    $ lx.show("无语")
    voice "cv2/linxi/linxi_0021.ogg"
    lx "哈啊？那你到底在卖什么关子。"

    $ jwq.show("游刃有余")
    voice "cv2/jiangwanqing/jiangwanqing_0031.ogg"
    jwq "我的意思是，我是在理解了一切的基础上选择去相信他，比起你而言，我的层次会更高一点。"

    voice "cv2/linxi/linxi_0022.ogg"
    lx "……………………"
    "我能打她吗？林曦在心中想道。"
    stop music fadeout 1.0

    # ================= 场景：教室-黄昏 =================
    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene black
    $ renpy.pause(1.0, hard=True)

    scene bg classroom2 with fade
    play music "audio/bgm/BGM_忧郁2.ogg" loop

    "放学铃已经打了一阵子，周围的人窃窃私语着，看着我这边。"
    "承受着常人不可承受之重，夕阳透过窗口洒在我的脸上，宛如一层滤镜，给我的视野内映照得一片煌煌。"

    cz "我输了……"

    "为什么会这样呢？"
    "明明得分比对面高，明明Galgame也顺利打完了真结局……"

    cz "啊，我输了。"
    "我趴在桌上，漫无精神地发散思绪，感觉脑袋里有气泡在咕噜咕噜的往上飘。"
    "今天一整个下午，我都无精打采。"

    $ lx.show("平静", pos=center, x_offset=0)
    voice "cv2/linxi/linxi_0023.ogg"
    lx "那个，那个那个，舟子，该走啦。"

    "戳戳。"
    "曦曦在用手指戳我。"
    "我没反应。"
    "戳戳戳。"
    "我还是没反应。"

    $ lx.show("萌怒")
    $ lx.act(anim_jump)
    voice "cv2/linxi/linxi_0024.ogg"
    lx "啊~！给我起来！"

    play sound fx.pa
    "啪——！"
    "她猛地一下两掌合并……如果中间不是我的脸挡着的话，就好了。"
    "肉夹馍？"

    $ lx.show("鼓嘴气气")
    "感受着两颊温热的触感，还有眼前少女鼓起嘴巴气呼呼的样子，宛如盐落水中，眼前的薄膜渐渐消解了，嗯……果然也没什么好纠结的，呵，我真傻。"

    cz "哈——"
    with vpunch
    "我长出了一口气，然后猛地站起。"

    cz "曦曦，我们走。"

    $ lx.show("开心")
    voice "cv2/linxi/linxi_0025.ogg"
    lx "嗯嗯！"

    # ================= 场景：街道-黄昏 =================
    scene bg street1_2 with fade
    play music "audio/bgm/BGM_日常4.ogg" loop

    $ jwq.show("叹气", pos=right)
    voice "cv2/jiangwanqing/jiangwanqing_0032.ogg"
    jwq "阿舟……你怎么会，写出那样一篇感想。"

    cz "怎，怎么了，我，我觉得挺好的啊……"
    "话是这么说，好吧，其实我心里并没有底气，毕竟输就是输在这个上面。"

    $ lx.show("微笑", pos=left, x_offset=270)
    voice "cv2/linxi/linxi_0026.ogg"
    lx "我，我看着也不错呀，那个，女主角的魅力，不是都好好地写出来了吗……"
    "曦曦，还得是你……我最好的朋友……"

    $ jwq.show("平静")
    voice "cv2/jiangwanqing/jiangwanqing_0033.ogg"
    jwq "我问你，当你评价一个Galgame女主的时候，你是怎么评价的？"

    cz "额……都是女主角了，当然是可爱程度啊，\n比如说脸好不好看，声音好不好听，整体的造型怎么样，是什么属性，三无还是傲娇还是妹妹……"
    cz "哦对了我个人的话会比较喜欢白毛透明感空气系萝莉，\n还有黑长直金瞳威严小萝莉……"

    $ jwq.show("叹气")
    voice "cv2/jiangwanqing/jiangwanqing_0034.ogg"
    jwq "……哎……玉貌娇柔，粉黛罩骷髅，容貌美丑，风流一笔勾。所谓的第一印象，是最浅薄的视角，你就不能，从更加深入内核的角度去看吗，真是不知道该怎么说你了。"
    $ jwq.show("落寞")
    voice "cv2/jiangwanqing/jiangwanqing_0035.ogg"
    jwq "那些美少女，可能内核空空如也，只是你的幻想也说不定哦？"
    cz "……"
    cz "我觉得我、我的角度也没错吧，就像是甜豆腐脑和咸豆腐脑……"

    play music "audio/bgm/BGM_欢快2.ogg" loop
    $ jwq.show("指摘")
    $ lx.show("惊讶")
    with vpunch
    voice "cv2/jiangwanqing/jiangwanqing_0036.ogg"
    jwq "典型的废萌思维、废萌逻辑、废萌态度！"
    voice "cv2/jiangwanqing/jiangwanqing_0037.ogg"
    jwq "来，给我看看你的手机！"

    cz "额，给，给你……"

    $ jwq.show("嫌弃")
    voice "cv2/jiangwanqing/jiangwanqing_0038.ogg"
    jwq "果然，废萌手机！"

    "什，什么废萌手机……这么说，好伤心。"
    "这可是我以前玩的Galgame的联名周边，看吧，上面可是有着，一个这么可爱的美少女Logo呢……"

    $ jwq.show("叹气")
    voice "cv2/jiangwanqing/jiangwanqing_0039.ogg"
    jwq "哎……废萌人……"

    cz "有，有这么严重吗……"

    voice "cv2/jiangwanqing/jiangwanqing_0040.ogg"
    jwq "啊，是啊，在之后的辅导中，我一定要纠正你。"

    cz "噫——！？"

    $ lx.show("平静")
    voice "cv2/linxi/linxi_0027.ogg"
    lx "对了，你是要怎么辅导？"

    "嗯嗯，这个我可是很关心的，事关我的人生大事，不可不慎重。"
    "江晚晴既然是经历者，那想必肯定有她的小妙招，对此能够给予信任。"
    "……希望不是禁止游玩废萌之类的反人类方式。"
    "我摇了摇头，提起精神，希望能探询到具体内容。"

    $ jwq.show("游刃有余")
    voice "cv2/jiangwanqing/jiangwanqing_0041.ogg"
    jwq "为了应对天选试，需要进行Galgame特别辅导。\n具体的做法也很简单，我把它命名为……"

    play sound fx.dingdong
    $ jwq.show("微笑")
    voice "cv2/jiangwanqing/jiangwanqing_0042.ogg"
    jwq "认真和我们谈恋爱！！"

    cz "……"
    with vpunch
    cz "{size=+20}——哎？哎哎哎哎哎？？？{/size}"
    "这女人在说什么啊！"

    $ lx.show("白眼")
    voice "cv2/linxi/linxi_0028.ogg"
    lx "……「我们」是什么意思？"

    voice "cv2/jiangwanqing/jiangwanqing_0043.ogg"
    jwq "包括你，简单来说，就是让阿舟和我，还有你，两个人谈恋爱……"

    $ lx.show("惊讶")
    voice "cv2/linxi/linxi_0029.ogg"
    lx "这，这么弄？"

    cz "哈？不是不是不是不是不行不行不行不行——！"
    cz "我可是有女朋友的啊！"

    "我赶忙拒绝，开什么玩笑，就算我没有爱人，这同时和两个人谈恋爱什么的也太前卫了吧！虽说现在的确是一个前卫的时代吧！但我可是一个传统的人啊！"

    $ jwq.show("平静")
    voice "cv2/jiangwanqing/jiangwanqing_0044.ogg"
    jwq "哦~你误会了，这个叫做现实模拟Galgame，作为一种非常富有效率的实践方式，在培养你的综合素质方面具有极大的功效。"

    "{size=+20}什么鬼，还有这种说法？！{/size}"

    $ jwq.show("游刃有余")
    voice "cv2/jiangwanqing/jiangwanqing_0045.ogg"
    jwq "而在这个基础上，多女主当然比单女主更普适一点，简单来说就是，把我们当成Galgame里的女主，去攻略吧！我们会配合你的！"

    voice "cv2/jiangwanqing/jiangwanqing_0046.ogg"
    jwq "林曦，你说呢？"

    $ lx.show("平静")
    voice "cv2/linxi/linxi_0030.ogg"
    lx "哦，哦哦……我会配合的。"

    cz "哈——？曦曦，你怎么也？？但是，但是，就算是模拟的……"

    $ jwq.show("指摘")
    with vpunch
    voice "cv2/jiangwanqing/jiangwanqing_0047.ogg"
    jwq "阿舟！难道说，你对你女友的感情如此肤浅？！"

    cz "什么！"
    "我…我对小涟的爱，当然是很严肃的。"

    voice "cv2/jiangwanqing/jiangwanqing_0048.ogg"
    jwq "现实Galgame，看得见摸得着，这可是你难得的宝贵经验，不是一般人能拥有的！"
    voice "cv2/jiangwanqing/jiangwanqing_0049.ogg"
    jwq "为了让你通过天选试，我可是在用心计划着，绝无一丝他意！你在想什么，你居然在想，真的攻略我们，或者说可能会被我们反攻略？你意思是你可能会当真，背叛你的女友？"
    voice "cv2/jiangwanqing/jiangwanqing_0050.ogg"
    jwq "原来你对你自己的爱，这么没自信吗！"

    $ jwq.show("平静")
    cz "这……这？嘶——"
    "我靠，她说的好对啊！"
    "对啊！要知道，天选试可是对Galgame人才的综合选拔，\n如果我有所谓的「现实Gal」经验，那么对比起来，不就是凭空多玩了一种类型的Galgame吗？"
    "这种情况下和别人竞争起来，实际经验会转化为直接优势。"
    "这么一想，无论如何都无法拒绝了。"
    "不如说，我想要！我想要游玩，现实Galgame！"

    cz "……呵，呵呵呵，怎么会呢。"
    cz "小涟，我的生命之光，我的欲念之火，我的罪恶，我的灵魂……让我背叛她？哈哈哈，我忍不住大笑起来！我说，你不懂小涟而妄下论断！"

    "回过神来，越想，我就越觉得靠谱。"
    "是了，这么一看，江晚晴……果然是天才啊。"
    "既然有关于天选试，那就没有什么好说的了，一切都是为了小涟，我不能放过这个机会！"

    $ jwq.show("游刃有余")
    voice "cv2/jiangwanqing/jiangwanqing_0051.ogg"
    jwq "不错，就是这个觉悟。"

    "咦？怎么回事？好像看到江晚晴和曦曦两个人眉来眼去，像是达成了什么共识一样，奇了怪了，她俩什么时候这么熟的。"
    "然后，林曦好像是下定了什么决心，站出来一步。"
    "仅这一步，便来到了我的面前，和我近距离对视着。"

    $ lx.show("萌怒")
    voice "cv2/linxi/linxi_0031.ogg"
    lx "我要！成为你的个人线女主！给我做好觉悟！"

    "嚯！来这一招？"
    "跟老子整蛊是吧，曦曦啊，想让我出丑，你还太年轻！"
    "我心中冷笑。"
    "看我之后怎么弄你就是了！我玩了这么多的废萌，攻略女孩子宛如呼吸般自然，在这方面作为超级大师，还没怕过谁！"
    "Galgame里的女主，我都是略施小计，好感度槽就直接爆表了的，想来现实里的女人也大差不差。"
    "既然是模拟，那我也不用藏着掖着了，等到时候让曦曦留下害羞的表情，肯定要好好拍个照，以后拿出来反复取笑，三回啊三回。"
    "我控制不住地扬起了嘴角。"

    cz "嘿，行，反正要个人线之后才是真女主线呢，Galgame里可都是这个套路。来，我已经理解了一切了，全给我放马过来，桀桀桀。"

    $ jwq.show("微笑")
    voice "cv2/jiangwanqing/jiangwanqing_0052.ogg"
    jwq "哼~~这样就好咯。"

    cz "没关系，不就是模拟？正合我意，反正也没什么心理负担了，那就按照流程来吧——"
    cz "现实Galgame，共通线，启动！"

    "在别样的喧闹中，我眯起了眼。"
    "两位少女的影子在眼前摇曳着，好像有风儿拂起了她们的头发。"
    "这幅光景，与当前温馨的夕阳格外相衬。"
    "看来，接下来的日子，是有得玩了。"

    stop music fadeout 1.0
    scene black with fade
    "我回到了家。"

    play music "audio/bgm/BGM_安慰.ogg" loop fadein 1.0
    show cg 001 with dissolve
    voice "cv2/xiaolian/xiaolian_0001.ogg"
    xl "哎呀哎呀，回来啦？"

    cz "是呀，今天一天感觉还不赖。"

    voice "cv2/xiaolian/xiaolian_0002.ogg"
    xl "哦~？"
    "她只是歪着头，眼睛眨巴眨巴着。"

    cz "和人比赛了旮旯篮球……虽然小输了一手，但也是相当宝贵的经验。"
    cz "对我之后的天选试，可以起到积极作用。"

    show cg 002 with dissolve
    voice "cv2/xiaolian/xiaolian_0003.ogg"
    xl "呜呜……为什么会输呢？我明明，每天都在和你一起，看着你努力的。"

    "她情不自禁地向我这边走了一步，露出了非常沮丧的表情。"
    "那一身轻飘飘的衣服，让我有种幻觉，仿佛只要她往前轻轻走一走，就要悬浮起来似的。"

    show cg 001 at truecenter:
        zoom 1.2
    with dissolve
    "于是，我抱住了她。"

    voice "cv2/xiaolian/xiaolian_0004.ogg"
    xl "嗯~"

    "我贪婪地吸取着她身上的味道，直到肺里全部充满了小涟的气息后，才说道。"

    cz "大抵是，我对于游戏的理解还不到位吧……好像，必须要分析剧情结构，人物内核之类的，才能拿到高分。"

    show cg 002 with dissolve
    voice "cv2/xiaolian/xiaolian_0005.ogg"
    xl "……真是讨厌的标准。"

    cz "但大家都是这么说的呀，所以，路子走偏的，其实是我？"
    "有一点点的迷茫，我的底气确实不够。"
    "而她只是用头顶了顶我，然后反手抱了过来，在我背后自上而下，反复抚摸着……真的，真的让人感到，好安心。"

    show cg 001 with dissolve
    voice "cv2/xiaolian/xiaolian_0006.ogg"
    xl "我希望，你可以更相信自己一点哦？怀疑自己的这幅样子也太丢人了。"

    cz "呜呜呜，没办法啊，输了就是输了。"
    cz "我可是要参加天选试的，所以，一定要在所有地方都做到最好才行。"
    
    voice "cv2/xiaolian/xiaolian_0007.ogg"
    xl "好啦好啦~别伤心，别伤心。"
    voice "cv2/xiaolian/xiaolian_0008.ogg"
    xl "你是想要……去见神明是吗？那就没问题了，神明最看重的就是心灵，其他的程序化的、标准化的逻辑，怎么能代表你真实的感性呢？"
    voice "cv2/xiaolian/xiaolian_0009.ogg"
    xl "诺提拉肯定会更喜欢你这一边，我担保哦。"

    cz "……真的？"

    "相传，天选试在千年前，是作为一种沟通天上神明的仪式，旨在展现出这个世界上最优秀之人，以获得神明垂怜，保国家安康、风调雨顺。"
    "——可偿诸愿。"
    "故事如此流传。"
    "而诺提拉，则是传说中神明的名字，虽然写在了教科书里，但那仍然是传说。"
    "然而小涟却很笃定的样子。"

    voice "cv2/xiaolian/xiaolian_0010.ogg"
    xl "嗯嗯，真的。"

    "不知道为什么，我一到小涟的面前，就只能暴露出一个不那么自信的自己……我明明想让她见到我帅气的样子的。"
    "这肯定代表着，我对她就是有如此的依恋吧……"

    cz "可是，我还听专家说了，我眼里那些女主角的模样，内核空空如也，都是我的幻想。"

    show cg 002:
        xalign 0.5
        yalign 0.5
        linear 0.5 zoom 1.0

    voice "cv2/xiaolian/xiaolian_0011.ogg"
    xl "唉~~~好坏哟。"
    voice "cv2/xiaolian/xiaolian_0012.ogg"
    xl "才不是这样子的。"
    voice "cv2/xiaolian/xiaolian_0013.ogg"
    xl "破专家，坏专家…思考本质什么的，起点就错了。"

    cz "这样啊，可是我感觉，探寻本质什么的，也说得过去，毕竟，总会有的吧，所有人身上都有。"
    cz "本质也好，内核也好，只是我的视野狭窄……没有去看而已。"

    show cg 001 with dissolve
    voice "cv2/xiaolian/xiaolian_0014.ogg"
    xl "……不对不对，感受才是最重要的啦，阿舟，你玩游戏、看电影的时候，会去想那些深奥的东西么？"

    cz "一般是不会的吧。"
    "除非作品实在是太无聊了。"

    voice "cv2/xiaolian/xiaolian_0015.ogg"
    xl "如果你在看的时候，在玩的时候，还在想那之外的事，这个时候应该说是学者呢，还是研究者呢？哎呀哎呀，总之不会是一个玩家，也不可能是观众啦。"
    voice "cv2/xiaolian/xiaolian_0016.ogg"
    xl "那些本质啊，内涵呀之类的，是要全看完了才能回过头去想的，而到了那时，你最初对美的感知早就已经忘光光了，事后用嘴巴说出来的，都是牵强附会的啦。"

    "……道可道，非常道么。"

    voice "cv2/xiaolian/xiaolian_0017.ogg"
    xl "归根结底，大家都是从情感出发的……为了那一瞬间的愉快或不舒服，来决定如何评价……大家看到的，其实都是记忆里，加上了滤镜的作品哦。"

    cz "如果这样说的话，那这世间的一切，好像都可以套上这个逻辑吧。"

    voice "cv2/xiaolian/xiaolian_0018.ogg"
    xl "对呀，只要经过人为解释的，就会失真，而没有经过中介的直接体验，我们又不可能表达出来。"

    cz "看样子是一根筋两头堵了。"

    voice "cv2/xiaolian/xiaolian_0019.ogg"
    xl "就像是…嗯……你认为，我是一个什么样的存在，是你的幻想吗？"

    cz "不是的。"
    "这是在说什么话，小涟当然不是。"

    voice "cv2/xiaolian/xiaolian_0020.ogg"
    xl "呼呼呼~那不就够了？\n我希望，你对其他的Galgame女主，也抱有对我相同的爱。"

    cz "原来…如此，我大概，明白了。"
    "虽然并没有搞得太明白，但我还是凭借属于我的直觉，明白了些什么。"
    "如果换一个人这样对我说，我肯定是无法同意的吧。"
    "但是小涟说出的话，我就能理解。"

    voice "cv2/xiaolian/xiaolian_0021.ogg"
    xl "什么是对的，什么是错的……那都是世人的评价啦，不作数的。"

    show cg 001 at truecenter:
        zoom 1.2
    with dissolve
    "她偷偷地把我的手牵了起来，翠白的指尖逐个划入缝隙中，直到完全贴合。"
    "就这样，我就感觉到有些散落的碎片被整合了起来，从体内萌发出奇异的舒畅感……我真好搞定。"
    "她趴在我的胸口，像是在喃喃自语一般。"

    voice "cv2/xiaolian/xiaolian_0022.ogg"
    xl "天上的星星，有些已经不存在了，它们要穿越数亿年的时光，才能到达你的眼前……"
    voice "cv2/xiaolian/xiaolian_0023.ogg"
    xl "人类可能永远永远，都不会知道，哪个是真的，哪个是假的了……"

    "我抱紧了她。"

    cz "真残酷啊……"
    voice "cv2/xiaolian/xiaolian_0024.ogg"
    xl "真美丽啊……"

    # 本场结束，大幕关闭
    stop music fadeout 2.0
    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene black
    $ renpy.pause(1.0, hard=True)
    $ lx.reset_position()
    $ jwq.reset_position()
    $ xl.reset_position()
    return