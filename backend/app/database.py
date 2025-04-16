from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
hoi_vien_collection = db['HoiVien']
the_hoi_vien_collection = db['TheHoiVien']
huan_luyen_vien_collection = db['HuanLuyenVien']
nhan_vien_collection = db['NhanVien']
dich_vu_collection = db['DichVu']
goi_tap_collection = db['GoiTap']
def init_db():
    # Perform any necessary database initialization
    pass
