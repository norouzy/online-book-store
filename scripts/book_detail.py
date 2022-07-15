from PyQt5 import QtCore, QtGui, QtWidgets
from scripts.tables import db
from sqlalchemy import text


class Ui_BookDetailWindow(object):

    def __init__(self, id):
        
        self.book_id = id
        self.baseQuery = "SELECT Book.picture_url, Book.name, Book.author, Book.description, book_publisher.quantity,"\
                        +"\n    Publisher.name, Book.date_added, Book.price "\
                        +"\n    FROM book_publisher"\
                        +"\n    JOIN Book ON book_publisher.book_id=Book.id"\
                        +"\n    JOIN Publisher ON Publisher.id=book_publisher.publisher_id"\
                        +"\n    LEFT JOIN book_order ON book_order.book_id=book.id and book_order.publisher_id=Publisher.id"\
                        +"\n    GROUP BY Book.id, Publisher.id"\
                        +f"\n    HAVING Book.id={self.book_id}"


        self.categoryQuery = "SELECT Category.name FROM Category JOIN book_category ON Category.id=book_category.category_id"+\
                            f"\n    WHERE book_category.book_id={self.book_id}"

        self.bookData = list(db.engine.execute(text(self.baseQuery)))
        self.bookData = self.bookData[0]

    def fillItems(self):

        categories = []
        bookData = self.bookData
        try:
            catNames = list(db.engine.execute(text(self.categoryQuery)))[0]
            categories = [cat for cat in catNames]
        except:
            categories = "No Category"
        
        self.book_nam_detail_label.setText(bookData[1])
        self.author_book_detail_label.setText(bookData[2])
        self.description_book_detail_label.setText(bookData[3])
        self.quantity_book_detail_label.setText(str(bookData[4]))
        self.publisher_book_detail_label.setText(bookData[5])
        self.date_book_detail_label.setText(bookData[6])
        self.price_book_detail_label.setText(str(bookData[7]))
        self.category_book_detail_label.setText(str(categories))

    def close_window(self,BookDetailWindow):
        BookDetailWindow.deleteLater()
    

    def setupUi(self, BookDetailWindow):
        BookDetailWindow.setObjectName("BookDetailWindow")
        BookDetailWindow.resize(327, 674)
        self.centralwidget = QtWidgets.QWidget(BookDetailWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_fram = QtWidgets.QFrame(self.centralwidget)
        self.main_fram.setGeometry(QtCore.QRect(20, 20, 301, 611))
        self.main_fram.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_fram.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_fram.setObjectName("main_fram")
        self.detail_book_image = QtWidgets.QGraphicsView(self.main_fram)
        self.detail_book_image.setStyleSheet("#detail_book_image { background-image: url(pictures/"+ self.bookData[0] +");background-repeat: no-repeat;background-attachment: fixed;background-position: center;border:0px;}")
        self.detail_book_image.setGeometry(QtCore.QRect(10, 10, 261, 191))
        self.detail_book_image.setObjectName("detail_book_image")
        self.scrollArea = QtWidgets.QScrollArea(self.main_fram)
        self.scrollArea.setGeometry(QtCore.QRect(9, 209, 281, 351))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollView_book_detail = QtWidgets.QWidget()
        self.scrollView_book_detail.setGeometry(QtCore.QRect(0, -208, 265, 557))
        self.scrollView_book_detail.setObjectName("scrollView_book_detail")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollView_book_detail)
        self.gridLayout.setObjectName("gridLayout")
        self.quantity_book_detail = QtWidgets.QFrame(self.scrollView_book_detail)
        self.quantity_book_detail.setMinimumSize(QtCore.QSize(0, 50))
        self.quantity_book_detail.setMaximumSize(QtCore.QSize(16777215, 70))
        self.quantity_book_detail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.quantity_book_detail.setFrameShadow(QtWidgets.QFrame.Raised)
        self.quantity_book_detail.setObjectName("quantity_book_detail")
        self.quantity_book_detail_title_label = QtWidgets.QLabel(self.quantity_book_detail)
        self.quantity_book_detail_title_label.setGeometry(QtCore.QRect(10, 19, 58, 16))
        self.quantity_book_detail_title_label.setObjectName("quantity_book_detail_title_label")
        self.quantity_book_detail_label = QtWidgets.QLabel(self.quantity_book_detail)
        self.quantity_book_detail_label.setGeometry(QtCore.QRect(87, 19, 151, 20))
        self.quantity_book_detail_label.setObjectName("quantity_book_detail_label")
        self.gridLayout.addWidget(self.quantity_book_detail, 3, 0, 1, 1)
        self.description__book_detail = QtWidgets.QFrame(self.scrollView_book_detail)
        self.description__book_detail.setMinimumSize(QtCore.QSize(0, 100))
        self.description__book_detail.setMaximumSize(QtCore.QSize(16777215, 70))
        self.description__book_detail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.description__book_detail.setFrameShadow(QtWidgets.QFrame.Raised)
        self.description__book_detail.setObjectName("description__book_detail")
        self.description_book_detail_label = QtWidgets.QLabel(self.description__book_detail)
        self.description_book_detail_label.setGeometry(QtCore.QRect(10, 10, 241, 71))
        self.description_book_detail_label.setObjectName("description_book_detail_label")
        self.gridLayout.addWidget(self.description__book_detail, 2, 0, 1, 1)
        self.book_name_detail = QtWidgets.QFrame(self.scrollView_book_detail)
        self.book_name_detail.setMinimumSize(QtCore.QSize(0, 55))
        self.book_name_detail.setMaximumSize(QtCore.QSize(16777215, 70))
        self.book_name_detail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.book_name_detail.setFrameShadow(QtWidgets.QFrame.Raised)
        self.book_name_detail.setObjectName("book_name_detail")
        self.book_nam_detail_label = QtWidgets.QLabel(self.book_name_detail)
        self.book_nam_detail_label.setGeometry(QtCore.QRect(10, 13, 231, 31))
        self.book_nam_detail_label.setObjectName("book_nam_detail_label")
        self.gridLayout.addWidget(self.book_name_detail, 0, 0, 1, 1)
        self.price_book_detail = QtWidgets.QFrame(self.scrollView_book_detail)
        self.price_book_detail.setMinimumSize(QtCore.QSize(0, 50))
        self.price_book_detail.setMaximumSize(QtCore.QSize(16777215, 70))
        self.price_book_detail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.price_book_detail.setFrameShadow(QtWidgets.QFrame.Raised)
        self.price_book_detail.setObjectName("price_book_detail")
        self.price_book_detail_title_label = QtWidgets.QLabel(self.price_book_detail)
        self.price_book_detail_title_label.setGeometry(QtCore.QRect(10, 20, 51, 16))
        self.price_book_detail_title_label.setObjectName("price_book_detail_title_label")
        self.price_book_detail_label = QtWidgets.QLabel(self.price_book_detail)
        self.price_book_detail_label.setGeometry(QtCore.QRect(60, 20, 171, 20))
        self.price_book_detail_label.setObjectName("price_book_detail_label")
        self.gridLayout.addWidget(self.price_book_detail, 7, 0, 1, 1)
        self.date_book_detail = QtWidgets.QFrame(self.scrollView_book_detail)
        self.date_book_detail.setMinimumSize(QtCore.QSize(0, 50))
        self.date_book_detail.setMaximumSize(QtCore.QSize(16777215, 70))
        self.date_book_detail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.date_book_detail.setFrameShadow(QtWidgets.QFrame.Raised)
        self.date_book_detail.setObjectName("date_book_detail")
        self.date_book_detail_title_label = QtWidgets.QLabel(self.date_book_detail)
        self.date_book_detail_title_label.setGeometry(QtCore.QRect(10, 17, 81, 16))
        self.date_book_detail_title_label.setObjectName("date_book_detail_title_label")
        self.date_book_detail_label = QtWidgets.QLabel(self.date_book_detail)
        self.date_book_detail_label.setGeometry(QtCore.QRect(90, 15, 151, 20))
        self.date_book_detail_label.setObjectName("date_book_detail_label")
        self.gridLayout.addWidget(self.date_book_detail, 5, 0, 1, 1)
        self.author_book_detail = QtWidgets.QFrame(self.scrollView_book_detail)
        self.author_book_detail.setMinimumSize(QtCore.QSize(0, 55))
        self.author_book_detail.setMaximumSize(QtCore.QSize(16777215, 70))
        self.author_book_detail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.author_book_detail.setFrameShadow(QtWidgets.QFrame.Raised)
        self.author_book_detail.setObjectName("author_book_detail")
        self.author_book_detail_label = QtWidgets.QLabel(self.author_book_detail)
        self.author_book_detail_label.setGeometry(QtCore.QRect(50, 13, 191, 31))
        self.author_book_detail_label.setObjectName("author_book_detail_label")
        self.author_book_detail_title_label = QtWidgets.QLabel(self.author_book_detail)
        self.author_book_detail_title_label.setGeometry(QtCore.QRect(20, 21, 21, 16))
        self.author_book_detail_title_label.setObjectName("author_book_detail_title_label")
        self.gridLayout.addWidget(self.author_book_detail, 1, 0, 1, 1)
        self.publisher_book_detail = QtWidgets.QFrame(self.scrollView_book_detail)
        self.publisher_book_detail.setMinimumSize(QtCore.QSize(0, 50))
        self.publisher_book_detail.setMaximumSize(QtCore.QSize(16777215, 70))
        self.publisher_book_detail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.publisher_book_detail.setFrameShadow(QtWidgets.QFrame.Raised)
        self.publisher_book_detail.setObjectName("publisher_book_detail")
        self.publisher_book_detail_title_label = QtWidgets.QLabel(self.publisher_book_detail)
        self.publisher_book_detail_title_label.setGeometry(QtCore.QRect(10, 16, 61, 16))
        self.publisher_book_detail_title_label.setObjectName("publisher_book_detail_title_label")
        self.publisher_book_detail_label = QtWidgets.QLabel(self.publisher_book_detail)
        self.publisher_book_detail_label.setGeometry(QtCore.QRect(90, 16, 161, 20))
        self.publisher_book_detail_label.setObjectName("publisher_book_detail_label")
        self.gridLayout.addWidget(self.publisher_book_detail, 4, 0, 1, 1)
        self.category_book_detail = QtWidgets.QFrame(self.scrollView_book_detail)
        self.category_book_detail.setMinimumSize(QtCore.QSize(0, 87))
        self.category_book_detail.setMaximumSize(QtCore.QSize(16777215, 70))
        self.category_book_detail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.category_book_detail.setFrameShadow(QtWidgets.QFrame.Raised)
        self.category_book_detail.setObjectName("category_book_detail")
        self.category_book_detail_title_label = QtWidgets.QLabel(self.category_book_detail)
        self.category_book_detail_title_label.setGeometry(QtCore.QRect(10, 10, 58, 16))
        self.category_book_detail_title_label.setMinimumSize(QtCore.QSize(0, 0))
        self.category_book_detail_title_label.setObjectName("category_book_detail_title_label")
        self.category_book_detail_label = QtWidgets.QLabel(self.category_book_detail)
        self.category_book_detail_label.setGeometry(QtCore.QRect(80, 9, 161, 71))
        self.category_book_detail_label.setObjectName("category_book_detail_label")
        self.gridLayout.addWidget(self.category_book_detail, 6, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollView_book_detail)
        self.close_btn = QtWidgets.QPushButton(self.main_fram)
        self.close_btn.setGeometry(QtCore.QRect(100, 570, 80, 24))
        self.close_btn.clicked.connect(lambda: self.close_window(BookDetailWindow))
        self.close_btn.setObjectName("close_btn")
        BookDetailWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BookDetailWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 327, 21))
        self.menubar.setObjectName("menubar")
        BookDetailWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BookDetailWindow)
        self.statusbar.setObjectName("statusbar")
        BookDetailWindow.setStatusBar(self.statusbar)

        # call fill items function
        self.fillItems()

        self.retranslateUi(BookDetailWindow)
        QtCore.QMetaObject.connectSlotsByName(BookDetailWindow)

    def retranslateUi(self, BookDetailWindow):
        _translate = QtCore.QCoreApplication.translate
        BookDetailWindow.setWindowTitle(_translate("BookDetailWindow", "BookDetailWindow"))
        self.quantity_book_detail_title_label.setText(_translate("BookDetailWindow", "quantity :"))
        # self.quantity_book_detail_label.setText(_translate("BookDetailWindow", "12"))
        # self.description_book_detail_label.setText(_translate("BookDetailWindow", "here write our description<br>and with <br>get next line"))
        # self.book_nam_detail_label.setText(_translate("BookDetailWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Harray pater</span></p></body></html>"))
        self.price_book_detail_title_label.setText(_translate("BookDetailWindow", "price :"))
        # self.price_book_detail_label.setText(_translate("BookDetailWindow", "130000"))
        self.date_book_detail_title_label.setText(_translate("BookDetailWindow", "Time added :"))
        # self.date_book_detail_label.setText(_translate("BookDetailWindow", "1378/08/9"))
        # self.author_book_detail_label.setText(_translate("BookDetailWindow", "wison miler"))
        self.author_book_detail_title_label.setText(_translate("BookDetailWindow", "by : "))
        self.publisher_book_detail_title_label.setText(_translate("BookDetailWindow", "publisher:"))
        # self.publisher_book_detail_label.setText(_translate("BookDetailWindow", "tolo"))
        self.category_book_detail_title_label.setText(_translate("BookDetailWindow", "category :"))
        # self.category_book_detail_label.setText(_translate("BookDetailWindow", "action ,comedy"))
        self.close_btn.setText(_translate("BookDetailWindow", "close"))