#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide6.QtCore import Qt, Property, QPropertyAnimation
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QGradient
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsEffect,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFrame,
)


class BackgroundPanEffect(QGraphicsEffect):
    """
    Pan background gradient theo direction:
        - panTop
        - panBottom
        - panLeft
        - panRight
    """

    def __init__(self, variant="panTop", colors=None, duration=5000, ease="linear", parent=None):
        super().__init__(parent)

        self.variant = variant
        self.colors = colors or ["#ee7752", "#e73c7e", "#23a6d5", "#23d5ab"]
        self._progress = 0.0  # 0 → 1

        self.direction = self._detect_direction(variant)

    @staticmethod
    def _detect_direction(v):
        v = v.lower()
        if "top" in v:
            return "top"
        if "bottom" in v:
            return "bottom"
        if "left" in v:
            return "left"
        if "right" in v:
            return "right"
        return "top"

    # ---------------- Property ----------------
    def getProgress(self):
        return self._progress

    def setProgress(self, v):
        self._progress = v
        self.update()

    progress = Property(float, getProgress, setProgress)

    # ---------------- Drawing ----------------
    def draw(self, painter: QPainter):
        pixmap = self.sourcePixmap()
        if pixmap.isNull():
            return

        w, h = pixmap.width(), pixmap.height()

        grad = None
        offset = 0.0

        colors_ext = self.colors + [self.colors[0]]
        num_intervals = len(self.colors)

        if self.direction in ("top", "bottom"):
            fill_factor = 6
            fill_h = h * fill_factor
            fill_w = w
            grad = QLinearGradient(0, 0, 0, fill_h)
            for i in range(len(colors_ext)):
                grad.setColorAt(float(i) / num_intervals, QColor(colors_ext[i]))

            pos = self._progress
            if self.direction == "top":
                pos = 1 - pos  # reverse for top (pan upwards)
            offset = -pos * fill_h
            grad.setStart(0, offset)
            grad.setFinalStop(0, offset + fill_h)

        else:  # left, right
            fill_factor = 6
            fill_w = w * fill_factor
            fill_h = h
            grad = QLinearGradient(0, 0, fill_w, 0)
            for i in range(len(colors_ext)):
                grad.setColorAt(float(i) / num_intervals, QColor(colors_ext[i]))

            pos = self._progress
            if self.direction == "left":
                pos = 1 - pos  # reverse for left (pan leftwards)
            offset = -pos * fill_w
            grad.setStart(offset, 0)
            grad.setFinalStop(offset + fill_w, 0)

        if grad:
            grad.setSpread(QGradient.RepeatSpread)

        painter.save()
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # Fill background without translate
        if grad:
            painter.fillRect(0, 0, w, h, grad)

        # Vẽ widget lên trên
        self.drawSource(painter)

        painter.restore()


# ================= DEMO ====================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = QMainWindow()
    central = QWidget()
    layout = QVBoxLayout(central)
    layout.setAlignment(Qt.AlignCenter)
    win.setCentralWidget(central)

    frame = QFrame()
    frame.setFixedSize(320, 240)
    frame.setStyleSheet("background: transparent; border-radius: 20px;")
    layout.addWidget(frame)

    # ---------------- Apply effect ----------------
    effect = BackgroundPanEffect(
        variant="panRight",  # panTop / panBottom / panLeft / panRight
        colors=["#ee7752", "#e73c7e", "#23a6d5", "#23d5ab"],
    )
    frame.setGraphicsEffect(effect)

    # ---------------- Animate progress 0→1 LOOP ----------------
    anim = QPropertyAnimation(effect, b"progress")
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setDuration(10000)
    anim.setLoopCount(-1)
    anim.start()

    win.resize(420, 420)
    win.show()
    sys.exit(app.exec())