# character_core.rpy

#临时修改：把anim_shake和anim_jump加入到core调用


transform anim_shake(z=1.0, x=0, y=0):
    # 基础状态保持
    zoom z
    yoffset y
    # 震动逻辑 (相对于当前的 x)
    subpixel True
    # 先设置初始偏移为 0
    xoffset x
    easein 0.05 xoffset x + 10
    easeout 0.05 xoffset x -10
    easein 0.05 xoffset x + 10
    easeout 0.05 xoffset x

transform anim_jump(z=1.0, x=0, y=0):
    # 基础状态保持
    zoom z
    xoffset x
    # 跳跃逻辑 (相对于当前的 y)
    yoffset y
    subpixel True
    # 从当前位置向上偏移 30 像素
    easein 0.15 yoffset y - 30
    # 归位到 0 相对偏移（即动画前的位置）
    easeout 0.15 yoffset y

# 【关键点 1】定义一个全局字典来存储所有角色的运行时状态
# 使用 default 声明，确保它会被 Ren'Py 的存档/读档/回滚系统完美追踪
default actor_states = {}

init python:
    import os

    class Actor(object):
        """
        角色封装类：逻辑代理。
        注意：它现在是一个"无状态"的包装器，实际数据存储在 store.actor_states 中。
        """
        def __init__(self, code, config_data):
            self.code = code
            self.name = config_data["name"]
            self.voice_tag = config_data.get("voice_tag")
            self.color = config_data["color"]
            self.expressions = config_data["expressions"]
            
            # 样式配置 (这些是静态配置，不需要存入存档)
            self.style_config = config_data.get("style", {})
            self.zoom = self.style_config.get("zoom", global_actor_settings["zoom"])
            self.y_offset = self.style_config.get("y_offset", global_actor_settings["y_offset"])
            
            # 创建原生的 Ren'Py Character 对象
            self._rpy_char = Character(self.name, color=self.color, image=code,voice_tag=self.voice_tag)
            
            # 自动注册立绘图像
            self._register_images()

        # 【关键点 2】获取当前角色的实时状态数据
        def _get_state(self):
            # 如果字典里还没这个角色的数据（比如刚开始游戏），初始化它
            if self.code not in store.actor_states:
                store.actor_states[self.code] = {
                    "last_at_list": [],      # 记录位置
                    "current_expression": None, # 记录表情
                    "current_zoom": 1.0,  # 【新增】默认动态倍率为 1.0
                    "current_y_offset": 0,
                    "current_x_offset": 0
                }
            return store.actor_states[self.code]

        def _register_images(self):
            for expr_name, file_path in self.expressions.items():
                image_tag_name = "{} {}".format(self.code, expr_name)
                
                # if renpy.exists(file_path):
                actor_style = self._create_actor_style()
                renpy.image(image_tag_name, At(Image(file_path), actor_style))
                # else:
                    # 调试用：如果找不到图，显示文字
                    # renpy.image(image_tag_name, Text(expr_name, size=50))

        def _create_actor_style(self):
            return Transform(
                xanchor=0.5,
                yanchor=1.0,
                zoom=self.zoom,
                yalign=1.0,
                yoffset=self.y_offset,
                subpixel=True
            )

        def __call__(self, what, voice_file=None , **kwargs):
            
            
            
            
            # 调用原生的 Ren'Py Character 对象进行对话
            
            self._rpy_char(what, **kwargs)

        # --------------------------------------------------------
        # 封装的演出接口 (读写均通过 _get_state)
        # --------------------------------------------------------

        def show(self, expression, pos=None, transition=dissolve, zoom=None, y_offset=None, x_offset=None):
            """
            切换立绘表情。
            """
            state = self._get_state()
            name_tuple = (self.code, expression)
            
            # 更新状态：表情
            state["current_expression"] = expression
            
            # 更新状态：位置
            if pos:
                self.set_position(pos)
            
            # 读取当前位置（如果没有位置，默认为 center）
            current_at = state["last_at_list"] if state["last_at_list"] else [center]
            
            # 如果是第一次显示且没有指定位置，必须保存这个默认位置
            if not state["last_at_list"]:
                state["last_at_list"] = [center]
                current_at = [center]

            # 定义缩放
            if zoom is not None:
                state["current_zoom"] = zoom
            
            # y轴
            if y_offset is not None:
                state["current_y_offset"] = y_offset
            
            # x轴
            if x_offset is not None:
                state["current_x_offset"] = x_offset
            
            dynamic_transform = Transform(
                zoom=state["current_zoom"], 
                yoffset=state["current_y_offset"],
                xoffset=state["current_x_offset"]
            )

            # 组合 At List (位置 + 动态缩放)
            final_at_list = list(current_at) + [dynamic_transform]

            # 执行显示命令（在后台更新图层，此时玩家还看不到变化）
            renpy.show(name_tuple, at_list=final_at_list)

            # 只在 show 之后调用一次 transition
            if transition:
                # 这一步会将画面从“旧表情”渐变到“新表情”R
                # 不直接写 renpy.with_statement(transition)
                # 而是指定：只对 "master" 层应用这个 transition
                # "screens" 层（对话框所在层）保持静止，不参与转场
                renpy.with_statement({"master": transition})

        def hide(self, transition=dissolve):
            renpy.hide(self.code)
            
            # 清除状态
            state = self._get_state()
            state["current_expression"] = None
            
            if transition:
                renpy.with_statement(transition)

        def reset_position(self):
            state = self._get_state()
            state["current_zoom"] = 1.0  # 缩放默认是 1.0
            state["current_y_offset"] = 0 # 偏移默认是 0
            state["current_x_offset"] = 0
            state["last_at_list"] = []
            
        def set_position(self, pos):
            """
            同步位置记忆
            """
            state = self._get_state()
            if pos:
                state["last_at_list"] = [pos] if not isinstance(pos, list) else pos
            else:
                state["last_at_list"] = []

        def act(self, action_transform):
            #"""
            #执行特殊演出
            #"""
            #state = self._get_state()
            #expr = state["current_expression"]

            # 确定 tag
            #if expr:
                #tag = (self.code, expr)
            #else:
                #tag = self.code
            
            # 获取当前位置
            #current_at_list = state["last_at_list"] if state["last_at_list"] else [center]

           
            
            # 应用动作
            #renpy.show(tag, at_list=current_at_list + [action_transform])
            
            #renpy.pause(0.3, hard=True)
        
            """
            执行特殊演出 (支持 anim_shake 和 anim_jump 并保留当前位置/缩放)
            调用示例:
                lx.act(anim_shake)
                lx.act(anim_jump)
            """
            state = self._get_state()
            expr = state["current_expression"]

            # 确定 tag (如果有表情，tag是元组)
            if expr:
                tag = (self.code, expr)
            else:
                tag = self.code
            
            # 1. 获取当前的基础位置 (如 left, center, right)
            base_at_list = state["last_at_list"] if state["last_at_list"] else [center]

            # 2. 获取当前的动态属性 (缩放和偏移)
            c_zoom = state["current_zoom"]
            c_x = state["current_x_offset"]
            c_y = state["current_y_offset"]

            # 3. 判断传入的 transform 是否是我们定义的特殊动作
            # 我们需要检查传入的变量是否是那两个 ATL 变换
            # 注意：在 Python 中访问 Ren'Py 的 transform 需要用 store.前缀或者直接比较
            
            final_transform = None

            if action_transform in [anim_shake, anim_jump]:
                # 如果是震动或跳跃，我们将当前状态作为参数传进去
                # 这样动作就会在“当前缩放”和“当前偏移”的基础上执行
                final_transform = action_transform(z=c_zoom, x=c_x, y=c_y)
                
                # 设置等待时间：震动和跳跃大约需要 0.3~0.4 秒
                pause_time = 0.35
            else:
                # --- 兼容其他普通变换 ---
                # 如果传入的是其他未适配的变换，为了不丢失缩放，我们需要手动叠加
                # 先应用当前的静态属性，再应用动作 (注意：如果不小心覆盖了属性可能会有跳变)
                static_part = Transform(zoom=c_zoom, xoffset=c_x, yoffset=c_y)
                
                # 这里返回一个包含两个变换的列表给 renpy.show
                # 这种写法比较 hack，但对于简单变换有效
                # 更稳妥的是只用 final_transform = action_transform，但那样会丢失 zoom
                # 这里我们假设用户主要用 shake 和 jump
                final_transform = action_transform
                base_at_list = list(base_at_list) + [static_part] 
                pause_time = 0.3

            # 4. 执行显示
            # 注意：如果 final_transform 是参数化后的结果，它是一个单一的 Transform 对象
            renpy.show(tag, at_list=list(base_at_list) + [final_transform])
            
            # 5. 暂停等待动作完成
            renpy.pause(pause_time, hard=True)

            # 6. 【重要】动作结束后，恢复到静止状态
            # 因为 anim_shake 结束后虽然画面归位了，但此时图层上的 transform 还是 anim_shake 的实例
            # 为了防止后续操作出问题，我们立刻“重绘”一次角色的静止状态
            self.show(expr, transition=None)

    # --------------------------------------------------------
    # 初始化
    # --------------------------------------------------------
    actors = {}

    def init_actors():
        if 'CHARACTERS_CONFIG' in globals():
            for code, data in CHARACTERS_CONFIG.items():
                actor_instance = Actor(code, data)
                actors[code] = actor_instance
                # 将 Actor 实例注册到全局变量，方便脚本调用 (lx, jwq)
                setattr(store, code, actor_instance)
        else:
            print("Error: CHARACTERS_CONFIG not found.")

    init_actors()

# 普通角色定义保持不变
define cz = Character("陈舟", color="#ffffff")
define zhengke = Character("政客", color="#ffffff")
define me = Character("我", color="#ffffff")