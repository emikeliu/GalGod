transform foot_to_head_scan:
    zoom 2.0
    xalign 0.5

    # 从脚部开始
    yanchor 1.0
    ypos 1.0
    yoffset 0

    blur 20
    alpha 0.0

    parallel:
        linear 0.6 alpha 1.0
    parallel:
        easeout 12.2 yoffset 2200
    parallel:
        linear 1.5 blur 0

    # —— 扫描结束后，稍微停一下
    pause 2.5

    # —— 自然回到正常立绘状态
    parallel:
        easein 1.2 zoom 1.0
    parallel:
        easein 1.2 yoffset 0




label scene_1_2:
    # === 场景：教室-白天 ===
    play music "audio/bgm/BGM_日常5.ogg" loop fadein 1.0
    scene bg classroom1
    with fade

    # 这里的 student_a 和 student_b 如果没有定义，可以用动态字符，这里假设已定义
    # 如果未定义，可以用 "同学A" "内容" 的方式
    
    voice "cv/tongxuea/tongxuea_0001.ogg"
    "同学A" "哟，这不是咱们舟少吗。"
    
    cz "早上好。"

    "我走过去，直接伸拳捶了他胸口一下。"

    voice "cv/tongxuea/tongxuea_0002.ogg"
    "同学A" "嘿嘿，话说，你的AI女友呢？真不准备给哥们看下长什么样？"

    cz "不行不行，不能给你看。"

    "我行事做人大大方方，没什么好遮掩的。\n小涟的存在我并没有刻意隐瞒，毕竟我们是正儿八经在谈恋爱。"

    cz "话说也不是AI啊，是真实存在的。"
    cz "小涟可是很漂亮的……我怕，你们一看到她，就要被勾了魂去。"

    voice "cv/tongxueb/tongxueb_0001.ogg"
    "同学B" "我靠，真的假的？游戏名透露一下，画师是哪个？"

    "旁边几个兄弟也围了过来，把林曦都挤到了一边去。"

    voice "cv/tongxuea/tongxuea_0003.ogg"
    "同学A" "哥们不是，你这就不对了，你不知道我最喜欢白毛美少女了吗？听你说，那个小涟是白毛，我早就馋她好久了。游戏名真得给大伙透露一下吧？"
    
    voice "cv/tongxueb/tongxueb_0002.ogg"
    "同学B" "就是就是，你都玩了那个游戏几年了，都被那个女主俘虏了，好东西就是要和兄弟们分享啊，藏着掖着多没意思。"
    voice "cv/tongxueb/tongxueb_0003.ogg"
    "同学B" "……对了，有咱们男同胞想要的那种环节吗。"

    cz "哈哈哈，她可是我的恋人，我与她真心相爱，才不想被你们横插一脚。"

    voice "cv/tongxueb/tongxueb_0004.ogg"
    "同学B" "啧，你真狗啊，这么小气。"
    voice "cv/tongxuea/tongxuea_0004.ogg"
    "同学A" "嗐，不过我也不是不能理解这种心情吧，就像是发现了一个小众秘密餐厅一样，人少高级还实惠，巴不得只有自己知道。"
    
    cz "嘿，知道就好！"

    # $ _window_during_transitions = True

    show sdcg 003 with dissolve
    voice "cv/linxi/linxi_0050.ogg"
    lx "我……我可是玩过那个游戏的！"

    "在这个时候，刚和其他几个圈子打完招呼的林曦又凑到了这边来。"

    show sdcg 004 with dissolve
    voice "cv/linxi/linxi_0051.ogg"
    lx "当然，我也不告诉你们，嘻嘻，这可是秘密，你们就别打听了。"

    voice "cv/tongxuea/tongxuea_0005.ogg"
    "同学A" "好啊，好啊！宣示主权是吧？还有共享秘密这招？！"
    voice "cv/tongxuea/tongxuea_0006.ogg"
    "同学A" "不过啊我劝你还是死了心吧，我看咱们舟少完全没有别的想法啊。"
    voice "cv/tongxueb/tongxueb_0005.ogg"
    "同学B" "有一说一，确实。"

    show sdcg 005 with dissolve
    voice "cv/linxi/linxi_0052.ogg"
    lx "哼，随你们怎么说。"

    voice "cv/tongxuea/tongxuea_0007.ogg"
    "同学A" "话说你也不玩Galgame啊？你来干什么？\n我们这里可是在进行一场高端的、顶级的战略商讨，一边去一边去。"

    show sdcg 006 with dissolve
    voice "cv/linxi/linxi_0053.ogg"
    lx "怎么就不玩了，我……我最近也是玩了几部Galgame的，也写了一些感想。"

    "林曦一向人缘好，不管是什么人都能无缝交流，插进我这边的圈子里来后自然而然就接管了整个氛围，反倒我都有些插不上话了，不得不说这真是让人有点羡慕。"

    voice "cv/tongxuea/tongxuea_0008.ogg"
    "同学A" "真的假的？转性了？"
    voice "cv/tongxueb/tongxueb_0006.ogg"
    "同学B" "你玩了哪些？我看看我有没有玩过的。"

    "旁边的人，不管是男的女的，听到这边的动静，都不由自主的升起了一些探询之意。"
    "毕竟，就算Galgame从来不被大伙当为终极目的，但由于它对国家政治、对商业策略、对人文修养、对科技发展有着如此重大的作用，所以，大家普遍都在对此展开品鉴与学习。"
    "而林曦，其实本来是少数的那些，对Galgame完全没兴趣的人。"

    show sdcg 007 with dissolve
    voice "cv/linxi/linxi_0054.ogg"
    lx "那个…那个……"
    
    "她犹犹豫豫。"
    "但最终还是提起一口气，说了出来。"

    show sdcg 008 with dissolve
    voice "cv/linxi/linxi_0055.ogg"
    lx "就是……爱猫啊，爱刀啊，爱火车啊……那些。"

    voice "cv/tongxueb/tongxueb_0007.ogg"
    "同学B" "哈——？！"
    voice "cv/tongxuea/tongxuea_0009.ogg"
    "同学A" "废萌？"

    "我的眼角控制不住的跳动了一下，赶紧低下头来。"
    show sdcg 009 with dissolve
    "但是，林曦的目光却尴尬的看向了我。"

    voice "cv/linxi/linxi_0056.ogg"
    lx "是舟子推荐我的……其实我觉得还不赖吧，也还是能让人感到有趣的。"

    "听到这话，旁边的人立马用一副「你在说什么呢」的表情来回打量着我和林曦。"

    voice "cv/tongxuea/tongxuea_0010.ogg"
    "同学A" "可是，废萌不是那个最达利特……"
    voice "cv/tongxueb/tongxueb_0008.ogg"
    "同学B" "别说了别说了，没事没事，废萌也是不差的，听说，有一部分幼儿园、还有早教机构，会将废萌作为学前教育环节。"
    voice "cv/tongxuea/tongxuea_0011.ogg"
    "同学A" "啊，这个我知道，我记得有家长们举报的，说殆害无穷，影响孩子的Galgame世界观。"

    # 咳嗽打断，使用 vpunch 震动屏幕
    cz "额咳咳！"
    with vpunch

    "事到如今，我必须打断一下了。"
    "要知道，「废萌玩家」这四个字，基本上可以和最底边的loser划上等号。"
    "我虽然是一个废萌党，但我也不敢在外声张。"
    "只敢在网上，用自己的账号进行大肆宣扬。"
    "所幸，我在现实世界还可以隐藏起来，因为我的Galgame知识足够。"
    "而林曦这种待人友善、事事周全、阳光明媚的高能量少女，要是让她一不小心被贴上这个标签就麻烦了。"
    "我连忙插嘴。"

    cz "你们啊，就不懂了，今年的天选试……我可是听说，和废萌有关。"

    "——我根本没听说，完全是我编的。"
    "旁边的人听到我的话语，纷纷倒吸一口凉气，让我身边的温度都降低了几分。"

    cz "对，很多事情都是空穴来风，但是，我们绝不能放弃每一个希望，不能放弃每一种可能，就如同Galgame一般，你会因为，不喜欢那个角色的属性，就不走她的线路吗？"

    with vpunch
    play sound fx.deng
    "我站了起来！"
    with vpunch
    play sound fx.deng2
    "瞪大双眼，直面整个班级的目光。"

    show sdcg 010 with dissolve
    cz "不能！"

    "双臂被我大大地张开，感觉自己成了飞上天穹的雄鹰。"

    cz "每一个女角色，我们都要沟通充分！每一条选择肢，哪怕是通往bad end，我们也绝不能心生退缩！"
    cz "全都要！哪怕是福瑞，哪怕是男娘！\n对！这才是我们Galgame玩家，真正的目标！"

    "他们都被我的气势威慑住了！"
    "那是当然的，因为，我对Galgame的学习，可和他们不在一个层面上！"

    cz "废萌是如此，剧情作也是如此……"

    "声音回响在整个室内，盘旋着，盘旋着，\n我带着十分乃至九分的自信，昂首挺胸坐了下来。"

    cz "呵呵，你们啊，还是得多学习一个。"

    "教室内的分贝降低了些许。"
    "果然，听到我的主张后，旁边的几位同学，逐渐变为了若有所思的样子。"
    "至于更远的那些人们……\n哼，连参与我们Galgame大讨论的水平都没有，不在我的眼中。"

    show sdcg 011 with dissolve
    voice "cv/linxi/linxi_0057.ogg"
    lx "嘿，嘿嘿。"
    voice "cv/linxi/linxi_0058.ogg"
    lx "你也就只有在这个时候，靠谱一点了……"

    cz "……？你怎么扭扭捏捏的，别犯病。\n额，大姨妈来了？"

    show sdcg 012 with dissolve
    voice "cv/linxi/linxi_0059.ogg"
    lx "才不是！"
    
    play sound fx.slap
    # 巴掌音效 + 震动
    with vpunch

    "嗖——"
    "她一巴掌拍了过来，还好还好，我勤于锻炼，仅在零点几秒内就做出了合适的反应，真是千钧一发！"
    "要是被这一巴掌扇中，今天一天估计都别想见人了。"

    voice "cv/tongxuea/tongxuea_0012.ogg"
    "同学A" "我说你啊……对女孩子也别太下头了。"

    cz "……"
    cz "？"

    "他看到我一脸疑惑的表情，嘴角抽搐了一下。"

    voice "cv/tongxuea/tongxuea_0013.ogg"
    "同学A" "这就是青梅竹马的诅咒吗……听说，人对太熟悉的家人，根本产生不了欲望，原来是真的啊。"
    voice "cv/tongxueb/tongxueb_0009.ogg"
    "同学B" "唉……你要不要看看，我们整个高年级，喜欢林曦的有多少人……"
    
    cz "真的假的……"
    show sdcg 013 with dissolve
    "我瞥向曦曦的脸，她的脸因为激动而红红的，要说可爱的话，确实，应该是可爱的吧……"
    "但是……把她当做恋爱对象？"

    hide sdcg with dissolve
    # $ _window_during_transitions = False

    $ lx.show("忧伤", pos=center)
    $ lx.act(anim_jump)
    "我还没想明白，肩膀忽然被人轻轻撞了一下。"
    
    $ lx.show("忧伤", zoom=2, transition=dissolve, y_offset=1900)
    "不知何时起，她居然已经凑到了我这边。"
    "曦曦凑得很近，近得能看到她睫毛微微颤动的样子。"

    voice "cv/linxi/linxi_0060.ogg"
    lx "你在想什么？"

    cz "额，没什么。"

    "我下意识后退半步。"
    "结果她立刻抓住了我衣领，像是怕我跑掉似的。"

    $ lx.show("鼓嘴气气")
    voice "cv/linxi/linxi_0061.ogg"
    lx "说呀。"

    "周围同学熙熙攘攘，好像还有人发出了一声调侃的“哦——”。"

    cz "要不，你先放开我。"
    
    $ lx.show("忧伤")
    voice "cv/linxi/linxi_0062.ogg"
    lx "唔唔唔——我又不是吃人的。"
    "她压根没有放开的意思。"

    voice "cv/tongxuea/tongxuea_0014.ogg"
    "同学A" "难说哦？刚刚那一巴掌，换我肯定当场去世。"
    
    "而她听了这一调侃，眉头挑了挑，显得更气了。"

    voice "cv/linxi/linxi_0063.ogg"
    lx "舟子，你是不是……真的一点都不在意我啊？"

    cz "没，没啊。"

    "我被一股莫名的气势压制住了……这种氛围，难道说……"


    play sound fx.deng2
    with vpunch
    "{size=+15}——要与我为敌吗？{/size}"

    voice "cv/linxi/linxi_0064.ogg"
    lx "你刚刚…在想什么呢？"

    "看得出，她明显地动摇着。"
    "应该没有像个鹌鹑一样的敌人吧，我不想糊弄，还是直接说比较好。"

    cz "……哎，好吧，一说起来确实就意识到了。你好像的确很漂亮。"

    "但假设说要作为恋爱对象的话，更吸引人的大概是她的性格和内心，那里才是真正的可贵之处。"

    cz "也就只有这时候，能充分认识到你是个女孩子了……"

    $ lx.show("鼓嘴气气")
    voice "cv/linxi/linxi_0065.ogg"
    lx "算了，我知道你就这样。笨死了。"

    "短暂的气气后，她又变脸似的换了个表情。"

    $ lx.show("微笑", zoom=1, transition=dissolve, y_offset=0)
    voice "cv/linxi/linxi_0066.ogg"
    lx "话说，嚯嚯，哎？我没听错吧？你居然会把我当女孩子吗？看不出来呀。"

    cz "……"

    "调笑的言语向我逼来。"
    "我这死党，哪里都好，就是有时候会变得莫名其妙的烦人。"
    "哎，谁叫我做人靠谱呢，对于她这种情况，我也是见怪不怪了。"

    cz "哼哼，那你可太轻视我了，我可是把你当成……"

    stop music fadeout 1.0

    voice "cv/others/yuanchudeshengyin_0001.ogg"
    "远处的声音" "喂喂！那一位来了……上一次天选试……那个本省的……"

    "嗯？天选试？"
    "我捕获到了熟悉的关键字。"

    voice "cv/others/yuanchudeshengyin_0002.ogg"
    "远处的声音" "呼哇，真的是，我以前在电视上看到过她，怎么会来我们这……"

    "吵吵闹闹的，是我们学校来了什么大人物么？"

    # 音效：上课铃
    play sound fx.classbell
    
    "就在这时，上课铃响了。"

    voice "cv/banzhuren/banzhuren_0001.ogg"
    "班主任" "肃静！！"
    
    # 隐藏林曦
    $ lx.hide()

    play music "audio/bgm/BGM_忧郁.ogg" loop fadein 1.0
    voice "cv/tongxuea/tongxuea_0015.ogg"
    "同学A" "呜哇，老头来了，赶紧溜——"
    voice "cv/banzhuren/banzhuren_0002.ogg"
    "班主任" "上课时间到了，大家赶紧回到座位！"

    "同学们稀稀拉拉地各自回到了自己的位置上。"

    voice "cv/banzhuren/banzhuren_0003.ogg"
    "班主任" "我也不瞒着你们了，反正等到时候下课了，你们自然会知道的。"
    voice "cv/banzhuren/banzhuren_0004.ogg"
    "班主任" "学校里转来了一个女孩子，在别的班上……那可是位大人物。"
    voice "cv/banzhuren/banzhuren_0005.ogg"
    "班主任" "在三年前的天选试上，她通过了初试。"

    play sound fx.crowd
    "哇！！！"
    "同学们果然全部都嚷嚷了起来。"
    "而班主任只是缓缓摇了摇头，像是在为青春期的急躁而发笑。"

    stop sound fadeout 1.0
    voice "cv/banzhuren/banzhuren_0006.ogg"
    "班主任" "不止如此，她啊，在省级考核中，居然也获得了不错的名次，获得了前往殿试的资格。"

    "什么！"

    voice "cv/banzhuren/banzhuren_0007.ogg"
    "班主任" "虽然殿试落选了，但当时的记录，你们应该还能搜得到。"
    voice "cv/banzhuren/banzhuren_0008.ogg"
    "班主任" "当时的她，只有14岁。"
    voice "cv/banzhuren/banzhuren_0009.ogg"
    "班主任" "14岁的……Galgame领域大神。"

    "这…这多少年才能出一个？"
    "喉头滚动，胃部不自觉感到一抹下坠感。"
    "如此地位和才能，哪怕是重要部门的大领导在她面前，也得好声好气表示才行。"
    "但是，但是，三年前，我也就差不多这个岁数，如果我去了的话…说不定……"
    "空气逐渐沉重起来，好一会后，我才后知后觉发现自己已经握紧了双拳。"

    voice "cv/banzhuren/banzhuren_0010.ogg"
    "班主任" "人外有人，天外有天。"
    voice "cv/banzhuren/banzhuren_0011.ogg"
    "班主任" "除了一些玩票性质的人外，那些真正的天选试种子，都是从小培养领导力、社交力、组织力，并熟读天文地理，四书五经，在国际战略和全局视野上都具备丰富的沉淀。"
    voice "cv/banzhuren/banzhuren_0012.ogg"
    "班主任" "只有童子功加天赋的化合，才能在优异家境与艰难的实战历练中，蜕变而出。"
    voice "cv/banzhuren/banzhuren_0013.ogg"
    "班主任" "哪怕是在那些超级精英里，能在20岁以前前往殿试的，也能称得上是相当恐怖了，像是考了10次，花了30年才到殿试环节的人，大家都听过不少了吧。"
    voice "cv/banzhuren/banzhuren_0014.ogg"
    "班主任" "这样的天之骄子特地转来我们学校，连校长都无法理解，说起来，真是我们学校的荣幸。"

    "完完全全，是正确的。"
    "台上老师的话语无比正确，甚至让我流下汗水。"
    "我的能力，我的才能……真的够么……"
    "不，不对，这不是能不能的问题，而是，我必须要去。"

    voice "cv/banzhuren/banzhuren_0015.ogg"
    "班主任" "你们啊，有机会的话，可以多学一学她的思想，学一学人家的学习模式。"
    voice "cv/banzhuren/banzhuren_0016.ogg"
    "班主任" "我也建议你们去认识一下。"
    voice "cv/banzhuren/banzhuren_0017.ogg"
    "班主任" "毕竟都是同龄人，能交上朋友的话，甚至于，只要能留下一面之缘，也会是你们将来巨大的人脉。"
    voice "cv/banzhuren/banzhuren_0018.ogg"
    "班主任" "当然！大家也不要太在意那一边，要是浪费了学习时间就不好了，我提醒你们，人家的世界和你们没关系，倒是后面的高考对你们来说是人生大事！"
    voice "cv/banzhuren/banzhuren_0019.ogg"
    "班主任" "来，注意这边。"

    "老师切换了PPT，激光笔点出，在两个争锋相对的女主脸上着重画了几圈。"
    "我们学校还算重点，所以大家全部都很自觉的开始做起了笔记。"

    voice "cv/banzhuren/banzhuren_0020.ogg"
    "班主任" "这个机场告别场景，完美诠释了战略模糊性政策的失败案例。"
    voice "cv/banzhuren/banzhuren_0021.ogg"
    "班主任" "当主角在雪中追逐出租车时，就相当于什么？同学，你，你来回答一下。"

    "我？"
    "我站了起来，很轻松地回答了问题。"

    voice "cv/banzhuren/banzhuren_0022.ogg"
    "班主任" "嗯，不错，记住了同学们，这就像是在核聚变实验堆里突然注入过多氚元素，必然导致政治反应堆熔毁，对于我们国家在当今世界上的生态来说…一定有着不可忽视的意义……比如说……还有……"

    "……"
    "…………"
    "………………"

    # === 黑屏转场 ===
    scene black with Dissolve(1.5)
    stop music fadeout 1.0
    
    # 保持黑屏一小会儿
    pause 1.0


    scene bg classroom2 with dissolve

    # 音效：下课铃
    # play sound "audio/bell.ogg"

    "一天过去，我也没见到那一位神秘的天选之子候补。"
    "身边的人都在叽叽喳喳地讨论着，听他们说，似乎是个长得很好看的人。"
    "上厕所的时候我远远瞟过一眼，那边的教室整个都被围得水泄不通。"
    "午休时，似乎她又被叫到了校长室去商讨要事，看起来就很忙的样子。"
    "不过我也没什么兴趣就是了。"

    $ lx.show("惊讶", pos=center)
    voice "cv/linxi/linxi_0067.ogg"
    lx "那个，舟子，我们赶紧回去吧。"

    cz "嗯，我本来就是这么想的。"

    "我要把时间放在Galgame，还有小涟的身上，赶紧吃完饭回家，没空想那么多有的没的。"

    $ lx.show("微笑")
    voice "cv/linxi/linxi_0068.ogg"
    lx "好呀，走吧走吧，和我一起走。"

    cz "……? 你急什么，行吧，我收拾一下。"

    "班里的人有留下来复习的，有玩闹着的，\n也有像我一样在收拾背包，准备开溜的，没有任何异样。"
    "不太懂林曦为什么这么急。"
    "……是因为要去什么很热门的店排队？"
    "钱包够不够啊……"
    "三下五除二把东西都塞进了包里，我站了起来。"

    # (呼喊声)
    play sound fx.crowd
    "门外却在这时传来了嘈杂且成堆的声音！"

    voice "cv/linxi/linxi_0069.ogg"
    lx "我们从后门走吧。"

    "她挡在了我的面前。"
    "我只是点了点头，便向后门走去，前门挤了一堆人，虽然有点好奇，但感觉好像很麻烦的样子。"
    "我这人不太喜欢麻烦。"
    "于是我转身陪着林曦向后走去。"

    "向后走的时候，可以察觉到，自同学们那边传来的一些讨论说话声。"
    "而就在我走到门槛，一步踏出时——"

    voice "cv/jiangwanqing/jiangwanqing_0001.ogg"
    jwq "陈舟！"

    $ lx.show("惊讶", pos=right)
    voice "cv/linxi/linxi_0070.ogg"
    lx "！"
    
    cz "？"

    "叫我，谁？"
    "我收回了即将踏出门外的脚，缓缓回头。"
    stop sound

    # BGM切换：忧伤/有故事的曲子
    play music "audio/bgm/BGM_寂寞的温柔.ogg" loop fadein 1.0

    # 白屏淡入（背景 → 白）
    scene bg white with dissolve

    # 江晚晴登场
    $ lx.hide()
    show jwq 平静 at foot_to_head_scan
    $ renpy.pause(1.0)

    "那是一个怎样的女孩子啊……"
    # hide jwq with dissolve
    # $ jwq.show("平静", pos=center)
    "分明被周身的人群围绕着，却丝毫不见半点局促，她的存在感异常地将旁人压迫出一段距离，无人接近，却仍被其诱引。"
    "教室里的高亮度白炽灯打在她的头上，她自然的挺身而立，仅仅是站在儿，就不禁让人想到即将出鞘的宝剑，有种周遭空气为之一变的错觉。"
    "最重要的是——她的眼睛。"
    "强韧的意志，如火焰般闪烁在她的眼瞳中。"
    "人类的美，绝不是由外在的造型和脸庞所决定，否则的话，Galgame中由画师所创造的角色，不就成为这世上最美之物了吗？"
    "——人类的美，是由其生存姿态与行为方式决定，而这一切，会从皮肉中渗透而出，以气质的方式影响他人。"
    "眼前的女子，真正值得赞赏的，并非一眼看去就可得知的外貌。"
    "我被她瞳孔中的温度所熏染，心中，仿佛有着什么正蒸腾而出。"
    "若说是宝剑的话，那一定是……由神明所锻造而出，乃超越人类的存在赐下……这份光芒，让我如此想到。"

    voice "cv/jiangwanqing/jiangwanqing_0002.ogg"
    jwq "阿舟……"

    voice "cv/linxi/linxi_0071.ogg"
    lx "……咕…………"

    voice "cv/jiangwanqing/jiangwanqing_0003.ogg"
    jwq "我在找你。"

    "找我？"
    "为什么，会叫我阿舟？"
    "我没能出声。"
    "或许是没能意识到，她在对我说话。"

    voice "cv/jiangwanqing/jiangwanqing_0004.ogg"
    jwq "你……还记得我么？"

    "人影于背景中流淌，与眼前的女子交织在一起，好似电影中的叠化镜头，她的身影透明而虚幻，仅存糯湿鸦羽的黑色长发，流溢着光泽。"
    "看到那个姿态，我，想起来了。"

    cz "三年前，是你发现了事故后的我……我，还记得你。"

    "她的眼睛眯了一下，旋即笑了出来。"

    $ jwq.show("微笑")
    voice "cv/jiangwanqing/jiangwanqing_0005.ogg"
    jwq "呵呵，还记得就好。"

    "那真是一个温柔且端庄的笑容。"

    voice "cv/jiangwanqing/jiangwanqing_0006.ogg"
    jwq "那你可就不得不帮我咯？我来找你，正是因为需要你的协助。"

    "我真的十分感激她。"
    "这，就是缘分吧。"
    "或者说，是命运？"
    "事故那天，是我去参加天选试的日子，我走在路上，不小心被卡车撞了。"
    "而她，正是第一发现人。"
    "幸运的是，因为年纪尚小，浑身血供充足，所以我虽然做了几次手术，甚至差点要死掉，但属于少年的恢复力还是让我挺了过来，过了几年，连后遗症也没多少了。"
    "我很清楚，那是和时间赛跑的结果，若不是及时被好心人送进医院，等待着我的，很可能是一个更灰暗的未来……甚至，有无未来也尚未可知。"
    "好心人……江晚晴，这个身姿，我绝不会忘记。"
    "我要帮她。"

    cz "嗯，你说吧，我会尽一切可能去帮你。"

    "再造之恩，无以为报，只要不是涉及到天选试——"

    scene bg classroom2 with fade

    # BGM改变，欢快
    play music "audio/bgm/BGM_欢快2.ogg" loop fadein 1.0

    $ jwq.show("游刃有余")
    voice "cv/jiangwanqing/jiangwanqing_0007.ogg"
    jwq "那我就直说了，你，有女朋友吗？"
    
    $ lx.show("惊讶", pos=right)
    
    voice "cv/others/zhongren.ogg"
    "众人" "哎——！！！——！！！"

    "……………………？？什么意思？！"
    "这，这……我？"
    "突如其来的问题，让我整个人都懵了。"

    $ lx.show("萌怒")
    $ lx.act(anim_shake)

    voice "cv/linxi/linxi_0072.ogg"
    lx "江晚晴，你到底要干什么？！"

    voice "cv/tongxuea/tongxuea_0016.ogg"
    "同学A" "什么情况，舟少，你认识她？不是吧！她就是那个，今天刚入学的大佬啊！"
    voice "cv/tongxueb/tongxueb_0010.ogg"
    "同学B" "有故事有故事？我靠，这，这他妈，不对啊，你怎么回事？\n这，人家刚入学就……啊？快点如实招来！"

    "周围的人挤成了一窝蜂，各种各样的声音涌来，有惊叹，有艳羡，有疑惑……"
    "最多的，是难以置信的、发自内心的震惊！"
    "刚注意到林曦那不同寻常的反应，我的思绪就被身边的四五六种情绪给冲得七零八落。"

    $ jwq.show("微笑")
    "而江晚晴……她却只是神色莫名地看着我这边，对我绽放着可爱微笑，还眨了眨眼。"
    "……她真好看。"
    "不，不对……到底什么意思？"
    "眼看着事态就要继续升级，不给个回答，看来是不行了！"
    "爱怎么样怎么样吧，我不管了！"

    with vpunch
    cz "听好了，我有女友的！而且，我们之间，十分相爱！"

    voice "cv/tongxuea/tongxuea_0017.ogg"
    "同学A" "啊？不是，哥们。"

    cz "她非常可爱，有着一头纯洁的银发，轻飘飘的，可以感受到那种梦幻感和破碎感，你懂那种感觉吗？"
    cz "就是那种触之即碎、如梦似幻的存在感，仿佛身边有着一层光晕般，啊啊啊，是的，我每天一回到家，就要吸收我的女友能量，她是我最喜欢的游戏里的女孩子……"

    "不知怎么，随着我的念叨，身边的人都沉默了……"
    "额，嗯？我，我没说错话吧？"

    $ jwq.show("叹气")
    voice "cv/jiangwanqing/jiangwanqing_0008.ogg"
    jwq "……哎。"

    "她紧闭着双眼，长叹了一口气，唔，这是无奈？无语？"
    "好吧，看来是我理解错了。"

    $ lx.show("白眼")
    voice "cv/linxi/linxi_0073.ogg"
    lx "……额…………"

    "曦曦，你怎么也这样？！"

    $ jwq.show("微笑")
    voice "cv/jiangwanqing/jiangwanqing_0009.ogg"
    jwq "我知道的，那个女孩子，叫做小涟对吧。"

    cz "啊？！你怎么知道？"

    $ jwq.show("游刃有余")
    voice "cv/jiangwanqing/jiangwanqing_0010.ogg"
    jwq "你很出名的，不只是你的学校，有人把你发到网上去了，论坛里也有人在讨论你，我当然会知道她的名字。"

    cz "呵呵，原来是这样，那我懂了。"

    "她窥视着我的表情，好像是在担忧什么。"
    "为什么她在我的面前，隐约间就失去了那种锋利的感觉？"

    cz "不用担心，我们的爱情比天高，别小看我，我可是很严肃地在践行着我的生存哲学，一些言语上的置喙根本不算什么。"

    $ jwq.show("微笑")
    voice "cv/jiangwanqing/jiangwanqing_0011.ogg"
    jwq "……那就好。"

    $ lx.hide()
    $ jwq.show("微笑", zoom=2, transition=dissolve, y_offset=2100)
    "她的声音不知不觉间柔和了许多，向我靠近过来——这个距离，已经不是同学之间的正常距离了吧。"

    voice "cv/jiangwanqing/jiangwanqing_0012.ogg"
    jwq "我刚刚……问你女朋友，其实，就是在问小涟的事。"

    cz "咦？还有小涟的事？可是……"

    $ jwq.show("平静")
    voice "cv/jiangwanqing/jiangwanqing_0013.ogg"
    jwq "我知道的，她是一个Galgame中的女主角对吧？"

    cz "是，是这样没错，但她可是真实存在的哦，在我的世界里……"

    voice "cv/jiangwanqing/jiangwanqing_0014.ogg"
    jwq "……是的，我就是为了这个而来。"

    cz "？"

    $ jwq.show("坚定")
    voice "cv/jiangwanqing/jiangwanqing_0015.ogg"
    jwq "我……对今年的天选试，有想法。"

    $ jwq.show("计划通")
    voice "cv/jiangwanqing/jiangwanqing_0016.ogg"
    jwq "我认为你的经历，你的爱情，是一个非常好的观察样本，可以让我了解，一个人到底要如何去爱一个不存在的角色……"
    voice "cv/jiangwanqing/jiangwanqing_0017.ogg"
    jwq "这对于Galgame研究来说，是非常有价值的情报。"

    cz "唔……"

    "想了想，她说的确实有一些道理。"
    "更何况人家还是我的救命恩人，如果只是想看一看我的生活，看看平时在干什么，问问话的话，对于我个人而言，也并不是很排斥。"

    $ jwq.show("微笑")
    voice "cv/jiangwanqing/jiangwanqing_0018.ogg"
    jwq "我们之间，也有不少缘分，不是么？"
    voice "cv/jiangwanqing/jiangwanqing_0019.ogg"
    jwq "我希望，你可以配合我，作为回报……"

    # 贴耳小声
    $ jwq.show("游刃有余")
    voice "cv/jiangwanqing/jiangwanqing_0020.ogg"
    jwq "你想参与天选试对吧？"

    cz "……！"

    voice "cv/jiangwanqing/jiangwanqing_0021.ogg"
    jwq "我会辅导你的，一 · 对 · 一 · 辅 · 导。"

    $ jwq.show("游刃有余", zoom=1, y_offset=0)

    $ lx.show("萌怒", pos=right)
    $ lx.act(anim_jump)
    voice "cv/linxi/linxi_0078.ogg"
    lx "你们在说什么悄悄话！舟子，告诉我！\n还有，江、江晚晴，我、我忍不了你，放学后别走！"
    
    "……"
    # === 场景：街道-黄昏 ===
    # 模拟快速逃离后的场景切换
    scene bg street2_2 with dissolve 
    stop music fadeout 2.0 

    "………………"
    "感到事情不妙，我在众多争吵中、围堵中，艰难逃了出来。"

    cz "我去……"
    cz "哈，呼——呼嗤。"

    "好累，哎？原来，我们学校里，有这么多人吗？"
    "想起刚才那副地狱绘卷，我不由得流下一丝冷汗。"
    "坏了，感觉，今后的日子，不好过了……"
    "曦曦好像没跟上来，但看她似乎也有别的事，好吧，今天只能一个人回家了。"

    "………………"

    # 隐藏对话框

    # 使用你在 1-1 中定义的 screen 来展示最后的心理独白
    "缓缓走在斑驳的树叶下，黄昏的光如碎片般洒在眼角。"
    "我心中咕噜咕噜的复杂情绪向外冒泡，无法抑制。"
    "总感觉，自己招惹上了不得了的人啊……"
    "好累，想回家休息了。"

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