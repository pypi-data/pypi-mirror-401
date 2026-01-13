import sys
import math
import re
from functools import lru_cache

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

# =============================================================================
# 0) TỔNG QUAN Ý TƯỞNG TỐI ƯU (đọc trước)
# -----------------------------------------------------------------------------
# Vấn đề bạn nêu rất đúng:
#   - _shadow_cache_key hiện tại chỉ cache "nội bộ từng AnimEffect"
#   - Nếu tạo 10 button giống nhau (cùng box-shadow, cùng size) => mỗi button lại bake 1 lần
#   - Điều này lãng phí CPU + RAM, đặc biệt với blur lớn (50+)
#
# Giải pháp:
#   - Dùng cache toàn cục bằng functools.lru_cache
#   - Cùng 1 "key" (size + radius + shadow params + dpr + tuning) => trả về chung 1 QPixmap
#
# Lưu ý quan trọng:
#   - lru_cache chỉ cache theo tham số hashable (int/float/tuple/str)
#   - QPixmap/QImage là object trả về, lru_cache vẫn cache được (không cần hash)
#   - Tuy nhiên phải đảm bảo key đủ để phân biệt:
#       width/height, radius, border?, x,y, blur, spread, color_rgba, dpr, blur_map, strength
#
# Kết quả:
#   - Nếu bạn lặp lại "box-shadow: 10px 10px grey;" nhiều lần, các widget sẽ dùng chung pixmap cache
# =============================================================================


# =============================================================================
# 1) PARSER: CSS box-shadow string -> BoxShadowSpec
# =============================================================================

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
    """
    Parse một box-shadow string (không cần prefix 'box-shadow:').
    Hỗ trợ đúng các case bạn đưa:
      - "10px 10px grey"
      - "20px 20px 50px 15px grey"
      - "20px 20px 50px 10px pink inset"
      - "none"
    """
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

    # CSS keyword thường opaque => set alpha mặc định cho giống web
    if color.alpha() == 255:
        color.setAlpha(150)

    return BoxShadowSpec(x=x, y=y, blur=blur, spread=spread, color=color, inset=inset)


# =============================================================================
# 2) CACHE TOÀN CỤC BẰNG lru_cache (điểm chính bạn yêu cầu)
# -----------------------------------------------------------------------------
# Hàm dưới đây sẽ "bake" OUTSET shadow thành QPixmap dựa trên key.
#
# Vì lru_cache là toàn cục => nhiều widget giống nhau sẽ dùng chung kết quả.
#
# Giới hạn maxsize:
#   - Bạn có thể tăng/giảm tuỳ nhu cầu.
#   - 256 thường đủ tốt cho UI (nhiều kiểu shadow khác nhau).
# =============================================================================

