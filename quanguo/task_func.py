#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 导入当前目录下的文件夹作为路径
# from re import S
# from sre_parse import State
import set_path
from cart.widgets import *
import time
from config import *
from camera import Camera
from detector.detectors import *
from cart.driver import Driver

driver = Driver()


buzzer = Buzzer()
motor_LR = Motor_rotate(2, 1)   # 左右移动电机
motor_UD = Motor_rotate(2, 2)   # 上下移动电机

# left_camera = Camera(LEFT_CAM, [640, 480])   #左侧摄像头
# right_camera = Camera(RIGHT_CAM, [640, 480])  #右侧摄像头

task_detector = TaskDetector(0)  # 侧边目标物检测

magsens = Magneto_sensor(4)     # 磁感应
# limit_switch = LimitSwitch(4)   # 限位开关
ultrasonic = UltrasonicSensor(2)  #超声波
ultrasonic2 = UltrasonicSensor(3)  #超声波

servo_shot = Servo_pwm(3)       # 击打伺服
servo_grasp = Servo_pwm(2)      # 抓手伺服
light = Light(5)                # 集成灯接D3口
servo_press = Servo_pwm(6)      #跷跷板

servo_raise = Servo(2)

shot_open = 25
shot_close = 140
grasp_open = 80
grasp_close = 20
def task_init():
    print("task init ...")
    #servo_press.servo_control(175, 90)

    servo_press.servo_control(185, 90)
    move_UD(60,1.5)
    # move_LR(60, 0.8)
    # servo_grasp.servo_control(grasp_open, 70)  # 张开抓手
    # time.sleep(1)
    servo_shot.servo_control(shot_close, 80)   # 收回
    servo_grasp.servo_control(grasp_close, 70)  # 关闭抓手
    # servo_press.servo_control(185, 90)
    task_lowest()
    time.sleep(0.5)
    
def task_init_reverse():
    print("task init ...")
    servo_shot.servo_control(shot_close, 80)   # 收回
    servo_grasp.servo_control(grasp_close, 70)  # 关闭抓手
    while limit_switch.clicked() is not True:
        motor_UD.motor_rotate(100)
    time.sleep(0.05)
    motor_UD.motor_rotate(0)
    time.sleep(0.5)
    
# 下降到最低
# def task_lowest():
#     while limit_switch.clicked() is not True:
#         motor_UD.motor_rotate(-100)
#     time.sleep(0.05)
#     motor_UD.motor_rotate(0)
    
def task_lowest():
    count = 0
    while 60 > ultrasonic2.read() > 5 and count < 3 :
        if ultrasonic2.read() == 6:
            count += 1
        # print(ultrasonic2.read())
        motor_UD.motor_rotate(-100)
    print("1:",ultrasonic2.read())
    time.sleep(0.05)
    motor_UD.motor_rotate(0)

def task_down():
    while True:
        kl = magsens.read()
        if kl != None and kl >= 70:
            break
        motor_UD.motor_rotate(-100)
    time.sleep(0.05)
    motor_UD.motor_rotate(0)
    
def task_up():
    print("up ...")
    while True:
        kl = magsens.read()
        if kl != None and kl >= 70:
            break
        motor_UD.motor_rotate(100)
    time.sleep(0.05)
    motor_UD.motor_rotate(0)
    print("up ok!")

def light_work(color, tim_t):
    red = [80, 0, 0]
    green = [0, 80, 0]
    yellow = [80, 80, 0]
    off = [0, 0, 0]
    light_color = [0, 0, 0]
    if color == 'red':
        light_color = red
    elif color == 'green':
        light_color = green
    elif color == 'yellow':
        light_color = yellow
    light.light_control(0, light_color[0], light_color[1], light_color[2])
    time.sleep(tim_t)
    light.light_off()

def move_LR(speed_m, time_m):
    motor_LR.motor_rotate(speed_m)
    time.sleep(time_m)
    motor_LR.motor_rotate(0)
    
def move_UD(speed_m, time_m):
    motor_UD.motor_rotate(speed_m)
    time.sleep(time_m)
    motor_UD.motor_rotate(0)

def press_down():
    # 翘翘板压下去
    up = 175
    down = 80
    servo_press.servo_control(down, 90)
    time.sleep(1)
    servo_press.servo_control(up, 90)
    time.sleep(1)


