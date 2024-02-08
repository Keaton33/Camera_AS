import json
import multiprocessing
import sys
import time
from multiprocessing import Process, Queue

import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
import threading

from camera import Camera
from UI import main_window, setting_window, alarm_window, comm_window
import plc

shared_data = {}
is_running = False
points = {}
data1_1, data1_2, data1_3, data2_1, data2_2, data2_3 = [], [], [], [], [], []


# region sub process, main logic, queue put all info for ui
def process_frames(q_put, share_list):
    url = 'rtsp://admin:hhmc123456@192.168.16.64/Streaming/Channels/2'
    camera = Camera(url)
    integral, prev_error = 0, 0

    with open('./config.json', 'r') as cfg:
        cfg_dit = json.load(cfg)
        ref_center = cfg_dit['process']['points']
        start_height = cfg_dit['process']['point_start'][0]
        stop_height = cfg_dit['process']['point_stop'][0]
        hb_horizontal = cfg_dit['headblock_dimension']['hb_horizontal']
        hb_vertical = cfg_dit['headblock_dimension']['hb_vertical']
        cfg.close()

    center_height = list(map(int, list(ref_center.keys())))
    center_point = list(ref_center.values())
    combined_list = [[x, y] for x, y in zip(center_height, center_point)]
    transformed_list = [[i[0]] + i[1] for i in combined_list]
    combined_np = np.array(transformed_list)

    while True:
        t = time.time()
        frame = camera.get_frame()
        hoist_height = plc.get_hoist_height()
        index_np = np.where(combined_np[:, 0] > hoist_height)[0]
        if len(index_np) > 0:
            result_np = combined_np[index_np[-1], 1:].tolist()
            hb_center_set = [int((result_np[2] + result_np[0]) / 2), int((result_np[3] + result_np[1]) / 2)]
            distance_scale = (hb_horizontal / (result_np[2] - result_np[0]) + hb_vertical / (
                    result_np[3] - result_np[1])) / 2
        else:
            hb_center_set = [0, 0]
            distance_scale = 0
        if frame is not None:
            img, xyxy = camera.process_frame(frame, hb_center_set)
            if len(xyxy) > 0:
                hb_center_act = [int((xyxy[0][2] + xyxy[0][0]) / 2), int((xyxy[0][3] + xyxy[0][1]) / 2)]

                trolley_spd_set = plc.get_trolley_set_spd()
                trolley_spd_act = plc.get_trolley_act_spd()
                trolley_position = plc.get_trolley_position()
                distance_diff = (hb_center_act[1] - hb_center_set[1]) * distance_scale
                # hb_spd = trolley_spd_act - distance_diff /
                Kp = share_list[0]
                Ki = share_list[1]
                Kd = share_list[2]
                share_list[3] = integral
                share_list[4] = prev_error

                error = 0 - distance_diff
                integral += error * 0.05
                derivative = (error - prev_error) / 0.05
                distance_offset = Kp * error + Ki * integral + Kd * derivative
                prev_error = error

                trolley_spd_cmd =  -distance_offset / 1000 / 0.02 / 2


                # setpoint = pid(distance_diff, 0, 0.1)
                # setpoint = 0
                # if trolley_spd_act > 0 and trolley_spd_set >= 0 and distance_diff > 100:
                #     trolley_spd_cmd = trolley_spd_set * 0.2
                # elif trolley_spd_act > 0 and trolley_spd_set >= 0 and distance_diff < -100:
                #     trolley_spd_cmd = -trolley_spd_set * 0.2
                # elif trolley_spd_act < 0 and trolley_spd_set <= 0 and distance_diff < -100:
                #     trolley_spd_cmd = trolley_spd_set * 0.2
                # elif trolley_spd_act < 0 and trolley_spd_set <= 0 and distance_diff > 100:
                #     trolley_spd_cmd = -trolley_spd_set * 0.2
                # else:
                # trolley_spd_cmd = 0
                plc.set_trolley_cmd_spd(trolley_spd_cmd)
                print(time.time() - t)
                q_dict = {'hoist_height': hoist_height, 'img': img, 'xyxy': xyxy[0], 'center_set': hb_center_set,
                          'center_act': hb_center_act, 'trolley_spd_set': trolley_spd_set,
                          'trolley_spd_act': trolley_spd_act, 'distance_diff': distance_diff,
                          'trolley_position': trolley_position, 'trolley_spd_cmd': trolley_spd_cmd, 'setpoint': distance_offset}
                q_put.put(q_dict)


# endregion




# region 'main window' thread for queue get all info to global variable
def update_ui(q_get):
    global shared_data

    while True:
        shared_data = q_get.get()

        main_window.show_pix(shared_data['img'])

        main_window.show_center_act(str(shared_data['xyxy']))


# endregion

