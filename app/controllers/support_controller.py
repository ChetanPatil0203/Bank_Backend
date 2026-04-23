from flask import request, jsonify
from app.services.support_service import SupportService

class SupportController:

    @staticmethod
    def create_ticket():
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'success': False, 'message': 'Missing Token'}), 401
        
        token = auth_header.split(" ")[1]
        data = request.get_json() or {}
        result = SupportService.create_ticket(token, data)
        status_code = 201 if result.get('success') else (401 if 'isAuth' in result else 400)
        return jsonify(result), status_code

    @staticmethod
    def get_my_tickets():
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'success': False, 'message': 'Missing Token'}), 401
        
        token = auth_header.split(" ")[1]
        result = SupportService.get_my_tickets(token)
        status_code = 200 if result.get('success') else (401 if 'isAuth' in result else 400)
        return jsonify(result), status_code

    @staticmethod
    def get_ticket_details(id):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'success': False, 'message': 'Missing Token'}), 401
        
        token = auth_header.split(" ")[1]
        result = SupportService.get_ticket_details(token, id)
        status_code = 200 if result.get('success') else (401 if 'isAuth' in result else 400)
        return jsonify(result), status_code

    @staticmethod
    def add_message(id):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'success': False, 'message': 'Missing Token'}), 401
        
        token = auth_header.split(" ")[1]
        data = request.get_json() or {}
        message_text = data.get('message')
        if not message_text:
            return jsonify({'success': False, 'message': 'Message is required'}), 400

        result = SupportService.add_message(token, id, message_text)
        status_code = 200 if result.get('success') else (401 if 'isAuth' in result else 400)
        return jsonify(result), status_code

    @staticmethod
    def admin_get_tickets():
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'success': False, 'message': 'Missing Token'}), 401
        
        token = auth_header.split(" ")[1]
        status = request.args.get('status')
        result = SupportService.admin_get_tickets(token, status)
        status_code = 200 if result.get('success') else (401 if 'isAuth' in result else 400)
        return jsonify(result), status_code

    @staticmethod
    def admin_update_status(id):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'success': False, 'message': 'Missing Token'}), 401
        
        token = auth_header.split(" ")[1]
        data = request.get_json() or {}
        status = data.get('status')
        if not status:
            return jsonify({'success': False, 'message': 'Status is required'}), 400

        result = SupportService.admin_update_status(token, id, status)
        status_code = 200 if result.get('success') else (401 if 'isAuth' in result else 400)
        return jsonify(result), status_code
