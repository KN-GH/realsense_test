import cv2 
import numpy as np

class QRFinderClass:
    def __init__(self):
        self._qcd = cv2.QRCodeDetectorAruco()

    def get_pixel(self, bgr_image):
        retval, _, points, _ = self._qcd.detectAndDecodeMulti(bgr_image)
        if retval:
            center = np.mean(points[0], axis=0)
            cx = int(center[0])
            cy = int(center[1])
            return cx, cy
