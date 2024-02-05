import json


from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QWidget


class Process():
    def __init__(self):
        with open('./config.json', 'r') as cfg:
            dic_cfg = json.load(cfg)
            self.slope_x = dic_cfg['process']['slope_x']
            self.slope_y = dic_cfg['process']['slope_y']
            self.scale = dic_cfg['process']['scale']
            self.hb_hor_dimension = dic_cfg['headblock']['hb_horizontal']
            self.hb_ver_dimension = dic_cfg['headblock']['hb_vertical']
            self.plc_ip = dic_cfg['plc']['ip']
            self.h_height = dic_cfg['plc']['db_hoist_height']
        cfg.close()

        # client.disconnect()
        # self.h_height = hoist_height
        # self.t_position = trolley_position
        # self.t_speed = trolley_speed

    def set_slope_scale(self, hoist_height_top, hoist_height_bottom, xyxy_top, xyxy_bottom):
        mid_top = [(int(xyxy_top[2]) + int(xyxy_top[0])) / 2, (int(xyxy_top[3]) + int(xyxy_top[1])) / 2]
        mid_bottom = [(int(xyxy_bottom[2]) + int(xyxy_bottom[0])) / 2, (int(xyxy_bottom[3]) + int(xyxy_bottom[1])) / 2]

        self.slope_x[0] = (mid_top[0] - mid_bottom[0]) / (hoist_height_top - hoist_height_bottom)
        self.slope_x[1] = mid_top[0] - self.slope_x[0] * hoist_height_top

        self.slope_y[0] = (mid_top[1] - mid_bottom[1]) / (hoist_height_top - hoist_height_bottom)
        self.slope_y[1] = mid_top[1] - self.slope_y[0] * hoist_height_top

        self.scale[0] = (self.hb_hor_dimension / (int(xyxy_top[2]) - int(xyxy_top[0])) -
                         self.hb_hor_dimension / (int(xyxy_bottom[2]) - int(xyxy_bottom[0]))) / \
                        (hoist_height_top - hoist_height_bottom)
        self.scale[1] = self.hb_hor_dimension / (int(xyxy_top[2]) - int(xyxy_top[0])) - self.scale[0] * hoist_height_top

        with open('./config.json', 'r') as cfg:
            dic_cfg = json.load(cfg)
            dic_cfg['process']['slope_x'] = self.slope_x
            dic_cfg['process']['slope_y'] = self.slope_y
            dic_cfg['process']['scale'] = self.scale
        with open('./config.json', 'w') as cfg:
            json.dump(dic_cfg, cfg, indent=2)

            cfg.close()


    def set_points(self, xyxy, flag):
        points = {}
        while not flag:
            hoist_height = self.get_hoist_height()
            if points:
                last_point_height = list(points.keys())[-1]
                if last_point_height - hoist_height > 10:
                    points[hoist_height] = xyxy
            else:
                points[hoist_height] = xyxy
        # self.client.disconnect()
        # self.client.destroy()
        print(flag)
        with open('./config.json', 'w') as cfg:
            dic_cfg = json.load(cfg)
            dic_cfg['process']['point_top'][0] = self.get_hoist_height()
            dic_cfg['process']['point_top'][1] = xyxy
            dic_cfg['process']['points'] = points
            json.dump(dic_cfg, cfg, indent=4)

            cfg.close()

    def set_trolley_max_spd(self):
        pass

    def set_trolley_acc(self):
        pass

    def set_hb_dimension_hori(self):
        pass

    def set_hb_dimension_ver(self):
        pass


# p = Process()
#
# # p.y_slope
# p.hb_hor_dimension
# p.hb_ver_dimension
