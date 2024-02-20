import multiprocessing
import sys
import time
from multiprocessing import Process, Queue

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

import pc_process
import sc_process
from UI import main_window, setting_window, alarm_window, comm_window, automation_window
import plc

shared_data = {}
data1_1, data1_2, data1_3, data2_1, data2_2, data2_3, data3_1, data3_2 = [], [], [], [], [], [], [], []


# region 'main window' thread for queue get all info to global variable
def update_ui(q_get):
    global shared_data
    if q_get.qsize() > 1:
        q_get.get()
    shared_data = q_get.get()

    main_window.show_pix(shared_data['img'])
    main_window.ui.label_hbCenterSet.setText(str(shared_data['center_set'][1]))
    main_window.ui.label_hbCenterAct.setText(str(shared_data['xyxy'][1]))
    main_window.ui.label_trolleySpdCmd.setText(str(int(shared_data['trolley_spd_cmd'])))
    main_window.ui.label_trolleySpdSet.setText(str(int(shared_data['trolley_spd_set'])))
    main_window.ui.label_trolleySpdAct.setText(str(int(shared_data['trolley_spd_act'])))
    main_window.ui.label_trolley_act_pos.setText(str(round(manager_list[6] / 1000, 3)))
    main_window.ui.label_trolley_target_pos.setText(str(manager_list[15][0]))
    main_window.ui.label_hoist_act_pos.setText(str(round(manager_list[5] / 1000, 3)))
    main_window.ui.label_hoist_target_pos.setText(str(manager_list[15][1]))


# endregion

def update_trend():
    global shared_data
    limit = 10000
    global data1_1, data1_2, data1_3, data2_1, data2_2, data2_3, data3_1, data3_2
    if shared_data != {}:
        center_act = shared_data['center_act'][1]
        center_set = shared_data['center_set'][1]
        diff = shared_data['distance_diff'] * 1000

        data1_1.append(center_act)
        data1_2.append(center_set)
        data1_3.append(diff)

        # 截取数据
        data1_1 = data1_1[-limit:]
        data1_2 = data1_2[-limit:]
        data1_3 = data1_3[-limit:]

        main_window.show_chart1(data1_1, data1_2, data1_3)

        trolley_spd_set = shared_data['trolley_spd_set']
        trolley_spd_act = shared_data['trolley_spd_act']
        trolley_spd_cmd = shared_data['trolley_spd_cmd']
        data2_1.append(trolley_spd_set)
        data2_2.append(trolley_spd_act)
        data2_3.append(trolley_spd_cmd)

        data2_1 = data2_1[-limit:]
        data2_2 = data2_2[-limit:]
        data2_3 = data2_3[-limit:]

        main_window.show_chart2(data2_1, data2_2, data2_3)

        hoist_spd_act = manager_list[12]
        hoist_height = manager_list[5] / 1000
        data3_1.append(hoist_spd_act)
        data3_2.append(hoist_height)

        data3_1 = data3_1[-limit:]
        data3_2 = data3_2[-limit:]

        main_window.show_chart3(data3_1, data3_2)

        auto_window.update_polygon([manager_list[6] / 1000, hoist_height])

    manager_list[0] = float(setting_window.ui.lineEdit_Kp.text())
    manager_list[1] = float(setting_window.ui.lineEdit_Ki.text())
    manager_list[2] = float(setting_window.ui.lineEdit_Kd.text())
    setting_window.ui.label_integral.setText(str(round(manager_list[3], 2)))
    setting_window.ui.label_prev_error.setText(str(round(manager_list[4], 2)))
    manager_list[5] = plc.get_hoist_height()
    manager_list[6] = plc.get_trolley_position()
    manager_list[7] = plc.get_trolley_set_spd()
    manager_list[8] = plc.get_trolley_act_spd()
    manager_list[13] = plc.get_auto_start()
    plc.set_trolley_cmd_statue(manager_list[9])
    plc.set_trolley_cmd_spd(manager_list[10])
    plc.set_hoist_cmd_statue(manager_list[11])
    plc.set_hoist_cmd_spd(manager_list[12])
    manager_list[14] = plc.get_hoist_set_spd()


