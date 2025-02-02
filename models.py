from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    plate_number = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20))
    car_color = db.Column(db.String(50))
    mileage = db.Column(db.Integer)
    reception_date = db.Column(db.DateTime, default=datetime.utcnow)
    entry_date = db.Column(db.DateTime)
    car_model = db.Column(db.String(100))
    invoices = db.relationship('Invoice', backref='customer', lazy=True)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    services = db.Column(db.JSON)  # ذخیره لیست خدمات انتخاب شده
    total_amount = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)