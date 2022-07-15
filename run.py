from scripts.login import Ui_LoginWindow 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('./img/icon.png'))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())