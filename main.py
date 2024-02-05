import json
import plc
import sys
from multiprocessing import Process, Queue

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow

from camera import Camera
from UI import main_window, setting_window, alarm_window, comm_window
import sa_process
import numpy as np
import threading


def update_ui(q_get, window):
    global XYXY
    while True:
        img, xyxy = q_get.get()
        window.show_pix(img)
        XYXY = xyxy
        if np.size(xyxy):
            window.show_center_act(str(xyxy[0]))


# global XYXY


XYXY = []
hoist_height = 0

def get_xyxy():
    return XYXY

def process_frames(q_put):
    url = 'rtsp://admin:hhmc123456@192.168.16.64/Streaming/Channels/2'
    camera = Camera(url)
    # sc = sa_process.Process()

    while True:
        frame = camera.get_frame()
        # hoist_height = sc.get_hoist_height()
        # hb_center_set = [(hoist_height * sc.slope_x[0] + sc.slope_x[1]), (hoist_height * sc.slope_y[0] + sc.slope_y[1])]
        hb_center_set = [100, 100, 100, 100]
        frame_ret = camera.process_frame(frame, hb_center_set)
        q_put.put(frame_ret)

        # print(hb_center_set)


def config_points(sc_top):
    start = setting_window.ui.pushButton_bottom.isChecked()

    points = {}
    while not start:
        hoist_height = sc_top.get_hoist_height()
        if points:
            last_point_height = list(points.keys())[-1]
            if last_point_height - hoist_height > 10:
                points[hoist_height] = XYXY
        else:
            points[hoist_height] = XYXY
    # self.client.disconnect()
    # self.client.destroy()
    with open('./config.json', 'w') as cfg:
        dic_cfg = json.load(cfg)
        dic_cfg['process']['point_top'][0] = sc_top.get_hoist_height()
        dic_cfg['process']['point_top'][1] = XYXY
        dic_cfg['process']['points'] = points
        json.dump(dic_cfg, cfg, indent=4)

        cfg.close()


def setting_top(sc_top):
    global XYXY
    setting_window.ui.label_hoist_height_top.setText(str(sc_top.get_hoist_height()))
    setting_window.ui.label_xyxy_top.setText(str(XYXY[0]))

    t1 = threading.Thread(target=config_points)
    t1.daemon = True
    t1.start()

    # t1.join()
    # sc_top.set_points(XYXY, flag= start)


def setting_bottom(sc_bottom):
    global XYXY
    # setting_window.ui.label_hoist_height_bottom.setText(str(sc_bottom.get_hoist_height()))
    setting_window.ui.label_xyxy_bottom.setText(str(XYXY[0]))
    # sa = sa_process.Process()
    h_top = int(setting_window.ui.label_hoist_height_top.text())
    # xyxy_top = setting_window.ui.label_xyxy_top.text().strip('[').strip(']').split(' ')
    # while xyxy_top.count(''):
    #     xyxy_top.remove('')

    # h_bottom = int(setting_window.ui.label_hoist_height_bottom.text())
    # xyxy_bottom = setting_window.ui.label_xyxy_bottom.text().strip('[').strip(']').split(' ')
    # while xyxy_bottom.count(''):
    #     xyxy_bottom.remove('')

    # sc.set_slope_scale(h_top, h_bottom, xyxy_top, xyxy_bottom)


def setting_config():
    pass


if __name__ == '__main__':
    q = Queue()
    # sc = sa_process.Process()

    # hoist_height = sc.get_hoist_height()

    # Start the processor to process frames
    p1 = Process(target=process_frames, args=(q,))
    p1.daemon = True
    p1.start()

    # Create the QApplication instance
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Create and show the main window
    main_window = main_window.MainWindow()
    setting_window = setting_window.SettingWindow(get_xyxy(), plc.get_hoist_height())
    alarm_window = alarm_window.AlarmWindow()
    comm_window = comm_window.CommWindow()
    main_window.show()

    main_window.ui.actionSettings.triggered.connect(setting_window.show)
    main_window.ui.actionComm.triggered.connect(comm_window.show)
    main_window.ui.actionAlarm.triggered.connect(alarm_window.show)
    # setting_window.ui.pushButton_top.clicked.connect(lambda: setting_top(sc))
    # setting_window.ui.pushButton_bottom.clicked.connect(lambda: setting_bottom(sc))

    # Initialize ui

    # Start the thread to update the UI
    ui_update_thread = threading.Thread(target=update_ui, args=(q, main_window))
    ui_update_thread.daemon = True
    ui_update_thread.start()

    # Execute the application event loop
    sys.exit(app.exec_())
