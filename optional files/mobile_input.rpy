## 移动端输入 ################################################################
##
## 这是一个自定义的 InputValue，它不会以选中/准备输入的状态开始，
## 需要一个动作来启用它。按下回车键将再次禁用输入。
##
## 这使它成为大多数自定义输入屏幕的好选择，特别是
## 在移动设备上，键盘可能会占据大部分屏幕空间。
##
## 和往常一样，此文件可以毫无影响地删除。
##
## 在此处阅读更多关于 InputValue 的信息：
## https://www.renpy.org/doc/html/screen_python.html#inputvalue
##
init python:

    class EnterInputValue(FieldInputValue):
        """
        InputValue 的子类，允许回车键关闭输入按钮。
        不会以选中状态开始（因此，在移动端键盘不会立即出现）。
        """

        def __init__(self, object, field, default=False):
            self.object = object
            self.field = field

            self.default = default

        def enter(self):
            """当用户按下回车键时禁用此输入。"""
            renpy.run(self.Disable())
            raise renpy.IgnoreEvent()

default demo_name = "Feniks"

## 使用 EnterInputValue 的示例屏幕
screen name_input_screen():

    ## 这里的"object"是 `store`，因为它是一个常规的 store 变量。
    ## 如果变量是 persistent.name，则会使用 `persistent` 代替。
    default name_input = EnterInputValue(store, 'demo_name')

    add "#601249bb"

    vbox:
        align (0.5, 0.5)
        spacing 25
        button:
            background "#000b"
            hover_background "#0003"
            # 确保无需悬停此按钮即可输入
            key_events True
            # 启用输入
            action name_input.Toggle()
            has hbox
            spacing 25
            text "Name:"
            # 实际的输入，使用前面的 EnterInputValue
            input value name_input

        textbutton "Done" action Return() xalign 0.5