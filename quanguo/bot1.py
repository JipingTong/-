#!/usr/bin/python3
# -*- coding: utf-8 -*-
from re import T
import time
from config import *
# 导入路径
import set_path
from cart.widgets import *
from cart.driver import Driver
from camera import Camera
from detector.detectors import *
from task_func import *

front_camera = Camera(FRONT_CAM, [640, 480])
side_camera = Camera(SIDE_CAM, [640, 480])
driver = Driver()
cruiser = Cruiser(1)
# 地面标志检测
sign_detector = SignDetector()
# 侧边目标物检测
task_detector = TaskDetector(0)  # 这里需要填0原始颜色模型，除任务1后面全部一样
# 程序开启运行开关
start_button = Button_angel(1, "2")
# 程序关闭开关
stop_button = Button_angel(1, "4")
# 巡航开关
cruise_button = Button_angel(1, "3")

seesaw_button = Button_angel(1, "1")

servo1 = Servo(1)
task_9_flag = False

STATE_IDLE = "idle"
STATE_CRUISE = "cruise"
STATE_LOCATE_TASK = "sign_detected"
STATE_DO_TASK = "task"


sign_list = [0] * 11
order_num = 1
cam_dir = 1  # 左边为-1，右边为1
seesaw_flag = False
seesaw_sign = False
saw_count = 0

# 确认"4"按键是否按下，程序是否处于等待状态
def check_stop():
    if stop_button.clicked():
        return True
    return False

def idle_handler(params=None):
    driver.stop()
    global order_num
    global seesaw_flag
    global seesaw_sign
    order_num = 1
    print("IDLE")
    while True:
        if start_button.clicked():
            time.sleep(0.1)
            if start_button.clicked():
                print("program start!")
                seesaw_flag = False
                buzzer.rings()
                time.sleep(0.1)
                return STATE_CRUISE, None
        if seesaw_button.clicked():
            time.sleep(0.1)
            if seesaw_button.clicked():
                print("seesaw program start!")
                seesaw_flag = True
                buzzer.rings()
                time.sleep(0.1)
                return STATE_CRUISE, None

        if cruise_button.clicked():
            time.sleep(0.1)
            if cruise_button.clicked():
                print("cruise start")
                seesaw_flag = True
                while True:
                    if seesaw_sign:
                        state, params = locate_task_handler(8)    # 返回的params=11
                        state, params = do_task_handler(params)
                        seesaw_sign = False
                    else:
                        only_cruise()



# 按照给定速度沿着道路前进给定的时间
def lane_time(speed, my_time):
    start_time = time.time()
    driver.set_speed(speed)
    while True:
        if check_stop():
            return STATE_IDLE, None
        front_image = front_camera.read()
        error = cruiser.infer_cnn(front_image)
        driver.steer(error)
        timeout = time.time()
        if timeout - start_time > my_time:
            driver.stop()
            break