@lru_cache(maxsize=256)
def build_outset_shadow_pixmap_cached(
    # Kích thước src rect (kích thước nút)
    src_w: int,
    src_h: int,

    # Bo góc của shape gốc
    radius: int,

    # Shadow params
    x: int,
    y: int,
    blur: int,
    spread: int,
    color_rgba: int,

    # HiDPI
    dpr_x100: int,     # dpr * 100 (tránh float key)
    blur_map_x100: int,  # blur_map * 100
    strength_x100: int,  # strength * 100
):
    """
    Trả về QPixmap shadow OUTSET đã bake.
    Key chỉ gồm số nguyên => lru_cache hoạt động ổn định.

    Ghi chú:
    - QPixmap trả về có setDevicePixelRatio(dpr)
    - Pixmap bao gồm cả phần mở rộng (expand) để chứa shadow.
    - Caller sẽ tự đặt vị trí (top-left) bằng QRectF.
    """
    print("__________")  
    
    dpr = dpr_x100 / 100.0
    blur_map = blur_map_x100 / 100.0
    strength = strength_x100 / 100.0

    # Tính expand giống logic boundingRectFor (không cộng border ở đây)
    expand = max(0, spread) + max(0, blur) + max(abs(x), abs(y))

    full_w = src_w + 2 * expand
    full_h = src_h + 2 * expand

    img_w = max(1, int(math.ceil(full_w * dpr)))
    img_h = max(1, int(math.ceil(full_h * dpr)))

    color = QColor.fromRgba(color_rgba)
    if color.alpha() <= 0:
        img = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.transparent)
        pm = QPixmap.fromImage(img)
        pm.setDevicePixelRatio(dpr)
        return pm

    # ---------------------------------------------------------
    # B1) Tạo mask trắng (rounded rect + spread + offset)
    # ---------------------------------------------------------
    mask = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
    mask.fill(Qt.transparent)

    pmask = QPainter(mask)
    try:
        pmask.setRenderHint(QPainter.Antialiasing, True)
        pmask.scale(dpr, dpr)

        # src_rect gốc nằm tại (expand, expand)
        # offset bóng: +x +y
        base_left = expand + x - spread
        base_top = expand + y - spread
        base_w = src_w + 2 * spread
        base_h = src_h + 2 * spread

        rr = QRectF(base_left, base_top, base_w, base_h)

        path = QPainterPath()
        path.addRoundedRect(rr, radius + spread, radius + spread)
        pmask.fillPath(path, QColor(255, 255, 255, 255))
    finally:
        pmask.end()

    # ---------------------------------------------------------
    # B2) Blur mask nếu blur > 0 (blur offscreen bằng C++)
    #     blur=0 => mask chính là kết quả (bóng cứng)
    # ---------------------------------------------------------
    if blur > 0:
        mask_pm = QPixmap.fromImage(mask)
        mask_pm.setDevicePixelRatio(dpr)

        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(mask_pm)

        blur_eff = QGraphicsBlurEffect()
        blur_eff.setBlurRadius(float(blur) * float(blur_map))
        blur_eff.setBlurHints(QGraphicsBlurEffect.QualityHint)

        item.setGraphicsEffect(blur_eff)
        scene.addItem(item)

        blurred = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
        blurred.fill(Qt.transparent)

        pblur = QPainter(blurred)
        try:
            scene.setSceneRect(0, 0, full_w, full_h)
            scene.render(pblur, QRectF(0, 0, full_w, full_h))
        finally:
            pblur.end()
    else:
        blurred = mask

    # ---------------------------------------------------------
    # B3) Tô màu shadow + nhân strength:
    #     fillRect(color) rồi DestinationIn với blurred mask
    # ---------------------------------------------------------
    boosted = QColor(color)
    boosted_alpha = int(boosted.alpha() * float(strength))
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
    return pm


