from math import sin
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

g = 9.8  # 重力加速度

# PID控制器参数
Kp = 10.0  # 比例增益
Ki = 0.1   # 积分增益
Kd = 0.1   # 微分增益

# PID控制器状态
integral = 0.0
prev_error = 0.0

# PID控制器
def pid_control(theta, target_theta, dt):
    global integral, prev_error
    error = target_theta - theta
    integral += error * dt
    derivative = (error - prev_error) / dt
    output = Kp * error + Ki * integral + Kd * derivative
    prev_error = error
    return output

# 单摆方程
def pendulum_equations(w, t):
    th, v = w
    dth = v
    dv  = - g * sin(th) + pid_control(th, 0.0, 0.01)  # 加入PID控制
    return dth, dv

if __name__ == "__main__":
    # 时间范围
    t = np.arange(0, 10, 0.01)

    # 初始角度和角速度
    initial_conditions = (1.0, 0)

    # 解微分方程
    track = odeint(pendulum_equations, initial_conditions, t)

    # 绘制结果
    plt.plot(t, track[:, 0])
    plt.title("Single Pendulum Motion with PID Control")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (radians)")
    plt.grid(True)
    plt.show()