def only_cruise(params=None):
    global order_num
    global saw_count
    # 设置小车巡航速度
    global sign_list
    global cam_dir
    global seesaw_sign
    driver.set_speed(FULL_SPEED)
    # driver.set_speed(SLOW_SPEED)
    driver.set_kx(1)          #巡航设置kx为1， 不在是0.85
    # servo1.servo_control(task[order_num]['angle'], 50)
    time.sleep(0.1)
    count = 0
    angle_count = 0
    no_count = 0
    see_saw = False
    print("Order_num: ", order_num)
    # if order_num in [1]:
    #     # cruiser.set_model(1)
    #     cruiser.__init__(4)
    #     time.sleep(0.2)

    if order_num in [4]:
        # cruiser.set_model(3)
        cruiser.__init__(2)
        time.sleep(0.2)
        driver.set_speed(SLOW_SPEED)

    if order_num in [5]:
        # cruiser.set_model(3)
        cruiser.__init__(3)
        time.sleep(0.2)
        driver.set_speed(FULL_SPEED)

    if order_num in [11]:
        # cruiser.set_model(3)
        cruiser.__init__(4)
        time.sleep(0.2)

        # driver.stop()
        # task_detector.__init__(1)  # 这里切换
        # # lane_time(0, 2)
        # time.sleep(0.2)
    # else:
    #     cruiser.set_model(0)   # 除非你再次改变这个值， 改变作用域
   
    
    if order_num > 11:
        order_num = 11
    # lane_time(30, 1)
    # driver.set_speed(20)
    while True:
        if check_stop():
            idle_handler()
        front_image = front_camera.read()
        angle = cruiser.infer_cnn(front_image)   # 这里进行了修改！！！steer_liu

        if see_saw:   # 检测三次后的
            print("see_saw")
            print(angle)
            angle_count += 1
            if angle_count > 3:
                see_saw = False

            if angle > 0.3:
                if angle > 1:
                    angle = 0.5
                angle = angle * 0.3


            if angle < -0.3:
                if angle < -1:
                    angle = -0.5
                angle = angle * 0.3

            driver.steer(angle)



            # if order_num < 10:
            #     # driver.run(0, 15)
            #     if abs(angle) > 0.01:
            #         driver.run(0, 17)
            #         turn_count += 1
            #         print("turn_count: ", turn_count)
            #     else:
            #         driver.steer(angle)
            # if order_num > 10:
            #     if abs(angle) > 0.01:
            #         driver.run(17, 0)
            #         turn_count += 1
            #         print("turn_count: ", turn_count)
            #     else:
            #         driver.steer(angle)
                # driver.run(15, 0)
            # if angle < -0.01:
            #     driver.run(0, 20)
            # elif angle > 0.01:
            #     driver.run(20, 0)
            # else:
            #     driver.steer(angle)
        else:
            driver.steer(angle)
        # 侦测车道上有无标志图标
        res = sign_detector.detect(front_image)
        if len(res) != 0:
            print(res)
            for sign in res:
                if sign.index == task[8]['sign']:
                    count+=1
                    # sign_list[sign.index] += 1
                    # if sign_list[sign.index] > 10:
                    #     print('*****', res, '*****')
                    if count == 3:
                        see_saw = True

                    if count == 7:
                        print("111")   # order_num不该动
                        saw_count += 1
                        print("the saw_count: ", saw_count)
                        # if saw_count == 1:
                        # cruiser.__init__(3)
                        # time.sleep(0.2)
                        seesaw_sign = True
                        see_saw = False
                        return   # 函数结束
                    #     if count == 8:
                    #         print("222")
                    #         seesaw_sign = True
                    #         return   # 函数结束

                    # if saw_count > 1:
                    #     saw_count = 0
                    #     print("222")
                    #     seesaw_sign = True
                    #     return   # 函数结束


                elif sign.index == task[order_num]['sign']:
                    sign_list[sign.index] += 1
                    # 连续加测到一定次数，认为检测到，进入到任务定位程序
                    if sign_list[sign.index] > 4:
                        print('*****', res, '*****')

                        if order_num == 7:
                            order_num += 2

                        else:
                            order_num += 1
                        return 
                else:
                    pass    
        else:
            no_count += 1
            if no_count > 2:
                count = 0
            sign_list = [0] * 7


