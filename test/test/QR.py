import cv2
import pyrealsense2 as rs
import numpy as np

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

# アライメントを設定（カラー画像と深度画像の位置を合わせる）
align_to = rs.stream.color
align = rs.align(align_to)

# ★★★ 変換に必要なカメラの内部パラメータを取得 ★★★
depth_intrinsics = (
    profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()
)

### QRコード検出器のインスタンスを作成 (ループの外で一度だけ)
qcd = cv2.QRCodeDetectorAruco()
image = cv2.imread("./../../getpos/QR/QR.png")

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

        ### QRコードの検出とデコード
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(bgr_image)
        print(points)
        ### ↓↓↓ここからが追加・変更部分↓↓↓

        # QRコードが1つ以上検出された場合 (retvalがTrueになる)
        if retval:
            # 検出された全てのQRコードに対してループ処理
            for i, pts in enumerate(points):
                # 頂点座標を整数の配列に変換
                qr_points = pts.astype(np.int32)
                
                # cv2.polylines() を使ってQRコードを囲む四角形を描画
                # 引数: (描画対象画像, [頂点座標の配列], 閉じた線か, 色, 太さ)
                cv2.polylines(bgr_image, [qr_points], isClosed=True, color=(0, 255, 0), thickness=3)

                # (任意) デコードされた情報をQRコードの近くに表示
                if decoded_info[i]:
                    # 情報を描画する位置をQRコードの左上の頂点に設定
                    text_position = tuple(qr_points[0])
                    cv2.putText(
                        bgr_image,
                        decoded_info[i],
                        text_position,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255), # 赤色
                        2,
                        cv2.LINE_AA
                    )

        ### ↑↑↑追加・変更部分ここまで↑↑↑
        
        # 結果の画像を表示 (ウィンドウ名を変更)
        cv2.imshow("QR Code Detection", bgr_image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    pipe.stop()
    cv2.destroyAllWindows()