from app.db import db
from datetime import datetime

class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    issue_type = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), default='medium') # low, medium, high, critical
    status = db.Column(db.String(20), default='open') # open, in-progress, resolved, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_number': self.ticket_number,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'email': self.email,
            'subject': self.subject,
            'description': self.description,
            'issue_type': self.issue_type,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'messages': [m.to_dict() for m in self.messages]
        }

class TicketMessage(db.Model):
    __tablename__ = 'ticket_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('support_tickets.id'), nullable=False)
    sender_id = db.Column(db.Integer, nullable=False) # Can be user_id or admin_id
    sender_role = db.Column(db.String(10), nullable=False) # 'user' or 'admin'
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    ticket = db.relationship('SupportTicket', backref=db.backref('messages', lazy=True, cascade="all, delete-orphan"))

    def to_dict(self):
        return {
            'sender_role': self.sender_role,
            'message': self.message,
            'created_at': self.created_at.isoformat()
        }
