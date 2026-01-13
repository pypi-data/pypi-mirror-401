from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

from PySide6.QtCore import QRect, QSize, Qt, QTimer, QEvent
from PySide6.QtWidgets import QWidget, QLayout, QLayoutItem

# tái dùng engine đã test pass
from .flexbox_engine import StackLayoutEngine, StackItem


LayoutCallback = Callable[[Dict[str, Any]], None]


def _sx_of_widget(w: QWidget) -> Dict[str, Any]:
    sx = getattr(w, "_sx_dict", None)
    return sx if isinstance(sx, dict) else {}


def _safe_item_sizes(w: QWidget) -> Tuple[QSize, QSize]:
    sh = w.sizeHint()
    msh = w.minimumSizeHint()

    sw = sh.width() if sh.width() > 0 else msh.width()
    shh = sh.height() if sh.height() > 0 else msh.height()

    if sw <= 0:
        sw = 1
    if shh <= 0:
        shh = 1

    size_hint = QSize(sw, shh)

    mw = max(0, int(w.minimumWidth()))
    mh = max(0, int(w.minimumHeight()))
    if mw <= 0 and msh.width() > 0:
        mw = msh.width()
    if mh <= 0 and msh.height() > 0:
        mh = msh.height()
    min_size = QSize(mw, mh)
    return size_hint, min_size


def _parse_item_sx(sx: Dict[str, Any]) -> Tuple[int, int, int, Optional[str]]:
    order = int(sx.get("order", 0) or 0)
    fg = int(sx.get("flexGrow", 0) or 0)
    fs = int(sx.get("flexShrink", 1) or 1)
    al = sx.get("alignSelf", None)
    al = str(al) if isinstance(al, str) else None
    return order, fg, fs, al


def _summarize_lines_by_y(rects: Dict[str, QRect], keys_in_order: List[str]) -> List[List[str]]:
    # group theo y giống test_case_011
    lines: List[List[str]] = []
    y_to_line: Dict[int, List[str]] = {}
    for k in keys_in_order:
        r = rects.get(k)
        if not r:
            continue
        y_to_line.setdefault(r.y(), []).append(k)
    for y in sorted(y_to_line.keys()):
        lines.append(y_to_line[y])
    return lines


class _FlexEngineLayout(QLayout):
    """
    QLayout "mỏng": chỉ bridge Qt layout lifecycle -> StackLayoutEngine.compute
    Không container widget, setGeometry trực tiếp cho QLayoutItem.
    """

    def __init__(self, owner: "FlexBox", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._owner = owner
        self._items: List[QLayoutItem] = []
        self.engine = StackLayoutEngine()

        self.setSpacing(0)

    # ---- QLayout required ----
    def addItem(self, item: QLayoutItem) -> None:
        self._items.append(item)
        self.invalidate()

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int) -> Optional[QLayoutItem]:
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index: int) -> Optional[QLayoutItem]:
        if 0 <= index < len(self._items):
            it = self._items.pop(index)
            self.invalidate()
            return it
        return None

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, w: int) -> int:
        if w <= 0 or not self._items:
            return 0
        props = self._owner._props_dict()
        stack_items = self._to_stack_items()
        return self.engine.measure_height_for_width(w, stack_items, props)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        # tối thiểu gọn: max(min_size) + margins
        mw = 0
        mh = 0
        for it in self._items:
            w = it.widget()
            if not w:
                continue
            _, mn = _safe_item_sizes(w)
            mw = max(mw, mn.width())
            mh = max(mh, mn.height())
        l, t, r, b = self.getContentsMargins()
        return QSize(mw + l + r, mh + t + b)

    def setGeometry(self, rect: QRect) -> None:
        super().setGeometry(rect)
        if not self._items:
            return

        props = self._owner._props_dict()
        stack_items = self._to_stack_items()

        rects = self.engine.compute(rect, stack_items, props)

        # apply geometry
        for it in self._items:
            w = it.widget()
            if not w:
                continue
            key = self._key_for_widget(w)
            r = rects.get(key)
            if r is not None:
                it.setGeometry(r)

        # notify owner (for logging/testing)
        self._owner._emit_layout(rect, rects)

    # ---- internal ----
    def _key_for_widget(self, w: QWidget) -> str:
        # ổn định theo vị trí trong layout (index) + id, tránh trùng
        idx = -1
        for i, it in enumerate(self._items):
            if it.widget() is w:
                idx = i
                break
        name = w.objectName()
        base = name if (name and name != "Stack") else f"{idx}"
        return f"{base}#{id(w)}"

    def _to_stack_items(self) -> List[StackItem]:
        out: List[StackItem] = []
        for it in self._items:
            w = it.widget()
            if not w:
                continue
            size_hint, min_size = _safe_item_sizes(w)
            sx = _sx_of_widget(w)
            order, fg, fs, al = _parse_item_sx(sx)
            out.append(
                StackItem(
                    key=self._key_for_widget(w),
                    size_hint=size_hint,
                    min_size=min_size,
                    flex_grow=max(0, int(fg)),
                    flex_shrink=max(0, int(fs)),
                    order=int(order),
                    align_self=al,
                )
            )
        return out


