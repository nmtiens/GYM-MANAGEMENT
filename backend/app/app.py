from flask import Flask
from flask_cors import CORS
import logging
from reset_thread import start_reset_thread
from routes.auth import auth_bp # type: ignore
from routes.chat_rasa import chat_bp # type: ignore
from routes.huanluyenvien import api_hlv # type: ignore
from routes.nhanvien import api_nhanvien    
from routes.dichvu import api_dichvu
from routes.goitap import api_goitap
from routes.thehoivien import api_thehoivien
from routes.uploads import uploads_bp
logging.basicConfig(level=logging.DEBUG)  # Bật debug log

app = Flask(__name__)

        
# Cấu hình CORS đúng cách
CORS(app, resources={r"/*": {"origins": "*"}})


# Đăng ký blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(api_hlv)
app.register_blueprint(api_dichvu)
app.register_blueprint(api_goitap)
app.register_blueprint(api_thehoivien)
app.register_blueprint(api_nhanvien)
app.register_blueprint(uploads_bp)
# Bắt đầu reset thread      
start_reset_thread()


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Đảm bảo cổng khớp với frontend
