from app.models.notification_model import Notification
from app.db import db

class NotificationService:
    @staticmethod
    def get_user_notifications(user_id):
        notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
        return [n.to_dict() for n in notifications]

    @staticmethod
    def mark_as_read(notification_id):
        notification = Notification.query.get(notification_id)
        if notification:
            notification.is_read = True
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_notification(notification_id):
        notification = Notification.query.get(notification_id)
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def create_notification(user_id, title, message, type='info'):
        new_notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type
        )
        db.session.add(new_notification)
        db.session.commit()
        return new_notification.to_dict()