# 巡航模式
def cruise_handler(params=None):


    global order_num
    # 设置小车巡航速度
    global sign_list
    global cam_dir
    see_saw = False
    driver.set_kx(1)          #巡航设置kx为1， 不在是0.85
    servo1.servo_control(task[order_num]['angle'], 50)
    time.sleep(0.1)
    print(task[order_num]['angle'])
    if task[order_num]['angle'] > 45:
        cam_dir = -1
    else:
        cam_dir = 1
    print("Order_num: ", order_num)


    # if order_num in [1]:
    #     # cruiser.set_model(1)
    #     cruiser.__init__(1)
    #     time.sleep(0.2)

    # if order_num in [2]:
    #     cruiser.__init__(3)
    #     time.sleep(0.2)
    # #     task_detector.__init__(1)  # 这里切换
    # #     time.sleep(0.2)
    # #     # driver.stop()
    # #     # time.sleep(2)
    # if order_num in [4]:
    #     cruiser.__init__(2)
    #     time.sleep(0.2)
    driver.set_speed(FULL_SPEED)

    if order_num in [4]:
        # cruiser.set_model(3)
        cruiser.__init__(2)
        time.sleep(0.2)
        driver.set_speed(SLOW_SPEED)


    if order_num in [5]:
        # cruiser.set_model(3)
        cruiser.__init__(3)
        time.sleep(0.2)
        driver.set_speed(FULL_SPEED)
        

    if order_num in [11]:
        # cruiser.set_model(3)
        cruiser.__init__(4)
        time.sleep(0.2)

        # driver.stop()
        # task_detector.__init__(1)  # 这里切换
        # # lane_time(0, 2)
        # time.sleep(0.2)


    # lane_time(20, 0.2)
    # driver.set_speed(20)
    
    # driver.set_speed(SLOW_SPEED)

    count = 0
    no_count = 0
    angle_count = 0
    turn_count = 0
    while True:
        if check_stop():
            return STATE_IDLE, None
        front_image = front_camera.read()
        angle = cruiser.infer_cnn(front_image)
        # 这里可以修改为steer/steer_liu两种转向函数
        # driver.steer_liu(angle)
        if see_saw:   # 检测三次后的
            print("see_saw")
            print(angle)
            angle_count += 1
            if angle_count > 3:
                see_saw = False

            if angle > 0.3:
                if angle > 1:
                    angle = 0.5
                angle = angle * 0.3


            if angle < -0.3:
                if angle < -1:
                    angle = -0.5
                angle = angle * 0.3

            driver.steer(angle)
            # if order_num < 10:
            #     # driver.run(0, 15)
            #     if abs(angle) > 0.01:
            #         driver.run(0, 15)
            #         # time.sleep(0.2)
            #         turn_count += 1
            #         print("turn_count: ", turn_count)
            #     else:
            #         driver.steer(angle)
            # if order_num > 10:
            #     if abs(angle) > 0.01:
            #         driver.run(15, 0)
            #         # time.sleep(0.2)
            #         turn_count += 1
            #         print("turn_count: ", turn_count)
            #     else:
            #         driver.steer(angle)
                # driver.run(15, 0)
            # if angle < -0.01:
            #     driver.run(0, 20)
            # elif angle > 0.01:
            #     driver.run(20, 0)
            # else:
            #     driver.steer(angle)
        else:
            driver.steer(angle)


        # driver.steer(angle)
        # 侦测车道上有无标志图标
        res = sign_detector.detect(front_image)
        if len(res) != 0:
            print(res)
            for sign in res:
                if sign.index == task[8]['sign']:
                    count+=1
                    # sign_list[sign.index] += 1
                    # if sign_list[sign.index] > 10:
                    #     print('*****', res, '*****')

                    if count == 3:   # 5-8次断掉一次
                        see_saw = True

                    if count == 7:
                        print("111")
                        # saw_count += 1
                        # print("the saw_count: ", saw_count)
                        see_saw = False
                        return STATE_LOCATE_TASK, 8

                elif sign.index == task[order_num]['sign']:
                    # angle = sign.error_from_center()[0] / 150
                    # driver.steer(angle)
                    # 获取标志识别结果，获得所在列表的索引值

                    sign_list[sign.index] += 1
                    # 连续加测到一定次数，认为检测到，进入到任务定位程序
                    if sign_list[sign.index] > REC_NUM:
                        print('*****', res, '*****')

                        return STATE_LOCATE_TASK, order_num
                else:
                    # count = 0

                    pass

        else:
            no_count += 1
            if no_count > 2:
                count = 0
            sign_list = [0] * 7

