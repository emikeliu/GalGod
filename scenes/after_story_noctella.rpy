label after_story_noctella:

    window auto
    $ quick_menu = True
    $ custom_ui = True

    # === 【卧室】 ===
    scene bg computer_desk
    play music "audio/bgm/BGM_gnossienne-no-1.ogg" loop fadein 1.0
    
    me "呼……终于打完了这部Galgame，还行吧。"

    "蓝白色的荧光打在脸上，我感到眼睛有点疲累。"
    "推开键盘，取下耳机，看了看时间，即将到零点，今天又是平凡的一天。"
    "我大概还是为我沉浸在自己世界的才能感到自豪的，这份专注力真是称得上恐怖，一下子就能将长长的时间折叠成一瞬，让时间过得飞快，就像超能力。"
    "连中午吃饭的记忆都有些消失模糊了，这也是我经历过无数次的遗忘体验。"
    "刚打完的这部Galgame也称不上多喜欢吧，只能说还行。"
    "说到底，这种只能鼠标点击，类似幻灯片一样的题材，玩起来多少有些无趣。"
    "这回只是被人推荐，所以心血来潮，体验一番。"

    me "美少女很可爱是真的，嘿嘿，也不亏。"

    "心情还不错，"
    "只是有点饿了。"
    "说起来，家里还有什么东西能吃吗，\n现在这个情况，还是得搞点夜宵，搞点夜宵……"

    # === 【厨房】 ===
    scene bg kitchen with fade

    "到冰箱里翻找一阵，结果全是饮料，翻来翻去，总算翻出来两根火腿，还有剩下的两个鸡蛋。"
    "行吧，既然如此，泡碗面得了。"
    "等会正好网购一些东西，嗯嗯，不错，然后休息一会，刷刷论坛，看看明天再玩些什么比较好。"
    "夜宵的话，就不用吃太饱了，一根火腿加一个鸡蛋，算上面饼，足矣！"
    "至于剩下的……"

    voice "cv3/epilogue/Noctella_story_00.ogg"
    noctella "给我吃。"

    me "哎？"

    "客厅里，传来了女孩子的声音。"
    with hpunch
    "谁？！"
    "我身体一僵。"
    "陌生的声音，拽着我后知后觉来到客厅边上。"
    "我谨慎地窥视过去。"
    "——随后，便看见了。"
    "看见了，异样的光景。"

    # === 【客厅】 ===
    # 诺提拉初登场
    scene bg living_room1
    $ noctella.show("无口", pos=center, zoom=0.7, y_offset=-350, transition=None)
    with dissolve

    "一个看起来比我小不少的女孩子，穿着便服，坐在客厅沙发上，\n双腿摇啊…摇啊……"
    "宛如这片空间真正的主人。"
    "我被她震慑住了。"
    "被她这种闯入他人家中，还当自己主人翁一般的大心脏震慑住。"
    "而就在我刚想出声询问时，她，看了过来。"

    $ noctella.reset_position()
    $ noctella.show("无口")

    me "……！"

    "鎏金般的眼瞳，只一瞬便将人钉在原地，炽金的视线仿佛要将灵魂洞穿。"
    "刚欲说出的话语，就这样冻结在喉间。"
    "我沉默了。"
    "可她却只是歪了歪头。"

    voice "cv3/epilogue/Noctella_story_01.ogg"
    noctella "可以给我吃吗？"

    me "嗳？"

    voice "cv3/epilogue/Noctella_story_02.ogg"
    noctella "我闻到了……食物的味道。"

    "莫名其妙的话语，甚至让我的思绪有点转不过来。"
    "停顿了足足三息，我才顺着她的视线看去，这才发现，\n她看着的……是我手里的火腿？"

    me "额，你要吃？"

    "我举起拿着火腿的手，摇了摇。"

    voice "cv3/epilogue/Noctella_story_03.ogg"
    noctella "嗯，嗯嗯。"

    me "……"
    me "…………！"

    with vpunch
    me "喂不对吧？你到底是谁，怎么进来的？？？"

    "差点忘了这一茬！"

    voice "cv3/epilogue/Noctella_story_04.ogg"
    noctella "唔？我是诺提拉，门自己开了。"

    "诺、诺提拉？好奇怪的名字……"

    "自设？中二病？"

    "看样子，像是中学生，这个年龄，倒也正常。"

    me "听起来不像真名……"

    voice "cv3/epilogue/Noctella_story_05.ogg"
    noctella "这就是我的名字。"

    me "好吧……那门是怎么回事？我记得我锁了。"

    voice "cv3/epilogue/Noctella_story_06.ogg"
    noctella "但它对我敞开了。"

    me "？"
    me "……原来门没关紧吗，靠，真服了。"

    "可是我明明记得锁了门啊……难不成是记混了……\n哎，事已至此，多想无益。"

    voice "cv3/epilogue/Noctella_story_07.ogg"
    noctella "可以吗？我饿了。"

    me "……"
    me "话说，我也不认识你啊，你爹妈呢？这是离家出走了？\n怎么到我家来蹭饭来了……"

    voice "cv3/epilogue/Noctella_story_08.ogg"
    noctella "我……没有父母。"

    me "……"
    "……好像很沉重的样子，还是别问了。"

    me "你是想吃东西是吧？\n行吧，吃完了记得回家，我就不报警了，你应该也有你的难处。"
    me "不过……你怎么知道我这里有吃的？"

    voice "cv3/epilogue/Noctella_story_09.ogg"
    noctella "你告诉我的。"

    me "……啊？"

    voice "cv3/epilogue/Noctella_story_10.ogg"
    noctella "世界告诉我的。"

    me "……"
    "无言以对。"
    "哎，这个年龄的人，一点点小事，对于他们来说都是天大的事。"
    "闹大了也不好，算了，无非是一顿饭。"
    "而且……她好可爱，简直就像我刚刚玩的，那部Galgame里的出场角色一般。"
    "不知怎么的，光是看到她，我就接受了要给她做饭的事实。"

    # === 【厨房】 ===
    scene bg kitchen with dissolve
    $ noctella.hide()

    "嗯，行吧，那就这样吧。"
    "现状大概已经理解了，客厅目前坐着一个来历不明的少女。"
    "她说她叫诺提拉，她说她饿了，她说门自己开了。"
    "⋯⋯好！\n其实我完全没理解。"
    "我深吸一口气，决定暂时不去深究这些奇奇怪怪的说法。\n毕竟，现在已经快凌晨了，我的脑子也不太转得动。"
    "既然答应了给她做饭，那就做吧。"
    "我站在灶台前，手里拿着那根火腿，陷入了短暂的沉默。"
    "随后，打开橱柜，往里瞅了两眼。"
    "沙漠么……呵呵。"
    "沙漠不一定都是沙子，它本质上是很干旱的地区，提起它，一般人脑中的印象大抵是某部电影中沙尘漫天、金丘无垠的黄色世界。"
    "无论是岩漠、砾漠、还是盐漠，给人的感觉都是贫瘠、荒芜。"
    "人们也经常使用这个意象造词。"
    "文化沙漠指的是人的知识贫瘠，这个厨房或许用「食材沙漠」来形容才最是贴切。"
    "望着几乎空无一物的橱柜，手中的火腿将我拉回了现实。"

    me "连泡面也只剩下两三袋......早知道上午就去买点备用了。"

    "哎，没办法，我从柜子里翻出泡面，又拿出平底锅。"
    "好歹有个蛋吃，也不错了。"

    play sound fx.fry loop
    "油沸腾着。"
    "像我一样。"
    "……"
    play sound fx.boil loop
    "水沸腾着。"
    "像我一样。"
    "…………"
    
    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene black
    $ renpy.pause(1.0, hard=True)

    stop sound fadeout 1.0
    scene bg kitchen with dissolve
    "五分钟后，我看着眼前的成品，点了点头。"
    "面前是两个碗，碗里是泡好的面，上面卧着一颗煎蛋，旁边放着切成片的火腿。"
    "说起来，我做过的最「豪华」的泡面，也不过如此。"
    "我将两个碗端起，回头，准备去客厅与这个不速之客来一场餐桌上的交流。"
    "然而，我刚一回头——"

    # 诺提拉突然出现在厨房
    $ noctella.show("无口", pos=right, x_offset=-250)
    "所看见的，便是已经站在冰箱前的少女。"

    me "………………"
    "这……啊？"
    "为何？"
    "这回可以肯定，先前进来时，厨房的门已经关上。"
    "可我刚才，除了冰箱均匀的嗡鸣声以外，什么声音都没能听见"

    me "你什么时候进来的？"

    voice "cv3/epilogue/Noctella_story_11.ogg"
    noctella "刚刚。"

    "原来我做饭的时候，注意力这么集中？"
    "来不及细想，目光便被她那异常的存在感拖曳过去。"

    $ noctella.act(anim_jump)
    "她拉开冰箱门，踮起脚，\n能反射光一般的柔顺长发就这样垂在身侧，悠悠晃荡着，我一时之间被这幅美丽的画卷摄住了。"
    "而她，目光却几乎没有停顿，直接锁定了最上层的饮料，粉色的，亮晶晶的。"

    me "……"
    "应该是百香果味的魔爪吧，我自己平时喝起来都觉得有点伤身体。"

    me "那个很酸，还有咖啡因，喝了晚上会睡不着的。"

    voice "cv3/epilogue/Noctella_story_12.ogg"
    noctella "睡不着的话，可以陪你看星星。"

    me "看星星？城市里光污染严重，哪来的星星给你看……"

    voice "cv3/epilogue/Noctella_story_13.ogg"
    noctella "看得见的哟，在看不见的地方。"

    "……算了，想喝就喝吧。"
    "她伸手。"
    "动作轻盈得不像是在「够」，更像是顺理成章地取用。"
    "饮料被稳稳地拿了下来。"

    voice "cv3/epilogue/Noctella_story_14.ogg"
    noctella "这个，可以吗？"

    "银铃般的声音将我拉回现实，她回头看我，语气礼貌得无可挑剔。"
    "我张了张嘴。"
    "脑子里冒出了一个完全不合时宜的问题。"
    "——这是我家还是她家？"

    me "啊……可以是可以，你就是想要这个才来的厨房？\n那你是怎么知道它放在什么地方的。"

    "诺提拉点点头。"

    voice "cv3/epilogue/Noctella_story_15.ogg"
    noctella "嗯，应该在那里。"

    "……是什么禅宗问答吗？"

    $ noctella.show("无口", pos=right, x_offset=-150)
    "她没再管我，只是把果汁抱在怀里，转身走回客厅。"
    "脚步轻快。"
    "我站在原地，看了两秒。"
    "真是……好有个性的女孩子。"
    "宛如来自异度空间的存在，自顾自地、循着某种未知轨迹，侵入了我的生活场域。"
    "不过，感觉不坏。"
    "于每天沿着既定轨道运行的日子里，不过是按时吃饭，按时睡觉，做完该做的事，再等着下一天到来。"
    "明天和今天一样，今天和昨天一样。"
    "所以，这场意外的闯入，说不准也为我带来了一点点欢愉。"

    me "哎，已经做好了，你先去坐着。"

    "我大概是笑着说的。"
    "她听闻，慢吞吞地转身看了看我，很认真地点了一下头，接着便走了出去。"
    "我注意到，她走路的时候几乎没有声音，脚步如猫儿一般。"
    "……"

    # === 【客厅】 ===
    scene bg living_room2 with dissolve
    $ noctella.show("无口", pos=center, x_offset=0)

    "我把碗放在茶几上，又递给她一双筷子。"

    me "吃吧。"
    me "小心烫，刚泡好的。"

    voice "cv3/epilogue/Noctella_story_16.ogg"
    noctella "嗯，谢谢。"

    "诺提拉慢慢坐到椅子上，动作很轻柔，又带着些许优雅，那是种不符合她这个年纪的小朋友该有的动作。"
    "她接过筷子，低头看着面前的食物。"
    "并没有立刻动筷，而是盯着那碗面看了好几秒。"

    me "怎么了？不合胃口？"

    "诺提拉摇了摇头。"

    voice "cv3/epilogue/Noctella_story_17.ogg"
    noctella "⋯⋯好香。"

    "她的声音很轻，带着一丝我不太能分辨的情绪。"
    "然后，她开始吃了。"
    "少女拿起勺子扒拉了一勺送进嘴里，看不出来表情。"

    me "好吃吗？"

    voice "cv3/epilogue/Noctella_story_18.ogg"
    noctella "10分。"

    me "吼吼，这么合你口味啊。"

    voice "cv3/epilogue/Noctella_story_19.ogg"
    noctella "满分是100分。"

    me "……"
    "这家伙还挺坏心眼的。"
    "唔，我就知道，平时都是我一个人住，也没有朋友来家里吃过饭。"
    "厨艺这块，只能算可以吃的程度。"

    voice "cv3/epilogue/Noctella_story_20.ogg"
    noctella "但是很好吃。"

    me "哦，哦。"
    "这补充的一句是安慰？\n真是让人心情复杂。"
    "我大口大口吃着眼前的泡面，全无对座少女的半分优雅——只见她伸出纤白指尖，娴熟地开启汽水，送至唇边轻轻一抿。"

    me "酸吗？"

    voice "cv3/epilogue/Noctella_story_21.ogg"
    noctella "气泡在舌尖跳动，很解渴……"

    me "你喜欢喝汽水？"

    voice "cv3/epilogue/Noctella_story_22.ogg"
    noctella "喜欢这种……活着的感觉。"

    "我自认为我是个比较自私的家伙，并不在意别人活得怎么样，但看着她像小动物一点一点吃饭的样子，还是很好奇她为什么会出现在这里。"

    me "嗯……那你有朋友吗？"

    voice "cv3/epilogue/Noctella_story_23.ogg"
    noctella "没有哟。"

    "风轻而云淡，很无所谓的样子。"

    me "好吧。"

    "总感觉很难和她开口说点什么，于是，周遭的时间也识趣地慢了下来。"
    "就这样，在氤氲的泡面热气与无声的沉默交织中，我竟品出了一丝奇怪的安逸。"
    "直到咽下最后一口。"

    me "吃完就放着，我来收拾。"

    $ noctella.show("微笑")

    "对面的少女靠在沙发背上，双手轻轻捧着自己的肚子。"
    "那个姿势，配上她微微眯起的眼睛，和嘴角残留的一点汤汁⋯⋯"
    "说实话，和刚才她给我的氛围，简直判若两人。"

    me "吃饱了没？"

    "诺提拉缓缓点头。"

    voice "cv3/epilogue/Noctella_story_24.ogg"
    noctella "⋯⋯饱了。"

    "声音软软的，带着餐后的慵懒。"
    "我看着她那副心满意足的样子，忽然不知道该说什么了。"
    "她的脸颊微微鼓起，耳尖也泛着一点淡淡的粉色。"
    "有着一种……很奇怪的可爱。"

    me "喂。"

    voice "cv3/epilogue/Noctella_story_25.ogg"
    noctella "⋯⋯我在哦。"

    "她半睁着眼睛看向我。"
    "我指了指自己的嘴角。"

    me "这里，有东西。"

    "少女愣了一下，然后伸出舌尖，舔了舔唇边。"
    "那个动作，让我瞬间移开了视线。"

    me "⋯⋯总之，你吃饱了就好。"

    "我站起身，开始收拾茶几上的碗筷。"
    "她没有说话，只是用那双金色的眼眸，静静地注视着我。"

    # === 【客厅 - 睡前】 ===
    "吃完夜宵，已经到就寝的时间了，我也不准备再玩什么游戏。"
    "更何况……现在还面临一个很严肃的问题。"

    me "那个，诺提拉。"

    voice "cv3/epilogue/Noctella_story_26.ogg"
    noctella "嗯？"

    me "你这边⋯⋯后面有什么打算？"

    "我隐晦地提了提问。"
    "诺提拉歪了歪头，似乎不太理解我的意思。"
    "我换了个问法。"

    me "你有要去的地方吗？或者说，有认识的人可以投靠吗？"

    $ noctella.show("无口")
    "诺提拉只是静静地看着我。"
    "那沉默持续了很长时间。"
    "长到我以为她不打算回答了。"
    "然后，她轻轻点了点头。"

    me "？"
    "然后，她轻轻点了点头。"

    me "……"
    me "啊？"

    voice "cv3/epilogue/Noctella_story_27.ogg"
    noctella "要去的地方，我已经到了⋯⋯大概，是这样的。"

    me "⋯⋯"
    "这回答，怎么听都像是在敷衍。"
    "但看她的神情，又不像是在说谎。"
    "她只是用那双金色眼眸平静地看着我，眼神清澈得不含一丝杂质。"
    "我叹了口气。"

    me "……行吧。\n虽然完全听不懂你在说什么。"

    $ noctella.hide()
    "我转过身，没去关灯，而是走到窗边。"
    "窗外，路灯在沥青路上投下橘色的波光，似乎先前下了点小雨，偶尔有一辆车滑过水坑，声音像撕开绸缎。"
    "看了两眼，我就走了回去。"

    $ noctella.show("无口", pos=center, zoom=0.7, y_offset=-350)
    me "可能还会下雨……你带伞了吗？"

    voice "cv3/epilogue/Noctella_story_28.ogg"
    noctella "我不需要伞。"

    me "今天先呆我这也没事，如果你没地方去，沙发可以借你。"

    "我回头看她，少女并没有露出感激或者局促的神色，她只是安静地坐在那，像是一尊被安置在现代客厅里的古老摆件。"
    play sound fx.cans
    "她伸出指尖，轻轻拨弄着刚才那个空掉的粉色魔爪罐子。"
    play sound fx.cans
    "那个声音在安静的客厅里显得格外突兀。"

    voice "cv3/epilogue/Noctella_story_29.ogg"
    noctella "这里的氛围，很暖和。"

    "她的视线锁定了我。"

    voice "cv3/epilogue/Noctella_story_30.ogg"
    noctella "不是在说温度。"

    me "？"

    "我也不知道该如何回复才好，所以只能一头雾水打开柜子，抱出一床叠得并不整齐的备用小被，还有一只印着滑稽猫猫头图案的软枕。"

    me "给，洗手间在那边，牙刷……你先用我备用的，你要洗澡吗？"

    voice "cv3/epilogue/Noctella_story_31.ogg"
    noctella "我身上，没有灰尘。"

    me "哈，你这回答还真是够仙气。"

    "说出口的同时，我却觉得，她的言语莫名能让人信服……"
    "少女周身纤尘不染，光洁的服装、肌肤与眼眸，共同勾勒出一种看似寻常却毫无冗余的至纯存在，她的轮廓线条仿佛能切开室内的暖色灯光。"
    "我抱着被子靠近她，这时甚至还闻到了一股味道，不太像是沐浴露，有点那种老旧整洁的书房中，清冷而沉静的气味。"
    "我将被子放在沙发上，然后下意识地往后退了一半步。"

    me "那我去睡了，有事叫我。"

    "进入自己卧室前，我回头看了一眼。"
    "被整个客厅空间吞没的她，如此渺小，\n她太小了，揉进那张沙发里，显得像个精致的洋娃娃。"
    stop music fadeout 1.0

    # === 【卧室】 ===
    $ noctella.hide()
    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene black
    $ renpy.pause(1.0, hard=True)
    scene bg computer_desk with fade
    play music "audio/bgm/BGM_gymnopedie-1.ogg" loop fadein 1.0

    "我坐在电竞椅上，并没有立刻关机。"
    "屏幕里，刚刚通关的Galgame还停留在全收集后的主界面内。"
    "蓝白色的荧光打在我的脸上，在这间没开灯的卧室里显得有些落寞。"
    "我把鼠标移到退出游戏按钮上，准备退出。"

    # 诺提拉突然出现在卧室
    voice "cv3/epilogue/Noctella_story_32.ogg"
    noctella "她笑了。"

    "我猛地回头。"
    $ noctella.show("无口", pos=left, x_offset=250, zoom=1.35, y_offset=400)
    "少女不知什么时候起已经站在了我电竞椅旁边，没有敲门，就这样无声无息地潜入了这块最私密的领地。"

    me "……喂，吓我一跳。"

    "她没有回应我，目光越过我的肩膀，直勾勾地盯着电脑。"
    "诺提拉慢慢走近，屏幕的冷光攀上她的脸颊，将那双金色的眼瞳染上了一层虚幻色彩。"

    voice "cv3/epilogue/Noctella_story_33.ogg"
    noctella "你……喜欢Galgame吗？"

    "啊？"
    "少女转过头看着我。\n在屏幕荧光的映衬下，她的肤色白得近乎透明。"
    "一时间，我没太懂她在说什么。"
    "房间里陷入了粘稠的沉默，只有电脑主机风扇在轻微地嗡鸣，诺提拉看着我，眼神内透着一种有如天真般的审视。"

    voice "cv3/epilogue/Noctella_story_34.ogg"
    noctella "Galgame，你喜欢吗？"

    me "哦……哦。"
    "问我喜不喜欢Galgame？这妹子的话题还真是跳脱……怎么说呢，能从这样一个女孩子的嘴里听到Galgame这个词，让我的心情有些奇怪。"

    me "没那么喜欢吧……只是恰巧在玩而已。"

    "我停下了鼠标，继续让屏幕留在游戏的主界面。"

    voice "cv3/epilogue/Noctella_story_35.ogg"
    noctella "她在笑，是吗。"

    "她伸出手，指尖停在屏幕中那个二次元少女的脸庞前几厘米处，没有碰触到，只是隔空描摹着轮廓。"

    me "额，是的。"

    $ noctella.show("微笑")
    voice "cv3/epilogue/Noctella_story_36.ogg"
    noctella "为了让她笑……你努力了呢，乖孩子。"

    me "……大概？\n这只是主界面，不管我打通什么结局，回到这里都是这个画面就是了。"
    "实不相瞒，我有点懵。"
    "到底是我疯了还是这个世界疯了，我居然在我的房间里，和这样一个小小的女孩子，聊Galgame？"
    "我的妈耶……"
    "话说，这对于她来说，不是很危险吗，\n要知道我可是独居的单身年轻小伙子……嘶，这家伙心脏是真大。"

    $ noctella.show("无口")
    voice "cv3/epilogue/Noctella_story_37.ogg"
    noctella "如果选错了选项，她会哭吗？"

    me "好像也不会？只不过结局可能会有一些遗憾吧……当然，我觉得并不悲伤，反而完美结局太圆满了，让我觉得不太真实。"

    voice "cv3/epilogue/Noctella_story_38.ogg"
    noctella "圆满是不真实的，所以你更喜欢支离破碎的真实？"

    me "倒也不能这么说，我只是为了看一下所有结局，所以全打了一遍而已，称不上有多少想法……"

    "少女点了点头。"
    "我继续说道。"
    
    me "可能是和合理性有关，因为和我想象的不太一样，才多少会认为有些奇怪。"

    voice "cv3/epilogue/Noctella_story_39.ogg"
    noctella "嗯……不合理，不正常，不符合预设……"
    voice "cv3/epilogue/Noctella_story_40.ogg"
    noctella "这样的话，我就明白了……"

    me "明白什么？"

    $ noctella.show("神之笑")
    voice "cv3/epilogue/Noctella_story_41.ogg"
    noctella "因为，你的世界，就是靠这种方式运行的。"

    me "我只是在玩游戏哦，现实里可没有存档读档，也没那么多选项给你选。"

    voice "cv3/epilogue/Noctella_story_42.ogg"
    noctella "真的吗？"

    $ noctella.show("神之笑", pos=center, x_offset=80, zoom=1.8, y_offset=1000)
    "她忽然凑近了一点，我能感觉到她身上那股清冷的气息压过了电子元件发热的味道。"
    voice "cv3/epilogue/Noctella_story_43.ogg"
    noctella "今天对于你而言，是符合预设的一天，还是不符合预设的一天？"

    "……看来是，不符合预设的一天。"

    voice "cv3/epilogue/Noctella_story_44.ogg"
    noctella "你现在面对我……是在选哪个选项？"

    "她的鼻尖距离我不到十厘米，金色的眼瞳内倒映出我那张略显慌乱的脸。"
    "被这样一双眼睛盯着，我呼吸一滞，刹那间，甚至有种自己会被抛入异世界中，日常生活顷刻被颠覆的错觉。"

    me "……让我想想啊。"
    me "嗯，也许我该选「礼貌地请她出去」。"
    me "你觉得如何。"

    voice "cv3/epilogue/Noctella_story_45.ogg"
    noctella "选项A：请她出去。\n选项B：让她留下。"

    "她微微歪头，嘴角勾起一个极小的弧度\n——见证之时，我自心底感到战栗。"
    "仿佛路西法在门后微笑。"

    voice "cv3/epilogue/Noctella_story_46.ogg"
    noctella "为什么不是选第二个选项？"

    "……"
    "看了看她的脸庞……我开始思考……"
    "是要判几年来着……"
    "如果我年龄小一点，是不是……"

    voice "cv3/epilogue/Noctella_story_47.ogg"
    noctella "呼呼~在重要选项前，要存档么。"

    me "可惜存不得啊。"

    voice "cv3/epilogue/Noctella_story_48.ogg"
    noctella "唔……我可以让你存档哦。"

    me "咦？什么意思。"

    voice "cv3/epilogue/Noctella_story_49.ogg"
    noctella "谁知道呢，我只是想这么说而已~"

    me "……"
    me "你喜欢Galgame？我看你似乎很感兴趣的样子。"
    "我问出了这样一句话。"
    $ noctella.show("无口")
    "少女直直的盯着我看，先前的调皮荡然无存，给我一种她开始认真了的感觉。"

    voice "cv3/epilogue/Noctella_story_50.ogg"
    noctella "喜欢。"

    "——我有点心跳加速。"

    voice "cv3/epilogue/Noctella_story_51.ogg"
    noctella "Galgame，喜欢。"

    me "……呵呵，不赖，挺难得的。"

    "接着，宛如鲜花绽放一般，她，露出笑容。"

    $ noctella.show("微笑")
    voice "cv3/epilogue/Noctella_story_52.ogg"
    noctella "你，我也喜欢。"

    play sound fx.heartbeat
    me "————"
    "语出惊人的少女，就这样自斜下方仰视着我，使我一时之间没能理解她诉说的话。"

    me "啊……"
    me "这……"

    voice "cv3/epilogue/Noctella_story_53.ogg"
    noctella "嗯？"

    "她倒是一副觉得我大惊小怪的样子。"

    voice "cv3/epilogue/Noctella_story_54.ogg"
    noctella "你也喜欢Galgame，不是么？"

    me "但这和喜欢我是两码事吧……"

    voice "cv3/epilogue/Noctella_story_55.ogg"
    noctella "一样的哦。"

    me "哦……是，是吗。"

    "过于奇异的对话，使得我只能被动回应。"

    voice "cv3/epilogue/Noctella_story_56.ogg"
    noctella "嗯，没关系的，没问题的。"

    "到底是哪里没关系，又到底是哪里没问题，什么都搞不明白了。"
    "和这位迷之少女呆在同一个空间中，感觉就像在做梦，难不成，我已经在梦乡中了？"
    "该说她呆萌呢，还是说，她的话语是有着某种深意呢。"
    "不知为何，听着她的声音，有种……奇特的安心感涌上心头。"
    "我也不愿去思考那么多了。"

    voice "cv3/epilogue/Noctella_story_57.ogg"
    noctella "感觉你有点累，要姐姐抱抱吗？"

    me "诶……不是，你这小东西，调戏我是吧……"

    "就在我差点绷不住要笑出来时。"

    $ noctella.show("微笑", pos=center, x_offset=80, zoom=2.2, y_offset=1500)
    play sound fx.fabric_collision
    show bg white with flash
    "啪——"

    me "哎？"

    "清冷的气息，混合着如婴儿一般的牛奶味道，丝丝缕缕钻入鼻腔，我感受着将自身包裹起来的热度，失声了。"
    "她真的——抱住了我。"

    show bg computer_desk with dissolve
    me "……"
    "电脑内风扇转动的细微噪音，在此刻仿佛被放大了数倍，成了房间里唯一的背景音。"
    "她的怀抱并不像我想象中那样带着少女的羞涩或局促，反而异常的……平静。"
    "这份温热持续且稳定，一点点地吸纳掉我周身的防备和那股如影随形的疲惫。"

    voice "cv3/epilogue/Noctella_story_58.ogg"
    noctella "怎么样？"

    me "……"

    voice "cv3/epilogue/Noctella_story_59.ogg"
    noctella "那就好。"

    "我的头被她柔和地按在胸口上，少女小小的胸膛，此刻却有如母亲一般宽广……或许是久远的记忆苏醒了，我有点……恋恋不舍。"

    voice "cv3/epilogue/Noctella_story_60.ogg"
    noctella "叫我妈妈也可以哦？"

    me "嗳？妈妈？"
    "我被吓到了。"

    $ noctella.show("微笑")
    voice "cv3/epilogue/Noctella_story_61.ogg"
    noctella "嗯，乖孩子。"

    me "……我不是那个意思。"

    voice "cv3/epilogue/Noctella_story_62.ogg"
    noctella "那是什么意思？呵呵。"

    me "……"
    "现在，大概已经过了零点了吧。"
    "过完这一天，休息日就结束了……\n原本，我确实有点……累，身体……也沉甸甸的。"
    "少女的小手轻轻抚弄着我的头，我感受着她的气息，整个人都轻盈了起来，不可思议，随着抚摸，阴霾被逐渐扫清。"
    "几根发丝随着她的动作，在我的脸庞上剐蹭起来，产生了丝丝麻麻的瘙痒感。"

    "于是，我贪婪地问出了不该问的话。"

    me "你会走吗？"

    voice "cv3/epilogue/Noctella_story_63.ogg"
    noctella "我会走，就像所有事情最终都会发生。"

    me "你存在吗？"

    voice "cv3/epilogue/Noctella_story_64.ogg"
    noctella "我存在，就像存在本身。"

    me "我现在是在做梦吗？"

    voice "cv3/epilogue/Noctella_story_65.ogg"
    noctella "或许你正在醒来，只是醒在另一场梦里。"

    me "那你呢？你是梦还是现实？"

    voice "cv3/epilogue/Noctella_story_66.ogg"
    noctella "对你而言，有区别吗？"

    me "……"
    "她的声音蕴含着特有的磁性，十分之温柔，令我感到释然。"

    me "我们还能再见么？"

    voice "cv3/epilogue/Noctella_story_67.ogg"
    noctella "还能再见的。"
    voice "cv3/epilogue/Noctella_story_68.ogg"
    noctella "Galgame，你会一直玩下去，对吧。"

    me "……或许。"

    voice "cv3/epilogue/Noctella_story_69.ogg"
    noctella "只要你还愿意点开下一个故事，我们就可能再度相逢。"

    me "在游戏里？"

    voice "cv3/epilogue/Noctella_story_70.ogg"
    noctella "在任何地方。"

    me "看来以后要多玩Galgame了……"

    voice "cv3/epilogue/Noctella_story_71.ogg"
    noctella "嗯，如果是你的话，一定没有问题的，终有一天……你会在某个地方遇见我。"

    me "这样么，那我可要期待了……"
    "我能感觉到她的指尖划过我的发缝，动作轻柔得像是某种古老仪式。"

    voice "cv3/epilogue/Noctella_story_72.ogg"
    noctella "要睡觉了么？要睡的话，那就睡吧。"

    me "……我还想和你多呆一会儿。"

    "然而，麻酥酥的感觉从头皮蔓延到脊椎，带走了最后的一丝清醒。"

    voice "cv3/epilogue/Noctella_story_73.ogg"
    noctella "存档……已经完成了，这个格子的内容，永远不会消失。"
    voice "cv3/epilogue/Noctella_story_74.ogg"
    noctella "就算明天醒来，你不记得我。"
    voice "cv3/epilogue/Noctella_story_75.ogg"
    noctella "今天，也已经被记录在世界。"

    me "嗯，世界不世界的，无所谓吧，反正我会记得的……这一天……"

    "我迷迷糊糊地嘟囔着，眼皮像灌了铅一样沉重。"

    voice "cv3/epilogue/Noctella_story_76.ogg"
    noctella "辛苦了，一直以来，都在努力达成Happy End的你。"

    me "也没有……其实……我一直在努力达成的，都是True End……"

    voice "cv3/epilogue/Noctella_story_77.ogg"
    noctella "那么，现在就是True End。"

    "我听到了她轻细的笑声，像是一阵掠过风铃的微风。"

    voice "cv3/epilogue/Noctella_story_78.ogg"
    noctella "晚安，玩家。"

    stop music fadeout 2.0
    show cinematic_black_overlay
    $ renpy.pause(2.0, hard=True)
    scene black
    $ renpy.pause(2.0, hard=True)

    $ achievement.grant("ACH_08")
    $ achievement.sync()
    return