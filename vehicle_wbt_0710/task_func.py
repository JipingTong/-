from vehicle import ArmBase, ScreenShow, Key4Btn, ServoBus, ServoPwm
import cv2
import time
import numpy as np
import yaml, os
from whalesbot import *


class MyTask:
    def __init__(self):
        # 旋转舵机
        self.servo_rotate = ServoBus(2)
        self.servo_rotate.set_angle(90, 0)

        # 放球舵机
        self.servo_ball = ServoBus(3)
        self.servo_ball.set_angle(50, -38)

        # 机械臂
        self.arm = ArmBase()
        # 初始化机器人
        self.arm.shangbi_angle(90)
        self.arm.xiabi_angle(76)
        time.sleep(0.6)
        self.arm.zhuazi_angle(93)
        time.sleep(0.5)
        self.arm.shangbi_angle(70)
        self.arm.zhongbi_angle(20)
        time.sleep(0.3)
        self.arm.dipan_angle(90)
        time.sleep(1)
        self.arm.zhongbi_angle(0)
        self.arm.xiabi_angle(65)

    def jixiebi_reset(self):
        self.arm.shangbi_angle(90)
        self.arm.xiabi_angle(86)
        time.sleep(1)
        self.arm.zhongbi_angle(90)
        self.arm.dipan_angle(90)
        time.sleep(1)
        self.arm.zhuazi_angle(60)

    def reset_car(self):
        # 初始化机器人
        self.arm.shangbi_angle(90)
        self.arm.zhongbi_angle(30)
        time.sleep(0.5)
        self.arm.xiabi_angle(86)
        time.sleep(0.6)
        self.arm.zhuazi_angle(90)
        time.sleep(0.5)
        self.arm.dipan_angle(90)
        time.sleep(0.5)
        self.arm.xiabi_angle(65)
        self.arm.zhongbi_angle(0)
        self.arm.shangbi_angle(70)

    def save_ball(self):
        pass
        # self.servo_ball.set_angle(100, -50)
        # time.sleep(0.3)
        self.servo_ball.set_angle(100, -30)
        # time.sleep(0.6)

    def pick_up_block1_1(self, arm_set=False):
        # 抓手打开指定角度稍微大角度, 到达指定位置上方
        self.arm.xiabi_angle(86)
        self.arm.shangbi_angle(120)
        time.sleep(0.3)
        self.arm.dipan_angle(150)
        time.sleep(0.3)
        self.arm.shangbi_angle(160)
        time.sleep(0.3)
        self.arm.zhuazi_angle(50)  # 爪子张开
        time.sleep(0.3)
        self.arm.xiabi_angle(127)  # 爪子下降
        time.sleep(0.5)

    def pick_up_block1_2(self, arm_set=False):
        self.arm.zhuazi_angle(90)  # 抓住方块
        time.sleep(0.5)
        self.arm.xiabi_angle(86)  # 上升
        time.sleep(0.3)

    def put_down_self_block(self):
        self.arm.dipan_angle(90)
        self.arm.shangbi_angle(100)
        time.sleep(0.4)
        self.arm.xiabi_angle(75)
        self.arm.shangbi_angle(60)
        time.sleep(0.5)
        self.arm.zhuazi_angle(65)  # 放下方块
        time.sleep(0.5)
        self.arm.shangbi_angle(70)

    def pick_up_block2_1(self, arm_set=False):
        # 抓手打开指定角度稍微大角度, 到达指定位置上方
        self.arm.xiabi_angle(86)
        self.arm.shangbi_angle(120)
        time.sleep(0.3)
        self.arm.dipan_angle(150)
        time.sleep(0.3)
        self.arm.shangbi_angle(160)
        time.sleep(0.3)
        self.arm.zhuazi_angle(50)  # 爪子张开
        time.sleep(0.3)
        self.arm.xiabi_angle(127)  # 爪子下降
        time.sleep(0.5)

    def pick_up_block2_2(self, arm_set=False):
        self.arm.zhuazi_angle(90)  # 抓住方块
        time.sleep(0.5)
        self.arm.xiabi_angle(95)  # 上升


    def put_down_block1_1(self):
        self.arm.dipan_angle(154)
        time.sleep(0.5)
        self.arm.xiabi_angle(140)  # 爪子下降
        time.sleep(1)
        self.arm.shangbi_angle(150)
        time.sleep(0.4)

    def pick_up_block_self(self):
        self.arm.xiabi_angle(86)
        time.sleep(0.4)
        self.arm.shangbi_angle(40)
        self.arm.dipan_angle(86)
        self.arm.shangbi_angle(50)
        time.sleep(0.5)
        self.arm.xiabi_angle(73)
        time.sleep(0.4)
        self.arm.zhongbi_angle(20)
        self.arm.shangbi_angle(45)
        time.sleep(0.4)
        self.arm.xiabi_angle(94)
        time.sleep(0.4)

    # def put_down_block1(self):
    #     self.arm.dipan_angle(154)
    #     time.sleep(0.5)
    #     self.arm.xiabi_angle(140)  # 爪子下降
    #     time.sleep(1.5)
    #     self.arm.shangbi_angle(160)
    #     time.sleep(0.5)

    def put_down_block1_2(self):
        self.arm.zhuazi_angle(45)  # 爪子张开
        time.sleep(0.5)
        self.arm.xiabi_angle(86)  #

    def put_down_block2_1(self):
        self.arm.zhuazi_angle(90)
        time.sleep(1)
        self.arm.shangbi_angle(45)
        self.arm.xiabi_angle(83)
        time.sleep(0.5)
        self.arm.shangbi_angle(100)
        self.arm.dipan_angle(154)
        time.sleep(0.5)
        self.arm.xiabi_angle(86)  # 爪子下降
        self.arm.shangbi_angle(150)
        time.sleep(0.5)

    def put_down_block2_2(self):
        self.arm.zhongbi_angle(0)
        self.arm.xiabi_angle(140)  # 爪子下降
        time.sleep(1)
        self.arm.shangbi_angle(155)
        time.sleep(0.4)


    def weitiao(self):
        self.arm.xiabi_angle(142)
        self.arm.shangbi_angle(148)
        time.sleep(1)

    def prepare_pick_up(self):
        self.arm.xiabi_angle(86)
        self.arm.shangbi_angle(120)
        time.sleep(0.5)
        self.arm.dipan_angle(23)
        time.sleep(0.5)
        self.arm.xiabi_angle(35)
        self.arm.zhongbi_angle(0)
        self.arm.shangbi_angle(50)
        self.arm.zhuazi_angle(75)
        time.sleep(0.5)

    def prepare_servo_ball(self):
        self.servo_ball.set_angle(50, -55)  # -10

    def pick_up_ball(self, arm_set=False):
        tar = [4, 0, 'blue_ball', 0.6, -0.07, 0.15, 0.37, 0.42]  # -0.05, 0.15, 0.37, 0.42
        if arm_set:
            self.servo_ball.set_rotate(0)
            return tar
        self.arm.shangbi_angle(50)
        self.arm.zhongbi_angle(10)
        time.sleep(0.5)
        self.arm.shangbi_angle(107)
        self.arm.xiabi_angle(95)
        time.sleep(1)

    def put_down_self_ball(self):
        self.arm.zhuazi_angle(93)
        time.sleep(0.5)
        self.arm.zhongbi_angle(20)
        time.sleep(0.5)
        self.arm.xiabi_angle(86)
        time.sleep(0.5)
        self.arm.dipan_angle(80)
        time.sleep(0.4)
        self.arm.xiabi_angle(80)
        time.sleep(0.5)
        self.arm.shangbi_angle(70)
        self.arm.zhongbi_angle(5)
        time.sleep(1.0)
        self.arm.zhuazi_angle(65)  # 放下方块
        time.sleep(1)
        self.arm.shangbi_angle(70)
        time.sleep(0.5)
        self.arm.shangbi_angle(80)
        self.arm.dipan_angle(90)
        self.arm.xiabi_angle(70)
        # 回到识别角度
        self.arm.xiabi_angle(86)
        self.arm.shangbi_angle(120)
        time.sleep(0.5)
        self.arm.dipan_angle(23)
        time.sleep(0.5)
        self.arm.xiabi_angle(35)
        self.arm.zhongbi_angle(0)
        self.arm.shangbi_angle(50)
        self.arm.zhuazi_angle(70)

    def elevation_pole(self, arm_set=False):
        self.servo_rotate.set_rotate(100)
        time.sleep(6.8)
        self.servo_rotate.set_rotate(0)

    def pick_high_ball(self):
        self.arm.shangbi_angle(90)
        self.arm.zhongbi_angle(90)
        self.arm.xiabi_angle(86)
        time.sleep(3)
        self.arm.dipan_angle(28)
        self.arm.zhuazi_angle(50)
        time.sleep(1)
        self.arm.shangbi_angle(74)
        time.sleep(0.5)
        self.arm.xiabi_angle(99)
        time.sleep(2)
        self.arm.zhuazi_angle(93)
        time.sleep(1)
        self.arm.xiabi_angle(86)
        time.sleep(0.5)
        self.arm.dipan_angle(90)
        time.sleep(0.5)
        self.arm.zhongbi_angle(30)
        self.arm.shangbi_angle(60)
        time.sleep(1.5)

    def put_down_ball(self):
        self.servo_ball.set_angle(50, -15)
        time.sleep(4)
        self.arm.xiabi_angle(65)
        self.arm.zhongbi_angle(20)
        self.arm.shangbi_angle(50)
        time.sleep(0.5)
        self.servo_ball.set_angle(50, -50)
        self.arm.zhuazi_angle(60)
        time.sleep(0.5)
        self.arm.zhuazi_angle(90)

    def turn_left(self):
        self.arm.xiabi_angle(86)
        self.arm.shangbi_angle(120)
        time.sleep(0.5)
        self.arm.dipan_angle(23)
        time.sleep(0.5)
        self.arm.xiabi_angle(50)
        self.arm.zhongbi_angle(0)
        self.arm.shangbi_angle(50)
        self.arm.zhuazi_angle(69)
        time.sleep(0.5)

    def turn_right(self):
        self.arm.xiabi_angle(86)
        self.arm.shangbi_angle(120)
        time.sleep(0.5)
        self.arm.dipan_angle(153)
        time.sleep(0.5)
        self.arm.xiabi_angle(50)
        self.arm.zhongbi_angle(0)
        self.arm.shangbi_angle(50)
        self.arm.zhuazi_angle(69)
        time.sleep(0.5)

    # 抓圆柱，选则大小
    def pick_up_cylinder1(self, radius, arm_set=False):
        tar_list = [[1, 0, "cylinder1", 0.6, -0.02, -0.22, 0.67, 0.67],
                    [2, 0, "cylinder2", 0.6, -0.02, -0.22, 0.37, 0.60],
                    [3, 0, "cylinder3", 0.6, -0.02, -0.23, 0.3, 0.53]]
        pt_tar = tar_list[radius - 1]
        if arm_set:
            return pt_tar
        self.arm.zhongbi_angle(8)
        self.arm.xiabi_angle(95)
        self.arm.shangbi_angle(90)
        time.sleep(1)
        self.arm.zhuazi_angle(82)
        time.sleep(0.4)
        self.arm.xiabi_angle(80)
        self.arm.shangbi_angle(92)  # 87
        time.sleep(0.4)

    def put_down_cylinder1(self, radius):
        self.arm.zhongbi_angle(8)
        self.arm.xiabi_angle(100)
        self.arm.shangbi_angle(90)
        time.sleep(1)
        self.arm.zhuazi_angle(70)
        time.sleep(0.4)
        self.arm.xiabi_angle(50)
        time.sleep(0.2)
        self.arm.shangbi_angle(50)
        self.arm.zhongbi_angle(8)
        time.sleep(0.5)

    def pick_up_cylinder2(self, radius, arm_set=False):
        tar_list = [[1, 0, "cylinder1", 0, -0.02, -0.22, 0.69, 0.69], [2, 0, "cylinder2", 0, -0.02, -0.22, 0.50, 0.60],
                    [3, 0, "cylinder3", 0, -0.02, -0.23, 0.3, 0.53]]
        pt_tar = tar_list[radius - 1]
        if arm_set:
            return pt_tar
        self.arm.zhongbi_angle(8)
        self.arm.xiabi_angle(95)
        self.arm.shangbi_angle(90)
        time.sleep(1)
        self.arm.zhuazi_angle(93)
        time.sleep(0.4)
        self.arm.xiabi_angle(70)
        self.arm.shangbi_angle(89)
        time.sleep(0.4)

    def put_down_cylinder2(self, radius):
        self.arm.zhongbi_angle(8)
        self.arm.xiabi_angle(90)
        self.arm.shangbi_angle(85)
        time.sleep(1)
        self.arm.zhuazi_angle(70)
        self.arm.xiabi_angle(70)
        time.sleep(0.5)
        self.arm.shangbi_angle(100)
        self.arm.zhongbi_angle(15)
        time.sleep(0.5)
        # 回到初始识别位置
        self.arm.xiabi_angle(86)
        self.arm.shangbi_angle(120)
        time.sleep(0.5)
        self.arm.dipan_angle(153)
        time.sleep(0.5)
        self.arm.xiabi_angle(50)
        self.arm.zhongbi_angle(0)
        self.arm.shangbi_angle(50)
        self.arm.zhuazi_angle(69)
        time.sleep(0.5)

    def put_down_cylinder2_2(self, radius):
        self.arm.zhongbi_angle(8)
        self.arm.xiabi_angle(90)
        self.arm.shangbi_angle(85)
        time.sleep(1)
        self.arm.zhuazi_angle(70)
        self.arm.xiabi_angle(70)
        time.sleep(0.5)
        self.arm.shangbi_angle(100)
        self.arm.zhongbi_angle(15)
        time.sleep(0.5)
        # 回到初始识别位置
        self.arm.xiabi_angle(86)
        self.arm.shangbi_angle(120)
        time.sleep(0.5)
        self.arm.dipan_angle(23)
        time.sleep(0.5)
        self.arm.xiabi_angle(50)
        self.arm.zhongbi_angle(0)
        self.arm.shangbi_angle(50)
        self.arm.zhuazi_angle(69)
        time.sleep(0.5)

    def pick_up_cylinder3(self, radius, arm_set=False):
        tar_list = [[1, 0, "cylinder1", 0, -0.02, -0.22, 0.69, 0.69], [2, 0, "cylinder2", 0, -0.02, -0.22, 0.50, 0.60],
                    [3, 0, "cylinder3", 0, -0.02, -0.23, 0.4, 0.53]]
        pt_tar = tar_list[radius - 1]
        if arm_set:
            return pt_tar
        self.arm.zhongbi_angle(8)
        self.arm.xiabi_angle(95)
        self.arm.shangbi_angle(90)
        time.sleep(1)
        self.arm.zhuazi_angle(95)
        time.sleep(0.4)
        self.arm.xiabi_angle(63)
        self.arm.zhongbi_angle(5)
        self.arm.shangbi_angle(80)
        time.sleep(0.4)

    def put_down_cylinder3(self, radius):
        self.arm.zhuazi_angle(70)
        time.sleep(0.5)
        self.arm.xiabi_angle(50)
        time.sleep(0.5)
        self.arm.zhongbi_angle(30)

    def task_test(self):
        self.servo_high.set(50, 50)

    def prepare_ocr(self):
        self.arm.xiabi_angle(86)
        self.arm.shangbi_angle(120)
        time.sleep(0.5)
        self.arm.dipan_angle(152)
        time.sleep(0.5)
        self.arm.xiabi_angle(30)
        self.arm.zhongbi_angle(0)
        self.arm.shangbi_angle(40)
        self.arm.zhuazi_angle(60)

    def punish_crimall(self, arm_set=False):
        tar = [0, 1, 'pedestrian', 0.5, -0.02, 0.4, 0.19, 0.68]
        self.arm.xiabi_angle(30)
        self.arm.zhongbi_angle(0)
        self.arm.shangbi_angle(40)
        self.arm.zhuazi_angle(60)
        if arm_set:
            return tar
        self.arm.zhuazi_angle(94)
        time.sleep(0.5)
        self.arm.xiabi_angle(97)
        self.arm.shangbi_angle(140)


    def punish_crimall1(self):
        self.arm.zhuazi_angle(94)
        time.sleep(0.5)
        self.arm.xiabi_angle(97)
        self.arm.shangbi_angle(140)

    def ocr_arm_ready(self, side=-1):
        self.arm.switch_side(side)
        tar_height = 0.04
        tar_horiz = -0.12
        self.arm.set(tar_horiz, tar_height)


