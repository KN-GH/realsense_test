import pyrealsense2 as rs
import numpy as np
import cv2


class RealsenseClass:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._pipe = None
        self._config = None
        self._align = None
        self._depth_intrinsics = None
        self._color_frame = None
        self._depth_frame = None

    # 画像の取得を開始する
    def start_camera(self):
        self._pipe = rs.pipeline()
        self._config = rs.config()
        self._config.enable_stream(
            rs.stream.color, self._width, self._height, rs.format.bgr8, 30
        )
        self._config.enable_stream(
            rs.stream.depth, self._width, self._height, rs.format.z16, 30
        )
        profile = self._pipe.start(self._config)
        align_to = rs.stream.color
        self._align = rs.align(align_to)
        self._depth_intrinsics = (
            profile.get_stream(rs.stream.depth)
            .as_video_stream_profile()
            .get_intrinsics()
        )
    
    def stop_camera(self):
        self._pipe.stop()

    # データを更新する
    def get_frame(self):
        frames = self._pipe.wait_for_frames()
        aligned_frames = self._align.process(frames)
        self._depth_frame = aligned_frames.get_depth_frame()
        self._color_frame = aligned_frames.get_color_frame()
        if not self._depth_frame or not self._color_frame:
            pass  # TODO エラー処理

    # 画像データを持つnp配列を返す
    def get_color_img(self, hsv_flag=0):
        image = np.asanyarray(self._color_frame.get_data())
        if hsv_flag:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return image

    def get_depth_flame(self):
        return self._depth_frame

    # 画像上の座標から実世界座標を返す
    def get_point(self, x, y, depth_frame = None):
        if depth_frame == None:
            depth_frame = self._depth_frame
        depth_in_meters = depth_frame.get_distance(x, y)
        point_3d = rs.rs2_deproject_pixel_to_point(
            self._depth_intrinsics, [x, y], depth_in_meters
        )
        return point_3d