def sc_main(q_put: Queue, manager_list_sc: multiprocessing.Manager):
    sway_control_process = sc_process.SC_Process()
    trolley_spd_auto = 0
    while True:
        sway_control_process.sc_main(q_put, manager_list_sc, trolley_spd_auto)


def pc_main(q_put: Queue, manager_list_pc: multiprocessing.Manager):
    sway_control_process = sc_process.SC_Process()
    position_control_process = pc_process.PC_Process()
    position_control_process.get_profile()

    while True:
        t = time.time()
        hoist_height = manager_list_pc[5]
        trolley_position = manager_list_pc[6]
        trolley_spd_set = manager_list_pc[7]
        trolley_spd_act = manager_list_pc[8]
        hoist_spd_set = manager_list_pc[14]
        position_control_process.get_target(manager_list_pc[16])

        target = position_control_process.set_target(trolley_position, hoist_height)
        # print("\rtarget：", target, [round(trolley_position / 1000, 2), round(hoist_height / 1000, 2)], end='')
        # print(position_control_process.preset_point)
        if manager_list_pc[13] == 1.0:
            hoist_motion, hoist_spd_auto, trolley_spd_auto = \
                position_control_process.motion_control(target, trolley_position, hoist_height)
        else:
            hoist_motion = 0.0
            hoist_spd_auto = hoist_spd_set
            trolley_spd_auto = trolley_spd_set

        sway_control_process.sc_main(q_put, manager_list_pc, trolley_spd_auto, target[0])
        manager_list_pc[11] = hoist_motion
        manager_list_pc[12] = hoist_spd_auto
        manager_list_pc[15] = target
        # print(time.time() - t)


def set_target():
    point_1 = auto_window.ui.lineEdit.text()
    l1 = []
    for i in point_1.split(','):
        l1.append(float(i))
    point_2 = auto_window.ui.lineEdit_2.text()
    l2 = []
    for i in point_2.split(','):
        l2.append(float(i))
    point_3 = auto_window.ui.lineEdit_3.text()
    l3 = []
    for i in point_3.split(','):
        l3.append(float(i))

    target_list = [l1,l2,l3]
    manager_list[16] = target_list
    auto_window.points_to_draw.clear()


if __name__ == '__main__':
    q = Queue()
    manager = multiprocessing.Manager()
    manager_list = manager.list([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, []])

    # Start the processor to process frames
    p1 = Process(target=pc_main, args=(q, manager_list))

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
    auto_window = automation_window.AutoWindow()
    main_window.show()

    main_window.ui.actionSettings.triggered.connect(setting_window.show)
    main_window.ui.actionComm.triggered.connect(comm_window.show)
    main_window.ui.actionAlarm.triggered.connect(alarm_window.show)
    main_window.ui.actionAuto.triggered.connect(auto_window.show)
    setting_window.ui.pushButton_top.clicked.connect(setting_window.start_point)
    setting_window.ui.pushButton_bottom.clicked.connect(setting_window.stop_point)
    auto_window.ui.pushButton.clicked.connect(set_target)

    # Start the thread to update the UI
    # ui_update_thread = threading.Thread(target=update_ui, args=(q,))
    # ui_update_thread.daemon = True
    # ui_update_thread.start()

    timer_update_ui = QTimer()
    timer_update_ui.setInterval(20)
    timer_update_ui.timeout.connect(lambda: update_ui(q))
    timer_update_ui.start()

    timer = QTimer()
    timer.setInterval(20)
    timer.timeout.connect(update_trend)
    timer.start()

    # timer_auto = QTimer()
    # timer_auto.timeout.connect(lambda: auto_window.update_polygon([manager_list[6] / 1000, manager_list[5] / 1000]))
    # timer_auto.start(10)

    # Execute the application event loop
    sys.exit(app.exec_())
