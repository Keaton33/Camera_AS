import multiprocessing
import sys
from multiprocessing import Process, Queue

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

import sc_process
from UI import main_window, setting_window, alarm_window, comm_window
import plc

shared_data = {}
data1_1, data1_2, data1_3, data2_1, data2_2, data2_3 = [], [], [], [], [], []


# region 'main window' thread for queue get all info to global variable
def update_ui(q_get):
    global shared_data

    # while True:

    shared_data = q_get.get()

    main_window.show_pix(shared_data['img'])

    main_window.show_center_act(str(shared_data['xyxy']))

    setting_window.hoist_height = shared_data['hoist_height']
    setting_window.xyxy = shared_data['xyxy']


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
    setting_window.ui.label_integral.setText(str(round(manager_list[3], 2)))
    setting_window.ui.label_prev_error.setText(str(round(manager_list[4], 2)))
    manager_list[5] = plc.get_hoist_height()
    manager_list[6] = plc.get_trolley_position()
    manager_list[7] = plc.get_trolley_set_spd()
    manager_list[8] = plc.get_trolley_act_spd()
    plc.set_trolley_cmd_statue(manager_list[9])
    plc.set_trolley_cmd_spd(manager_list[10])


def sc_main(q_put: Queue, manager_list: multiprocessing.Manager):
    sway_control_process = sc_process.SC_Process()

    sway_control_process.sc_main(q_put, manager_list)


if __name__ == '__main__':
    q = Queue()
    manager = multiprocessing.Manager()
    manager_list = manager.list([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # Start the processor to process frames
    # p1 = Process(target=sway_control_process.sc_main, args=(q, manager_list))
    p1 = Process(target=sc_main, args=(q, manager_list))

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
    setting_window.ui.pushButton_top.clicked.connect(setting_window.start_point)
    setting_window.ui.pushButton_bottom.clicked.connect(setting_window.stop_point)

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

    # Execute the application event loop
    sys.exit(app.exec_())
