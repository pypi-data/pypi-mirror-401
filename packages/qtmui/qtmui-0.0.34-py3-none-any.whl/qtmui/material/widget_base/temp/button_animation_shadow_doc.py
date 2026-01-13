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

# =============================================================================
# 0) TỔNG QUAN (đọc trước khi xem code)
# -----------------------------------------------------------------------------
# Mục tiêu:
#   - Mô phỏng CSS box-shadow cho QPushButton (Qt/PySide6)
#   - Nhận box-shadow dưới dạng chuỗi giống CSS:
#       "10px 10px grey"
#       "20px 20px 50px 15px grey"
#       "20px 20px 50px 10px pink inset"
#       "none"
#   - Shadow OUTSET (thường) phải giống CSS:
#       + Có offset (x,y), có spread, có blur (Gaussian-like)
#       + blur=0 vẫn phải có bóng "cứng" (đúng CSS)
#   - Shadow INSET: demo cơ bản (không blur effect offscreen vì mask ngược phức tạp hơn)
#
# Vấn đề kỹ thuật:
#   - Nếu vẽ blur bằng vòng for trong draw() => rất nặng vì draw() chạy liên tục.
#   - Nếu tự làm blur bằng nhiều vòng alpha => dễ bị "gợn" / banding.
#
# Giải pháp tối ưu:
#   - "Bake" (render sẵn) shadow OUTSET ra QPixmap cache.
#   - Việc bake diễn ra ngoài draw() (schedule bằng QTimer.singleShot).
#   - Bake dùng kỹ thuật:
#       1) Vẽ mask trắng của hình (rounded rect + spread + offset)
#       2) Blur mask bằng QGraphicsBlurEffect (C++ xử lý, mượt, ít banding)
#       3) Tô màu shadow bằng CompositionMode_DestinationIn:
#           alpha_kết_quả = alpha_màu * alpha_mask_blur
#   - draw() chỉ:
#       + drawPixmap(shadow_cache)
#       + vẽ gradient border
#       + clip và drawSource()
#
# Lưu ý:
#   - QGraphicsEffect trong PySide6 KHÔNG có source()/parentWidget().
#     Cách an toàn lấy DPR (HiDPI) là dùng self.parent() vì effect được gắn vào button.
# =============================================================================


# =============================================================================
# 1) PARSER: CHUYỂN CHUỖI CSS box-shadow -> BoxShadowSpec
# -----------------------------------------------------------------------------
# Parser này tối giản theo đúng các ví dụ bạn đưa:
#   - Chỉ 1 shadow (không xử lý multi-shadow tách bằng dấu phẩy)
#   - Nhận màu keyword, hex, rgb/rgba
#   - Cú pháp:
#       x y [blur] [spread] color [inset]
#   - "none" => không có shadow
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
    """Parse '10px' hoặc '-5px' -> int, nếu không khớp trả None."""
    m = re.fullmatch(r"(-?\d+)\s*px", token.strip().lower())
    return int(m.group(1)) if m else None


