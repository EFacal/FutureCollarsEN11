from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    quantity = db.Column(db.Integer, default=0)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    product_name = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=True)
    amount = db.Column(db.Float)