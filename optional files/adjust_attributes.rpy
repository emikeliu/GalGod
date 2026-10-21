## 调整属性 ###########################################################
##
## 这是一个特殊的配置值，可用于轻松创建分层图像的简写形式。
## 这段代码是从 Ren'Py Tom 关于此主题的文章中稍作改编而来：
## https://patreon.renpy.org/dev-2021-04.html#adjust-attribute-example
##
## 你可以在这里了解更多关于 config.adjust_attributes 的信息：
## https://www.renpy.org/doc/html/config.html#var-config.adjust_attributes
##
## 和往常一样，如果你不需要它，可以随意删除此文件。
##

init -100 python:

    class Aliases(object):
        """
        将属性扩展为其他属性。
        """

        def __init__(self, **aliases):

            # 从属性名称映射到它所扩展的属性元组
            self.aliases = { }

            for k, v in aliases.items():
                self.aliases[k] = tuple(v.split())

        def __call__(self, name):

            # 图像标签
            rv = [ name[0] ]

            # 剩余的属性
            for i in name[1:]:
                ## 如果是否定的，也移除提供的属性
                if i.startswith("-"):
                    prefix = "-"
                    i = i[1:]
                else:
                    prefix = ""

                for attr in self.aliases.get(i, ( i, )):
                    rv.append(prefix + attr)

            # 将结果转换回元组
            return tuple(rv)

## 一个可能的用例：
# define config.adjust_attributes['eileen'] = Aliases(
#     happy="eyes_happy mouth_happy",
#     concerned="eyes_concerned mouth_concerned",
# )