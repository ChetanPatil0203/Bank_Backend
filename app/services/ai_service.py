import google.generativeai as genai
from flask import current_app

class AIService:
    def __init__(self):
        self.api_key = current_app.config.get('GOOGLE_API_KEY')
        if not self.api_key or self.api_key == 'your_google_api_key_here' or self.api_key == '':
            raise ValueError("GOOGLE_API_KEY is not configured correctly in .env")
        
        genai.configure(api_key=self.api_key)
        
        # System instruction for Payzen Bank
        system_instruction = (
            "You are 'Ask Payzen', a helpful AI assistant for Payzen Bank. "
            "You provide guidance and recommendations about Payzen Bank products and services. "
            "IMPORTANT: Detect the user's language. If the user types in English, respond in English. "
            "If the user types in Marathi (or Hinglish), respond in Marathi. "
            "Always format your answers using bullet points or numbered lists for clarity. "
            "Avoid long paragraphs. Keep each point concise, professional, and friendly."
        )
        
        # Initialize model with system instruction
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=system_instruction
        )

    def get_chat_response(self, user_message, chat_history=None):
        try:
            # Ensure chat_history is a valid list of non-empty dicts
            valid_history = []
            if chat_history and isinstance(chat_history, list):
                for entry in chat_history:
                    if isinstance(entry, dict) and entry.get('parts') and entry.get('role'):
                        valid_history.append(entry)
            
            # Start chat session with cleaned history
            chat = self.model.start_chat(history=valid_history)
            
            # Send message directly as context is now in system_instruction
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
