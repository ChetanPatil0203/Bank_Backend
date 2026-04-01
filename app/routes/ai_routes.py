from flask import Blueprint
from app.controllers.ai_controller import AIController

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/chat', methods=['POST'])
def chat():
    return AIController.chat()
