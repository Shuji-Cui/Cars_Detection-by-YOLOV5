
from PyQt5.QtWidgets import *
import sys
import demo2



app = QApplication(sys.argv)
mainWindow = QMainWindow()
ui = demo2.Ui_MainWindow()
mainWindow = ui.setupUi(mainWindow)
mainWindow.show()
app.exit(app.exec_())


