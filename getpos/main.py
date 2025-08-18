import realsense_reader as rsr
import pyrealsense2 as rs
import numpy as np
import cv2

realsense = rsr.RealsenseClass(1280, 720)
realsense.start_camera()
try:
    while True:
        realsense.get_frame()
        bgr_image = realsense.get_color_img()
        hsv_image = realsense.get_color_img(hsv_flag=1)
        depth_frame = realsense.get_depth_flame()

        # 赤色検出
        lower_red = np.array([0, 150, 0])
        upper_red = np.array([5, 255, 255])
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

                point_3d = realsense.get_coord(center[0], center[1], depth_frame)
                print(
                    f"Pixel: {center}, Radius: {radius}, 3D Point (X,Y,Z): {point_3d}"
                )

        cv2.imshow("Enclosing Circles", circle_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    realsense.stop_camera()
    cv2.destroyAllWindows()


