from PyQt5 import QtWidgets

from ui.ui_action import Ui

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui()

    ui.setupUi(MainWindow)
    ui.init_ui()

    MainWindow.show()
    sys.exit(app.exec_())
