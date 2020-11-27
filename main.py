
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox

from mainwindow import Ui_wechatqrcode


# if __name__=="__main__":
import sys

from proxy import closeproxy
from umeng import Ui_umeng

class Closewindow(QMainWindow):
    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     '退出',
                                     "退出程序吗？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            closeproxy()
        else:
            event.ignore()


app=QApplication(sys.argv)
mainwindow=Closewindow()
# ui=Ui_wechatqrcode()
# ui.setupUi(mainwindow)
# mainwindow.show()
ui=Ui_umeng()
ui.setupUi(mainwindow)
mainwindow.show()
sys.exit(app.exec_())