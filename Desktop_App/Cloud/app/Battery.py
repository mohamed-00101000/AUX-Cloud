from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt


class BatteryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.battery_level = 100  # default SOC
        self.setMinimumSize(150, 100)

    def set_battery_level(self, level):
        """
        Update battery level (0–100) and refresh widget.
        """
        try:
            self.battery_level = max(0, min(100, float(level)))
        except:
            self.battery_level = 0

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # ----------------------------
        # OUTER BATTERY SHELL
        # ----------------------------
        pen = QPen(Qt.black, 3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        # Main battery body
        painter.drawRect(5, 5, 130, 70)

        # Positive terminal
        painter.drawRect(135, 35, 10, 10)

        # ----------------------------
        # INNER LEVEL BAR
        # ----------------------------
        if self.battery_level > 60:
            fill_color = QColor("green")
        elif self.battery_level > 20:
            fill_color = QColor("yellow")
        else:
            fill_color = QColor("red")

        painter.setBrush(QBrush(fill_color))

        # Width of the filled part (max 130px)
        width = int((self.battery_level / 100) * 130)
        painter.drawRect(5, 5, width, 70)

        # ----------------------------
        # BATTERY PERCENT TEXT
        # ----------------------------
        painter.setPen(Qt.black)
        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)

        text = f"{int(self.battery_level)}%"
        painter.drawText(5, 5, 130, 70, Qt.AlignCenter, text)
