from PyQt5 import QtWidgets, uic
import sys

app = QtWidgets.QApplication(sys.argv)
w = uic.loadUi("front.ui")
w.show()
sys.exit(app.exec_())
