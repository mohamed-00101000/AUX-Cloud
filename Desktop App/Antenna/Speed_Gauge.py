from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class CarGaugeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)  # Set the minimum size for the widget
        self.max_speed = 100  # Maximum speed of the gauge
        self.value = 0  # Current speed value

    def setValue(self, value):
        self.value = value
        self.update()  # Trigger a repaint to reflect the new speed value

    def paintEvent(self, event):
        painter = QPainter(self)
        gauge_rect = self.rect()

        # Draw the gauge background
        painter.setBrush(Qt.black)
        painter.drawEllipse(gauge_rect.adjusted(18, 18, -18, -18))

        # Draw the inner arc
        painter.setBrush(Qt.white)
        painter.drawEllipse(gauge_rect.adjusted(25, 25, -25, -25))

        # Draw the needle
        painter.setBrush(Qt.red)
        center = gauge_rect.center()
        painter.translate(center)
        angle = (self.value / self.max_speed) * 270 - 135
        painter.rotate(angle)

        # Define needle shape
        needle_polygon = QtGui.QPolygon([
            QtCore.QPoint(0, -gauge_rect.height() // 3 + 5),
            QtCore.QPoint(-5, 0),
            QtCore.QPoint(5, 0)
        ])
        painter.drawPolygon(needle_polygon)
        painter.resetTransform()

        # Draw the speed labels
        painter.setPen(Qt.black)
        font = QtGui.QFont('Arial', 12)
        font.setBold(True)
        painter.setFont(font)
        labels = range(0, self.max_speed + 1, 10)
        for i, label in enumerate(labels):
            angle = -135 + (i * 270 / (len(labels) - 1))
            painter.save()
            painter.translate(center)
            painter.rotate(angle)
            painter.translate(0, -gauge_rect.height() // 2 + 25)
            painter.drawText(-10, 0, 25, 25, Qt.AlignCenter, str(label))
            painter.restore()

        # Draw the current speed number below the gauge
        painter.setPen(Qt.black)
        font.setPointSize(17)
        painter.setFont(font)
        speed_text = str(self.value) + " km/h"
        x = gauge_rect.width() // 2 - 50
        y = gauge_rect.height() // 2 + 80
        painter.drawText(x, y, 100, 40, Qt.AlignCenter, speed_text)
