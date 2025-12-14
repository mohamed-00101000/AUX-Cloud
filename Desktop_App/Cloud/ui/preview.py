from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QStyleFactory
from PyQt5.QtWidgets import QListView



app = QtWidgets.QApplication(sys.argv)
app.setStyle(QStyleFactory.create("Fusion"))


base_font = app.font()
base_font.setPointSize(base_font.pointSize() + 1)
app.setFont(base_font)


w = uic.loadUi("front.ui")

title = w.findChild(QtWidgets.QLabel, "titleLabel")

if title:
    glow = QGraphicsDropShadowEffect()
    glow.setBlurRadius(18)              # glow strength
    glow.setOffset(0, 0)                # centered glow
    glow.setColor(QtGui.QColor(190, 30, 45))  # ASURT red

    title.setGraphicsEffect(glow)
    title.setStyleSheet("color: #d6d6d6;")



w.show()
sys.exit(app.exec_())
