# -*- coding: utf-8 -*-

import ffmpeg
import cv2
import numpy as np
import time
from ultralytics import YOLO
import torch
import queue
import threading


class Camera:
    def __init__(self, source):
        self.bboxes_xyxy = None
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = YOLO('./best.pt')
        self.model.to('cuda:0')

        self.bbox_color = (0, 255, 0)
        self.bbox_thickness = 2

        self.bbox_label_str = {'font_size': 0.5,
                               'font_thickness': 1,
                               'offset_x': 0,
                               'offset_y': -20, }

        self.kpt_color_map = {0: {'name': 'SL', 'color': [0, 0, 255], 'radius': 1},
                              1: {'name': 'SR', 'color': [0, 255, 0], 'radius': 1},
                              2: {'name': 'LR', 'color': [255, 0, 0], 'radius': 1},
                              3: {'name': 'LL', 'color': [0, 255, 255], 'radius': 1}, }

        self.kpt_label_str = {'font_size': 0.5,
                              'font_thickness': 1,
                              'offset_x': 0,
                              'offset_y': 10, }

        self.skeleton_map = [{'srt_kpt_id': 0, 'dst_kpt_id': 2, 'color': [0, 0, 150], 'thickness': 2},
                             {'srt_kpt_id': 2, 'dst_kpt_id': 1, 'color': [0, 150, 0], 'thickness': 2},
                             {'srt_kpt_id': 1, 'dst_kpt_id': 3, 'color': [155, 0, 0], 'thickness': 2},
                             {'srt_kpt_id': 3, 'dst_kpt_id': 0, 'color': [0, 150, 150], 'thickness': 2}, ]

        self.source = source

        self.args = {
            "rtsp_transport": "tcp",
            "fflags": "nobuffer",
            "flags": "low_delay"
        }  # 添加参数
        self.process = (
            ffmpeg
            .input(self.source, **self.args)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .overwrite_output()
            .run_async(pipe_stdout=True)
        )

    def get_frame(self):
        in_bytes = self.process.stdout.read(640 * 480 * 3)  # 读取图片
        if in_bytes:
            # 转成ndarray
            in_frame = (np.frombuffer(in_bytes, np.uint8).reshape([480, 640, 3]))
            frame = cv2.cvtColor(in_frame, cv2.COLOR_RGB2BGR)  # 转成BGR
            return frame
        self.process.kill()  # 关闭

    def process_frame(self, img_bgr, hb_center_set):
        """
        输入摄像头画面 bgr-array，输出图像 bgr-array
        """

        # 记录该帧开始处理的时间
        start_time = time.time()

        results = self.model(img_bgr, verbose=False)  # verbose设置为False，不单独打印每一帧预测结果

        # 预测框的个数
        num_bbox = len(results[0].boxes.cls)

        # 预测框的 xyxy 坐标
        self.bboxes_xyxy = results[0].boxes.xyxy.cpu().numpy().astype('uint32')

        # 关键点的 xy 坐标
        bboxes_key_points = results[0].keypoints.data.cpu().numpy().astype('uint32')

        for idx in range(num_bbox):  # 遍历每个框

            # 获取该框坐标
            bbox_xyxy = self.bboxes_xyxy[idx]

            # 获取框的预测类别（对于关键点检测，只有一个类别）
            bbox_label = results[0].names[0]

            # 画框
            img_bgr = cv2.rectangle(img_bgr, (bbox_xyxy[0], bbox_xyxy[1]), (bbox_xyxy[2], bbox_xyxy[3]),
                                    self.bbox_color,
                                    self.bbox_thickness)

            # 写框类别文字：图片，文字字符串，文字左上角坐标，字体，字体大小，颜色，字体粗细
            img_bgr = cv2.putText(img_bgr, bbox_label,
                                  (bbox_xyxy[0] + self.bbox_label_str['offset_x'],
                                   bbox_xyxy[1] + self.bbox_label_str['offset_y']),
                                  cv2.FONT_HERSHEY_SIMPLEX, self.bbox_label_str['font_size'], self.bbox_color,
                                  self.bbox_label_str['font_thickness'])

            bbox_key_points = bboxes_key_points[idx]  # 该框所有关键点坐标和置信度

            # 画该框的骨架连接
            for skeleton in self.skeleton_map:
                # 获取起始点坐标
                srt_kpt_id = skeleton['srt_kpt_id']
                srt_kpt_x = bbox_key_points[srt_kpt_id][0]
                srt_kpt_y = bbox_key_points[srt_kpt_id][1]

                # 获取终止点坐标
                dst_kpt_id = skeleton['dst_kpt_id']
                dst_kpt_x = bbox_key_points[dst_kpt_id][0]
                dst_kpt_y = bbox_key_points[dst_kpt_id][1]

                # 获取骨架连接颜色
                skeleton_color = skeleton['color']

                # 获取骨架连接线宽
                skeleton_thickness = skeleton['thickness']

                # 画骨架连接
                # img_bgr = cv2.line(img_bgr, (srt_kpt_x, srt_kpt_y), (dst_kpt_x, dst_kpt_y), color=skeleton_color,
                #                    thickness=skeleton_thickness)

            # 画该框的关键点
            for kpt_id in self.kpt_color_map:
                # 获取该关键点的颜色、半径、XY坐标
                kpt_color = self.kpt_color_map[kpt_id]['color']
                kpt_radius = self.kpt_color_map[kpt_id]['radius']
                kpt_x = bbox_key_points[kpt_id][0]
                kpt_y = bbox_key_points[kpt_id][1]

                # 画圆：图片、XY坐标、半径、颜色、线宽（-1为填充）
                img_bgr = cv2.circle(img_bgr, (kpt_x, kpt_y), kpt_radius, kpt_color, -1)

                # 写关键点类别文字：图片，文字字符串，文字左上角坐标，字体，字体大小，颜色，字体粗细
                # kpt_label = str(kpt_id)  # 写关键点类别 ID（二选一）
                kpt_label = str(self.kpt_color_map[kpt_id]['name'])  # 写关键点类别名称（二选一）
                img_bgr = cv2.putText(img_bgr, kpt_label,
                                      (kpt_x + self.kpt_label_str['offset_x'], kpt_y + self.kpt_label_str['offset_y']),
                                      cv2.FONT_HERSHEY_SIMPLEX, self.kpt_label_str['font_size'], kpt_color,
                                      self.kpt_label_str['font_thickness'])

        # 记录该帧处理完毕的时间
        end_time = time.time()
        # 计算每秒处理图像帧数FPS
        fps = 1 / (end_time - start_time)

        # 在画面上写字：图片，字符串，左上角坐标，字体，字体大小，颜色，字体粗细
        fps_string = 'FPS  ' + str(int(fps))  # 写在画面上的字符串
        img_bgr = cv2.putText(img_bgr, fps_string, (25, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        img_bgr = cv2.circle(img_bgr, (int(hb_center_set[0]), int(hb_center_set[1])), radius=5, color=(0, 255, 0),
                             thickness=-1)
        return img_bgr, self.bboxes_xyxy


if __name__ == '__main__':
    q = queue.Queue()


    def get_img(q_put):
        url = 'rtsp://admin:hhmc123456@192.168.16.64/Streaming/Channels/2'
        camera = Camera(url)
        while True:
            frame = camera.get_frame()
            img, xyxy = camera.process_frame(frame, [1, 1, 1, 1])
            q_put.put(img)


    def show_img(q_get):

        while True:
            frame = q_get.get()
            cv2.imshow('HD Webcam ', frame)
            key_pressed = cv2.waitKey(1)
            if key_pressed in [ord('q'), 27]:
                break
        cv2.destroyAllWindows()


    t_get_img = threading.Thread(target=get_img, args=(q,))
    t_show_img = threading.Thread(target=show_img, args=(q,))
    t_get_img.daemon = True
    t_show_img.daemon = True
    #
    t_get_img.start()
    t_show_img.start()
    #
    t_get_img.join()
    t_show_img.join()
