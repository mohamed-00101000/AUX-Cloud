import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QStyleFactory, QGridLayout, QGroupBox


def apply_gauge_glow(label):
    glow = QGraphicsDropShadowEffect()
    glow.setBlurRadius(90)
    glow.setXOffset(0)
    glow.setYOffset(0)
    glow.setColor(QtGui.QColor(220, 20, 30, 180))
    label.setGraphicsEffect(glow)


def fix_thermal_summary_layout(w):
    summary_box = w.findChild(QGroupBox, "grpThermalSummary")
    if not summary_box:
        return

    grid = summary_box.layout()
    if not isinstance(grid, QtWidgets.QGridLayout):
        return

    # 🔥 THIS IS THE FIX
    grid.setColumnStretch(0, 1)  # labels column expands
    grid.setColumnStretch(1, 0)  # values column stays tight

    # Optional polish
    grid.setHorizontalSpacing(18)
    grid.setVerticalSpacing(14)

    for name in (
        "lblSummaryLeftMos",
        "lblSummaryRightMos",
        "lblSummaryMotor",
        "lblSummaryAmbient",
    ):
        lbl = w.findChild(QtWidgets.QLabel, name)
        if lbl:
            lbl.setSizePolicy(
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Preferred
            )
            lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


# ---------------------------
# App setup
# ---------------------------
app = QtWidgets.QApplication(sys.argv)
app.setStyle(QStyleFactory.create("Fusion"))

# ---------------------------
# Load UI
# ---------------------------
w = uic.loadUi("front.ui")

# IMPORTANT:
# Move the .ui stylesheet to the QApplication so it applies consistently everywhere.
# (Does NOT change structure; just makes QSS application more reliable.)
ui_qss = w.styleSheet()
if ui_qss:
    app.setStyleSheet(ui_qss)
    w.setStyleSheet("")

# ---------------------------
# Fix layout behavior (THE BUG)
# ---------------------------
fix_thermal_summary_layout(w)

# ---------------------------
# Gauge: glow + stacking
# ---------------------------
bg = w.findChild(QtWidgets.QLabel, "lblGaugeBg")
needle = w.findChild(QtWidgets.QLabel, "lblGaugeNeedle")

if bg:
    apply_gauge_glow(bg)

if needle:
    needle.raise_()
    needle.show()

# Optional: glow on ASURT title
title = w.findChild(QtWidgets.QLabel, "titleLabel")
if title:
    title_glow = QGraphicsDropShadowEffect()
    title_glow.setBlurRadius(18)
    title_glow.setOffset(0, 0)
    title_glow.setColor(QtGui.QColor(190, 30, 45))
    title.setGraphicsEffect(title_glow)

# ---------------------------
# Show window
# ---------------------------
w.show()
sys.exit(app.exec_())
