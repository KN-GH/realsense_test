import realsense_reader as rsr
import obj_tracker_by_color as tracker
import qr_finder as qr
import point_converter as pc
import pyrealsense2 as rs
import numpy as np
import cv2

width = 1280
height = 720

red_tracker = tracker.ObjTrackerByColorClass(80, 100, 200, 110, 255, 255)
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
        for x, y, radius_in_pixel in red_tracker.detect(hsv_image):
            obj_point = realsense.get_point(x, y)
            if radius_in_pixel > 30 and obj_point[2] > 0:
                cv2.circle(circle_image, (x, y), radius_in_pixel, (0, 255, 0), 2)
                radius = realsense.get_length_from_px(obj_point[2], radius_in_pixel)
                obj_point_from_origin = converter.point_convert(obj_point[0], obj_point[1], obj_point[2], qr_point[0], qr_point[1], qr_point[2])
                print(
                    f"obj_point_from_origin: {obj_point_from_origin}, radius: {radius}"
                )

        cv2.imshow("Enclosing Circles", circle_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    realsense.stop_camera()
    cv2.destroyAllWindows()


