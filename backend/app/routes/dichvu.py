from flask import request, jsonify, Blueprint
from pymongo import MongoClient
import random
from database import dich_vu_collection
from bson import ObjectId
from flask_cors import CORS

api_dichvu = Blueprint("dichvu", __name__, url_prefix="/dichvu")
CORS(api_dichvu)

def serialize_object(obj):
    obj["_id"] = str(obj["_id"])
    return obj

# Hàm tạo mã dịch vụ tự động
def generate_ma_dichvu():
    while True:
        maDV = f"MaDV{random.randint(1000, 9999)}"
        if not dich_vu_collection.find_one({"MaDV": maDV}):
            return maDV

# API thêm Dịch Vụ
@api_dichvu.route("/", methods=["POST"])
def add_dich_vu():
    data = request.json
    print("Dữ liệu nhận được:", data) 
    required_fields = ["TenDichVu", "MoTa", "Gia"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Thiếu dữ liệu"}), 400

    new_dv = {
        "MaDV": generate_ma_dichvu(),
        "TenDichVu": data["TenDichVu"],
        "MoTa": data["MoTa"],
        "Gia": data["Gia"],
        "TrangThai": data["TrangThai"]
    }

    result = dich_vu_collection.insert_one(new_dv)
    if not result.inserted_id:
        return jsonify({"error": "Không thể thêm Dịch Vụ"}), 500

    return jsonify({"message": "Thêm thành công", "id": str(result.inserted_id)}), 201

@api_dichvu.route("/", methods=["GET"])
def get_dichvu():
    dichvu = dich_vu_collection.find()
    return jsonify([serialize_object(dv) for dv in dichvu])

@api_dichvu.route("/<id>", methods=["GET"])
def get_dich_vu(id):
    try:
        object_id = ObjectId(id)
        dv = dich_vu_collection.find_one({"_id": object_id})
    except:
        dv = dich_vu_collection.find_one({"MaDV": id}, {"_id": 0})

    if not dv:
        return jsonify({"error": "Dịch Vụ không tồn tại"}), 404

    if "_id" in dv:
        dv["_id"] = str(dv["_id"])

    return jsonify(dv), 200

@api_dichvu.route("/<id>", methods=["PUT"])
def update_dichvu(id):
    data = request.json
    if "_id" in data:
        del data["_id"]

    result = dich_vu_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    
    if result.modified_count == 0:
        return jsonify({"message": "Không có thay đổi nào được thực hiện."}), 400

    return jsonify({"message": "Dịch vụ đã được cập nhật."})

@api_dichvu.route("/<id>", methods=["DELETE"])
def delete_dichvu(id):
    dich_vu_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Dịch vụ đã được xóa."})