# =============================================================================
# 3) ANIMEFFECT: dùng cache toàn cục cho OUTSET
# =============================================================================

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
        self._angle = 0.0

        # Shadow spec
        self._shadow_spec = None

        # Tuning match CSS (2 tham số bạn đang dùng)
        self.blur_map = 0.85
        self.strength = 1.25

        # Cache nội bộ: giờ chỉ giữ reference pixmap đã lấy từ lru_cache
        # (nó vẫn có ích để tránh gọi cache quá nhiều lần trong 1 frame)
        self._shadow_cache_pixmap = None
        self._shadow_cache_rect = QRectF()
        self._shadow_dirty = True
        self._rebuild_scheduled = False

    # =========================
    # API set box-shadow string
    # =========================
    def setBoxShadow(self, value: str):
        self._shadow_spec = parse_box_shadow(value)
        self._shadow_dirty = True
        self._shadow_cache_pixmap = None

        if not self._rebuild_scheduled:
            self._rebuild_scheduled = True
            QTimer.singleShot(0, self._rebuild_shadow_cache)

        self.update()

    # =====================================================
    # boundingRectFor: nới để tránh clip OUTSET
    # =====================================================
    def boundingRectFor(self, rect: QRectF) -> QRectF:
        b = max(0, self.border)
        s = self._shadow_spec

        if s is None:
            return rect.adjusted(-b, -b, b, b)

        if s.inset or s.color.alpha() <= 0:
            return rect.adjusted(-b, -b, b, b)

        expand = b + max(0, s.spread) + max(0, s.blur) + max(abs(s.x), abs(s.y))
        return rect.adjusted(-expand, -expand, expand, expand)

    # =====================================================
    # Angle property
    # =====================================================
    def getAngle(self):
        return self._angle

    def setAngle(self, v):
        self._angle = float(v)
        self.update()

    angle = Property(float, getAngle, setAngle)

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
    # Rebuild shadow cache:
    # - OUTSET: lấy từ lru_cache (toàn cục)
    # - INSET: không dùng lru_cache ở bản demo này (vẽ trực tiếp)
    # =====================================================
    def _rebuild_shadow_cache(self):
        self._rebuild_scheduled = False

        src_rect = self.sourceBoundingRect()
        if src_rect.isNull() or src_rect.width() <= 0 or src_rect.height() <= 0:
            return

        s = self._shadow_spec
        if s is None or s.color.alpha() <= 0:
            self._shadow_cache_pixmap = None
            self._shadow_dirty = False
            self.update()
            return

        # INSET: không bake vào pixmap cache ở bản này
        if s.inset:
            self._shadow_cache_pixmap = None
            self._shadow_dirty = False
            self.update()
            return

        # Ở QGraphicsEffect, sourceBoundingRect thường bắt đầu (0,0)
        # Ta chỉ cần width/height để build pixmap cache.
        src_w = int(round(src_rect.width()))
        src_h = int(round(src_rect.height()))

        dpr = self._get_dpr()

        # expand dùng để tính _shadow_cache_rect (vị trí pixmap so với src_rect)
        expand = max(0, s.spread) + max(0, s.blur) + max(abs(s.x), abs(s.y))

        # full rect trong toạ độ effect: src_rect được nới ra bởi expand + border
        # Lưu ý: trong build_outset_shadow_pixmap_cached() mình không cộng border,
        # vì border chỉ phục vụ gradient outline, không ảnh hưởng vùng shadow.
        full_rect = QRectF(
            src_rect.left() - expand,
            src_rect.top() - expand,
            src_rect.width() + 2 * expand,
            src_rect.height() + 2 * expand,
        )
        self._shadow_cache_rect = full_rect

        # Key cho lru_cache: tất cả là int để ổn định
        pm = build_outset_shadow_pixmap_cached(
            src_w=src_w,
            src_h=src_h,
            radius=int(self.radius),
            x=int(s.x),
            y=int(s.y),
            blur=int(s.blur),
            spread=int(s.spread),
            color_rgba=int(s.color.rgba()),
            dpr_x100=int(round(dpr * 100)),
            blur_map_x100=int(round(self.blur_map * 100)),
            strength_x100=int(round(self.strength * 100)),
        )

        self._shadow_cache_pixmap = pm
        self._shadow_dirty = False
        self.update()

    # =====================================================
    # Vẽ INSET shadow (demo nhẹ)
    # =====================================================
    def _draw_inset_shadow(self, painter: QPainter, src_rect: QRectF, s: BoxShadowSpec):
        if s.color.alpha() <= 0:
            return

        clip_path = QPainterPath()
        clip_path.addRoundedRect(src_rect, self.radius, self.radius)

        painter.save()
        try:
            painter.setClipPath(clip_path)

            # blur=0 inset: 1 lớp cứng
            if s.blur <= 0:
                rr = src_rect.adjusted(
                    s.spread, s.spread, -s.spread, -s.spread
                ).translated(s.x, s.y)
                path = QPainterPath()
                path.addRoundedRect(rr, max(0, self.radius - s.spread), max(0, self.radius - s.spread))
                painter.fillPath(path, s.color)
                return

            # blur>0 inset: vài vòng nhẹ (demo)
            steps = min(48, max(18, int(s.blur * 0.9)))
            base_rect = src_rect.adjusted(
                s.spread, s.spread, -s.spread, -s.spread
            ).translated(s.x, s.y)

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
    # draw(): cực nhẹ
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
                # OUTSET: dùng pixmap từ cache toàn cục
                if (self._shadow_cache_pixmap is None and s is not None) or self._shadow_dirty:
                    if not self._rebuild_scheduled:
                        self._rebuild_scheduled = True
                        QTimer.singleShot(0, self._rebuild_shadow_cache)

                if self._shadow_cache_pixmap is not None:
                    painter.drawPixmap(self._shadow_cache_rect.topLeft(), self._shadow_cache_pixmap)

            # 1) Gradient border
            grad = QConicalGradient(cx, cy, self._angle)
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


# =============================================================================
# 4) BUTTON: nhận box-shadow string
# =============================================================================

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

        # Animate gradient angle (demo)
        self.anim_grad = QPropertyAnimation(self.effect, b"angle", self)
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


# =============================================================================
# 5) DEMO: có 2 lần "10px 10px grey" để kiểm chứng lru_cache
# =============================================================================

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtMUI – lru_cache global shadow cache")
        self.resize(1040, 900)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(26)
        layout.setContentsMargins(30, 30, 30, 30)

        examples = [
            "box-shadow: 10px 10px grey;",
            "box-shadow: 10px 10px grey;",  # lặp lại để test cache toàn cục
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


# =============================================================================
# 6) ENTRY
# =============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec())