def up_jade():
    move_LR(-60, 1.2)
    time.sleep(0.1)
    move_UD(100, 6.2)
    time.sleep(0.2)
    move_UD(-100, 2.5)
    move_LR(60, 1.5)
    task_lowest()




def purchase_good():
    """
    2 - 60 - 0.4
    4 - 60 - 0.6
    6 - 60 - 0.8
    8 - 60 - 1
    10 - 60 - 1.2
    """
    # right_camera = cv2.VideoCapture(RIGHT_CAM)
    # right_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # right_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # pu_falg = False
    # count = 0
    # start_time = time.time()
    # while pu_falg is not True:
    #     _, right_image = right_camera.read()
    #     res_side = task_detector.detect(right_image)
    #     if len(res_side) > 0:
    #         for res in res_side:
    #             if res.index == 9:
    #                 _x, _y = res.error_updown([595, 240])
    #                 print(_x)
    #                 if _x < -5:
    #                     print("front")
    #                     driver.run(8, 8)
    #                 elif _x > 5:
    #                     print("back")
    #                     driver.run(-8, -8)
    #                 else:
    #                     driver.stop()
    #                     print("purchase location ok")
    #                     pu_flag = True
    #     else:
    #         if count == 3:
    #             print(count)
    #             driver.stop()
    #             break
    #         print("back")
    #         count += 1
    #         driver.run(-8,-8)
    #     current_time = time.time()
    #     # 长时间未到达位置
    #     if current_time - start_time > 5:
    #         print(0)
    #         driver.stop()
    #         break
    # right_camera.release()


    servo_press.servo_control(175, 90)
    task_up()   # 上升到磁感应
    move_UD(100,0.5)
    move_LR(-60, 0.2)
    servo_grasp.servo_control(grasp_open, 90)   # 打开抓手
    time.sleep(1)
    while True:
        distance = ultrasonic.read()
        if distance is None:
            continue
        else:
            break
    print(distance)
    if distance > 12 or distance == 0:
        distance = 12
    print(distance)
    times = float(distance) * 0.128 -0.374
    move_LR(-60, times)   # 放出
    servo_grasp.servo_control(grasp_close, 70)  # 抓住
    time.sleep(1)
    move_UD(100,1) # 上升一些
    move_LR(60, times+0.5)  # 收回
    task_lowest()   # 购物完成后下降

    # servo_grasp.servo_control(grasp_open, 90)   # 打开抓手



def raise_flag(flagname):

    servo_press.servo_control(175, 90)
    print("raise_flag", flagname,  "start!")
    if flagname == "dunhuang":
        # dunhuang
        servo_raise.servo_control(-40, 60)
        time.sleep(1)
        for i in range(0, 3):
            light_work("green", 0.1)
    elif flagname == "jstdb":
        # jstdb
        servo_raise.servo_control(-120, 60)
        time.sleep(1)
        for i in range(0, 3):
            light_work("green", 0.1)
    elif flagname == "alamutu":
        # almutu
        servo_raise.servo_control(122, 60)
        time.sleep(1)
        for i in range(0, 3):
            light_work("green", 0.1)

    servo_raise.servo_control(42, 60)
    # time.sleep(2)
    print("raise_flag stop!")

def friendship():
    print("friendship start!")
    for i in range(3):
        # print(i)
        light_work("red", 0.2)
        buzzer.rings()
        time.sleep(0.2)



