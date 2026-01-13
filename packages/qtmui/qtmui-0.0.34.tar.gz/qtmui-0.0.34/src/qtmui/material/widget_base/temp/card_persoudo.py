#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CardHost đóng gói QGraphicsView/QGraphicsScene bên trong chính nó.

Yêu cầu đã đáp ứng:
- PseudoFrame nhận stylesheet (QSS) thật sự.
- paintEvent của PseudoFrame chỉ làm 1 nhiệm vụ: XOAY (rotate) rồi vẽ theo QSS (không vẽ thêm shape).
- Kích thước pseudo do PseudoFrame tự xử lý (tính từ sx + content size).

Cách vẽ QSS khi override paintEvent:
- Không thể gọi super().paintEvent() sau khi rotate vì super dùng painter nội bộ.
- Giải pháp chuẩn: dùng QStyleOption + style().drawPrimitive(QStyle.PE_Widget, ...)
  => vẽ nền/border theo stylesheet vào painter hiện tại (đã rotate).
"""

import sys
import re
from typing import Any, Dict, List, Tuple, Optional

from PySide6.QtCore import Qt, QRectF, QPointF, QTimer, Property, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFrame,
    QVBoxLayout,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsProxyWidget,
    QStyle,
    QStyleOption,
    QGraphicsEffect,
)


# ============================================================
# Helpers parse kiểu CSS đơn giản
# ============================================================

_len_re = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*(px|%)?\s*$", re.IGNORECASE)

def parse_len(v: Any) -> Tuple[str, float]:
    """Trả về (unit, value) unit ∈ {'px','%'}"""
    if v is None:
        return ("px", 0.0)
    if isinstance(v, (int, float)):
        return ("px", float(v))
    s = str(v).strip()
    m = _len_re.match(s)
    if not m:
        return ("px", 0.0)
    num = float(m.group(1))
    unit = (m.group(2) or "px").lower()
    if unit not in ("px", "%"):
        unit = "px"
    return (unit, num)

def len_to_px(lenv: Tuple[str, float], basis: float) -> float:
    unit, val = lenv
    return basis * val / 100.0 if unit == "%" else val

def parse_translate(v: Any) -> Tuple[Tuple[str, float], Tuple[str, float]]:
    if not v:
        return (("px", 0.0), ("px", 0.0))
    parts = str(v).strip().split()
    if len(parts) == 1:
        parts = [parts[0], "0"]
    return (parse_len(parts[0]), parse_len(parts[1]))

def px_int(v: Any, default: int = 0) -> int:
    unit, val = parse_len(v)
    if unit == "%":
        return default
    return int(round(val))

def easing_from_name(name: Any) -> QEasingCurve:
    s = str(name or "linear").strip().lower()
    if s == "linear":
        return QEasingCurve.Linear
    if s in ("inoutquad", "in_out_quad", "easeinout"):
        return QEasingCurve.InOutQuad
    if s in ("outquad", "easeout"):
        return QEasingCurve.OutQuad
    if s in ("inquad", "easein"):
        return QEasingCurve.InQuad
    return QEasingCurve.Linear

def direction_from_name(name: Any) -> QPropertyAnimation.Direction:
    s = str(name or "forward").strip().lower()
    if s in ("backward", "reverse", "backwards"):
        return QPropertyAnimation.Backward
    return QPropertyAnimation.Forward

def loop_from_value(v: Any) -> int:
    if v is None:
        return -1
    if isinstance(v, str) and v.strip().lower() == "infinite":
        return -1
    try:
        return int(v)
    except Exception:
        return -1


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
        self.border = 2

    def boundingRectFor(self, rect: QRectF) -> QRectF:
        b = self.border
        return rect.adjusted(-b, -b, b, b)

    def getAngle(self):
        return self._angle

    def setAngle(self, v):
        self._angle = v
        self.update()

    angle = Property(float, getAngle, setAngle)

    def draw(self, painter: QPainter):
        src_rect = self.sourceBoundingRect()

        painter.setRenderHint(QPainter.Antialiasing)

        c = src_rect.center()
        painter.translate(c)
        painter.rotate(self._angle)
        painter.translate(-c)


        # content
        self.drawSource(painter)

# ============================================================
# PseudoFrame: QWidget thật, nhận QSS, paintEvent chỉ rotate + draw QSS
# ============================================================

class PseudoFrame(QFrame):
    """
    - Nhận QSS bình thường (background-color, border-radius, border, ...)
    - paintEvent chỉ xoay painter, sau đó vẽ widget theo QSS bằng QStyle (PE_Widget)
    - Kích thước tự tính từ sx + content size qua sync_to_content()
    """

    def __init__(self, sx: Dict[str, Any], kind: str):
        super().__init__()
        self.sx = sx
        self.kind = kind

        # Góc xoay
        self._angle = 0.0

        # Để stylesheet có hiệu lực nền trên QWidget khi tự paint
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        # Lấy radius/padding để tính geometry (không dùng để vẽ)
        self._pad = px_int(sx.get("padding", "0px"), 0)

        # Áp stylesheet từ sx:
        bg = sx.get("background-color") or sx.get("background") or "pink"
        br = px_int(sx.get("border-radius", "0px"), 0)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        self.contentFrame = QFrame()
        self.contentFrame.setObjectName("contentFrame")
        self.layout().addWidget(self.contentFrame)

        self.setStyleSheet(
            "PseudoFrame { "
            f"background-color: transparent; "
            "}"
            "QFrame#contentFrame { "
            f"border-radius: {br}px; "
            f"background-color: {bg}; "
            f"border: 1px solid red; "
            "}"
        )

        # Animation angle nếu có
        self._anim: Optional[QPropertyAnimation] = None

        self._effect = AnimEffect(self)
        self.setGraphicsEffect(self._effect)

        self._setup_angle_animation()



    def _setup_angle_animation(self):
        anim = self.sx.get("animation")
        if not isinstance(anim, dict):
            return
        if str(anim.get("propertyName", "")).strip().lower() != "angle":
            return

        # ==============================
        # FIX DUY NHẤT:
        # Animate trực tiếp AnimEffect.angle thay vì PseudoFrame.angle
        # Vì xoay đang diễn ra ở AnimEffect.draw() dùng self._angle của effect.
        # ==============================
        self._anim = QPropertyAnimation(self._effect, b"angle", self)

        self._anim.setStartValue(float(anim.get("from", 0)))
        self._anim.setEndValue(float(anim.get("to", 360)))
        self._anim.setDuration(int(anim.get("duration", 10000)))
        self._anim.setLoopCount(loop_from_value(anim.get("loop", "infinite")))
        self._anim.setEasingCurve(easing_from_name(anim.get("easingCurve", "linear")))
        self._anim.setDirection(direction_from_name(anim.get("direction", "forward")))
        self._anim.start()

    # ---- geometry: pseudo tự tính ----
    def compute_rect_in_content(self, content_w: float, content_h: float) -> QRectF:
        w = len_to_px(parse_len(self.sx.get("width", "100%")), content_w)
        h = len_to_px(parse_len(self.sx.get("height", "100%")), content_h)

        left = len_to_px(parse_len(self.sx.get("left", "0px")), content_w)
        top = len_to_px(parse_len(self.sx.get("top", "0px")), content_h)

        tx_len, ty_len = parse_translate(self.sx.get("translate", "0px 0px"))
        tx = len_to_px(tx_len, w)
        ty = len_to_px(ty_len, h)

        pad = float(self._pad)

        x = left + tx - pad
        y = top + ty - pad
        return QRectF(x, y, w + 2 * pad, h + 2 * pad)

    def sync_to_content(self, content_w: float, content_h: float) -> QRectF:
        r = self.compute_rect_in_content(content_w, content_h)
        self.setFixedSize(int(round(r.width())), int(round(r.height())))
        print(int(round(r.width())), int(round(r.height())))
        return r


# ============================================================
# CardContent: thân card (vẽ background, bo góc) bằng QSS
# ============================================================

class CardContent(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("CardContent")
        # self.setAttribute(Qt.WA_StyledBackground, True)

    def apply_style(self, sx: Dict[str, Any]):
        bg = sx.get("background", "#1c1f2b")
        bd = sx.get("border", "1px solid blue")
        br = px_int(sx.get("border-radius", "0px"), 0)
        self.setStyleSheet(
            f"QFrame#CardContent {{ background-color: {bg}; border-radius: {br}px;border: {bd}; }}"
        )


# ============================================================
# CardHost: tự đóng gói view+scene khi có pseudo
# ============================================================

class CardHost(QFrame):
    def __init__(self, parent: Optional[QWidget] = None, sx=None):
        super().__init__(parent)
        
        self.setObjectName("CardHost")

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.view: Optional[QGraphicsView] = None
        self.scene: Optional[QGraphicsScene] = None

        self.proxy_content: Optional[QGraphicsProxyWidget] = None
        self.before_widgets: List[PseudoFrame] = []
        self.after_widgets: List[PseudoFrame] = []
        self.before_proxies: List[QGraphicsProxyWidget] = []
        self.after_proxies: List[QGraphicsProxyWidget] = []

        self._timer: Optional[QTimer] = None
        
        self.apply_sx(sx)
        

    def apply_sx(self, sx: Dict[str, Any]):
        self._sx = sx

        w = px_int(sx.get("width", "200px"), 200)
        h = px_int(sx.get("height", "50px"), 50)
        self.setFixedSize(w, h)

        pseudo_blocks = self._extract_pseudo_blocks(sx)
        has_pseudo = len(pseudo_blocks) > 0

        if not has_pseudo:
            self._destroy_graphics_if_any()
            return

        self._ensure_graphics()
        self._rebuild_scene(pseudo_blocks)
        self._update_scene_layout()

    def _extract_pseudo_blocks(self, sx: Dict[str, Any]) -> List[Tuple[List[str], Dict[str, Any]]]:
        blocks: List[Tuple[List[str], Dict[str, Any]]] = []
        for k, v in sx.items():
            if isinstance(k, str) and k.strip().startswith("::") and isinstance(v, dict):
                selectors = [s.strip().lower() for s in k.split(",") if s.strip()]
                blocks.append((selectors, v))
        return blocks


    def _ensure_graphics(self):
        if self.view and self.scene:
            return

        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        
        self.view.setStyleSheet(f'QGraphicsView{{background: green;}}')

        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setFrameShape(QFrame.NoFrame)
        self.view.setRenderHints(self.view.renderHints() | QPainter.Antialiasing)
                
        self.layout().addWidget(self.view)


    def _destroy_graphics_if_any(self):
        if self._timer:
            self._timer.stop()
            self._timer.deleteLater()
            self._timer = None

        if self.view:
            self.view.setParent(None)
            self.view.deleteLater()
            self.view = None

        self.scene = None
        self.proxy_content = None
        self.before_widgets.clear()
        self.after_widgets.clear()
        self.before_proxies.clear()
        self.after_proxies.clear()

    def _rebuild_scene(self, pseudo_blocks: List[Tuple[List[str], Dict[str, Any]]]):
        assert self.scene is not None, "Scene phải được khởi tạo!"

        self.scene.clear()
        self.before_widgets.clear()
        self.after_widgets.clear()
        self.before_proxies.clear()
        self.after_proxies.clear()
        self.proxy_content = None


        # Pseudo proxies
        for selectors, rules in pseudo_blocks:
            if "::before" in selectors:
                w = PseudoFrame(rules, "before")
                p = QGraphicsProxyWidget()
                p.setWidget(w)
                self.scene.addItem(p)
                self.before_widgets.append(w)
                self.before_proxies.append(p)

            if "::after" in selectors:
                w = PseudoFrame(rules, "after")
                p = QGraphicsProxyWidget()
                p.setWidget(w)
                self.scene.addItem(p)
                self.after_widgets.append(w)
                self.after_proxies.append(p)
                
            
        # content frame
        # content = PseudoFrame(
        #     sx={
        #         # 'width': "200px", 
        #         # "height": "100px", 
        #         'width': "198px", 
        #         "height": "98px", 
        #         "background-color": "yellow", 
        #         "border-radius": "8px", 
        #         # "padding": "4px"
        #     }, 
        #     kind="after"
        # )
        # proxyContent = QGraphicsProxyWidget()
        # proxyContent.setWidget(content)
        # self.scene.addItem(proxyContent)
        # self.after_widgets.append(content)
        # self.after_proxies.append(proxyContent)


        # Z-order
        for p in self.before_proxies + self.after_proxies:
            p.setZValue(-1)

    def _update_scene_layout(self):

        vw = float(self.width())
        vh = float(self.height())

        self.scene.setSceneRect(0, 0, vw, vh)
        self.view.setSceneRect(self.scene.sceneRect())

        cw = float(self.width())
        ch = float(self.height())

        def place(pw: PseudoFrame, pr: QGraphicsProxyWidget):
            r = pw.sync_to_content(cw, ch)
            pr.setPos(r.topLeft())

        for pw, pr in zip(self.before_widgets, self.before_proxies):
            place(pw, pr)
        for pw, pr in zip(self.after_widgets, self.after_proxies):
            place(pw, pr)


    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._update_scene_layout()


# ============================================================
# Demo MainWindow
# ============================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CardHost đóng gói GraphicsView, PseudoFrame ăn QSS + chỉ rotate")
        self.resize(900, 520)

        self.central = QWidget(self)
        self.central.setLayout(QVBoxLayout())
        self.central.layout().setAlignment(Qt.AlignCenter)

        self.central.layout().addWidget(
            CardHost(
                sx={
                    "width": "200px",
                    "height": "100px",
                    "border-radius": "12px",
                    "background": "red",
                    # "background": "transparent",
                    "border": "2px solid blue",
                    "padding": "2px",
                    "::before": {
                        "content": "",
                        "height": "100%",
                        "width": "100%",
                        "background-color": "green",
                        "z-index": -1,
                        "padding": "0px",
                        "border-radius": "12px",
                        "border": "1px solid pink",
                        "top": "0px",
                        "left": "0px",
                    },
                    "::before": {
                        "content": "",
                        "height": "100%",
                        "width": "100%",
                        "background-color": "blue",
                        "z-index": -1,
                        "padding": "0px",
                        "border-radius": "12px",
                        "border": "1px solid pink",
                        "top": "0px",
                        "left": "0px",
                        "animation": {
                            "propertyName": "angle",
                            "easingCurve": "linear",
                            "direction": "forward",
                            "from": 0,
                            "to": 360,
                            "loop": "infinite",
                            "duration": 4000,
                        },
                    },
                }
            )
        )
        
        self.setCentralWidget(self.central)
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
