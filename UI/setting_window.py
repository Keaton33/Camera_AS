import json
import sys
import threading

from PyQt5.QtWidgets import QApplication, QDialog
from UI import settings_ui


class SettingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = settings_ui.Ui_SettingWindow()
        self.ui.setupUi(self)
        self.is_running = False
        self.hoist_height = 0
        self.xyxy = []
        self.points = {}

    # region 'setting window' set reference start point
    def start_point(self):
        self.ui.label_hoist_height_top.setText(str(self.hoist_height))
        self.ui.label_xyxy_top.setText(str(self.xyxy))
        self.is_running = True
        t = threading.Thread(target=self.set_points)
        t.start()

        with open('./config.json', 'r') as cfg:
            dic_cfg = json.load(cfg)
            dic_cfg['process']['point_start'][0] = self.hoist_height
            dic_cfg['process']['point_start'][1] = self.xyxy
        with open('./config.json', 'w') as cfg:
            json.dump(dic_cfg, cfg)

            cfg.close()

    # endregion

    # region 'setting window' save reference points to config.json
    def stop_point(self):

        self.is_running = False
        self.ui.label_hoist_height_bottom.setText(str(self.shared_data['hoist_height']))
        self.ui.label_xyxy_bottom.setText(str(self.shared_data['xyxy']))
        with open('./config.json', 'r') as cfg:
            dic_cfg = json.load(cfg)
            dic_cfg['process']['point_stop'][0] = self.shared_data['hoist_height']
            dic_cfg['process']['point_stop'][1] = self.shared_data['xyxy'].tolist()
            dic_cfg['process']['points'] = self.points
        with open('./config.json', 'w') as cfg:
            json.dump(dic_cfg, cfg)  # , indent=4

            cfg.close()

    # endregion

    # region 'setting window' thread for start_point
    def set_points(self):

        while self.is_running:
            if self.points:
                last_point_height = list(self.points.keys())[-1]
                if last_point_height - self.hoist_height > 10:
                    self.points[self.hoist_height] = self.xyxy
            else:
                self.points[self.hoist_height] = self.xyxy

    # endregion


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setting = SettingWindow()
    setting.show()
    setting.ui.pushButton_top.clicked.connect(lambda: setting.show_hoist_height_top('555'))
    sys.exit(app.exec_())
