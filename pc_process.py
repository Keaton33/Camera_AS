import json

import numpy as np


class PC_Process:
    def __init__(self):
        self.Kp_position = 1.0
        self.Ki_position = 0.001
        self.Kd_position = 0.01
        self.prev_output_position = 0
        self.prev_error_position = 0
        self.integral_position = 0
        self.preset_point = None
        self.profile = None
        with open('./config.json') as cfg:
            cfg_dit = json.load(cfg)
            self.trolley_max_spd = cfg_dit['crane_data']['trolley_speed']['max_speed']
            self.hoist_max_spd = cfg_dit['crane_data']['hoist_speed']['max_speed']
            self.up_end_height = cfg_dit['crane_data']['hoist_position']['up_end']
            self.hoist_acc_time = cfg_dit['crane_data']['hoist_speed']['acc_time']
            self.hoist_dec_time = cfg_dit['crane_data']['hoist_speed']['dec_time']

    def get_profile(self):
        with open('./config.json') as cfg:
            cfg_dit = json.load(cfg)
            self.profile = np.array(cfg_dit['profile'])
        # 增加数据校验(数据连续、在行程内)

    def get_target(self):
        self.preset_point = [[15, 16], [30, 16], [40, 12]]
        # 增加数据校验（按照向前或向后方向排序点、在行程内）

    def set_target(self, trolley_position, hoist_position):
        trolley_pos = trolley_position / 1000
        hoist_pos = hoist_position / 1000
        target_next = [trolley_pos, hoist_pos]

        if self.profile[-1][2] >= self.preset_point[-1][0] >= self.profile[0][0]:  # 最终目标位置在轮廓内
            if self.preset_point[-1][0] > trolley_pos and self.preset_point[-1][0] > self.preset_point[0][0]:  # 向前
                for i in self.preset_point:  # 找预设点
                    if i[0] > trolley_pos:  # [15, 16], [30, 16], [40, 12]
                        target_point = i

                        target_trolley = self.preset_point[-1][0]  # 小车目标为最终位置
                        target_hoist = target_point[1]

                        indices = np.where(self.profile[:, 2] > trolley_pos)[0]
                        if np.size(indices) > 1:
                            profile_region_current = self.profile[indices[0]]
                            profile_region_next = self.profile[indices[1]]  # 确保有当前轮廓和下一个轮廓
                        elif np.size(indices) == 1:
                            profile_region_current = self.profile[indices[0]]
                            profile_region_next = profile_region_current  # 确保有当前轮廓和下一个轮廓
                        else:
                            profile_region_current = self.profile[-1]
                            profile_region_next = profile_region_current  # 确保有当前轮廓和下一个轮廓

                        f_down_profile = self.profile[indices]
                        f_down_profile_max_height = np.max(f_down_profile[:, 1])

                        profile_region_current_trolley = profile_region_current[2]
                        profile_region_current_hoist = profile_region_current[1]
                        profile_region_next_hoist = profile_region_next[1]

                        if target_hoist < f_down_profile_max_height:
                            target_hoist = f_down_profile_max_height

                        if hoist_pos < target_hoist:  # 向上
                            if hoist_pos > profile_region_next_hoist:  # 增加高度确保安全
                                target_next = [target_trolley, target_hoist]
                            elif hoist_pos < profile_region_current_hoist:
                                target_next = [trolley_pos, target_hoist]
                            else:
                                target_next = [profile_region_current_trolley, target_hoist]  # 减小距离确保安全
                        else:  # 向下

                            if hoist_pos > f_down_profile_max_height:  # 增加高度确保安全
                                target_next = [target_trolley, target_hoist]
                            elif hoist_pos < profile_region_current_hoist:
                                target_next = [trolley_pos, target_hoist]
                            else:
                                target_next = [profile_region_current_trolley, f_down_profile_max_height]
                        break

            elif self.preset_point[-1][0] < trolley_pos and self.preset_point[-1][0] < self.preset_point[0][0]:  # 向后
                for i in self.preset_point:

                    if i[0] < trolley_pos:  # [50, 9], [30, 16], [15, 16]
                        target_point = i

                        target_trolley = self.preset_point[-1][0]
                        target_hoist = target_point[1]

                        indices = np.where(self.profile[:, 0] < trolley_pos)[0]
                        if np.size(indices) > 1:
                            profile_region_current = self.profile[indices[-1]]
                            profile_region_next = self.profile[indices[-2]]  # 确保有当前轮廓和下一个轮廓
                        elif np.size(indices) == 1:
                            profile_region_current = self.profile[indices[-1]]
                            profile_region_next = profile_region_current  # 确保有当前轮廓和下一个轮廓
                        else:
                            profile_region_current = self.profile[0]
                            profile_region_next = profile_region_current  # 确保有当前轮廓和下一个轮廓

                        b_down_profile = self.profile[indices]
                        b_down_profile_max_height = np.max(b_down_profile[:, 1])

                        profile_region_current_trolley = profile_region_current[0]
                        profile_region_current_hoist = profile_region_current[1]
                        profile_region_next_hoist = profile_region_next[1]

                        if target_hoist < b_down_profile_max_height:
                            target_hoist = b_down_profile_max_height

                        if hoist_pos < target_hoist:  # 向上

                            if hoist_pos > profile_region_next_hoist:  # 增加高度确保安全
                                target_next = [target_trolley, target_hoist]
                            elif hoist_pos < profile_region_current_hoist:
                                target_next = [trolley_pos, target_hoist]
                            else:
                                target_next = [profile_region_current_trolley, target_hoist]  # 减小距离确保安全
                        else:  # 向下

                            if hoist_pos > b_down_profile_max_height:  # 增加高度确保安全
                                target_next = [target_trolley, target_hoist]
                            elif hoist_pos < profile_region_current_hoist:
                                target_next = [trolley_pos, target_hoist]
                            else:
                                target_next = [profile_region_current_trolley, b_down_profile_max_height]
                        break
            else:
                target_next = [self.preset_point[-1][0], self.preset_point[-1][1]]
        else:
            target_next = [trolley_pos, self.up_end_height]
        return target_next

    def motion_control(self, target, trolley_position, hoist_position):
        trolley_pos = trolley_position / 1000
        hoist_pos = hoist_position / 1000
        target_trolley = target[0]
        target_hoist = target[1]

        t_dec = self.hoist_dec_time
        s_dec = 0.5 * (self.hoist_max_spd / t_dec) * t_dec * t_dec
        k_dec = 100 / s_dec

        hoist_spd_limit = (target_hoist - hoist_pos) * k_dec
        if hoist_spd_limit > 0:
            hoist_spd_cmd = min(hoist_spd_limit, 100)
        else:
            hoist_spd_cmd = max(-100, hoist_spd_limit)

        if abs(hoist_pos - target_hoist) < 0.1:
            hoist_motion = 0.0
            hoist_spd_cmd = 0
        else:
            hoist_motion = 1.0

        if (target_trolley - trolley_pos) > 1:
            trolley_spd_cmd = 100
        elif abs(target_trolley - trolley_pos) <= 1:  # 距离小于1m时位置控制

            trolley_spd_cmd = self.position_control(trolley_pos, target_trolley, dt=0.03)
        else:
            trolley_spd_cmd = -100


        return hoist_motion, hoist_spd_cmd, trolley_spd_cmd

    def position_control(self, trolley_position, target_position, dt):
        error = target_position - trolley_position  # 当前误差
        self.integral_position += error * dt  # 累积误差

        # 计算PID控制器的输出
        output = self.Kp_position * error + self.Ki_position * self.integral_position + self.Kd_position * (
                error - self.prev_error_position) / dt

        # 保存当前误差作为下一次的前一次误差
        self.prev_error_position = error

        return output