class FlexBox(QWidget):
    """
    FlexBox = QWidget dùng engine flexbox (StackLayoutEngine) qua QLayout.
    - children=[...] trong constructor là đủ (không setup ngoài)
    - sx={...} chứa props flex
    - onLayout(payload) để lấy rects/lines/breakpoints
    """

    def __init__(
        self,
        *,
        sx: Optional[Dict[str, Any]] = None,
        children: Optional[List[QWidget]] = None,
        onLayout: Optional[LayoutCallback] = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._sx = sx if isinstance(sx, dict) else {}
        self._onLayout = onLayout

        self._layout_pending = False
        self._last_payload_sig: Optional[Tuple[int, int]] = None

        lay = _FlexEngineLayout(owner=self, parent=self)
        self.setLayout(lay)

        # margins/padding sẽ nằm trong props, nhưng Qt layout margins cũng cần 0 để engine toàn quyền
        self.layout().setContentsMargins(0, 0, 0, 0)

        if children:
            for w in children:
                self.addChild(w)

        # request initial layout (coalesce)
        self.requestLayout()

    def addChild(self, w: QWidget) -> None:
        # mọi thứ gọn trong tree: addChild chỉ dùng nội bộ constructor/updates
        self.layout().addWidget(w)
        self.requestLayout()

    def setSx(self, sx: Dict[str, Any]) -> None:
        self._sx = sx if isinstance(sx, dict) else {}
        self.requestLayout()

    def requestLayout(self) -> None:
        if self._layout_pending:
            return
        self._layout_pending = True
        QTimer.singleShot(0, self._do_layout)

    def _do_layout(self) -> None:
        self._layout_pending = False
        # Qt sẽ gọi setGeometry khi cần; nhưng đôi khi cần kích hoạt lại
        self.updateGeometry()
        self.layout().activate()

    def event(self, e: QEvent):
        # khi show/resize, đảm bảo layout cập nhật
        if e.type() in (QEvent.Show, QEvent.Resize, QEvent.Polish):
            self.requestLayout()
        return super().event(e)

    # ---- props + emit ----
    def _props_dict(self) -> Dict[str, Any]:
        # normalize sx giống MUI naming
        gap = self._sx.get("gap", 0)
        padding = self._sx.get("padding", 0)

        # padding: nếu dùng hệ spacing scale 8px, bạn có thể đổi ở đây.
        # hiện lấy trực tiếp số px (giống các test).
        return {
            "direction": self._sx.get("flexDirection", "row"),
            "flexWrap": self._sx.get("flexWrap", "nowrap"),
            "justifyContent": self._sx.get("justifyContent", "flex-start"),
            "alignItems": self._sx.get("alignItems", "stretch"),
            "alignContent": self._sx.get("alignContent", "flex-start"),
            "gap": int(gap),
            "padding": int(padding),
        }

    def _emit_layout(self, outer_rect: QRect, item_rects: Dict[str, QRect]) -> None:
        if not self._onLayout:
            return

        # stable ordered keys by layout order (index in keys string starts with idx)
        keys = list(item_rects.keys())

        # line grouping theo y của items (cho parent)
        lines = _summarize_lines_by_y(item_rects, keys)

        payload = {
            "rect": outer_rect,
            "items": item_rects,
            "lines": lines,
            "props": self._props_dict(),
        }

        # tránh spam: signature theo (w,h)
        sig = (outer_rect.width(), outer_rect.height())
        if self._last_payload_sig == sig:
            # vẫn có thể thay đổi lines khi wrap, nên không chặn tuyệt đối
            pass
        self._last_payload_sig = sig

        self._onLayout(payload)
