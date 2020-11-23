import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from mainwindow import Ui_wechatqrcode


# if __name__=="__main__":
import sys

from umeng import Ui_umeng

app=QApplication(sys.argv)
mainwindow=QMainWindow()
# ui=Ui_wechatqrcode()
# ui.setupUi(mainwindow)
# mainwindow.show()
ui=Ui_umeng()
ui.setupUi(mainwindow)
mainwindow.show()
sys.exit(app.exec_())