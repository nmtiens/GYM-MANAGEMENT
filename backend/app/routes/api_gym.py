from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

# Tạo Blueprint
api_bp = Blueprint("api", __name__)

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["gym_management"]

# Các collection
nhanvien_collection = db["NhanVien"]
huanluyenvien_collection = db["HuanLuyenVien"]
goitap_collection = db["GoiTap"]
dichvu_collection = db["DichVu"]
thehoivien_collection = db["TheHoiVien"]

# Helper function to convert ObjectId to string for response
def serialize_object(obj):
    obj["_id"] = str(obj["_id"])
    return obj

# API Nhân viên
@api_bp.route("/nhanvien/", methods=["GET"])
def get_nhanvien():
    nhanvien = nhanvien_collection.find()
    return jsonify([serialize_object(nv) for nv in nhanvien])

@api_bp.route("/nhanvien/", methods=["POST"])
def create_nhanvien():
    data = request.json
    nhanvien_collection.insert_one(data)
    return jsonify({"message": "Nhân viên đã được thêm."}), 201

@api_bp.route("/nhanvien/<id>", methods=["PUT"])
def update_nhanvien(id):
    data = request.json
    nhanvien_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Nhân viên đã được cập nhật."})

@api_bp.route("/nhanvien/<id>", methods=["DELETE"])
def delete_nhanvien(id):
    nhanvien_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Nhân viên đã được xóa."})


# API Gói tập
@api_bp.route("/goitap/", methods=["GET"])
def get_goitap():
    goitap = goitap_collection.find()
    return jsonify([serialize_object(gt) for gt in goitap])

@api_bp.route("/goitap/", methods=["POST"])
def create_goitap():
    data = request.json
    goitap_collection.insert_one(data)
    return jsonify({"message": "Gói tập đã được thêm."}), 201

@api_bp.route("/goitap/<id>", methods=["PUT"])
def update_goitap(id):
    data = request.json
    goitap_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Gói tập đã được cập nhật."})

@api_bp.route("/goitap/<id>", methods=["DELETE"])
def delete_goitap(id):
    goitap_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Gói tập đã được xóa."})

# API Dịch vụ
@api_bp.route("/dichvu/", methods=["GET"])
def get_dichvu():
    dichvu = dichvu_collection.find()
    return jsonify([serialize_object(dv) for dv in dichvu])

@api_bp.route("/dichvu/", methods=["POST"])
def create_dichvu():
    data = request.json
    dichvu_collection.insert_one(data)
    return jsonify({"message": "Dịch vụ đã được thêm."}), 201

@api_bp.route("/dichvu/<id>", methods=["PUT"])
def update_dichvu(id):
    data = request.json
    dichvu_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Dịch vụ đã được cập nhật."})

@api_bp.route("/dichvu/<id>", methods=["DELETE"])
def delete_dichvu(id):
    dichvu_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Dịch vụ đã được xóa."})

# API Thẻ hội viên
@api_bp.route("/thehoivien/", methods=["GET"])
def get_thehoi_vien():
    thehoi_vien = thehoivien_collection.find()
    result = [serialize_object(thv) for thv in thehoi_vien]  # Chuyển đổi tất cả các ObjectId
    return jsonify(result)
 
@api_bp.route('/thehoivien/<maHoiVien>', methods=['GET'])
def get_member_card(maHoiVien):
    the_hoi_vien = thehoivien_collection.find_one({"maHoiVien": maHoiVien})
    if the_hoi_vien:
        the_hoi_vien["_id"] = str(the_hoi_vien["_id"])  # Chuyển ObjectId về string
        return jsonify({"memberCard": the_hoi_vien})
    else:
        return jsonify({"error": "Không tìm thấy thẻ hội viên"}), 404

@api_bp.route("/thehoivien/", methods=["POST"])
def create_thehoi_vien():
    data = request.json
    thehoivien_collection.insert_one(data)
    return jsonify({"message": "Thẻ hội viên đã được thêm."}), 201

@api_bp.route("/thehoivien/<id>", methods=["PUT"])
def update_thehoi_vien(id):
    data = request.json

    # Đảm bảo không cập nhật trường _id
    if "_id" in data:
        del data["_id"]

    # Kiểm tra nếu "dichVu" là danh sách, cập nhật phù hợp
    if "dichVu" in data and isinstance(data["dichVu"], list):
        data["dichVu"] = list(data["dichVu"])  # Chuyển thành danh sách nếu cần

    # Thực hiện cập nhật
    result = thehoivien_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    
    if result.modified_count == 0:
        return jsonify({"message": "Không có thay đổi nào được thực hiện."}), 400

    return jsonify({"message": "Thẻ hội viên đã được cập nhật."})


@api_bp.route("/thehoivien/<id>", methods=["DELETE"])
def delete_thehoi_vien(id):
    thehoivien_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Thẻ hội viên đã được xóa."})
