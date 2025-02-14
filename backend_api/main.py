from fastapi import FastAPI, File, Request, UploadFile, Form
from fastapi.responses import StreamingResponse
import shutil
import os
from utilsfastapi import load_model, predict_image_or_video
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cấu hình CORS middleware để cho phép frontend từ cổng 5500
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bạn có thể thay "*" bằng URL cụ thể nếu muốn hạn chế
    allow_credentials=True,
    allow_methods=["*"],  # Chấp nhận tất cả các phương thức HTTP
    allow_headers=["*"],  # Chấp nhận tất cả các header
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Route upload ảnh hoặc video và trả về ID kết quả
@app.post("/predictions")
async def predict(file: UploadFile = File(...), minConfidence: float = Form(...)):
    # Tạo tên file duy nhất để lưu ảnh hoặc video
    file_location = f"temp_{uuid.uuid4().hex}_{file.filename}"
    
    # Lưu file tạm thời
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Tải mô hình YOLOv5
    model = load_model()

    # Kiểm tra nếu file là video hoặc ảnh
    is_video = file.filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))

    # Dự đoán
    prediction_result = predict_image_or_video(file_location, model, is_video, minConfidence)
    if isinstance(prediction_result, dict):  # Kiểm tra có đối tượng không
            return {"message": "No objects detected."}  
    # Lấy tên file của ảnh đã lưu
    result_id = os.path.basename(prediction_result).replace('.jpg', '')
    # Trả kết quả cho người dùng
    return {"result_id": result_id}

# Route lấy ảnh đã xử lý từ ID
@app.get("/results/{result_id}")
async def get_result(result_id: str):
    """
    Trả về ảnh đã xử lý từ ID.
    """
    result_path = f"C:/Users/khiem/Downloads/Nine-dashmodel/detections/{result_id}.jpg" # Đường dẫn lưu ảnh
    if os.path.exists(result_path):
        # Trả về ảnh dưới dạng streaming
        return StreamingResponse(open(result_path, "rb"), media_type="image/jpeg")
    else:
        return {"error": "Result not found"}  # Trả về thông báo lỗi nếu không tìm thấy ảnh
