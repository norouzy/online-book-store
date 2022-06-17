from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


tableQueries = [

    "CREATE TABLE User("
    +"\n    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    +"\n    username VARCHAR(100) UNIQUE NOT NULL,"
    +"\n    password VARCHAR(150) NOT NULL,"
    +"\n    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    +"\n    is_admin BOOLEAN DEFAULT FALSE"
    +"\n );",

     
    "CREATE TABLE Customer("
    +"\n    user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
    +"\n    first_name VARCHAR(100) NOT NULL,"
    +"\n    last_name VARCHAR(150) NOT NULL,"
    +"\n    phone_number VARCHAR(20) NOT NULL,"
    +"\n    address TEXT NOT NULL,"
    +"\n    FOREIGN KEY(user_id) REFERENCES User(id)"
    +"\n );",
    
     
    "CREATE TABLE Book("
    +"\n    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    +"\n    name VARCHAR(100) NOT NULL,"
    +"\n    author VARCHAR(150),"
    +"\n    picture_url VARCHAR(255),"
    +"\n    price INT NOT NULL,"
    +"\n    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    +"\n    description TEXT NOT NULL"
    +"\n );",

     
    "CREATE TABLE Publisher("
    +"\n    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    +"\n    name VARCHAR(100) UNIQUE NOT NULL,"
    +"\n    phone_number VARCHAR(20) NOT NULL,"
    +"\n    website_url VARCHAR(255)"
    +"\n );",


    "CREATE TABLE Category("
    +"\n    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    +"\n    name VARCHAR(100) NOT NULL"
    +"\n );",
     

   "CREATE TABLE book_order("
    +"\n    book_id INT,"
    +"\n    customer_id INT,"
    +"\n    publisher_id INT,"
    +"\n    quantity INT NOT NULL,"
    +"\n    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    +"\n    FOREIGN KEY(customer_id) REFERENCES Customer(id),"
    +"\n    FOREIGN KEY(book_id) REFERENCES Book(id),"
    +"\n    FOREIGN KEY(publisher_id) REFERENCES Publisher(id),"
    +"\n    PRIMARY key(book_id, customer_id)"
    +"\n );",


    "CREATE TABLE book_category("
    +"\n    book_id INT,"
    +"\n    category_id INT,"
    +"\n    FOREIGN KEY(book_id) REFERENCES Book(id),"
    +"\n    FOREIGN KEY(category_id) REFERENCES Category(id),"
    +"\n    PRIMARY key(book_id, category_id)"
    +"\n );",


    "CREATE TABLE book_publisher("
    +"\n    book_id INT,"
    +"\n    publisher_id INT,"
    +"\n    quantity INT NOT NULL,"
    +"\n    FOREIGN KEY(book_id) REFERENCES Book(id),"
    +"\n    FOREIGN KEY(publisher_id) REFERENCES Publisher(id),"
    +"\n    PRIMARY key(book_id, publisher_id)"
    +"\n );",

]


# for table in tableQueries:
#     print(table)
#     db.engine.execute(text(table))