import sys
from PyQt5.QtWidgets import QApplication
from app.back import BackEndClass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BackEndClass()
    win.show()
    sys.exit(app.exec_())
