from flask import Blueprint
from app.controllers.notification_controller import NotificationController

notification_bp = Blueprint('notification', __name__)

notification_bp.route('/', methods=['GET'])(NotificationController.get_notifications)
notification_bp.route('/<int:id>/read', methods=['PUT'])(NotificationController.mark_read)
notification_bp.route('/<int:id>', methods=['DELETE'])(NotificationController.delete)
