# /backend/routes/uploads.py
from flask import Blueprint, send_from_directory
import os

uploads_bp = Blueprint('uploads', __name__)

# Trỏ đến thư mục uploads (cùng cấp với app)
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '../uploads'))

@uploads_bp.route('/uploads/<path:filename>')
def serve_file(filename):
    print("Serving file from:", os.path.join(UPLOAD_FOLDER, filename))
    return send_from_directory(UPLOAD_FOLDER, filename)
