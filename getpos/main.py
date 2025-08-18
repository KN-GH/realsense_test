import realsense_reader as rsr
import obj_tracker_by_color as tracker
import qr_finder as qr
import pyrealsense2 as rs
import numpy as np
import cv2

red_tracker = tracker.ObjTrackerByColorClass(0, 150, 100, 5, 255, 255)
qr__ = qr.QRFinderClass()
realsense = rsr.RealsenseClass(1280, 720)
realsense.start_camera()
try:
    while True:
        realsense.get_frame()
        bgr_image = realsense.get_color_img()
        hsv_image = realsense.get_color_img(hsv_flag=1)
        depth_frame = realsense.get_depth_flame()
        circle_image = bgr_image.copy()
        for x, y, radius in red_tracker.detect(hsv_image):
            if radius > 30:
                cv2.circle(circle_image, (x, y), radius, (0, 255, 0), 2)

                point_3d = realsense.get_coord(x, y, depth_frame)
                # print(
                #     f"Pixel: {(x, y)}, Radius: {radius}, 3D Point (X,Y,Z): {point_3d}"
                # )
                print(qr__.get_coord(bgr_image))

        cv2.imshow("Enclosing Circles", circle_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    realsense.stop_camera()
    cv2.destroyAllWindows()