def walk_sign(params):
    is_run = True
    while is_run:
        continue_flag = 0
        front_image = front_camera.read()
            # 计算标签偏移，根据标签前进
        res = sign_detector.detect(front_image)
        print(res)
        if len(res) != 0:
            for sign in res:          # index=0, score=0, name="", box=None, shape=None
                print(sign)
                _x, _y = sign.error_from_center()
                print("from center x is{}, y is {}".format(_x, _y))
                if (sign.box[3] - sign.box[1]) < 160:
                    pass
                    # is_run = False
                if _y > 95:
                    is_run = False
                elif _y < 0:
                    continue_flag = 1
                    continue
                if sign.index == task[params]['sign']:
                    angle = _x / 160
                    driver.steer(angle)

        if continue_flag == 1:
            angle = cruiser.infer_cnn(front_image)
            driver.steer(angle)
    driver.stop()


def walk_sign_test(params):
    is_run = True
    start_time = time.time()
    while is_run:
        continue_flag = 0
        front_image = front_camera.read()
            # 计算标签偏移，根据标签前进
        res = sign_detector.detect(front_image)
        print(res)
        now_time = time.time()
        if now_time - start_time > 1.5:
            is_run = False
        if len(res) != 0:
            for sign in res:
                print(sign)
                # _x, _y = sign.error_from_center()
                # print("from center x is{}, y is {}".format(_x, _y))
            
                # if _y > 130:
                #     is_run = False
                # elif _y < 0:
                #     continue_flag = 1
                #     continue
                if sign.index == task[params]['sign']:
                    _x, _y = sign.error_from_center()
                    print("from center x is{}, y is {}".format(_x, _y))
                
                    if _y > 50:
                        is_run = False
                    elif _y < 0:
                        continue_flag = 1
                        continue
                    angle = _x / 160
                    driver.steer(angle)

                else:
                    continue_flag = 1
        else:
            continue_flag = 1
            
            # driver.stop()
                
        if continue_flag == 1:
            angle = cruiser.infer_cnn(front_image)
            driver.steer(angle)
            
    driver.stop()


def rush_seesaw(params):   # 其实是做任务task_fun()函数里面
    driver.set_speed(35)
    print("---->rushseesaw<----".format(params))
    is_rush = True   # 检测不到退出循环
    rush_count = 0
    detect_no_count = 0
    while is_rush:
        # continue_flag = 1  # 0
        front_image = front_camera.read()
        # 计算标签偏移，根据标签前进
        res = sign_detector.detect(front_image)
        if len(res) != 0:
            print(res)
            for sign in res:
                _x, _y = sign.error_from_center()
                print("from seesaw center x is {}, y is {}".format(_x, _y))

                if (sign.box[3] - sign.box[1]) < 160:  # ymax - ymin
                    pass  # 离得特别近
                    # is_rush = False  # 这里可以_y在负正变化

                if _y > 80:   # 由 -50 到 0的范围内调整方向
                    print("***************End!")
                    is_rush = False  # 离得很近  跳出循环
                # elif _y < -50:  # 初始0
                #     continue_flag = 1
                #     continue
                # ############
                # else:  # 0-100   下面的angle不会执行
                #     continue_flag = 0
                ###########
                if sign.index == task[params]['sign']:
                    # print("driver with angle = _x / setted!")
                    angle = _x / 130  # 160
                    print("angle = x / setted : {}!".format(angle))
                    if angle > 0.4:
                        if angle > 1:
                            angle = 1
                        angle = angle * 0.85
                    if angle < -0.4:
                        if angle < -1:
                            angle = -1
                        angle = angle * 0.85

                    driver.steer(angle)  # 转向
                    rush_count += 1
                    if rush_count > 2:
                        is_rush = False


                else:  # 检测到其他的地标信息就冲
                    driver.run(35, 35)


        else:  # 直到检测不到冲  过程中检测不到  也跳出 停车
            # lane_time(30, 1)
            print("detect no !")
            detect_no_count += 1
            if detect_no_count > 2:

                driver.run(30, 30)
                time.sleep(0.5)
                driver.stop()
                is_rush = False
    driver.set_speed(30)

