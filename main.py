

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
import sys

from fuck import Ui_MainWindow

class Closewindow(QMainWindow):
    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     '退出',
                                     "退出程序吗？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


app=QApplication(sys.argv)
mainwindow=Closewindow()
ui=Ui_MainWindow()
ui.setupUi(mainwindow)
mainwindow.show()
sys.exit(app.exec_())