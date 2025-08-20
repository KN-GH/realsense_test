#TODO
class PointConverterClass:
    def __init__(self, qrx_from_origin, qry_from_origin, qrz_from_origin):
        self.qrx_from_origin = qrx_from_origin #原点から見たQRコードの相対位置のX座標
        self.qry_from_origin = qry_from_origin #原点から見たQRコードの相対位置のY座標
        self.qrz_from_origin = qrz_from_origin #原点から見たQRコードの相対位置のZ座標

    def point_convert(self, objx_from_cam, objy_from_cam, objz_from_cam, qrx_from_cam, qry_from_cam, qrz_from_cam):
        objx_from_origin = self.qrx_from_origin - qrx_from_cam + objx_from_cam
        objy_from_origin = self.qry_from_origin - qry_from_cam + objy_from_cam
        objz_from_origin = -(self.qrz_from_origin - qrz_from_cam + objz_from_cam)
        return objx_from_origin, objy_from_origin, objz_from_origin