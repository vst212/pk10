# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 Double Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from mainwindow import Ui_MainWindow


if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    mainwindow=QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())