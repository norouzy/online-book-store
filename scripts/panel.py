from PyQt5 import QtCore, QtWidgets, QtGui
from scripts.tables import db
from sqlalchemy import false, text
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import shutil,re,os,random

class Ui_MainWindow(object):
    # main functions

    def __init__(self, user_id, is_admin, username, MainWindow):

        self.baseQuery = "SELECT Book.name, book_publisher.quantity, Book.author, Book.price, Publisher.name,"\
                        +"\n    ifnull(book_order.quantity, 0) as ordcount, publisher.id, Book.id, Book.picture_url"\
                        +"\n    FROM book_publisher"\
                        +"\n    JOIN Book ON book_publisher.book_id=Book.id"\
                        +"\n    JOIN Publisher ON Publisher.id=book_publisher.publisher_id"\
                        +"\n    LEFT JOIN book_order ON book_order.book_id=book.id and book_order.publisher_id=Publisher.id"\
                        +"\n    GROUP BY Book.id, Publisher.id"
                       

        self.userQuery = "SELECT User.id, User.username, Customer.first_name, Customer.last_name, Customer.address, "\
                        +"\n    Customer.phone_number, User.is_admin, ifnull(SUM(book_order.quantity), 0) AS total, User.date_JOINed"\
                        +"\n    FROM User "\
                        +"\n    JOIN Customer ON User.id=Customer.user_id"\
                        +"\n    LEFT JOIN book_order ON book_order.customer_id=User.id"\
                        +"\n    GROUP BY User.username"

        self.MainWindow = MainWindow   
        self.user_id = user_id
        self.username = username
        self.is_admin = is_admin      
        self.bookSearch = None
        self.userSearch = None
        self.bookObjects = None
        self.userObjects = []
        self.pictures = None
        self.categoryBoxes = []
        self.bookCatBoxes = []
        self.bookDetailUi = None
        self.bookEditUi = None
        self.initialInfo = None


    def logout(self):
        from scripts.login import Ui_LoginWindow
        ui = Ui_LoginWindow()
        ui.setupUi(self.MainWindow)

    def logout(self):
        from scripts.login import Ui_LoginWindow
        ui = Ui_LoginWindow()
        ui.setupUi(self.MainWindow)


    def OkMsgBox(self,type, title, text):
        msg = QMessageBox()
        if type == 'warning':
            msg.setIcon(QMessageBox.Warning)
        else:
            msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def getPublishers(self):
        query = "SELECT name FROM Publisher"
        return [res[0] for res in list(db.engine.execute(text(query)))]


    def placeCatBoxes(self, tab, x, y, w, h):

        query = "SELECT name FROM category"
        catResult = list(db.engine.execute(text(query)))

        for index, cat in enumerate(catResult):    

            if tab == 0:          
                if index % 3 == 0:
                    x += 111
                    y = 18
                elif index % 3 == 1:
                    y = 43
                else:
                    y = 68       

                self.bookCatBoxes.append(QtWidgets.QCheckBox(self.frame_list_main))
                self.bookCatBoxes[index].setObjectName(cat[0])
                self.bookCatBoxes[index].setGeometry(QtCore.QRect(x, y, w, h))
            else:  
                if index % 2 == 0:
                    x += 100
                    y = 2
                else:
                    y = 32 

                self.categoryBoxes.append(QtWidgets.QCheckBox(self.scrollAreaWidgetContents_addbook_main))
                self.categoryBoxes[index].setObjectName(cat[0])           
                self.categoryBoxes[index].setGeometry(QtCore.QRect(x, y, w, h))

            

    def fillBooks(self, query):

        detailBtns = []
        buyEditBtns = []
        deleteBtns = []
        self.bookObjects = []
        self.pictures = []

        books = list(db.engine.execute(text(query)))

        for index, item in enumerate(books):
            self.bookObjects.append(QtWidgets.QFrame(self.scrollAreaWidgetContents))
            self.bookObjects[index].setMaximumSize(QtCore.QSize(485, 150))
            self.bookObjects[index].setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.bookObjects[index].setFrameShadow(QtWidgets.QFrame.Raised)
            self.bookObjects[index].setObjectName("frame_list_" + str(index))
            self.gridLayoutWidget = QtWidgets.QWidget(self.bookObjects[index])
            self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 9, 471, 136))
            self.gridLayoutWidget.setObjectName("gridLayoutWidget")
            self.gridLayout_list_0 = QtWidgets.QGridLayout(self.gridLayoutWidget)
            self.gridLayout_list_0.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_list_0.setObjectName("gridLayout_list_0")
            self.label_list_name_0 = QtWidgets.QLabel(self.gridLayoutWidget)
            self.label_list_name_0.setObjectName("label_list_name_0")
            self.gridLayout_list_0.addWidget(self.label_list_name_0, 0, 0, 1, 1)
            self.label_list_quantity_0 = QtWidgets.QLabel(self.gridLayoutWidget)
            self.label_list_quantity_0.setObjectName("label_list_quantity_0")
            self.gridLayout_list_0.addWidget(self.label_list_quantity_0, 4, 0, 1, 1)
            self.label_list_author_0 = QtWidgets.QLabel(self.gridLayoutWidget)
            self.label_list_author_0.setObjectName("label_list_author_0")
            self.gridLayout_list_0.addWidget(self.label_list_author_0, 1, 0, 1, 1)
            self.label_list_price_0 = QtWidgets.QLabel(self.gridLayoutWidget)
            self.label_list_price_0.setObjectName("label_list_price_0")
            self.gridLayout_list_0.addWidget(self.label_list_price_0, 5, 0, 1, 1)
            self.label_list_publisher_0 = QtWidgets.QLabel(self.gridLayoutWidget)
            self.label_list_publisher_0.setObjectName("label_list_publisher_0")
            self.gridLayout_list_0.addWidget(self.label_list_publisher_0, 3, 0, 1, 1)
            # detail buttons
            detailBtns.append(QtWidgets.QPushButton(self.gridLayoutWidget))
            detailBtns[index].setObjectName(str(item[7]))
            self.gridLayout_list_0.addWidget(detailBtns[index], 6, 0, 1, 1)
            detailBtns[index].clicked.connect(lambda ch, index=index: self.bookDetails(detailBtns[index].objectName()))
            detailBtns[index].setText("👀 More Details")
            detailBtns[index].setStyleSheet("#"+str(detailBtns[index].objectName())+" {color:blue;}")
            # buy/edit buttons
            buyEditBtns.append(QtWidgets.QPushButton(self.gridLayoutWidget))
            buyEditBtns[index].setObjectName(str(item[7]) + '_' + str(item[6]))
            self.gridLayout_list_0.addWidget(buyEditBtns[index], 6, 2, 1, 1)
            if self.is_admin:
                # detail buttons
                deleteBtns.append(QtWidgets.QPushButton(self.gridLayoutWidget))
                deleteBtns[index].setObjectName(str(item[7]))
                self.gridLayout_list_0.addWidget(deleteBtns[index], 6, 4, 1, 1)
                deleteBtns[index].clicked.connect(lambda ch, index=index: self.deleteBook(deleteBtns[index].objectName()))
                deleteBtns[index].setText("🗑 Delete")
                deleteBtns[index].setStyleSheet("#"+str(deleteBtns[index].objectName())+" {color:red;}")
                buyEditBtns[index].clicked.connect(lambda ch, index=index: self.editBook(buyEditBtns[index].objectName().split('_')[0],self.MainWindow))
                buyEditBtns[index].setText("♻️ Edit")
                buyEditBtns[index].setStyleSheet("#"+str(buyEditBtns[index].objectName())+" {color:green;}")
            else:
                buyEditBtns[index].clicked.connect(lambda ch, index=index:
                            self.buyBook(buyEditBtns[index].objectName().split('_')[0], buyEditBtns[index].objectName().split('_')[1]))
                buyEditBtns[index].setText("🛒 Buy")
            # pic
            self.gridLayout_5.addWidget(self.bookObjects[index], index, 1, 1, 1)
            self.pictures.append(QtWidgets.QGraphicsView(self.scrollAreaWidgetContents))
            self.pictures[index].setMinimumSize(QtCore.QSize(220, 150))
            self.pictures[index].setMaximumSize(QtCore.QSize(220, 150))
            self.pictures[index].setStyleSheet("#list_picture_"+str(index)+
            " { background-image: url(pictures/"+ item[8] +
            ");background-repeat: no-repeat;background-attachment: fixed;background-position: center;border:0px;}")
            # self.pictures[index].setStyleSheet("#list_picture_"+str(index)+" { background-image: url(pictures/book.jpeg);background-repeat: no-repeat;background-attachment: fixed;background-position: center;border:0px;}")
            self.pictures[index].setObjectName("list_picture_" + str(index))        
            self.gridLayout_5.addWidget(self.pictures[index], index, 0, 1, 1)
            # giving values
            self.label_list_name_0.setText('📚 book name: ' + item[0])
            self.label_list_quantity_0.setText('🧮 number in stock: ' + str('{:,}'.format(item[1])))
            self.label_list_author_0.setText('✒️ author: ' + item[2])
            self.label_list_price_0.setText('💰 price: ' + str('{:,}'.format(item[3]))+ "💲")
            self.label_list_publisher_0.setText('🗂 publisher: ' + item[4])
        

    def bookDetails(self, book_id):
        from scripts.book_detail import Ui_BookDetailWindow
        self.bookDetailUi = QtWidgets.QMainWindow()
        ui_book_detail = Ui_BookDetailWindow(book_id)
        ui_book_detail.setupUi(self.bookDetailUi)
        self.bookDetailUi.show()
  
    def update_main_window(main_self):
        self = main_self   
        self.setupUi(self.MainWindow)
    
    def editBook(self, book_id,MainWindow):
        from scripts.edit_book import Ui_BookEditWindow
        self.MainWindow = MainWindow
        self.bookEditUi = QtWidgets.QMainWindow()
        ui_book_detail = Ui_BookEditWindow(book_id,self)
        ui_book_detail.setupUi(self.bookEditUi)
        self.bookEditUi.show() 


    def buyBook(self, book_id, publisher_id):
        
        query = "SELECT book_publisher.quantity FROM Book JOIN book_publisher"\
                +"\n    ON Book.id=book_publisher.book_id"\
                +f"\n   WHERE Book.id={book_id}"
        quantity = list(db.engine.execute(text(query)))[0][0]

        query = f"SELECT User.id FROM User WHERE username='{self.username}'"
        user_id = list(db.engine.execute(text(query)))[0][0]

        if quantity != 0:
            query = "SELECT book_order.quantity FROM book_order WHERE"\
                    +f"\n  book_order.book_id={book_id} and book_order.customer_id={user_id}"
            try:
                userOrderQuantity = list(db.engine.execute(text(query)))[0][0]
                query = f"UPDATE book_order SET quantity={userOrderQuantity+1}"\
                       +f"\n  WHERE book_id={book_id} and customer_id={user_id}"
                db.engine.execute(text(query))
                self.OkMsgBox("information", "success", "order added sucessfully!")
            except:
                query = "INSERT INTO book_order(book_id, customer_id, publisher_id, quantity)"\
                       +f"\n  VALUES({book_id}, {user_id}, {publisher_id}, 1)"
                db.engine.execute(text(query))

            query = f"UPDATE book_publisher SET quantity={quantity-1} WHERE book_id={book_id}"
            db.engine.execute(text(query))
            self.OkMsgBox("information", "order success", "order added sucessfully!")
            self.setupUi(self.MainWindow)
    
        else:
            self.OkMsgBox("warning", "order failure", "selected book is currently unavailable!")

                     
 
    def deleteBook(self, book_id):
        queries = [
            f"DELETE FROM Book WHERE Book.id={book_id}",
            f"DELETE FROM book_publisher WHERE book_publisher.book_id={book_id}",
            f"DELETE FROM book_category WHERE book_category.book_id={book_id}",
            f"DELETE FROM book_order WHERE book_order.book_id={book_id}"
        ]

        for query in queries:
            db.engine.execute(text(query))
        self.OkMsgBox("information", "success", "book deleted sucessfully!")
        self.setupUi(self.MainWindow)


    def removeBooks(self):
        for obj in self.bookObjects:
            obj.deleteLater()

        for pic in self.pictures:
            pic.deleteLater()


    def search(self, input):    
        if input:
            self.input_list_search.setText(input)
            self.bookSearch = f"Book.name LIKE '%{input}%' OR Book.author LIKE '%{input}%' OR Publisher.name LIKE '%{input}%'" 
            self.removeBooks()
            self.fillBooks(self.baseQuery + f"\n HAVING " +  self.bookSearch)
            self.reloadFilters()
            
        else:
            self.input_list_search.setText('')
            self.bookSearch = None
            self.removeBooks()
            self.fillBooks(self.baseQuery)
            self.setupUi(self.MainWindow)   
        
   
    def bookFilter(self):

        selectedCategories = []

        for cat in self.bookCatBoxes:
            if cat.isChecked():
                selectedCategories.append(cat.objectName())

        selectedFilter = self.bookCombo.currentText()
        selectedPublisher = self.pubCombo1.currentText()

        donothing = False

        if selectedCategories:

            convertedList = f"('{selectedCategories[0]}')" if len(selectedCategories) == 1 else tuple(selectedCategories)
            
            query = f"SELECT Book.name,book_publisher.quantity,Book.author,Book.price,Publisher.name,"\
                    +"\n    ifnull(book_order.quantity, 0) as ordcount, publisher.id, Book.id, Book.picture_url"\
                    +"\n    FROM book_category"\
                    +"\n    JOIN Book ON Book.id=book_category.book_id"\
                    +"\n    JOIN Category ON Category.id=book_category.category_id"\
                    +"\n    JOIN book_publisher ON book_publisher.book_id=Book.id"\
                    +"\n    JOIN Publisher ON Publisher.id=book_publisher.publisher_id"\
                    +"\n    LEFT JOIN book_order ON book_order.book_id=book.id and book_order.publisher_id=Publisher.id"\
                    +f"\n   GROUP BY Book.id, Publisher.id HAVING Category.name IN {convertedList}"

        else:
            query = self.baseQuery
            if selectedFilter == 'select filter' and selectedPublisher == 'select publisher':
                donothing = True
                if self.bookSearch:                  
                    query = self.baseQuery + f"\n HAVING " +  self.bookSearch
                else:
                    query = self.baseQuery
               

        if not donothing:
            if self.bookSearch:
                query += f" AND ({self.bookSearch})"
        
            if selectedPublisher != 'select publisher':
                if selectedCategories:
                    query += f" AND Publisher.name='{selectedPublisher}'"
                else:
                    query += f"\n   HAVING Publisher.name='{selectedPublisher}'"

            if selectedFilter != 'select filter':
                if selectedFilter == 'most popular':
                    query += "\n ORDER BY ordcount DESC"
                elif selectedFilter == 'least popular':
                    query += "\n ORDER BY ordcount"
                elif selectedFilter == 'most expensive':
                    query += "\n ORDER BY Book.price DESC"
                elif selectedFilter == 'least expensive':
                    query += "\n ORDER BY Book.price"
                elif selectedFilter == 'newest':
                    query += "\n ORDER BY Book.date_added DESC"
                else:
                    query += "\n ORDER BY Book.date_added"
    
        
        self.removeBooks()
        self.fillBooks(query)



    def reloadFilters(self):
        self.bookCombo.setCurrentText('select filter')
        self.pubCombo1.setCurrentText('select publisher')

        for cat in self.bookCatBoxes:
            cat.setChecked(False)


    def addPublisher(self):
   
        inputDict = {
            'name': self.input_publisher_name.text(),
            'phone_number': self.input_publisher_number.text(),
            'website_url': self.input_publisher_web.text()
        }

        query = f"SELECT COUNT(*) FROM Publisher WHERE name='{inputDict['name']}'"
        result = db.engine.execute(text(query))
        publisher_exists = True if list(result)[0][0] == 1 else False

        if '' in inputDict.values():
            self.OkMsgBox("warning", "failure", "input filed/fields can not be empty!")

        elif publisher_exists:
            self.OkMsgBox("warning", "failure", "another publisher with this name found!")

        elif not inputDict['phone_number'].isdigit():
            self.OkMsgBox("warning", "failure", "entered phone number is not valid!")

        else:  
            query = f"INSERT INTO Publisher(name, phone_number, website_url)"\
                    +f"\n   VALUES('{inputDict['name']}', '{inputDict['phone_number']}', '{inputDict['website_url']}')"
            db.engine.execute(text(query))
            self.OkMsgBox("information", "success", "new publisher have been sucessfully added!")
            self.setupUi(self.MainWindow)           



    def addBook(self):
        
        inputDict = {
            'name': self.input_publisher_name_2.text(),
            'author': self.input_publisher_author.text(),
            'price': self.input_publisher_price.text(),
            'quantity': self.input_publisher_quantity.text(),
            'description': self.plainTextEdit_publisher_description.toPlainText(),
            'publisher': self.select_addbook_publisher.currentText(),
            'image_url': self.input_addbook_picture.text()
        }
        
        if not '' in inputDict.values():

            query = f"SELECT id FROM Book WHERE name='{inputDict['name']}'"
            matchedIds = list(db.engine.execute(text(query)))
            query = f"SELECT id FROM Publisher WHERE name='{inputDict['publisher']}'"
            publisher_id = list(db.engine.execute(text(query)))[0][0]

            if matchedIds:
                for mid in matchedIds:                    
                    query = f"SELECT EXISTS(SELECT * FROM book_publisher WHERE book_id={mid[0]} and publisher_id={publisher_id})"
                    result = list(db.engine.execute(query))[0][0]
                    if result == 0:
                        bookExists = False
                    else:
                        bookExists = True
                        break
            else:
                bookExists = False

           
            if bookExists:
                self.OkMsgBox("warning", "failure", "another book with this name and publisher found!")
            
            elif not inputDict['price'].isdigit():
                self.OkMsgBox("warning", "failure", "wrong price input!")

            elif not inputDict['quantity'].isdigit():
                self.OkMsgBox("warning", "failure", "wrong quantity input!")

            else:      
                try:
                    url = str(random.randint(9999,9999999))+"_"+os.path.basename(inputDict['image_url'])
                    shutil.copy(inputDict['image_url'], f"pictures/{url}")

                    query = f"INSERT INTO book(name, author, picture_url, price, description)"\
                            +f"\n   VALUES('{inputDict['name']}', '{inputDict['author']}', '{url}',"\
                            +f" {inputDict['price']}, '{inputDict['description']}')"
                    db.engine.execute(text(query))
                    query = f"SELECT id FROM Book WHERE name='{inputDict['name']}' ORDER BY date_added DESC LIMIT 1"
                    insertedBook_id = list(db.engine.execute(text(query)))[0][0]
                    query = f"INSERT INTO book_publisher(book_id, publisher_id, quantity)"\
                            +f"\n   VALUES({insertedBook_id}, {publisher_id}, {inputDict['quantity']})"
                    db.engine.execute(text(query))

                    for cat in self.categoryBoxes:
                        if cat.isChecked():
                            query = f"SELECT id FROM category WHERE name='{cat.objectName()}'"
                            category_id = list(db.engine.execute(text(query)))[0][0]
                            query = f"INSERT INTO book_category(book_id, category_id) VALUES({insertedBook_id}, {category_id})"
                            db.engine.execute(text(query))

                    
                    self.removeBooks()
                    self.fillBooks(self.baseQuery)

                except:
                    self.OkMsgBox("warning", "failure", "something went wrong while uploading photo!")

        else:
            self.OkMsgBox("warning", "failure", "input field/fields can not be empty!")
        


    def getPicture(self):
        url, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Book Photo', '', '(*.jpg *.gif *.png *.jpeg)')
        self.input_addbook_picture.setText(url)


    def fillUsers(self, query):
        users = list(db.engine.execute(text(query)))

        self.userObjects = []
        deleteButtons = []
        updateButtons = []
    
        for index, item in enumerate(users):   
            
            self.userObjects.append(QtWidgets.QFrame(self.scrollAreaWidgetContents_user_main))
            self.userObjects[index].setMinimumSize(QtCore.QSize(839, 65))   
            self.userObjects[index].setMaximumSize(QtCore.QSize(839, 65)) 
            self.userObjects[index].setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.userObjects[index].setFrameShadow(QtWidgets.QFrame.Raised)  
            self.userObjects[index].setObjectName("frame_user_" + str(index))

            self.gridLayoutWidget_5 = QtWidgets.QWidget(self.userObjects[index])
            self.gridLayoutWidget_5.setGeometry(QtCore.QRect(10, 10, 821, 52))
            self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")

            self.gridLayout_user_0 = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
            self.gridLayout_user_0.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_user_0.setObjectName("gridLayout_user_0")

            updateButtons.append(QtWidgets.QPushButton(self.gridLayoutWidget_5))
            updateButtons[index].setMaximumSize(QtCore.QSize(55, 16777215))
            deleteButtons.append(QtWidgets.QPushButton(self.gridLayoutWidget_5))
            deleteButtons[index].setMaximumSize(QtCore.QSize(55, 16777215))
            
            self.gridLayout_user_0.addWidget(updateButtons[index], 0, 6, 1, 1)
            self.label_user_address_0 = QtWidgets.QLabel(self.gridLayoutWidget_5)
            self.label_user_address_0.setMinimumSize(QtCore.QSize(100, 0))
            self.label_user_address_0.setMaximumSize(QtCore.QSize(150, 50))
            self.label_user_address_0.setObjectName("label_user_address_0")
            self.gridLayout_user_0.addWidget(self.label_user_address_0, 0, 4, 1, 1)
            self.gridLayout_user_0.addWidget(deleteButtons[index], 0, 7, 1, 1)
            self.label_user_lastname_0 = QtWidgets.QLabel(self.gridLayoutWidget_5)
            self.label_user_lastname_0.setMinimumSize(QtCore.QSize(83, 50))
            self.label_user_lastname_0.setMaximumSize(QtCore.QSize(83, 50))
            self.label_user_lastname_0.setObjectName("label_user_lastname_0")
            self.gridLayout_user_0.addWidget(self.label_user_lastname_0, 0, 1, 1, 1)
            self.label_user_isadmin_0 = QtWidgets.QLabel(self.gridLayoutWidget_5)
            self.label_user_isadmin_0.setMinimumSize(QtCore.QSize(55, 50))
            self.label_user_isadmin_0.setMaximumSize(QtCore.QSize(55, 50))
            self.label_user_isadmin_0.setObjectName("label_user_isadmin_0")
            self.gridLayout_user_0.addWidget(self.label_user_isadmin_0, 0, 5, 1, 1)
            self.label_user_phone_0 = QtWidgets.QLabel(self.gridLayoutWidget_5)
            self.label_user_phone_0.setMinimumSize(QtCore.QSize(83, 50))
            self.label_user_phone_0.setMaximumSize(QtCore.QSize(83, 50))
            self.label_user_phone_0.setObjectName("label_user_phone_0")
            self.gridLayout_user_0.addWidget(self.label_user_phone_0, 0, 3, 1, 1)
            self.label_user_username_0 = QtWidgets.QLabel(self.gridLayoutWidget_5)
            self.label_user_username_0.setMinimumSize(QtCore.QSize(83, 50))
            self.label_user_username_0.setMaximumSize(QtCore.QSize(83, 50))
            self.label_user_username_0.setObjectName("label_user_username_0")
            self.gridLayout_user_0.addWidget(self.label_user_username_0, 0, 2, 1, 1)
            self.label_user_name_0 = QtWidgets.QLabel(self.gridLayoutWidget_5)
            self.label_user_name_0.setMinimumSize(QtCore.QSize(83, 50))
            self.label_user_name_0.setMaximumSize(QtCore.QSize(83, 50))
            self.label_user_name_0.setObjectName("label_user_name_0")
            self.gridLayout_user_0.addWidget(self.label_user_name_0, 0, 0, 1, 1)
            
            self.gridLayout_9.addWidget(self.userObjects[index], index+1 , 0, 1, 1, QtCore.Qt.AlignTop)
            
            self.label_user_phone_0.setText(item[5])
            self.label_user_lastname_0.setText(item[3])
            self.label_user_name_0.setText(item[2])
            self.label_user_username_0.setText(item[1])
            self.label_user_address_0.setText(item[4])         
            deleteButtons[index].setText("Delete")
            
            if item[6] == 1:
                self.label_user_isadmin_0.setText('yes')
                updateButtons[index].setText('Demote')
                updateButtons[index].setObjectName("demote_" + str(item[0]))
            else:
                self.label_user_isadmin_0.setText('no')
                updateButtons[index].setText('Promote')
                updateButtons[index].setObjectName("promote_" + str(item[0]))

            deleteButtons[index].setObjectName('delete_' + str(item[0]))

            updateButtons[index].clicked.connect(lambda ch, index=index: 
                        self.updateUser(updateButtons[index].objectName().split('_')[0], updateButtons[index].objectName().split('_')[1]))
            deleteButtons[index].clicked.connect(lambda ch, index=index:
                        self.deleteUser(updateButtons[index].objectName().split('_')[1]))


    def usersSearch(self, input):
        if input:
            self.input_user_search.setText(input)
            self.userSearch = f"User.username LIKE '%{input}%' OR Customer.first_name LIKE '%{input}%' OR Customer.last_name LIKE '%{input}%'" 
            self.removeUsers()
            self.fillUsers(self.userQuery + f"\n HAVING " +  self.userSearch)
            self.usersCombo.setCurrentText('select filter')
            
        else:
            self.input_user_search.setText('')
            self.userSearch = None
            self.removeUsers()
            self.fillUsers(self.userQuery)
            # self.setupUi(MainWindow)  


    def userFilter(self):
        
        selectedFilter = self.usersCombo.currentText()
        query = self.userQuery

        if self.userSearch:
            q = query + "\n HAVING " +  self.userSearch
        else:
            q = query
       
        if selectedFilter != 'select filter':   
            if selectedFilter == 'admin':
                query = q + " AND User.is_admin=1" if self.userSearch else q + "\n  HAVING User.is_admin=1"                                        
            elif selectedFilter == 'most loyal':
                query = q + "\n ORDER BY Total DESC"
            elif selectedFilter == 'least loyal':
                query = q + "\n ORDER BY Total"
            elif selectedFilter == 'newest':
                query = q + "\n ORDER BY User.date_JOINed DESC"
            else:
                query = q + "\n ORDER BY User.date_JOINed"

        self.removeUsers()
        self.fillUsers(query)


    def removeUsers(self):
        for obj in self.userObjects:
            obj.deleteLater()

            
    def deleteUser(self, id):     

        queries = [
            f"DELETE FROM User WHERE id={id}",
            f"DELETE FROM Customer WHERE user_id={id}",
            f"DELETE FROM book_order WHERE customer_id={id}"
        ]

        for query in queries:
            db.engine.execute(text(query))

        # self.removeUsers()
        self.OkMsgBox("information", "success", "user deleted sucessfully!")
        self.setupUi(self.MainWindow)
        # self.fillUsers(self.userQuery)


    def updateUser(self, action, id):
        is_admin = 1 if action == 'promote' else 0
        
        query = f"UPDATE User SET is_admin={is_admin} WHERE id={id}"
        db.engine.execute(text(query))

        self.OkMsgBox("information", "success", "user updates sucessfully!")
        self.removeUsers()
        self.fillUsers(self.userQuery)

            
    def fillInventory(self):
        
        objects = []

        titles = [
            '📈 Total Number Of Books ',
            '📈 Number Of Sold Books ',
            '💰 Total Books Price ',
            '💰 Total Sold Books Price ',
            '💰 Total Sold Books Price(last 7 days) ',
            '💰 Total Sold Books Price(last 30 days) '
        ]
        queries = [
            "SELECT SUM(book_publisher.quantity) FROM Book JOIN book_publisher ON Book.id=book_publisher.book_id",
            "SELECT SUM(quantity) FROM book_order",
            "SELECT SUM(price) FROM Book",
            "SELECT SUM(Book.price) FROM Book JOIN book_order ON Book.id=book_order.book_id",
            
            "SELECT SUM(Book.price) FROM Book JOIN book_order ON Book.id=book_order.book_id"\
            +"\n    WHERE book_order.date_added>=(SELECT DATETIME('now', '-7 day'))",

            "SELECT SUM(Book.price) FROM Book JOIN book_order ON Book.id=book_order.book_id"\
            +"\n    WHERE book_order.date_added>=(SELECT DATETIME('now', '-30 day'))"

        ]

        for index in range(0, len(titles)):

            objects.append(QtWidgets.QFrame(self.verticalLayoutWidget))
            objects[index].setFrameShape(QtWidgets.QFrame.StyledPanel)
            objects[index].setFrameShadow(QtWidgets.QFrame.Raised)
            objects[index].setObjectName("frame_inventory")

            self.label_inventory_title_0 = QtWidgets.QLabel(objects[index])
            self.label_inventory_title_0.setGeometry(QtCore.QRect(20, 10, 200, 41))
            self.label_inventory_title_0.setObjectName("label_inventory_title")

            self.label_inventory_0 = QtWidgets.QLabel(objects[index])
            self.label_inventory_0.setGeometry(QtCore.QRect(250, 10, 180, 40))
            self.label_inventory_0.setObjectName("label_inventory_0")

            self.verticalLayout_inventory_main.addWidget(objects[index]) 

            qResult = list(db.engine.execute(queries[index]))[0][0]

            self.label_inventory_title_0.setText(titles[index]) 
            if index>1:
                qResult = '{:,}'.format(qResult)
                self.label_inventory_0.setText(str(qResult) + "💲")
            else:
                qResult = '{:,}'.format(qResult)
                self.label_inventory_0.setText(str(qResult))

   


    def fillOrders(self):

        query = "SELECT Book.name, User.username, Publisher.name, book_order.date_added, book_order.quantity, Book.price"\
                +"\n    FROM book_publisher"\
                +"\n    JOIN Book on book_publisher.book_id=Book.id"\
                +"\n    JOIN Publisher on Publisher.id=book_publisher.publisher_id"\
                +"\n    JOIN book_order on book_order.book_id=book.id and book_order.publisher_id=Publisher.id"\
                +"\n    JOIN Customer on customer.user_id=book_order.customer_id"\
                +"\n    JOIN User on User.id=Customer.user_id"
        
        if not self.is_admin:
            query += f"\n WHERE User.username='{self.username}'"
        

        orders = list(db.engine.execute(text(query)))

        self.tableWidget_order.setRowCount(len(orders))

        for row in range(0, len(orders)):

            for col in range(0, 7):
                
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget_order.setItem(row, col, item)

                totalPrice = orders[row][4] * orders[row][5]

                if col == 6:
                    item.setText(str('{:,}'.format(totalPrice)))
                else:
                    if col>3 and not col==6:
                        item.setText(str('{:,}'.format(orders[row][col])))
                    else:
                        item.setText(str(orders[row][col]))


    def fillInfo(self):
        username = self.username
        query = f"SELECT User.username, Customer.first_name, Customer.last_name, Customer.phone_number,"\
                +"\n    Customer.address, User.password FROM User JOIN Customer"\
                +f"\n    ON User.id=Customer.user_id Where User.username = '{username}'"
        
        infoData = list(db.engine.execute(text(query)))[0]
        self.initialInfo = [info for info in infoData]

        self.input_user_info_username.setText(infoData[0])
        self.input_user_info_name.setText(infoData[1])
        self.input_user_info_lastname.setText(infoData[2])
        self.input_user_info_number.setText(infoData[3])
        self.input_user_info_address.setPlainText(infoData[4])
        self.input_user_info_password.setText(infoData[5])


    def updateInfo(self):

        newData = [
            self.input_user_info_username.text(),
            self.input_user_info_name.text(),
            self.input_user_info_lastname.text(),
            self.input_user_info_number.text(),
            self.input_user_info_address.toPlainText(),
            self.input_user_info_password.text()
        ]
       
        nochanges = newData == self.initialInfo

        if not nochanges:
            query = f"UPDATE User SET username='{newData[0]}', password='{newData[5]}' WHERE id='{self.user_id}'"
            db.engine.execute(text(query))
            query = f"UPDATE Customer SET first_name='{newData[1]}', last_name='{newData[2]}',"\
                    +f"\n   phone_number='{newData[3]}', address='{newData[4]}' WHERE Customer.user_id={self.user_id}"
            db.engine.execute(text(query))
            self.OkMsgBox("information", "success", "user info updated!")
            self.initialInfo = newData
            self.setupUi(self.MainWindow)
        else:
            self.OkMsgBox("warning", "failure", "no changes detected!")
            


    # layout functions
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(895, 648)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(9, 39, 891, 581))
        self.tabWidget.setMinimumSize(QtCore.QSize(786, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(500000, 50000))
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.list = QtWidgets.QWidget()
        self.list.setObjectName("list")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.list)
        self.gridLayout_6.setObjectName("gridLayout_6")
        # -------------------------------------book display tab--------------------------------------------------------
        self.frame_list_main = QtWidgets.QFrame(self.list)
        self.frame_list_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_list_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_list_main.setObjectName("frame_list_main")
        self.scrollArea_book_list = QtWidgets.QScrollArea(self.frame_list_main)
        self.scrollArea_book_list.setGeometry(QtCore.QRect(10, 100, 751, 451))
        self.scrollArea_book_list.setWidgetResizable(True)
        self.scrollArea_book_list.setObjectName("scrollArea_book_list")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 749, 449))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setObjectName("gridLayout_5")
        # fill books
        self.fillBooks(self.baseQuery)
  
        self.scrollArea_book_list.setWidget(self.scrollAreaWidgetContents)
        self.input_list_search = QtWidgets.QLineEdit(self.frame_list_main)
        self.input_list_search.setGeometry(QtCore.QRect(540, 20, 220, 24))
        self.input_list_search.setObjectName("input_list_search")
        self.btn_list_search = QtWidgets.QPushButton(self.frame_list_main)
        self.btn_list_search.setGeometry(QtCore.QRect(450, 20, 80, 24))
        self.btn_list_search.setObjectName("btn_list_search")
        # search button event listener
        self.btn_list_search.clicked.connect(lambda: self.search(self.input_list_search.text()))   
        # filter combo boxes
        self.bookCombo = QtWidgets.QComboBox(self.frame_list_main)
        self.bookCombo.setGeometry(QtCore.QRect(10, 20, 100, 20))
        bookFilters = ['select filter', 'newest', 'oldest', 'most expensive', 'least expensive', 'most popular', 'least popular']
        self.bookCombo.addItems(bookFilters)
        # publisher selection combo boxes
        self.pubCombo1 = QtWidgets.QComboBox(self.frame_list_main)
        self.pubCombo1.setGeometry(QtCore.QRect(10, 45, 100, 20))
        publishers = self.getPublishers()
        self.pubCombo1.addItem("select publisher")
        self.pubCombo1.addItems(publishers)
        # check boxes display function call
        self.bookCatBoxes = []
        self.placeCatBoxes(0, 20, 45, 80, 22)
        # filter button creation
        self.btn_list_show = QtWidgets.QPushButton(self.frame_list_main)
        self.btn_list_show.setGeometry(QtCore.QRect(10, 70, 75, 24))
        self.btn_list_show.setObjectName("btn_list_show")
        # filter button event listener
        self.btn_list_show.clicked.connect(lambda: self.bookFilter())
      
        self.gridLayout_6.addWidget(self.frame_list_main, 0, 0, 1, 1)
        self.tabWidget.addTab(self.list, "")
        # -------------------------------------categories tab--------------------------------------------------------
        if self.is_admin:

            # -------------------------------------add publisher tab--------------------------------------------------------
            self.publisher = QtWidgets.QWidget()
            self.publisher.setObjectName("publisher")
            self.frame_publisher_add = QtWidgets.QFrame(self.publisher)
            self.frame_publisher_add.setGeometry(QtCore.QRect(269, 102, 351, 211))
            self.frame_publisher_add.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_publisher_add.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_publisher_add.setObjectName("frame_publisher_add")
            self.formLayoutWidget = QtWidgets.QWidget(self.frame_publisher_add)
            self.formLayoutWidget.setGeometry(QtCore.QRect(19, 29, 311, 181))
            self.formLayoutWidget.setObjectName("formLayoutWidget")
            self.formLayout_publisher_main = QtWidgets.QFormLayout(self.formLayoutWidget)
            self.formLayout_publisher_main.setContentsMargins(0, 0, 0, 0)
            self.formLayout_publisher_main.setObjectName("formLayout_publisher_main")
            self.label_publisher_name = QtWidgets.QLabel(self.formLayoutWidget)
            self.label_publisher_name.setObjectName("label_publisher_name")
            self.formLayout_publisher_main.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_publisher_name)
            self.input_publisher_name = QtWidgets.QLineEdit(self.formLayoutWidget)
            self.input_publisher_name.setObjectName("input_publisher_name")
            self.formLayout_publisher_main.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_publisher_name)
            self.label_publisher_number = QtWidgets.QLabel(self.formLayoutWidget)
            self.label_publisher_number.setObjectName("label_publisher_number")
            self.formLayout_publisher_main.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_publisher_number)
            self.input_publisher_number = QtWidgets.QLineEdit(self.formLayoutWidget)
            self.input_publisher_number.setObjectName("input_publisher_number")
            self.formLayout_publisher_main.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.input_publisher_number)
            self.label_publisher_web = QtWidgets.QLabel(self.formLayoutWidget)
            self.label_publisher_web.setObjectName("label_publisher_web")
            self.formLayout_publisher_main.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_publisher_web)
            self.input_publisher_web = QtWidgets.QLineEdit(self.formLayoutWidget)
            self.input_publisher_web.setObjectName("input_publisher_web")
            self.formLayout_publisher_main.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.input_publisher_web)
            self.btn_publisher_add = QtWidgets.QPushButton(self.formLayoutWidget)
            self.btn_publisher_add.setObjectName("btn_publisher_add")
            self.formLayout_publisher_main.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.btn_publisher_add)
            # new publisher button event listener
            self.btn_publisher_add.clicked.connect(lambda: self.addPublisher())
            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.formLayout_publisher_main.setItem(1, QtWidgets.QFormLayout.FieldRole, spacerItem)
            spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.formLayout_publisher_main.setItem(6, QtWidgets.QFormLayout.FieldRole, spacerItem1)
            spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.formLayout_publisher_main.setItem(4, QtWidgets.QFormLayout.FieldRole, spacerItem2)
            spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.formLayout_publisher_main.setItem(8, QtWidgets.QFormLayout.FieldRole, spacerItem3)
            self.label_publisher_error = QtWidgets.QLabel(self.publisher)
            self.label_publisher_error.setGeometry(QtCore.QRect(580, 410, 271, 31))
            self.label_publisher_error.setObjectName("label_publisher_error")
            self.label_publisher_title = QtWidgets.QLabel(self.publisher)
            self.label_publisher_title.setGeometry(QtCore.QRect(340, 10, 181, 41))
            self.label_publisher_title.setObjectName("label_publisher_title")
            self.tabWidget.addTab(self.publisher, "")
            # -------------------------------------add new book tab--------------------------------------------------------
            self.add = QtWidgets.QWidget()
            self.add.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.add.setObjectName("add")
            self.gridLayout_3 = QtWidgets.QGridLayout(self.add)
            self.gridLayout_3.setObjectName("gridLayout_3")
            self.label_addbook_error = QtWidgets.QLabel(self.add)
            self.label_addbook_error.setObjectName("label_addbook_error")
            self.gridLayout_3.addWidget(self.label_addbook_error, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
            self.gridLayout_addbook_main = QtWidgets.QGridLayout()
            self.gridLayout_addbook_main.setObjectName("gridLayout_addbook_main")
            self.label_addbook_name = QtWidgets.QLabel(self.add)
            self.label_addbook_name.setObjectName("label_addbook_name")
            self.gridLayout_addbook_main.addWidget(self.label_addbook_name, 0, 0, 1, 1)
            self.label_addbook_picture = QtWidgets.QLabel(self.add)
            self.label_addbook_picture.setObjectName("label_addbook_picture")
            self.gridLayout_addbook_main.addWidget(self.label_addbook_picture, 7, 0, 1, 1)
            self.label_addbook_author = QtWidgets.QLabel(self.add)
            self.label_addbook_author.setObjectName("label_addbook_author")
            self.gridLayout_addbook_main.addWidget(self.label_addbook_author, 1, 0, 1, 1)
            self.input_publisher_name_2 = QtWidgets.QLineEdit(self.add)
            self.input_publisher_name_2.setObjectName("input_publisher_name_2")
            self.gridLayout_addbook_main.addWidget(self.input_publisher_name_2, 0, 1, 1, 1)
            self.input_publisher_author = QtWidgets.QLineEdit(self.add)
            self.input_publisher_author.setObjectName("input_publisher_author")
            self.gridLayout_addbook_main.addWidget(self.input_publisher_author, 1, 1, 1, 1)      
            self.label_addbook_description = QtWidgets.QLabel(self.add)
            self.label_addbook_description.setObjectName("label_addbook_description")
            self.gridLayout_addbook_main.addWidget(self.label_addbook_description, 4, 0, 1, 1)
            self.plainTextEdit_publisher_description = QtWidgets.QPlainTextEdit(self.add)
            self.plainTextEdit_publisher_description.setObjectName("plainTextEdit_publisher_description")
            self.gridLayout_addbook_main.addWidget(self.plainTextEdit_publisher_description, 4, 1, 1, 1)
            # publisher selection combo box
            self.select_addbook_publisher = QtWidgets.QComboBox(self.add)
            self.select_addbook_publisher.setObjectName("select_addbook_publisher")       
            self.select_addbook_publisher.addItems(publishers)
            self.gridLayout_addbook_main.addWidget(self.select_addbook_publisher, 5, 1, 1, 1)

            self.input_publisher_quantity = QtWidgets.QLineEdit(self.add)
            self.input_publisher_quantity.setObjectName("input_publisher_quantity")
            self.gridLayout_addbook_main.addWidget(self.input_publisher_quantity, 3, 1, 1, 1)
            self.scrollArea_addbook_category = QtWidgets.QScrollArea(self.add)
            self.scrollArea_addbook_category.setWidgetResizable(True)
            self.scrollArea_addbook_category.setObjectName("scrollArea_addbook_category")
            self.scrollAreaWidgetContents_addbook_main = QtWidgets.QWidget()
            self.scrollAreaWidgetContents_addbook_main.setGeometry(QtCore.QRect(0, 0, 777, 72))
            self.scrollAreaWidgetContents_addbook_main.setObjectName("scrollAreaWidgetContents_addbook_main")
            # check boxes display function call
            self.categoryBoxes = []
            self.placeCatBoxes(1, 10, 2, 83, 22)

            self.scrollArea_addbook_category.setWidget(self.scrollAreaWidgetContents_addbook_main)
            self.gridLayout_addbook_main.addWidget(self.scrollArea_addbook_category, 6, 1, 1, 1)
            self.label_addbook_quantity = QtWidgets.QLabel(self.add)
            self.label_addbook_quantity.setObjectName("label_addbook_quantity")
            self.gridLayout_addbook_main.addWidget(self.label_addbook_quantity, 3, 0, 1, 1)
            self.btn_addbook_submit = QtWidgets.QPushButton(self.add)
            self.btn_addbook_submit.setObjectName("btn_addbook_submit")
            self.gridLayout_addbook_main.addWidget(self.btn_addbook_submit, 8, 1, 1, 1)
            # add book button event listener
            self.btn_addbook_submit.clicked.connect(lambda: self.addBook())

            self.label_addbook_publisher = QtWidgets.QLabel(self.add)
            self.label_addbook_publisher.setObjectName("label_addbook_publisher")
            self.gridLayout_addbook_main.addWidget(self.label_addbook_publisher, 5, 0, 1, 1)
            self.input_publisher_price = QtWidgets.QLineEdit(self.add)
            self.input_publisher_price.setObjectName("input_publisher_price")
            self.gridLayout_addbook_main.addWidget(self.input_publisher_price, 2, 1, 1, 1)
            self.label_addbook_price = QtWidgets.QLabel(self.add)
            self.label_addbook_price.setObjectName("label_addbook_price")
            self.gridLayout_addbook_main.addWidget(self.label_addbook_price, 2, 0, 1, 1)
            self.frame_addbook_picture = QtWidgets.QFrame(self.add)
            self.frame_addbook_picture.setMinimumSize(QtCore.QSize(0, 38))
            self.frame_addbook_picture.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.frame_addbook_picture.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_addbook_picture.setObjectName("frame_addbook_picture")
            self.btn_addbook_broswer = QtWidgets.QPushButton(self.frame_addbook_picture)
            self.btn_addbook_broswer.setGeometry(QtCore.QRect(510, 10, 80, 21))
            self.btn_addbook_broswer.setObjectName("btn_addbook_broswer")
            # addBook browse picture button event listener
            self.btn_addbook_broswer.clicked.connect(lambda: self.getPicture())

            self.input_addbook_picture = QtWidgets.QLineEdit(self.frame_addbook_picture)
            self.input_addbook_picture.setGeometry(QtCore.QRect(0, 10, 500, 21))
            self.input_addbook_picture.setMinimumSize(QtCore.QSize(500, 0))
            self.input_addbook_picture.setObjectName("input_addbook_picture")      
            self.gridLayout_addbook_main.addWidget(self.frame_addbook_picture, 7, 1, 1, 1)
            self.gridLayout_3.addLayout(self.gridLayout_addbook_main, 2, 0, 1, 1)
            self.label_addbook_title = QtWidgets.QLabel(self.add)
            self.label_addbook_title.setObjectName("label_addbook_title")
            self.gridLayout_3.addWidget(self.label_addbook_title, 1, 0, 1, 1)
            self.tabWidget.addTab(self.add, "")
            # -------------------------------------users tab--------------------------------------------------------
            self.users = QtWidgets.QWidget()
            self.users.setObjectName("users")
            self.gridLayout_8 = QtWidgets.QGridLayout(self.users)
            self.gridLayout_8.setObjectName("gridLayout_8")
            self.frame_user_main = QtWidgets.QFrame(self.users)
            self.frame_user_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_user_main.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_user_main.setObjectName("frame_user_main")
            self.input_user_search = QtWidgets.QLineEdit(self.frame_user_main)
            self.input_user_search.setGeometry(QtCore.QRect(540, 20, 220, 24))
            self.input_user_search.setObjectName("input_user_search")
            self.btn_user_search = QtWidgets.QPushButton(self.frame_user_main)
            self.btn_user_search.setGeometry(QtCore.QRect(450, 20, 80, 24))
            self.btn_user_search.setObjectName("btn_user_search")
            # user search event handler
            self.btn_user_search.clicked.connect(lambda: self.usersSearch(self.input_user_search.text()))   

            self.scrollArea_user = QtWidgets.QScrollArea(self.frame_user_main)
            self.scrollArea_user.setGeometry(QtCore.QRect(10, 70, 871, 461))
            self.scrollArea_user.setWidgetResizable(True)
            self.scrollArea_user.setObjectName("scrollArea_user")
            self.scrollAreaWidgetContents_user_main = QtWidgets.QWidget()
            self.scrollAreaWidgetContents_user_main.setGeometry(QtCore.QRect(0, 0, 869, 459))
            self.scrollAreaWidgetContents_user_main.setObjectName("scrollAreaWidgetContents_user_main")
            self.gridLayout_9 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_user_main)
            self.gridLayout_9.setObjectName("gridLayout_9")
            # fill users tab
            self.fillUsers(self.userQuery)

            self.frame_user_header = QtWidgets.QFrame(self.scrollAreaWidgetContents_user_main)
            self.frame_user_header.setEnabled(True)
            self.frame_user_header.setMinimumSize(QtCore.QSize(839, 65))
            self.frame_user_header.setMaximumSize(QtCore.QSize(730, 65))
            self.frame_user_header.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.frame_user_header.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_user_header.setObjectName("frame_user_header")
            self.gridLayoutWidget_2 = QtWidgets.QWidget(self.frame_user_header)
            self.gridLayoutWidget_2.setGeometry(QtCore.QRect(9, 9, 821, 52))
            self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
            self.gridLayout_user_header = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
            self.gridLayout_user_header.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_user_header.setObjectName("gridLayout_user_header")
            self.label_user_phone = QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.label_user_phone.setMinimumSize(QtCore.QSize(83, 50))
            self.label_user_phone.setMaximumSize(QtCore.QSize(83, 50))
            self.label_user_phone.setObjectName("label_user_phone")
            self.gridLayout_user_header.addWidget(self.label_user_phone, 0, 3, 1, 1)
            self.label_user_name = QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.label_user_name.setMinimumSize(QtCore.QSize(83, 50))
            self.label_user_name.setMaximumSize(QtCore.QSize(83, 50))
            self.label_user_name.setObjectName("label_user_name")
            self.gridLayout_user_header.addWidget(self.label_user_name, 0, 0, 1, 1)
            self.label_user_delete = QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.label_user_delete.setMinimumSize(QtCore.QSize(55, 50))
            self.label_user_delete.setMaximumSize(QtCore.QSize(55, 16777215))
            self.label_user_delete.setObjectName("label_user_delete")
            self.gridLayout_user_header.addWidget(self.label_user_delete, 0, 7, 1, 1)
            self.label_user_lastname = QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.label_user_lastname.setMinimumSize(QtCore.QSize(83, 50))
            self.label_user_lastname.setMaximumSize(QtCore.QSize(83, 50))
            self.label_user_lastname.setObjectName("label_user_lastname")
            self.gridLayout_user_header.addWidget(self.label_user_lastname, 0, 1, 1, 1)
            self.label_user_username = QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.label_user_username.setMinimumSize(QtCore.QSize(83, 50))
            self.label_user_username.setMaximumSize(QtCore.QSize(83, 50))
            self.label_user_username.setObjectName("label_user_username")
            self.gridLayout_user_header.addWidget(self.label_user_username, 0, 2, 1, 1)
            self.label_user_update = QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.label_user_update.setMinimumSize(QtCore.QSize(55, 50))
            self.label_user_update.setMaximumSize(QtCore.QSize(55, 16777215))
            self.label_user_update.setObjectName("label_user_update")
            self.gridLayout_user_header.addWidget(self.label_user_update, 0, 6, 1, 1)
            self.label_user_address = QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.label_user_address.setMinimumSize(QtCore.QSize(150, 0))
            self.label_user_address.setMaximumSize(QtCore.QSize(150, 50))
            self.label_user_address.setObjectName("label_user_address")
            self.gridLayout_user_header.addWidget(self.label_user_address, 0, 4, 1, 1)
            self.label_user_isadmin = QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.label_user_isadmin.setMinimumSize(QtCore.QSize(55, 50))
            self.label_user_isadmin.setMaximumSize(QtCore.QSize(55, 16777215))
            self.label_user_isadmin.setObjectName("label_user_isadmin")
            self.gridLayout_user_header.addWidget(self.label_user_isadmin, 0, 5, 1, 1)
            self.gridLayout_9.addWidget(self.frame_user_header, 0, 0, 1, 1, QtCore.Qt.AlignTop)
            self.scrollArea_user.setWidget(self.scrollAreaWidgetContents_user_main)

            self.btn_user_show = QtWidgets.QPushButton(self.frame_user_main)
            self.btn_user_show.setGeometry(QtCore.QRect(150, 20, 75, 24))
            self.btn_user_show.setObjectName("btn_user_show")
            # filter button creation
            userFilters = ['admin', 'newest', 'oldest', 'most loyal', 'least loyal']
            self.usersCombo = QtWidgets.QComboBox(self.frame_user_main)
            self.usersCombo.setGeometry(QtCore.QRect(20, 20, 100, 24))
            self.usersCombo.addItem("select filter")
            self.usersCombo.addItems(userFilters)
            # filter button event listener
            self.btn_user_show.clicked.connect(lambda: self.userFilter())

            self.gridLayout_8.addWidget(self.frame_user_main, 0, 0, 1, 1)
            self.tabWidget.addTab(self.users, "")
        # -------------------------------------orders tab--------------------------------------------------------
        self.orders = QtWidgets.QWidget()
        self.orders.setObjectName("orders")
        self.tableWidget_order = QtWidgets.QTableWidget(self.orders)
        self.tableWidget_order.setGeometry(QtCore.QRect(34, 50, 811, 481))
        self.tableWidget_order.setObjectName("tableWidget_order")
        self.tableWidget_order.setColumnCount(7)
        # orders columns creation
        columns = ['Book', 'User', 'Publisher', 'Date Added', 'Quantity', 'Price', 'Total']
        for column in range(0, 7):
            self.tableWidget_order.setHorizontalHeaderItem(column, QtWidgets.QTableWidgetItem())
            item = self.tableWidget_order.horizontalHeaderItem(column)
            item.setText(columns[column])

        # fill Orders tab
        self.fillOrders()

        self.label_order_title = QtWidgets.QLabel(self.orders)
        self.label_order_title.setGeometry(QtCore.QRect(320, 9, 181, 41))
        self.label_order_title.setObjectName("label_order_title")
        self.tabWidget.addTab(self.orders, "")
        # -------------------------------------inventory tab--------------------------------------------------------
        if self.is_admin:
            self.inventory = QtWidgets.QWidget()
            self.inventory.setObjectName("inventory")
            self.scrollArea_inventory_main = QtWidgets.QScrollArea(self.inventory)
            self.scrollArea_inventory_main.setGeometry(QtCore.QRect(155, 89, 601, 411))
            self.scrollArea_inventory_main.setWidgetResizable(True)
            self.scrollArea_inventory_main.setObjectName("scrollArea_inventory_main")
            self.scrollAreaWidgetContents_inventory = QtWidgets.QWidget()
            self.scrollAreaWidgetContents_inventory.setGeometry(QtCore.QRect(0, 0, 599, 409))
            self.scrollAreaWidgetContents_inventory.setObjectName("scrollAreaWidgetContents_inventory")
            self.verticalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_inventory)
            self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 581, 391))
            self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.verticalLayout_inventory_main = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
            self.verticalLayout_inventory_main.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_inventory_main.setObjectName("verticalLayout_inventory_main")
            # inventory tab data fill
            self.fillInventory()

            self.scrollArea_inventory_main.setWidget(self.scrollAreaWidgetContents_inventory)
            self.label_inventory_title = QtWidgets.QLabel(self.inventory)
            self.label_inventory_title.setGeometry(QtCore.QRect(340, 30, 231, 41))
            self.label_inventory_title.setObjectName("label_inventory_title")
            self.tabWidget.addTab(self.inventory, "")
        else:
            # -------------------------------------user info tab--------------------------------------------------------
            self.info = QtWidgets.QWidget()
            self.info.setObjectName("info")
            self.user_info_fram = QtWidgets.QFrame(self.info)
            self.user_info_fram.setGeometry(QtCore.QRect(140, 90, 521, 421))
            self.user_info_fram.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.user_info_fram.setFrameShadow(QtWidgets.QFrame.Raised)
            self.user_info_fram.setObjectName("user_info_fram")
            self.formLayoutWidget_2 = QtWidgets.QWidget(self.user_info_fram)
            self.formLayoutWidget_2.setGeometry(QtCore.QRect(19, 19, 481, 351))
            self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
            self.formLayout_user_info = QtWidgets.QFormLayout(self.formLayoutWidget_2)
            self.formLayout_user_info.setContentsMargins(0, 0, 0, 0)
            self.formLayout_user_info.setObjectName("formLayout_user_info")
            self.label_info_name = QtWidgets.QLabel(self.formLayoutWidget_2)
            self.label_info_name.setObjectName("label_info_name")
            self.formLayout_user_info.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_info_name)
            self.label_user_info_lastname = QtWidgets.QLabel(self.formLayoutWidget_2)
            self.label_user_info_lastname.setObjectName("label_user_info_lastname")
            self.formLayout_user_info.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_user_info_lastname)
            self.label_user_info_number = QtWidgets.QLabel(self.formLayoutWidget_2)
            self.label_user_info_number.setObjectName("label_user_info_number")
            self.formLayout_user_info.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_user_info_number)
            self.label_user_info_address = QtWidgets.QLabel(self.formLayoutWidget_2)
            self.label_user_info_address.setObjectName("label_user_info_address")
            self.formLayout_user_info.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_user_info_address)
            self.input_user_info_lastname = QtWidgets.QLineEdit(self.formLayoutWidget_2)
            self.input_user_info_lastname.setObjectName("input_user_info_lastname")
            self.formLayout_user_info.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_user_info_lastname)
            self.input_user_info_name = QtWidgets.QLineEdit(self.formLayoutWidget_2)
            self.input_user_info_name.setObjectName("input_user_info_name")
            self.formLayout_user_info.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_user_info_name)
            self.input_user_info_number = QtWidgets.QLineEdit(self.formLayoutWidget_2)
            self.input_user_info_number.setObjectName("input_user_info_number")
            self.formLayout_user_info.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.input_user_info_number)
            self.input_user_info_address = QtWidgets.QPlainTextEdit(self.formLayoutWidget_2)
            self.input_user_info_address.setObjectName("input_user_info_address")
            self.formLayout_user_info.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.input_user_info_address)
            self.label_user_info_username = QtWidgets.QLabel(self.formLayoutWidget_2)
            self.label_user_info_username.setObjectName("label_user_info_username")
            self.formLayout_user_info.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_user_info_username)
            self.input_user_info_username = QtWidgets.QLineEdit(self.formLayoutWidget_2)
            self.input_user_info_username.setObjectName("input_user_info_username")
            self.formLayout_user_info.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.input_user_info_username)
            self.label_user_info_password = QtWidgets.QLabel(self.formLayoutWidget_2)
            self.label_user_info_password.setObjectName("label_user_info_password")
            self.formLayout_user_info.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_user_info_password)
            self.input_user_info_password = QtWidgets.QLineEdit(self.formLayoutWidget_2)
            self.input_user_info_password.setObjectName("input_user_info_password")
            self.formLayout_user_info.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.input_user_info_password)
            self.btn_user_info_update = QtWidgets.QPushButton(self.user_info_fram)
            self.btn_user_info_update.setGeometry(QtCore.QRect(230, 380, 80, 24))
            self.btn_user_info_update.setObjectName("btn_user_info_update")
            self.label_user_info_title = QtWidgets.QLabel(self.info)
            self.label_user_info_title.setGeometry(QtCore.QRect(290, 20, 231, 41))
            self.label_user_info_title.setObjectName("label_user_info_title")
            self.tabWidget.addTab(self.info, "")
            # fill info tab
            self.fillInfo()
            # update info event handler
            self.btn_user_info_update.clicked.connect(lambda: self.updateInfo())

        self.btn_logout = QtWidgets.QPushButton(self.centralwidget)
        self.btn_logout.setGeometry(QtCore.QRect(800, 10, 80, 24))
        self.btn_logout.setObjectName("btn_logout")
        self.btn_logout.clicked.connect(self.logout)

        self.label_login_username = QtWidgets.QLabel(self.centralwidget)
        self.label_login_username.setGeometry(QtCore.QRect(10, 10, 201, 16))
        self.label_login_username.setObjectName("label_login_username")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.btn_list_show.clicked.connect(MainWindow.update)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Online Shop ❤️"))
        # book tab   
        self.btn_list_search.setText(_translate("MainWindow", "🔎 Search"))
        self.btn_list_show.setText(_translate("MainWindow", "✂️ Filter"))         
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.list), _translate("MainWindow", "📚 Books"))
        # orders tab
        __sortingEnabled = self.tableWidget_order.isSortingEnabled()
        self.tableWidget_order.setSortingEnabled(False)       
        self.tableWidget_order.setSortingEnabled(__sortingEnabled)
        self.label_order_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">All Orders</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.orders), _translate("MainWindow", "🛒 Orders"))
        if self.is_admin:

            self.label_publisher_name.setText(_translate("MainWindow", "Name"))
            self.label_publisher_number.setText(_translate("MainWindow", "Phone Number"))
            self.label_publisher_web.setText(_translate("MainWindow", "Web site"))
            self.btn_publisher_add.setText(_translate("MainWindow", "Add"))
            # self.label_publisher_name_0.setText(_translate("MainWindow", "tolo"))
            # self.btn_publisher_delete_0.setText(_translate("MainWindow", "Delete"))
            # self.label_publisher_error.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Error</p></body></html>"))
            self.label_publisher_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Publishers</span></p></body></html>"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.publisher), _translate("MainWindow", "📝 Add Publisher"))
            # add book tab
            # self.label_addbook_error.setText(_translate("MainWindow", "error"))
            self.label_addbook_name.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">name</span></p></body></html>"))
            self.label_addbook_picture.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Picture</span></p></body></html>"))
            self.label_addbook_author.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">author</span></p></body></html>"))
            self.label_addbook_description.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">description</span></p><p align=\"center\"><br/></p></body></html>"))
            self.label_addbook_quantity.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">quantity</span></p></body></html>"))
            self.btn_addbook_submit.setText(_translate("MainWindow", "Submit"))
            self.label_addbook_publisher.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">pulisher</span></p></body></html>"))
            self.label_addbook_price.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">price</span></p></body></html>"))
            self.btn_addbook_broswer.setText(_translate("MainWindow", "Broswer"))
            self.label_addbook_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600;\">add books</span></p></body></html>"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.add), _translate("MainWindow", "✏️ Add Book"))
            # users tab
            self.btn_user_search.setText(_translate("MainWindow", "🔎 Search"))
            self.label_user_phone.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Phone</span></p></body></html>"))
            self.label_user_name.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">name</span></p></body></html>"))
            self.label_user_delete.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Delete</span></p></body></html>"))
            self.label_user_lastname.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Last Name</span></p></body></html>"))
            self.label_user_username.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Username</span></p></body></html>"))
            self.label_user_update.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Update</span></p></body></html>"))
            self.label_user_address.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Address</span></p></body></html>"))
            self.label_user_isadmin.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Is Admin</span></p></body></html>"))     
            self.btn_user_show.setText(_translate("MainWindow", "✂️ filter"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.users), _translate("MainWindow", "🚻 Users"))
            # inventory tab
            self.label_inventory_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:13pt; font-weight:600;\">💜Online Book Store Info💜</span></p></body></html>"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.inventory), _translate("MainWindow", "📊 Inventory"))

        else:
            # info tab
            self.label_info_name.setText(_translate("MainWindow", "Name"))
            self.label_user_info_lastname.setText(_translate("MainWindow", "Last Name"))
            self.label_user_info_number.setText(_translate("MainWindow", "Phone Number"))
            self.label_user_info_address.setText(_translate("MainWindow", "Address"))
            # self.input_user_info_lastname.setText(_translate("MainWindow", "noroozi"))
            # self.input_user_info_name.setText(_translate("MainWindow", "mohamad"))
            # self.input_user_info_number.setText(_translate("MainWindow", "09126542563"))
            # self.input_user_info_address.setPlainText(_translate("MainWindow", "iran , tehran ,32"))
            self.label_user_info_username.setText(_translate("MainWindow", "Username"))
            # self.input_user_info_username.setText(_translate("MainWindow", "Norouzy"))
            self.label_user_info_password.setText(_translate("MainWindow", "Password"))
            # self.input_user_info_password.setText(_translate("MainWindow", "123456"))
            self.btn_logout.setText(_translate("MainWindow", "Log out"))
            self.label_login_username.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\"></span></p></body></html>"))
            self.btn_user_info_update.setText(_translate("MainWindow", "Update"))
            self.label_user_info_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Online Book Store Info</span></p></body></html>"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.info), _translate("MainWindow", "⚙️ info"))

        
        self.btn_logout.setText(_translate("MainWindow", "↩️ Log out"))
        self.label_login_username.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\"></span></p></body></html>"))
        self.label_login_username.setText("👤 "+str(self.username))

        # check boxes text fill
        for bx in range(0, len(self.bookCatBoxes)):
            objName = self.bookCatBoxes[bx].objectName()
            self.bookCatBoxes[bx].setText(_translate("MainWindow", objName))
            if self.is_admin:
                self.categoryBoxes[bx].setText(_translate("MainWindow", objName))