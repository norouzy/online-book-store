from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import time
from os.path import exists


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
    +"\n    FOREIGN KEY(customer_id) REFERENCES Customer(user_id),"
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

dataFillQueries = [

    "INSERT INTO  User(username, password, is_admin)"
    +"\n    VALUES('admin', 'root', TRUE),"
    +"\n    ('Ali123', 'passwd', FALSE),"
    +"\n    ('Mohammad1950', '1234', FALSE),"
    +"\n    ('MahdiKing', 'abcd', TRUE),"
    +"\n    ('yas', 'yastv1397', FALSE),"
    +"\n    ('zahra', 'zhra78', FALSE);",

    "INSERT INTo customer(first_name,last_name, user_id, phone_number, address)"
    +"\n    VALUES('Ali', 'Hasanzadeh', 2, '09305898647', 'Lorem ipsum dolor sit amet,"
    +"\n     suas porro viris est te,"
    +"\n      cum ei partem evertitur consetetur."
    +"\n       Et pri utroque qualisque delicatissimi.'),"
    +"\n    ('Mohammad', 'Noruzi', 3, '09101398655', 'Lorem ipsum dolor sit amet,"
    +"\n     suas porro viris est te, cum ei partem evertitur consetetur.'),"
    +"\n    ('Mahdi', 'Ebrahimi', 4, '09303291264', 'Lorem ipsum dolor sit amet,"
    +"\n     suas porro viris est te, cum ei partem evertitur consetetur.'),"
    +"\n     ('yasaman', 'tavasolian', 5, '09124260890', 'Lorem ipsum dolor sit amet,"
    +"\n     suas porro viris est te, cum ei partem evertitur consetetur.ructior et eum. Sed no verear'),"
    +"\n     ('zahra', 'karimi', 6, '09365103551', 'Lorem ipsum dolor sit amet,"
    +"\n     suas porro viris est te, cum ei partem evertitur consetetur.definiebas usu in, choro feugait tincidunt sit ea');",


    "INSERT INTO book(name, author, picture_url, price, description)"
    +"\n    VALUES('Nineteen Eighty-Four', 'George Orwell','1984.jpg',"
    +"\n    80000, 'Lorem ipsum dolor sit amet, te eam elit modus homero vis.'),"
    +"\n    ('Nineteen Eighty-Four', 'george orwell','1984(2).jpg',"
    +"\n    82000, 'Lorem ipsum dolor sit amet, te eam elit'),"
    +"\n    ('The Plague', 'Albert Camus','the_plague.jpg',"
    +"\n    106000, 'Lorem ipsum dolor sit amet'),"
    +"\n    ('The Plague', 'Albert Camus','the_plague(2).jpg',"
    +"\n    122000, 'Lorem ipsum dolor'),"
    +"\n    ('Java: How to Program', 'Harvey Deitel and Paul Deitel','Java_How_to_Program.jpg',"
    +"\n    190000, 'Lorem ipsum dolor sit amet,"
    +"\n     nam ut facer erant quaestio,"
    +"\n     duo cu scripta epicurei philosophia. Molestie repudiandae.'),"
    +"\n    ('Under the Banner of Heaven', 'Jon Krakauer','under_the_banner_of_heaven.jpg',"
    +"\n    77000, 'Lorem ipsum dolor sit amet,"
    +"\n    diam summo duo ad, ne inani tractatos torquatos pro.'),"
    +"\n    ('Mein Kampf', 'Adolf Hitler','mein_kampf.jpg',"
    +"\n    98400, 'Lorem ipsum dolor sit amet,"
    +"\n    diam summo duo ad'),"
    +"\n    ('The Sandman', 'Neil Gaiman','sandman.jpg',"
    +"\n    340000, 'Vidisse definiebas usu in, choro feugait tincidunt sit ea. Eum errem legendos eu,"
    +"\n    alia phaedrum duo ea. Et simul integre qui, ius an saperet accusata comprehensam. Ex everti reformidans sea.');",


    "INSERT INTO publisher(name, phone_number, website_url)"
    +"\n    VALUES('negah', '214534', 'https://negahpub.com'),"
    +"\n    ('cheshme', '33457', 'http://www.cheshmeh.ir'),"
    +"\n    ('ghoghnus', '98557', 'https://qoqnoos.ir'),"
    +"\n    ('sales', '66678', 'https://salesspublication.com'),"
    +"\n    ('amirkabir', '34956', 'https://amirkabirpub.ir');",


    "INSERT INTO category(name)"
    +"\n    VALUES('novel'), ('history'), ('educational'), ('religious'),"
    +"\n    ('philosophy'), ('encyclopedia'), ('litrature'), ('children'),"
    +"\n    ('commic');",


    "INSERT INTO book_order(book_id, customer_id, publisher_id, quantity)"
    +"\n    VALUES(1, 2, 3, 12),"
    +"\n    (3, 2, 3, 3),"
    +"\n    (6, 3, 2, 1),"
    +"\n    (8, 4, 1, 2),"
    +"\n    (4, 5, 1, 7),"
    +"\n    (5, 2, 4, 4);",

    
    "INSERT INTO book_category(book_id, category_id)"
    +"\n    VALUES(1, 1), (1, 5), (2, 1),(2, 5), (3, 1), (3, 5),(3, 7), (4, 1), (4, 5), (5, 3), (5, 6),"
    +"\n    (6, 4), (6, 2), (6, 7),(7, 1), (7, 2), (7, 8),(8, 1), (8, 9), (8, 8);",


    "INSERT INTO book_publisher(book_id, publisher_id, quantity)"
    +"\n    VALUES(1, 3, 0), (2, 5, 10), (3, 3, 16), (4, 1, 1), (5, 4, 17), (6, 2, 110),"
    +"\n    (7, 2, 76), (8, 1, 35);"

]


file_exists = exists('scripts/db.sqlite3')

if not file_exists:
    for table in tableQueries:
        print(table)
        db.engine.execute(text(table))

    for table in dataFillQueries:
        print(table)
        db.engine.execute(text(table))
    