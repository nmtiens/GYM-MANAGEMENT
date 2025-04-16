from flask import request, jsonify, Blueprint
from pymongo import MongoClient
import random
from database import nhan_vien_collection
from bson import ObjectId
from flask_cors import CORS

api_nhanvien = Blueprint("nhanvien", __name__, url_prefix="/nhanvien")
CORS(api_nhanvien)

def serialize_object(obj):
    obj["_id"] = str(obj["_id"])
    return obj

# Hàm tạo mã nhân viên tự động
def generate_ma_nhanvien():
    while True:
        maNV = f"MaNV{random.randint(1000, 9999)}"
        if not nhan_vien_collection.find_one({"MaNV": maNV}):
            return maNV

# API thêm Nhân Viên
@api_nhanvien.route("/", methods=["POST"])
def add_nhan_vien():
    data = request.json

    required_fields = ["HoTen", "NgaySinh", "GioiTinh", "SDT", "DiaChi", "ChucVu", "Luong"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Thiếu dữ liệu"}), 400

    new_nv = {
        "MaNV": generate_ma_nhanvien(),
        "HoTen": data["HoTen"],
        "NgaySinh": data["NgaySinh"],
        "GioiTinh": data["GioiTinh"],
        "SDT": data["SDT"],
        "DiaChi": data["DiaChi"],
        "ChucVu": data["ChucVu"],
        "Luong": data["Luong"]
    }

    result = nhan_vien_collection.insert_one(new_nv)
    if not result.inserted_id:
        return jsonify({"error": "Không thể thêm Nhân Viên"}), 500

    return jsonify({"message": "Thêm thành công", "id": str(result.inserted_id)}), 201

@api_nhanvien.route("/", methods=["GET"])
def get_nhanvien():
    nhanvien = nhan_vien_collection.find()
    return jsonify([serialize_object(nv) for nv in nhanvien])

@api_nhanvien.route("/<id>", methods=["GET"])
def get_nhan_vien(id):
    try:
        object_id = ObjectId(id)
        nv = nhan_vien_collection.find_one({"_id": object_id})
    except:
        nv = nhan_vien_collection.find_one({"MaNV": id}, {"_id": 0})

    if not nv:
        return jsonify({"error": "Nhân Viên không tồn tại"}), 404

    if "_id" in nv:
        nv["_id"] = str(nv["_id"])

    return jsonify(nv), 200

@api_nhanvien.route("/<id>", methods=["PUT"])
def update_nhanvien(id):
    data = request.json
    if "_id" in data:
        del data["_id"]

    result = nhan_vien_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    
    if result.modified_count == 0:
        return jsonify({"message": "Không có thay đổi nào được thực hiện."}), 400

    return jsonify({"message": "Nhân viên đã được cập nhật."})

@api_nhanvien.route("/<id>", methods=["DELETE"])
def delete_nhanvien(id):
    nhan_vien_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Nhân viên đã được xóa."})
