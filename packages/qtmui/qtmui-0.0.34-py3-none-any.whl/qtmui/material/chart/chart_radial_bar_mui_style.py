"""
chart_radial_bar.py

Widget Radial Bar đa vòng (multi-ring) cho Qt (qtpy).
- Hỗ trợ gọi dạng: ChartRadialBar(series, labels, options, width, height, dir="ltr")
- Hover: highlight vòng và hiện tên + phần trăm ở tâm.
- Click/Legend toggle: ẩn/hiện giá trị (chỉ ẩn phần value, background ring vẫn hiển thị).
- Khi unhide sẽ animate từ 0 -> value (1s).
- Lấy màu từ useTheme() nếu có, fallback màu cố định nếu không.
- Có chú thích tiếng Việt chi tiết trong code.
"""

from typing import List, Optional, Dict, Any
from PySide6.QtCore import (
    Qt, QRectF, QPropertyAnimation, QEasingCurve, Property, Signal, QSize, QEvent
)
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QApplication, QFrame
)

# Nếu project có useTheme (PyMUI), dùng nó để lấy palette. Nếu không có, fallback.
try:
    from qtmui.material.styles import useTheme
    HAS_THEME = True
except Exception:
    HAS_THEME = False

def lighten_color(qcolor: QColor, factor: float = 1.3) -> QColor:
    """Trả về màu sáng hơn một chút (dùng cho highlight)."""
    h, s, v, a = qcolor.getHsvF()
    v = min(1.0, v * factor)
    return QColor.fromHsvF(h, s, v, a)

def darken_color(qcolor: QColor, factor: float = 0.7) -> QColor:
    """Trả về màu tối hơn một chút."""
    h, s, v, a = qcolor.getHsvF()
    v = max(0.0, v * factor)
    return QColor.fromHsvF(h, s, v, a)

