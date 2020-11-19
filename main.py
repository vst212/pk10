import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from mainwindow import Ui_wechatqrcode


if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    mainwindow=QMainWindow()
    ui=Ui_wechatqrcode()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())