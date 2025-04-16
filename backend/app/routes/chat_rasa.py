from flask import Blueprint, request, jsonify
import requests

chat_bp = Blueprint("chat", __name__)

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"  # Địa chỉ API của Rasa

@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Gửi tin nhắn đến Rasa
        response = requests.post(RASA_URL, json={"sender": "user", "message": user_message})
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to connect to Rasa"}), 500
        
        rasa_response = response.json()
        messages = [res["text"] for res in rasa_response if "text" in res]

        return jsonify({"messages": messages})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
