-- table schemas
.schema book
.schema user
.schema customer
.schema category
.schema order
.schema publisher
.schema book_category
.schema book_publisher
.schema book_order

-- new users
INSERT INTO  User(username, password, user_type)
VALUES('admin', 'root', 'admin');

INSERT INTO  User(username, password, user_type)
VALUES('Ali', 'passwd', 0),
('Mohammad', '1234', 0),
('Mahdi', 'abcd', 1);

INSERT INTo customer(user_id, phone_number, address)
VALUES(2, '09305898647', 'Lorem ipsum dolor sit amet,
 suas porro viris est te,
  cum ei partem evertitur consetetur.
   Et pri utroque qualisque delicatissimi.'),
(3, '09101398655', 'Lorem ipsum dolor sit amet,
 suas porro viris est te,
  cum ei partem evertitur consetetur.'),
(4, '09303291264', 'Lorem ipsum dolor sit amet,
 suas porro viris est te,
  cum ei partem evertitur consetetur.');


-- new books
INSERT INTO book(name, author, picture_url, price, description, quantity)
VALUES('Nineteen Eighty-Four', 'George Orwell','pictures/1984.jpg', 
80000, 'Lorem ipsum dolor sit amet, te eam elit modus homero vis.', 19),
('The Plague', 'Albert Camus','pictures/the_plague.jpg', 
106000, 'Lorem ipsum dolor sit amet', 7), 
('Java: How to Program', 'Harvey Deitel and Paul Deitel','pictures/Java_How_to_Program.jpg', 
190000, 'Lorem ipsum dolor sit amet,
 nam ut facer erant quaestio,
 duo cu scripta epicurei philosophia. Molestie repudiandae.', 33), 
('Under the Banner of Heaven', 'Jon Krakauer','pictures/under_the_banner_of_heaven.jpg', 
77000, 'Lorem ipsum dolor sit amet, 
diam summo duo ad, ne inani tractatos torquatos pro.', 14), 
('Mein Kampf', 'Adolf Hitle','pictures/mein_kampf.jpg', 
98400, 'Lorem ipsum dolor sit amet, 
diam summo duo ad', 
40);

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
INSERT INTO 'order'(customer_id, quantity, status)
VALUES(2, 1, 0), 
(2, 1, 1),
(3, 3, 0), 
(4, 2, 0); 

-- book_categories
INSERT INTO book_category(book_id, category_id)
VALUES(1, 1), (2, 1), (2, 2), (2, 5), (3, 3), (4, 4),
(4, 5), (5, 1), (5, 2);

-- book_publishers
INSERT INTO book_publisher(book_id, publisher_id)
VALUES(1, 3), (1, 5), (2, 3), (3, 1), (4, 4), (4, 2), 
(4, 5), (5, 1);

-- book_orders
INSERT INTO book_order(order_id, book_id)
VALUES(1, 3), (2, 4), (3, 1), (4, 4);


SELECT * FROM user;
SELECT * from customer;
SELECT * FROM book;
SELECT * from publisher;
SELECT * from category;
SELECT * from 'order';
SELECT * from book_category;
SELECT * from book_publisher;
SELECT * FROM book_order;

DELETE from book;