import sys
import math
import re

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QGraphicsEffect,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsBlurEffect,
)
from PySide6.QtCore import (
    Qt,
    QRectF,
    QPointF,
    Property,
    QPropertyAnimation,
    QEasingCurve,
    QTimer,
)
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPainterPath,
    QConicalGradient,
    QPixmap,
    QImage,
)

# ============================================================
# Parse CSS box-shadow (string) -> BoxShadowSpec
# Hỗ trợ:
#   "10px 10px grey"
#   "20px 20px 50px 15px grey"
#   "... pink inset"
#   "none"
# ============================================================

_COLOR_KEYWORDS = {
    "black": QColor(0, 0, 0),
    "white": QColor(255, 255, 255),
    "red": QColor(255, 0, 0),
    "green": QColor(0, 128, 0),
    "blue": QColor(0, 0, 255),
    "pink": QColor(255, 192, 203),
    "grey": QColor(128, 128, 128),
    "gray": QColor(128, 128, 128),
}


def _parse_px(token: str):
    m = re.fullmatch(r"(-?\d+)\s*px", token.strip().lower())
    return int(m.group(1)) if m else None


def _parse_color(token: str):
    t = token.strip().lower()

    if t in _COLOR_KEYWORDS:
        return QColor(_COLOR_KEYWORDS[t])

    # #RRGGBB / #AARRGGBB
    if re.fullmatch(r"#([0-9a-f]{6}|[0-9a-f]{8})", t):
        c = QColor(t)
        return c if c.isValid() else None

    # rgb(...)
    m = re.fullmatch(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", t)
    if m:
        return QColor(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    # rgba(..., a)  a: 0..1 hoặc 0..255
    m = re.fullmatch(
        r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([0-9]*\.?[0-9]+)\s*\)", t
    )
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        a_raw = float(m.group(4))
        a = int(a_raw * 255) if a_raw <= 1.0 else int(a_raw)
        return QColor(r, g, b, max(0, min(255, a)))

    return None


class BoxShadowSpec:
    """
    Tương đương CSS:
      box-shadow: x y blur spread color [inset];
    """
    def __init__(self, x=0, y=0, blur=0, spread=0, color=None, inset=False):
        self.x = int(x)
        self.y = int(y)
        self.blur = int(blur)
        self.spread = int(spread)
        self.color = QColor(color) if color is not None else QColor(0, 0, 0, 140)
        self.inset = bool(inset)


def parse_box_shadow(value: str):
    v = (value or "").strip().rstrip(";").strip()
    if not v or v.lower() == "none":
        return None

    tokens = [t for t in v.split() if t]

    inset = False
    if "inset" in [t.lower() for t in tokens]:
        inset = True
        tokens = [t for t in tokens if t.lower() != "inset"]

    # Lấy token màu đầu tiên parse được
    color = None
    rest = []
    for t in tokens:
        c = _parse_color(t)
        if c is not None and color is None:
            color = c
        else:
            rest.append(t)

    if color is None:
        color = QColor(0, 0, 0, 140)

    # Lấy px theo thứ tự: x y [blur] [spread]
    nums = []
    for t in rest:
        px = _parse_px(t)
        if px is not None:
            nums.append(px)

    if len(nums) < 2:
        return None

    x, y = nums[0], nums[1]
    blur = nums[2] if len(nums) >= 3 else 0
    spread = nums[3] if len(nums) >= 4 else 0

    # CSS keyword thường opaque -> set alpha nhìn giống web hơn
    if color.alpha() == 255:
        color.setAlpha(150)

    return BoxShadowSpec(x=x, y=y, blur=blur, spread=spread, color=color, inset=inset)


# ============================================================
# AnimEffect – compositor QtMUI:
# - OUTSET: bake pixmap cache (mask -> blur offscreen -> tô màu)
# - BLUR=0 vẫn phải ra shadow "cứng" (đúng CSS)
# - INSET: vẽ nhẹ trong draw()
# ============================================================
class AnimEffect(QGraphicsEffect):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Gradient border
        self.border = 2
        self.radius = 28
        self.colors = [
            QColor("#ff4545"),
            QColor("#00ff99"),
            QColor("#006aff"),
            QColor("#ff0095"),
            QColor("#ff4545"),
        ]
        
        self._startAngle = 0.0

        # Shadow spec
        self._shadow_spec = None

        # Match CSS
        self.blur_map = 0.85
        self.strength = 1.25

        # Cache outset shadow
        self._shadow_cache_pixmap = None
        self._shadow_cache_rect = QRectF()
        self._shadow_cache_key = None
        self._shadow_dirty = True
        self._rebuild_scheduled = False

    # =========================
    # API set box-shadow string
    # =========================
    def setBoxShadow(self, value: str):
        print('value__________', value)
        self._shadow_spec = parse_box_shadow(value)
        self._shadow_dirty = True
        self._shadow_cache_pixmap = None
        self._shadow_cache_key = None

        if not self._rebuild_scheduled:
            self._rebuild_scheduled = True
            QTimer.singleShot(0, self._rebuild_shadow_cache)

        self.update()

    # =====================================================
    # boundingRectFor:
    # - OUTSET shadow dù blur=0 vẫn phải expand theo offset/spread
    # - INSET không cần expand
    # =====================================================
    def boundingRectFor(self, rect: QRectF) -> QRectF:
        b = max(0, self.border)
        s = self._shadow_spec

        if s is None:
            return rect.adjusted(-b, -b, b, b)

        if s.inset or s.color.alpha() <= 0:
            return rect.adjusted(-b, -b, b, b)

        # OUTSET: blur có thể = 0 nhưng vẫn phải mở theo offset/spread
        expand = b + max(0, s.spread) + max(0, s.blur) + max(abs(s.x), abs(s.y))
        return rect.adjusted(-expand, -expand, expand, expand)

    # =====================================================
    # Angle property
    # =====================================================
    def getStartAngle(self):
        return self._startAngle

    def setStartAngle(self, v):
        self._startAngle = float(v)
        self.update()

    startAngle = Property(float, getStartAngle, setStartAngle)

    # =====================================================
    # DPR (HiDPI)
    # =====================================================
    def _get_dpr(self) -> float:
        w = self.parent()
        if w is not None and hasattr(w, "devicePixelRatioF"):
            try:
                return float(w.devicePixelRatioF())
            except Exception:
                return 1.0
        return 1.0

    # =====================================================
    # Cache key (outset)
    # =====================================================
    def _make_shadow_key(self, src_rect: QRectF, dpr: float, s: BoxShadowSpec) -> tuple:
        return (
            round(src_rect.width(), 2),
            round(src_rect.height(), 2),
            self.radius,
            s.x,
            s.y,
            s.blur,
            s.spread,
            s.color.rgba(),
            round(dpr, 2),
            round(self.blur_map, 3),
            round(self.strength, 3),
        )

    # =====================================================
    # Rebuild OUTSET shadow cache (ngoài draw)
    # - BLUR=0: không blur mask, vẫn tô màu và offset đúng CSS
    # =====================================================
    def _rebuild_shadow_cache(self):
        self._rebuild_scheduled = False

        src_rect = self.sourceBoundingRect()
        if src_rect.isNull() or src_rect.width() <= 0 or src_rect.height() <= 0:
            return

        s = self._shadow_spec
        dpr = self._get_dpr()

        # Không có shadow hoặc inset -> không build cache
        if s is None or s.inset or s.color.alpha() <= 0:
            self._shadow_cache_pixmap = None
            self._shadow_cache_key = None
            self._shadow_dirty = False
            self.update()
            return

        key = self._make_shadow_key(src_rect, dpr, s)
        if (not self._shadow_dirty) and (key == self._shadow_cache_key):
            return

        self._shadow_cache_key = key
        self._shadow_dirty = False

        full_rect = self.boundingRectFor(src_rect)
        self._shadow_cache_rect = full_rect

        img_w = max(1, int(math.ceil(full_rect.width() * dpr)))
        img_h = max(1, int(math.ceil(full_rect.height() * dpr)))

        # 1) mask trắng (shape + spread + offset)
        mask = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
        mask.fill(Qt.transparent)

        pmask = QPainter(mask)
        try:
            pmask.setRenderHint(QPainter.Antialiasing, True)
            pmask.scale(dpr, dpr)

            origin = QPointF(-full_rect.left(), -full_rect.top())

            base_rect = src_rect.adjusted(
                -s.spread, -s.spread, s.spread, s.spread
            ).translated(s.x, s.y).translated(origin)

            path = QPainterPath()
            path.addRoundedRect(
                base_rect,
                self.radius + s.spread,
                self.radius + s.spread,
            )
            pmask.fillPath(path, QColor(255, 255, 255, 255))
        finally:
            pmask.end()

        # 2) Nếu blur > 0 thì blur mask offscreen, còn blur == 0 thì dùng mask luôn
        if s.blur > 0:
            mask_pm = QPixmap.fromImage(mask)
            mask_pm.setDevicePixelRatio(dpr)

            scene = QGraphicsScene()
            item = QGraphicsPixmapItem(mask_pm)

            blur = QGraphicsBlurEffect()
            blur.setBlurRadius(float(s.blur) * float(self.blur_map))
            blur.setBlurHints(QGraphicsBlurEffect.QualityHint)

            item.setGraphicsEffect(blur)
            scene.addItem(item)

            blurred = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
            blurred.fill(Qt.transparent)

            pblur = QPainter(blurred)
            try:
                scene.setSceneRect(0, 0, full_rect.width(), full_rect.height())
                scene.render(pblur, QRectF(0, 0, full_rect.width(), full_rect.height()))
            finally:
                pblur.end()
        else:
            # BLUR=0: mask chính là "blurred" (bóng cứng, đúng CSS)
            blurred = mask

        # 3) tô màu + strength
        boosted = QColor(s.color)
        boosted_alpha = int(boosted.alpha() * float(self.strength))
        boosted.setAlpha(max(0, min(255, boosted_alpha)))

        colored = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
        colored.fill(Qt.transparent)

        pcol = QPainter(colored)
        try:
            pcol.fillRect(0, 0, img_w, img_h, boosted)
            pcol.setCompositionMode(QPainter.CompositionMode_DestinationIn)
            pcol.drawImage(0, 0, blurred)
        finally:
            pcol.end()

        pm = QPixmap.fromImage(colored)
        pm.setDevicePixelRatio(dpr)
        self._shadow_cache_pixmap = pm
        self.update()

    # =====================================================
    # Vẽ INSET shadow (nhẹ)
    # =====================================================
    def _draw_inset_shadow(self, painter: QPainter, src_rect: QRectF, s: BoxShadowSpec):
        if s.color.alpha() <= 0:
            return

        clip_path = QPainterPath()
        clip_path.addRoundedRect(src_rect, self.radius, self.radius)

        painter.save()
        try:
            painter.setClipPath(clip_path)

            # blur=0 inset: vẽ một lớp cứng ở trong
            if s.blur <= 0:
                rr = src_rect.adjusted(s.spread, s.spread, -s.spread, -s.spread).translated(s.x, s.y)
                path = QPainterPath()
                path.addRoundedRect(rr, max(0, self.radius - s.spread), max(0, self.radius - s.spread))
                painter.fillPath(path, s.color)
                return

            # blur>0 inset: vài vòng nhẹ
            steps = min(48, max(18, int(s.blur * 0.9)))
            base_rect = src_rect.adjusted(s.spread, s.spread, -s.spread, -s.spread).translated(s.x, s.y)

            for i in range(steps):
                t = i / steps
                alpha = int(s.color.alpha() * (1.0 - t) ** 2)
                if alpha <= 0:
                    continue

                c = QColor(s.color)
                c.setAlpha(alpha)

                inset = t * s.blur
                rr = base_rect.adjusted(inset, inset, -inset, -inset)
                if rr.width() <= 0 or rr.height() <= 0:
                    break

                path = QPainterPath()
                path.addRoundedRect(rr, max(0.0, self.radius - inset), max(0.0, self.radius - inset))
                painter.fillPath(path, c)
        finally:
            painter.restore()

    # =====================================================
    # draw()
    # =====================================================
    def draw(self, painter: QPainter):
        src_rect = self.sourceBoundingRect()
        w, h = src_rect.width(), src_rect.height()
        cx, cy = w / 2, h / 2

        painter.save()
        try:
            painter.setRenderHint(QPainter.Antialiasing, True)

            s = self._shadow_spec

            # 0) Shadow
            if s is not None and s.inset:
                self._draw_inset_shadow(painter, src_rect, s)
            else:
                # OUTSET: dùng cache (kể cả blur=0)
                if (self._shadow_cache_pixmap is None and s is not None) or self._shadow_dirty:
                    if not self._rebuild_scheduled:
                        self._rebuild_scheduled = True
                        QTimer.singleShot(0, self._rebuild_shadow_cache)

                if self._shadow_cache_pixmap is not None:
                    painter.drawPixmap(self._shadow_cache_rect.topLeft(), self._shadow_cache_pixmap)

            # 1) Gradient border
            grad = QConicalGradient(cx, cy, self._startAngle)
            step = 1.0 / (len(self.colors) - 1)
            for i, col in enumerate(self.colors):
                grad.setColorAt(i * step, col)

            b = self.border
            outer_rect = QRectF(src_rect.left() - b, src_rect.top() - b, w + b * 2, h + b * 2)
            outer_path = QPainterPath()
            outer_path.addRoundedRect(outer_rect, self.radius + b, self.radius + b)
            painter.fillPath(outer_path, grad)

            # 2) Clip inner để border không đè content
            inner_path = QPainterPath()
            inner_path.addRoundedRect(src_rect, self.radius, self.radius)
            painter.setClipPath(inner_path)

            # 3) Vẽ content gốc
            self.drawSource(painter)

        finally:
            painter.restore()


# ============================================================
# Button: nhận box-shadow string
# ============================================================
class GradientBorderButton(QPushButton):
    def __init__(self, text: str, box_shadow: str):
        super().__init__(text)

        self.setFixedSize(560, 56)

        self.setStyleSheet(
            """
            QPushButton {
                background-color: #121212;
                color: white;
                border: none;
                border-radius: 28px;
                font-size: 14px;
                font-weight: 600;
                padding: 0 16px;
                text-align: left;
            }
            """
        )

        self.effect = AnimEffect(self)
        self.setGraphicsEffect(self.effect)

        self.setBoxShadow(box_shadow)

        # Animate gradient angle
        self.anim_grad = QPropertyAnimation(self.effect, b"startAngle", self)
        self.anim_grad.setStartValue(0)
        self.anim_grad.setEndValue(360)
        self.anim_grad.setDuration(3000)
        self.anim_grad.setLoopCount(-1)
        self.anim_grad.setEasingCurve(QEasingCurve.Linear)
        self.anim_grad.start()

    def setBoxShadow(self, box_shadow: str):
        v = (box_shadow or "").strip()
        if v.lower().startswith("box-shadow:"):
            v = v.split(":", 1)[1].strip()
        self.effect.setBoxShadow(v)


# ============================================================
# Demo app: đủ ví dụ theo yêu cầu
# ============================================================
class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtMUI – Box-shadow string examples (blur=0 vẫn có shadow)")
        self.resize(1040, 860)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(26)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        examples = [
            "box-shadow: 10px 10px grey;",
            "box-shadow: 10px 10px grey;",
            "box-shadow: 50px 50px grey;",
            "box-shadow: 20px 20px 10px grey;",
            "box-shadow: 20px 20px 50px grey;",
            "box-shadow: 20px 20px 50px 15px grey;",
            "box-shadow: 20px 20px 20px 10px red;",
            "box-shadow: 20px 20px 20px 10px blue;",
            "box-shadow: 20px 20px 50px 10px pink inset;",
            "box-shadow: none;",
        ]

        for ex in examples:
            btn = GradientBorderButton(ex, ex)
            layout.addWidget(btn)


# ============================================================
# Entry
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec())