def update_trend():
    global shared_data
    limit = 10000
    global data1_1, data1_2, data1_3, data2_1, data2_2, data2_3
    if shared_data != {}:
        center_act = shared_data['center_act'][1]
        center_set = shared_data['center_set'][1]
        diff = shared_data['distance_diff']

        data1_1.append(center_act)
        data1_2.append(center_set)
        data1_3.append(diff)

        # 截取数据
        data1_1 = data1_1[-limit:]
        data1_2 = data1_2[-limit:]
        data1_3 = data1_3[-limit:]

        main_window.show_chart1(data1_1, data1_2, data1_3)

        trolley_spd_set = shared_data['trolley_spd_cmd']
        trolley_spd_act = shared_data['trolley_spd_act']
        trolley_spd_cmd = shared_data['setpoint']
        data2_1.append(trolley_spd_set)
        data2_2.append(trolley_spd_act)
        data2_3.append(trolley_spd_cmd)

        data2_1 = data2_1[-limit:]
        data2_2 = data2_2[-limit:]
        data2_3 = data2_3[-limit:]

        main_window.show_chart2(data2_1, data2_2, data2_3)

    manager_list[0] = float(setting_window.ui.lineEdit_Kp.text())
    manager_list[1] = float(setting_window.ui.lineEdit_Ki.text())
    manager_list[2] = float(setting_window.ui.lineEdit_Kd.text())
    setting_window.ui.label_integral.setText(str(round(manager_list[3],2)))
    setting_window.ui.label_prev_error.setText(str(round(manager_list[4], 2)))

# region 'setting window' set reference start point
def start_point():
    global shared_data
    global is_running
    setting_window.ui.label_hoist_height_top.setText(str(shared_data['hoist_height']))
    setting_window.ui.label_xyxy_top.setText(str(shared_data['xyxy']))
    is_running = True
    t = threading.Thread(target=set_points)
    t.start()

    with open('./config.json', 'r') as cfg:
        dic_cfg = json.load(cfg)
        dic_cfg['process']['point_start'][0] = shared_data['hoist_height']
        dic_cfg['process']['point_start'][1] = shared_data['xyxy'].tolist()
    with open('./config.json', 'w') as cfg:
        json.dump(dic_cfg, cfg)

        cfg.close()


# endregion

# region 'setting window' save reference points to config.json
def stop_point():
    global shared_data
    global is_running
    global points

    is_running = False
    setting_window.ui.label_hoist_height_bottom.setText(str(shared_data['hoist_height']))
    setting_window.ui.label_xyxy_bottom.setText(str(shared_data['xyxy']))
    with open('./config.json', 'r') as cfg:
        dic_cfg = json.load(cfg)
        dic_cfg['process']['point_stop'][0] = shared_data['hoist_height']
        dic_cfg['process']['point_stop'][1] = shared_data['xyxy'].tolist()
        dic_cfg['process']['points'] = points
    with open('./config.json', 'w') as cfg:
        json.dump(dic_cfg, cfg)  # , indent=4

        cfg.close()


# endregion

# region 'setting window' thread for start_point
def set_points():
    global points
    global shared_data
    global is_running

    while is_running:
        if points:
            last_point_height = list(points.keys())[-1]
            if last_point_height - shared_data['hoist_height'] > 10:
                points[shared_data['hoist_height']] = shared_data['xyxy'].tolist()
        else:
            points[shared_data['hoist_height']] = shared_data['xyxy'].tolist()


# endregion


if __name__ == '__main__':
    q = Queue()
    manager = multiprocessing.Manager()
    manager_list = manager.list([0, 0, 0, 0, 0])
    # Start the processor to process frames
    p1 = Process(target=process_frames, args=(q, manager_list))
    p1.daemon = True
    p1.start()

    # Create the QApplication instance
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Create and show the main window
    main_window = main_window.MainWindow()
    setting_window = setting_window.SettingWindow()
    alarm_window = alarm_window.AlarmWindow()
    comm_window = comm_window.CommWindow()
    main_window.show()

    main_window.ui.actionSettings.triggered.connect(setting_window.show)
    main_window.ui.actionComm.triggered.connect(comm_window.show)
    main_window.ui.actionAlarm.triggered.connect(alarm_window.show)
    setting_window.ui.pushButton_top.clicked.connect(start_point)
    setting_window.ui.pushButton_bottom.clicked.connect(stop_point)

    # Start the thread to update the UI
    ui_update_thread = threading.Thread(target=update_ui, args=(q,))
    ui_update_thread.daemon = True
    ui_update_thread.start()

    timer = QTimer()
    timer.setInterval(50)
    timer.timeout.connect(update_trend)
    timer.start()
    # trend1_update_thread = threading.Thread(target=update_trend, args=(main_window,))
    # trend1_update_thread.daemon = True
    # trend1_update_thread.start()

    # Execute the application event loop
    sys.exit(app.exec_())
