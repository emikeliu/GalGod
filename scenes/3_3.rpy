# 定义未在配置中出现的额外角色
define man_parent = Character("成熟男士", color="#fff")
define woman_parent = Character("贵气妇人", color="#fff")

label scene_3_3:

    # === 第一幕：河边（白天） ===
    # 暂定使用街道背景作为基板
    play music "audio/bgm/BGM_痛苦落泪.ogg" loop fadein 1.0
    scene bg riverside_road2 with dissolve

    "我察觉到了，两个少女在旁边，似乎正说着什么很重要的话。"
    "但是，我的五感却好像只是针对那边失去了所有机能，完全没能接受任何信息。"
    "全部的思绪，都被手机上展示的内容所箍住。"

    cz "小涟……怎么会，小涟……"

    "那是一张照片。"
    "上面记载着的是…我的……不对，是…小涟？"

    cz "这种过去，可是……"

    "照片上没有我的存在，所以，应该是我拍的吧。"
    "毕竟这是我的房间。"
    "首要看到的，就是镜头旁边的曦曦，她啃着冰激凌，坐在床上摆着脚，舌头舔着舔着，一边斜过眼来，用一副百无聊赖的目光看向我这边。"
    "更远一点的，是江晚晴的背影，她正对着我的电脑屏幕，在操作着什么，好像是一个板子。"
    "而这其中，最吸引我目光的，是我再熟悉不过的显示器。"
    "那上面是一个是只铺了底色的半成品。"
    "我再熟悉不过的地方，再熟悉不过的屏幕上，出现了我再熟悉不过的人物。\n光从线稿就能看出，那是……"
    "——小涟。"

    cz "小涟，明明是我玩过的一部同人废萌Galgame里的女主——"
    "说起来，我完全不知道，那个游戏的作者到底是谁。"

    play sound fx.heartbeat
    cz "——呃！"

    # 【逐渐黑屏】
    scene black with Dissolve(2.0)

    "飘飞的思绪，宛如湖水一般凝固起来\n——让我以为自己身在水中，逐渐下沉，无法呼吸直到溺毙。"
    "我是一个溺水者。"
    "是一个稻草就在眼前，试图把我拉上岸的双手就在眼前，却视而不见的溺水者。"
    "我……沉迷于水底的月亮。"

    cz "哈，哈……"
    cz "——呼，呵，呵呵。"
    "哈哈。"
    "只感觉浑身发软，手和脚都操控不了了似的。"
    "好像连喘气都喘不过来了，也不知道究竟是在笑什么。"

    "——是这样么？这一瞬间，很想再问这么一句。"
    "如果说此前心中有着什么迷雾的话，在此刻，的确烟消云散了。"
    "是啊，就应该是这样。"
    "宛如一个解不开的锁找到了原本的钥匙一般，只是轻轻一转，便应声而开。"
    "脑子里闪过许多许多起事情，以各种方式暗示自己的林曦；入学时直奔而来的江晚晴；扑倒自己后神色晦暗的林曦；在雨中看不出有没有在哭的江晚晴。"
    cz "原来……如此。"
    "双眼的视线不知何时起有所模糊，\n原来，我从一开始就是只看着自己的家伙。"

    "林曦，我从小玩到大的好友……\n明明，我最不想伤害的就是她……"
    "江晚晴，或许…是重要的人……\n为什么……"
    "想不通，怎么会变成这样的呢。"
    "他妈的，\n我这些年来，\n简直活成了一坨狗屎。"

    # 【逐渐白屏】
    scene bg white with Dissolve(1.5)

    "一阵逆风吹过，属于我肉体的世界宛如和外界有着气压差一般，耳朵内感到阵阵发疼。"
    "里面的我和外面的我，正进行一场血腥无比的厮杀。"
    "而构成人形的透明牢笼，则死死箍住了我的所有、我的一切。"
    "只觉得很奇怪。"
    "只觉得身体很轻。"
    "手脚不受控制，眼前白的黑的，亮的暗的一起在闪烁着，\n被切成具有形状的光，\n漂浮流动。"
    "或许也能称得上有生以来第一次尝到了有把刀在心中转动的快乐。"
    "意识随着我的呼吸，要从鼻孔里流出。"
    "然后，我就这么倒下——"

    play sound fx.fabric_collision # 音效：衣物扑通
    
    # 【白屏取消】
    scene bg riverside_road2 with Dissolve(1.0)

    "……"
    "一秒钟，还是一分钟过去了？"
    "我抵在一个，柔软的怀里。"

    $ jwq.show("落寞", pos=center)
    voice "cv3/jiangwanqing/jiangwanqing_0059.ogg"
    jwq "阿舟……你，没事吧。"

    "她目光中的担忧与关怀毫不掩饰，在默默支撑我的这件事上尽数流露。"
    "我睁开眼，看向她，眼中的少女宛如变了一个模样。"

    cz "……晚晴。"

    $ jwq.show("微笑")
    voice "cv3/jiangwanqing/jiangwanqing_0060.ogg"
    jwq "不是说好的，不要在第三个人面前这么叫我么。"

    "我没能在意她说的话，只是自顾自地将心底的话语喃喃而出。"
    cz "抱歉，我…我根本……"

    "话还没有说完，嘴上就传来了柔软的触感，她的指尖抵在了我的唇中。"

    voice "cv3/jiangwanqing/jiangwanqing_0061.ogg"
    jwq "不用说了……"
    voice "cv3/jiangwanqing/jiangwanqing_0062.ogg"
    jwq "呵呵，这些事情，都是剪不断，理还乱的。\n没有什么去整理的必要。"
    voice "cv3/jiangwanqing/jiangwanqing_0063.ogg"
    jwq "过去不重要，对么？\n未来会怎样，只能由当下决定。"
    voice "cv3/jiangwanqing/jiangwanqing_0064.ogg"
    jwq "天选试……你去吧，肯定会通过的，我保证。"

    "肠胃中的沉痛，顺着喉管逆形而上，流入眼眶，在我的眼底聚集起了热量。"
    "有种，上次那样，要失去曦曦一样的不安感。"

    cz "我会去，嗯，我肯定会去的。"
    "我想要抓住稻草。"

    cz "所以——"

    stop music
    voice "cv3/chengshunanshi/chengshunanshi_0001.ogg"
    man_parent "江晚晴！"

    "我的话语被粗暴打断。"

    $ jwq.show("嫌弃")
    "一瞬间，晚晴身上的氛围就变化了。"
    voice "cv3/jiangwanqing/jiangwanqing_0065.ogg"
    jwq "……"

    "我看向声音传来的地方，是一辆带着商务沉稳风格的高级轿车。"

    $ jwq.show("挺好颜")
    "少女对我笑了一下，轻轻摩挲了一会我的脸，安抚似的，确认我没有问题后，才转身离开。"

    # 拉远 + 缩小
    $ jwq.show("坚定", pos=right, zoom=0.5, y_offset=-1050, x_offset=-250)

    show father shadow:
        zoom 0.45
        xalign 0.5
        yalign 1.0
        yoffset 120

    play music "audio/bgm/BGM_孤独夜晚.ogg" loop fadein 1.0
    voice "cv3/jiangwanqing/jiangwanqing_0066.ogg"
    jwq "你来做什么，父亲。"

    "她脊背挺得笔直，犹如一柄出鞘的利剑，大步向前走去。"
    "阳光自她她飘扬的发丝中穿过，洒落周身，\n一阵风来……她的衣裙，宛如披风般猎猎扬起。"

    voice "cv3/linxi/linxi_0122.ogg"
    lx "舟子，你……没事吧。"

    "曦曦不知不觉靠近了我的身边。"

    cz "嗯，我没事的，谢谢你……"

    "几个眼神交流，便代替了诸多话语，我看向晚晴那边，是家事？"
    "一个中年男人站在那边，穿着正装，从上到下打理得一丝不苟。\n他的西装笔挺，衣角平整得几乎没有一丝多余折痕。腕表隐藏在袖口之下，只有抬手时才露出短暂的光影。"
    "男人看着江晚晴的神情冷静而内敛，眼角没有笑意，而是微微皱眉，只是这样就让人感到一种不容忽视的存在感。"
    "那边的气氛，似乎和我这边完全无关，是另一个世界……"
    "现在这个状况，可能需要……先整理一番。"
    "我也需要确定一下，自己这个人的存在，自己这个人的……想法。"
    "不能再像以前那样了。"

    voice "cv3/chengshunanshi/chengshunanshi_0002.ogg"
    man_parent "你还知道我是你的亲爹？这些日子，你都做什么去了。"

    $ jwq.show("叹气")
    voice "cv3/jiangwanqing/jiangwanqing_0067.ogg"
    jwq "唉，我已经这么大了，该放手了啊。你这种人，放在Galgame里就叫做女儿控吧？"

    voice "cv3/chengshunanshi/chengshunanshi_0003.ogg"
    man_parent "你少跟我打岔！你到底在外面瞎折腾什么！\n家里给你的那些……你全都不要了？你以为你现在还是江家的人？"

    $ jwq.show("平静")
    voice "cv3/jiangwanqing/jiangwanqing_0068.ogg"
    jwq "我当然知道我是什么人。\n至于身份嘛……你们不是早就准备好，把我从族谱里上划掉了么？"
    voice "cv3/jiangwanqing/jiangwanqing_0069.ogg"
    jwq "那些成就，放弃了就放弃了，我看你们已经足够有钱有权，再贪恋更多不是好事哦。"

    voice "cv3/chengshunanshi/chengshunanshi_0004.ogg"
    man_parent "你——！"

    "他上前一步，怒火几乎要把空气点燃。"
    "见到他有种要动手的氛围，站在远处观望的我连忙上前一步。"

    with hpunch
    "——然后被曦曦拉住。"

    cz "……？"

    "她摇了摇头，露出一脸微妙的表情。"
    "再度回望晚晴那边，她却只是悠然立在原地，\n颇有一种「他强任他强，清风拂山岗」之意。"

    $ jwq.show("游刃有余")
    voice "cv3/jiangwanqing/jiangwanqing_0070.ogg"
    jwq "老爸，你该不会，想要对我使用暴力吧。"

    voice "cv3/chengshunanshi/chengshunanshi_0005.ogg"
    man_parent "——咯……"

    $ jwq.show("微笑")
    voice "cv3/jiangwanqing/jiangwanqing_0071.ogg"
    jwq "忘了你的宝贝女儿，从小接受的是什么教育吗？"
    voice "cv3/jiangwanqing/jiangwanqing_0072.ogg"
    jwq "你们花重金请了全国最好的武术教练，教我怎么防身，怎么制服敌人……应该有看过教练给我写的评语吧？好像是全优秀来着。"

    "面对江晚晴放松的态度，那位中年男士果不其然退缩了，只是脸扭曲地抽动了一下，气焰凭空弱了三分。"

    voice "cv3/chengshunanshi/chengshunanshi_0006.ogg"
    man_parent "……这样子的你，到底哪里有社交礼仪了？"

    "他分明具备更加高大的身躯，在堂堂正正的江晚晴面前，居然有种矮了一头的感觉。"

    cz "……"

    voice "cv3/linxi/linxi_0123.ogg"
    lx "……唉，你就别担心她了……"

    "曦曦，你这家伙，早就知道了吗！"

    "而就在这时——"

    show mother shadow:
        zoom 0.45
        xalign 0.2
        yalign 1.0
        yoffset 180
    voice "cv3/guifuren/guiqifuren_0001.ogg"
    woman_parent "够了，别丢人现眼。"

    "一道尖锐的高跟鞋声踏入光里。"
    "从那边的豪华高级车中下来的，是一位卓有气质的奢华女士。"
    "她走过来，眼神冷得像冰霜。"

    voice "cv3/guifuren/guiqifuren_0002.ogg"
    woman_parent "晚晴，我真的……替你羞耻。\n我们辛苦养你到这么大，你却跑出去做这种……荒唐事。"
    voice "cv3/guifuren/guiqifuren_0003.ogg"
    woman_parent "你知不知道亲戚们怎么看你？你一个女孩子，不学好、不守规矩、不回家，像个没人要的野种。"

    $ jwq.show("微笑")
    voice "cv3/jiangwanqing/jiangwanqing_0073.ogg"
    jwq "呵……原来他们是这么想的吗，还有老妈，你们也是。"

    "似乎是江晚晴母亲的女人，转过头来，扫了我和曦曦一眼，\n那其中的寒意，简直就让我周身凭空下降三度。"
    "我们之间隔着好一阵距离，或许，是把我们当成路人，或者同学，警告我们别凑在这边多管闲事吧。"
    "她没将我们放在眼中，一眼过后便不再关心，只是专注地看向江晚晴。"
    
    voice "cv3/guifuren/guiqifuren_0004.ogg"
    woman_parent "真是个风流浪子，可让我们好找，要不是底下的人调查到了你莫名其妙转学进去的学校，到现在我们还不知道你在哪里。"
    voice "cv3/guifuren/guiqifuren_0005.ogg"
    woman_parent "家里的人倾尽全力，费尽心血，一点一滴从各方面构建你的能力，换来的就是这样的结果？"

    $ jwq.show("平静")
    voice "cv3/jiangwanqing/jiangwanqing_0074.ogg"
    jwq "请问一句——是什么结果？"

    voice "cv3/guifuren/guiqifuren_0006.ogg"
    woman_parent "晚晴，你自己心里没数吗？到底是为了什么，要把你所有能换的东西都换出去？家里替你争取的光明大道你不要？"

    voice "cv3/chengshunanshi/chengshunanshi_0007.ogg"
    man_parent "别人都说我们江家教出个败家女，你自己没被气死，我们都给你气死了！"

    voice "cv3/jiangwanqing/jiangwanqing_0075.ogg"
    jwq "原来如此。"
    "她轻轻吸了一口气，然后——"

    voice "cv3/jiangwanqing/jiangwanqing_0076.ogg"
    jwq "你们在说我之前，可不可以先搞清楚，我已经给你们带来过什么？"

    voice "cv3/chengshunanshi/chengshunanshi_0008.ogg"
    man_parent "你这是什么态度！"

    $ jwq.show("坚定")
    voice "cv3/jiangwanqing/jiangwanqing_0077.ogg"
    jwq "该让你们炒作的，让你们炒作了，拿我的身份去做虎皮扯大旗，我也没有作声……嗯，这些都不谈，早在那之前，我起到的作用，就已经足够报答你们的养育之恩了吧。"
    voice "cv3/jiangwanqing/jiangwanqing_0078.ogg"
    jwq "毕竟从小作为家族继承人培养，集团里的一些规划，还有年度战略的决策，背后都有我的功劳才对。"

    "阳光落在她脸侧，她抬起下巴，那一刹那，我好像意识到了……真正意识到，她到底在承受些什么。"

    voice "cv3/chengshunanshi/chengshunanshi_0009.ogg"
    man_parent "还敢顶嘴？！你看看你现在这种样子，居然会有这么的倔！我告诉你，你还没成年，你要不跟我们回去，我就——"

    $ jwq.show("坚定") 
    voice "cv3/jiangwanqing/jiangwanqing_0079.ogg"
    jwq "我不会回去。"

    "她像是在宣判。"
    "我吞了口口水。"

    "曦曦也捏紧了我的衣角。"

    voice "cv3/chengshunanshi/chengshunanshi_0010.ogg"
    man_parent "你！晚晴，我可是已经调查过了。你现在住的那个出租屋，在城中村里，各种环境都破破烂烂的，你从小到大，娇生惯养，怎么忍得了的！"
    
    "像是附和似的，那位颇有威仪的女士也是柔声说道。"

    voice "cv3/guifuren/guiqifuren_0007.ogg"
    woman_parent "是呀，是呀，晚晴，别在外面晃荡了，来，我们回家。"

    $ jwq.show("挺好颜")
    "江晚晴露出了一个，非常非常，让我觉得非常美丽的笑容——"
    voice "cv3/jiangwanqing/jiangwanqing_0080.ogg"
    jwq "谢谢你们，父亲，母亲，把我培养成了一个如此坚强的女人。"

    "只是看到，就让我失神了。"
    "然而，等待着她的，确是逐渐变得冰凉的话语。"

    voice "cv3/guifuren/guiqifuren_0008.ogg"
    woman_parent "……你知不知道，因为你的任性，我们家族失去了多少机会。"

    "江晚晴的母亲终于变脸了，声音中也不带柔软，而是带有一种冷静的审视，那绝对不是一个作为母亲所拥有的眼神。"

    $ jwq.show("平静")
    voice "cv3/jiangwanqing/jiangwanqing_0081.ogg"
    jwq "最多，失去一些面子吧。"
    voice "cv3/jiangwanqing/jiangwanqing_0082.ogg"
    jwq "贪爱银子的，不因得银子知足；贪爱丰富的，也不因得利益知足。\n我猜，你们是不是，把别人得到的，当成了自己所失去的呢？"

    voice "cv3/chengshunanshi/chengshunanshi_0011.ogg"
    man_parent "畜生！怎么对你爹妈说话的！"

    $ jwq.show("微笑")
    "江晚晴听言，只是侧头微笑，光在她睫上颤了一下，却看不出是嘲讽还是苦涩。"
    "她握着衣角的指尖轻轻动了一下\n——大概只有我看到了。"

    voice "cv3/guifuren/guiqifuren_0009.ogg"
    woman_parent "本来可以获得的权力、资本、金钱、光环，你全拿出去了吧，不然怎么会是现在这样一副样子，说，你拿出去交换什么了。"
    "这语气不像是人母在斧正女儿，而更像是高官正施于命令。"
    "其中，有一个词引起了我的注意。"
    
    cz "交换？"
    "什么意思。"

    voice "cv3/guifuren/guiqifuren_0010.ogg"
    woman_parent "把那些换来的资源给家里，还能补救你的过错。"

    voice "cv3/chengshunanshi/chengshunanshi_0012.ogg"
    man_parent "你是不是在海外开了户，还是说，给别人担保融资了？你和谁接触？是谁让你全换出去的？没事，你只要把那些合作、备案、担保关系全部交代清楚，家里还能接纳你……"

    "江晚晴只是安静地听完，眨了眨眼。"
    "然后——轻轻地笑了。"

    voice "cv3/jiangwanqing/jiangwanqing_0083.ogg"
    jwq "我还以为……你们多少会担心一下，我是不是受了委屈，是不是饿着冷着、被欺负了……"
    voice "cv3/jiangwanqing/jiangwanqing_0084.ogg"
    jwq "原来只是因为我把你们能利用的东西，都用掉了，感到不服啊，\n可那些——本来就是我的呀？"

    "空气瞬间如刀片般锐利。"

    voice "cv3/guifuren/guiqifuren_0011.ogg"
    woman_parent "你——"

    voice "cv3/chengshunanshi/chengshunanshi_0013.ogg"
    man_parent "你到底在外面做了什么交易？！告诉我！\n你把那些资格、通行证、特批名额……都给谁做交易去了？！"

    "资格。"
    "通行证。"
    "特批名额。"
    "？"
    "我不是傻子……起码在智力的意义上不是，\n所以，只是一听，脑中就划过了不少线索。"

    cz "……"
    "是为了我？"

    $ jwq.show("平静")
    voice "cv3/jiangwanqing/jiangwanqing_0085.ogg"
    jwq "给谁了，不知道呢，说不定，是觉得那些弯弯绕绕太烦了，所以主动丢掉了哦。"

    "对面的交谈逐渐火热化，你一言我一语，风暴一般地席卷了整个空间。"
    "宛如青山松雪一般的少女，任凭风吹浪打，自有巍然不动之姿。"
    "那一份过于宽阔的背影，让我感受到了其意志的重量。"
    "不由得想起了，不久前，我们在餐厅外的交谈……"
    "一切，我都理解了。"
    "完全理解了。"
    "所以，我，因为这……有一点害怕。"
    "害怕自己根本配不上，被她如此保护着的那份东西。"
    "但，就算是害怕，也并不是退缩的理由。"
    "因为，只是单单站在旁边，看着少女一个人在针锋相对的环境里战斗，我便心中不快。"
    "没有什么考虑，不如说，根本就没有考虑的必要。"

    "所以，我踏前数步——"

    camera:
        zoom 1.3
        xpos 0.5
        ypos 0.5
        xanchor 0.5
        yanchor 0.4
        ease 2.0
    "正站入几人中间。"

    $ jwq.show("尴尬") # 表现惊讶
    voice "cv3/jiangwanqing/jiangwanqing_0086.ogg"
    jwq "……阿舟？"

    "一刹那，安静了，所有视线的焦点，通通聚集在我的身上。"
    "他们本来以为，站在旁边的我们只是不相关的家伙吧。"
    "要做什么，该做什么，没什么好想的。"
    "无非就是，选择。"
    "我只是对晚晴点了点头，没有给第三人反应过来的时间，趁着彼此打量的间隙，我大大方方地说出了想说的话。"

    cz "晚晴把它们赌在天选试上面了。"
    "我做出了选择。"

    voice "cv3/chengshunanshi/chengshunanshi_0014.ogg"
    man_parent "晚晴？"
    "他咀嚼着这个称呼，眯起来眼睛，如探照灯般在我身上来回扫视。"
    "男士的怒容忽然收敛，像按下开关一样，眼中划过一丝诡异的光。"

    cz "风险投资嘛……这个概念，也不用我多说。"

    "江母沉默着，锐利的视线第一次落在我的瞳孔正中，如有实质般压在我的心头，我用自己的意志覆盖了回去。"
    "我想要呈现的，并非针锋相对的、敌对的视线，而是和蔼，却带有坚定信念的视线。"
    "——总之，不能怂。"
    "只要露出一丝怯懦，就会被他们连皮带骨地吞掉。"
    "她沉默了一会，没有多说话，而是在等着我的后文。"

    cz "在我们这里，有地位、有权利，没有什么是不能做到的，做不到的话，无非是手不够大而已。"
    cz "只要手够大，审核也好，监管也好，通通都将畅通无阻……自然，天选试也包括在内。"
    cz "几位长辈，应该是远远比我更熟稔此道的。"

    "还好，我早就把手插进了口袋，所以他们发现不了我因为无措正微微揉搓着的指尖。"

    voice "cv3/chengshunanshi/chengshunanshi_0015.ogg"
    man_parent "你刚刚说的是天选试，我没听错吧。"

    "这位中年男人不复有先前的激动，宛如有什么目的达到了似的，一下子就沉静了下来，让我有些许诧异。"
    "他来到这里，难道不是为了逼迫晚晴么。"

    cz "……不错，正是如此。"

    cz "晚晴……交易出去了很多东西，自然，也会获得相应的回报。"

    "我看向她，她微微点了一次头，我能理解这个意思。"
    "——无论如何都会配合我。"
    "原来我们有着如此深刻的默契？"

    cz "而有关交易物的对等性……你们应该是最了解你们女儿的，我就不多说了。"
    cz "她是一个很聪明的人，怎么会让自己吃亏呢？"

    "虽然我并不知道她付出了多大的代价，但这里还是先让我扯一扯虎皮吧。"

    $ jwq.show("叹气")
    "果不其然，她叹了一口气，好像就是在说「唉，明明我不想说的」一样，一副无奈的表情。"
    "可能只有我能看出，她只是在表演。"

    $ jwq.show("平静")
    voice "cv3/guifuren/guiqifuren_0012.ogg"
    woman_parent "没有意义。"
    "江母冰冷的话语切中了要害。"
    voice "cv3/guifuren/guiqifuren_0013.ogg"
    woman_parent "别人拿到地位，和自己拿到地位，这之间完全不是一个概念。"
    voice "cv3/guifuren/guiqifuren_0014.ogg"
    woman_parent "哪怕她给某个种子人物打通了环节，雪中送炭也好，锦上添花也罢，终归还是不如自己资源在手。"

    cz "这你就错了。"
    "我摇了摇头，也是为了用态度掩饰没底的内心。"
    cz "投资嘛，不能用底线思维。"
    cz "自然，如果满盘皆输，那么大家确实只能认了。"
    cz "但要是成功了呢？"

    voice "cv3/chengshunanshi/chengshunanshi_0016.ogg"
    man_parent "嚯，什么意思。"

    cz "或许……得到的，是一个真正的、天选之子。"
    cz "不是什么只通过省级筛选的，预备役……\n到达殿试，和通过殿试，\n这里边的差别，可比同样的资源在谁手里，大得多的多"

    "只要有1%%的可能性，也会有人为此拼上身家，这，就是Galgame天选之子的含金量。"
    "是远超Galgame领域大神的存在。"
    "我并不是在说天方夜谭。"

    voice "cv3/chengshunanshi/chengshunanshi_0017.ogg"
    man_parent "……"
    voice "cv3/guifuren/guiqifuren_0015.ogg"
    woman_parent "……"

    "泰山一般的视线压在我的头顶，但是，我仍然强撑余裕，大大方方挺直胸膛。"
    "其实我完全是在乱说，到底是怎么一回事，会变成怎样一结果……\n我都是通过先前的只言片语，胡编乱造出来。"
    "还好有晚晴的配合，我才能够站立在这里。"
    "不知道过了多久，如果是现在的话，哪怕短短的十秒种，在我的世界内都有着好几分钟的体感。"
    "如此的沉重，如此的喘不过气来。"
    "接着，沉凝成实质的空间，终于是迎来了一些波动。"

    voice "cv3/guifuren/guiqifuren_0016.ogg"
    woman_parent "如果，被晚晴投资的，是个男人……"
    "眼前这位女士的目光牢牢锁定着我，简直就像是在对我说话。"

    # 有点尬，删除
    # voice "cv3/guifuren/guiqifuren_0017.ogg"
    # woman_parent "我能理解为，他到时候会入赘我们江家么。"

    $ jwq.show("尴尬")
    voice "cv3/jiangwanqing/jiangwanqing_0088.ogg"
    jwq "……呃。"

    "一声怪声从我旁边发出，差点让我伪装出来的、余裕满满的表情出了破绽。"

    cz "……说不定，是个女人哦。"
    "我尽可能地打着哈哈。"

    voice "cv3/chengshunanshi/chengshunanshi_0018.ogg"
    man_parent "空头支票谁都会开……呵，你知道每年死在筛选里的天才有多少吗？"

    cz "她的能力。"
    "我指向晚晴。"
    cz "你不信？"
    "我把话题抛了回去。"

    voice "cv3/chengshunanshi/chengshunanshi_0019.ogg"
    man_parent "哼……算算日子就快到了，不差这一点时间，我倒要看看是个什么结果。"

    "男人上下打量了我两眼，皱起眉头。"
    voice "cv3/chengshunanshi/chengshunanshi_0020.ogg"
    man_parent "说起来，你，叫什么名字。\n怎么总感觉你好眼熟，五六年前，好像见过你？"

    cz "陈舟，耳东陈，同舟共济的舟，我对您没有印象，可能是记错了？"

    "听到我名字的刹那，他眯起了眼，\n似乎露出了一个意味深长的表情，像是有点……意想不到？"
    "而当我再一次看过去时，却仿佛什么都没发生。"
    "是我的错觉？"
    "他一下就收回了目光，失去兴趣。"

    voice "cv3/chengshunanshi/chengshunanshi_0021.ogg"
    man_parent "陈舟吗。"
    voice "cv3/chengshunanshi/chengshunanshi_0022.ogg"
    man_parent "什么狗屁东西，也敢来玩Galgame了。"

    cz "……"
    "他没有理那些细枝末节，整个人的态度转变后，身上的气质就完全成了另一副模样。"

    voice "cv3/chengshunanshi/chengshunanshi_0023.ogg"
    man_parent "天选试就快了，我们这边也很忙，晚晴，我就不和你多说了。"
    voice "cv3/chengshunanshi/chengshunanshi_0024.ogg"
    man_parent "等到那时候，有得是你要负起的责。"

    $ jwq.show("坚定")
    voice "cv3/jiangwanqing/jiangwanqing_0089.ogg"
    jwq "啊，我从来没有逃避身上责任的意思，这点你放心。"

    voice "cv3/chengshunanshi/chengshunanshi_0025.ogg"
    man_parent "我们走。"
    
    voice "cv3/guifuren/guiqifuren_0018.ogg"
    woman_parent "嗯……晚晴，注意好保护自己。"

    "江晚晴的母亲只是再看了江晚晴一眼，然后随着男人走向轿车，立在那边的司机优雅地打开车门。"
    "自我站出来之后，江母也好，江父也好，他们身上那种热烈的、带有攻击性的激动和控制，在顷刻间就消失不见，转而代之的是冷静的试探。"
    "究竟什么东西在他们的掌控中，什么不在呢，\n他们是已经完成了所有的目的？？"
    "听说，身居高位的人都有好几张脸。"
    "……真分不清，到底哪一个才是真正的他们。"

    # 【黑屏切换】
    scene black with dissolve
    play music "audio/bgm/BGM_忧郁.ogg" loop fadein 2.0

    camera:
        zoom 1.0
        xpos 0.5
        ypos 0.5
        xanchor 0.5
        yanchor 0.5
    with None

    "车辆驶远。"
    "风停了，扬起的尘埃缓缓落下。"

    scene bg riverside_road2 with dissolve
    $ jwq.reset_position()
    $ jwq.show("叹气", pos=right, x_offset=-250)
    "在他们离开后，江晚晴才叹了一口气，回到了只在我面前有的那份松弛模样。"

    voice "cv3/jiangwanqing/jiangwanqing_0090.ogg"
    jwq "我的布置，还是被猜出来了……我就是怕，出什么岔子。"

    "晚晴无奈地看着我。"

    $ jwq.show("尴尬")
    voice "cv3/jiangwanqing/jiangwanqing_0091.ogg"
    jwq "虽然不是我的问题。"

    cz "……呃，我坏事了？"

    $ jwq.show("微笑")
    voice "cv3/jiangwanqing/jiangwanqing_0092.ogg"
    jwq "呵呵，没有。"
    voice "cv3/jiangwanqing/jiangwanqing_0093.ogg"
    jwq "不如说，你还是原来那样，本质没变过，我很开心。"

    "还是怎么样？"
    "我根本就不知道，以前的我，面对她时是什么样。"
    "少女眼底的这份怀念，让我舌尖泛起苦味。"

    $ lx.show("忧伤", pos=left, x_offset=250)
    voice "cv3/linxi/linxi_0124.ogg"
    lx "晚晴，你没事吧。"

    "远比我更加敏锐的曦曦，似是察觉了一些藏在晚晴心底的事情，所以有些担忧。"

    $ jwq.show("叹气")
    voice "cv3/jiangwanqing/jiangwanqing_0094.ogg"
    jwq "哎……被你们知道属实是意料之外，时机不凑巧了，陪你们闲逛太久是我的问题，这么说的话，还是有事的。"

    "她捏起自己一丝头发，盘在手上玩了玩，然后将其挥开。"

    $ jwq.show("平静")
    voice "cv3/jiangwanqing/jiangwanqing_0095.ogg"
    jwq "你们可能会想问我一些事情，但是抱歉了，我还有一些工作需要处理……"

    "她很真诚，但她也有她的执念。"
    "她的的确确地在属于她的战场上战斗着，选择背负了一些事物，那些事物，光是凭我想象，都能感受到其沉甸甸的重量。"
    "直到现在，她也不愿多说什么，只是转移话题。"
    "面对社会上的大人时，难道她真的心里有底吗？"
    "面对亲戚家人的白眼，甚至辱骂，她不会感到有一点难过吗？"
    "我早就奇怪，她怎么没有车接车送，保镖相伴，刚刚才知道，原来是这样……\n这样的生活着，她的心里不会偶尔泛起一丝苦涩吗？"
    "或许是有的吧，也或许，这些对于她而言都是浮云一般的事物。"
    "但无论是什么，作为我，作为她的「目的」本身，我……无法接受。"
    "我不愿将她的坚韧，当作我安心接受的理由。"
    "这份重量，不应只由她一人来背负。"

    cz "晚晴。"

    $ jwq.show("平静")
    voice "cv3/jiangwanqing/jiangwanqing_0096.ogg"
    jwq "嗯？"

    cz "无论怎么样，我不会让你做的那些白费。"
    "我没有说那些温温婉婉的滥情话，只是坚定地说出自己的想法。"
    cz "选择已经做好了…我会去天选试的，去那里直面自身……"

    "神明什么的，无所谓了。"
    "重要的是，我要做什么。"

    "听闻我的话，晚晴只是露出了一个落寞的笑容。"

    $ jwq.show("微笑")
    "心有灵犀似的，我察觉到了，\n那个笑容所代表的意思是，一切结束后，就要退场了吗？"
    "呵，没想到，我居然能这么懂你，"
    "既然如此，那就由不得你了。"
    "……我不会让这种事发生。"

    cz "曦曦。"

    "我转头看向另一个一直陪伴着我的少女。"

    cz "谢谢你告诉我一切，放心吧，我已经没有事了，不用担心我。\n如果没有今天，我肯定不会有现在的觉悟。"

    "最感谢的，是你的相信。"
    "相信我能走出来……这被你料到了吗？不愧是你，最了解我的人。"
    "那些散落的碎片，就让我一点一点拾起吧。"

    $ lx.show("闭眼微笑")
    voice "cv3/linxi/linxi_0125.ogg"
    lx "嗯！"

    cz "今天过后，就不要来找我了。"
    "我很认真。"

    cz "我需要一个人冷静一下，整理一番，同时，也需要完完全全地，全身心投入到天选试的备战中去。"
    "已经没有什么好纠结的了。"

    cz "到时候，首都见。"
    "我一定会抓到星星。"

    $ jwq.show("尴尬")
    voice "cv3/jiangwanqing/jiangwanqing_0097.ogg"
    jwq "说起来……"


    stop music fadeout 1.0
    "接着，就在我下定完决心时……江晚晴带着犹豫和踌躇，试探性地说出了话。"

    play music "audio/bgm/BGM_日常5.ogg" loop fadein 1.0
    voice "cv3/jiangwanqing/jiangwanqing_0098.ogg"
    jwq "这个……那个……"

    $ lx.show("平静")
    voice "cv3/linxi/linxi_0126.ogg"
    lx "嗯？"

    cz "……什么？"

    voice "cv3/jiangwanqing/jiangwanqing_0099.ogg"
    jwq "之前，曦曦……不是说，那个，就是，其实，对你……表白了……吗……"
    voice "cv3/jiangwanqing/jiangwanqing_0100.ogg"
    jwq "那…你的回复是……"

    $ lx.show("哭哭")
    $ lx.act(anim_shake)
    voice "cv3/linxi/linxi_0127.ogg"
    lx "哇——哇哇哇哇哇哇！！你，你不要提这个啊啊啊啊啊——！我，我什么都不想听！呜呜呜，不要拒绝我，我，我不要离开，让我一直呆在你旁边吧，我什么都会做哒——"

    cz "……"
    "因为事情太多，情绪跟过山车似的，才想起来好像还有这回事。"
    "这里，能，能先混过去吗……"
    "但，混过去的话，是不是有点太刻意了。"
    "问题是，我现在，也没招啊。"
    "有点尴尬。"
    "目前这情况，不管怎么回答，都很难说是正确答案啊。"
    "……"
    "风轻轻吹过，带走了刚才剑拔弩张的硝烟味，取而代之的，是久违的、属于日常的喧嚣。"
    "只见三条影子斜铺在地板上，泾渭分明地延伸着，没入尘世。"
    "曦曦急促的呼吸在阳光下起伏，晚晴方才绷紧的肩线渐渐松下来，带着笑意。"
    "我顶着她俩的视线，坐立难安，干脆看向河水。"
    "啊，里边的太阳，真圆。"
    "……"
    "不过。"
    "在天选试的终点，我会找到的，找到那个——能容纳所有人的结局。"
    "至于今天，先把今天过完再说吧。"

    cz "走了！去吃晚饭！"

    $ lx.show("哭哭")
    voice "cv3/linxi/linxi_0128.ogg"
    lx "诶？别丢下我~~你们都要先把之前听到的忘掉，不要欺负我！"

    $ jwq.show("微笑")
    voice "cv3/jiangwanqing/jiangwanqing_0101.ogg"
    jwq "呵呵……"

    "再之后，就是我一个人要去面对的了——"
    "……"
    "…………"
    "………………"

    stop music fadeout 2.0
    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene black
    $ renpy.pause(1.0, hard=True)
    
    $ jwq.reset_position()
    $ lx.reset_position()

    # 【电梯】
    scene bg elevator with dissolve
    play sound fx.elevator loop

    "……"
    "昏暗的电梯内，半死不活的灯光弥漫进入瞳孔。"
    "咕咚、咕咚的电梯声，伴随着爬升感，使我稍有疲惫的心得到了一丝慰藉。"
    "可我那正咚咚跳动的心脏，却像是要覆盖那份感觉似的。"

    "深层的不安在体内躁动。"
    "血液持续而坚定地泵向全身，有如灼烧起来的热度，给每一寸血管都带来了焦裂般的发麻滋味。"
    "在本应最安心的此刻，身体却像要背叛自己似的。"
    "我有着这样的预感，说不定，以后再也体会不到那种令人沉醉的安心了。"
    "甚至称不上是预感，而是一种笃定。"
    "……"
    "狭小的电梯……它究竟在上升，还是在原地打转，我已分不清楚。"
    "只是我内心深处，仍不想去面对吧。"
    "呼……我深吸了口气。"
    "这是属于我一人的战场，要做的也很简单。"
    "小涟——"
    "我要去见她了。"
    "我能够好好地去见她么？"

    stop music fadeout 1.0
    stop sound
    show bg white with flash # （闪光）
    play sound fx.door_open # （开门声）

    # === 第三幕：小窝/分手 ===
    scene bg room1_4 with dissolve
    play music "audio/bgm/BGM_安慰.ogg" loop fadein 2.0

    "我终于回到了我的小窝。"
    "我终于……回到了我渴望的归处。"
    "这一次，是抱着目的来的。"

    $ xl.show("温柔", pos=center)
    voice "cv3/xiaolian/xiaolian_0001.ogg"
    xl "哎呀哎呀，今天回得好晚哦~"

    # 闪回
    # "（江晚晴：“哎呀哎呀~是这样吗，这可真是。”）"
    scene bg street2_1
    camera master at memory_filter
    $ jwq.show("微笑", pos=center, transition=None)
    with flash

    voice "cv3/jiangwanqing/jiangwanqing_0007.ogg"
    jwq "哎呀哎呀~是这样吗，这可真是。"

    scene bg room1_4 
    camera master
    with dissolve

    $ xl.show("温柔", pos=center)
    voice "cv3/xiaolian/xiaolian_0002.ogg"
    xl "真是的，让我等了这么久，哎……谁叫我是你的贤妻呢，原谅你啦。"

    # "（林曦（吐槽）：“咕咕……让我等了好久哦。” 林曦：“哼哼~看你也挺累的，原谅你了。”）"

    scene bg riverside_road
    camera master at memory_filter
    $ lx.show("鼓嘴气气", pos=center, x_offset=0, zoom=2, transition=None,  y_offset=1900)
    with flash
    
    voice "cv2/linxi/linxi_0076.ogg"
    lx "咕咕……让我等了好久哦。"
    $ lx.show("微笑")
    voice "cv2/linxi/linxi_0077.ogg"
    lx "哼哼~看你也挺累的，原谅你了。"

    scene bg room1_4 
    camera master
    with dissolve

    show layer master at reset_filter
    $ xl.show("温柔", pos=center)

    "她捏着裙角、睫毛轻颤的样子，像易碎的琉璃，每一次呼吸都牵动着我的心跳，也加剧着那份埋藏于体内的躁动……"
    "眼前稍带笨拙的真实，是让我心碎又迷恋的毒药。"
    "我下意识向前挪了一步。"
    "想就这么抱上去。"
    "小涟为什么会让我觉得这么可爱呢？她的身上，究竟有着哪些特质呢？"
    "我的视线落在她洁白无瑕，软软糯糯的脸上。"
    "如果摸上去的话，肯定能感受到惊人的触感吧。"

    cz "啊，我回来了……"
    "我无法藏住言语中的颤抖。"

    $ xl.show("卖萌疑惑")
    voice "cv3/xiaolian/xiaolian_0003.ogg"
    xl "咦？是发生了什么吗，怎么感觉你，好累好累的。"

    "她捏了捏裙子，红着脸庞，睫毛颤抖着畏缩看来，我已经闻到了她发间的幽香。"

    $ xl.show("害羞")
    voice "cv3/xiaolian/xiaolian_0004.ogg"
    xl "那个……要不要，我治愈你……"

    play sound fx.heartbeat
    play music "audio/bgm/BGM_悲伤八音盒.ogg" loop fadein 2.5
    "咚咚——"
    "心脏在跳动。"
    "身体的内侧，像被什么慢慢拧紧。"
    "宛如要将整个人都解剖开来，我在对我们做残忍的事。"
    "但至少，这次是我自己选择的痛楚。"
    "可以认为，这样的经历弥足珍贵。"

    cz "小涟，你听我说。"

    $ xl.show("卖萌惊讶")
    voice "cv3/xiaolian/xiaolian_0005.ogg"
    xl "唔？"

    cz "我们……我们……"

    "话语在颤抖，我好想，好想好想，让她的笑容一直保留下去。"
    "我……真的很喜欢她。"
    "但是，就连这份喜欢，此刻，都让我有点喘不过气。"
    "所谓的爱，是不存在理由的，对吧？"
    "什么真的假的，都他妈无所谓。"
    "但是，一旦知道了……就变不回去了。"
    "一个人的世界，就是会因为知道和不知道，而产生绝大的颠覆。"

    cz "我想说的是，我和你……"

    $ xl.show("温柔")
    voice "cv3/xiaolian/xiaolian_0006.ogg"
    xl "阿舟，你很不舒服吗？\n要不要……先休息一会儿然后再说？"

    "她每一次，都会在我最想获得安慰的时候，安慰我。"

    cz "不行啊。"
    "我摇了头，同时也是借助这个动作来指示自己。"
    cz "我怕，再休息一会儿就说不出口了。"

    voice "cv3/xiaolian/xiaolian_0007.ogg"
    xl "唔……那，嗯！"
    "她用十分轻快的语气对我说道。"
    voice "cv3/xiaolian/xiaolian_0008.ogg"
    xl "加油~既然是我优秀的丈夫，就好好展现一下你坚定的气概~"

    "她每一次，都会在我最想获得鼓舞的时候，鼓舞我。"

    cz "小涟……"
    "我所爱之人。"
    cz "我们……"
    "我想一直和你在一起。"
    cz "……"
    cz "我们初次见面的那一天，是在医院里，对吧？"

    $ xl.show("温柔")
    voice "cv3/xiaolian/xiaolian_0009.ogg"
    xl "唔……是的，当时你躺在病床上，很危险呢，医生也是忙来忙去的，我在旁边看着真的好担心好担心。"

    cz "是的啊，我有一段很模糊的记忆，就是那时，恍恍惚惚听到医生说，我的状况完全不能掉以轻心，能不能挺过来，不只要看身体情况，还得看我的求生意志什么的。"
    "事后想想，什么狗屁求生意志，当时的我脑子混混沌沌的，连自己什么情况都不知道。"
    "要是真是靠求生意志，我早就死球了。"
    cz "我只是看到了你担心的模样，然后，不知怎么的，我特别、特别不想让你露出那幅表情。"
    cz "睁开眼睛也好，昏迷过去也好，反正，我心里想的只有一个东西，那就是你。"
    cz "说起来，我接受得还挺快的……Galgame里的角色在现实里出现这回事。"
    cz "简直就像是心底最深处的地方，有个位置，专门为你预留了一样……"

    $ xl.show("害羞")
    voice "cv3/xiaolian/xiaolian_0011.ogg"
    xl "因为……那就是我们的「缘」呀，阿舟。\n从你第一次为我心跳加速，在屏幕前许下愿望开始……我就一直在等你，等你需要我的那一刻，降落到你身边。"
    voice "cv3/xiaolian/xiaolian_0010.ogg"
    xl "或许是神的旨意也说不定哦~"

    cz "呵呵，我还真想过是这么回事。"
    cz "不管怎么说，小涟……是你让我活下来的，在那个混沌的、冰冷的病房里。"
    cz "所以，我喜欢你。"
    "——这是毫无疑问的，无论谁都无可动摇的事实。"

    voice "cv3/xiaolian/xiaolian_0012.ogg"
    xl "好啦好啦，我知道了啦，哎，你有多喜欢我，我早就知道了，都听腻了~"

    "我笑了笑，摇了摇头。"
    cz "要说的话，喜欢你的同时，也是在喜欢我自己吧。"

    $ xl.show("卖萌疑惑")
    voice "cv3/xiaolian/xiaolian_0013.ogg"
    xl "唔？"

    cz "因为和你在一起，被你改变了许多许多啊，嗯，我想想，你每次都会让我走在最正确的道路上，我退缩时，你鼓励我，我失落时，你安慰我，我犯错时，你严厉又温柔地指导我……"
    "我说着，就像是在对自己说一样。"
    cz "不知不觉地，我就成长了好多。"
    "人要如何喜欢上自己？\n说不定意外地简单，只要被人支持，被人肯定，不知不觉就会变得喜欢上自己了……"
    "没错，就连当下站立于此处的这份成长，归根结底也有小涟的功劳。"

    $ xl.show("害羞")
    voice "cv3/xiaolian/xiaolian_0014.ogg"
    xl "哎呀哎呀，我有这么好么……"

    cz "对，就是这么好，太纯粹，太完美了。"
    "纯粹完美到，以至于让我忽视了……有些不完美的、会犯错、需要努力去修补关系的、真实的事情。"
    cz "所以，我想，也是时候到此为止了……"

    $ xl.show("卖萌惊讶")
    voice "cv3/xiaolian/xiaolian_0015.ogg"
    xl "哎？"

    "这副摸不着头脑的表情，使我胸口一沉。"
    "随后，我深吸了口气，那口气仿佛带着滚烫的荆棘，刮擦着喉咙。"
    "我终于做好觉悟，说道。"

    cz "小涟。"

    cz "我们……"
    cz "……分手吧。"

    $ xl.show("卖萌疑惑")
    voice "cv3/xiaolian/xiaolian_0016.ogg"
    xl "……"

    $ xl.show("卖萌惊讶")
    "突然的宣言，甚至让小涟宕机了。"
    "此刻，我甚至不敢去看她，现在的我，表情肯定好看不到哪儿去。"
    "她沉默了一瞬了，然后——"

    $ xl.act(anim_shake)
    $ xl.show("卖萌哭哭")

    voice "cv3/xiaolian/xiaolian_0017.ogg"
    xl "哎，唉唉唉唉唉唉——？？！"

    cz "……"

    voice "cv3/xiaolian/xiaolian_0018.ogg"
    xl "阿，阿舟，你，你刚刚说什么？我，我没听错吧……"

    cz "……嗯。"
    
    "正如自己所想的那样。"
    "正如要面对的那样。"
    "这不是宣判。"
    "也不是命令。"
    "而是说出一个事实。"
    "就像是早就存在于此的事实一般。"
    "它清晰无比地摆在眼前，只是因为这回没有移开目光，于是就理所当然地浮出了水面。"
    "忽然间，我很冷静，再度，我清晰地说出口，看着她的眼睛，调整了措辞。"
    "就像是在对自己说一样。"
    cz "我想，我们到了该分手的时候。"

    voice "cv3/xiaolian/xiaolian_0019.ogg"
    xl "我，我被始乱终弃了嘛——不，不要啊，呜呜呜。"

    $ xl.show("抽泣")
    voice "cv3/xiaolian/xiaolian_0020.ogg"
    xl "但，但是……我，我这个性格……天生就是，呜，就是要被丈夫在外面赌博酗酒然后出轨的……我太软弱了啦，可，可是没办法啊……"
    voice "cv3/xiaolian/xiaolian_0021.ogg"
    xl "呜呜，出生后就是这样的，我就是一个无能的妻子……"
    voice "cv3/xiaolian/xiaolian_0022.ogg"
    xl "咿……你都，没有什么，要解释的吗，嘶——"

    cz "我……是有原因的。"
    "原因就是……我必须为了那些……真实的、不完美的、会因为我沉溺于完美幻梦而受伤的人。"
    "也为了……对得起你曾经作为灯光照亮我的那份意义。"

    voice "cv3/xiaolian/xiaolian_0023.ogg"
    xl "嗯，嘶，嗯嗯。"
    "她一脸担忧地看着我，憋着自己的伤心情绪，就这么安静了下来。"

    cz "小涟，你说过的吧，五好青年……是不能伤害别人的。"
    "我现在，是不是就在伤害小涟呢？"
    "呵呵，这就是选择的意义吗，真是够沉重。"
    cz "我过了好久，真的是好久好久，才终于意识到。"
    cz "自己其实，一直有在不自觉的情况下，伤害身边的、重要的人。"
    cz "我也不想……奢求什么原谅了，但是，弥补……或者说，不要继续将错就错……作为我，肯定是想要去证明一下的。"

    "听着断断续续的抽泣声，我只能用力提起一口气。"
    cz "证明一下，一直有你陪伴着的我，一直有你鼓舞着的我，是一个可以自信挺起胸膛的人。"
    "真的非常谢谢。"
    cz "所以，"
    "我把肺里的淤塞的所有东西，全部吐了出来。"

    $ xl.show("抽泣")
    voice "cv3/xiaolian/xiaolian_0024.ogg"
    xl "……"

    $ xl.show("温柔")
    "她还在抽泣着，却慢慢抬起头，对我挤出一个微笑。"

    cz "……所以。"
    "一看到这个表情，本来提起的气势，便溶解在了灯光里。"
    "我只能强行再提起一口气。"
    cz "所以，接下来，我要去参加天选试了。"
    cz "在那里结束一切。"
    "……只有在那里，才能真正结束这一切。\n结束这伤害他人、也伤害我自己的循环。"

    voice "cv3/xiaolian/xiaolian_0025.ogg"
    xl "……呜——\n那样的话，就没办法了呢……"
    "她没有问更多，似乎就这样，理解了一切。"
    "只是带着泪，故作轻松地说道。"
    voice "cv3/xiaolian/xiaolian_0026.ogg"
    xl "毕竟……我作为妻子，也有很多没做好的事情，是我的修行不足呀，能到今天这个地步……有我的责任。"

    "为什么？"
    "为什么，你总是这样……明明一切都是我的问题。"
    "那一副自怜自艾的模样，我真的……看不下去了。"
    "不知不觉间，可能是下意识吧，我在先前说话的时候，就已经前进了几步。"

    cz "……小涟。"

    $ xl.hide()
    $ xl_l.show("温柔")
    "我又靠近了一步。"
    "这是一个，伸手可及的距离。"
    "然而……"

    $ xl_l.hide()
    $ xl.show("温柔")
    voice "cv3/xiaolian/xiaolian_0027.ogg"
    xl "不行哦。"
    "软和的躯体上，软和的声音里，所透露出来的，是带有坚定意志的拒绝。"
    "面对着我的接近，她，毫不留情地，向后退去。"
    voice "cv3/xiaolian/xiaolian_0028.ogg"
    xl "现在开始，不会再让你碰我了。"

    cz "……"

    voice "cv3/xiaolian/xiaolian_0029.ogg"
    xl "如果又开始依赖我，那不就没有意义了吗？"
    voice "cv3/xiaolian/xiaolian_0030.ogg"
    xl "我可不想，丈夫是个想一出是一出的，没用的男人。"

    $ xl.show("抽泣")
    voice "cv3/xiaolian/xiaolian_0031.ogg"
    xl "哦，对了……"
    "她的睫毛打着颤，里面有水雾弥漫而出。"
    voice "cv3/xiaolian/xiaolian_0032.ogg"
    xl "不是…丈夫……"
    voice "cv3/xiaolian/xiaolian_0033.ogg"
    xl "我们已经…分手了……嗯，这样……就好。"

    "裁决的话语，明明是我先说出口的。"
    "在反过来听到的这瞬间，却还是感觉整个房间都开始旋转起来。"

    cz "……这样就好。"
    "我对她笑了笑。"

    $ xl.show("温柔")
    "她也对我回以一个笑容。"
    "虽然只是掩饰，我不过是想要装成自己很坚强的样子。"
    "只是，装着装着，"
    "感觉自己似乎真的变坚强了。"

    stop music fadeout 2.0
    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene black
    $ renpy.pause(1.0, hard=True)
    
    $ lx.reset_position()
    $ jwq.reset_position()
    $ xl.reset_position()
    return