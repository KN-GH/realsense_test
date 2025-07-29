import pyrealsense2 as rs
import numpy as np
import cv2

width = 1280
height = 720

# パイプライン開始
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(
    rs.stream.color, width, height, rs.format.bgr8, 30
)  # カラーストリームを有効化
config.enable_stream(
    rs.stream.depth, width, height, rs.format.z16, 30
)  # 深度ストリームを有効化

profile = pipe.start(config)

# 深度センサーのスケールを取得（深度値をメートルに変換するため）
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# アライメントを設定（カラー画像と深度画像の位置を合わせる）
align_to = rs.stream.color
align = rs.align(align_to)

# ★★★ 変換に必要なカメラの内部パラメータを取得 ★★★
depth_intrinsics = (
    profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()
)


try:
    while True:
        frames = pipe.wait_for_frames()

        # カラーと深度のフレームをアライメント
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        bgr_image = np.asanyarray(color_frame.get_data())
        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

        depth_data = np.asanyarray(depth_frame.get_data())

        # 赤色検出
        lower_red = np.array([0, 200, 130])
        upper_red = np.array([5, 255, 180])
        binary_image = cv2.inRange(hsv_image, lower_red, upper_red)

        contours, _ = cv2.findContours(
            binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        circle_image = bgr_image.copy()

        for cnt in contours:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)

            if radius > 30:
                cv2.circle(circle_image, center, radius, (0, 255, 0), 2)

                # 深度値を取得
                depth_in_meters = depth_frame.get_distance(center[0], center[1])

                # 深度が0でなければ（有効な深度が取得できれば）座標変換を実行
                if depth_in_meters > 0:
                    # ★★★ ピクセル座標と深度から3D座標へ変換 ★★★
                    point_3d = rs.rs2_deproject_pixel_to_point(
                        depth_intrinsics, [center[0], center[1]], depth_in_meters
                    )

                    # 結果を表示（メートル単位）
                    print(
                        f"Pixel: {center}, Radius: {radius}, 3D Point (X,Y,Z): {point_3d}"
                    )

        cv2.imshow("Enclosing Circles", circle_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    pipe.stop()
    cv2.destroyAllWindows()