def walk_seesaw():
    global order_num
    turn_count = 0
    buzzer.rings()
    print("---->WWWWW go in walk_road_sign 8 : walk_seesaw!")
    is_run = True
    start_t = time.time() + 2.3  # 不可能2.3s 还未到位
    while is_run:
        front_image = front_camera.read()
        # 计算标签偏移，根据标签前进
        res = sign_detector.detect(front_image)

        if len(res) != 0:
            for sign in res:
                print(" the seesaw box Y : ", sign.box[3] - sign.box[1])
                if sign.index == task[8]['sign']:
                    _x, _y = sign.error_from_center()
                    print("the seesaw _x : {}, _y : {}".format(_x, _y))
                    if _y > -60 and abs(_x) < 50:  # 已经进入范围，且误差是20
                        print("in range!")
                        start_t = time.time()
                    if _y > -50:  # 原来是-55
                        print("Nearly by the seesaw")
                        is_run = False
                    if (sign.box[3] - sign.box[1]) < 10:  # ymax - ymin
                        print("Small!!!")
                        is_run = False
                    angle = _x / 200  # 180
                    #
                    # if angle > 0.4:
                    #     if angle > 1:
                    #         angle = 0.5
                    #     angle = angle * 0.5
                    # if angle < -0.4:
                    #     if angle < -1:
                    #         angle = -0.5
                    #     angle = angle * 0.5

                    if angle > 0.4:
                        if angle > 1:
                            angle = 0.7
                        angle = angle * 0.65
                    if angle < -0.4:
                        if angle < -1:
                            angle = -0.7
                        angle = angle * 0.65

                    driver.steer(angle)

                    # if order_num < 10:
                    #     # driver.run(0, 15)
                    #     if abs(angle) > 0:
                    #         if turn_count < 4:
                    #             driver.run(0, 13)
                    #             time.sleep(0.1)
                    #             turn_count += 1
                    #             print("turn_count: ", turn_count)
                    #         else:
                    #             is_run = False

                    #     else:
                    #         driver.steer(angle)

                    # if order_num > 10:
                    #     if abs(angle) > 0:
                    #         if turn_count < 4:
                    #             driver.run(13, 0)
                    #             time.sleep(0.1)
                    #             turn_count += 1
                    #             print("turn_count: ", turn_count)
                    #         else:
                    #             is_run = False
                    #     else:
                    #         driver.steer(angle)

              
        else:
            # driver.run(30, 30)
            angle = cruiser.infer_cnn(front_image)
            driver.steer(angle)
        if time.time() - start_t > 1:
            is_run = False
            print("time out")
    # driver.run(20, 20)
    # time.sleep(1)
    # # lane_time(0, 0.2)
    driver.stop()
    time.sleep(0.2)

def turn_seesaw():
    turn_count = 0
    global order_num
    if order_num < 10:
        # driver.run(0, 15)
        
        if turn_count < 2:
            driver.run(0, 13)
            time.sleep(0.1)
            turn_count += 1
            print("turn_count: ", turn_count)
        else:
            return


    if order_num > 10:
      
        if turn_count < 2:
            driver.run(13, 0)
            time.sleep(0.1)
            turn_count += 1
            print("turn_count: ", turn_count)
        else:
            return

# 寻找任务目标
def task_lookfor(params = None):
    time_lookfor = 3
    start_time = time.time()
    find_flag = False
    task_list = [0]*12
    while find_flag is not True:
        if check_stop():
            return STATE_IDLE
        side_image = side_camera.read()
        res_side = task_detector.detect(side_image)
        if len(res_side) > 0:
            print(res_side)
            for res in res_side:
                if res.index in task[params]['index']:
                    task_list[res.index] += 1
                    if task_list[res.index] > 1:
                        if params == 11:
                            res.index += 10
                        # 标签到一定位置退出循环
                        _x, _y = res.error_from_point(task_functions[res.index]['position'])
                        if params == 10 and _y > 100:
                            res.index += 10
                        _x = _x * cam_dir
                        print("find task,distance is:", _x)
                        if task_functions[res.index]['location'] == False:
                            # 不需要定位直接做任务
                            print("do not location ")
                            return res.index
                        else:
                            driver.run(10,10)
                        if _x > POSITION_THRESHOLD:
                            driver.run(-10, -10)
                            return res.index
                        elif _x > 0-POSITION_THRESHOLD:
                            return res.index
                else:
                     driver.run(10, 10)
        else:
            front_image = front_camera.read()
            angle = cruiser.infer_cnn(front_image)
            driver.steer(angle)
        current_time = time.time()
        # 长时间未到达位置
        if current_time - start_time > LOCATE_TIME:
            return None

