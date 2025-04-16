import cv2
import logging

# Khởi tạo biến toàn cục để lưu trạng thái camera
cap = cv2.VideoCapture(0)

# Kiểm tra xem camera có mở thành công không
if not cap.isOpened():
    raise RuntimeError("Cannot access the camera")
    
logging.debug("Camera initialized.")

def capture_image_from_camera():
    logging.debug("Capturing image. Please look at the camera.")
    ret, frame = cap.read()  # Lấy một frame từ camera
    if not ret:
        raise RuntimeError("Failed to capture image")
    
    logging.debug("Image captured successfully.")
    return frame

# Giải phóng camera khi không còn sử dụng
def release_camera():
    cap.release()
    logging.debug("Camera released.")
