from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# Kết nối đến MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["gym_management"]

from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# Kết nối đến MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["gym_management"]

from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# Kết nối đến MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["gym_management"]

# Collection thẻ hội viên
bang_the_hoi_vien = db["TheHoiVien"]

def tao_ma_the_hoi_vien():
    so_hien_tai = bang_the_hoi_vien.count_documents({}) + 1
    return f"THV{str(so_hien_tai).zfill(3)}"

ma_the_hoi_vien = tao_ma_the_hoi_vien()

# Thay thế các ID bằng mã tương ứng
ma_hoi_vien = "HV001"  # Example mã Hội viên
ma_nhan_vien_tao = "NV001"  # Example mã Nhân viên
ma_hlv_huong_dan = "HLV001"  # Example mã Huấn luyện viên
ma_goi_tap = "GT001"  # Example mã Gói tập

du_lieu_the_hoi_vien = {
    "ma_the_hoi_vien": ma_the_hoi_vien,
    "ma_hoi_vien": ma_hoi_vien,  # Mã hội viên
    "ma_nhan_vien_tao": ma_nhan_vien_tao,  # Mã nhân viên
    "ma_hlv_huong_dan": ma_hlv_huong_dan,  # Mã huấn luyện viên
    "ma_goi_tap": ma_goi_tap,  # Mã gói tập
    "dich_vu_da_dang_ky": ["DV001", "DV002"],  # Example dịch vụ
    "ngay_bat_dau": datetime(2023, 6, 1),
    "ngay_het_han": datetime(2024, 6, 1)
}

id_the_hoi_vien = bang_the_hoi_vien.insert_one(du_lieu_the_hoi_vien).inserted_id
print(f"Đã thêm thẻ hội viên với mã: {ma_the_hoi_vien}, ID: {id_the_hoi_vien}")