def shot_target_left():
    print("shot_target_left start!")

 
    left_camera = cv2.VideoCapture(LEFT_CAM)
    left_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    left_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    move_LR(-50, 0.3)
    h_location = 360
    flag = False
    count = 0
    start_time = time.time()
    while flag is not True:
        _, left_image = left_camera.read()
        res_side = task_detector.detect(left_image)
   
        if len(res_side) > 0:
            for res in res_side:
                # print(res)
                if res.index == 2 or res.index == 3:
                    print(res.box)
                    flag = True
                    driver.stop()
                    motor_UD.motor_rotate(0)
                    # 96， 145 左
                    # 水平
                    # 417 447 480 左
                    # 高度
                    # 350, 370, 410 zuo
                    if res.box[3] - res.box[1] >= 134:
                        h_location = 420
                        w_location = 480
                    elif 108 <= res.box[3] - res.box[1] < 134:
                        h_location = 379
                        w_location = 447
                    else:
                        h_location = 344
                        w_location = 417
                else:
                    current_time = time.time()
                    if current_time - start_time > 3:
                        return None
                    else:
                        driver.run(8, 8)

        else:

            if ultrasonic2.read() > 8:
                print("3:", ultrasonic2.read())
                motor_UD.motor_rotate(0)
                task_lowest()
                return
            elif count <10:
                print("left count: ", count)
                motor_UD.motor_rotate(100)
                count += 1
            else:
                task_lowest()
                return

    print("0:", h_location)
    start_time = time.time()
    ud_flag = False
    i = 1
    count = 0

    ud_start_time = time.time()
    while ud_flag is not True:
        _,left_image = left_camera.read()
        res_side = task_detector.detect(left_image)
        print(res_side)
        if len(res_side) > 0:
            for res in res_side:
                if res.index == 2 or res.index == 3:
                    i = 1
                    _x, _y = res.error_updown([320,h_location])
                    print("_y:",_y)
                    if _y < -5:
                        if ultrasonic2.read() == 17:
                            print("1:", ultrasonic2.read())
                            motor_UD.motor_rotate(0)
                            ud_flag = True
                        else:
                            current_time = time.time()
                            motor_UD.motor_rotate(100)
                            if current_time - ud_start_time >7.5:
                                motor_UD.motor_rotate(0)
                                ud_flag = True

                            
                    elif _y > 5:
                        if ultrasonic2.read() == 5:
                            print("2:", ultrasonic2.read())
                            motor_UD.motor_rotate(0)
                            ud_flag = True
                        else:
                            motor_UD.motor_rotate(-100)
                    else:
                        print("ud_location_ok !")
                        motor_UD.motor_rotate(0)
                        ud_flag = True
        elif i == 0:
            motor_UD.motor_rotate(0)
            ud_flag = True
        else:
            if count == 5:
                i = 0
            if ultrasonic2.read() == 17:
                print("3:", ultrasonic2.read())
                motor_UD.motor_rotate(0)
                ud_flag = True
            else:
                count += 1
                motor_UD.motor_rotate(100)
        current_time = time.time()
        # 长时间未到达位置
        if current_time - start_time > 10:
            print(2)
            motor_UD.motor_rotate(0)
            break

    lr_flag = False
    j = 1
    count = 0
    start_time = time.time()
    while lr_flag is not True:
        _, left_image = left_camera.read()
        res_side = task_detector.detect(left_image)
        if len(res_side) > 0:
            for res in res_side:
                if res.index == 2 or res.index == 3:
                    # 矮人：远-380
                    j = 1
                    _x, _y = res.error_updown([w_location, 240])
                    print("_x:", _x)
                    if _x < -10:
                        print("back")
                        driver.run(-8, -8)
                    elif _x > 10:
                        print("front")
                        driver.run(8, 8)
                    else:
                        driver.stop()
                        print("lr_location ok")
                        lr_flag = True
        elif j == 0:
            print("j:")
            driver.stop()
            lr_flag = True
        else:
            count+=1
            if count == 10:
                j = 0
        current_time = time.time()
        # 长时间未到达位置
        if current_time - start_time > 8:
            print(1)
            driver.stop()
            break
    left_camera.release()

    servo_shot.servo_control(shot_open, 80)    # 击打
    time.sleep(1)
    servo_shot.servo_control(shot_close, 80)   # 收回
    print("3:",ultrasonic2.read())
    if ultrasonic2.read() > 10:
        move_UD(-100,4)
    move_LR(50,0.8)
    move_UD(100,0.2)
    task_lowest()
    motor_UD.motor_rotate(0)
    print("shot_target stop!")

