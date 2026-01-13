import re
import sys
from typing import Any, Dict, Optional, Callable, Tuple

from PySide6 import QtAsyncio

from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import QSize, Qt, QTimer, QRectF, QPointF
from PySide6.QtGui import (
    QPainter, QColor, QPen, QPixmap,
    QBrush, QLinearGradient, QPainterPath
)

from qtmui.material.qtmui_app import QtMuiApp
from qtmui.material.window import QtMuiWindow
from qtmui.material.button import Button

from flow_layout import FlowLayout


# =============================================================================
# Helper: StyleDecorator (border + radius + background + cache pixmap)
# =============================================================================

class StyleDecorator:
    """
    Helper xử lý style dạng sx cho QWidget:
      - Parse sx 1 lần (tránh parse/alloc trong paintEvent)
      - Render ra pixmap cache theo (size, dpr, styleKey)
      - Paint: chỉ drawPixmap (nhẹ)

    Hỗ trợ:
      - border (4 cạnh khác nhau hoặc đồng nhất)
      - border-radius (uniform hoặc theo từng góc)
      - background: color / linear-gradient(...)
    """

    def __init__(self, owner: QFrame, sx: Optional[Dict[str, Any]] = None):
        self._owner = owner
        self._sx: Dict[str, Any] = sx or {}

        self._border_spec: Dict[str, Dict[str, Any]] = {}
        self._radius_spec: Dict[str, float] = {}
        self._bg_spec: Dict[str, Any] = {}

        self._cache_size: Optional[Tuple[int, int]] = None
        self._cache_dpr: Optional[float] = None
        self._cache_key: Optional[str] = None
        self._pixmap: Optional[QPixmap] = None

        self.set_sx(self._sx)

    # ------------------------- Public API -------------------------

    def set_sx(self, sx: Dict[str, Any]):
        self._sx = sx or {}
        self._border_spec = self._parse_border_sx(self._sx)
        self._radius_spec = self._parse_radius_sx(self._sx)
        self._bg_spec = self._parse_background_sx(self._sx)
        self.invalidate_cache()

    def invalidate_cache(self):
        self._cache_size = None
        self._cache_dpr = None
        self._cache_key = None
        self._pixmap = None

    def paint(self, painter: QPainter, rect_size: QSize, dpr: float):
        pm = self._get_pixmap(rect_size, dpr)
        if pm is None or pm.isNull():
            return
        painter.drawPixmap(0, 0, pm)

    # ------------------------- Enum helpers (PySide6-safe) -------------------------

    def _enum_to_int(self, v) -> int:
        try:
            if isinstance(v, int):
                return v
            if hasattr(v, "value"):
                return int(v.value)
            return int(v)
        except Exception:
            return 0

    # ------------------------- Parsing utils -------------------------

    def _parse_px(self, s: str) -> float:
        if not isinstance(s, str):
            return 0.0
        m = re.search(r"(-?\d+(?:\.\d+)?)\s*px", s.strip(), re.I)
        if not m:
            m = re.search(r"(-?\d+(?:\.\d+)?)", s.strip())
        if not m:
            return 0.0
        try:
            return max(0.0, float(m.group(1)))
        except Exception:
            return 0.0

    def _parse_color(self, v: Any) -> QColor:
        if v is None:
            return QColor(0, 0, 0, 0)
        if isinstance(v, QColor):
            return v
        if isinstance(v, (tuple, list)) and len(v) in (3, 4):
            r, g, b = int(v[0]), int(v[1]), int(v[2])
            a = int(v[3]) if len(v) == 4 else 255
            return QColor(r, g, b, max(0, min(255, a)))

        if not isinstance(v, str):
            return QColor(0, 0, 0, 0)

        s = v.strip()

        m = re.search(
            r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([0-9.]+)\s*)?\)",
            s, re.I
        )
        if m:
            r = int(m.group(1))
            g = int(m.group(2))
            b = int(m.group(3))
            a_raw = m.group(4)
            if a_raw is None:
                a = 255
            else:
                a_f = float(a_raw)
                a = int(round(a_f * 255)) if a_f <= 1.0 else int(round(a_f))
                a = max(0, min(255, a))
            return QColor(r, g, b, a)

        if s.startswith("#"):
            c = QColor(s)
            if c.isValid():
                return c

        c = QColor(s)
        if c.isValid():
            return c

        return QColor(0, 0, 0, 0)

    def _parse_pen_style_int(self, s: str) -> int:
        ss = (s or "").lower()
        if "dashed" in ss:
            return self._enum_to_int(Qt.PenStyle.DashLine)
        if "dotted" in ss:
            return self._enum_to_int(Qt.PenStyle.DotLine)
        return self._enum_to_int(Qt.PenStyle.SolidLine)

    # ------------------------- Border parsing -------------------------

    def _parse_border_value(self, v: Any) -> Dict[str, Any]:
        """
        Output: {"w": int, "color": QColor, "style": int(enum_value)}
        """
        solid_i = self._enum_to_int(Qt.PenStyle.SolidLine)

        if v is None:
            return {"w": 0, "color": QColor(0, 0, 0, 0), "style": solid_i}

        if isinstance(v, (int, float)):
            w = max(0, int(round(v)))
            return {"w": w, "color": QColor(0, 0, 0, 255), "style": solid_i}

        if not isinstance(v, str):
            return {"w": 0, "color": QColor(0, 0, 0, 0), "style": solid_i}

        s = v.strip()
        w = int(round(self._parse_px(s)))
        style_i = self._parse_pen_style_int(s)

        m_rgba = re.search(r"rgba?\([^)]+\)", s, re.I)
        if m_rgba:
            color = self._parse_color(m_rgba.group(0))
        else:
            m_hex = re.search(r"(#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{8}))", s)
            if m_hex:
                color = self._parse_color(m_hex.group(1))
            else:
                color = QColor(0, 0, 0, 255)

        return {"w": w, "color": color, "style": style_i}

    def _parse_border_sx(self, sx: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        base = self._parse_border_value(sx.get("border") or sx.get("borderWidth") or sx.get("border-width"))

        def pick(*keys):
            for k in keys:
                if k in sx and sx[k] is not None:
                    return sx[k]
            return None

        left_v = pick("borderLeft", "border-left", "borderLeftWidth", "border-left-width")
        right_v = pick("borderRight", "border-right", "borderRightWidth", "border-right-width")
        top_v = pick("borderTop", "border-top", "borderTopWidth", "border-top-width")
        bottom_v = pick("borderBottom", "border-bottom", "borderBottomWidth", "border-bottom-width")

        left = self._parse_border_value(left_v) if left_v is not None else base
        right = self._parse_border_value(right_v) if right_v is not None else base
        top = self._parse_border_value(top_v) if top_v is not None else base
        bottom = self._parse_border_value(bottom_v) if bottom_v is not None else base

        return {"left": left, "right": right, "top": top, "bottom": bottom}

    # ------------------------- Radius parsing -------------------------

    def _parse_radius_sx(self, sx: Dict[str, Any]) -> Dict[str, float]:
        base = sx.get("borderRadius", sx.get("border-radius", 0))
        base_r = float(base) if isinstance(base, (int, float)) else float(self._parse_px(str(base)))
        base_r = max(0.0, base_r)

        def pick_radius(*keys) -> float:
            for k in keys:
                if k in sx and sx[k] is not None:
                    v = sx[k]
                    if isinstance(v, (int, float)):
                        return max(0.0, float(v))
                    return max(0.0, float(self._parse_px(str(v))))
            return base_r

        tl = pick_radius("borderTopLeftRadius", "border-top-left-radius")
        tr = pick_radius("borderTopRightRadius", "border-top-right-radius")
        br = pick_radius("borderBottomRightRadius", "border-bottom-right-radius")
        bl = pick_radius("borderBottomLeftRadius", "border-bottom-left-radius")

        return {"tl": tl, "tr": tr, "br": br, "bl": bl}

    # ------------------------- Background parsing -------------------------

    def _parse_linear_gradient(self, s: str) -> Optional[Dict[str, Any]]:
        s = s.strip()
        if not s.lower().startswith("linear-gradient(") or not s.endswith(")"):
            return None

        inner = s[len("linear-gradient("):-1].strip()
        parts = [p.strip() for p in inner.split(",") if p.strip()]
        if len(parts) < 2:
            return None

        direction = "to bottom"
        colors = parts

        first = parts[0].lower()
        if first.startswith("to ") or first.endswith("deg"):
            direction = parts[0]
            colors = parts[1:]

        if len(colors) < 2:
            return None

        c1 = self._parse_color(colors[0])
        c2 = self._parse_color(colors[1])

        return {"type": "linear-gradient", "dir": direction, "c1": c1, "c2": c2}

    def _parse_background_sx(self, sx: Dict[str, Any]) -> Dict[str, Any]:
        v = sx.get("background", None)
        if v is None:
            v = sx.get("backgroundColor", sx.get("background-color", None))

        if v is None:
            return {"type": "none"}

        if isinstance(v, str):
            grad = self._parse_linear_gradient(v)
            if grad:
                return grad

        return {"type": "color", "color": self._parse_color(v)}

    # ------------------------- Cache key -------------------------

    def _style_key(self) -> str:
        b = self._border_spec
        r = self._radius_spec
        bg = self._bg_spec

        def border_one(side: str) -> str:
            s = b.get(side, {})
            c: QColor = s.get("color", QColor(0, 0, 0, 0))
            style_i = self._enum_to_int(s.get("style", self._enum_to_int(Qt.PenStyle.SolidLine)))
            return f"{side}:{int(s.get('w', 0) or 0)}:{style_i}:{c.rgba()}"

        b_key = "|".join([border_one("left"), border_one("top"), border_one("right"), border_one("bottom")])
        r_key = f"r:{r.get('tl',0):.2f},{r.get('tr',0):.2f},{r.get('br',0):.2f},{r.get('bl',0):.2f}"

        if bg.get("type") == "none":
            bg_key = "bg:none"
        elif bg.get("type") == "color":
            c: QColor = bg.get("color", QColor(0, 0, 0, 0))
            bg_key = f"bg:color:{c.rgba()}"
        else:
            c1: QColor = bg.get("c1", QColor(0, 0, 0, 0))
            c2: QColor = bg.get("c2", QColor(0, 0, 0, 0))
            bg_key = f"bg:grad:{bg.get('dir','')}:{c1.rgba()}:{c2.rgba()}"

        return f"{b_key}||{r_key}||{bg_key}"

    # ------------------------- Pixmap render -------------------------

    def _get_pixmap(self, size: QSize, dpr: float) -> Optional[QPixmap]:
        w = max(0, int(size.width()))
        h = max(0, int(size.height()))
        if w <= 0 or h <= 0:
            return None

        key = self._style_key()

        if (
            self._pixmap is not None
            and self._cache_size == (w, h)
            and self._cache_dpr == dpr
            and self._cache_key == key
        ):
            return self._pixmap

        pm = QPixmap(int(w * dpr), int(h * dpr))
        pm.setDevicePixelRatio(dpr)
        pm.fill(Qt.GlobalColor.transparent)

        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        self._render(p, float(w), float(h))

        p.end()

        self._pixmap = pm
        self._cache_size = (w, h)
        self._cache_dpr = dpr
        self._cache_key = key
        return pm

    def _render(self, p: QPainter, w: float, h: float):
        self._render_background(p, w, h)
        self._render_border(p, w, h)

    def _rounded_path(self, rect: QRectF, r: Dict[str, float]) -> QPainterPath:
        tl = float(r.get("tl", 0.0))
        tr = float(r.get("tr", 0.0))
        br = float(r.get("br", 0.0))
        bl = float(r.get("bl", 0.0))

        max_rx = rect.width() / 2.0
        max_ry = rect.height() / 2.0
        tl = min(tl, max_rx, max_ry)
        tr = min(tr, max_rx, max_ry)
        br = min(br, max_rx, max_ry)
        bl = min(bl, max_rx, max_ry)

        x, y, rw, rh = rect.x(), rect.y(), rect.width(), rect.height()
        path = QPainterPath()

        path.moveTo(x + tl, y)
        path.lineTo(x + rw - tr, y)
        if tr > 0:
            path.quadTo(x + rw, y, x + rw, y + tr)
        else:
            path.lineTo(x + rw, y)

        path.lineTo(x + rw, y + rh - br)
        if br > 0:
            path.quadTo(x + rw, y + rh, x + rw - br, y + rh)
        else:
            path.lineTo(x + rw, y + rh)

        path.lineTo(x + bl, y + rh)
        if bl > 0:
            path.quadTo(x, y + rh, x, y + rh - bl)
        else:
            path.lineTo(x, y + rh)

        path.lineTo(x, y + tl)
        if tl > 0:
            path.quadTo(x, y, x + tl, y)
        else:
            path.lineTo(x, y)

        path.closeSubpath()
        return path

    def _render_background(self, p: QPainter, w: float, h: float):
        bg = self._bg_spec
        if bg.get("type") == "none":
            return

        rect = QRectF(0.0, 0.0, w, h)
        r = self._radius_spec
        has_radius = any((r.get("tl", 0), r.get("tr", 0), r.get("br", 0), r.get("bl", 0)))

        if has_radius:
            path = self._rounded_path(rect, r)
            p.save()
            p.setClipPath(path)

        if bg.get("type") == "color":
            c: QColor = bg.get("color", QColor(0, 0, 0, 0))
            p.fillRect(rect, QBrush(c))
        elif bg.get("type") == "linear-gradient":
            grad = self._build_linear_gradient(w, h, bg.get("dir", "to bottom"), bg.get("c1"), bg.get("c2"))
            p.fillRect(rect, QBrush(grad))

        if has_radius:
            p.restore()

    def _build_linear_gradient(self, w: float, h: float, direction: str, c1: QColor, c2: QColor) -> QLinearGradient:
        direction = (direction or "").strip().lower()
        c1 = c1 if isinstance(c1, QColor) else QColor(0, 0, 0, 0)
        c2 = c2 if isinstance(c2, QColor) else QColor(0, 0, 0, 0)

        x1, y1, x2, y2 = 0.0, 0.0, 0.0, h

        if direction.startswith("to "):
            if "right" in direction:
                x1, y1, x2, y2 = 0.0, 0.0, w, 0.0
            elif "left" in direction:
                x1, y1, x2, y2 = w, 0.0, 0.0, 0.0
            elif "top" in direction:
                x1, y1, x2, y2 = 0.0, h, 0.0, 0.0
            else:
                x1, y1, x2, y2 = 0.0, 0.0, 0.0, h
        elif direction.endswith("deg"):
            try:
                import math
                deg = float(direction.replace("deg", "").strip())
                rad = math.radians(deg)
                vx = math.sin(rad)
                vy = -math.cos(rad)
                cx, cy = w / 2.0, h / 2.0
                half = max(w, h) / 2.0
                x1, y1 = cx - vx * half, cy - vy * half
                x2, y2 = cx + vx * half, cy + vy * half
            except Exception:
                x1, y1, x2, y2 = 0.0, 0.0, 0.0, h

        g = QLinearGradient(QPointF(x1, y1), QPointF(x2, y2))
        g.setColorAt(0.0, c1)
        g.setColorAt(1.0, c2)
        return g

    def _border_is_uniform(self) -> bool:
        s = self._border_spec
        a = s["left"]
        for k in ("top", "right", "bottom"):
            b = s[k]
            if int(a.get("w", 0) or 0) != int(b.get("w", 0) or 0):
                return False
            if int(a.get("style", 0) or 0) != int(b.get("style", 0) or 0):
                return False
            ca: QColor = a.get("color", QColor(0, 0, 0, 0))
            cb: QColor = b.get("color", QColor(0, 0, 0, 0))
            if ca.rgba() != cb.rgba():
                return False
        return int(a.get("w", 0) or 0) > 0

    def _render_border(self, p: QPainter, w: float, h: float):
        s = self._border_spec
        lw = int(s["left"].get("w", 0) or 0)
        rw = int(s["right"].get("w", 0) or 0)
        tw = int(s["top"].get("w", 0) or 0)
        bw = int(s["bottom"].get("w", 0) or 0)

        if (lw + rw + tw + bw) <= 0:
            return

        if self._border_is_uniform():
            self._render_uniform_border(p, w, h)
            return

        x_left = lw / 2.0 if lw > 0 else 0.0
        x_right = (w - rw / 2.0) if rw > 0 else w
        y_top = tw / 2.0 if tw > 0 else 0.0
        y_bottom = (h - bw / 2.0) if bw > 0 else h

        def set_pen(side_spec: Dict[str, Any]):
            bw_ = int(side_spec.get("w", 0) or 0)
            col: QColor = side_spec.get("color", QColor(0, 0, 0, 255))
            style_i = int(side_spec.get("style", self._enum_to_int(Qt.PenStyle.SolidLine)) or 0)
            pen = QPen(col, bw_, Qt.PenStyle(style_i))
            pen.setCapStyle(Qt.PenCapStyle.SquareCap)
            p.setPen(pen)

        if tw > 0:
            set_pen(s["top"])
            p.drawLine(QPointF(x_left, y_top), QPointF(x_right, y_top))
        if bw > 0:
            set_pen(s["bottom"])
            p.drawLine(QPointF(x_left, y_bottom), QPointF(x_right, y_bottom))
        if lw > 0:
            set_pen(s["left"])
            p.drawLine(QPointF(x_left, y_top), QPointF(x_left, y_bottom))
        if rw > 0:
            set_pen(s["right"])
            p.drawLine(QPointF(x_right, y_top), QPointF(x_right, y_bottom))

    def _render_uniform_border(self, p: QPainter, w: float, h: float):
        s = self._border_spec["left"]
        bw = int(s.get("w", 0) or 0)
        if bw <= 0:
            return

        col: QColor = s.get("color", QColor(0, 0, 0, 255))
        style_i = int(s.get("style", self._enum_to_int(Qt.PenStyle.SolidLine)) or 0)
        pen = QPen(col, bw, Qt.PenStyle(style_i))
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)

        inset = bw / 2.0
        rect = QRectF(inset, inset, max(0.0, w - 2 * inset), max(0.0, h - 2 * inset))

        r = self._radius_spec
        has_radius = any((r.get("tl", 0), r.get("tr", 0), r.get("br", 0), r.get("bl", 0)))
        if not has_radius:
            p.drawRect(rect)
            return

        rr = {
            "tl": max(0.0, r.get("tl", 0.0) - inset),
            "tr": max(0.0, r.get("tr", 0.0) - inset),
            "br": max(0.0, r.get("br", 0.0) - inset),
            "bl": max(0.0, r.get("bl", 0.0) - inset),
        }
        path = self._rounded_path(rect, rr)
        p.drawPath(path)


