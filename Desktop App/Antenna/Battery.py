
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt

SOC = 100

class BatteryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.battery_level = SOC  # Initial battery level (percentage)
        self.setMinimumSize(150, 100)  # Increase height for the widget

    def set_battery_level(self, level):
        self.battery_level = level
        self.update()  # Repaint the widget with the new level

    def paintEvent(self, event):
        painter = QPainter(self)

        # Drawing the outer battery shape with a bolder stroke
        pen = QPen(Qt.black, 3.5)  # Increase pen width for a bolder stroke
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)  # Ensure no fill for the outer battery body
        painter.drawRect(5, 5, 130, 70)  # Draw the main battery body with increased height
        painter.drawRect(135, 35, 10, 10)  # Draw the battery positive terminal

        # Drawing the battery level (inner rectangle)
        if self.battery_level > 60:
            painter.setBrush(QBrush(QColor("green")))
        elif 20 < self.battery_level <= 60:
            painter.setBrush(QBrush(QColor("yellow")))
        else:
            painter.setBrush(QBrush(QColor("red")))

        # Adjust width calculation based on battery level
        width = int(self.battery_level * 1.3)
        painter.drawRect(5, 5, width, 70)  # Draw the inner rectangle for battery level

        # Display the battery level text inside the battery body
        painter.setPen(Qt.black)
        font = painter.font()
        font.setPointSize(20)  # Set font size for the battery percentage text
        painter.setFont(font)

        # Calculate the center of the battery body to place the percentage text
        text_rect = painter.boundingRect(5, 5, 130, 70, Qt.AlignCenter, f"{self.battery_level}%")
        painter.drawText(text_rect, Qt.AlignCenter, f"{self.battery_level}%")
