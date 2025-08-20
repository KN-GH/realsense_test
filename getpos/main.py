import realsense_reader as rsr
import obj_tracker_by_color as tracker
import qr_finder as qr
import point_converter as pc
import pyrealsense2 as rs
import numpy as np
import cv2

red_tracker = tracker.ObjTrackerByColorClass(0, 200, 100, 5, 255, 200)
qr__ = qr.QRFinderClass()
converter = pc.PointConverterClass(0.05, 0.05, 0)
realsense = rsr.RealsenseClass(1280, 720)
realsense.start_camera()
qrx = None
qry = None
qr_point = None
try:
    while qrx == None or qry == None:
        realsense.get_frame()
        bgr_image = realsense.get_color_img()
        qr_pixel = qr__.get_pixel(bgr_image)
        if qr_pixel != None:
            qrx, qry = qr_pixel
    qr_point = realsense.get_point(qrx, qry)
    while True:
        realsense.get_frame()
        bgr_image = realsense.get_color_img()
        hsv_image = realsense.get_color_img(hsv_flag=1)
        circle_image = bgr_image.copy()
        for x, y, radius in red_tracker.detect(hsv_image):
            if radius > 30:
                cv2.circle(circle_image, (x, y), radius, (0, 255, 0), 2)
                obj_point = realsense.get_point(x, y)
                obj_point_from_origin = converter.point_convert(obj_point[0], obj_point[1], obj_point[2], qr_point[0], qr_point[1], qr_point[2])
                print(
                    f"obj_point_from_origin: {obj_point_from_origin}"
                )

        cv2.imshow("Enclosing Circles", circle_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    realsense.stop_camera()
    cv2.destroyAllWindows()


