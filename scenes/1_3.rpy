label scene_1_3:

    # 【教室（夜）】
    scene bg classroom3 with fade
    
    # 剧本气氛：冷清、寂静。
    play music "audio/bgm/BGM_沉闷.ogg" loop fadein 1.0

    # 旁白描写
    "黄昏过后，暮色如潮水般漫进这间位于三楼的教室，无声无息。"
    "在这本应是吃饭的好时间里，教室中的气氛，那种温馨的烟火气息丝毫不存。"
    "这里什么人都没有，是一间空教室。"
    "空气还残留着白日里粉笔灰与少年汗水混合的气息，此刻却被一种铅灰色的寂静所凝固。"
    "窗外，远处食堂的灯火与隐约的喧闹，像是从另一个世界传来，非但没能驱散这里的冷清，反而像隔着磨砂玻璃看到的暖色光景，可望不可即。"
    
    "而这样一个世界，终于在冷寂的气氛下，迎来了它的搅局者——"

    # 角色入场：对峙状态
    # 林曦在左，江晚晴在右
    $ lx.show("平静带怒", pos=left, x_offset=250)
    $ jwq.show("平静", pos=right, x_offset=-250)

    voice "cv/linxi/linxi_0079.ogg"
    lx "……"
    voice "cv/jiangwanqing/jiangwanqing_0022.ogg"
    jwq "……"

    "林曦给人的感觉完全变了模样，分明是同样的身影与装饰，内在的神韵却已截然不同。"

    voice "cv/linxi/linxi_0080.ogg"
    lx "江晚晴，你为什么要来。"

    $ jwq.show("微笑")
    voice "cv/jiangwanqing/jiangwanqing_0023.ogg"
    jwq "呵呵，不是你叫我，放学后别走吗。"

    voice "cv/linxi/linxi_0081.ogg"
    lx "不要在我面前转移话题，你知道的，我不是在说这个意思。"

    "沉静、冷澈，眼前的林曦有如被注入了新的灵魂，那些构成她人形的线条，此刻正散发着一种近乎实质的、凝练的张力。"
    "江晚晴的心中产生了一丝讶异，自己记忆里的她，并不会给人这样的感觉。"

    $ jwq.show("眯眼")
    voice "cv/jiangwanqing/jiangwanqing_0024.ogg"
    jwq "……嗯，该从哪里说起呢。"

    "经年累月习得的端庄礼仪，没有让她露出半分心中所想。"
    "她装模做样地思考了一番，旋即像是真的临时想到了什么一样。"

    $ jwq.show("微笑")
    voice "cv/jiangwanqing/jiangwanqing_0025.ogg"
    jwq "我在想，你，果然还是不行啊，阿舟还是不能交给你。"

    voice "cv/linxi/linxi_0082.ogg"
    lx "……"

    "四目相对，林曦毫不为之动摇，江晚晴只是笑意更浓。"

    $ jwq.show("游刃有余")
    voice "cv/jiangwanqing/jiangwanqing_0026.ogg"
    jwq "你刚刚没见到么？我和他…初次见面，他居然就误会我在向他告白，这意味着什么，我想你很清楚吧。"

    "刻刀般精准的话语。"
    "果然，林曦的脸上浮现出扭曲之色，这对于十数年来待在陈舟身边，却完全不被视为女孩子的她而言，是处于绝对上位的压制。"

    $ lx.show("平静带怒")
    voice "cv/linxi/linxi_0083.ogg"
    lx "那又怎么样？你难道不清楚？他现在的情况。"

    $ jwq.show("平静")
    voice "cv/jiangwanqing/jiangwanqing_0027.ogg"
    jwq "清楚又怎样？正是因为清楚，所以我才来了。"

    "二人的立场完全不同，但却微妙地在遥远的远端形成了交集。"

    voice "cv/linxi/linxi_0084.ogg"
    lx "你既然什么都知道的话，就不应该再靠近陈舟了，过了三年，终于还是忍不住了么？"

    $ jwq.show("微笑")
    voice "cv/jiangwanqing/jiangwanqing_0028.ogg"
    jwq "嗯，要说忍不住的话，确实，我忍不住，这很正常。"
    voice "cv/jiangwanqing/jiangwanqing_0029.ogg"
    jwq "不过，我也并非单单为此而来。"

    voice "cv/linxi/linxi_0085.ogg"
    lx "江晚晴，你有些事……能不能说清楚？"

    $ jwq.show("游刃有余")
    voice "cv/jiangwanqing/jiangwanqing_0030.ogg"
    jwq "哎，也别把我当成什么要偷人东西的小偷啊，这样我会很伤心的。"

    voice "cv/linxi/linxi_0086.ogg"
    lx "哼，我看，不是小偷，而是灾星才对。"

    $ jwq.show("挺好颜")
    voice "cv/jiangwanqing/jiangwanqing_0031.ogg"
    jwq "随你怎么说吧，我已经决定好的事，你没有什么说话的余地。"

    "事实如此，她作为通过天选试第二轮的人，哪怕是校长也能指挥得动，在一个小小学校里呼风唤雨，根本不成问题。"
    "可眼前的少女却丝毫不把她的话语放在耳中，\n江晚晴敏锐的察见，林曦眼中寄宿着的，是绝不逊于自己的意志。"
    "幽邃、深远，有如一汪万年深潭，\n仅仅是存在于那里，就散发出了日积月累的、坚实的强。"
    "这万万不是一个能简单对待的对手。"

    $ lx.show("忧伤")
    voice "cv/linxi/linxi_0087.ogg"
    lx "我没有资格干涉你，但我至少……可以挡在前面。"
    voice "cv/linxi/linxi_0088.ogg"
    lx "若是做出出格举动，我会阻止你的，哪怕要被陈舟反感。"

    $ jwq.show("嫌弃")
    voice "cv/jiangwanqing/jiangwanqing_0032.ogg"
    jwq "……"

    "作为“外来”的狼，江晚晴没有办法绕过眼前的外婆，直取小红帽，她不得不感到一丝无奈。"

    $ jwq.show("叹气")
    voice "cv/jiangwanqing/jiangwanqing_0033.ogg"
    jwq "我可不想事事都被你搅局啊，哎，想想就很麻烦。"
    voice "cv/jiangwanqing/jiangwanqing_0034.ogg"
    jwq "其实，我也并不会做什么，起码对你来说，是这样的。"

    $ lx.show("平静")
    voice "cv/linxi/linxi_0089.ogg"
    lx "究竟如何，我会自己判断，你只需要告诉我你的目的即可。我会和陈舟一起互相印证，哼，他肯定会配合我。"

    "啧，这就是青梅竹马的余裕么，这种无条件的相信，让江晚晴一直以来都觉得非常碍事。"
    "一想到这儿，她总是会难得地升起一丝火气来。"

    $ jwq.show("游刃有余")
    voice "cv/jiangwanqing/jiangwanqing_0035.ogg"
    jwq "如果我主动靠近他，你难道还有什么立场来阻止我不成？"
    voice "cv/jiangwanqing/jiangwanqing_0036.ogg"
    jwq "你可别忘了…你只是一个好朋友而已。"

    $ lx.show("鼓嘴气气")
    voice "cv/linxi/linxi_0090.ogg"
    lx "咯……"
    voice "cv/linxi/linxi_0091.ogg"
    lx "……我知道自己算不上什么，你不用提醒我。"

    $ jwq.show("计划通")
    voice "cv/jiangwanqing/jiangwanqing_0037.ogg"
    jwq "我可是天降，而且理由充足，无论怎么行事，只要阿舟自己认可，你也好别人也好，没人能挡路。"

    "但是，林曦的容许，是一定需要的。"
    "可能林曦自己都不知道吧，她在阿舟的眼里究竟是有多么重要，江晚晴在这点上有着极度清晰的认知。"
    "自然而然，在初步的逼迫后，少女主动做出了退步姿态。"

    $ jwq.show("平静")
    voice "cv/jiangwanqing/jiangwanqing_0038.ogg"
    jwq "不过呢…跟你说也没什么，毕竟这并不算是什么需要保密的计划，我只是，想要让他通过天选试而已。"

    $ lx.show("平静带怒")
    $ lx.act(anim_jump)
    voice "cv/linxi/linxi_0092.ogg"
    lx "天选试？"
    
    voice "cv/linxi/linxi_0093.ogg"
    lx "这怎么可能？先不说你为什么要这么做，天选试作为一步登天的天梯，究竟有多大的含金量，你应该是最清楚的。"
    voice "cv/linxi/linxi_0094.ogg"
    lx "怎么才能做得到「让」他通过？不会是在做什么危险的事吧。"

    $ jwq.show("游刃有余")
    voice "cv/jiangwanqing/jiangwanqing_0039.ogg"
    jwq "放心，我已经安排好一切了，对你们来说，不会有太大的感知。"

    voice "cv/linxi/linxi_0095.ogg"
    lx "……"

    "林曦讨厌眼前的家伙游刃有余的样子。"
    "但她只能沉默，在这个领域，她完全没有任何了解，而江晚晴则是毫无疑问的专家，不仅从小就被精英教育，耳熏目染，长大后还亲身参与其中，具备无可置疑的说服力。"
    "对此，林曦不需要有回应，所以，她只是提出了一个关键的问题。"

    voice "cv/linxi/linxi_0096.ogg"
    lx "为什么？"
    voice "cv/linxi/linxi_0097.ogg"
    lx "你为什么要这么做？"

    $ jwq.show("微笑")
    voice "cv/jiangwanqing/jiangwanqing_0040.ogg"
    jwq "为什么？当然是因为，你的做法，让我看不到希望——你，不行。"
    voice "cv/jiangwanqing/jiangwanqing_0041.ogg"
    jwq "这些年来，我也不是完全在观望，暗地里可是辛苦做了许多的，回头来看，我未雨绸缪得没错……让你待在阿舟的身边，根本就起不到什么建设性的效果，空耗时间罢了！"
    voice "cv/jiangwanqing/jiangwanqing_0042.ogg"
    jwq "一年不行，两年不行，三年四年、五年十年，照样不可行，阿舟的情况，已经没有任何平缓结果的余地了。"

    $ lx.show("鼓嘴气气")
    $ lx.act(anim_shake)
    voice "cv/linxi/linxi_0098.ogg"
    lx "那又如何！难道就这样平平安安地生活下去，不好吗？！"
    voice "cv/linxi/linxi_0099.ogg"
    lx "你到底是站在你自己的立场上说出的这话，还是真的在陈舟的立场上考虑过了？轻易地插手，有没有想到过后果是什么！"

    $ jwq.show("落寞")
    voice "cv/jiangwanqing/jiangwanqing_0043.ogg"
    jwq "……"

    "在江晚晴的回忆里，林曦除了恋爱外，于其他的事务上均十分有主见，是热烈有激情的性子……一看到这般模样，果然就能发觉，她的内核其实一直没变。"
    "……如果这不是由针对自己的攻击性而转化出来，就好了。"
    "我们之间，或许再也回不去那时了。"

    $ lx.show("平静")
    voice "cv/linxi/linxi_0100.ogg"
    lx "你根本回答不了吧，困在老黄历里出不来的女鬼，还想从活人身上吸取温暖，哪有这种好事。"

    play music "audio/bgm/BGM_孤独夜晚.ogg" loop fadeout 2.0 fadein 2.0
    voice "cv/jiangwanqing/jiangwanqing_0044.ogg"
    jwq "……我的确，很怀念以前……但那，绝不是我的本心。"

    "江晚晴的语气，第一次产生了动摇。"

    voice "cv/jiangwanqing/jiangwanqing_0045.ogg"
    jwq "我这一次……也不是，想要来再续前缘的。"

    "这完完全全就只是一个十来岁少女的表情，绝非某个大人物高高在上的面孔，不知何时起，有一层隐形的衣袍从她身上褪了下来，林曦发现了，所以……她除了咬牙外，什么都做不了。"

    voice "cv/jiangwanqing/jiangwanqing_0046.ogg"
    jwq "你是可以一直帮衬他，我也认为……你是最好的对象。"
    voice "cv/jiangwanqing/jiangwanqing_0047.ogg"
    jwq "但是，你能在他身边待上3年、5年，还能在他身边待上30年、50年吗？"

    $ lx.show("平静带怒")
    voice "cv/linxi/linxi_0101.ogg"
    lx "我……"

    $ jwq.show("坚定")
    voice "cv/jiangwanqing/jiangwanqing_0048.ogg"
    jwq "青春、活力。我们现在无论是肉体还是心灵，都正处于最巅峰的时期，很多事情都可以抛到脑后去……"
    voice "cv/jiangwanqing/jiangwanqing_0049.ogg"
    jwq "但是将来，你也好他也好，在日复一日的闲言碎语下，在年复一年的不可企及下，究竟又能坚持多久呢？人的意志力是有极限的，它会随着肉体的衰老和时间的流逝而被慢慢消磨，直到再也绷不住那根弦的日子到来。"

    $ jwq.show("指摘")
    # 逐渐激动
    $ jwq.act(anim_shake)
    voice "cv/jiangwanqing/jiangwanqing_0050.ogg"
    jwq "你难道要等到那一天么？到那时，就晚了！"

    "林曦无言以对，因为江晚晴的话实在是再正确不过。"
    "但她的感性，还是无法让她就此认同，因为……"

    $ lx.show("忧伤")
    # 语调要缓、轻，低沉
    voice "cv/linxi/linxi_0102.ogg"
    lx "……你就不怕，陈舟再一次被你所害么。"

    $ jwq.show("恐惧")
    $ jwq.act(anim_shake)
    voice "cv/jiangwanqing/jiangwanqing_0051.ogg"
    jwq "噫——"

    "第一次，这个无论被谁指摘都宛如青山松雪一般的少女，第一次流露出了带颤的恐惧。"

    voice "cv/jiangwanqing/jiangwanqing_0052.ogg"
    jwq "我…我，没有想要……这样的，不，不是……"

    "要形容的话，就像是一只无措的幼兔。"
    "看到这样的她，林曦竟感同身受，不自觉地有种流泪的冲动。"
    "不行啊，怎么可以……我，真的是一个笨蛋。"

    voice "cv/linxi/linxi_0103.ogg"
    lx "对不起…我不是在怪你。"
    voice "cv/linxi/linxi_0104.ogg"
    lx "那只是一个事故，不幸的…事故，不是你的错，也不是他的错。"
    voice "cv/linxi/linxi_0105.ogg"
    lx "你说的我能懂…陈舟的认知失调，如果没有外力影响，可能一辈子也不会好转了，明明待在他身边的我是最清楚的。"

    "少女看着眼前仿佛坠入恐怖回忆中的旧识好友，仿佛肠胃被拧紧了一般。"

    voice "cv/linxi/linxi_0106.ogg"
    lx "……对不起。"

    $ jwq.show("尴尬")
    voice "cv/jiangwanqing/jiangwanqing_0053.ogg"
    jwq "啊……嚇…呼，没，没事……"

    "带着一点残留的失态，她很快就缓了过来。"

    $ jwq.show("平静")
    voice "cv/jiangwanqing/jiangwanqing_0054.ogg"
    jwq "……我们都知道，他想去天选试的目的，那或许能成为一个契机。"

    voice "cv/linxi/linxi_0107.ogg"
    lx "小涟……"

    "这个名字的提出，让两个人都僵了一会儿。"

    $ jwq.show("嫌弃")
    voice "cv/jiangwanqing/jiangwanqing_0055.ogg"
    jwq "是，小涟。那个Galgame角色……"

    "林曦欲言又止，只是手不自觉地握紧。"

    voice "cv/jiangwanqing/jiangwanqing_0056.ogg"
    jwq "她已经，成了阿舟的魔障了。"
    
    "江晚晴断言。"

    voice "cv/jiangwanqing/jiangwanqing_0057.ogg"
    jwq "阿舟居然，在和她这样一个完全不存在的虚拟角色…谈恋爱。"
    voice "cv/jiangwanqing/jiangwanqing_0058.ogg"
    jwq "这些年来，暗示也好，明示也罢，我相信你应该都尝试过了吧。"
    voice "cv/jiangwanqing/jiangwanqing_0059.ogg"
    jwq "想必是毫无办法。"

    "陈舟是不想听，还是说根本就听不见呢？"
    "这是个禁忌的话题，二人不想对此过多深入。"

    $ lx.show("叹气")
    voice "cv/linxi/linxi_0108.ogg"
    lx "……无言以对呢，我甚至已经，习惯陈舟的说话方式、生活习惯了。"
    voice "cv/linxi/linxi_0109.ogg"
    lx "他已经沉浸在自己的世界里了，和我们眼里的，完全不一样。"

    $ jwq.show("计划通")
    voice "cv/jiangwanqing/jiangwanqing_0060.ogg"
    jwq "呵呵，这真是和我所想不差。"
    voice "cv/jiangwanqing/jiangwanqing_0061.ogg"
    jwq "所以，我认为之后是一个好时机…依靠天选试，既然他如此相信的话……"
    
    $ jwq.show("坚定")
    voice "cv/jiangwanqing/jiangwanqing_0062.ogg"
    jwq "省考，我会让他通过的，绝对。"
    
    "少女的声音散发着绝不容拒绝的威严。"

    $ lx.show("忧伤")
    voice "cv/linxi/linxi_0110.ogg"
    lx "……可是。"
    voice "cv/linxi/linxi_0111.ogg"
    lx "他可是想要在天选试上，让小涟「诞生」啊，他非常相信这一点。"

    $ jwq.show("嫌弃")
    voice "cv/jiangwanqing/jiangwanqing_0063.ogg"
    jwq "……远古的传说呢，简直和都市传说一样不靠谱。"

    voice "cv/linxi/linxi_0112.ogg"
    lx "但他还是信了。"
    voice "cv/linxi/linxi_0113.ogg"
    lx "……"

    "二人对这一点心知肚明，可仍然毫无办法，林曦在这些年里，该做的都做遍了。"

    voice "cv/linxi/linxi_0114.ogg"
    lx "我还是无法同意让他通过天选试，你是想要辅导他，让他通过第一道选拔吧。"
    voice "cv/linxi/linxi_0115.ogg"
    lx "如果一切顺利，你也真的能做到让他第二关百分百通过的话……那样的话，不就真的会让他实现心愿了吗。"
    voice "cv/linxi/linxi_0116.ogg"
    lx "你要知道，他的世界是和我们不一样的，就算现实世界里什么都不会发生，在他的世界里…肯定也会发生什么。"
    voice "cv/linxi/linxi_0117.ogg"
    lx "这难道不是一种心理强化？那样对他真的好吗？我……无法承受那个结果。"
    
    $ jwq.show("平静")
    "而江晚晴在听到这连续的质问后，只是轻微地、但又绝对稳重地点了点头。"
    "接着用手轻轻拂过旁边的书桌桌面。"

    
    voice "cv/jiangwanqing/jiangwanqing_0064.ogg"
    jwq "你误会了一点。"

    voice "cv/linxi/linxi_0118.ogg"
    lx "嗯？"

    "少女斜斜地看向了林曦。"

    $ jwq.show("计划通")
    voice "cv/jiangwanqing/jiangwanqing_0065.ogg"
    jwq "我是要让他去参加天选试没错，但并不会如他所想，让他以所谓的「小涟诞生」作为目标，我要让他替换成另一个目标。"

    voice "cv/linxi/linxi_0119.ogg"
    lx "……你这岂不是自相矛盾了么。"
    voice "cv/linxi/linxi_0120.ogg"
    lx "所谓的小涟根本就不存在，陈舟自己是最清楚这一点的，而他可是基于这个基本条件，在和小涟谈恋爱。"
    voice "cv/linxi/linxi_0121.ogg"
    lx "怎么可能会愿意放弃这个，让自己的「爱人」真正得到他人认可的机会。"

    $ jwq.show("平静")
    voice "cv/jiangwanqing/jiangwanqing_0066.ogg"
    jwq "嗯，你说的是正确的，阿舟的心意，操控起来几乎不可能。"
    voice "cv/jiangwanqing/jiangwanqing_0067.ogg"
    jwq "但是，在那不可能之下，我也仍然想到了一个方法。"

    "江晚晴表情凝重，神色坚定，身上透露出一阵锋芒之气，那是一往无前、绝不掉头的强劲气势。"
    "见到她如此认真，林曦提起了全部精神，生怕遗漏什么。"

    voice "cv/jiangwanqing/jiangwanqing_0068.ogg"
    jwq "我要……"

    stop music fadeout 1.0
    
    "林曦屏住了呼吸。"

    $ jwq.show("指摘")
    $ jwq.act(anim_jump)
    # 一本正经大声
    voice "cv/jiangwanqing/jiangwanqing_0069.ogg"
    jwq "我要当他的小三，把他从那个莫名其妙的虚拟女友手里给NTR过来！"

    voice "cv/linxi/linxi_01220.ogg"
    lx "……"
    voice "cv/linxi/linxi_01230.ogg"
    lx "…………"
    voice "cv/linxi/linxi_01240.ogg"
    lx "…………………………"

    # 切BGM，切成欢快的
    play music "audio/bgm/BGM_欢快.ogg" loop fadein 1.0

    $ lx.show("惊讶")
    $ lx.act(anim_jump)
    voice "cv/linxi/linxi_0123.ogg"
    lx "{size=+25}唉————！唉唉唉唉唉唉？?{/size}"

    $ jwq.show("游刃有余")
    voice "cv/jiangwanqing/jiangwanqing_0070.ogg"
    jwq "啊啊，是啊，前几年，我们都陷入了误区，认为要么顺他的意，要么就强行扭转他的思想。"

    $ lx.show("萌怒")
    "林曦瞪大了双眼，明显是不敢置信，俨然一副见了鬼的样子。"

    voice "cv/jiangwanqing/jiangwanqing_0071.ogg"
    jwq "可如果把棋盘翻转过来呢？"
    voice "cv/jiangwanqing/jiangwanqing_0072.ogg"
    jwq "不是我去斧正他，而是他自觉移情别恋到我身上，不就一切都可解决了么！"
    voice "cv/jiangwanqing/jiangwanqing_0073.ogg"
    jwq "有句老话说得很对，只要锄头挥得好，没有墙角挖不倒……我可没道理输给一个没心没爱，净凭借脑内幻想而存在的破女友。"

    $ jwq.show("挺好颜")
    voice "cv/jiangwanqing/jiangwanqing_0074.ogg"
    jwq "牵手也好，拥抱也好，亲吻也好……呵呵，呵呵呵，甚至更进一步的，那个虚拟女友能做到吗，其他人能做到吗？！"

    "少女是如此的认真，这股劲头，以至于让林曦的脑子现在都有些转不过来。"

    voice "cv/linxi/linxi_0124.ogg"
    lx "你……你？你真这么想的？"

    $ jwq.show("坚定")
    voice "cv/jiangwanqing/jiangwanqing_0075.ogg"
    jwq "啊，是啊，我已经决定好了。"
    voice "cv/jiangwanqing/jiangwanqing_0076.ogg"
    jwq "我是Galgame领域大神，光是在外面走一走，分分钟就能攻略十个八个小处男。拿下一个陈舟不是得心应手么。"

    $ lx.show("无语")
    voice "cv/linxi/linxi_0125.ogg"
    lx "嘶~~我记得你以前好像没这么厚脸皮……"

    $ jwq.show("游刃有余")
    voice "cv/jiangwanqing/jiangwanqing_0077.ogg"
    jwq "事已至此，只有这一条路可行了，哪怕不能成功，也不会有任何问题，大不了让他在第二轮被刷下去，我们已经没得选了。"

    voice "cv/linxi/linxi_0126.ogg"
    lx "你……你。"
    
    "林曦倒吸了一口凉气。"

    voice "cv/linxi/linxi_0127.ogg"
    lx "你还真想得出来！"

    $ lx.show("欲言又止")
    voice "cv/linxi/linxi_0128.ogg"
    lx "但是…感觉…是有说法？嗯，确实，说不定有戏。啊，对啊，对啊，我怎么没想到还能这样做？"

    voice "cv/jiangwanqing/jiangwanqing_0078.ogg"
    jwq "没错，看来你也意识到了……"

    "林曦根本就没听见江晚晴在说什么，她的瞳孔渐渐放大，已经逐渐理解了一切。"

    $ lx.show("微笑")
    voice "cv/linxi/linxi_0129.ogg"
    lx "是这样没错…只要我主动一点，把舟子攻略下来，那什么小涟不小涟的，不就无所谓了么……"

    # 空洞表情 -> 暂用呆滞或无语
    voice "cv/linxi/linxi_0130.ogg"
    lx "不就是当小三……我也不是不行，早就想弥补遗憾了……嗯，嗯嗯，对于虚拟角色，就不用讲什么江湖道义了……不错，感谢你给的思路，你真是个天才。"

    $ jwq.show("尴尬")
    voice "cv/jiangwanqing/jiangwanqing_0079.ogg"
    jwq "……"
    voice "cv/jiangwanqing/jiangwanqing_0080.ogg"
    jwq "哈？"

    $ jwq.show("嫌弃")
    voice "cv/jiangwanqing/jiangwanqing_0081.ogg"
    jwq "什么意思？跟你有什么关系？"
    voice "cv/jiangwanqing/jiangwanqing_0082.ogg"
    jwq "你在一边乖乖看着就行了，别来碍事。"

    $ lx.show("微笑")
    voice "cv/linxi/linxi_0131.ogg"
    lx "哼，呵呵呵。"
    voice "cv/linxi/linxi_0132.ogg"
    lx "既然被我知道了，那就由不得你了，话说，你不是已经安排好一切了吗？什么天选试之类的？"
    voice "cv/linxi/linxi_0133.ogg"
    lx "行了，你的活已经干完了，该干嘛干嘛去吧。剩下的我来。"

    $ jwq.show("指摘")
    $ jwq.act(anim_jump)
    voice "cv/jiangwanqing/jiangwanqing_0083.ogg"
    jwq "你！"

    "江晚晴万万没有想到，作为败犬的林曦……居然，居然敢！"

    $ lx.show("萌怒")
    voice "cv/linxi/linxi_0134.ogg"
    lx "我什么我！"

    $ jwq.show("眯眼")
    voice "cv/jiangwanqing/jiangwanqing_0084.ogg"
    jwq "呵，呵呵呵。"
    voice "cv/jiangwanqing/jiangwanqing_0085.ogg"
    jwq "看来，我们之间的矛盾，是无法调和了。"

    $ lx.show("鼓嘴气气")
    voice "cv/linxi/linxi_0135.ogg"
    lx "啊——看来是呢。"

    "两个人之间，剑拔弩张的氛围，简直可以把整个教室都点燃！"

    $ jwq.show("游刃有余")
    voice "cv/jiangwanqing/jiangwanqing_0086.ogg"
    jwq "不想被伤害到的话，现在退出还来得及哦。"
    voice "cv/jiangwanqing/jiangwanqing_0087.ogg"
    jwq "你心里也清楚吧，就算他不魔怔了，也没有你的机会。"

    voice "cv/linxi/linxi_0136.ogg"
    lx "谁知道呢？我根本不懂你在说什么。"

    voice "cv/jiangwanqing/jiangwanqing_0088.ogg"
    jwq "我没记错的话，当年是谁最后把阿舟搞定的？应该不是你吧？"

    $ lx.show("惊讶")
    voice "cv/linxi/linxi_0137.ogg"
    lx "咦？是这样来着？可是可是，你嘴巴里那个「可能」存在的回忆，陈舟他自己知道么？"

    $ jwq.show("尴尬")
    $ jwq.act(anim_shake)
    voice "cv/jiangwanqing/jiangwanqing_0089.ogg"
    jwq "——额。"
    
    $ jwq.show("坚定")
    voice "cv/jiangwanqing/jiangwanqing_0090.ogg"
    jwq "但……但是，呼，好吧……那我们就各凭本事吧。"

    $ lx.show("平静带怒")
    voice "cv/linxi/linxi_0138.ogg"
    lx "啊啊……我劝你做好觉悟。"
    voice "cv/linxi/linxi_0139.ogg"
    lx "这一次，我不会再囿于青梅这个身份了……我已经，不是当年那个后知后觉的我了。"

    $ jwq.show("眯眼")
    "江晚晴的眼睛微微眯了起来，因为她不想让眼前的少女看到自己的神色。"
    "自己其实…在林曦的面前，根本就没有任何心理优势。"
    "唯有这一点，不想被她看穿。"
    "若是以敌对视角来看，这可能是最为恐怖的对手了。"
    "拥抱也好，亲吻也好……那些小涟做不到的，眼前的少女都能做到，和自己的条件一模一样，可牵绊，却远远胜出。"
    "若不是因为自己足够早熟，哪怕是当年……"

    $ lx.show("平静")
    voice "cv/linxi/linxi_0140.ogg"
    lx "我不会让自己留下任何遗憾。"
    voice "cv/linxi/linxi_0141.ogg"
    lx "你也是……我不希望你，留下任何遗憾。"

    play music "audio/bgm/BGM_孤独夜晚.ogg" loop fadeout 0.5 fadein 0.5
    $ jwq.show("微笑")
    "江晚晴深呼吸了一口，开始重构脑内设想的所有计划，她认真起来了。"
    "福至心灵般地，有种回到当年的气氛——好像三人之间，什么都没变一样。"
    "别样的怀念。"
    "所以，她轻轻地笑了出来。"

    $ jwq.show("微笑")
    voice "cv/jiangwanqing/jiangwanqing_0091.ogg"
    jwq "啊，那就让我们，用少女的方式，决斗吧。"
    voice "cv/jiangwanqing/jiangwanqing_0092.ogg"
    jwq "以爱之名……"

    $ lx.show("微笑")
    voice "cv/linxi/linxi_0142.ogg"
    lx "……以爱之名。"

    "月光斜斜地洒入，在两人之间的地板上划出一道银色界线，宛如无形的楚河汉界。"
    "一阵微风从半开的窗户溜进来，轻轻掀动窗帘，也拂动了她们的发梢。"
    "在这无人见证的夜晚教室里，"
    "某种既温柔又锋利的东西正在悄然生长。"
    "两个少女，均下定决心。"
    "要将陈舟，从那个看不见摸不着的虚拟女友手上，抢夺……"

    # 本场结束，大幕关闭
    stop music fadeout 2.0

    show cinematic_black_overlay
    
    # 这里的硬暂停时间必须等于上面 linear 的时间
    $ renpy.pause(2.0, hard=True)
    
    # 此时已经彻底黑屏了
    scene black # 清理掉背景和刚才的覆盖层
    
    $ renpy.pause(1.0, hard=True) # 黑屏后再额外多等 1 秒（也是强制的）

    return