import cv2
import numpy as np

class ObjTrackerByColor:
    def __init__(self, lower1, lower2, lower3, upper1, upper2, upper3):
        self._lower = np.array([lower1, lower2, lower3])
        self._upper = np.array([upper1, upper2, upper3])
    
    def detect(self, image):
        binary_image = cv2.inRange(image, self._lower, self._upper)
        contours, _ = cv2.findContours(
            binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for cnt in contours:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            yield int(x), int(y), int(radius)