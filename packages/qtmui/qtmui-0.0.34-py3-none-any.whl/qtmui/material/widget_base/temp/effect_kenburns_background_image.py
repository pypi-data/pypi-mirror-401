#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QRectF
from PySide6.QtGui import QPainter, QColor, QGradient, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsEffect,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFrame,
)


class KenBurnsEffect(QGraphicsEffect):
    """
    Ken Burns effect for background image with directions:
        - kenburnsTop
        - kenburnsBottom
        - kenburnsLeft
        - kenburnsRight
    This simulates a gentle zoom and pan on the provided image.
    """

    def __init__(self, variant="kenburnsTop", image_path=None, duration=5000, ease="linear", parent=None):
        super().__init__(parent)

        self.variant = variant
        self.image_path = image_path or "path/to/your/image.jpg"  # Placeholder; replace with actual path
        self.pixmap = QPixmap(self.image_path)
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

    def boundingRectFor(self, sourceRect: QRectF) -> QRectF:
        # Override để ngăn chặn size widget thay đổi do effect vẽ ngoài bound.
        # Bằng cách return sourceRect, effect bị clip trong bound gốc, không mở rộng size.
        return sourceRect

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

        # Tính scale và pan
        scale = 1.0 + 0.1 * self._progress
        pan_x = 0.0
        pan_y = 0.0
        pan_amount = 0.1 * h if self.direction in ("top", "bottom") else 0.1 * w

        if self.direction == "top":
            pan_y = -self._progress * pan_amount  # Dịch image lên (pan to top)
        elif self.direction == "bottom":
            pan_y = self._progress * pan_amount   # Dịch image xuống
        elif self.direction == "left":
            pan_x = -self._progress * pan_amount  # Dịch image trái
        elif self.direction == "right":
            pan_x = self._progress * pan_amount   # Dịch image phải
            
        print('pan_x, pan_y', pan_x, pan_y)

        painter.save()
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        
        painter.setOpacity(0.3)

        if self.pixmap.isNull():
            painter.fillRect(0, 0, w, h, QColor("gray"))
        else:
            # Scale pixmap lớn hơn để zoom, giữ aspect by expanding (cover)
            scaled_pix = self.pixmap.scaled(
                int(w * scale), int(h * scale),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            # Tính vị trí vẽ để center, rồi thêm pan
            draw_x = (w - scaled_pix.width()) / 2.0 + pan_x
            draw_y = (h - scaled_pix.height()) / 2.0 + pan_y

            # Vẽ scaled pixmap tại vị trí điều chỉnh
            print(draw_y)
            painter.drawPixmap(draw_x, 0, scaled_pix)


        painter.restore()

        # Vẽ content widget lên trên background
        self.drawSource(painter)


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
    frame.setStyleSheet("background-color: transparent; border-radius: 20px;border: 2px solid red;")
    layout.addWidget(frame)

    # ---------------- Apply effect ----------------
    effect = KenBurnsEffect(
        variant="kenburnsRight",  # kenburnsTop / kenburnsBottom / kenburnsLeft / kenburnsRight
        image_path="cover.webp",  # Thay bằng đường dẫn thực tế đến file png/jpg
    )
    frame.setGraphicsEffect(effect)

    # ---------------- Animate progress 0→1 LOOP ----------------
    anim = QPropertyAnimation(effect, b"progress")
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setDuration(640)
    # anim.setLoopCount(-1)
    anim.start()

    win.resize(420, 420)
    win.show()
    sys.exit(app.exec())