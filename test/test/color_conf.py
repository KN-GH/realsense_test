# color_conf.py
# 画像の特定の座標の色を出力する
y = 530
x = 800

import pyrealsense2 as rs
import numpy as np
import cv2  # 色変換に必要
import colorsys

width = 1280
height = 720

# パイプライン開始
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, 30)  # カラーストリームを有効化

profile = pipe.start(config)

for _ in range(30):
    pipe.wait_for_frames()

try:
    for i in range(100):
        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # フレームを numpy 配列に変換
        bgr_image = np.asanyarray(color_frame.get_data())
        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

        h, s, v = hsv_image[y, x]
        print('h:', h, ' s:', s, ' v:', v)

        # b, g, r = bgr_image[y, x]
        # print('b:', b, ' g:', g, ' r:', r)
finally:
    pipe.stop()