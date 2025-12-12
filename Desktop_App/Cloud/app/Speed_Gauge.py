from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class CarGaugeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(300, 300)
        self.max_speed = 100
        self.value = 0

    # -----------------------------------------------------------
    # Set new value safely
    # -----------------------------------------------------------
    def setValue(self, value):
        try:
            self.value = max(0, min(self.max_speed, float(value)))
        except:
            self.value = 0
        self.update()

    # -----------------------------------------------------------
    # Draw gauge
    # -----------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        center = rect.center()

        # -------------------------------
        # Draw outer black circle
        # -------------------------------
        painter.setBrush(Qt.black)
        painter.setPen(Qt.black)
        painter.drawEllipse(rect.adjusted(20, 20, -20, -20))

        # -------------------------------
        # Inner white circle
        # -------------------------------
        painter.setBrush(Qt.white)
        painter.drawEllipse(rect.adjusted(30, 30, -30, -30))

        # -------------------------------
        # Draw needle
        # -------------------------------
        painter.save()
        painter.translate(center)

        angle = (self.value / self.max_speed) * 270 - 135
        painter.rotate(angle)

        needle = QtGui.QPolygon([
            QtCore.QPoint(0, -rect.height() // 3),
            QtCore.QPoint(-6, 0),
            QtCore.QPoint(6, 0)
        ])

        painter.setBrush(Qt.red)
        painter.setPen(Qt.red)
        painter.drawPolygon(needle)

        painter.restore()

        # -------------------------------
        # Draw speed labels
        # -------------------------------
        painter.setPen(Qt.black)
        font = QtGui.QFont("Arial", 11, QtGui.QFont.Bold)
        painter.setFont(font)

        label_values = range(0, self.max_speed + 1, 10)

        for i, label in enumerate(label_values):
            label_angle = -135 + (i * 270 / (len(label_values) - 1))

            painter.save()
            painter.translate(center)
            painter.rotate(label_angle)
            painter.translate(0, -rect.height() // 2 + 35)
            painter.drawText(-10, 0, 25, 20, Qt.AlignCenter, str(label))
            painter.restore()

        # -------------------------------
        # Draw current speed text
        # -------------------------------
        painter.setPen(Qt.black)
        font.setPointSize(18)
        painter.setFont(font)

        speed_text = f"{int(self.value)} km/h"
        painter.drawText(
            0,
            rect.height() // 2 - 30,
            rect.width(),
            40,
            Qt.AlignCenter,
            speed_text
        )
