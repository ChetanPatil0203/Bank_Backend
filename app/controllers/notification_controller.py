from flask import request, jsonify
from app.services.notification_service import NotificationService

class NotificationController:
    @staticmethod
    def get_notifications():
        user_id = request.args.get('user_id')
        print(f"[DEBUG] Fetching notifications for user_id: {user_id}")
        
        if not user_id:
            return jsonify({'success': False, 'message': 'user_id is required.'}), 400
        
        try:
            notifications = NotificationService.get_user_notifications(int(user_id))
            return jsonify({'success': True, 'notifications': notifications}), 200
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid user_id format.'}), 400

    @staticmethod
    def mark_read(id):
        success = NotificationService.mark_as_read(id)
        if success:
            return jsonify({'success': True, 'message': 'Notification marked as read.'}), 200
        return jsonify({'success': False, 'message': 'Notification not found.'}), 404

    @staticmethod
    def delete(id):
        success = NotificationService.delete_notification(id)
        if success:
            return jsonify({'success': True, 'message': 'Notification deleted.'}), 200
        return jsonify({'success': False, 'message': 'Notification not found.'}), 404
