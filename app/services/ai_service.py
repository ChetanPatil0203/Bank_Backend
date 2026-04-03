from google import genai
from google.genai import types
from flask import current_app
import os

class AIService:
    def __init__(self):
        self.api_key = current_app.config.get('GOOGLE_API_KEY')
        if not self.api_key or self.api_key == 'your_google_api_key_here' or self.api_key == '':
            raise ValueError("GOOGLE_API_KEY is not configured correctly in .env")
        
        # Initialize the new Google GenAI Client
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = 'gemini-2.0-flash' # Using stable flash model, adjust if gemini-2.5-flash is preferred
        
        # System instruction for Payzen Bank
        self.system_instruction = (
            "You are 'Ask Payzen', a helpful AI assistant for Payzen Bank. "
            "You provide guidance and recommendations about Payzen Bank products and services. "
            "IMPORTANT: Detect the user's language. If the user types in English, respond in English. "
            "If the user types in Marathi (or Hinglish), respond in Marathi. "
            "Always format your answers using bullet points or numbered lists for clarity. "
            "Avoid long paragraphs. Keep each point concise, professional, and friendly."
        )
        
        # Configuration with system instruction
        self.config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.7
        )

    def get_chat_response(self, user_message, chat_history=None):
        try:
            # Ensure chat_history is a valid list of non-empty dicts
            valid_history = []
            if chat_history and isinstance(chat_history, list):
                for entry in chat_history:
                    # The new SDK expects 'parts' as a list or a single Part object
                    if isinstance(entry, dict) and entry.get('parts') and entry.get('role'):
                        valid_history.append(entry)
            
            # Start chat session with cleaned history
            chat = self.client.chats.create(
                model=self.model_id,
                config=self.config,
                history=valid_history
            )
            
            # Send message
            response = chat.send_message(user_message)
            return response.text
            
        except Exception as e:
            with open("ai_error.log", "a") as f:
                f.write(f"Error in AIService: {str(e)}\n")
                import traceback
                traceback.print_exc(file=f)
            print(f"Error in AIService: {str(e)}")
            return "I'm sorry, I'm having trouble connecting to my brain right now. Please try again later."

ai_service = None

def get_ai_service():
    global ai_service
    if ai_service is None:
        ai_service = AIService()
    return ai_service
