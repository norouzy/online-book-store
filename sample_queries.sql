-- table schemas
.schema book
.schema User
.schema customer
.schema category
.schema book_order
.schema publisher
.schema book_category
.schema book_publisher
.schema book_order
.tables

-- new users
INSERT INTO  User(username, password, is_admin)
VALUES('admin', 'root', TRUE);

INSERT INTO  User(username, password, is_admin)
VALUES('Ali123', 'passwd', FALSE),
('Mohammad1950', '1234', FALSE),
('MahdiKing', 'abcd', TRUE);

INSERT INTo customer(first_name,last_name, user_id, phone_number, address)
VALUES('Ali', 'Hasanzadeh', 2, '09305898647', 'Lorem ipsum dolor sit amet,
 suas porro viris est te,
  cum ei partem evertitur consetetur.
   Et pri utroque qualisque delicatissimi.'),
('Mohammad', 'Noruzi', 3, '09101398655', 'Lorem ipsum dolor sit amet,
 suas porro viris est te,
  cum ei partem evertitur consetetur.'),
('Mahdi', 'Ebrahimi', 4, '09303291264', 'Lorem ipsum dolor sit amet,
 suas porro viris est te,
  cum ei partem evertitur consetetur.');


-- new books
INSERT INTO book(name, author, picture_url, price, description)
VALUES('Nineteen Eighty-Four', 'George Orwell','pictures/1984.jpg', 
80000, 'Lorem ipsum dolor sit amet, te eam elit modus homero vis.'),
('The Plague', 'Albert Camus','pictures/the_plague.jpg', 
106000, 'Lorem ipsum dolor sit amet'), 
('Java: How to Program', 'Harvey Deitel and Paul Deitel','pictures/Java_How_to_Program.jpg', 
190000, 'Lorem ipsum dolor sit amet,
 nam ut facer erant quaestio,
 duo cu scripta epicurei philosophia. Molestie repudiandae.'), 
('Under the Banner of Heaven', 'Jon Krakauer','pictures/under_the_banner_of_heaven.jpg', 
77000, 'Lorem ipsum dolor sit amet, 
diam summo duo ad, ne inani tractatos torquatos pro.'), 
('Mein Kampf', 'Adolf Hitle','pictures/mein_kampf.jpg', 
98400, 'Lorem ipsum dolor sit amet, 
diam summo duo ad');

-- new publishers
INSERT INTO publisher(name, phone_number, website_url)
VALUES('negah', '214534', 'https://negahpub.com'),
('cheshme', '33457', 'http://www.cheshmeh.ir'),
('ghoghnus', '98557', 'https://qoqnoos.ir'),
('sales', '66678', 'https://salesspublication.com'),
('amirkabir', '34956', 'https://amirkabirpub.ir');

-- new categories
INSERT INTO category(name)
VALUES('novel'), ('history'), ('reference'), ('religious'),
('philosophy'), ('music');

-- new orders
INSERT INTO book_order(book_id, customer_id, quantity)
VALUES(1, 2, 1), 
(4, 2, 3),
(1, 3, 3), 
(3, 4, 1); 

-- book_categories
INSERT INTO book_category(book_id, category_id)
VALUES(1, 1), (2, 1), (2, 2), (2, 5), (3, 3), (4, 4),
(4, 5), (5, 1), (5, 2);

-- book_publishers
INSERT INTO book_publisher(book_id, publisher_id, quantity)
VALUES(1, 3, 5), (1, 5, 10), (2, 3, 16), (3, 1, 1), (4, 4, 17), (4, 2, 110), 
(4, 5, 76), (5, 1, 35);


SELECT * FROM user;
SELECT * from customer;
SELECT * FROM book;
SELECT * from publisher;
SELECT * from book_publisher;
SELECT * from category;
SELECT * from book_category;
SELECT * FROM book_order;
select *
 from book join book_publisher on book.id=book_publisher.book_id
    join publisher on publisher.id=publisher_id;
DELETE from user;

ALTER TABLE book_publisher ADD quentity INT NOT NULL;

SELECT * FROM Book JOIN book_publisher ON book.id=book_publisher.book_id JOIN Publisher on Publisher.id=publisher_id order by book.price ,book.date_added desc;

SELECT * FROM Book JOIN book_publisher ON book.id=book_publisher.book_id JOIN Publisher on Publisher.id=publisher_id where Book.name LIKE '%nin%' order by book.price;
