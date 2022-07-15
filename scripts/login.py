from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from scripts.tables import db
from sqlalchemy import text

dir = "./"

class Ui_LoginWindow(object):
    # main functions

    def loginHandle(self,MainWindow):

        username = self.login_username.text()
        password = self.login_password.text()

        if username and password:
            query = f"SELECT EXISTS(SELECT * FROM User WHERE username='{username}' and password='{password}')"     
            result = db.engine.execute(text(query))
            authenticated = True if list(result)[0][0] == 1 else False
            
            if authenticated :
                query = f"SELECT id FROM User WHERE username='{username}'"
                user_id = list(db.engine.execute(text(query)))[0][0]

                query = f"SELECT is_admin FROM User WHERE username='{username}'"
                is_admin = True if list(db.engine.execute(text(query)))[0][0] == 1 else False
                
                # calling user panel
                from scripts.panel import Ui_MainWindow
                ui = Ui_MainWindow(user_id, is_admin, username ,MainWindow)
                ui.setupUi(MainWindow)
            else:
                self.createMsgBox("warning", "login failure", "incorrect username or password")     
        

    def signUpHandle(self,MainWindow):  

        valuesDict = {
            'first_name': self.last_name.text(),
            'last_name': self.first_name.text(),
            'username': self.username_sign.text(),
            'password': self.password_sign.text(),
            'phone_number': self.phoneNumber_sign.text(),
            'address': self.address_sign.toPlainText()
        }

        query = f"SELECT EXISTS(SELECT * FROM User WHERE username='{valuesDict['username']}')"
        result = db.engine.execute(text(query))
        user_exists = True if list(result)[0][0] == 1 else False

        if '' in valuesDict.values():
            self.createMsgBox("warning", "signup failure", "input field/fields can not be empty!")

        elif user_exists:
            self.createMsgBox("warning", "signup failure", "another user with this username exists!")

        elif len(valuesDict['password']) < 5:
            self.createMsgBox("warning", "signup failure", "entered password is too weak!")

        elif not valuesDict['phone_number'].isdigit():
            self.createMsgBox("warning", "signup failure", "please enter a valid phone number!")

        else:  
            query =  "INSERT INTO User(username, password, is_admin)"\
                    +f"\n      VALUES('{valuesDict['username']}', '{valuesDict['password']}', FALSE)"
            db.engine.execute(text(query))

            query = f"SELECT id FROM User WHERE username='{valuesDict['username']}'"
            result = db.engine.execute(text(query))
            user_id = list(result)[0][0]

            query = "INSERT INTO Customer(first_name, last_name, user_id, phone_number, address)"\
                    +f"\n   VALUES('{valuesDict['first_name']}', '{valuesDict['last_name']}', {user_id},"\
                    +f"\n  '{valuesDict['phone_number']}', '{valuesDict['address']}')"
            db.engine.execute(text(query))

            self.createMsgBox("information", "sign up success", "new user created!")

            # calling user panel
            from scripts.panel import Ui_MainWindow
            ui = Ui_MainWindow(user_id, False, valuesDict['username'], MainWindow)
            ui.setupUi(MainWindow)
            ui = Ui_MainWindow(valuesDict['username'],valuesDict['password'],MainWindow)
            ui.setupUi(MainWindow)


    def createMsgBox(self,type,  title, text):
        msg = QMessageBox()
        if type == 'warning':
            msg.setIcon(QMessageBox.Warning)
        else:
            msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    # ui functions
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(340, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.login = QtWidgets.QWidget()
        self.login.setObjectName("login")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.login)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.formWidget = QtWidgets.QWidget(self.login)
        self.formWidget.setObjectName("formWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.formWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.formWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.login_username = QtWidgets.QLineEdit(self.formWidget)
        self.login_username.setPlaceholderText("")
        self.login_username.setObjectName("login_username")
        self.gridLayout.addWidget(self.login_username, 1, 1, 1, 1, QtCore.Qt.AlignVCenter)
        self.graphicsView = QtWidgets.QGraphicsView(self.formWidget)
        self.graphicsView.setStyleSheet("color: rgb(80, 255, 121);")
        self.graphicsView.setStyleSheet("#graphicsView { background-image: url("+dir+"/img/login.png);background-repeat: no-repeat;background-attachment: fixed;background-position: center;border:0px;}")
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 1, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label = QtWidgets.QLabel(self.formWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.login_password = QtWidgets.QLineEdit(self.formWidget)
        self.login_password.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.login_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_password.setObjectName("login_password")
        self.gridLayout.addWidget(self.login_password, 2, 1, 1, 1, QtCore.Qt.AlignVCenter)
        self.login_btn = QtWidgets.QPushButton(self.formWidget)
        self.login_btn.setObjectName("login_btn")
        self.gridLayout.addWidget(self.login_btn, 3, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.formWidget)
        self.tabWidget.addTab(self.login, "")
        self.signup = QtWidgets.QWidget()
        self.signup.setObjectName("signup")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.signup)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formWidget_2 = QtWidgets.QWidget(self.signup)
        self.formWidget_2.setObjectName("formWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.formWidget_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.formWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 5, 0, 1, 1)
        self.phoneNumber_sign = QtWidgets.QLineEdit(self.formWidget_2)
        self.phoneNumber_sign.setObjectName("phoneNumber_sign")
        self.gridLayout_2.addWidget(self.phoneNumber_sign, 5, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.formWidget_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 6, 0, 1, 1)
        self.address_sign = QtWidgets.QPlainTextEdit(self.formWidget_2)
        self.address_sign.setObjectName("address_sign")
        self.gridLayout_2.addWidget(self.address_sign, 6, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.formWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.password_sign = QtWidgets.QLineEdit(self.formWidget_2)
        self.password_sign.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_sign.setObjectName("password_sign")
        self.gridLayout_2.addWidget(self.password_sign, 4, 1, 1, 1)
        self.signin_btn = QtWidgets.QPushButton(self.formWidget_2)
        self.signin_btn.setObjectName("signin_btn")
        self.gridLayout_2.addWidget(self.signin_btn, 7, 1, 1, 1)
        self.username_sign = QtWidgets.QLineEdit(self.formWidget_2)
        self.username_sign.setObjectName("username_sign")
        self.gridLayout_2.addWidget(self.username_sign, 3, 1, 1, 1)
        self.first_name = QtWidgets.QLineEdit(self.formWidget_2)
        self.first_name.setObjectName("first_name")
        self.gridLayout_2.addWidget(self.first_name, 2, 1, 1, 1)
        self.last_name = QtWidgets.QLineEdit(self.formWidget_2)
        self.last_name.setObjectName("last_name")
        self.gridLayout_2.addWidget(self.last_name, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.formWidget_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 4, 0, 1, 1)
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.formWidget_2)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_2.setStyleSheet("#graphicsView_2 { background-image: url("+dir+"/img/signup.png);background-repeat: no-repeat;background-attachment: fixed;background-position: center;border:0px;}")
        self.gridLayout_2.addWidget(self.graphicsView_2, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_7 = QtWidgets.QLabel(self.formWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.formWidget_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 2, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.formWidget_2)
        self.tabWidget.addTab(self.signup, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # ----------------------- connectors start-------------------------
        self.login_btn.clicked.connect(lambda:self.loginHandle(MainWindow))
        self.signin_btn.clicked.connect(lambda:self.signUpHandle(MainWindow))
        # ----------------------- connectors ending-------------------------

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.login_btn.clicked.connect(MainWindow.update)
        self.signin_btn.clicked.connect(MainWindow.update)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "💙 Online Book Store 💙"))
        self.label_2.setText(_translate("MainWindow", "🔑 Password"))
        self.label.setText(_translate("MainWindow", "👮‍ Username"))
        self.login_btn.setText(_translate("MainWindow", "👉 Login 👈"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.login), _translate("MainWindow", "🟢 Login"))
        self.label_5.setText(_translate("MainWindow", "Phone Number"))
        self.label_6.setText(_translate("MainWindow", "Address"))
        self.label_3.setText(_translate("MainWindow", "Username"))
        self.signin_btn.setText(_translate("MainWindow", "👉 Sign Up 👈"))
        self.label_4.setText(_translate("MainWindow", "Password"))
        self.label_7.setText(_translate("MainWindow", "Name"))
        self.label_8.setText(_translate("MainWindow", "Last Name"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.signup), _translate("MainWindow", "🔵 Sign Up"))
