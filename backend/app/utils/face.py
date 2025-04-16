import base64
import cv2
from deepface import DeepFace
from scipy.spatial.distance import cosine

def get_face_embedding(image, anti_spoofing=True):
    try:
        # Kiểm tra image có hợp lệ không
        if image is None:
            print("Invalid image input! Authentication failed.")
            return None
        # Trích xuất khuôn mặt với kiểm tra chống giả mạo
        face_objs = DeepFace.extract_faces(img_path=image, 
                                          anti_spoofing=anti_spoofing,
                                          detector_backend='ssd')
        # Kiểm tra có khuôn mặt nào được phát hiện không
        if not face_objs:
            print("No face found! Authentication failed.")
            return None
        # Kiểm tra chống giả mạo nếu được bật
        if anti_spoofing:
            # Kiểm tra rõ ràng hơn cho thuộc tính is_real
            all_real = True
            for face_obj in face_objs:
                if 'is_real' not in face_obj or not face_obj['is_real']:
                    all_real = False
                    break      
            if not all_real:
                print("Spoof detected! Authentication failed.")
                return None
        # Nếu vượt qua kiểm tra chống giả mạo, lấy embedding khuôn mặt
        embedding = DeepFace.represent(image, model_name='Facenet512', 
                                      detector_backend='ssd',
                                      enforce_detection=False)  # Không cần enforce vì đã kiểm tra
        # Kiểm tra embedding có tồn tại và có phần tử không
        if not embedding or len(embedding) == 0:
            print("Failed to generate face embedding.")
            return None
        return embedding[0]['embedding']
    except Exception as e:
        print(f"Error in face recognition: {e}")
        return None
    
def compare_face_embeddings(input_embedding, stored_embedding, threshold=0.3):
    if input_embedding is None or stored_embedding is None:
        return False
    return cosine(input_embedding, stored_embedding) < threshold

def encode_image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')