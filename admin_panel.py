from turtle import title
from PyQt5 import QtCore, QtWidgets
from tables import db
from sqlalchemy import text
from PyQt5.QtGui import QPixmap
import shutil
import re


class Ui_MainWindow(object):

    def __init__(self):
        self.baseQuery = f"SELECT * FROM Book JOIN book_publisher ON book.id=book_publisher.book_id JOIN Publisher ON Publisher.id=publisher_id"
        self.filteredQuery = None 
        self.allBooks = list(db.engine.execute(text(self.baseQuery)))
        self.books = self.allBooks
        self.objects = None
        self.userObjects = []
        self.pictures = None
        self.buttons = None
        self.filterOptions = []
        self.categoryBoxes = []
    

    def fillBooks(self):
        
        self.buttons = []
        self.objects = []
        self.pictures = []

        for index, item in enumerate(self.books):
            self.objects.append(QtWidgets.QFrame(self.scrollAreaWidgetContents))
            self.objects[index].setMaximumSize(QtCore.QSize(485, 150))
            self.objects[index].setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.objects[index].setFrameShadow(QtWidgets.QFrame.Raised)
            self.objects[index].setObjectName("frame_list_" + str(index))
            self.gridLayoutWidget = QtWidgets.QWidget(self.objects[index])
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
            # buttons creation + callback function
            self.buttons.append(QtWidgets.QPushButton(self.gridLayoutWidget))
            self.buttons[index].setObjectName(str(item[0]))
            self.gridLayout_list_0.addWidget(self.buttons[index], 6, 0, 1, 1)
            self.buttons[index].clicked.connect(lambda ch, index=index: self.buyBook(self.buttons[index].objectName()))
            # pic
            self.gridLayout_5.addWidget(self.objects[index], index, 1, 1, 1)
            self.pictures.append(QtWidgets.QGraphicsView(self.scrollAreaWidgetContents))
            self.pictures[index].setMinimumSize(QtCore.QSize(220, 150))
            self.pictures[index].setMaximumSize(QtCore.QSize(220, 150))
            self.pictures[index].setObjectName("list_picture_" + str(index))        
            self.gridLayout_5.addWidget(self.pictures[index], index, 0, 1, 1)
            # giving values
            self.label_list_name_0.setText('book name: ' + item[1])
            self.label_list_quantity_0.setText('number in stock: ' + str(item[9]))
            self.label_list_author_0.setText('author: ' + item[2])
            self.label_list_price_0.setText('price: ' + str(item[4]))
            self.label_list_publisher_0.setText('publisher: ' + item[11])
            

    def removeBooks(self):
        for obj in self.objects:
            obj.deleteLater()

        for pic in self.pictures:
            pic.deleteLater()


    def buyBook(self, book_id):
        print(book_id)


    def search(self, input):
        if input:
            self.filteredQuery = self.baseQuery + f" WHERE Book.name LIKE '%{input}%' OR Book.author LIKE '%{input}%' OR Publisher.name LIKE '%{input}%'" 
            self.books = db.engine.execute(text(self.filteredQuery))
            self.removeBooks()
            
        else:
            self.filteredQuery = None
            self.books = self.allBooks


        self.filterOptions = []
        self.setupUi(MainWindow)

    
    def checkBoxFilter(self, filterObj):
        checkBoxes = [ 
            self.checkBox_list_mostExpensive,
            self.checkBox_list_leastExpensive,
            self.checkBox_list_mostPopular,
            self.checkBox_list_leastPopular,
            self.checkBox_list_newest,
            self.checkBox_list_oldest
        ]
        
        if filterObj.isChecked():
            self.filterOptions.append(filterObj.objectName())
        else:
            self.filterOptions.remove(filterObj.objectName())
        

        for index, checkbx in enumerate(checkBoxes):
            if checkbx.isChecked():           
                if index % 2 == 0:
                    checkBoxes[index + 1].setEnabled(False)
                else:
                    checkBoxes[index - 1].setEnabled(False)
            else:
                if index % 2 == 0:
                    checkBoxes[index + 1].setEnabled(True)
                else:
                    checkBoxes[index - 1].setEnabled(True) 
               

    def filter(self):

        if self.filterOptions:
            query = self.filteredQuery if self.filteredQuery else self.baseQuery
            query += ' ORDER BY'

            for filter in self.filterOptions:
                query = query + filter + ","

            if query[-1] == ',':
                query = query[:-1]

            print(query)  
            self.books = db.engine.execute(text(query))
            self.removeBooks()
            self.fillBooks() 
            self.retranslateUi(MainWindow)


    def addPublisher(self):
   
        inputDict = {
            'name': self.input_publisher_name.text(),
            'phone_number': self.input_publisher_number.text(),
            'website_url': self.input_publisher_web.text()
        }

        query = f"SELECT COUNT(*) from Publisher WHERE name='{inputDict['name']}'"
        result = db.engine.execute(text(query))
        publisher_exists = True if list(result)[0][0] == 1 else False

        if '' in inputDict.values():
            print('field/fields can not be empty!')

        elif publisher_exists:
            print('another publisher with this name found!')

        elif not inputDict['phone_number'].isdigit():
            print('wrong phone number!')

        else:  
            query = f"INSERT INTO Publisher(name, phone_number, website_url) VALUES('{inputDict['name']}', '{inputDict['phone_number']}', '{inputDict['website_url']}')"
            db.engine.execute(text(query))
            print('new publisher added!')



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
                print('another book with this name and publisher found!')
            
            elif not inputDict['price'].isdigit():
                print('wrong price input!!')

            elif not inputDict['quantity'].isdigit():
                print('wrong quantity input!!')

            else:      
                try:
                    url = inputDict['image_url'][::-1]
                    x = re.search('^gpj(.+?)/', url, re.IGNORECASE)
                    url = url[x.start() : x.end()][::-1]
                    shutil.copy(inputDict['image_url'], 'online-book-store\pictures')

                    query = f"INSERT INTO book(name, author, picture_url, price, description) VALUES('{inputDict['name']}', '{inputDict['author']}', 'pictures{url}', {inputDict['price']}, '{inputDict['description']}')"
                    db.engine.execute(text(query))
                    query = f"SELECT id FROM Book WHERE name='{inputDict['name']}' ORDER BY date_added DESC LIMIT 1"
                    insertedBook_id = list(db.engine.execute(text(query)))[0][0]
                    query = f"INSERT INTO book_publisher(book_id, publisher_id, quantity) VALUES({insertedBook_id}, {publisher_id}, {inputDict['quantity']})"
                    db.engine.execute(text(query))

                    for cat in self.categoryBoxes:
                        if cat.isChecked():
                            query = f"SELECT id FROM category WHERE name='{cat.objectName()}'"
                            category_id = list(db.engine.execute(text(query)))[0][0]
                            query = f"INSERT INTO book_category(book_id, category_id) VALUES({insertedBook_id}, {category_id})"
                            db.engine.execute(text(query))

                    
                    self.books = list(db.engine.execute(text(self.baseQuery)))
                    self.removeBooks()
                    self.fillBooks()
                    self.retranslateUi(MainWindow)

                except:
                    print('something where wrong while uploading photo!')

        else:
            print('field/fields can not be empty!')
        


    def getPicture(self):
        url, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Book Photo', '', '*.jpg')
        self.input_addbook_picture.setText(url)


    def fillUsers(self):

        query = "SELECT * FROM User JOIN Customer ON User.id=Customer.user_id"
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
            
            self.label_user_phone_0.setText(item[7])
            self.label_user_lastname_0.setText(item[6])
            self.label_user_name_0.setText(item[5])
            self.label_user_username_0.setText(item[1])
            self.label_user_address_0.setText(item[8])         
            deleteButtons[index].setText("Delete")
            
            if item[3] == 1:
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


    def removeUsers(self):
        for obj in self.userObjects:
            obj.deleteLater()

            
    def deleteUser(self, id):     

        queries = [
            f"DELETE FROM User WHERE id={id}",
            f"DELETE FROM Customer WHERE user_id={id}"
        ]

        for query in queries:
            db.engine.execute(text(query))

        self.removeUsers()
        self.fillUsers()


    def updateUser(self, action, id):

        is_admin = 1 if action == 'promote' else 0
        
        query = f"UPDATE User SET is_admin={is_admin} WHERE id={id}"
        db.engine.execute(text(query))

        self.removeUsers()
        self.fillUsers()

            
    def fillInventory(self):
        
        objects = []
        titles = [
            'Total Number Of Books ',
            'Number Of Sold Books ',
            'Total Books Price ',
            'Total Sold Books Price ',
            'Total Sold Books Price(last 7 days) ',
            'Total Sold Books Price(last 30 days) '
        ]
        queries = [
            "SELECT SUM(book_publisher.quantity) FROM Book JOIN book_publisher ON Book.id=book_publisher.book_id",
            "SELECT SUM(quantity) FROM book_order",
            "SELECT SUM(price) FROM Book",
            "SELECT SUM(Book.price) FROM Book JOIN book_order ON Book.id=book_order.book_id",
            "SELECT SUM(Book.price) FROM Book JOIN book_order ON Book.id=book_order.book_id WHERE book_order.date_added>=(SELECT DATETIME('now', '-7 day'))",
            "SELECT SUM(Book.price) FROM Book JOIN book_order ON Book.id=book_order.book_id WHERE book_order.date_added>=(SELECT DATETIME('now', '-30 day'))"
        ]

        for index in range(0, 6):

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
            self.label_inventory_0.setText(str(qResult))
   

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
        self.fillBooks()
    
        self.scrollArea_book_list.setWidget(self.scrollAreaWidgetContents)
        self.input_list_search = QtWidgets.QLineEdit(self.frame_list_main)
        self.input_list_search.setGeometry(QtCore.QRect(480, 20, 281, 24))
        self.input_list_search.setObjectName("input_list_search")
        self.btn_list_search = QtWidgets.QPushButton(self.frame_list_main)
        self.btn_list_search.setGeometry(QtCore.QRect(390, 20, 80, 24))
        self.btn_list_search.setObjectName("btn_list_search")
        # search button event listener
        self.btn_list_search.clicked.connect(lambda: self.search(self.input_list_search.text()))   
        # price filter
        self.checkBox_list_mostExpensive = QtWidgets.QCheckBox(self.frame_list_main)
        self.checkBox_list_mostExpensive.setGeometry(QtCore.QRect(10, 10, 100, 22))
        self.checkBox_list_mostExpensive.setObjectName(" Book.price DESC")
        self.checkBox_list_leastExpensive = QtWidgets.QCheckBox(self.frame_list_main)
        self.checkBox_list_leastExpensive.setGeometry(QtCore.QRect(10, 40, 100, 22))
        self.checkBox_list_leastExpensive.setObjectName(" Book.price")
        self.checkBox_list_mostExpensive.stateChanged.connect(lambda: self.checkBoxFilter(self.checkBox_list_mostExpensive))
        self.checkBox_list_leastExpensive.stateChanged.connect(lambda: self.checkBoxFilter(self.checkBox_list_leastExpensive))
        # popularity filter    
        self.checkBox_list_mostPopular = QtWidgets.QCheckBox(self.frame_list_main)
        self.checkBox_list_mostPopular.setGeometry(QtCore.QRect(120, 10, 83, 22))
        self.checkBox_list_mostPopular.setObjectName(" checkBox_list_mostPopular")
        self.checkBox_list_leastPopular = QtWidgets.QCheckBox(self.frame_list_main)
        self.checkBox_list_leastPopular.setGeometry(QtCore.QRect(120, 40, 83, 22))
        self.checkBox_list_leastPopular.setObjectName(" checkBox_list_leastPopular")
        self.checkBox_list_mostPopular.stateChanged.connect(lambda: self.checkBoxFilter(self.checkBox_list_mostPopular))
        self.checkBox_list_leastPopular.stateChanged.connect(lambda: self.checkBoxFilter(self.checkBox_list_leastPopular))
        # added date filter
        self.checkBox_list_newest = QtWidgets.QCheckBox(self.frame_list_main)
        self.checkBox_list_newest.setGeometry(QtCore.QRect(220, 10, 87, 22))
        self.checkBox_list_newest.setObjectName(" Book.date_added DESC")
        self.checkBox_list_oldest = QtWidgets.QCheckBox(self.frame_list_main)
        self.checkBox_list_oldest.setGeometry(QtCore.QRect(220, 40, 87, 22))
        self.checkBox_list_oldest.setObjectName(" Book.date_added")
        self.checkBox_list_newest.stateChanged.connect(lambda: self.checkBoxFilter(self.checkBox_list_newest))
        self.checkBox_list_oldest.stateChanged.connect(lambda: self.checkBoxFilter(self.checkBox_list_oldest))
             
        self.btn_list_show = QtWidgets.QPushButton(self.frame_list_main)
        self.btn_list_show.setGeometry(QtCore.QRect(100, 70, 80, 24))
        self.btn_list_show.setObjectName("btn_list_show")
        # filter button event listener
        self.btn_list_show.clicked.connect(lambda: self.filter())
      
        self.gridLayout_6.addWidget(self.frame_list_main, 0, 0, 1, 1)
        self.tabWidget.addTab(self.list, "")
        self.categoreis = QtWidgets.QWidget()
        self.categoreis.setObjectName("categoreis")
        self.scrollArea_category = QtWidgets.QScrollArea(self.categoreis)
        self.scrollArea_category.setGeometry(QtCore.QRect(10, 120, 411, 421))
        self.scrollArea_category.setWidgetResizable(True)
        self.scrollArea_category.setObjectName("scrollArea_category")
        self.scrollAreaWidgetContents_category = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_category.setGeometry(QtCore.QRect(0, 0, 409, 419))
        self.scrollAreaWidgetContents_category.setObjectName("scrollAreaWidgetContents_category")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_category)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_category_main = QtWidgets.QGridLayout()
        self.gridLayout_category_main.setObjectName("gridLayout_category_main")
        self.frame_category_0 = QtWidgets.QFrame(self.scrollAreaWidgetContents_category)
        self.frame_category_0.setMinimumSize(QtCore.QSize(0, 45))
        self.frame_category_0.setMaximumSize(QtCore.QSize(16777215, 45))
        self.frame_category_0.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_category_0.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_category_0.setObjectName("frame_category_0")
        self.label_category_0 = QtWidgets.QLabel(self.frame_category_0)
        self.label_category_0.setGeometry(QtCore.QRect(7, 9, 251, 31))
        self.label_category_0.setObjectName("label_category_0")
        self.btn_category_delete_0 = QtWidgets.QPushButton(self.frame_category_0)
        self.btn_category_delete_0.setGeometry(QtCore.QRect(270, 10, 80, 24))
        self.btn_category_delete_0.setObjectName("btn_category_delete_0")
        self.gridLayout_category_main.addWidget(self.frame_category_0, 0, 0, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_category_main, 0, 0, 1, 1)
        self.scrollArea_category.setWidget(self.scrollAreaWidgetContents_category)
        self.input_category_add = QtWidgets.QLineEdit(self.categoreis)
        self.input_category_add.setGeometry(QtCore.QRect(10, 70, 251, 24))
        self.input_category_add.setObjectName("input_category_add")
        self.btn_category_add = QtWidgets.QPushButton(self.categoreis)
        self.btn_category_add.setGeometry(QtCore.QRect(290, 70, 80, 24))
        self.btn_category_add.setObjectName("btn_category_add")
        self.label_category_error = QtWidgets.QLabel(self.categoreis)
        self.label_category_error.setGeometry(QtCore.QRect(510, 420, 271, 31))
        self.label_category_error.setObjectName("label_category_error")
        self.label_category_title = QtWidgets.QLabel(self.categoreis)
        self.label_category_title.setGeometry(QtCore.QRect(380, 10, 181, 41))
        self.label_category_title.setObjectName("label_category_title")
        self.tabWidget.addTab(self.categoreis, "")
        self.publisher = QtWidgets.QWidget()
        self.publisher.setObjectName("publisher")
        self.frame_publisher_add = QtWidgets.QFrame(self.publisher)
        self.frame_publisher_add.setGeometry(QtCore.QRect(510, 70, 351, 211))
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
        self.scrollArea_publisher_main = QtWidgets.QScrollArea(self.publisher)
        self.scrollArea_publisher_main.setGeometry(QtCore.QRect(10, 70, 411, 421))
        self.scrollArea_publisher_main.setWidgetResizable(True)
        self.scrollArea_publisher_main.setObjectName("scrollArea_publisher_main")
        self.scrollAreaWidgetContents_publisher = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_publisher.setGeometry(QtCore.QRect(0, 0, 409, 419))
        self.scrollAreaWidgetContents_publisher.setObjectName("scrollAreaWidgetContents_publisher")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_publisher)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.gridLayout_publisher_main = QtWidgets.QGridLayout()
        self.gridLayout_publisher_main.setObjectName("gridLayout_publisher_main")
        self.frame_publisher_0 = QtWidgets.QFrame(self.scrollAreaWidgetContents_publisher)
        self.frame_publisher_0.setMinimumSize(QtCore.QSize(0, 45))
        self.frame_publisher_0.setMaximumSize(QtCore.QSize(16777215, 45))
        self.frame_publisher_0.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_publisher_0.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_publisher_0.setObjectName("frame_publisher_0")
        self.label_publisher_name_0 = QtWidgets.QLabel(self.frame_publisher_0)
        self.label_publisher_name_0.setGeometry(QtCore.QRect(17, 9, 241, 31))
        self.label_publisher_name_0.setObjectName("label_publisher_name_0")
        self.btn_publisher_delete_0 = QtWidgets.QPushButton(self.frame_publisher_0)
        self.btn_publisher_delete_0.setGeometry(QtCore.QRect(270, 10, 80, 24))
        self.btn_publisher_delete_0.setObjectName("btn_publisher_delete_0")
        self.gridLayout_publisher_main.addWidget(self.frame_publisher_0, 0, 0, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_publisher_main, 0, 0, 1, 1)
        self.scrollArea_publisher_main.setWidget(self.scrollAreaWidgetContents_publisher)
        self.label_publisher_error = QtWidgets.QLabel(self.publisher)
        self.label_publisher_error.setGeometry(QtCore.QRect(580, 410, 271, 31))
        self.label_publisher_error.setObjectName("label_publisher_error")
        self.label_publisher_title = QtWidgets.QLabel(self.publisher)
        self.label_publisher_title.setGeometry(QtCore.QRect(340, 10, 181, 41))
        self.label_publisher_title.setObjectName("label_publisher_title")
        self.tabWidget.addTab(self.publisher, "")
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
        # publisher selection
        self.select_addbook_publisher = QtWidgets.QComboBox(self.add)
        self.select_addbook_publisher.setObjectName("select_addbook_publisher")
        # self.select_addbook_publisher.addItem("")
        result = list(db.engine.execute(text("SELECT name FROM Publisher")))
        publishers = [res[0] for res in result]

        
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
        # categores selection
        self.categoryBoxes = []
        x = 10
        catResult = list(db.engine.execute(text("SELECT name FROM category")))

        for index, cat in enumerate(catResult):

            self.categoryBoxes.append(QtWidgets.QCheckBox(self.scrollAreaWidgetContents_addbook_main))
            self.categoryBoxes[index].setObjectName(cat[0])

            if index % 2 == 0:
                x += 100
                y = 2
            else:
                y = 32
   
            self.categoryBoxes[index].setGeometry(QtCore.QRect(x, y, 83, 22))
  
        
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
        # addBook browse button event listener
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
        self.users = QtWidgets.QWidget()
        self.users.setObjectName("users")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.users)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.frame_user_main = QtWidgets.QFrame(self.users)
        self.frame_user_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_user_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_user_main.setObjectName("frame_user_main")
        self.input_user_search = QtWidgets.QLineEdit(self.frame_user_main)
        self.input_user_search.setGeometry(QtCore.QRect(480, 20, 281, 24))
        self.input_user_search.setObjectName("input_user_search")
        self.btn_user_search = QtWidgets.QPushButton(self.frame_user_main)
        self.btn_user_search.setGeometry(QtCore.QRect(770, 20, 80, 24))
        self.btn_user_search.setObjectName("btn_user_search")
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
        self.fillUsers()

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
        self.checkBox_user_mb = QtWidgets.QCheckBox(self.frame_user_main)
        self.checkBox_user_mb.setGeometry(QtCore.QRect(10, 10, 91, 22))
        self.checkBox_user_mb.setObjectName("checkBox_user_mb")
        self.checkBox_user_wb = QtWidgets.QCheckBox(self.frame_user_main)
        self.checkBox_user_wb.setGeometry(QtCore.QRect(10, 40, 91, 22))
        self.checkBox_user_wb.setObjectName("checkBox_user_wb")
        self.checkBox_user_admin = QtWidgets.QCheckBox(self.frame_user_main)
        self.checkBox_user_admin.setGeometry(QtCore.QRect(140, 10, 83, 22))
        self.checkBox_user_admin.setObjectName("checkBox_user_admin")
        self.checkBox_user_da = QtWidgets.QCheckBox(self.frame_user_main)
        self.checkBox_user_da.setGeometry(QtCore.QRect(140, 40, 91, 22))
        self.checkBox_user_da.setObjectName("checkBox_user_da")
        self.btn_user_show = QtWidgets.QPushButton(self.frame_user_main)
        self.btn_user_show.setGeometry(QtCore.QRect(260, 20, 80, 24))
        self.btn_user_show.setObjectName("btn_user_show")

        
        self.gridLayout_8.addWidget(self.frame_user_main, 0, 0, 1, 1)
        self.tabWidget.addTab(self.users, "")
        self.orders = QtWidgets.QWidget()
        self.orders.setObjectName("orders")
        self.tableWidget_order = QtWidgets.QTableWidget(self.orders)
        self.tableWidget_order.setGeometry(QtCore.QRect(34, 50, 811, 481))
        self.tableWidget_order.setObjectName("tableWidget_order")
        self.tableWidget_order.setColumnCount(8)
        self.tableWidget_order.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_order.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_order.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_order.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_order.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_order.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_order.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_order.setItem(0, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_order.setItem(0, 7, item)
        self.label_order_title = QtWidgets.QLabel(self.orders)
        self.label_order_title.setGeometry(QtCore.QRect(320, 9, 181, 41))
        self.label_order_title.setObjectName("label_order_title")
        self.tabWidget.addTab(self.orders, "")
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
        self.btn_logout = QtWidgets.QPushButton(self.centralwidget)
        self.btn_logout.setGeometry(QtCore.QRect(800, 10, 80, 24))
        self.btn_logout.setObjectName("btn_logout")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
       
        for btn in self.buttons:
            btn.setText(_translate("MainWindow", "Buy"))
            
        self.btn_list_search.setText(_translate("MainWindow", "Search"))
        self.checkBox_list_mostExpensive.setText(_translate("MainWindow", "Most Expensive"))
        self.checkBox_list_leastExpensive.setText(_translate("MainWindow", "Least Expensive"))
        self.checkBox_list_mostPopular.setText(_translate("MainWindow", "Most Popular"))
        self.checkBox_list_leastPopular.setText(_translate("MainWindow", "Least Popular"))
        self.checkBox_list_newest.setText(_translate("MainWindow", "Newest"))
        self.checkBox_list_oldest.setText(_translate("MainWindow", "Oldest"))
        self.btn_list_show.setText(_translate("MainWindow", "filter"))
          
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.list), _translate("MainWindow", "Book List"))
        self.label_category_0.setText(_translate("MainWindow", "action"))
        self.btn_category_delete_0.setText(_translate("MainWindow", "Delete"))
        self.btn_category_add.setText(_translate("MainWindow", "Add"))
        self.label_category_error.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Error</p></body></html>"))
        self.label_category_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Publishers</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.categoreis), _translate("MainWindow", "Categorys"))
        self.label_publisher_name.setText(_translate("MainWindow", "Name"))
        self.label_publisher_number.setText(_translate("MainWindow", "Phone Number"))
        self.label_publisher_web.setText(_translate("MainWindow", "Web site"))
        self.btn_publisher_add.setText(_translate("MainWindow", "Add"))
        self.label_publisher_name_0.setText(_translate("MainWindow", "tolo"))
        self.btn_publisher_delete_0.setText(_translate("MainWindow", "Delete"))
        self.label_publisher_error.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Error</p></body></html>"))
        self.label_publisher_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Publishers</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.publisher), _translate("MainWindow", "Publisher"))
        self.label_addbook_error.setText(_translate("MainWindow", "error"))
        self.label_addbook_name.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">name</span></p></body></html>"))
        self.label_addbook_picture.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Picture</span></p></body></html>"))
        self.label_addbook_author.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">author</span></p></body></html>"))
        # self.label_addbook_category.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">category</span></p></body></html>"))
        self.label_addbook_description.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">description</span></p><p align=\"center\"><br/></p></body></html>"))
        # self.select_addbook_publisher.setItemText(0, _translate("MainWindow", "select"))
        
        # addbook categories checkboxes
        for bx in self.categoryBoxes:
            bx.setText(_translate("MainWindow", bx.objectName()))

        self.label_addbook_quantity.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">quantity</span></p></body></html>"))
        self.btn_addbook_submit.setText(_translate("MainWindow", "Submit"))
        self.label_addbook_publisher.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">pulisher</span></p></body></html>"))
        self.label_addbook_price.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">price</span></p></body></html>"))
        self.btn_addbook_broswer.setText(_translate("MainWindow", "Broswer"))
        self.label_addbook_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600;\">add books</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.add), _translate("MainWindow", "Add Book"))
        self.btn_user_search.setText(_translate("MainWindow", "Search"))
      
        self.label_user_phone.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Phone</span></p></body></html>"))
        self.label_user_name.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">name</span></p></body></html>"))
        self.label_user_delete.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Delete</span></p></body></html>"))
        self.label_user_lastname.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Last Name</span></p></body></html>"))
        self.label_user_username.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Username</span></p></body></html>"))
        self.label_user_update.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Update</span></p></body></html>"))
        self.label_user_address.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Address</span></p></body></html>"))
        self.label_user_isadmin.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Is Admin</span></p></body></html>"))
        self.checkBox_user_mb.setText(_translate("MainWindow", "Most Buyer"))
        self.checkBox_user_wb.setText(_translate("MainWindow", "Weak Buyer"))
        self.checkBox_user_admin.setText(_translate("MainWindow", "admin"))
        self.checkBox_user_da.setText(_translate("MainWindow", "Date Added"))
        self.btn_user_show.setText(_translate("MainWindow", "Show"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.users), _translate("MainWindow", "Users"))
        item = self.tableWidget_order.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget_order.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.tableWidget_order.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Book"))
        item = self.tableWidget_order.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "User"))
        item = self.tableWidget_order.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Publisher"))
        item = self.tableWidget_order.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Date added"))
        item = self.tableWidget_order.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Quantity"))
        item = self.tableWidget_order.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Price"))
        item = self.tableWidget_order.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Total Price"))
        __sortingEnabled = self.tableWidget_order.isSortingEnabled()
        self.tableWidget_order.setSortingEnabled(False)
        item = self.tableWidget_order.item(0, 0)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget_order.item(0, 1)
        item.setText(_translate("MainWindow", "Harry"))
        item = self.tableWidget_order.item(0, 2)
        item.setText(_translate("MainWindow", "Nrouzy"))
        item = self.tableWidget_order.item(0, 3)
        item.setText(_translate("MainWindow", "tolo"))
        item = self.tableWidget_order.item(0, 4)
        item.setText(_translate("MainWindow", "12/03/9"))
        item = self.tableWidget_order.item(0, 5)
        item.setText(_translate("MainWindow", "2"))
        item = self.tableWidget_order.item(0, 6)
        item.setText(_translate("MainWindow", "1200"))
        item = self.tableWidget_order.item(0, 7)
        item.setText(_translate("MainWindow", "2400"))
        self.tableWidget_order.setSortingEnabled(__sortingEnabled)
        self.label_order_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">All Orders</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.orders), _translate("MainWindow", "Orders"))
       
        self.label_inventory_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Online Book Store Info</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.inventory), _translate("MainWindow", "Inventory"))
        self.btn_logout.setText(_translate("MainWindow", "Log out"))
        self.label_login_username.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Norouzy</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())