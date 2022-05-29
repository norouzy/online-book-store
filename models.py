from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    # realations
    customers = db.relationship('Customer', backref='user', lazy=True)


class Customer(db.Model):
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(70), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    # relations
    orders = db.relationship('Order', backref='customer', lazy=True)
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    book_id = db.relationship('id', backref='book', lazy=True)
    # foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.user_id'), nullable=False)

book_publisher = db.Table('book_publisher',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('publisher_id', db.Integer, db.ForeignKey('publisher.id'), primary_key=True)
)
book_category = db.Table('book_category',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)
book_order = db.Table('book_order',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True)
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(70), nullable=False)
    picture_url = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    # relations
    publishers = db.relationship('Publisher', secondary=book_publisher, lazy='subquery', backref=db.backref('books', lazy=True))
    categories = db.relationship('Category', secondary=book_category, lazy='subquery', backref=db.backref('books', lazy=True))
    orders = db.relationship('Order', secondary=book_order, lazy='subquery', backref=db.backref('books', lazy=True))

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    website_url = db.Column(db.String(255))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


db.create_all()