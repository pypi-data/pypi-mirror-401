import sys

# ============================================================
# Qt imports
# ============================================================
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QGraphicsEffect,
)
from PySide6.QtCore import (
    Qt,
    QRectF,
    Property,
    QPropertyAnimation,
)
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPainterPath,
    QConicalGradient,
)

# ============================================================
# AnimEffect
# ------------------------------------------------------------
# Đây là unified effect cho qtmui:
# - KHÔNG phụ thuộc widget cụ thể
# - Vẽ gradient border bằng kỹ thuật giống CSS ::before
# - Không làm hỏng layout, không clip sai
#
# Triết lý:
#   CSS:
#     element
#       ├── ::before (gradient border)
#       └── content
#
#   Qt:
#     QGraphicsEffect.draw()
#       ├── draw gradient layer (ngoài)
#       ├── clip inner rounded rect
#       └── drawSource() (widget gốc)
# ============================================================
class AnimEffect(QGraphicsEffect):
    def __init__(self, parent=None):
        super().__init__(parent)

        # =====================================================
        # Animation state
        # -----------------------------------------------------
        # angle: dùng cho QConicalGradient
        # Qt sẽ gọi setAngle() liên tục khi animation chạy
        # =====================================================
        self._angle = 0.0

        # =====================================================
        # Border config
        # -----------------------------------------------------
        # border : độ dày viền gradient
        # radius : bo góc content (PHẢI khớp với QPushButton)
        # =====================================================
        self.border = 2
        self.radius = 28

        # =====================================================
        # Gradient colors (cyclic)
        # -----------------------------------------------------
        # Màu đầu = màu cuối để loop liền mạch
        # =====================================================
        self.colors = [
            QColor("#ff4545"),
            QColor("#00ff99"),
            QColor("#006aff"),
            QColor("#ff0095"),
            QColor("#ff4545"),
        ]

    # =====================================================
    # boundingRectFor
    # -----------------------------------------------------
    # BẮT BUỘC override
    #
    # Lý do:
    # - QGraphicsEffect mặc định clip theo rect widget
    # - Border nằm NGOÀI rect → sẽ bị cắt
    #
    # Giải pháp:
    # - Mở rộng rect thêm border px mỗi phía
    # =====================================================
    def boundingRectFor(self, rect: QRectF) -> QRectF:
        b = self.border
        return rect.adjusted(-b, -b, b, b)

    # =====================================================
    # angle property
    # -----------------------------------------------------
    # Dùng cho QPropertyAnimation
    # Mỗi lần set → update() → draw()
    # =====================================================
    def getAngle(self):
        return self._angle

    def setAngle(self, v):
        self._angle = v
        self.update()

    angle = Property(float, getAngle, setAngle)

    # =====================================================
    # draw()
    # -----------------------------------------------------
    # THỨ TỰ VẼ RẤT QUAN TRỌNG:
    #
    # 1. Vẽ gradient border (outer)
    # 2. Clip inner rounded rect
    # 3. drawSource() → widget gốc
    #
    # TUYỆT ĐỐI:
    # - Không dùng drawPixmap cho content
    # - drawSource() để tránh clip bug Qt
    # =====================================================
    def draw(self, painter: QPainter):
        b = self.border

        # rect của widget gốc (chưa expand)
        src_rect = self.sourceBoundingRect()
        w, h = src_rect.width(), src_rect.height()

        # tâm để xoay gradient
        cx, cy = w / 2, h / 2

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        # =================================================
        # 1. GRADIENT BORDER (CSS ::before equivalent)
        # -------------------------------------------------
        # Dùng QConicalGradient:
        # - center = tâm widget
        # - angle = self._angle (animate)
        #
        # Giống:
        # conic-gradient(from var(--angle), ...)
        # =================================================
        grad = QConicalGradient(cx, cy, self._angle)

        step = 1 / (len(self.colors) - 1)
        for i, c in enumerate(self.colors):
            grad.setColorAt(i * step, c)

        # Rect ngoài = widget + border
        outer_rect = QRectF(
            src_rect.left() - b,
            src_rect.top() - b,
            w + b * 2,
            h + b * 2,
        )

        # Rounded rect ngoài
        outer_path = QPainterPath()
        outer_path.addRoundedRect(
            outer_rect,
            self.radius + b,   # bo góc đồng tâm
            self.radius + b,
        )

        painter.fillPath(outer_path, grad)

        # =================================================
        # 2. CLIP INNER (mask) không có không sao
        # -------------------------------------------------
        # Cắt phần content để:
        # - Border KHÔNG đè lên content
        # - Bo góc đồng tâm hoàn hảo
        #
        # Đây chính là "dao cắt" giống CSS padding + mask
        # =================================================
        # inner_path = QPainterPath()
        # inner_path.addRoundedRect(
        #     src_rect,
        #     self.radius,
        #     self.radius,
        # )

        # painter.setClipPath(inner_path)

        # =================================================
        # 3. DRAW CONTENT
        # -------------------------------------------------
        # drawSource():
        # - Qt tự render widget gốc
        # - Không bị clip lệch phải / dưới
        # - Đúng tuyệt đối layout
        # =================================================
        self.drawSource(painter)

        painter.restore()


# ============================================================
# GradientBorderButton
# ------------------------------------------------------------
# Button bình thường + gắn AnimEffect
# Không custom paint button → giữ native behavior
# ============================================================
class GradientBorderButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

        # Kích thước demo
        self.setFixedSize(240, 56)

        # Style content
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #121212;
                color: white;
                border: none;
                border-radius: 28px; /* PHẢI khớp AnimEffect.radius */
                font-size: 14px;
                font-weight: 600;
            }
            """
        )
        # self.setStyleSheet(
        #     """
        #     QPushButton {
        #         background-color: transparent;
        #         color: white;
        #         border: none;
        #         border-radius: 28px; /* PHẢI khớp AnimEffect.radius */
        #         font-size: 14px;
        #         font-weight: 600;
        #     }
        #     """
        # )

        # Gắn effect
        self.effect = AnimEffect(self)
        self.setGraphicsEffect(self.effect)

        # Animate gradient angle
        self.anim = QPropertyAnimation(self.effect, b"angle", self)
        self.anim.setStartValue(0)
        self.anim.setEndValue(360)
        self.anim.setDuration(3000)
        self.anim.setLoopCount(-1)
        self.anim.start()


# ============================================================
# Demo app
# ============================================================
class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qtmui – Gradient Border Button (Documented)")
        self.resize(420, 300)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)

        layout.addWidget(GradientBorderButton("Primary Action"))
        layout.addWidget(GradientBorderButton("Confirm"))


# ============================================================
# Entry
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec())


"""
tôi muốn xây dựng cơ chế after, before
""" 