# =============================================================================
# Demo widgets
# =============================================================================

class Item(QFrame):
    def __init__(self, width=100, height=20, color="red"):
        super().__init__()
        self.setObjectName(str(id(self)))
        self.setFixedSize(QSize(width, height))
        self.setStyleSheet(f"#{self.objectName()} {{background: rgba(0,0,0,50);}}")


class Box(QFrame):
    def __init__(self, children=None):
        super().__init__()
        self.setObjectName(str(id(self)))
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        for widget in children:
            self.layout().addWidget(widget)


class FlexBoxWrap(QFrame):
    def __init__(
        self,
        name="FlexBoxWrap",
        children=None,
        flexWrap=True,
        align="left",
        color="blue",
        onLayout: Optional[Callable[[Dict[str, Any]], None]] = None,
        sx: dict = None
    ):
        super().__init__()
        self.setObjectName(str(id(self)))

        self._sx: Dict[str, Any] = sx or {"border": "1px solid rgba(0,0,0,100)"}
        self._decor = StyleDecorator(self, self._sx)

        # Không dùng stylesheet border để tránh Qt shrink contentsRect
        self.setLayout(
            FlowLayout(
                name=name,
                parent=self,
                children=children,
                alignItems="center",
                justifyContent="flex-start",
                sx={},
            )
        )

        self._repaint_scheduled = False

    def setSx(self, sx: Dict[str, Any]):
        self._sx = sx or {}
        self._decor.set_sx(self._sx)
        self._schedule_repaint()

    def _schedule_repaint(self):
        if self._repaint_scheduled:
            return
        self._repaint_scheduled = True

        def _go():
            self._repaint_scheduled = False
            self.update()

        QTimer.singleShot(0, _go)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._decor.invalidate_cache()
        self._schedule_repaint()

    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        self._decor.paint(p, self.size(), self.devicePixelRatioF())
        p.end()


class MainWindow(QtMuiWindow):
    def __init__(self):
        super().__init__()
        self.resize(300, 300)

        def _setMainWindowSize():
            self.resize(230, 300)

        self.setCentralWidget(
            Box(
                children=[
                    Button(text="230px", variant="contained", onClick=lambda: _setMainWindowSize()),
                    FlexBoxWrap(
                        name="FBW",
                        sx={
                            "border": "1px solid rgba(0,0,0,100)",
                            "borderRadius": "10px",
                            "background": "linear-gradient(to right, rgba(0,0,0,30), rgba(0,0,0,5))",
                        },
                        children=[
                            FlexBoxWrap(
                                name="FBW-1",
                                sx={
                                    "border": "1px solid rgba(0,0,0,100)",
                                    "borderRadius": "10px",
                                    "backgroundColor": "rgba(0,0,0,10)",
                                },
                                children=[Item(), Item()],
                            ),
                            Item(),
                        ],
                    ),
                ]
            )
        )


if __name__ == "__main__":
    app = QtMuiApp(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
