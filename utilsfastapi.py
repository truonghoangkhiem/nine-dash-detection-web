import torch
import cv2
from pathlib import Path
import os

def load_model(weights_path=r'C:/Users/khiem/Downloads/Nine-dashmodel/yolov5/runs/train/exp2/weights/best.pt'):
    """ Load trained YOLOv5 model """
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path, force_reload=True)
    model.conf = 0.4  # Confidence threshold
    return model

def predict_image_or_video(file_path: str, model, is_video=False):
    """ Predict on a single image or video based on the provided path """
    save_path = None
    if is_video:
        # Nếu là video, xử lý video từng frame
        cap = cv2.VideoCapture(file_path)
        frame_count = 0  # Đếm số frame đã xử lý
        object_detected = False  # Biến kiểm tra nếu đối tượng đã được phát hiện

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Dự đoán trên từng frame
            results = model(frame)
            pred = results.xywh[0]  # Dự đoán trên frame, trả về [class, x, y, w, h, confidence]

            # Kiểm tra xem có đối tượng nào được phát hiện không (confidence > 0)
            if len(pred) > 0:
                # Nếu có đối tượng, hiển thị kết quả và dừng
                results.show()
                object_detected = True  # Đánh dấu rằng đối tượng đã được phát hiện

                # Lưu kết quả cho frame đầu tiên có đối tượng
                output_path = Path(r"C:/Users/khiem/Downloads/Nine-dashmodel/detections")
                output_path.mkdir(parents=True, exist_ok=True)
                save_path = output_path / f"frame_{frame_count:04d}_detected_{os.path.basename(file_path).replace('.mp4', '')}.jpg"
                
                # Save the image manually
                cv2.imwrite(str(save_path), frame)  # Save the frame as an image

                print(f"Image saved at {save_path}")  # Không cần kiểm tra sự tồn tại vì cv2.imwrite sẽ tự động kiểm tra

                # Dừng video sau khi phát hiện đối tượng
                print(f"Object detected in video at frame {frame_count}")
                break  # Dừng việc xử lý video sau khi phát hiện đối tượng

            frame_count += 1

        cap.release()

        # Nếu không phát hiện đối tượng, in thông báo
        if not object_detected:
            print("No objects detected in video.")

    else:
        # Nếu là ảnh, dự đoán trên ảnh
        results = model(file_path)  # Dự đoán trên ảnh
        pred = results.xywh[0]  # Dự đoán trên ảnh, trả về [class, x, y, w, h, confidence]

        # Kiểm tra xem có đối tượng nào được phát hiện không
        if len(pred) > 0:
            results.show()  # Hiển thị ảnh với kết quả dự đoán
            output_path = Path(r"C:/Users/khiem/Downloads/Nine-dashmodel/detections")
            output_path.mkdir(parents=True, exist_ok=True)
            save_path = output_path / f"detected_{os.path.basename(file_path)}"

            # Save the image manually
            cv2.imwrite(str(save_path), frame)  # Save the frame as an image

            print(f"Image saved at {save_path}")

        else:
            print(f"No objects detected in image: {file_path}")

    print(f"Prediction completed for {file_path}")
    if save_path is None:
        print(f"No objects detected, no file to save.")
        return {"error": "No objects detected."}
    return save_path
