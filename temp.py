# import sys
# import time
#
# import numpy as np
# import pyqtgraph as pg
# from PyQt5.QtCore import QTimer
# from PyQt5.QtWidgets import QApplication, QMainWindow
#
# integral = 0
# prev_error = 0
# Kp = 1.0
# Ki = 0.1
# Kd = 0.1
#
#
# def points_visual():
#     global t
#     global y6
#     global x6
#     dt = time.time() - t
#     x6 += dt
#     plot_widget.plot( pen=None, symbol='+', symbolPen=None, symbolSize=5, symbolBrush=(255, 255, 255, 255))
#     t = time.time()
#
#
#
#
#
#
# # 创建 Qt 应用程序
# app = QApplication(sys.argv)
#
# # 创建主窗口
# main_window = QMainWindow()
#
# # 创建 PyQtGraph 画布
# plot_widget = pg.PlotWidget()
# main_window.setCentralWidget(plot_widget)
# t = time.time()
# # 绘制点图
# timer = QTimer()
# timer.timeout.connect(points_visual)
# timer.start(50)
#
# # 显示主窗口
# main_window.show()
#
# # 运行 Qt 应用程序
# sys.exit(app.exec_())
#
#
# class MyClass:
#     def __init__(self, instance_attr):
#         self.instance_attr = instance_attr
#
#     def update_class_attr(self):
#         new_value = self.instance_attr + 1
#
# a = 0
#
# # 实例化对象
# obj1 = MyClass(a)
# while True:
#     a += 1
#     obj1.update_class_attr()


import matplotlib.pyplot as plt
import numpy as np
speed_interior = 0
# 定义函数
def speed_adjustment(v_cmd, ramp_up, ramp_down, dt):
    global speed_interior
    if v_cmd >= 0:
        if v_cmd > speed_interior:
            if speed_interior < 0:
                speed_interior -= ramp_down * dt
            else:
                speed_interior += ramp_up * dt
        elif int(v_cmd) == int(speed_interior):
            speed_interior = v_cmd
        else:
            speed_interior += ramp_down * dt
    else:
        if speed_interior > v_cmd:
            if speed_interior > 0:
                speed_interior += ramp_down * dt
            else:
                speed_interior -= ramp_up * dt
        elif int(speed_interior) == int(v_cmd):
            speed_interior = v_cmd
        else:
            speed_interior -= ramp_down * dt

    return speed_interior

# 参数设定
ramp_up = 100/6
ramp_down = -100/6
dt = 0.1

# 初始化速度列表
speeds = []

# 初始化v_cmd列表
v_cmd_values = np.linspace(0, 100, 100)

# 循环执行speed_adjustment函数
for v_cmd in v_cmd_values:
    speed = speed_adjustment(-100,  ramp_up, ramp_down, dt)
    speeds.append(speed)

# 绘图
plt.plot(v_cmd_values, speeds)
plt.xlabel('v_cmd')
plt.ylabel('self.speed_interior')
plt.title('Speed Adjustment Function')
plt.grid(True)
plt.show()

