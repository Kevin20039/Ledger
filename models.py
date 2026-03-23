from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    business_name = db.Column(db.String(150), nullable=True)
    customers = db.relationship('Customer', backref='owner', lazy=True)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='customer', lazy=True)

    @property
    def balance(self):
        # Calculate balance: + if you gave (positive), - if you got (negative)
        # OR: Convention: 
        # "You Gave" (Credit) -> Positive standardly => Customer owes you.
        # "You Got" (Debit) -> Negative standardly => You owe customer / debt reduced.
        # Let's stick to: Positive = Customer owes YOU (You will get). Negative = You owe Customer (You will give).
        
        total = 0
        for tx in self.transactions:
            if tx.type == 'GAVE':
                total += tx.amount
            elif tx.type == 'GOT':
                total -= tx.amount
        return total

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'GAVE' or 'GOT'
    description = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
