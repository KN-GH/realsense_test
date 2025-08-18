import pyrealsense2 as rs
import numpy as np
import cv2  # 色変換に必要

width = 1280
height = 720

# パイプライン開始
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, 30)  # カラーストリームを有効化
config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30) # 深度ストリームを有効化

profile = pipe.start(config)

for _ in range(30):
    pipe.wait_for_frames()

try:
    while True:
        frames = pipe.wait_for_frames(500)
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame:
            continue
        if not depth_frame:
            continue

        # フレームを numpy 配列に変換
        bgr_image = np.asanyarray(color_frame.get_data())
        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 150, 100])
        upper_red = np.array([5, 255, 255])
        binary_image = cv2.inRange(hsv_image, lower_red, upper_red)

        # 輪郭抽出
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 輪郭描画
        circle_image = bgr_image.copy()
        #depth_data = np.asanyarray(depth_frame.get_data())
        # 抽出した各輪郭に対して外接円を計算して描画
        for cnt in contours:
            # 輪郭の外接円を計算
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            
            # 円の中心座標と半径を整数に変換
            center = (int(x), int(y))
            radius = int(radius)
            
            # 小さすぎる円はノイズの可能性があるので、半径が10以上のものだけ描画
            if radius > 30:
                # 元の画像に円を描画
                cv2.circle(circle_image, center, radius, (0, 255, 0), 2)
                depth = depth_frame.get_distance(int(x), int(y))
                print('center point : ', (int(x), int(y)), ' radius : ', radius, ' depth : ', depth)
        
        # 表示（リアルタイム）
        cv2.imshow("Enclosing Circles", circle_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pipe.stop()
    cv2.destroyAllWindows()
