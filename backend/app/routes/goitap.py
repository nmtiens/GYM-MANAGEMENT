from flask import request, jsonify, Blueprint
from pymongo import MongoClient
import random
from database import goi_tap_collection
from bson import ObjectId
from flask_cors import CORS

api_goitap = Blueprint("goitap", __name__, url_prefix="/goitap")
CORS(api_goitap)

def serialize_object(obj):
    obj["_id"] = str(obj["_id"])
    return obj

# Hàm tạo mã gói tập tự động
def generate_ma_goitap():
    while True:
        maGT = f"MaGT{random.randint(1000, 9999)}"
        if not goi_tap_collection.find_one({"MaGT": maGT}):
            return maGT

# API thêm Gói Tập
@api_goitap.route("/", methods=["POST"])
def add_goi_tap():
    data = request.json
    print("Dữ liệu nhận được:", data) 
    required_fields = ["TenGoiTap", "MoTa", "Gia"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Thiếu dữ liệu"}), 400

    new_gt = {
        "MaGT": generate_ma_goitap(),
        "TenGoiTap": data["TenGoiTap"],
        "MoTa": data["MoTa"],
        "Gia": data["Gia"],
        # Add QuyenLoi field, defaulting to empty list if not provided
        "QuyenLoi": data.get("QuyenLoi", [])
    }

    result = goi_tap_collection.insert_one(new_gt)
    if not result.inserted_id:
        return jsonify({"error": "Không thể thêm Gói Tập"}), 500

    # Convert ObjectId to string for JSON response
    new_gt['_id'] = str(result.inserted_id)
    
    return jsonify(new_gt), 201

@api_goitap.route("/", methods=["GET"])
def get_goitap():
    goitap = goi_tap_collection.find()
    return jsonify([serialize_object(gt) for gt in goitap])

@api_goitap.route("/<id>", methods=["GET"])
def get_goi_tap(id):
    try:
        object_id = ObjectId(id)
        gt = goi_tap_collection.find_one({"_id": object_id})
    except:
        gt = goi_tap_collection.find_one({"MaGT": id}, {"_id": 0})

    if not gt:
        return jsonify({"error": "Gói Tập không tồn tại"}), 404

    if "_id" in gt:
        gt["_id"] = str(gt["_id"])

    return jsonify(gt), 200

@api_goitap.route("/<id>", methods=["PUT"])
def update_goitap(id):
    data = request.json
    if "_id" in data:
        del data["_id"]

    result = goi_tap_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    
    if result.modified_count == 0:
        return jsonify({"message": "Không có thay đổi nào được thực hiện."}), 400

    return jsonify({"message": "Gói tập đã được cập nhật."})

@api_goitap.route("/<id>", methods=["DELETE"])
def delete_goitap(id):
    goi_tap_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Gói tập đã được xóa."})