from math import cos, pi
from PySide6.QtWidgets import QGraphicsEffect
from PySide6.QtCore import Property, QPointF, Qt, QRectF
from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QLinearGradient,
    QColor,
    QBrush
)


class AnimEffect(QGraphicsEffect):
    """
    AnimEffect dùng chung cho WidgetBase (qtmui)

    Hỗ trợ:
    - Opacity
    - Rotate / Flip / Scale
    - Background Image (src)
    - Background Gradient (gradient)
    """

    def __init__(
        self,
        parent=None,
        src: str | None = None,
        gradient: dict | None = None,
    ):
        super().__init__(parent)

        # ================= background image =================
        self._src = src
        self._pixmap = QPixmap(src) if src else None

        # ================= background gradient =================
        """
        gradient = {
            "colors": ("#ff512f", "#1c92d2"),
            "direction": "right",   # left | right | top | bottom
            "scale": 1.1            # mức zoom gradient
        }
        """
        self._gradient = gradient

        # ================= animation properties =================
        self._opacity = 1.0
        self._angle = 0.0
        self._rotationX = 0.0
        self._rotationY = 0.0
        self._scaleX = 1.0
        self._scaleY = 1.0
        self._scale = 1.0  # dùng chung cho background pan

        self.direction = "right"

    # ================= properties =================

    def getOpacity(self): return self._opacity
    def setOpacity(self, v): self._opacity = v; self.update()
    opacity = Property(float, getOpacity, setOpacity)

    def getAngle(self): return self._angle
    def setAngle(self, v): self._angle = v; self.update()
    angle = Property(float, getAngle, setAngle)

    def getRotationX(self): return self._rotationX
    def setRotationX(self, v): self._rotationX = v; self.update()
    rotationX = Property(float, getRotationX, setRotationX)

    def getRotationY(self): return self._rotationY
    def setRotationY(self, v): self._rotationY = v; self.update()
    rotationY = Property(float, getRotationY, setRotationY)

    def getScaleX(self): return self._scaleX
    def setScaleX(self, v): self._scaleX = v; self.update()
    scaleX = Property(float, getScaleX, setScaleX)

    def getScaleY(self): return self._scaleY
    def setScaleY(self, v): self._scaleY = v; self.update()
    scaleY = Property(float, getScaleY, setScaleY)

    def getScale(self): return self._scale
    def setScale(self, v): self._scale = v; self.update()
    scale = Property(float, getScale, setScale)

    # ================= draw =================

    def draw(self, painter: QPainter):
        pixmap = self.sourcePixmap()
        if pixmap.isNull():
            return

        painter.save()
        painter.setRenderHints(
            QPainter.Antialiasing |
            QPainter.SmoothPixmapTransform
        )

        # ================= opacity =================
        painter.setOpacity(self._opacity)

        w, h = pixmap.width(), pixmap.height()
        cx, cy = w / 2, h / 2

        # ================= flip / rotate =================
        painter.translate(cx, cy)

        if self._rotationX or self._rotationY:
            sx = cos(self._rotationY * pi / 180)
            sy = cos(self._rotationX * pi / 180)
            painter.scale(sx, sy)
        else:
            painter.scale(self._scaleX, self._scaleY)

        painter.translate(-cx, -cy)

        # ================= background gradient =================
        if self._gradient:
            self._draw_background_gradient(painter, w, h)

        # ================= background image =================
        if self._pixmap:
            self._draw_background_image(painter, w, h)

        # ================= draw widget =================
        self.drawSource(painter)
        painter.restore()

    # ==========================================================
    # ================= background: image ======================
    # ==========================================================

    def _draw_background_image(self, painter: QPainter, w: int, h: int):
        """
        Pan + scale background image
        """
        scale = self._scale
        progress = scale / 0.1 - 1.0

        pan = 0.1 * (w if self.direction in ("left", "right") else h)
        dx = dy = 0.0

        if self.direction == "right":
            dx = progress * pan
        elif self.direction == "left":
            dx = -progress * pan
        elif self.direction == "bottom":
            dy = progress * pan
        elif self.direction == "top":
            dy = -progress * pan

        scaled = self._pixmap.scaled(
            int(w * scale),
            int(h * scale),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        x = (w - scaled.width()) / 2 + dx
        y = (h - scaled.height()) / 2 + dy

        painter.drawPixmap(int(x), int(y), scaled)

    # ==========================================================
    # ================= background: gradient ===================
    # ==========================================================

    def _draw_background_gradient(self, painter: QPainter, w: int, h: int):
        """
        Vẽ background gradient + pan animation
        """
        colors = self._gradient.get("colors", ("#000", "#fff"))
        direction = self._gradient.get("direction", "right")
        scale = self._gradient.get("scale", 1.1)

        progress = self._scale / 0.1 - 1.0
        offset = progress * 0.1

        if direction == "right":
            grad = QLinearGradient(-w * offset, 0, w * scale, 0)
        elif direction == "left":
            grad = QLinearGradient(w * offset, 0, -w * scale, 0)
        elif direction == "bottom":
            grad = QLinearGradient(0, -h * offset, 0, h * scale)
        else:  # top
            grad = QLinearGradient(0, h * offset, 0, -h * scale)

        grad.setColorAt(0.0, QColor(colors[0]))
        grad.setColorAt(1.0, QColor(colors[1]))

        painter.fillRect(QRectF(0, 0, w, h), QBrush(grad))
