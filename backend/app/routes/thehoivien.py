from flask import request, jsonify, Blueprint
from pymongo import MongoClient
import random
from database import the_hoi_vien_collection
from bson import ObjectId
from flask_cors import CORS

api_thehoivien = Blueprint("thehoivien", __name__, url_prefix="/thehoivien")
CORS(api_thehoivien)

def serialize_object(obj):
    obj["_id"] = str(obj["_id"])
    return obj

@api_thehoivien.route("/", methods=["GET"])
def get_all_the_hoi_vien():
    cards = the_hoi_vien_collection.find()
    return jsonify([serialize_object(card) for card in cards])

@api_thehoivien.route('/member/<MaHoiVien>', methods=['GET'])
def get_member_card(MaHoiVien):
    the_hoi_vien = the_hoi_vien_collection.find_one({"MaHoiVien": MaHoiVien})
    if the_hoi_vien:
        the_hoi_vien["_id"] = str(the_hoi_vien["_id"])  # Chuyển ObjectId về string
        return jsonify(the_hoi_vien)
    else:
        return jsonify({"error": "Không tìm thấy thẻ hội viên"}), 404

@api_thehoivien.route("/id/<id>", methods=["GET"])
def get_the_hoi_vien(id):
    try:
        object_id = ObjectId(id)
        card = the_hoi_vien_collection.find_one({"_id": object_id})
    except:
        card = the_hoi_vien_collection.find_one({"MaThe": id}, {"_id": 0})

    if not card:
        return jsonify({"error": "Thẻ Hội Viên không tồn tại"}), 404

    if "_id" in card:
        card["_id"] = str(card["_id"])

    return jsonify(card), 200
@api_thehoivien.route("/<id>", methods=["PUT"])
def update_the_hoi_vien(id):
    data = request.json
    if "_id" in data:
        del data["_id"]

    result = the_hoi_vien_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    
    if result.modified_count == 0:
        return jsonify({"message": "Không có thay đổi nào được thực hiện."}), 400

    return jsonify({"message": "Thẻ Hội Viên đã được cập nhật."})

@api_thehoivien.route("/<id>", methods=["DELETE"])
def delete_the_hoi_vien(id):
    the_hoi_vien_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Thẻ Hội Viên đã được xóa."})
