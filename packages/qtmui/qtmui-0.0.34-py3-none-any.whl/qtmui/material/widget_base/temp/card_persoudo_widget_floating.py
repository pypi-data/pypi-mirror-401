#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
from typing import Any, Dict, List, Tuple, Optional

from PySide6.QtCore import Qt, QRectF, QPoint
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFrame


# ============================================================
# CSS-ish parsing helpers
# ============================================================

_len_re = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*(px|%)?\s*$", re.IGNORECASE)

def parse_len(v: Any) -> Tuple[str, float]:
    """Trả về (unit, value) với unit = 'px' hoặc '%'."""
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
    """Đổi độ dài sang px theo basis nếu là %."""
    unit, val = lenv
    return basis * val / 100.0 if unit == "%" else val

def parse_translate(v: Any) -> Tuple[Tuple[str, float], Tuple[str, float]]:
    """'-50% -50%' -> ((%, -50), (%, -50))"""
    if not v:
        return (("px", 0.0), ("px", 0.0))
    parts = str(v).strip().split()
    if len(parts) == 1:
        parts = [parts[0], "0"]
    return (parse_len(parts[0]), parse_len(parts[1]))

def px_int(v: Any, default: int = 0) -> int:
    """Chỉ lấy px/int, nếu là % thì fallback default."""
    unit, val = parse_len(v)
    if unit == "%":
        return default
    return int(round(val))


# ============================================================
# PseudoFrame: SIBLING của Card (cùng parent với Card)
# ============================================================

class PseudoFrame(QFrame):
    """
    PseudoFrame KHÔNG là con của Card nữa.
    Nó có parent = parent của Card (host), để có thể lower/raise so với Card.

    Vị trí/size của pseudo được tính theo sx trong hệ tọa độ Card,
    rồi map qua host bằng card.mapTo(host, ...).
    """

    def __init__(self, host: QWidget, card: "CardHost", sx: Dict[str, Any], kind: str):
        super().__init__(host)
        self.host = host
        self.card = card
        self.sx = sx
        self.kind = kind

        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        bg = sx.get("background-color") or sx.get("background") or "red"
        self._bg = QColor(str(bg))
        if not self._bg.isValid():
            self._bg = QColor("red")

        self._pad = px_int(sx.get("padding", "0px"), 0)
        self._radius = px_int(sx.get("border-radius", "0px"), 0)
        self._z = int(sx.get("z-index", -1))

        # Style để nhìn thấy
        self.setStyleSheet(
            f"QFrame {{ background-color: {self._bg.name()}; border-radius: {self._radius}px; }}"
        )

        print(f"[PseudoFrame:init] kind={self.kind} z={self._z} bg={self._bg.name()} pad={self._pad} radius={self._radius}")

        self.sync_geometry()
        self.show()

    def z_index(self) -> int:
        return self._z

    def compute_rect_in_card(self) -> QRectF:
        """
        Tính rect pseudo trong toạ độ CARD (local coords).
        """
        cw = float(self.card.width())
        ch = float(self.card.height())

        w = len_to_px(parse_len(self.sx.get("width", "100%")), cw)
        h = len_to_px(parse_len(self.sx.get("height", "100%")), ch)

        left = len_to_px(parse_len(self.sx.get("left", "0px")), cw)
        top = len_to_px(parse_len(self.sx.get("top", "0px")), ch)

        tx_len, ty_len = parse_translate(self.sx.get("translate", "0px 0px"))
        tx = len_to_px(tx_len, w)
        ty = len_to_px(ty_len, h)

        x = left + tx
        y = top + ty

        pad = float(self._pad)
        return QRectF(x - pad, y - pad, w + 2 * pad, h + 2 * pad)

    def sync_geometry(self):
        """
        Map rect từ CARD -> HOST để setGeometry.
        """
        r_card = self.compute_rect_in_card()

        # Map top-left từ card sang host
        tl_host: QPoint = self.card.mapTo(self.host, r_card.topLeft().toPoint())

        xi = int(tl_host.x())
        yi = int(tl_host.y())
        wi = int(round(r_card.width()))
        hi = int(round(r_card.height()))
        self.setGeometry(xi, yi, wi, hi)

        print(
            f"[PseudoFrame:sync_geometry] kind={self.kind} z={self._z}\n"
            f"  card_pos_in_host={self.card.pos()} card_size=({self.card.width()},{self.card.height()})\n"
            f"  rect_in_card=(x={r_card.x():.1f}, y={r_card.y():.1f}, w={r_card.width():.1f}, h={r_card.height():.1f})\n"
            f"  => geom_in_host=(x={xi}, y={yi}, w={wi}, h={hi})"
        )


