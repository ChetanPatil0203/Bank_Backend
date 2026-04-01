from flask import request, jsonify
from app.services.ai_service import AIService
import traceback

class AIController:
    @staticmethod
    def chat():
        data = request.get_json() or {}
        user_message = data.get('message')
        chat_history = data.get('history', [])
        
        if not user_message:
            return jsonify({"success": False, "message": "Message is required"}), 400
            
        try:
            service = AIService()
            response_text = service.get_chat_response(user_message, chat_history)
            
            return jsonify({
                "success": True,
                "response": response_text
            }), 200
        except ValueError as ve:
            return jsonify({"success": False, "message": str(ve)}), 500
        except Exception as e:
            traceback.print_exc()
            return jsonify({"success": False, "message": "Internal server error connecting to AI"}), 500