def _parse_color(token: str):
    """
    Parse màu từ token:
      - keyword: red/blue/grey...
      - hex: #RRGGBB hoặc #AARRGGBB
      - rgb(r,g,b)
      - rgba(r,g,b,a)
    """
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
    Thông số shadow đã parse xong.
    Tương đương CSS:
      box-shadow: x y blur spread color [inset];

    - x, y   : offset (dịch bóng)
    - blur   : blur radius
    - spread : spread radius (phóng to shape trước khi blur)
    - color  : màu shadow (có alpha)
    - inset  : True nếu là inset shadow
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

    Ví dụ:
      "10px 10px grey"
      "20px 20px 50px 15px grey"
      "20px 20px 50px 10px pink inset"
      "none"
    """
    v = (value or "").strip().rstrip(";").strip()
    if not v or v.lower() == "none":
        return None

    tokens = [t for t in v.split() if t]

    # Nhận biết inset
    inset = False
    if "inset" in [t.lower() for t in tokens]:
        inset = True
        tokens = [t for t in tokens if t.lower() != "inset"]

    # Tìm màu: lấy token đầu tiên parse được thành QColor
    """
        rest:   ['10px', '10px']
                ['50px', '50px']
                ['20px', '20px', '10px']
                ['20px', '20px', '50px']
                ['20px', '20px', '50px', '15px']
                ['20px', '20px', '20px', '10px']
                ['20px', '20px', '20px', '10px']
                ['20px', '20px', '50px', '10px']
    """
    color = None
    rest = []
    for t in tokens:
        c = _parse_color(t)
        if c is not None and color is None:
            color = c
        else:
            rest.append(t)

    if color is None:
        # Nếu không có màu, dùng mặc định đen mờ
        color = QColor(0, 0, 0, 140)

    # Lấy px theo thứ tự: x y [blur] [spread]
    nums = []
    for t in rest:
        px = _parse_px(t)
        if px is not None:
            nums.append(px)

    if len(nums) < 2:
        # Không đủ x y => parse fail
        return None

    x, y = nums[0], nums[1]
    blur = nums[2] if len(nums) >= 3 else 0
    spread = nums[3] if len(nums) >= 4 else 0

    # Keyword màu thường opaque 255 => set alpha mặc định cho giống web
    # (CSS thật: màu shadow thường có alpha, nếu không sẽ rất gắt)
    if color.alpha() == 255:
        color.setAlpha(150)

    return BoxShadowSpec(x=x, y=y, blur=blur, spread=spread, color=color, inset=inset)


# =============================================================================
# 2) ANIMEFFECT: "COMPOSITOR" TẠO SHADOW + BORDER
# -----------------------------------------------------------------------------
# Đây là trung tâm:
#   - Nhận BoxShadowSpec
#   - Nếu OUTSET:
#       + Bake shadow => QPixmap cache (tạo mask, blur offscreen, tô màu)
#       + draw() chỉ vẽ pixmap cache
#   - Nếu INSET:
#       + demo vẽ trực tiếp (clip + vòng ít bước)
#         (Nếu muốn inset chuẩn CSS hơn nữa: cũng có thể bake theo kiểu mask ngược)
#
# Hai tham số quan trọng để match CSS:
#   - blur_map  : blurQt = blurCSS * blur_map
#                (Qt blur thường "lan" hơn CSS -> blur_map < 1)
#   - strength  : nhân alpha để bóng nổi như CSS
# =============================================================================

class AnimEffect(QGraphicsEffect):
    def __init__(self, parent=None):
        super().__init__(parent)

        # -------------------------
        # Border gradient (tương tự ::before trong CSS)
        # -------------------------
        self.border = 2
        self.radius = 28
        self.colors = [
            QColor("#ff4545"),
            QColor("#00ff99"),
            QColor("#006aff"),
            QColor("#ff0095"),
            QColor("#ff4545"),
        ]
        self._angle = 0.0  # góc xoay gradient

        # Shadow spec (set từ button)
        self._shadow_spec = None

        # -------------------------
        # Tinh chỉnh để match CSS (bạn có thể chỉnh 2 tham số này)
        # -------------------------
        self.blur_map = 0.85   # giảm blur để bóng tập trung hơn (gần CSS)
        self.strength = 1.25   # tăng alpha để bóng "nổi" giống CSS

        # -------------------------
        # Cache cho OUTSET shadow
        # -------------------------
        self._shadow_cache_pixmap = None
        self._shadow_cache_rect = QRectF()
        self._shadow_cache_key = None
        self._shadow_dirty = True
        self._rebuild_scheduled = False

    # =====================================================
    # API: nhận box-shadow string (đã loại prefix "box-shadow:")
    # =====================================================
    def setBoxShadow(self, value: str):
        self._shadow_spec = parse_box_shadow(value)

        # Đánh dấu cache cần rebuild
        self._shadow_dirty = True
        self._shadow_cache_pixmap = None
        self._shadow_cache_key = None

        # Schedule rebuild ngoài draw() để tránh lag
        if not self._rebuild_scheduled:
            self._rebuild_scheduled = True
            QTimer.singleShot(0, self._rebuild_shadow_cache)

        self.update()

    # =====================================================
    # boundingRectFor:
    #   - OUTSET shadow cần nới rect để không bị clip
    #   - blur=0 vẫn phải nới theo offset/spread (vì bóng "cứng" vẫn có)
    #   - INSET không cần nới
    # =====================================================
    def boundingRectFor(self, rect: QRectF) -> QRectF:
        b = max(0, self.border)
        s = self._shadow_spec

        if s is None:
            return rect.adjusted(-b, -b, b, b)

        if s.inset or s.color.alpha() <= 0:
            # inset bóng nằm trong => không cần nới
            return rect.adjusted(-b, -b, b, b)

        expand = b + max(0, s.spread) + max(0, s.blur) + max(abs(s.x), abs(s.y))
        return rect.adjusted(-expand, -expand, expand, expand)

    # =====================================================
    # Property angle cho animation gradient
    # =====================================================
    def getAngle(self):
        return self._angle

    def setAngle(self, v):
        self._angle = float(v)
        self.update()

    angle = Property(float, getAngle, setAngle)

    # =====================================================
    # DPR (HiDPI):
    #   QGraphicsEffect không có parentWidget()/source() trong PySide6.
    #   Vì effect gắn vào QPushButton, self.parent() chính là button.
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
    # Cache key: tránh rebuild nếu không đổi gì
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
    # Các bước:
    #   1) Vẽ mask trắng (rounded rect + spread + offset)
    #   2) Nếu blur > 0:
    #        blur mask bằng QGraphicsBlurEffect offscreen (C++ nhanh & mượt)
    #      Nếu blur == 0:
    #        dùng mask luôn (shadow "cứng")
    #   3) Tô màu shadow:
    #        fillRect(màu shadow) rồi DestinationIn với mask
    # =====================================================
    def _rebuild_shadow_cache(self):
        self._rebuild_scheduled = False

        # hình chữ nhật gốc của widget/source (button thật), chưa có shadow
        src_rect = self.sourceBoundingRect()
        if src_rect.isNull() or src_rect.width() <= 0 or src_rect.height() <= 0:
            return

        s = self._shadow_spec
        dpr = self._get_dpr()

        # Không có shadow hoặc inset -> không cần cache
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

        # full_rect là rect đã nới theo shadow (để vẽ pixmap đúng vị trí)
        full_rect = self.boundingRectFor(src_rect)
        self._shadow_cache_rect = full_rect

        img_w = max(1, int(math.ceil(full_rect.width() * dpr)))
        img_h = max(1, int(math.ceil(full_rect.height() * dpr)))

        # 1) mask trắng
        mask = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
        mask.fill(Qt.transparent)

        pmask = QPainter(mask)
        try:
            pmask.setRenderHint(QPainter.Antialiasing, True)
            pmask.scale(dpr, dpr)

            # origin để đưa full_rect về (0,0) trong ảnh cache
            origin = QPointF(-full_rect.left(), -full_rect.top())

            """
                adjusted: nới ra
                translated(s.x, s.y): dịch đi so với gốc, offset
                translated(origin): đưa về ảnh cache
                Trước bước này:

                    base_rect đang nằm trong tọa độ widget thật

                    QImage cache thì tọa độ bắt đầu từ (0,0)

                    ➡️ Ta cần:

                    base_rect (widget space)
                    → base_rect (cache space)


                    📌 Công thức:

                    cache_x = widget_x - full_rect.left()
                    cache_y = widget_y - full_rect.top()
            """
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

        # 2) blur mask nếu blur > 0
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
            # blur=0: dùng mask luôn -> bóng cứng (đúng CSS)
            blurred = mask

        # 3) tô màu + strength
        boosted = QColor(s.color)
        boosted_alpha = int(boosted.alpha() * float(self.strength))
        boosted.setAlpha(max(0, min(255, boosted_alpha)))

        colored = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
        colored.fill(Qt.transparent)

        pcol = QPainter(colored)
        try:
            # Fill màu shadow toàn ảnh
            pcol.fillRect(0, 0, img_w, img_h, boosted)

            # DestinationIn: giữ lại alpha theo blurred mask
            pcol.setCompositionMode(QPainter.CompositionMode_DestinationIn)
            pcol.drawImage(0, 0, blurred)
        finally:
            pcol.end()

        pm = QPixmap.fromImage(colored)
        pm.setDevicePixelRatio(dpr)
        self._shadow_cache_pixmap = pm
        self.update()

    # =====================================================
    # Vẽ INSET shadow (demo):
    #   - Clip theo rounded rect
    #   - blur=0: 1 lớp cứng
    #   - blur>0: vài vòng nhẹ (ít bước để không nặng)
    # =====================================================
    def _draw_inset_shadow(self, painter: QPainter, src_rect: QRectF, s: BoxShadowSpec):
        if s.color.alpha() <= 0:
            return

        clip_path = QPainterPath()
        clip_path.addRoundedRect(src_rect, self.radius, self.radius)

        painter.save()
        try:
            painter.setClipPath(clip_path)

            if s.blur <= 0:
                # Inset blur=0: vẽ 1 lớp cứng bên trong
                rr = src_rect.adjusted(
                    s.spread, s.spread, -s.spread, -s.spread
                ).translated(s.x, s.y)
                path = QPainterPath()
                path.addRoundedRect(
                    rr,
                    max(0, self.radius - s.spread),
                    max(0, self.radius - s.spread),
                )
                painter.fillPath(path, s.color)
                return

            # Inset blur>0: vài vòng nhẹ để mô phỏng mờ
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
                path.addRoundedRect(
                    rr,
                    max(0.0, self.radius - inset),
                    max(0.0, self.radius - inset),
                )
                painter.fillPath(path, c)
        finally:
            painter.restore()

    # =====================================================
    # draw():
    #   0) vẽ shadow (outset: pixmap cache / inset: vẽ trực tiếp)
    #   1) vẽ gradient border
    #   2) clip inner
    #   3) drawSource (nội dung button)
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
                # OUTSET: dùng cache, nếu chưa có thì schedule rebuild
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

            # 3) Vẽ content gốc (QPushButton)
            self.drawSource(painter)

        finally:
            painter.restore()


# =============================================================================
# 3) BUTTON: NHẬN box-shadow STRING VÀ ÁP VÀO AnimEffect
# -----------------------------------------------------------------------------
# GradientBorderButton đóng vai trò API "thân thiện" kiểu QtMUI:
#   - init(text, box_shadow)
#   - setBoxShadow("box-shadow: ...")
# =============================================================================

class GradientBorderButton(QPushButton):
    def __init__(self, text: str, box_shadow: str):
        super().__init__(text)

        # Kích thước button demo
        self.setFixedSize(560, 56)

        # border-radius trong stylesheet phải khớp AnimEffect.radius
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

        # Gắn effect vào button
        self.effect = AnimEffect(self)
        self.setGraphicsEffect(self.effect)

        # Set shadow từ string
        self.setBoxShadow(box_shadow)

        # Animate gradient angle (chỉ để demo)
        self.anim_grad = QPropertyAnimation(self.effect, b"angle", self)
        self.anim_grad.setStartValue(0)
        self.anim_grad.setEndValue(360)
        self.anim_grad.setDuration(3000)
        self.anim_grad.setLoopCount(-1)
        self.anim_grad.setEasingCurve(QEasingCurve.Linear)
        self.anim_grad.start()

    def setBoxShadow(self, box_shadow: str):
        """
        Cho phép truyền cả dạng:
          "box-shadow: 20px 20px 50px 15px grey;"
        hoặc chỉ:
          "20px 20px 50px 15px grey"
        """
        v = (box_shadow or "").strip()
        if v.lower().startswith("box-shadow:"):
            v = v.split(":", 1)[1].strip()
        self.effect.setBoxShadow(v)


# =============================================================================
# 4) DEMO: ĐỦ CÁC VÍ DỤ THEO YÊU CẦU
# -----------------------------------------------------------------------------
# Bạn có thể thay danh sách examples để test thêm giá trị khác.
# =============================================================================

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtMUI – Box-shadow string examples (tài liệu trong code)")
        self.resize(1040, 860)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(26)
        layout.setContentsMargins(30, 30, 30, 30)

        examples = [
            "box-shadow: -10px 10px grey;",
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


# =============================================================================
# 5) ENTRY
# =============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec())