def task_reset():
    task = MyTask()
    task.reset()


def task():
    task = MyTask()


def block_reset():
    task = MyTask()
    task.reset()
    task.pick_up_block()
    task.put_down_self_block()
    # task.pick_up_block_self()
    # task.put_down_block()


def ball_test():
    task = MyTask()

    # 抓三个球
    for i in range(3):
        task.pick_up_ball()
        task.put_down_self_ball()

    task.put_down_ball()


def cylinder_test():
    task = MyTask()
    i = 0
    tar = task.pick_up_cylinder(i + 1, arm_set=True)
    time.sleep(0.8)
    task.pick_up_cylinder(i + 1)
    time.sleep(0.5)
    task.put_down_cylinder(i + 1)
    time.sleep(0.5)
    # for i in range(3):
    #     tar = task.pick_up_cylinder(i+1, arm_set=True)
    #     time.sleep(0.8)
    #     task.pick_up_cylinder(i+1)
    #     time.sleep(0.5)
    #     task.put_down_cylinder(i+1)
    #     time.sleep(0.5)


def highball_test():
    task = MyTask()
    task.pick_high_ball()


def punish_crimall_test():
    task = MyTask()
    task.punish_crimall()


if __name__ == "__main__":
    import argparse

    task = MyTask()
    task.prepare_servo_ball()
    #    args = argparse.ArgumentParser()
    print("end")
#    args.add_argument('--op', type=str, default="reset")
#    args = args.parse_args()
#    print(args)
#    if args.op == "reset":
#        task_reset()
#    if args.op == "stop":
#        punish_crimall_test("infer_back_end.py")
#    print(12121212)
#    task_reset()

