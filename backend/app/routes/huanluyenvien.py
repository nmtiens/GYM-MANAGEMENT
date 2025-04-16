import os
import shutil
import random
from flask import request, jsonify, Blueprint
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS
from werkzeug.utils import secure_filename
from database import huan_luyen_vien_collection

# Khởi tạo Blueprint và CORS
api_hlv = Blueprint("huanluyenvien", __name__, url_prefix="/huanluyenvien")

# Thư mục chính để lưu ảnh
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Chuyển ObjectId thành string
def serialize_object(obj):
    obj["_id"] = str(obj["_id"])
    return obj

# Hàm tạo mã HLV tự động
def generate_ma_hlv():
    while True:
        maHLV = f"MaHLV{random.randint(1000, 9999)}"
        if not huan_luyen_vien_collection.find_one({"MaHLV": maHLV}):
            return maHLV

# Tạo thư mục lưu ảnh theo tên Huấn Luyện Viên
def create_folder(folder_name):
    folder_path = os.path.join(UPLOAD_FOLDER, secure_filename(folder_name))
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

# API thêm Huấn Luyện Viên + nhiều ảnh
@api_hlv.route("/", methods=["POST"])
def add_huan_luyen_vien():
    data = request.form
    files = request.files.getlist("Anh")

    # Kiểm tra các trường bắt buộc
    required_fields = ["HoTen", "NgaySinh", "GioiTinh", "SDT", "DiaChi", "KinhNghiem", "MoTa"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Thiếu dữ liệu"}), 400

    # Tạo mã HLV
    maHLV = generate_ma_hlv()

    # Tạo thư mục theo HoTen
    ho_ten = data["HoTen"]
    folder_path = create_folder(ho_ten)

    # Lưu nhiều ảnh
    anh_urls = []
    for file in files:
        if file and file.filename:
            filename = f"{maHLV}_{secure_filename(file.filename)}"
            file_path = os.path.join(folder_path, filename)

            # Tránh ghi đè file
            counter = 1
            while os.path.exists(file_path):
                filename = f"{maHLV}_{counter}_{secure_filename(file.filename)}"
                file_path = os.path.join(folder_path, filename)
                counter += 1

            file.save(file_path)
            anh_urls.append(f"/{folder_path}/{filename}")

    # Thêm HLV vào DB
    new_hlv = {
        "MaHLV": maHLV,
        "HoTen": ho_ten,
        "NgaySinh": data["NgaySinh"],
        "GioiTinh": data["GioiTinh"],
        "SDT": data["SDT"],
        "DiaChi": data["DiaChi"],
        "KinhNghiem": data["KinhNghiem"],
        "MoTa": data["MoTa"],
        "Anh": anh_urls
    }

    result = huan_luyen_vien_collection.insert_one(new_hlv)
    if not result.inserted_id:
        return jsonify({"error": "Không thể thêm Huấn Luyện Viên"}), 500

    return jsonify({"message": "Thêm thành công", "id": str(result.inserted_id), "Anh": anh_urls}), 201

# API xem tất cả HLV
@api_hlv.route("/", methods=["GET"])
def get_huanluyenvien():
    huanluyenvien = huan_luyen_vien_collection.find()
    return jsonify([serialize_object(hlv) for hlv in huanluyenvien])

# API xem chi tiết HLV theo ID
@api_hlv.route("/<id>", methods=["GET"])
def get_huanluyenvien_by_id(id):
    hlv = huan_luyen_vien_collection.find_one({"_id": ObjectId(id)})
    if not hlv:
        return jsonify({"error": "Không tìm thấy HLV"}), 404
    return jsonify(serialize_object(hlv))

@api_hlv.route("/<id>", methods=["PUT"])
def update_huanluyenvien(id):
    data = request.form
    files = request.files.getlist("Anh")

    # Các trường cho phép cập nhật
    update_data = {}
    for field in ["HoTen", "NgaySinh", "GioiTinh", "SDT", "DiaChi", "KinhNghiem", "MoTa"]:
        if field in data:
            update_data[field] = data[field]

    # Lấy thông tin HLV hiện tại
    hlv = huan_luyen_vien_collection.find_one({"_id": ObjectId(id)})
    if not hlv:
        return jsonify({"error": "HLV không tồn tại"}), 404

    # Xử lý thư mục ảnh
    old_folder = os.path.join(UPLOAD_FOLDER, secure_filename(hlv["HoTen"]))
    new_folder = old_folder

    # Nếu đổi tên HLV, đổi tên thư mục ảnh
    if "HoTen" in data and data["HoTen"] != hlv["HoTen"]:
        new_folder = os.path.join(UPLOAD_FOLDER, secure_filename(data["HoTen"]))
        if os.path.exists(old_folder):
            os.rename(old_folder, new_folder)
        elif not os.path.exists(new_folder):
            os.makedirs(new_folder)

    # Xóa ảnh cũ nếu có ảnh mới
    anh_urls = hlv.get("Anh", [])
    if files:
        # Xóa tất cả ảnh cũ
        for old_image in anh_urls:
            old_image_path = old_image.lstrip("/")
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        # Lưu ảnh mới
        anh_urls = []
        for file in files:
            if file and file.filename:
                filename = f"{id}_{secure_filename(file.filename)}"
                file_path = os.path.join(new_folder, filename)

                # Đảm bảo không ghi đè ảnh trùng tên
                counter = 1
                while os.path.exists(file_path):
                    filename = f"{id}_{counter}_{secure_filename(file.filename)}"
                    file_path = os.path.join(new_folder, filename)
                    counter += 1

                file.save(file_path)
                anh_urls.append(f"/{new_folder}/{filename}")

    # Cập nhật dữ liệu HLV
    update_data["Anh"] = anh_urls

    result = huan_luyen_vien_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": update_data}
    )

    if result.modified_count == 0:
        return jsonify({"message": "Không có thay đổi nào được thực hiện."}), 400

    return jsonify({"message": "Cập nhật thành công", "Anh": anh_urls})

# API xóa HLV (Xóa cả thư mục ảnh)
@api_hlv.route("/<id>", methods=["DELETE"])
def delete_huanluyenvien(id):
    hlv = huan_luyen_vien_collection.find_one({"_id": ObjectId(id)})
    if not hlv:
        return jsonify({"error": "Huấn Luyện Viên không tồn tại"}), 404

    # Xóa thư mục ảnh
    folder_path = os.path.join(UPLOAD_FOLDER, secure_filename(hlv["HoTen"]))
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    # Xóa dữ liệu trong DB
    result = huan_luyen_vien_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Không thể xóa HLV"}), 500

    return jsonify({"message": "Xóa thành công"}), 200
