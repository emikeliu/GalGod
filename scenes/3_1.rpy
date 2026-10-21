# --- 额外角色定义 ---
define zhengke = Character("政客", color="#ffffff")

label scene_3_1:

    # ==========================================
    # 场景：街道（白天）
    # ==========================================
    scene bg street2_1 with Dissolve(2.0)
    play music "audio/bgm/BGM_日常.ogg" loop fadein 1.0

    "一夜过去。"
    "第二天，本以为我的世界有了些许的改变。"
    "结果……并没有？"

    $ lx.show("白眼", pos=left, x_offset=250)
    voice "cv3/linxi/linxi_0001.ogg"
    lx "都说了你能不能不要凑过来，这周对我来说很重要的……"

    $ jwq.show("游刃有余", pos=right, x_offset=-250)
    voice "cv3/jiangwanqing/jiangwanqing_0001.ogg"
    jwq "嚯？是吗？这下不得不来了。"

    "我们三个人在前往校园的路上打闹着，两个女人在我的身边吵吵闹闹，甚至让我有点烦。"
    "这、这不就是，之前那种平凡的、平凡的，上学路么。"
    "……"
    "咦？是我个人太多愁善感了？"

    $ lx.show("萌怒")
    $ lx.act(anim_jump)
    voice "cv3/linxi/linxi_0002.ogg"
    lx "不是都说好了，要先走我的线么，现在就是吧？应该还没结束吧？你一边去，一边去，现在是我的回合！"

    $ jwq.show("微笑")
    voice "cv3/jiangwanqing/jiangwanqing_0002.ogg"
    jwq "哎，你啊，是情弱呢。"

    $ lx.show("惊讶")
    voice "cv3/linxi/linxi_0003.1.ogg"
    lx "情，情弱？"

    voice "cv3/jiangwanqing/jiangwanqing_0003.ogg"
    jwq "情报弱者的意思，就是说，你真是什么都不知道啊。"

    $ lx.show("欲言又止")
    voice "cv3/linxi/linxi_0003.ogg"
    lx "嘎？难道，已经没我什么事了。"

    "曦曦一脸呆呆的表情，不敢置信的这幅模样还怪可爱的，好想给她拍下来。"

    $ jwq.show("眯眼")
    voice "cv3/jiangwanqing/jiangwanqing_0004.ogg"
    jwq "呵呵呵呵……"

    $ jwq.show("计划通")
    voice "cv3/jiangwanqing/jiangwanqing_0005.ogg"
    jwq "还没收到通知吗？阿舟已经决定了，现在是我的线路，是的，昨天晚上，我就和阿舟见面了，在你之后呢。"

    cz "啊？"

    "怎么还有我的事……\n不对不对，我是这一次模拟的主人公，当然有我的事，不过，怎么感觉好像和江晚晴说的不一样……"

    "江晚晴无视了我的反应，只是单纯以一副尽在掌握的表情，对曦曦说着话。"

    $ jwq.show("游刃有余")
    voice "cv3/jiangwanqing/jiangwanqing_0006.ogg"
    jwq "意思就是，你的回合已经过去了，现在是我的回合，碍事的是你呀。"

    $ lx.show("惊讶")
    $ lx.act(anim_shake)
    voice "cv3/linxi/linxi_0004.ogg"
    lx "唉，唉唉唉唉？？？\n——是，是这样吗？哎？我，我还以为我的线路，起码要走一个星期呢。"

    "她看向了我，我心底咯噔一下。"

    $ lx.show("哭哭")
    voice "cv3/linxi/linxi_0005.ogg"
    lx "……呜，呜呜呜，我，我明明还想在这个周末……呜呜，舟子，你，你放弃我了吗？是我不够可爱吗？难道说我和你约会，你其实没那么开心，都是在哄我……"

    cz "我不是，我没有……"

    $ lx.show("萌怒")
    voice "cv3/linxi/linxi_0006.ogg"
    lx "我的线路只有一天什么的，那种事情不要啊！！！"

    "我话还没说完，就被她给打断。"
    "她们俩走在街上本就是一道靓丽的风景线，已经够引人注目的了。\n现在闹出这么大动静，更是引得路人纷纷驻足将视线投过来。"
    "最熟悉她的我，非常清楚如何让她冷静下来，这里不能再耽误了。"

    cz "啊是的，你的个人线，我已经走完了。"

    voice "cv3/linxi/linxi_0007.ogg"
    lx "呜呜……"

    cz "不过，她的我也走完了。"

    $ lx.show("惊讶")
    voice "cv3/linxi/linxi_0008.ogg"
    lx "唉？"

    cz "因为现实Galgame这种存在，我已经完全理解了。"
    cz "这对我十分有用，必将活用于下一次……"

    $ jwq.show("微笑")
    voice "cv3/jiangwanqing/jiangwanqing_0007.ogg"
    jwq "哎呀哎呀~是这样吗，这可真是。"

    "其实我也有点难以应对她们……要是再和她们多接触一点，再多接触一点点……说不定……"


    stop music fadeout 1.0
    cz "而且……现在，我想要把心思放在天选试上。"

    $ lx.show("忧伤")
    $ jwq.show("平静")
    play music "audio/bgm/BGM_月夜温柔.ogg" loop fadein 2.0
    voice "cv3/linxi/linxi_0009.ogg"
    lx "……"
    voice "cv3/jiangwanqing/jiangwanqing_0008.ogg"
    jwq "……"

    "空气中出现了诡异的沉默。"
    "一息前的欢乐光影仿佛是幻觉一般，走在我一左一右的两个女孩，她们目光看了过来，扎得我生疼。"

    voice "cv3/jiangwanqing/jiangwanqing_0009.ogg"
    jwq "小涟？"

    "她只说了一个名字，但我清楚她想问什么。"

    cz "……嗯。"
    cz "是，也不是。"
    cz "天选试，是一个契机，我或许可以找清楚我的本心。"

    $ jwq.show("微笑")
    voice "cv3/jiangwanqing/jiangwanqing_0010.ogg"
    jwq "是吗，那我就放心了，我只希望，你能做出不后悔的选择。"

    "经过昨晚，她好像对什么释怀了一般，甚至能够用这么温柔的声音对我说话。"
    "她有所改变了吗？这个改变对她而言是好的吗？对我而言是好的吗？"
    "不过，我也没什么立场去多嘴……"
    "突然觉得……心有点痛。"
    "我不想，我不想，不想失去任何人。"

    cz "我真的不想，失去小涟……"

    play sound fx.crowd loop fadein 1.0
    "而就在这时，另一边传来了熙熙攘攘的闹腾声音，将我的喃喃碎语盖过，不知不觉间，我们又靠近了学校。"

    $ lx.show("平静")
    voice "cv3/linxi/linxi_0010.ogg"
    lx "咦，那边不是我们上次见到的官员么？"

    "我看向林曦指的方向。"

    cz "还真是！"

    $ jwq.show("平静")
    "估算下时间的话，或许是和天选试有关。"

    # voice "cv3/jiangwanqing/jiangwanqing_0011.ogg"
    jwq "……"

    $ jwq.hide()
    $ lx.hide()
    show sdcg 002 with dissolve

    voice "cv3/others/zhengke_0001.ogg"
    zhengke "各位乡亲，各位媒体朋友，今天，我可以站在这里，荣幸地告诉大家。"

    "簇拥的媒体和比上次更多的民众，让现场显得有些拥挤。"

    show sdcg 001 with dissolve

    play sound fx.camera
    voice "cv3/others/zhengke_0002.ogg"
    zhengke "就在先前，我收到了正式通报。经过慎重评估与统筹，本届天选试，我们省的名额……增加了一个。"

    "话音落地，瞬间的寂静！"

    play sound fx.camera
    with flash
    pause 0.15

    play sound fx.camera
    with flash
    pause 0.15
    "然后，随着闪光灯的咔咔作响，簇拥着的人们开始喧闹起来。"

    cz "……真的，多了一个……"

    "我不敢置信。"

    voice "cv3/linxi/linxi_0011.ogg"
    lx "哇，真的，舟子，是不是之前那个线上的请愿书有了效果。"

    cz "可能吧。"

    "不过据我的了解，最近这些年，省里并没有什么特别大的动作，经济增长也很普通。"
    "别看只多了一个名额，这一个，可是这个国家未来的支柱之一……"
    "是妥协的产物？是平衡的艺术？还是他个人政治能量的直接体现？"
    "亦或者，是省里出了什么我不知道的，Galgame领域圣子圣女？毕竟顶级背景自有顶级的方便。"

    show sdcg 002 with dissolve
    voice "cv3/others/zhengke_0003.ogg"
    zhengke "这是第一步，但绝不是最后一步！没错，这代表着我们的人才培养方向是正确的……"

    "那边站着的他，身材挺拔，面带得体的笑容，在笑容之下，他的眼神锐利如鹰。"

    voice "cv3/linxi/linxi_0012.ogg"
    lx "嗯…现在，我也想让你去参加天选试了……所以，应该是好事吧。"

    "她看着我的目光有些飘渺，似乎是在思考着什么遥远的事。"

    cz "好事，当然是好事，谢谢你支持我，曦曦……"

    "虽然还想听一会，但很可惜待不了那么久，要上课了。"
    "我们只在这停顿了一下子，就向着学校走去。"
    "离开之前，台上的那位官员，正用双眼扫动全场，在看向我这边时，目光交错而过，他……微微地眯起了眼。"
    "是在，看什么呢？"

    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene bg classroom1 with Dissolve(1.0)
    $ renpy.pause(2.0, hard=True)
    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene bg classroom2 with Dissolve(2.0)
    
    "……"
    "暮色如期漫过窗沿，将课桌染成朦胧的橘色。"
    "又一个白日，就这样在翻书声与偶尔响起的交谈中，安静地流逝而过。"
    "今天，毫无波澜。"
    "过了一整天，我自然而然察觉了，这看似平静的日常，暗地里还是有所变化。"
    "为了天选试而进行的Galgame大讨论也好，日间和她们偶尔的交谈也好，都让我有种蒙蒙昧昧的感觉，就像是隔了一层迷雾。"
    "想来就是这样吧。"
    "时间会流走，太阳会下山，启示录尚未翻页，审判却早已写在天空与大地之间……"
    "该来的那一天，不会失约。"
    scene bg street2_2 with Dissolve(2.0)
    "终于，我们各自怀着飘渺的心境，踏上了放学路。"
    "风吹过，带给我一缕凉意。"

    $ lx.show("平静", pos=left)
    voice "cv3/linxi/linxi_0013.ogg"
    lx "现实Galgame，已经结束了么。"

    $ jwq.show("平静", pos=right)
    voice "cv3/jiangwanqing/jiangwanqing_0011.ogg"
    jwq "早上就说了呢。"

    "就连她们的语气仿佛都比平时低了几度。"
    "所以我忍不住插嘴，想要将气氛带得活跃点。"

    cz "怎么，曦曦，你对这个的兴趣还挺大？"

    $ lx.show("闭眼微笑")
    voice "cv3/linxi/linxi_0014.ogg"
    lx "……哼哼，你猜。"

    "黄昏的残光打在我们三人身上，随着行走，三条影子如同指针旋转一般重叠在一起，然后再度分离。"
    "昨天的事情，还是对她们造成了影响。\n或许早上的那段时光，只是一种应激反应。"
    "当然……我认为，我受到的影响也不少就是了。"
    "确实有什么东西，不见了，抑或者说，回不去了。"

    $ lx.show("叹气")
    voice "cv3/linxi/linxi_0015.ogg"
    lx "这样也好吧，本来也想着，要是舟子太喜欢我了，一直舍不得离开我的线路，那才难办。"

    cz "……"

    "耳边的触感，宛如再度复苏了似的，让我的心跳略有加速。"
    "但是一想到她当时的表情，又让我一瞬间说不出话来。"

    $ lx.show("平静")
    voice "cv3/linxi/linxi_0016.ogg"
    lx "只有这样，回到了正常的关系，有的话说出来才有意义。"

    $ jwq.show("落寞")
    voice "cv3/jiangwanqing/jiangwanqing_0012.ogg"
    jwq "……是么，反正，应该和我无关吧。"

    $ lx.show("闭眼微笑")
    voice "cv3/linxi/linxi_0017.ogg"
    lx "和你有关哦，因为我要，打倒小涟。"

    cz "哎？"

    "打倒……小涟？"

    cz "什，什么意思？"

    "自己的语气，确实有点慌乱，但是，既然听到了，不管怎么样都不可能若无其事地左耳进右耳出，那可是我的女友啊。"

    $ lx.show("平静")
    voice "cv3/linxi/linxi_0018.ogg"
    lx "字面意思，我想让你放弃她。"

    cz "……"

    $ jwq.show("落寞")
    voice "cv3/jiangwanqing/jiangwanqing_0013.ogg"
    jwq "林曦，难道说，是我们最开始说的那个，你要，踏出那一步么……"

    "她们之间，似乎背着我说过些什么……"

    voice "cv3/linxi/linxi_0019.ogg"
    lx "是的。"

    "曦曦声音中所透出来的坚定意志，让我为之侧目。"
    "事到如今，我也没什么能插嘴的了，不如说，我的心里，也是一团乱麻。"

    voice "cv3/jiangwanqing/jiangwanqing_0014.ogg"
    jwq "……那，祝你成功。"

    "反观江晚晴，平日间威风凛凛的她，此刻却宛如一个落寞的小女孩。"
    "她们之间，简直就像是灵魂互换了一般。"
    "不，不对，或许，只是我一叶障目了。"
    "我早就知道的，曦曦一直是一个做事一往无前的女孩子，只是在我的面前太放松了。"
    "而江晚晴，在昨天……我也看到了她的另一面，所以，或许这也是她性格的一部分。"

    voice "cv3/linxi/linxi_0020.ogg"
    lx "说起来，我以前就一直是第二啊，不过，那时候已经释怀了的。"

    voice "cv3/linxi/linxi_0021.ogg"
    lx "但现在这种情况下，还是作为第二的话，我果然还是不服。"

    voice "cv3/linxi/linxi_0022.ogg"
    lx "小涟……她让一切的一切都乱套了。"

    voice "cv3/linxi/linxi_0023.ogg"
    lx "江晚晴，如果你一直不出现的话，或许我会就这样将错就错下去，但是既然你出现了，我就再也忍不了了。"

    voice "cv3/jiangwanqing/jiangwanqing_0015.ogg"
    jwq "……"

    "江晚晴只是咬着嘴唇，神色晦暗，她究竟在想什么？"
    "第二不第二的，曦曦又到底是要做什么，她要升到第一的话，应该不是在说什么学习成绩。"
    "根据她们的行动来看，是在说我吧……可我一直都觉得曦曦是我重要的人……"

    voice "cv3/jiangwanqing/jiangwanqing_0016.ogg"
    jwq "你……不用和我说，想做什么，就去做吧。"

    voice "cv3/jiangwanqing/jiangwanqing_0017.ogg"
    jwq "我早就已经没有执念了，所以不用顾虑我。"

    voice "cv3/linxi/linxi_0024.ogg"
    lx "是吗，就是这一点，让我觉得耿耿于怀啊，所以……"

    voice "cv3/linxi/linxi_0025.ogg"
    lx "所以，这周末你也来吧……\n或者说，你一定要来，来见证，我击败小涟的瞬间。"

    voice "cv3/jiangwanqing/jiangwanqing_0018.ogg"
    jwq "真的，对自己这么有信心吗。"

    "她的声音分明地在颤抖着。"

    $ lx.show("闭眼微笑")
    voice "cv3/linxi/linxi_0026.ogg"
    lx "是，我了解陈舟。"

    cz "……"

    "既然提到了小涟，如若说小涟是第一的话，在我这里，小涟是什么意义上的第一？"
    "答案，只有一个。"
    "——爱。"

    play sound fx.heartbeat
    "我心中一颤，回忆起了昨天的光影。"
    "有发丝的触感，有身前的温热，还有指尖连在一起时所感受到的那份心动……\n——回想起来的这一瞬，胸腔中的跃动感再次复苏。"

    $ jwq.show("落寞")
    voice "cv3/jiangwanqing/jiangwanqing_0019.ogg"
    jwq "……真是好残忍，……怕见灯前影，羞睹镜中人，我都已经到了这种地步了，你还想要，更彻底的打击我。"

    $ lx.show("微笑")
    voice "cv3/linxi/linxi_0027.ogg"
    lx "……"

    "曦曦没能回话，只是用幽邃的目光看着她。"

    $ jwq.show("叹气")
    voice "cv3/jiangwanqing/jiangwanqing_0020.ogg"
    jwq "也罢，这样就好。"

    voice "cv3/jiangwanqing/jiangwanqing_0021.ogg"
    jwq "就当是一报还一报，作为始作俑者，这点背负的觉悟还是不缺的。"

    $ jwq.show("挺好颜")
    "她那副仿佛释怀了的语气，让我胃里沉甸甸的。我不想，不想看到江晚晴露出这种表情……"

    cz "所以说啊，小涟到底是……怎么你们了……"

    "明明已经在好好思考了，纠结也纠结过了。"
    "我喜欢她，真的会有这么大的困扰吗……"
    "我的世界，和她们的世界之间，到底……"

    $ lx.show("白眼")
    voice "cv3/linxi/linxi_0028.ogg"
    lx "呸呸~~大猪头，左一个小涟，右一个小涟的，虽然不怪你，但是听了这话我可是会生气的，她也会生气的。"

    cz "……哦，哦哦。"

    "好吧，那我还是不说话了。"

    $ jwq.show("叹气")
    voice "cv3/jiangwanqing/jiangwanqing_0022.ogg"
    jwq "呵呵，是呀，只有这一点，是怎么样都难以接受的。"

    "连你也这样说？！"

    "……"

    scene bg street1_2 with Dissolve(2.0)
    $ renpy.pause(2.0, hard=True)

    $ jwq.show("微笑")
    $ lx.show("微笑")
    "平凡至极的归途上，我们一路走着。"
    "感受着她们的气息，我眯起了眼。"
    "有什么确实已悄然改变，但某些更深处的什么，或许从未动摇，也永不会动摇。"
    "她们微微走在前面一步，自遥远天际漫来的光，将两人的影子轻轻投在我身上。"
    "我透过朦胧的滤镜看向她们，心中竟不可置信地平静了下来\n——昨天、今天、明天……所有的杂音都无法侵入这方小小世界。"
    "说着一些无关紧要的想法，谈着一些可有可无的日常，\n我们就这样，走着，走着。"
    "就好像会一直这样走下去。"

    cz "说起来，我最近玩了一部Galgame……"

    "不如说，我多希望我们能一直这样走下去。"
    "曦曦，一直都是我重要的人。"
    "晚晴，也渐渐变得重要起来。"
    "贪婪又心胸狭窄的我所妄想的，是比悠远天空还要更悠远的空虚之事。"

    stop music fadeout 2.0
    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene black
    $ renpy.pause(1.0, hard=True)
    
    $ lx.reset_position()
    $ jwq.reset_position()
    $ xl.reset_position()
    return