def shot_target_right():
    print("shot_target_right start!")

    right_camera = cv2.VideoCapture(RIGHT_CAM)
    right_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    right_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    move_LR(-50, 0.4)
    h_location = 360
    flag = False
    count = 0
    start_time = time.time()
    while flag is not True:
        _, right_image = right_camera.read()
        res_side = task_detector.detect(right_image)
        if len(res_side) > 0:
            for res in res_side:
                if res.index == 2 or res.index == 3:
                    print(res.box)
                    flag = True
                    driver.stop()
                    motor_UD.motor_rotate(0)
                    # 96，146 you
                    # 水平
                    # 275 260 240 右
                    # 高度
                    # 360， 409，433
                    if res.box[3] - res.box[1] >= 122:
                        h_location = 433
                        w_location = 279
                    elif 102 <= res.box[3] - res.box[1] < 122:
                        h_location = 409
                        w_location = 266
                        # w_location = 270
                    else:
                        h_location = 360
                        w_location = 250
                        # w_location = 265

                else:
                    current_time = time.time()
                    if current_time - start_time > 3:
                        return None
                    else:
                        driver.run(8, 8)
        else:
            if ultrasonic2.read() > 8:
                print("3:", ultrasonic2.read())
                motor_UD.motor_rotate(0)
                task_lowest()
                return
            elif count <10:
                motor_UD.motor_rotate(100)
                count += 1
            else:
                task_lowest()
                return


    print("0:",h_location)
    start_time = time.time()
    ud_flag = False
    i = 1
    count = 0
    ud_start_time = time.time()
    while ud_flag is not True:
        _,right_image = right_camera.read()
        res_side = task_detector.detect(right_image)
        print(res_side)
        if len(res_side) > 0:
            for res in res_side:
                if res.index == 2 or res.index == 3:
                    _x, _y = res.error_updown([320,h_location])
                    i = 1
                    print("_y:",_y)
                    if _y < -5:
                        if ultrasonic2.read() == 17:
                            print("1:", ultrasonic2.read())
                            motor_UD.motor_rotate(0)
                            ud_flag = True
                            i = 1
                        else:

                            current_time = time.time()
                            motor_UD.motor_rotate(100)
                            if current_time - ud_start_time >7.5:
                                print("ud time out !")
                                motor_UD.motor_rotate(0)
                                ud_flag = True
                            
                    elif _y > 5:
                        if ultrasonic2.read() == 5:
                            print("2:", ultrasonic2.read())
                            motor_UD.motor_rotate(0)
                            ud_flag = True
                        else:
                            motor_UD.motor_rotate(-100)
                    else:
                        print("ud_location_ok !")
                        motor_UD.motor_rotate(0)
                        ud_flag = True
                else:
                    pass

        elif i == 0:
            motor_UD.motor_rotate(0)
            ud_flag = True
        else:
            if count == 5:
                i = 0
            if ultrasonic2.read() == 17:
                print("3:", ultrasonic2.read())
                motor_UD.motor_rotate(0)
                ud_flag = True
            else:
                count += 1
                motor_UD.motor_rotate(100)
        current_time = time.time()
        # 长时间未到达位置
        if current_time - start_time > 10:
            print(2)
            motor_UD.motor_rotate(0)
            break

    lr_flag = False
    start_time = time.time()
    count = 0
    j = 1
    while lr_flag is not True:
        _, right_image = right_camera.read()
        res_side = task_detector.detect(right_image)
        if len(res_side) > 0:
            for res in res_side:
                if res.index == 2 or res.index == 3:
                    # 矮人：远-380
                    j = 1
                    _x, _y = res.error_updown([w_location, 240])
                    print("_x:", _x)
                    if _x < -5:
                        print("front")
                        driver.run(8, 8)
                    elif _x > 5:
                        print("back")
                        driver.run(-8, -8)
                    else:
                        driver.stop()
                        print("lr_location ok")
                        lr_flag = True
        elif j == 0:
            print("j:")
            driver.stop()
            lr_flag = True
        else:
            count+=1
            if count == 10:
                j = 0
        current_time = time.time()
        # 长时间未到达位置
        if current_time - start_time > 8:
            print(1)
            driver.stop()
            break
    right_camera.release()

    driver.stop()
    servo_shot.servo_control(shot_open, 80)    # 击打
    time.sleep(1)
    servo_shot.servo_control(shot_close, 80)   # 收回
    print("4:",ultrasonic2.read())
    if ultrasonic2.read() > 10:
        move_UD(-100, 4)
    move_LR(50, 0.8)
    move_UD(100, 0.2)
    task_lowest()
    print("shot_target stop!")

