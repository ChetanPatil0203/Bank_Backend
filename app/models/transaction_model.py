from app.db import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False) # 'Deposit' or 'Withdraw'
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    note = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Success')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'account_number': self.account_number,
            'user': self.user_name,
            'type': self.type,
            'amount': float(self.amount),
            'note': self.note,
            'status': self.status,
            'date': self.created_at.strftime('%Y-%m-%d') if self.created_at else None,
            'time': self.created_at.strftime('%I:%M %p') if self.created_at else None,
            'timestamp': self.created_at.isoformat() if self.created_at else None
        }