def location_ok(params = None):
    start_time = time.time()
    location_flag = False
    while location_flag is not True:
        if check_stop():
            return STATE_IDLE, None
        side_image = side_camera.read()
        res_side = task_detector.detect(side_image)
        if len(res_side) > 0:
            for res in res_side:
                if res.index in task[params]['index']:
                    if params == 11:
                        res.index += 10
                    # 标签到一定位置退出循环
                    _x, _y = res.error_from_point(task_functions[res.index]['position'])
                    if params == 10 and _y > 100:
                        print("_y:", _y)
                        res.index += 10
                    _x = _x * cam_dir
                    print(_x)
                    if _x < 0-5:
                        print("front")
                        driver.run(10, 10)
                    elif _x > 5:
                        print("back")
                        driver.run(-10, -10)
                    else:
                        driver.stop()
                        print("location ok")
                        return STATE_DO_TASK, res.index
        current_time = time.time()
        # 长时间未到达位置
        if current_time - start_time > 7:
            return STATE_CRUISE, None
        if check_stop():
            return STATE_IDLE, None

def locate_task_handler(params=None):
    global order_num
    global cam_dir
    print("params is", params)
    start_time = time.time()
    this_flag = True
    if params == 8:
        turn_seesaw()

        walk_seesaw()
        # turn_seesaw()
        buzzer.rings()
        # walk_sign(params)
        driver.stop()
        print("ready to do task")
        return STATE_DO_TASK, task[params]['index'][0]
    # walk_sign(params)
    walk_sign_test(params)
    adjust_angle()

    if order_num == 3:
        driver.run(15, 15)
        time.sleep(2.8)
        driver.stop()
        up_jade()
        driver.run(-15, -15)
        time.sleep(2.5)
        driver.stop()


    if task[params]['check'] is not True:
        order_num += 1
        print("ready to do task")
        return STATE_DO_TASK, task[params]['index'][0]

    print("sign location ok!")
    if order_num == 7:
        order_num += 2
    else:
        order_num += 1
    if task[params]['location']:
        driver.set_speed(15)
        print("speed is 15")
    else:
        driver.set_speed(20)
        print("speed is 20")
    driver.steer(0)



    if order_num > 11:
        order_num = 11

    print("looking for task")
    index = task_lookfor(params)
    if index == STATE_IDLE:
        return index, None
    if index is None:
        return STATE_CRUISE , None
    if task_functions[index]['location'] == False:
        return STATE_DO_TASK, index
    print("find task!")
    state, index = location_ok(params)
    if state == STATE_IDLE:
        return STATE_IDLE, None
    if state == STATE_CRUISE:
        return STATE_CRUISE, None
    return STATE_DO_TASK, index

