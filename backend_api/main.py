from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
import shutil
import os
from utilsfastapi import load_model, predict_image_or_video
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = '*'  # Cho phép tất cả các nguồn
    return response
@app.get("/")
async def root():
    return {"message": "Hello World"}
# Route upload ảnh hoặc video và trả về kết quả
@app.post("/predictions")
async def predict(file: UploadFile = File(...)):
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
    prediction_result = predict_image_or_video(file_location, model, is_video)
    if isinstance(prediction_result, dict):  # Kiểm tra có đổi tượng không
            return {"message": "No objects detected."}  
    # Lấy tên file của ảnh đã lưu
    result_id = os.path.basename(prediction_result).replace('.jpg', '')
    # Trả kết quả cho người dùng
    return {"result_id": result_id}

@app.get("/results/{result_id}")
async def get_result(result_id: str):
    """
    Trả về ảnh đã xử lý từ ID.
    """
    result_path = f"C:/Users/khiem/Downloads/Nine-dashmodel/detections/{result_id}.jpg" #Đường dẫn lưu ảnh
    if os.path.exists(result_path):
        # Trả về ảnh dưới dạng streaming
        return StreamingResponse(open(result_path, "rb"), media_type="image/jpeg")
    else:
        return {"error": "Result not found"}  # Trả về thông báo lỗi nếu không tìm thấy ảnh

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Chỉ cho phép frontend từ cổng này
    allow_credentials=True,
    allow_methods=["*"],  # Chấp nhận tất cả HTTP methods
    allow_headers=["*"],  # Chấp nhận tất cả headers
)