class RadialSegment(QWidget):
    """
    Widget vẽ một vòng (ring) - gồm:
    - background full circle (mờ)
    - value arc (bắt đầu ở 12 o'clock, đi theo chiều kim đồng hồ)
    - phát hiện hover/click bằng signals
    Lưu ý: widget có bounding-box vuông; chúng ta dùng Z-order và raise_() để
    tránh vòng lớn che event của vòng nhỏ hơn.
    """
    hovered = Signal(int)
    unhovered = Signal(int)
    clicked = Signal(int)

    def __init__(self, index:int, name:str, value:float, base_value:float,
                 color:QColor, thickness:int, radius:int, parent=None):
        super().__init__(parent)
        # --- thông tin cơ bản ---
        self.index = index
        self.name = name
        self._value = float(value)        # giá trị thực của series
        self._base = float(base_value)    # base để tính percent (total hoặc max)
        self.color = QColor(color)
        # background ring (mờ)
        self.bg_color = QColor(self.color)
        self.bg_color.setAlpha(35)
        self.thickness = int(thickness)
        self.radius = int(radius)

        # cho phép nhận hover
        self.setAttribute(Qt.WA_Hover, True)
        self.setMouseTracking(True)

        # flag hiển thị arc value (toggleable)
        self.show_value = True

        # giá trị dùng cho animation (animatedValue)
        self._animated_value = 0.0
        self.anim = QPropertyAnimation(self, b"animatedValue")
        self.anim.setDuration(1000)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

        # kích thước widget tính theo radius + thickness tránh bị clipping
        outer = (self.radius + self.thickness/2)
        sz = int(outer*2 + 6)
        self.setMinimumSize(sz, sz)
        self.setMaximumSize(sz, sz)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # màu highlight khi hover
        self.highlight_color = lighten_color(self.color, 1.35)

    # property để animation có thể thao tác
    def getAnimatedValue(self):
        return self._animated_value

    def setAnimatedValue(self, v):
        self._animated_value = float(v)
        self.update()

    animatedValue = Property(float, getAnimatedValue, setAnimatedValue)

    # --- sự kiện chuột/hover ---
    def enterEvent(self, event):
        self.hovered.emit(self.index)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.unhovered.emit(self.index)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)
        super().mousePressEvent(event)

    # thay đổi giá trị (option animate)
    def setValue(self, v: float, animate: bool = False):
        self._value = float(v)
        if animate:
            self.anim.stop()
            self.anim.setStartValue(0.0)
            self.anim.setEndValue(self._value)
            self.anim.start()
        else:
            self._animated_value = self._value
            self.update()

    def paintEvent(self, event):
        """
        Vẽ background (full circle) và value arc (nếu show_value == True).
        Quy ước góc:
         - Qt: 0 deg ở 3 o'clock, + là CCW.
         - Muốn start ở 12 o'clock và đi theo chiều kim đồng hồ → start = 90*16, span negative.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)  # Thêm để khử răng cưa tốt hơn
        # painter.setRenderHint(QPainter.SmoothPixmapTransform)
        w = self.width(); h = self.height(); cx, cy = w/2, h/2

        # rect dùng để drawArc (dùng radius)
        rect = QRectF(cx - self.radius, cy - self.radius, self.radius*2, self.radius*2)

        # draw background full ring
        pen_bg = QPen(self.bg_color, self.thickness, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen_bg)
        painter.drawArc(rect, 0, 360*16)

        # draw value arc (tỉ lệ dựa trên _base)
        if self.show_value:
            val = getattr(self, "_animated_value", self._value)
            base = self._base if (self._base and self._base > 0) else 1.0
            val = max(0.0, min(val, base))
            start_angle = 90 * 16
            span_deg = -360.0 * (val / base)
            span_angle = int(span_deg * 16)
            pen_fg = QPen(self.color, self.thickness, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen_fg)
            painter.drawArc(rect, start_angle, span_angle)

        painter.end()

class ChartRadialBar(QFrame):
    """
    ChartRadialBar: widget chính
    Signature thay đổi để tương thích gọi kiểu:
      ChartRadialBar(series, labels, options=None, width=None, height=None, dir="ltr", type="radialBar")
    - series: List[float] (bắt buộc)
    - labels: List[str] (tùy chọn)
    - options: dict (thickness, gap, baseRadius, colors, usePercentOfTotal ...)
    - width/height: kích thước container (tùy chọn)
    """
    def __init__(self,
                 series: Optional[List[float]] = None,
                 options: Optional[Dict[str,Any]] = None,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 dir: str = "ltr",
                 type: str = "radialBar",
                 total: Optional[int] = None,
                 parent=None):
        super().__init__(parent)

        # --- map các tham số ---
        self._dir = dir
        self._type = type
        self._series = series or []
        self._options = options or {}
        self._width = width
        self._height = height

        # --- theme (nếu có) ---
        if HAS_THEME:
            self.theme = useTheme()
            self.mode = self.theme.palette.mode  # 'light' or 'dark' to decide lighten/darken
        else:
            self.theme = None
            self.mode = 'light'  # fallback

        # --- labels & colors ---
        self.labels = self._options.get("labels", [f"Series {i+1}" for i in range(len(self._series))])
        print("ChartRadialBar: labels =", self.labels)
        prov_colors = self._options.get("colors", None)
        if prov_colors:
            # nếu options truyền list màu strings
            self.colors = [QColor(c) for c in prov_colors]
        else:
            # cố gắng lấy từ theme, fallback màu mặc định
            if self.theme:
                pal = self.theme.palette
                try:
                    self.colors = [
                        QColor(pal.primary.main),
                        QColor(pal.warning.main),
                        QColor(pal.info.main),
                        QColor(pal.success.main),
                        QColor(pal.error.main),
                    ]
                except Exception:
                    self.colors = [QColor("#00A86B"), QColor("#FFC107"), QColor("#2196F3"), QColor("#9C27B0")]
            else:
                self.colors = [QColor("#00A86B"), QColor("#FFC107"), QColor("#2196F3"), QColor("#9C27B0")]

        # --- tuỳ chọn tính %: theo tổng (default) hoặc theo max ---
        self.use_percent_of_total = bool(self._options.get("usePercentOfTotal", True))

        # sizing params (cho phép override via options)
        thickness = int(self._options.get("thickness", 14))
        gap = int(self._options.get("gap", 6))
        base_radius = int(self._options.get("baseRadius", 50))

        # compute base values
        self.total_value = sum(self._series)
        self.max_value = max(self._series) if self._series else 1.0
        base_for_segments = self.total_value if self.use_percent_of_total else self.max_value

        # --- compute radii cho mỗi ring ---
        n = len(self._series)
        # ta muốn radii list: outer -> inner (outer lớn nhất)
        radii = []
        for i in range(n):
            r = base_radius + (n - 1 - i) * (thickness + gap)
            radii.append(r)
        max_radius = max(radii) if radii else base_radius
        outer_ext = max_radius + thickness/2
        container_size = int(outer_ext*2 + 8)

        # --- layout chính ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(4,4,4,4)
        self.main_layout.setSpacing(6)

        # rings_container: chứa tất cả RadialSegment (absolute positioning)
        self.rings_container = QWidget(self)
        # Nếu caller truyền width/height, dùng chúng; nhưng đảm bảo tối thiểu bằng container_size
        if self._width or self._height:
            w = self._width or container_size
            h = self._height or container_size
            self.rings_container.setFixedSize(max(w, container_size), max(h, container_size))
        else:
            self.rings_container.setFixedSize(container_size, container_size)

        # Cài event filter trên rings_container để bắt event chung
        self.rings_container.installEventFilter(self)
        self.rings_container.setMouseTracking(True)  # Bật mouse tracking để nhận hover

        # Center label (hiện Total hoặc tên+% khi hover)
        self.center_widget = QLabel("", self.rings_container)
        center_font = QFont(); center_font.setPointSize(14); center_font.setBold(True)
        self.center_widget.setFont(center_font)
        self.center_widget.setAlignment(Qt.AlignCenter)
        # kích thước box trung tâm (tỉ lệ so với container)
        cw = int(self.rings_container.width() * 0.6)
        ch = int(self.rings_container.height() * 0.25)
        self.center_widget.resize(cw, ch)
        self.center_widget.move((self.rings_container.width()-cw)//2,
                                (self.rings_container.height()-ch)//2 - 6)

        # --- tạo RadialSegment: tạo theo thứ tự OUTER -> INNER (radii list đã tính)
        self.rings: List[RadialSegment] = []
        for i in range(n):
            radius = radii[i]
            value = self._series[i]
            color = self.colors[i % len(self.colors)]
            # tạo segment (là child của rings_container)
            seg = RadialSegment(i, self.labels[i] if i < len(self.labels) else f"Series {i+1}",
                                value, base_for_segments, color, thickness, radius, parent=self.rings_container)
            # đặt chính giữa
            seg.move((self.rings_container.width() - seg.width()) // 2,
                     (self.rings_container.height() - seg.height()) // 2)
            seg.setValue(value, animate=False)
            # connect signals
            seg.hovered.connect(self._on_segment_hovered)
            seg.unhovered.connect(self._on_segment_unhovered)
            seg.clicked.connect(self._on_segment_clicked)
            seg.show()
            self.rings.append(seg)

        # --- Đảm bảo Z-order: ring nhỏ nhất (radius nhỏ) nằm trên cùng ---
        ordered = sorted(self.rings, key=lambda s: s.radius)
        for s in ordered:
            s.raise_()

        # Sau khi raise tất cả rings, ta phải đặt center_widget luôn ở trên cùng
        # để không bị che bởi các ring (đây là nguyên nhân 'Total' bị che một phần).
        self.center_widget.raise_()

        # --- legend / toggles dưới cùng ---
        self.legend_widget = QWidget(self)
        self.legend_layout = QHBoxLayout(self.legend_widget)
        self.legend_layout.setContentsMargins(0,0,0,0)
        self.legend_layout.setSpacing(8)
        self.toggle_buttons = []
        for i, label in enumerate(self.labels):
            print("Creating toggle button for legend:", label)
            b = QPushButton(label)
            b.setCheckable(True)
            b.setChecked(True)
            color = self.colors[i % len(self.colors)].name()
            # style đơn giản: khi checked hiển marker màu
            b.setStyleSheet(
                f"QPushButton{{border:none;padding:6px;border-radius:8px}}"
                f"QPushButton::checked{{background:{color}33}}"
            )
            b.clicked.connect(lambda checked, idx=i: self._on_toggle(idx, checked))
            self.legend_layout.addWidget(b)
            self.toggle_buttons.append(b)

        # hiển thị total ban đầu
        self._show_total()

        # thêm widget vào layout chính
        self.main_layout.addWidget(self.rings_container, alignment=Qt.AlignHCenter)
        self.main_layout.addWidget(self.legend_widget, alignment=Qt.AlignHCenter)

        # set minimal size cho ChartRadialBar (tránh bị window resize quá nhỏ)
        # self.setMinimumSize(self.rings_container.width() + 8, self.rings_container.height() + 40)

    # def sizeHint(self) -> QSize:
    #     """Gợi ý kích thước cho parent/layout manager."""
    #     w = max(200, self.rings_container.width() + 8)
    #     h = max(200, self.rings_container.height() + 40)
    #     return QSize(w, h)

    # --- handlers ---
    def _on_segment_hovered(self, idx:int):
        """Khi hover 1 segment: đổi màu tạm thời, hiển thị tên + percent ở center."""
        if idx < 0 or idx >= len(self.rings): return
        seg = self.rings[idx]
        # Highlight màu tùy mode
        if self.mode == 'light':
            seg.color = lighten_color(self.colors[idx % len(self.colors)])
        else:
            seg.color = darken_color(self.colors[idx % len(self.colors)])
        # base tính percent theo tuỳ chọn
        if self.use_percent_of_total:
            base = self.total_value if self.total_value > 0 else 1.0
        else:
            base = self.max_value if self.max_value > 0 else 1.0
        percent = seg._value / base * 100
        # Hiển thị "Name\nXX%"
        self.center_widget.setText(f"{seg.name}\n{percent:.0f}%")
        self.center_widget.setAlignment(Qt.AlignCenter)
        seg.update()

    def _on_segment_unhovered(self, idx:int):
        """Khi rời hover: reset màu và hiện lại total."""
        if idx < 0 or idx >= len(self.rings): return
        seg = self.rings[idx]
        seg.color = self.colors[idx % len(self.colors)]
        self._show_total()
        seg.update()

    def _on_segment_clicked(self, idx:int):
        """Click tương tự toggle legend: invert state."""
        if idx < 0 or idx >= len(self.toggle_buttons): return
        btn = self.toggle_buttons[idx]
        btn.setChecked(not btn.isChecked())
        self._on_toggle(idx, btn.isChecked())

    def _on_toggle(self, idx:int, checked:bool):
        """Ẩn/hiện phần value (chỉ ẩn arc value, background vẫn hiển thị)."""
        if idx < 0 or idx >= len(self.rings): return
        seg = self.rings[idx]
        seg.show_value = checked
        if checked:
            seg.setValue(seg._value, animate=True)
        else:
            seg.anim.stop()
            seg._animated_value = 0.0
            seg.update()

        # Cập nhật center: nếu all checked = False, show total; nếu not, show % of last toggled (or total)
        all_off = all(not b.isChecked() for b in self.toggle_buttons)
        if all_off:
            self._show_total()
        else:
            # Show % of this toggled ring
            base = self.total_value if self.use_percent_of_total else self.max_value
            percent = seg._value / base * 100 if base > 0 else 0
            self.center_widget.setText(f"{seg.name}\n{percent:.0f}%")

    def _show_total(self):
        """Hiển thị tổng ở center."""
        self.center_widget.setText("Total\n" + f"{self.total_value:,}")
        self.center_widget.setAlignment(Qt.AlignCenter)

    # --- Event Filter trên rings_container ---
    def eventFilter(self, obj, event):
        if obj == self.rings_container:
            if event.type() == QEvent.MouseMove:
                # Tính khoảng cách từ center đến chuột
                cx, cy = self.rings_container.width() / 2, self.rings_container.height() / 2
                mx, my = event.pos().x(), event.pos().y()
                dist = ((mx - cx)**2 + (my - cy)**2)**0.5

                # Kiểm tra từ ngoài vào trong (outer ring đầu tiên)
                hit = False
                for seg in sorted(self.rings, key=lambda s: -s.radius):  # lớn đến nhỏ
                    inner = seg.radius - seg.thickness / 2
                    outer = seg.radius + seg.thickness / 2
                    if inner < dist < outer:
                        self._on_segment_hovered(seg.index)
                        hit = True
                        break
                if not hit:
                    self._on_segment_unhovered(-1)
                return True
            elif event.type() == QEvent.Leave:
                self._on_segment_unhovered(-1)
                return True
            elif event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    # Tương tự mouse move, tính dist và tìm ring
                    cx, cy = self.rings_container.width() / 2, self.rings_container.height() / 2
                    mx, my = event.pos().x(), event.pos().y()
                    dist = ((mx - cx)**2 + (my - cy)**2)**0.5
                    hit = False
                    for seg in sorted(self.rings, key=lambda s: -s.radius):
                        inner = seg.radius - seg.thickness / 2
                        outer = seg.radius + seg.thickness / 2
                        if inner < dist < outer:
                            self._on_segment_clicked(seg.index)
                            hit = True
                            break
                    if hit:
                        return True
        return super().eventFilter(obj, event)

# # Demo đơn giản: chạy file như script để hiển thị widget
# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)

#     # Lưu ý: gọi theo thứ tự: series, labels, options (nếu cần)
#     data = [20, 24, 20, 35, 12]
#     labels = ["Apples", "Oranges", "Bananas", "Grapes", "Pears"]
#     # Ví dụ options: đổi baseRadius/thickness/gap hoặc colors
#     options = {
#         "baseRadius": 60,
#         "thickness": 16,
#         "gap": 8,
#         "usePercentOfTotal": True,
#         # "colors": ["#00A86B", "#FFC107"]
#     }

#     # Tạo widget - chú ý signature giống demo của bạn
#     w = ChartRadialBar(data, labels, options, width=100, height=100)
#     w.setWindowTitle("ChartRadialBar Demo")
#     w.show()

#     sys.exit(app.exec_())