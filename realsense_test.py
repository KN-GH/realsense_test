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

        binary_image = np.zeros((height, width, 3), dtype=np.uint8)

        # しきい値により特定の色が存在する空間を抽出
        for y in range(height):
            for x in range(width):
                if hsv_image[y, x, 0] < 10 or hsv_image[y, x, 0] > 350:
                    binary_image[y, x] = [255, 255, 255]


#############################
        # 輪郭抽出
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 輪郭描画
        contour_image = bgr_image.copy()
        cv2.drawContours(contour_image, contours, -1, (0, 0, 255), 2)

        # 表示（リアルタイム）
        cv2.imshow("Contours", contour_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pipe.stop()
