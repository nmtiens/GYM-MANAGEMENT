from fastapi import FastAPI, HTTPException, Body
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import List
import re
from utils.camera import capture_image_from_camera
from utils.face import get_face_embedding
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Chỉ cho phép frontend truy cập
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Cho phép tất cả các headers
)

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["gym_management"]

# API Đăng ký Hội Viên
@app.post("/dangky_hoivien/")
async def dang_ky_hoi_vien(
    hoTen: str = Body(...),
    ngaySinh: str = Body(...),
    gioiTinh: str = Body(...),
    diaChi: str = Body(...),
    soDienThoai: str = Body(...),
    email: str = Body(...),
    nhanVienTao: str = Body(...),
    huanLuyenVien: str = Body(...),
    goiTap: str = Body(...),
    dichVu: List[str] = Body(...),
    luuKhuonMat: bool = Body(True)  # Thêm tham số để bật/tắt lưu khuôn mặt
):
    # Kiểm tra email & số điện thoại hợp lệ
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise HTTPException(status_code=400, detail="Email không hợp lệ!")
    if len(soDienThoai) != 10 or not soDienThoai.isdigit():
        raise HTTPException(status_code=400, detail="Số điện thoại không hợp lệ!")

    # Kiểm tra xem email hoặc số điện thoại đã tồn tại chưa
    if db.HoiVien.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email này đã được đăng ký!")
    if db.HoiVien.find_one({"so_dien_thoai": soDienThoai}):
        raise HTTPException(status_code=400, detail="Số điện thoại này đã được đăng ký!")

    # Xử lý dữ liệu khuôn mặt nếu `luuKhuonMat` = True
    face_images = []
    if luuKhuonMat:
        for _ in range(7):  # Chụp 7 ảnh khuôn mặt
            face_image = capture_image_from_camera()
            if face_image is None:
                raise HTTPException(status_code=500, detail="Không thể chụp ảnh khuôn mặt!")
            
            face_embedding = get_face_embedding(face_image)
            if face_embedding is None:
                raise HTTPException(status_code=500, detail="Không thể trích xuất dữ liệu khuôn mặt!")
            
            face_images.append(face_embedding)

        if not face_images:
            raise HTTPException(status_code=500, detail="Không thu thập được dữ liệu khuôn mặt!")

    # Tạo mã hội viên và thẻ hội viên
    ma_hoi_vien = "HV" + datetime.now().strftime("%y%m%d%H%M%S")
    id_the_hoi_vien = "THE" + datetime.now().strftime("%y%m%d%H%M%S")

    # Lưu hội viên vào MongoDB
    hoi_vien = {
        "ma_hoi_vien": ma_hoi_vien,
        "ho_ten": hoTen,
        "email": email,
        "so_dien_thoai": soDienThoai,
        "ngay_sinh": ngaySinh,
        "gioi_tinh": gioiTinh,
        "dia_chi": diaChi,
        "ngay_tham_gia": datetime.now(),
        "du_lieu_khuon_mat": face_images if luuKhuonMat else None,  # Lưu hoặc bỏ qua khuôn mặt
        "so_lan_dang_nhap": 0,
        "id_the_hoi_vien": id_the_hoi_vien
    }

    hoi_vien_id = db.HoiVien.insert_one(hoi_vien).inserted_id

    # Lưu thẻ hội viên
    the_hoi_vien = {
        "ma_the": id_the_hoi_vien,
        "id_hoi_vien": ObjectId(hoi_vien_id),
        "id_nhan_vien_tao": ObjectId(nhanVienTao),
        "id_hlv_huong_dan": ObjectId(huanLuyenVien),
        "id_goi_tap": ObjectId(goiTap),
        "dich_vu_da_dang_ky": [ObjectId(dv) for dv in dichVu],
        "ngay_bat_dau": datetime.now(),
        "ngay_het_han": datetime(2025, 6, 30),
        "trang_thai": "Hoạt động"
    }

    db.TheHoiVien.insert_one(the_hoi_vien)

    return {
        "message": "Đăng ký hội viên thành công!",
        "hoiVien_id": str(hoi_vien_id),
        "ma_hoi_vien": ma_hoi_vien,
        "id_the_hoi_vien": id_the_hoi_vien
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