# ============================================================
# CardHost: frame chính (vẫn giữ background ở đây)
# ============================================================

class CardHost(QFrame):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.before: List[PseudoFrame] = []
        self.after: List[PseudoFrame] = []
        self._host: Optional[QWidget] = None  # parent của card (nơi pseudo được attach)

    def apply_sx(self, sx: Dict[str, Any]):
        # Host = parent của card
        self._host = self.parentWidget()
        if self._host is None:
            raise RuntimeError("CardHost phải có parentWidget để đặt pseudo sibling.")

        # Base style của CardHost (giữ nguyên như bạn muốn)
        cw = px_int(sx.get("width", "200px"), 200)
        ch = px_int(sx.get("height", "50px"), 50)
        bg = sx.get("background", "#1c1f2b")
        br = px_int(sx.get("border-radius", "0px"), 0)

        self.setFixedSize(cw, ch)
        self.setStyleSheet(f"QFrame {{ background-color: {bg}; border-radius: {br}px; }}")

        print(f"[CardHost:apply_sx] size=({cw},{ch}) bg={bg} radius={br} host={type(self._host).__name__}")

        # Xoá pseudo cũ
        for w in (self.before + self.after):
            w.deleteLater()
        self.before, self.after = [], []

        # Parse pseudo rules
        for k, rules in sx.items():
            if not (isinstance(k, str) and k.strip().startswith("::") and isinstance(rules, dict)):
                continue
            selectors = [s.strip().lower() for s in k.split(",") if s.strip()]

            if "::before" in selectors:
                self.before.append(PseudoFrame(self._host, self, rules, "before"))
            if "::after" in selectors:
                self.after.append(PseudoFrame(self._host, self, rules, "after"))

        self.update_pseudos()

    def update_pseudos(self):
        """
        Cập nhật vị trí pseudo khi card move/resize.
        Đồng thời sắp xếp layer theo z-index tương đối với card.
        """
        all_p = self.before + self.after
        print(f"[CardHost:update_pseudos] card_pos={self.pos()} card_size={self.size()} pseudo={len(all_p)}")

        for p in all_p:
            p.sync_geometry()

        # Stacking: nếu z < 0 => pseudo xuống dưới card
        # vì cùng parent nên raise_/lower_ sẽ có tác dụng
        for p in all_p:
            if p.z_index() < 0:
                p.lower()
            else:
                p.raise_()

        # Đảm bảo card nằm trên tất cả pseudo z<0
        # và nằm dưới pseudo z>=0 (vì pseudo z>=0 đã raise_ rồi)
        self.raise_()

    def moveEvent(self, e):
        super().moveEvent(e)
        print(f"[CardHost:moveEvent] new_pos={self.pos()}")
        self.update_pseudos()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        print(f"[CardHost:resizeEvent] new_size={self.size()}")
        self.update_pseudos()


# ============================================================
# Demo MainWindow
# ============================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pseudo sibling (same parent) -> raise/lower works")
        self.resize(800, 450)

        central = QWidget(self)
        self.setCentralWidget(central)

        self.card = CardHost(central)
        self.card.move(300, 180)

        # NOTE: ::before z-index=-1 sẽ nằm DƯỚI card (nhìn như border phía sau)
        sx = {
            "width": "200px",
            "height": "50px",
            "border-radius": "10px",
            "background": "#1c1f2b",
            "::before": {
                "content": "",
                "height": "100%",
                "width": "100%",
                "background-color": "red",
                "z-index": -1,          # thử -1 để nằm dưới card
                "padding": "8px",       # nới ra để thấy rõ viền
                "border-radius": "10px",
                "top": "50%",
                "left": "50%",
                "translate": "-50% -50%",
            },
            "::after": {
                "content": "",
                "height": "90%",
                "width": "90%",
                "background-color": "green",
                "z-index": 1,          # thử -1 để nằm dưới card
                "padding": "14px",       # nới ra để thấy rõ viền
                "border-radius": "10px",
                "top": "50%",
                "left": "50%",
                "translate": "-50% -50%",
            },
            # Bạn có thể bật after để test nằm trên:
            # "::after": { ... "z-index": 1, ... }
        }
        self.card.apply_sx(sx)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        # Nếu central layout thay đổi, cập nhật pseudo
        self.card.update_pseudos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
