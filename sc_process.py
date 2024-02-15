import json

import numpy as np


# def calculate_error_and_dt(func):
#     def wrapper(self, *args, **kwargs):
#         distance = kwargs.get('distance', 0.0)
#         t_previous = kwargs.get('t_previous', time.time())
#         dt = time.time() - t_previous
#         return func(self, distance, dt, *args, **kwargs)
#
#     return wrapper


class SC_Process:
    def __init__(self, Kp=1.0, Ki=0.1, Kd=0.1):

        self.ramp_down = 1
        self.ramp_up = None
        self.min_amplitude_sign = False
        self.max_amplitude_sign = False
        self.duration = 0
        self.max_amplitude = 0
        try:
            with open('./config.json', 'r') as cfg:
                dic_cfg = json.load(cfg)
                self.hb_hor_dimension = dic_cfg['headblock_dimension']['hb_horizontal']
                self.hb_ver_dimension = dic_cfg['headblock_dimension']['hb_vertical']
        except FileNotFoundError:
            print("Config file not found.")
            # 如果文件不存在，则可以提供默认值或者抛出异常进行处理

        self.integral = 0
        self.prev_error = 0
        self.speed_interior = 0
        self.set_spd = [0]
        self.smooth_spd = [0]
        self.distance_diff_record = [0]
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def set_pid_constants(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def pid(self, distance_diff, dt):
        error = 0.0 - distance_diff
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        dis_offset = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error
        return dis_offset

    def speed_with_ramp(self, **kwargs) -> float:
        """
            v_now: speed input
            v_cmd: speed command
            dt: time of speed input
            pid_offset: pid -> predict point - reference point, (-) hb at front (+) hb at back
            ramp_up_time: drive up ramp
            ramp_down_time: drive down ramp
            max_spd_per: percentage 0.0 - 1.0
        :return: speed percentage control for next cycle
        """
        v_now = kwargs.get('v_now', 0.0)
        v_cmd = kwargs.get('v_cmd', 0.0)
        ramp_up_time = kwargs.get('ramp_up_time', 6.0)
        ramp_down_time = kwargs.get('ramp_down_time', 6.0)
        max_spd_per = kwargs.get('max_spd_per', 0.9)
        pid_offset = kwargs.get('pid_offset', 0)
        dt = kwargs.get('dt', 0)
        trolley_position = kwargs.get('trolley_position', 0)

        self.ramp_up = 100 * max_spd_per / ramp_up_time
        self.ramp_down = -100 * max_spd_per / ramp_down_time

        if v_cmd >= 0:
            if v_cmd > self.speed_interior:
                if self.speed_interior < 0:
                    self.speed_interior -= self.ramp_down * dt
                else:
                    self.speed_interior += self.ramp_up * dt
            elif int(v_cmd) == int(self.speed_interior) and (int(v_cmd) != 0 or int(self.speed_interior) == 0):
                self.speed_interior = v_cmd
            else:
                self.speed_interior += self.ramp_down * dt
        else:
            if self.speed_interior > v_cmd:
                if self.speed_interior > 0:
                    self.speed_interior += self.ramp_down * dt
                else:
                    self.speed_interior -= self.ramp_up * dt
            elif int(self.speed_interior) == int(v_cmd) and (int(v_cmd) != 0 or int(self.speed_interior) == 0):
                self.speed_interior = v_cmd
            else:
                self.speed_interior -= self.ramp_down * dt
        #  斜坡后达到控制速度

        if len(self.set_spd) > 100:
            self.set_spd = self.set_spd[-100:]
            self.smooth_spd = self.smooth_spd[-100:]
        #  清空速度记录列表

        if dt == 0:
            speed_out = self.speed_interior
            self.set_spd = [0]
        else:
            speed_offset = (pid_offset / dt) / (180 / 60)  # 要补偿调节量的速度
            # print("\rspeed adjust： {:.2f}%".format(speed_offset), end='')
            self.set_spd.append(self.speed_interior + speed_offset)  # 基础速度 + 调节速度
            self.smooth_spd = self.moving_average(self.set_spd, 5)

            if len(self.smooth_spd) > 5:
                max_spd_offset = self.smooth_spd[-2] + (100 / ramp_up_time * dt)
                min_spd_offset = self.smooth_spd[-2] - (100 / ramp_down_time * dt)
                speed_out = max(min_spd_offset, min(max_spd_offset, self.smooth_spd[-1]))
                #  限制pid后在基本速度上调整下周期速度变化量????只变一次
            else:
                speed_out = self.speed_interior

        if v_cmd > 0:
            cntr_spd = max(0, speed_out)
        elif v_cmd < 0:
            cntr_spd = min(0, speed_out)
        else:
            cntr_spd = speed_out
        # 限制最终输出速度, 向前时不可以-速度

        return cntr_spd

    @staticmethod
    def moving_average(data, window_size):
        # 定义一个窗口，其中包含所有权重的平均值
        weights = np.repeat(1.0, window_size) / window_size
        # 使用convolve函数来计算移动平均
        # mode='valid' 表示只计算完全重叠的部分
        return np.convolve(data, weights, 'valid')

    @staticmethod
    def pendulum_model_duration(L):
        # 计算单摆的周期
        period = 2 * np.pi * np.sqrt(L / 9.8)
        return period

    @staticmethod
    def pendulum_model(L, max_amplitude):
        """
        根据摆长和最大摆幅生成单摆的周期，并在整个周期内计算每隔0.01秒的摆角、摆幅、角速度和加速度

        参数:
        L: 单摆长度（米）
        max_amplitude: 最大摆幅（米）

        返回:
        period: 单摆的周期（秒）
        angles: 每隔0.01秒的摆角（弧度）数组
        amplitudes: 每隔0.01秒的摆幅（米）数组
        angular_velocities: 每隔0.01秒的角速度（弧度/秒）数组
        accelerations: 每隔0.01秒的加速度（米/秒^2）数组
        """

        # 如果最大摆幅为0，则将摆角、摆幅、角速度和加速度设置为0
        if max_amplitude == 0:
            period = 0
            angles = np.array([0])
            amplitudes = np.array([0])
            angular_velocities = np.array([0])
            accelerations = np.array([0])
        else:
            # 计算单摆的周期
            period = 2 * np.pi * np.sqrt(L / 9.8)

            # 计算摆角数组
            t = np.arange(0, period, 0.01)
            angles = np.arcsin(max_amplitude / L * np.sin(2 * np.pi / period * t))

            # 计算摆幅数组
            amplitudes = L * np.sin(angles)

            # 计算角速度数组
            angular_velocities = np.ones_like(t) * (2 * np.pi / period)

            # 计算加速度数组
            accelerations = -(9.8 / L) * np.sin(angles)

        return period, angles, amplitudes, angular_velocities, accelerations

    #  initial_angle_radian = np.deg2rad(initial_angle_degree)
    @staticmethod
    def find_closest_value(target_value, array):
        """
        在数组中查找最接近目标值的元素，并返回该元素的索引和值
        eg:在 amplitudes 中查找最接近的值,np.argmin返回最小值的索引
        closest_index, closest_amplitude = find_closest_value(target_amplitude, amplitudes)
        """
        closest_index = np.argmin(np.abs(array - target_value))
        closest_value = array[closest_index]
        return closest_index, closest_value

    def find_max_amplitude(self, distance_diff, dt, duration):
        if abs(distance_diff - self.distance_diff_record[-1]) > 0.05:  # 防摇结束灵敏度
            self.distance_diff_record.append(distance_diff)
            self.duration = 0
        else:
            self.duration += dt
        if len(self.distance_diff_record) > 1:
            ds = self.distance_diff_record[-1] - self.distance_diff_record[-2]
            if distance_diff > 0 > ds / dt and not self.max_amplitude_sign:
                self.max_amplitude = self.distance_diff_record[-2]
                self.distance_diff_record = [0]
                self.max_amplitude_sign = True
                self.min_amplitude_sign = False
            elif distance_diff < 0 < ds / dt and not self.min_amplitude_sign:
                self.max_amplitude = self.distance_diff_record[-2]
                self.distance_diff_record = [0]
                self.min_amplitude_sign = True
                self.max_amplitude_sign = False
        else:
            self.max_amplitude = 0
            self.duration = 0
            self.distance_diff_record = [0]
            self.min_amplitude_sign = False
            self.max_amplitude_sign = False

        if self.duration > duration:
            self.max_amplitude = 0
            self.duration = 0
            self.distance_diff_record = [0]
            self.min_amplitude_sign = False
            self.max_amplitude_sign = False

        return {'max_amplitude': self.max_amplitude}

    def speed_limit(self, target_trolley, act_trolley, trolley_spd_act, s_offset):
        t_dec = abs(100 / self.ramp_down)
        # t_dec = 6
        s = 0.5 * ((180 / 60) / t_dec) * t_dec * t_dec  # 100% / 1/2att
        k = 100 / (s + s_offset)

        if trolley_spd_act > 0:
            if target_trolley >= act_trolley:
                trolley_spd_limit = ((target_trolley - act_trolley) / 1000) * k
                trolley_spd_limit = min(100, max(10, trolley_spd_limit))
            else:
                trolley_spd_limit = 0
        elif trolley_spd_act < 0:
            if target_trolley <= act_trolley:
                trolley_spd_limit = ((target_trolley - act_trolley) / 1000) * k
                trolley_spd_limit = max(-100, min(-10, trolley_spd_limit))
            else:
                trolley_spd_limit = 0
        else:
            trolley_spd_limit = None

        # print(s, s_offset, trolley_spd_limit)
        return trolley_spd_limit

    @staticmethod
    def calculate_swing_amplitude(L, v0, g):
        # 计算最大振幅
        h = v0 ** 2 / (2 * g)
        a = np.sqrt(L**2 - (L-h)**2)
        return a

    def position_control(self, trolley_position, target_position, dt):
        error = target_position - trolley_position  # 当前误差
        self.integral_position += error * dt  # 累积误差

        # 计算PID控制器的输出
        output = self.Kp_position * error + self.Ki_position * self.integral_position + self.Kd_position * (error - self.prev_error_position) / dt

        # 限制输出变化量
        output_change = output - self.prev_output_position
        if abs(output_change) > self.max_output_change:
            output = self.prev_output_position + np.sign(output_change) * self.max_output_change

        # 保存当前输出作为下一次的前一次输出
        self.prev_output_position = output

        # 保存当前误差作为下一次的前一次误差
        self.prev_error_position = error

        return output