#!/usr/bin/python3
# -*- coding: utf-8 -*-

FRONT_CAM = 0   # 前摄像头编号
SIDE_CAM = 2    # 边摄像头编号
LEFT_CAM = 1  # 左摄像头编号
RIGHT_CAM = 3  # 右摄像头编号

#侧边1.15
task = {
        1:{"label":"采购货物", "angle":-50, "check":True, "location":True, "sign":4, "index":[9]},
        2:{"label":"文化交流", "angle":130, "check":True, "location":False, "sign":1, "index":[1, 4, 8]},
        3:{"label":"守护丝路", "angle":130, "check":True, "location":True, "sign":3, "index":[2, 3, 6, 7]},
        4:{"label":"守护丝路", "angle":130, "check":True, "location":True, "sign":3, "index":[2, 3, 6, 7]},
        5:{"label":"放歌友谊", "angle":130, "check":False, "location":False, "sign":2, "index":[5]},
        6:{"label":"守护丝路", "angle":130, "check":True, "location":True, "sign":3, "index":[2, 3, 6, 7],},
        7:{"label":"文化交流", "angle":130, "check":True, "location":False, "sign":1, "index":[1, 4, 8], },
        8:{"label":"翻山越岭", "angle":130, "check":False, "location":False, "sign":5,"index":[11],},
        9:{"label":"文化交流", "angle":130, "check":True, "location":False, "sign":1, "index":[1, 4, 8],},
        10:{"label":"以物易物", "angle":-50, "check":True, "location":False, "sign":6, "index":[10]},
        11:{"label":"守护丝路", "angle":-50, "check":True, "location":True, "sign":3,"index":[2, 3, 6, 7]},
        }
        
task_functions = {
                1:{"label":"alamutu","location":False, "position":[540,340]}, # 位置7 阿拉木图
                2:{"label":"badperson1","location":False, "position":[550, 158]}, # 位置10 坏人1   已改
                3:{"label":"badperson2","location":False, "position":[550, 158]}, # 位置3 坏人2   已改
                4:{"label":"dunhuang","location":False, "position":[540,340]},  # 位置2 敦煌     已改
                5:{"label":"friendship","location":False, "position":[]},   #位置5 放歌友谊
                6:{"label":"goodperson1","location":False, "position":[550, 250]},    # 位置4 好人1
                7:{"label":"goodperson2","location":False, "position":[550, 250]},    # 位置6 好人2
                8:{"label":"jstdb","location":False, "position":[540, 340]},  # 位置8 君士坦丁堡
                9:{"label":"purchase","location":True, "position":[240,340]},    # 位置1  采购货物
                10:{"label":"trade","location":True, "position":[230,100]},  # 位置9  以货易货
                11:{"label":"seesaw","location":False, "position":[]},  # 位置9 翻山越岭
                20:{"label":"trade","location":True, "position":[230,100]},  # 位置9  以货易货
                12:{"label":"badperson1","location":False, "position":[40, 158]}, # 坏人1
                13:{"label":"badperson2","location":False, "position":[40, 158]}, #  坏人2
                16:{"label":"goodperson1","location":False, "position":[40, 250]},    #  好人1
                17:{"label":"goodperson2","location":False, "position":[40, 250]},    #  好人2
                }
CONTROLLER = "mc601"
# CONTROLLER = "wobot"


REC_NUM = 3    # 图标出现次数而统计确认识别结果

POSITION_THRESHOLD = 10    # 位置偏差阈值

HIGH_SPEED = 40         # 高速速度
FULL_SPEED = 32
# 中速速度
SLOW_SPEED = 20         # 慢速速度，加速速度
ACCELERATION_TIME = 3   # 启动时间

SIGN_LOCATE_TIME = 1.4
LOCATE_TIME = 8

sign_label = {"background": 1, "castle": 1, "friendship": 1, "guard": 1, "purchase": 1, "seesaw":1, "trade": 1}
TASK_LIST = []
TASK_LABEL = ["background", "alamutu", "badperson", "badperson2", "dunhuang", "friendship", "goodperson", "goodperson2", "jstdb", "purchase", "trade"]