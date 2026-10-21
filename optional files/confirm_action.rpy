## 自定义确认动作 #######################################################
##
## 此文件包含一个类似于 Confirm 屏幕动作的动作，
## 可用于信息和确认提示。
## 如果不需要可以删除。为了正常工作，需要在确认屏幕上设置
## `no_action=None`，以便第二个动作是可选的
## (此模板默认情况下就是这样)。
## 你可以毫无影响地删除此文件。
## 在此处查看原始的 Confirm 动作：
## https://www.renpy.org/doc/html/screen_actions.html#Confirm
##
## 它有三个主要用例：
## 1) CConfirm("你还没有解锁这张图片。")
##      这会向用户显示一个带有提供文本的提示和一个
##      "确认"按钮来关闭提示。没有"取消"按钮。
## 2) CConfirm("购买花？($10)", SetVariable('money', money-10))
##      这会显示一个带有确认和取消按钮的提示。确认
##      按钮会关闭提示并执行提示后提供的动作或动作列表，
##      而取消会隐藏提示而不执行任何其他动作。
## 3) CConfirm("前往下一章？", yes=Jump("chapter2"), no=MainMenu())
##      这会显示一个带有确认和取消按钮的提示。点击任一
##      按钮都会关闭提示，同时执行提供的 yes/no 动作。
##

init python:

    class CConfirm(Show):
        """
        一个类，使向玩家显示简单的确认提示变得容易。

        它还将 confirm_selected 的默认值设置为 True 而不是 False。
        """
        def __init__(self, prompt, yes=None, no=None, confirm_selected=True,
                *args, **kwargs):

            if config.confirm_screen and renpy.has_screen('confirm'):
                screen = "confirm"
            elif renpy.has_screen("yesno_prompt"):
                screen = "yesno_prompt"
            else:
                screen = None

            # 仅提示；这只会显示一个关闭提示的确认按钮。
            if yes is None:
                yes = Hide(screen, config.exit_yesno_transition)
                no = None
            else:
                # 所有提供的动作在被点击后都应该隐藏确认屏幕
                if isinstance(yes, list):
                    yes.insert(0, Hide(screen, config.exit_yesno_transition))
                elif yes != Hide(screen, config.exit_yesno_transition):
                    yes = [Hide(screen, config.exit_yesno_transition), yes]

                # 有两个按钮，但"取消"应该只是隐藏提示
                if no is None:
                    no = Hide(screen, config.exit_yesno_transition)
                elif no is not None:
                    if isinstance(no, list):
                        no.insert(0, Hide(screen, config.exit_yesno_transition))
                    elif no != Hide(screen, config.exit_yesno_transition):
                        no = [Hide(screen, config.exit_yesno_transition), no]

            self.prompt = prompt
            self.yes = yes
            self.no = no
            self.confirm_selected = confirm_selected
            self.screen = screen

            super(CConfirm, self).__init__(screen, config.exit_yesno_transition,
                *args, message=self.prompt, yes_action=self.yes,
                no_action=self.no, **kwargs)

        def get_sensitive(self):
            if self.yes is None:
                return False

            return renpy.is_sensitive(self.yes)

        def get_selected(self):
            return renpy.is_selected(self.yes)

        def get_tooltip(self):
            return renpy.display.behavior.get_tooltip(self.yes)

        def __call__(self):

            if self.screen is None:
                return Confirm(self.prompt, self.yes, self.no, self.confirm_selected)()
            elif self.confirm_selected or not self.get_selected():
                return super(CConfirm, self).__call__()
            else:
                return renpy.run(self.yes)