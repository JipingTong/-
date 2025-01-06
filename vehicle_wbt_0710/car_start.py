#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import threading
import os
import numpy as np
from task_func import MyTask
from log_info import logger
from car_wrap import MyCar
from tools import CountRecord
import math

if __name__ == "__main__":
    # kill_other_python()
    my_car = MyCar()
    my_car.STOP_PARAM = False



    def grap_block_func():
        my_car.lane_sensor(0.3, value_h=0.4, sides=-1, stop=False)  # 移动到第一个
        my_car.lane_dis_offset(0.4, 0.028)
        my_car.set_pos_offset([0.00, 0.055, 0], 0.5)  # 向左移动一段距离
        my_car.task.pick_up_block1_1(arm_set=True)
        my_car.set_pos_offset([0.00, -0.035, 0], 0.4)
        my_car.task.pick_up_block1_2(arm_set=True)
        my_car.task.put_down_self_block()
        my_car.set_pos_offset([0.00, -0.02, 0], 0.4)  # 向右移动一段距离
        my_car.lane_dis_offset(0.3, 0.2, stop=False)
        my_car.lane_sensor(0.3, value_h=0.4, sides=-1, stop=False)  # 移动到第二个
        my_car.lane_dis_offset(0.3, 0.03)
        my_car.set_pos_offset([0.00, 0.06, 0], 0.5)
        my_car.task.pick_up_block2_1(arm_set=True)
        my_car.set_pos_offset([0.00, -0.04, 0], 0.4)
        my_car.task.pick_up_block2_2(arm_set=True)
        my_car.set_pos_offset([0.00, -0.03, 0], 0.4)


    def release_block_func():
        my_car.lane_dis_offset(0.3, 3.2, stop=False)
        my_car.lane_sensor(0.2, value_h=0.4, sides=-1, stop=True)
        my_car.set_pos_offset([0.00, 0.055, 0], 0.4)  # 向左移动一段距离
        my_car.task.put_down_block1_1()
        my_car.set_pos_offset([0.00, -0.025, 0], 0.15)  # 向右移动一段距离
        my_car.task.put_down_block1_2()
        my_car.set_pos_offset([0.00, -0.04, 0], 0.4)  # 向右移动一段距离
        my_car.lane_dis_offset(0.3, 0.15, stop=True)  # 到达第二个放方块点
        my_car.task.pick_up_block_self()
        my_car.set_pos_offset([0.00, 0.058, 0], 0.4)  # 向左移动一段距离
        my_car.task.put_down_block2_1()
        my_car.task.put_down_block2_2()
        my_car.task.put_down_block1_2()
        my_car.task.reset_car()
        # my_car.lane_dis_offset(0.3, 1, stop=True)


    def get_ball_func():
        pt = my_car.task.prepare_pick_up()
        my_car.lane_sensor(0.2, value_h=0.3, sides=1, stop=True)
        start_dis = my_car.get_dis_traveled()
        my_car.task.prepare_servo_ball()
        for i in range(3):
            # 根据给定目标和位置、方向定位调整车子的位置
            pt = my_car.task.pick_up_ball(arm_set=True)
            res = my_car.lane_det_location(0.1, pt, side=1)
            if res:
                my_car.task.pick_up_ball()
                my_car.task.put_down_self_ball()
            else:
                # 距离超过0.4m就跳出
                if my_car.get_dis_traveled() - start_dis < 0.40:
                    logger.info("dis out {}".format(i))
                else:
                    logger.info("can not find ball")
                    break
                continue


    def elevation_pole_func():
        my_car.lane_dis_offset(0.3, 0.4)
        my_car.lane_sensor(0.2, value_h=0.3, sides=1, stop=True)
        my_car.lane_dis_offset(0.3, 0.1)  # 0.07
        my_car.set_pos_offset([0.00, 0.04, 0], 0.5)  # 向左移动一段距离    0.02
        my_car.task.elevation_pole()
        my_car.set_pos_offset([0.00, -0.09, 0], 0.5)  # 向右移动一段距离      -0.07
        my_car.task.reset_car()


    def get_high_ball_func():
        my_car.lane_sensor(0.4, value_h=0.3, sides=1, stop=True)
        my_car.set_pos_offset([0.00, 0.035, 0], 0.5)  # 向左移动一段距离
        my_car.task.pick_high_ball()
        my_car.set_pos_offset([0.00, -0.05, 0], 0.5)  # 向右移动一段距离


    def pull_ball_func():
        my_car.lane_dis_offset(0.3, 1)
        my_car.lane_sensor(0.4, value_h=0.3, sides=1)
        # 调整位置准备放置球
        my_car.lane_dis_offset(0.2, 0.13)
        my_car.set_pos_offset([0, 0.02, 0], 0.7)  # 向左移动
        my_car.task.put_down_ball()
        my_car.set_pos_offset([0, -0.05, 0], 0.7)  # 向右移动


    def hanoi_tower_func():
        my_car.lane_dis_offset(0.3, 1)
        my_car.set_pos_offset([0, -0.05, 0], 0.5)  # 向右移动
        det_side = my_car.lane_det_dis2pt(0.2, 1.5)
        side = my_car.get_card_side()
        if side == 1:
            my_car.task.turn_right()  # 面朝右边，走左边
            my_car.set_pos_offset([0, 0, math.pi / 4 * 1.5 * side], 1)
            # 第一个要抓取的圆柱
            cylinder_id = 1
            # 获取要抓取的圆柱信息
            pt = my_car.task.pick_up_cylinder1(cylinder_id, True)
            # 走一段距离
            my_car.lane_dis_offset(0.3, 0.55)
            # 第二次感应到侧面位置
            my_car.lane_sensor(0.1, value_l=0.2, sides=side * -1, stop=True)
            my_car.set_pos_offset([0, 0, -math.pi / 8 * 1.4], 1)
            # 记录此时的位置
            pos_start = np.array(my_car.get_odom())
            logger.info("start pos:{}".format(pos_start))
            # # # 根据给定信息定位目标
            my_car.lane_det_location(0.1, pt, side=side * -1)
            my_car.set_pos_offset([-0.02, 0.01, 0], 0.5)  # 向后移动一段距离
            # 抓取圆柱
            my_car.task.pick_up_cylinder1(cylinder_id)
            # # 计算走到记录位置的距离
            run_dis = my_car.calculation_dis(pos_start, np.array(my_car.get_odom()))
            # 后移刚才计算的距离，稍微多走一点儿
            my_car.set_pos_offset([0 - (run_dis - 0.013), 0, 0])
            tar_pos = my_car.get_odom()
            # 记录位置
            logger.info("tar_pos:{}".format(tar_pos))
            my_car.set_pos_offset([0.00, 0.025, 0], 0.5)  # 向左移动一段距离
            my_car.task.put_down_cylinder1(cylinder_id)
            # my_car.set_pos_offset([0.00, 0.02, 0], 0.5)  # 向左移动一段距离

            # 抓取2号圆柱
            cylinder_id = 2
            pt = my_car.task.pick_up_cylinder2(cylinder_id, True)
            my_car.lane_sensor(0.1, value_l=0.3, sides=side * -1, stop=True)
            # my_car.set_pos_offset([0, 0, -math.pi / 8 * 1.5], 1)
            my_car.lane_det_location(0.1, pt, dis_out=0.5, side=-1 * side)
            my_car.set_pos_offset([-0.02, 0.03, 0], 0.5)  # 向后移动一段距离
            my_car.task.pick_up_cylinder2(cylinder_id)
            my_car.set_pos(tar_pos)
            my_car.set_pos_offset([0.01, 0.00, 0], 0.5)  # 向前移动一段距离
            my_car.set_pos_offset([0.00, 0.05, 0], 0.5)  # 向左移动一段距离
            my_car.task.put_down_cylinder2(cylinder_id)

            # 抓取3号圆柱
            cylinder_id = 3
            pt = my_car.task.pick_up_cylinder3(cylinder_id, True)
            my_car.lane_sensor(0.1, value_l=0.3, sides=side * -1, stop=True)
            my_car.set_pos_offset([0, 0, -math.pi / 8 * 1.2], 1)
            my_car.lane_det_location(0.1, pt, dis_out=0.5, side=-1 * side)
            my_car.set_pos_offset([0.00, 0.02, 0], 0.5)  # 向左移动一段距离
            my_car.task.pick_up_cylinder3(cylinder_id)
            my_car.set_pos(tar_pos)
            my_car.set_pos_offset([0.01, 0.00, 0], 0.5)  # 向前移动一段距离
            my_car.set_pos_offset([0.00, 0.02, 0], 0.5)  # 向左移动一段距离
            my_car.task.put_down_cylinder3(cylinder_id)
            my_car.set_pos_offset([0.00, 0.03, 0], 0.5)  # 向左移动一段距离
        else:
            my_car.task.turn_left()  # 面朝左边，走右边
            my_car.set_pos_offset([0, 0, math.pi / 4 * 1.5 * side], 1)
            my_car.set_pos_offset([0.00, -0.06, 0], 0.5)  # 向右移动一段距离
            # 第一个要抓取的圆柱
            cylinder_id = 1
            # 获取要抓取的圆柱信息
            pt = my_car.task.pick_up_cylinder1(cylinder_id, True)
            # 走一段距离
            my_car.set_pos_offset([0.25, 0.0, 0], 1)  # 向前移动一段距离
            my_car.lane_dis_offset(0.2, 0.25)
            my_car.set_pos_offset([0.00, -0.05, 0], 0.5)  # 向右移动一段距离
            # 第二次感应到侧面位置
            my_car.lane_sensor(0.1, value_l=0.2, sides=side * -1, stop=True)
            my_car.set_pos_offset([0, 0, math.pi / 8 * 1.2], 1)
            my_car.set_pos_offset([-0.015, 0.00, 0], 0.5)  # 向后移动一段距离
            my_car.set_pos_offset([0.00, -0.05, 0], 0.5)  # 向右移动一段距离

            # 记录此时的位置
            pos_start = np.array(my_car.get_odom())
            logger.info("start pos:{}".format(pos_start))
            # # # 根据给定信息定位目标
            my_car.lane_det_location(0.1, pt, side=side * -1)
            # 抓取圆柱
            my_car.task.pick_up_cylinder1(cylinder_id)
            # # 计算走到记录位置的距离
            run_dis = my_car.calculation_dis(pos_start, np.array(my_car.get_odom()))
            # 后移刚才计算的距离，稍微多走一点儿
            my_car.set_pos_offset([0 - (run_dis + 0.0), 0, 0])
            tar_pos = my_car.get_odom()
            # 记录位置
            logger.info("tar_pos:{}".format(tar_pos))
            my_car.set_pos_offset([0.00, 0.0, 0], 0.5)  # 向左移动一段距离
            my_car.task.put_down_cylinder1(cylinder_id)
            my_car.set_pos_offset([0.00, -0.02, 0], 0.5)  # 向右移动一段距离
            # 抓取2号圆柱
            cylinder_id = 2
            pt = my_car.task.pick_up_cylinder2(cylinder_id, True)
            my_car.lane_sensor(0.1, value_l=0.3, sides=side * -1, stop=True)
            my_car.set_pos_offset([0, 0, math.pi / 8 * 1.2], 1)
            my_car.lane_det_location(0.1, pt, dis_out=0.5, side=-1 * side)
            my_car.set_pos_offset([0.015, 0.00, 0], 0.5)  # 向前移动一段距离
            my_car.set_pos_offset([0.00, -0.04, 0], 0.5)  # 向右移动一段距离
            my_car.task.pick_up_cylinder2(cylinder_id)
            my_car.set_pos(tar_pos)
            my_car.set_pos_offset([0.01, 0.00, 0], 0.5)  # 向前移动一段距离
            my_car.set_pos_offset([0.00, -0.03, 0], 0.5)  # 向左移动一段距离
            my_car.task.put_down_cylinder2_2(cylinder_id)

            # 抓取3号圆柱
            cylinder_id = 3
            pt = my_car.task.pick_up_cylinder3(cylinder_id, True)
            my_car.lane_sensor(0.1, value_l=0.3, sides=side * -1, stop=True)
            # my_car.set_pos_offset([0, 0, -math.pi / 8 * 1.0], 1)
            my_car.lane_det_location(0.1, pt, dis_out=0.5, side=-1 * side)
            # my_car.set_pos_offset([0.00, -0.05, 0], 0.5)  # 向右移动一段距离
            my_car.task.pick_up_cylinder3(cylinder_id)
            my_car.set_pos(tar_pos)
            my_car.set_pos_offset([0.01, 0.00, 0], 0.5)  # 向前移动一段距离
            my_car.set_pos_offset([0.00, 0.04, 0], 0.5)  # 向左移动一段距离
            my_car.task.put_down_cylinder3(cylinder_id)
            my_car.set_pos_offset([0.00, -0.05, 0], 0.5)  # 向右移动一段距离

        my_car.task.reset_car()


    def camp_fun():
        my_car.task.prepare_ocr()
        my_car.lane_sensor(0.2, value_h=0.4, sides=-1, stop=True)
        my_car.set_pos_offset([0, 0, math.pi / 8 * 1.5], 1)
        my_car.set_pos_offset([-0.11, 0.00, 0], 0.75)  # 向后移动一段距离
        my_car.set_pos_offset([0.00, -0.04, 0], 0.5)  # 向右移动一段距离
        time.sleep(2)
        text = my_car.get_ocr()
        logger.info("text:{}".format(text))
        actions_map = my_car.yiyan_get_actions(text)
        print(my_car.yiyan_get_actions(text))
        # 前移到营地左侧
        my_car.set_pos_offset([0.00, 0.02, 0], 0.5)  # 向左移动一段距离
        my_car.lane_dis_offset(0.3, 0.53)
        pos_start = np.array(my_car.get_odom())
        # 离开道路到修整营地
        my_car.set_pos_offset([0, -0.45, 0], 3)
        # 做任务
        my_car.do_action_list(actions_map)
        time.sleep(1)
        # 回到原来位置
        my_car.set_pos(pos_start)


    def find_criminal():
        my_car.task.prepare_ocr()
        my_car.lane_sensor(0.3, value_h=0.4, dis_offset=0.02, sides=-1, stop=True)
        my_car.set_pos_offset([-0.04, 0.00, 0], 0.5)  # 向后移动一段距离
        my_car.set_pos_offset([0.00, -0.04, 0], 0.25)  # 向右移动一段距离
        time.sleep(2)
        text = my_car.get_ocr()
        my_car.set_pos_offset([0.00, 0.04, 0], 0.25)  # 向左移动一段距离
        if text is not None:
            logger.info("text:{}".format(text))
            criminal_attr = my_car.hum_analysis.get_res_json(text)
            print(criminal_attr)
            # 调整机械手到识别的位置
            pt_tar = my_car.task.punish_crimall(arm_set=True)
            # 巡航到识别位置
            my_car.lane_sensor(0.1, value_h=0.4, sides=-1, stop=True)
            for i in range(4):
                my_car.lane_det_location(0.1, pt_tar, det="mot", side=-1)
                attr_hum = my_car.get_hum_attr(pt_tar)
                res = my_car.compare_humattr(criminal_attr, attr_hum)
                if res:
                    logger.info("找到罪犯")
                    my_car.set_pos_offset([0.00, 0.02, 0], 0.25)  # 向左移动一段距离
                    my_car.task.punish_crimall()
                    break
                else:
                    if i != 4:
                        # 前往下一个位置
                        my_car.set_pos_offset([0.06, 0, 0],1)
            else:
                logger.info("没有找到罪犯")
        else:
            # 未检测到字，或者检测到的字不稳定，继续往下执行
            my_car.lane_dis_offset(0.3, 0.4)

        # my_car.lane_dis_offset(0.3, 3.4)
        # 调整机械手到识别的位置
        # my_car.task.prepare_camp_fun()
        # # 感应到右侧障碍距离小于0.3
        # my_car.lane_sensor(0.3, value_h=0.3, sides=-1, stop=False)  # 移动到第一个
        # my_car.lane_dis_offset(0.3, 0.2)
        # my_car.set_pos_offset([-0.15, 0.00, 0], 0.5)  # 后移
        # my_car.set_pos_offset([0.00, -0.04, 0], 0.5)  # 向右移动一段距离
        # time.sleep(2)
        # my_car.lane_sensor(0.1, value_h=0.4, sides=-1, stop=True)
        # my_car.lane_dis_offset(0.1, 0.07)
        # my_car.task.punish_crimall1()
        # time.sleep(0.5)
        # my_car.task.reset_car()


    def go_start():
        my_car.lane_dis_offset(0.4, 1)
        # my_car.set_pos_offset([0.85, 0, 0], 2.8)


    my_car.beep()
    time.sleep(0.2)
    functions = [grap_block_func, release_block_func, get_ball_func, elevation_pole_func, get_high_ball_func,
                 pull_ball_func, hanoi_tower_func, camp_fun, find_criminal, go_start]
    my_car.manage(functions, 2)

