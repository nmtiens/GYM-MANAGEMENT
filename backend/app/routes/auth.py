from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from utils.camera import capture_image_from_camera
from utils.face import get_face_embedding
from utils.face import compare_face_embeddings
from utils.face import encode_image_to_base64
from database import hoi_vien_collection
from database import the_hoi_vien_collection# Make sure you reference the correct collection
from database import db
import logging
import time
from utils.sound import play_sound
from bson import ObjectId
from datetime import datetime


auth_bp = Blueprint("auth", __name__)


def serialize_object(obj):
    obj["_id"] = str(obj["_id"])
    return obj


@auth_bp.route('/api/count/<collection_name>', methods=['GET'])
def count_documents(collection_name):
    count = db[collection_name].count_documents({})
    return jsonify({"count": count})




@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        logging.info(f"Data received: {data}")

        # Validate required fields
        required_fields = ['hoTen', 'ngaySinh', 'gioiTinh', 'nhanVienTao', 
                           'huanLuyenVien', 'goiTap', 'soLuong', 'donVi', 'luuKhuonMat']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Extract the data
        hoTen = data['hoTen']
        ngaySinh = data['ngaySinh']
        gioiTinh = data['gioiTinh']
        diaChi = data.get('diaChi', '')
        soDienThoai = data.get('soDienThoai', '')
        email = data.get('email', '')
        nhanVienTao = data['nhanVienTao']
        huanLuyenVien = data['huanLuyenVien']
        goiTap = data['goiTap']
        soLuong = int(data['soLuong'])
        donVi = data['donVi']
        dichVu = data.get('dichVu', '')
        luuKhuonMat = data['luuKhuonMat']

        if donVi == 'Ngày':
            soNgayConLai = soLuong
        elif donVi == 'Tháng':
            soNgayConLai = soLuong * 30
        elif donVi == 'Năm':
            soNgayConLai = soLuong * 365
        else:
            return jsonify({"error": "Đơn vị không hợp lệ!"}), 400

        # Capture face embeddings and images if luuKhuonMat is True
        face_images = []
        face_image_data = []
        if luuKhuonMat:
            for _ in range(7):
                face_image = capture_image_from_camera()
                face_embedding = get_face_embedding(face_image)
                if face_embedding:
                    face_images.append(face_embedding)
                    face_image_data.append(encode_image_to_base64(face_image))

                time.sleep(0.5)
            if not face_images:
                return jsonify({"error": "Face capture failed. Try again in better lighting."}), 400

        # Create member and card codes
        maHoiVien = "HV" + datetime.now().strftime("%y%m%d%H%M%S")
        maTheHoiVien = "THE" + datetime.now().strftime("%y%m%d%H%M%S")

        # Save user data
        user_data = {
            "MaHoiVien": maHoiVien,
            "HoTen": hoTen,
            "NgaySinh": ngaySinh,
            "GioiTinh": gioiTinh,
            "DiaChi": diaChi,
            "SDT": soDienThoai,
            "Email": email,
            "Face_Embeddings": face_images,
            "MaTheHoiVien": maTheHoiVien,

        }
        hoi_vien_collection.insert_one(user_data)

        # Calculate expiration date
        now = datetime.utcnow()
        expiration_date = now + timedelta(days=soNgayConLai)

        # Create member card data
        the_hoi_vien_data = {
            "MaTheHoiVien": maTheHoiVien,
            "MaHoiVien": maHoiVien,
            "HoiVien": hoTen,
            "NhanVien": nhanVienTao,
            "HuanLuyenVien": huanLuyenVien,
            "GoiTap": goiTap,
            "DichVu": dichVu,
            "SoNgayConLai": soNgayConLai,
            "NgayTao": now,
            "NgayHetHan": expiration_date,
            "Face_Images": face_image_data
        }
        the_hoi_vien_collection.insert_one(the_hoi_vien_data)

        logging.info(f"User {hoTen} registered successfully and member card created.")
        return jsonify({"message": "Đã đăng ký hội viên thành công và thẻ hội viên cũng đã được tạo!!!"}), 201

    except Exception as e:
        logging.error(f"Registration error: {str(e)}")
        return jsonify({"error": f"Registration failed: {str(e)}"}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Chụp ảnh khuôn mặt từ camera
        input_face_image = capture_image_from_camera()
        input_embedding = get_face_embedding(input_face_image)

        if input_embedding is None:
            play_sound("Error.mp3")
            return jsonify({"error": "Face detection failed. Try again."}), 400

        # Lấy tất cả hội viên có Face_Embeddings
        users = hoi_vien_collection.find({"Face_Embeddings": {"$exists": True, "$ne": []}})
        today = datetime.now()
        today_date = today.date()
        today_str = today_date.strftime("%Y-%m-%d")
        
        # Thêm giờ phút giây cho lịch sử đăng nhập chi tiết
        login_timestamp = today.strftime("%Y-%m-%d %H:%M:%S")

        for user in users:
            for stored_embedding in user['Face_Embeddings']:
                if compare_face_embeddings(input_embedding, stored_embedding):
                    ma_hoi_vien = user.get("MaHoiVien")

                    # Tìm thẻ hội viên
                    the_hoi_vien = the_hoi_vien_collection.find_one({"MaHoiVien": ma_hoi_vien})
                    soNgayConLai = the_hoi_vien.get("SoNgayConLai", 0) if the_hoi_vien else 0
                    last_login_date = the_hoi_vien.get("Last_Login_Date")

                    # Kiểm tra xem đã đăng nhập hôm nay chưa
                    already_logged_in_today = False
                    if last_login_date:
                        try:
                            last_login = datetime.strptime(last_login_date, "%Y-%m-%d").date()
                            already_logged_in_today = (last_login == today_date)
                        except ValueError:
                            already_logged_in_today = False

                    # Chuẩn bị cập nhật cho Login_History
                    update_data = {}
                    
                    # Thêm vào mảng Login_History
                    # $push: thêm phần tử vào mảng
                    update_operations = {
                        "$push": {"Login_History": login_timestamp}
                    }
                    
                    # Nếu chưa đăng nhập hôm nay, giảm số ngày còn lại
                    if not already_logged_in_today:
                        new_expiration = max(soNgayConLai - 1, 0)
                        update_operations["$set"] = {
                            "SoNgayConLai": new_expiration,
                            "Last_Login_Date": today_str  # Vẫn cập nhật Last_Login_Date
                        }
                    
                    # Cập nhật thẻ hội viên
                    the_hoi_vien_collection.update_one(
                        {"MaHoiVien": ma_hoi_vien},
                        update_operations
                    )

                    # Phát âm thanh tương ứng
                    if already_logged_in_today:
                        play_sound("Goodbye.mp3")
                    else:
                        play_sound("Welcome.mp3")

                    return jsonify({
                        "MaHoiVien": ma_hoi_vien,
                        "Original_Expiration_Date": soNgayConLai,
                        "Already_Logged_In_Today": already_logged_in_today
                    }), 200
        play_sound("Error.mp3")  # Thêm dòng này ngay trước khi return
        return jsonify({"error": "Face not recognized."}), 401
      


    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        play_sound("Error.mp3")  # Thêm dòng này trước khi return
        return jsonify({"error": f"Login failed: {str(e)}"}), 400



# API xem tất cả hội viên
@auth_bp.route("/", methods=["GET"])
def get_hoivien():
    hoivien = hoi_vien_collection.find()
    return jsonify([serialize_object(hv) for hv in hoivien])

# API xem chi tiết hội viên theo ID
@auth_bp.route("/<ma_hoi_vien>", methods=["GET"])
def get_hoivien_by_ma_hoi_vien(ma_hoi_vien):
    hv = hoi_vien_collection.find_one({"MaHoiVien": ma_hoi_vien})
    
    if not hv:
        return jsonify({"error": "Không tìm thấy hội viên"}), 404
    
    return jsonify(serialize_object(hv))

@auth_bp.route('/<id>', methods=['PUT'])
def update_hoivien(id):
    data = request.json
    try:
        # Xóa _id khỏi data để tránh cập nhật nó
        if '_id' in data:
            del data['_id']
        
        result = hoi_vien_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        
        if result.matched_count == 0:
            return jsonify({"error": "Hội viên không tồn tại"}), 404
        
        return jsonify({"message": "Cập nhật hội viên thành công"}), 200
    except Exception as e:
        print(f"Lỗi server: {e}")
        return jsonify({"error": "Lỗi server"}), 500
# API xóa hội viên
@auth_bp.route("/<id>", methods=["DELETE"])
def delete_hoivien(id): 
    result = hoi_vien_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Không tìm thấy hội viên"}), 404
    return jsonify({"message": "Đã xóa hội viên thành công"})
