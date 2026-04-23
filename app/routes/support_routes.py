from flask import Blueprint
from app.controllers.support_controller import SupportController

support_bp = Blueprint('support_bp', __name__)

# User routes
@support_bp.route('/tickets', methods=['POST'])
def create_ticket():
    return SupportController.create_ticket()

@support_bp.route('/my-tickets', methods=['GET'])
def get_my_tickets():
    return SupportController.get_my_tickets()

@support_bp.route('/tickets/<int:id>', methods=['GET'])
def get_ticket_details(id):
    return SupportController.get_ticket_details(id)

@support_bp.route('/tickets/<int:id>/message', methods=['POST'])
def add_message(id):
    return SupportController.add_message(id)

# Admin routes
@support_bp.route('/admin/tickets', methods=['GET'])
def admin_get_tickets():
    return SupportController.admin_get_tickets()

@support_bp.route('/admin/tickets/<int:id>/status', methods=['PATCH'])
def admin_update_status(id):
    return SupportController.admin_update_status(id)
