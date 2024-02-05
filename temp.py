# import cv2
#
# cap = cv2.VideoCapture(0)
#
#
# def get_cap():
#     if cap.isOpened():
#         ret, frame = cap.read()
#         return frame
#
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QWidget, QLabel
#
# class SettingWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Setting")
#         self.setGeometry(100, 100, 400, 300)
#
#         # Add widgets, layout, etc. to your setting window
#         label = QLabel("Setting Window")
#         layout = QVBoxLayout()
#         layout.addWidget(label)
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Main Window")
#         self.setGeometry(200, 200, 600, 400)
#
#         # Create a menu bar and add a menu item for settings
#         menubar = self.menuBar()
#         settings_menu = menubar.addMenu("Settings")
#
#         # Add an action for opening the setting window
#         open_setting_action = QAction("Open Setting", self)
#         open_setting_action.triggered.connect(self.open_setting_window)
#         settings_menu.addAction(open_setting_action)
#
#     def open_setting_window(self):
#         self.setting_window = SettingWindow()
#         self.setting_window.show()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     sys.exit(app.exec_())
# from snap7 import util, client
# from snap7.types import S7AreaDB
#
# my_plc = client.Client()  # 实例化客户端
# my_plc.connect('192.168.0.1', 0, 0)  # 连接s7-1200
# byte_arrays = my_plc.db_read(21, 812, 4)
# # byte_arrays = my_plc.read_area(S7AreaDB, 21, 812, 4)  # 读出变量的字节数组
# value = util.get_real(byte_arrays, 0)  # 通过数据类型取值
# my_plc.disconnect()  # 断开连接
# my_plc.destroy()  # 销毁
# print(value)

import snap7
client = snap7.client.Client()
client.connect("192.168.0.1", 0, 0)
client.get_connected()

data = client.db_read(21, 812, 4)
value = snap7.util.get_dint(data, 0)
print(data)
print(value)
client.disconnect()  # 断开连接
client.destroy()  # 销毁

