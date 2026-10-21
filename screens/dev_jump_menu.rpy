screen dev_jump_menu():

    tag menu

    frame:
        xalign 0.5
        yalign 0.5
        padding (40, 30)
        background "#0008"

        vbox:
            spacing 10

            text "开发调试 · 跳转章节" size 28

            textbutton "Scene 1-1" action Start(label="scene_1_1")
            textbutton "Scene 1-2" action Start(label="scene_1_2")
            textbutton "Scene 1-3" action Start(label="scene_1_3")
            textbutton "Scene 1-4" action Start(label="scene_1_4")
            textbutton "Scene 2-1" action Start(label="scene_2_1")
            textbutton "Interlude 1" action Start(label="interlude1")
            textbutton "Interlude 2" action Start(label="interlude2")
            textbutton "Scene 2-2" action Start(label="scene_2_2")
            textbutton "Scene 2-3" action Start(label="scene_2_3")
            textbutton "Scene 2-4" action Start(label="scene_2_4")
            textbutton "Scene 3-1" action Start(label="scene_3_1")
            textbutton "Scene 3-2" action Start(label="scene_3_2")
            textbutton "Scene 3-3" action Start(label="scene_3_3")
            textbutton "Scene 3-4" action Start(label="scene_3_4")
            textbutton "After Story" action Start(label="after_story_noctella")
            null height 15
            textbutton "返回主菜单" action ShowMenu("main_menu")