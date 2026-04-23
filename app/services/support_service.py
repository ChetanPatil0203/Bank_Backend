import random
import string
from datetime import datetime
from app.models.support_model import SupportTicket, TicketMessage
from app.models.user_model import UserLogin, AdminLogin
from app.db import db

class SupportService:

    @staticmethod
    def create_ticket(token, data):
        try:
            user = UserLogin.query.filter_by(jwt_token=token).first()
            if not user:
                return {'success': False, 'message': 'Unauthorized', 'isAuth': False}

            ticket_num = "TKT-" + "".join(random.choices(string.digits, k=6))
            while SupportTicket.query.filter_by(ticket_number=ticket_num).first():
                ticket_num = "TKT-" + "".join(random.choices(string.digits, k=6))

            new_ticket = SupportTicket(
                ticket_number=ticket_num,
                user_id=user.id,
                full_name=data.get('full_name', 'User'),
                email=user.email,
                subject=data.get('subject'),
                description=data.get('description'),
                issue_type=data.get('issue_type', 'General'),
                priority=data.get('priority', 'medium'),
                status='open'
            )

            db.session.add(new_ticket)
            db.session.commit()

            return {'success': True, 'message': 'Ticket created successfully', 'data': new_ticket.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    @staticmethod
    def get_my_tickets(token):
        try:
            user = UserLogin.query.filter_by(jwt_token=token).first()
            if not user:
                return {'success': False, 'message': 'Unauthorized', 'isAuth': False}

            tickets = SupportTicket.query.filter_by(user_id=user.id).order_by(SupportTicket.created_at.desc()).all()
            return {'success': True, 'tickets': [t.to_dict() for t in tickets]}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def get_ticket_details(token, ticket_id):
        try:
            # Check if user or admin
            user = UserLogin.query.filter_by(jwt_token=token).first()
            if not user:
                user = AdminLogin.query.filter_by(jwt_token=token).first()
            
            if not user:
                return {'success': False, 'message': 'Unauthorized', 'isAuth': False}

            ticket = SupportTicket.query.get(ticket_id)
            if not ticket:
                return {'success': False, 'message': 'Ticket not found'}

            return {'success': True, 'data': ticket.to_dict()}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def add_message(token, ticket_id, message_text):
        try:
            # Check user
            user = UserLogin.query.filter_by(jwt_token=token).first()
            role = 'user'
            if not user:
                user = AdminLogin.query.filter_by(jwt_token=token).first()
                role = 'admin'
            
            if not user:
                return {'success': False, 'message': 'Unauthorized', 'isAuth': False}

            ticket = SupportTicket.query.get(ticket_id)
            if not ticket:
                return {'success': False, 'message': 'Ticket not found'}

            new_message = TicketMessage(
                ticket_id=ticket.id,
                sender_id=user.id,
                sender_role=role,
                message=message_text
            )

            # If admin replies, set status to 'in-progress' if it's currently 'open'
            if role == 'admin' and ticket.status == 'open':
                ticket.status = 'in-progress'

            db.session.add(new_message)
            db.session.commit()

            return {'success': True, 'message': 'Message added successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    @staticmethod
    def admin_get_tickets(token, status=None):
        try:
            admin = AdminLogin.query.filter_by(jwt_token=token).first()
            if not admin:
                return {'success': False, 'message': 'Unauthorized', 'isAuth': False}

            query = SupportTicket.query
            if status:
                query = query.filter_by(status=status)
            
            tickets = query.order_by(SupportTicket.created_at.desc()).all()
            return {'success': True, 'tickets': [t.to_dict() for t in tickets]}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def admin_update_status(token, ticket_id, status):
        try:
            admin = AdminLogin.query.filter_by(jwt_token=token).first()
            if not admin:
                return {'success': False, 'message': 'Unauthorized', 'isAuth': False}

            ticket = SupportTicket.query.get(ticket_id)
            if not ticket:
                return {'success': False, 'message': 'Ticket not found'}

            ticket.status = status
            db.session.commit()

            return {'success': True, 'message': f'Ticket status updated to {status}'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