# def shot_target_right():
#     right_camera = cv2.VideoCapture(RIGHT_CAM)
#     right_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     right_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#     print("shot_target_right start!")
#     move_UD(100, 2)
#     move_LR(-50, 0.5)  # 稍微伸出抓手
#     start_time = time.time()
#     find_flag = False
#     while find_flag is not True:
#         _, right_image = right_camera.read()
#         res_side = task_detector.detect(right_image)
#         print(res_side)
#         if len(res_side) > 0:
#             for res in res_side:
#                 if res.index == 2 or res.index == 3:
#                     _x, _y = res.error_updown([320, 270])
#                     print(_y)
#                     print(res.box)
#                     if _y < -5:
#                         motor_UD.motor_rotate(100)
#                         time.sleep(0.001)
#                     elif _y > 5:
#                         motor_UD.motor_rotate(-100)
#                         time.sleep(0.001)
#                     else:
#                         print("shot_location_ok !")
#                         motor_UD.motor_rotate(0)
#                         find_flag = True
#         current_time = time.time()
#         # 长时间未到达位置
#         if current_time - start_time > 50:
#             print(1)
#             motor_UD.motor_rotate(0)
#             break
#     servo_shot.servo_control(shot_open, 80)  # 击打
#     time.sleep(1)
#     servo_shot.servo_control(shot_close, 80)  # 收回
#     move_UD(-60,2)
#     move_LR(50,0.8)
#     task_lowest()
#     motor_UD.motor_rotate(0)
#     print("shot_target stop!")

def trade_good_1():
    print("trade_good_1 start!")
    # 以货易货1层
    move_UD(100, 0.8)
    while True:
        distance = ultrasonic.read()
        if distance is None:
            continue
        else:
            break
    print(distance)
    if distance > 12 or distance == 0:
        distance = 12
    print(distance)
    times = float(distance) * 0.128 -0.3
    move_LR(-50, times) # 伸出抓手
    servo_grasp.servo_control(grasp_close+10, 70) # 闭合抓手
    time.sleep(1.0)
    move_UD(100, 0.5)
    move_LR(50, 0.8) # 收回抓手


def trade_good_2():
    print("trade_good_2 start!")
    # 以货易货2层
    task_up()
    move_LR(-50, 0.3) # 稍微伸出抓手
    task_up()
    move_UD(100, 4.5)
    while True:
        distance = ultrasonic.read()
        if distance is None:
            continue
        else:
            break
    print(distance)
    if distance > 12 or distance == 0:
        distance = 12
    print(distance)
    times = float(distance) * 0.128 -0.374
    move_LR(-60, times) # 伸出抓手
    servo_grasp.servo_control(grasp_close+10, 70) # 闭合抓手
    time.sleep(1.0)
    move_UD(100, 0.3)
    move_LR(50, 0.5) # 收回抓手


def trade_good_over():
    task_lowest()
    # move_UD(100, 1)
    move_LR(50,1)
    # task_lowest()
    
    
def trade_good():
    # 以货易货即将开始
    move_UD(100, 1)
    move_LR(-50, 1.5) # 稍伸抓手
    servo_grasp.servo_control(grasp_open+25, 90)# 张开抓手
    time.sleep(1.0)
    move_LR(50, 1.8) # 收回抓手




if __name__ == '__main__':
    
    servo_grasp.servo_control(20, 90)
    # friendship()
    # task_init()
    # task_init_reverse()
    # purchase_good()
    time.sleep(0.5)
    # trade_good_1()
    # trade_good_2()
    # shot_target()
    # shot_target()
    # purchase_good()
    # trade_good()
    # time.sleep(3)
    # trade_good_2()
    # trade_good_over()
    # raise_flag(2, 3, "dunhuang")
    # time.sleep(1)
    # raise_flag(2, 3, "alamutu")
    # time.sleep(1)
    # raise_flag(2,3,"jsddb")
    # light = Light(5)
    servo_shot.servo_control(shot_open, 80)  # 击打
    time.sleep(1)
    servo_shot.servo_control(shot_close, 80)  # 收回
    time.sleep(1)

    # while True:
    #     print("kkk")
    #     light_work("green",0.2)
    press_down()