# 做任务
def do_task_handler(params=None):

    print("*******", "now do task:", str(params), task_functions[params], "*******")
    global task_9_flag
    global order_num
    global seesaw_flag
    i = order_num - 1
    print(i)
    # image = side_camera.read()
    # res = sign_detector.detect(image)
    # if

    if params == 1:  # alamutu
        driver.stop()
        raise_flag("alamutu")

    elif params == 2 and i < 7:  # bad_person1_left
        driver.stop()
        shot_target_left()

    elif params == 12 and i >7:  # bad_person1_right
        driver.stop()
        shot_target_right()

    elif params == 3 and i < 7:  # bad_person2_left
        driver.stop()
        shot_target_left()

    elif params == 13 and i > 7:  # bad_person2_right
        driver.stop()
        shot_target_right()

    elif params == 4:  # dunhuang
        driver.stop()
        raise_flag("dunhuang")

    elif params == 5:  # friendship
        driver.run(0, 22)
        time.sleep(1.2)
        driver.run(23, 23)
        time.sleep(1.4)
        driver.run(15, -13)
        time.sleep(1.35)
        driver.stop()

        # time.sleep(1.5)
        friendship()
        time.sleep(0.5)

        driver.run(15, -15)
        time.sleep(1.2)
        driver.run(22, 22)
        time.sleep(1.2)
        driver.run(0, 22)
        time.sleep(1.2)
        driver.stop()

    elif params == 6:  # goodperson1_left
        lane_time(30,1)

    elif params == 16:  # goodperson1_right
        lane_time(30,1)

    elif params == 7:  # goodperson2_left
        lane_time(30,1)

    elif params == 17:  # goodperson2_right
        lane_time(30,1)

    elif params == 8:  # jstdb
        driver.stop()
        raise_flag("jstdb")

    elif params == 9:  # purchase
        driver.stop()
     
        purchase_good()


    elif params == 10:  # trade
        
        driver.run(-13, -13)
        time.sleep(1.5)
        driver.stop()
        trade_good()

        driver.run(13, 13)
        time.sleep(1.5)
        driver.stop()
        trade_good_2()

        driver.run(13, 13)
        time.sleep(1.3)
        driver.stop()

        trade_good_over()
    elif params == 20:
        
        driver.run(-13, -13)
        time.sleep(1.5)
        driver.stop()
        trade_good()

        driver.run(13, 13)
        time.sleep(1.5)
        driver.stop()
        trade_good_1()

        driver.run(13, 13)
        time.sleep(1.2)
        driver.stop()

        trade_good_over()


    elif params == 11:  # seesaw
        if seesaw_flag:
            press_down()
            # buzzer.rings()
            pass

        rush_seesaw(8)
        buzzer.rings()
        # lane_time(30, 1)
        driver.run(35,35)
        time.sleep(0.3)
        driver.stop()
        # time.sleep(0.5)
        # lane_time(30,1)
        # driver.stop()

        # adjust_angle()
    return STATE_CRUISE, None


def adjust_angle():
    while True:
        frame = front_camera.read()
        angle = cruiser.infer_cnn(frame)
        print(angle)
        if angle < -0.01:
            driver.run(0, 15)
        elif angle > 0.01:
            driver.run(15, 0)
        else:
            driver.stop()
            return

state_map = {
    STATE_IDLE: idle_handler,
    STATE_CRUISE: cruise_handler,
    STATE_LOCATE_TASK: locate_task_handler,
    STATE_DO_TASK: do_task_handler,
}


if __name__ == '__main__':
    front_camera.start()
    side_camera.start()
    # 基准速度
    driver.set_speed(30)
    driver.set_kx(0.85)

    # 120，左；-50，右；
    # servo1.servo_control(-45, 50)
    # servo1.servo_control(120, 50)

    # sign_detecte_test()
    # task_detecte_test()
    # lane_test()
    order_num = 1
    time.sleep(0.1)
    current_state = STATE_IDLE
    arg = "cruise"

    task_init()
    # 延时
    time.sleep(0.2)
    startmachine()
    buzzer.rings()


    # while True:
    #     params = None
    #     idle_handler()
    #     order_num = 4
    #     _, params = cruise_handler(order_num)
    #     _, params = locate_task_handler(params)
    #     _, params = do_task_handler(params)
    #     driver.stop()
    # while True:
    #     pass
    #
    order_num = 1
    buzzer.rings()
    try:
        while True:
            current_state, arg = state_map[current_state](arg)
    except ZeroDivisionError as e:
        print('except:', e)
        driver.stop()
        front_camera.stop()
        side_camera.stop()
    finally:
        print('finally...')
        driver.stop()
        front_camera.stop()
        side_camera.stop()

    '''
    front_camera.stop()
    side_camera.stop()
    '''

