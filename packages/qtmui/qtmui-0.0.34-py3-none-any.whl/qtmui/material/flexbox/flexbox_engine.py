from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from PySide6.QtCore import QRect, QSize, Qt, QTimer, QEvent
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QWidget, QSizePolicy

try:
    from qtmui.hooks import State  # type: ignore
except Exception:  # pragma: no cover
    State = None  # noqa: N816


def _is_state(v: Any) -> bool:
    return State is not None and isinstance(v, State)


def _state_value(v: Any) -> Any:
    return v.value if _is_state(v) else v


def _try_connect_state(v: Any, slot) -> None:
    if not _is_state(v):
        return
    try:
        v.valueChanged.connect(slot)  # type: ignore[attr-defined]
    except Exception:
        try:
            v.valueChanged.connect(lambda *_: slot())  # type: ignore[attr-defined]
        except Exception:
            pass


VALID_DIRECTIONS = ("row", "row-reverse", "column", "column-reverse")
VALID_FLEX_WRAP = ("nowrap", "wrap")
VALID_ALIGN_ITEMS = ("flex-start", "center", "flex-end", "stretch", "baseline")
VALID_JUSTIFY = ("flex-start", "center", "flex-end", "space-between", "space-around", "space-evenly")
VALID_ALIGN_CONTENT = ("flex-start", "center", "flex-end", "space-between", "space-around", "space-evenly", "stretch")
VALID_VARIANTS = (None, "outlined")


def _validate_optional_number_or_dict(name: str, value: Any) -> None:
    if value is None:
        return
    if _is_state(value):
        return
    if isinstance(value, (int, float)):
        if value < 0:
            raise ValueError(f"[Stack] {name} phải >= 0")
        return
    if isinstance(value, dict):
        for k, v in value.items():
            if k not in ("xs", "sm", "md", "lg", "xl"):
                raise ValueError(f"[Stack] {name} breakpoint key không hợp lệ: {k}")
            if not isinstance(v, (int, float)) or v < 0:
                raise ValueError(f"[Stack] {name}[{k}] phải là số >=0")
        return
    raise TypeError(f"[Stack] {name} phải là (int|float|dict|State|None). Got {type(value)}")


def _validate_optional_dict(name: str, value: Any) -> None:
    if value is None:
        return
    if _is_state(value):
        return
    if not isinstance(value, dict):
        raise TypeError(f"[Stack] {name} phải là dict|State|None. Got {type(value)}")


@dataclass(frozen=True)
class StackItem:
    key: str
    size_hint: QSize
    min_size: QSize
    flex_grow: int = 0
    flex_shrink: int = 1
    order: int = 0
    align_self: Optional[str] = None


@dataclass(frozen=True)
class _NormProps:
    direction: str
    flexWrap: str
    wrap: bool
    gap: int
    justifyContent: str
    alignItems: str
    alignContent: str
    margins: Tuple[int, int, int, int]


def _get_prop(props: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    for k in keys:
        if k in props:
            return props[k]
    return default


def _normalize_props(props: Optional[Dict[str, Any]]) -> _NormProps:
    props = props or {}

    direction = _state_value(_get_prop(props, "direction", default="row")) or "row"
    if direction not in VALID_DIRECTIONS:
        direction = "row"

    flexWrap = _state_value(_get_prop(props, "flexWrap", "flex_wrap", default=None))
    wrap_flag = _state_value(_get_prop(props, "wrap", default=None))

    if isinstance(flexWrap, str):
        flexWrap = flexWrap.strip()
        if flexWrap not in VALID_FLEX_WRAP:
            flexWrap = "nowrap"
    else:
        if isinstance(wrap_flag, bool) and wrap_flag:
            flexWrap = "wrap"
        else:
            flexWrap = "nowrap"

    wrap = (flexWrap == "wrap")

    gap = _state_value(_get_prop(props, "gap", default=8))
    try:
        gap = int(gap)
    except Exception:
        gap = 8
    if gap < 0:
        gap = 0

    justifyContent = _state_value(_get_prop(props, "justifyContent", "justify_content", default="flex-start")) or "flex-start"
    if justifyContent not in VALID_JUSTIFY:
        justifyContent = "flex-start"

    alignItems = _state_value(_get_prop(props, "alignItems", "align_items", default="flex-start")) or "flex-start"
    if alignItems not in VALID_ALIGN_ITEMS:
        alignItems = "flex-start"

    alignContent = _state_value(_get_prop(props, "alignContent", "align_content", default="flex-start")) or "flex-start"
    if alignContent not in VALID_ALIGN_CONTENT:
        alignContent = "flex-start"

    margins = _state_value(_get_prop(props, "margins", default=(0, 0, 0, 0)))
    if isinstance(margins, (list, tuple)) and len(margins) == 4:
        try:
            margins = tuple(int(x) for x in margins)  # type: ignore[assignment]
        except Exception:
            margins = (0, 0, 0, 0)
    else:
        margins = (0, 0, 0, 0)

    return _NormProps(
        direction=direction,
        flexWrap=flexWrap,
        wrap=wrap,
        gap=gap,
        justifyContent=justifyContent,
        alignItems=alignItems,
        alignContent=alignContent,
        margins=margins,  # type: ignore[arg-type]
    )


class StackLayoutEngine:
    @staticmethod
    def _axis(p: _NormProps) -> str:
        return "row" if p.direction.startswith("row") else "column"

    @staticmethod
    def _is_reverse(p: _NormProps) -> bool:
        return p.direction in ("row-reverse", "column-reverse")

    @staticmethod
    def _avail_rect(container_rect: QRect, margins: Tuple[int, int, int, int]) -> QRect:
        l, t, r, b = margins
        return QRect(
            container_rect.x() + l,
            container_rect.y() + t,
            max(0, container_rect.width() - (l + r)),
            max(0, container_rect.height() - (t + b)),
        )

    @staticmethod
    def _distribute_main(remaining: int, n_gaps: int, gap: int, mode: str) -> Tuple[int, List[int]]:
        if n_gaps <= 0:
            return 0, []
        if mode == "flex-start":
            return 0, [gap] * n_gaps
        if mode == "flex-end":
            return remaining, [gap] * n_gaps
        if mode == "center":
            return remaining // 2, [gap] * n_gaps
        if mode == "space-between":
            each = remaining // n_gaps if n_gaps else 0
            return 0, [each] * n_gaps
        if mode == "space-around":
            each = remaining // (n_gaps + 1) if (n_gaps + 1) else 0
            return each // 2, [each] * n_gaps
        if mode == "space-evenly":
            each = remaining // (n_gaps + 2) if (n_gaps + 2) else 0
            return each, [each] * n_gaps
        return 0, [gap] * n_gaps

    @staticmethod
    def _distribute_cross(remaining: int, n_gaps: int, mode: str) -> Tuple[int, List[int]]:
        if n_gaps <= 0:
            return 0, []
        if mode == "flex-start":
            return 0, [0] * n_gaps
        if mode == "flex-end":
            return remaining, [0] * n_gaps
        if mode == "center":
            return remaining // 2, [0] * n_gaps
        if mode == "space-between":
            each = remaining // n_gaps if n_gaps else 0
            return 0, [each] * n_gaps
        if mode == "space-around":
            each = remaining // (n_gaps + 1) if (n_gaps + 1) else 0
            return each // 2, [each] * n_gaps
        if mode == "space-evenly":
            each = remaining // (n_gaps + 2) if (n_gaps + 2) else 0
            return each, [each] * n_gaps
        return 0, [0] * n_gaps

    @staticmethod
    def measure_height_for_width(width: int, items: List[StackItem], props: Dict[str, Any]) -> int:
        p = _normalize_props(props)
        if width <= 0 or not items:
            return 0

        axis = StackLayoutEngine._axis(p)
        gap = int(p.gap)

        def clamp_nonneg(n: int) -> int:
            return n if n > 0 else 0

        def item_w(it: StackItem) -> int:
            return clamp_nonneg(max(it.min_size.width(), it.size_hint.width()))

        def item_h(it: StackItem) -> int:
            return clamp_nonneg(max(it.min_size.height(), it.size_hint.height()))

        indexed = list(enumerate(items))
        indexed.sort(key=lambda t: (t[1].order, t[0]))
        ordered = [it for _, it in indexed]
        if StackLayoutEngine._is_reverse(p):
            ordered.reverse()

        if axis != "row":
            return sum(item_h(it) for it in ordered) + gap * max(0, len(ordered) - 1)

        if not p.wrap:
            return max(item_h(it) for it in ordered)

        lines: List[List[StackItem]] = []
        cur: List[StackItem] = []
        cur_w = 0
        for it in ordered:
            w0 = item_w(it)
            add = w0 if not cur else (gap + w0)
            if cur and (cur_w + add) > width:
                lines.append(cur)
                cur = [it]
                cur_w = w0
            else:
                cur.append(it)
                cur_w += add
        if cur:
            lines.append(cur)

        line_heights = [max(item_h(it) for it in line) for line in lines]
        return sum(line_heights) + gap * max(0, len(lines) - 1)

    @staticmethod
    def compute(container_rect: QRect, items: List[StackItem], props: Dict[str, Any]) -> Dict[str, QRect]:
        p = _normalize_props(props)

        axis = StackLayoutEngine._axis(p)
        reverse = StackLayoutEngine._is_reverse(p)
        avail = StackLayoutEngine._avail_rect(container_rect, p.margins)

        if avail.width() <= 0 or avail.height() <= 0 or not items:
            return {}

        indexed = list(enumerate(items))
        indexed.sort(key=lambda t: (t[1].order, t[0]))
        ordered = [it for _, it in indexed]
        if reverse:
            ordered.reverse()

        gap = int(p.gap)

        def clamp_nonneg(n: int) -> int:
            return n if n > 0 else 0

        def item_w(it: StackItem) -> int:
            return clamp_nonneg(max(it.min_size.width(), it.size_hint.width()))

        def item_h(it: StackItem) -> int:
            return clamp_nonneg(max(it.min_size.height(), it.size_hint.height()))

        def align_mode_for_item(it: StackItem) -> str:
            return it.align_self if it.align_self else p.alignItems

        result: Dict[str, QRect] = {}

        if not p.wrap:
            if axis == "row":
                line_cross = avail.height()

                base_ws = [item_w(it) for it in ordered]
                hs = [item_h(it) for it in ordered]
                n_gaps = max(0, len(ordered) - 1)

                used_main = sum(base_ws) + gap * n_gaps

                ws = base_ws[:]
                if used_main > avail.width():
                    overflow = used_main - avail.width()
                    total_shrink = sum(max(0, it.flex_shrink) for it in ordered)
                    if total_shrink > 0:
                        acc = 0
                        for i, it in enumerate(ordered):
                            s = max(0, it.flex_shrink)
                            dec = (overflow * s) // total_shrink
                            ws[i] = max(it.min_size.width(), ws[i] - dec)
                            acc += dec
                        rem = overflow - acc
                        if rem > 0:
                            for i in range(len(ordered) - 1, -1, -1):
                                if max(0, ordered[i].flex_shrink) > 0:
                                    ws[i] = max(ordered[i].min_size.width(), ws[i] - rem)
                                    break

                used_main = sum(ws) + gap * n_gaps
                remaining = max(0, avail.width() - used_main)

                if p.justifyContent in ("flex-start", "center", "flex-end"):
                    total_grow = sum(max(0, it.flex_grow) for it in ordered)
                    if total_grow > 0 and remaining > 0:
                        acc = 0
                        for i, it in enumerate(ordered):
                            g = max(0, it.flex_grow)
                            add = (remaining * g) // total_grow
                            ws[i] += add
                            acc += add
                        rem = remaining - acc
                        if rem > 0:
                            for i in range(len(ordered) - 1, -1, -1):
                                if max(0, ordered[i].flex_grow) > 0:
                                    ws[i] += rem
                                    break

                used_main = sum(ws) + gap * n_gaps
                remaining_after = max(0, avail.width() - used_main)

                start_off, gaps_main = StackLayoutEngine._distribute_main(
                    remaining_after, n_gaps, gap, p.justifyContent
                )

                x = avail.x() + start_off
                y_line = avail.y()

                max_h = max(hs) if hs else 0
                baseline_y = y_line + (max_h // 2)

                for i, it in enumerate(ordered):
                    w0 = ws[i]
                    h0 = hs[i]
                    mode = align_mode_for_item(it)

                    if mode == "flex-start":
                        iy, ih = y_line, h0
                    elif mode == "flex-end":
                        iy, ih = y_line + (line_cross - h0), h0
                    elif mode == "stretch":
                        iy, ih = y_line, line_cross
                    elif mode == "baseline":
                        iy, ih = baseline_y - (h0 // 2), h0
                    else:
                        iy, ih = y_line + (line_cross - h0) // 2, h0

                    result[it.key] = QRect(x, iy, w0, ih)

                    x += w0
                    if i < n_gaps:
                        x += gaps_main[i] if gaps_main else gap

            else:
                line_cross = avail.width()

                used_main = sum(item_h(it) for it in ordered) + gap * max(0, len(ordered) - 1)
                remaining = max(0, avail.height() - used_main)
                n_gaps = max(0, len(ordered) - 1)

                start_off, gaps_main = StackLayoutEngine._distribute_main(
                    remaining, n_gaps, gap, p.justifyContent
                )
                y = avail.y() + start_off
                x_line = avail.x()

                for i, it in enumerate(ordered):
                    w0, h0 = item_w(it), item_h(it)
                    mode = align_mode_for_item(it)

                    if mode == "flex-start":
                        ix, iw = x_line, w0
                    elif mode == "flex-end":
                        ix, iw = x_line + (line_cross - w0), w0
                    elif mode == "stretch":
                        ix, iw = x_line, line_cross
                    else:
                        ix, iw = x_line + (line_cross - w0) // 2, w0

                    result[it.key] = QRect(ix, y, iw, h0)
                    y += h0
                    if i < n_gaps:
                        y += gaps_main[i] if gaps_main else gap

            return result

        if axis != "row":
            return result

        lines: List[List[StackItem]] = []
        current: List[StackItem] = []
        cur_w = 0
        for it in ordered:
            w0 = item_w(it)
            add = w0 if not current else (gap + w0)
            if current and (cur_w + add) > avail.width():
                lines.append(current)
                current = [it]
                cur_w = w0
            else:
                current.append(it)
                cur_w += add
        if current:
            lines.append(current)

        line_crosses = [max(item_h(it) for it in line) for line in lines]

        if len(lines) == 1:
            props_nowrap = dict(props or {})
            props_nowrap["flexWrap"] = "nowrap"
            props_nowrap["wrap"] = False
            return StackLayoutEngine.compute(container_rect, items, props_nowrap)

        total_cross = sum(line_crosses) + gap * (len(lines) - 1)
        remaining_cross = max(0, avail.height() - total_cross)

        if p.alignContent == "stretch" and len(lines) > 0:
            extra_each = remaining_cross // len(lines)
            rem = remaining_cross - extra_each * len(lines)
            for i in range(len(line_crosses)):
                line_crosses[i] += extra_each + (1 if i < rem else 0)
            remaining_cross = 0

        start_cross_off, gaps_cross = StackLayoutEngine._distribute_cross(
            remaining_cross, len(lines) - 1, p.alignContent
        )

        y = avail.y() + start_cross_off
        for li, line in enumerate(lines):
            line_h = line_crosses[li]
            n_gaps = max(0, len(line) - 1)

            base_ws = [item_w(it) for it in line]
            hs = [item_h(it) for it in line]
            base_total = sum(base_ws) + gap * n_gaps
            remaining_main = max(0, avail.width() - base_total)

            ws = base_ws[:]
            if p.justifyContent in ("flex-start", "center", "flex-end"):
                total_grow = sum(max(0, it.flex_grow) for it in line)
                if total_grow > 0 and remaining_main > 0:
                    acc = 0
                    for i_it, it in enumerate(line):
                        g = max(0, it.flex_grow)
                        add = (remaining_main * g) // total_grow
                        ws[i_it] += add
                        acc += add
                    rem = remaining_main - acc
                    if rem > 0:
                        for i_it in range(len(line) - 1, -1, -1):
                            if max(0, line[i_it].flex_grow) > 0:
                                ws[i_it] += rem
                                break

            used_main = sum(ws) + gap * n_gaps
            remaining_after = max(0, avail.width() - used_main)

            start_main_off, gaps_main = StackLayoutEngine._distribute_main(
                remaining_after, n_gaps, gap, p.justifyContent
            )

            x = avail.x() + start_main_off
            baseline_y = y + (line_h // 2)

            for i_it, it in enumerate(line):
                w0 = ws[i_it]
                h0 = hs[i_it]
                mode = align_mode_for_item(it)

                if mode == "flex-start":
                    iy, ih = y, h0
                elif mode == "flex-end":
                    iy, ih = y + (line_h - h0), h0
                elif mode == "stretch":
                    iy, ih = y, line_h
                elif mode == "baseline":
                    iy, ih = baseline_y - (h0 // 2), h0
                else:
                    iy, ih = y + (line_h - h0) // 2, h0

                result[it.key] = QRect(x, iy, w0, ih)
                x += w0
                if i_it < n_gaps:
                    x += gaps_main[i_it] if gaps_main else gap

            if li < len(lines) - 1:
                y += line_h
                y += gap
                y += gaps_cross[li] if gaps_cross else 0

        return result


class Stack(QFrame):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *,
        spacing: Optional[Union[int, float, dict, Any]] = 0,
        direction: Optional[Union[str, dict, Any]] = "column",
        flexWrap: Optional[Union[str, Any]] = "nowrap",
        variant: Optional[Union[str, Any]] = None,
        alignItems: Optional[Union[str, Any]] = "stretch",
        alignItem: Optional[Union[str, Any]] = None,
        justifyContent: Optional[Union[str, Any]] = "flex-start",
        alignContent: Optional[Union[str, Any]] = "flex-start",
        children: Optional[Union[List[QWidget], Any]] = None,
        sx: Optional[Union[dict, Any]] = None,
        useFlexGap: Optional[Union[bool, Any]] = True,
        **kwargs,
    ):
        super().__init__(parent)
        self.setObjectName("Stack")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(0, 0, 0, 0)
        self._root.setSpacing(0)

        self._container = QWidget(self)
        self._container.setObjectName("StackContainer")
        self._container.setAttribute(Qt.WA_StyledBackground, True)
        self._root.addWidget(self._container)

        self.engine = StackLayoutEngine()

        self._widgets: List[Tuple[str, QWidget]] = []
        self._items: List[StackItem] = []
        self._item_sx: Dict[str, dict] = {}

        self.auto_height: bool = False
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self._kwargs = dict(kwargs)

        _validate_optional_number_or_dict("spacing", spacing)
        _validate_optional_dict("sx", sx)

        self._spacing = spacing
        self._direction = direction
        self._flexWrap = flexWrap
        self._alignItems = alignItem if alignItem is not None else alignItems
        self._justifyContent = justifyContent
        self._alignContent = alignContent
        self._variant = variant
        self._sx = sx
        self._useFlexGap = useFlexGap

        self._sx_dict = _state_value(self._sx) if self._sx is not None else None
        self._sx_dict = self._sx_dict if isinstance(self._sx_dict, dict) else {}

        self._connect_signals()
        self._apply_variant()
        self._init_children(children)

        QTimer.singleShot(0, self.apply_layout)
        
        self._container.installEventFilter(self)

    @staticmethod
    def _get_breakpoint() -> str:
        app = QApplication.instance()
        width = None
        try:
            aw = app.activeWindow() if app else None
            if aw is not None:
                width = aw.width()
        except Exception:
            width = None

        if width is None:
            try:
                if app and app.topLevelWidgets():
                    width = app.topLevelWidgets()[0].width()
            except Exception:
                width = None

        if width is None:
            width = 0

        if width >= 1536:
            return "xl"
        if width >= 1200:
            return "lg"
        if width >= 900:
            return "md"
        if width >= 600:
            return "sm"
        return "xs"

    @staticmethod
    def _resolve_breakpoint_value(v: Any, bp: str) -> Any:
        v = _state_value(v)
        if not isinstance(v, dict):
            return v
        breakpoints = ["xs", "sm", "md", "lg", "xl"]
        if bp not in breakpoints:
            bp = "xs"
        if bp in v:
            return v[bp]
        idx = breakpoints.index(bp)
        for i in range(idx - 1, -1, -1):
            k = breakpoints[i]
            if k in v:
                return v[k]
        return None

    def _compute_props_dict(self) -> Dict[str, Any]:
        bp = self._get_breakpoint()

        direction = self._resolve_breakpoint_value(self._direction, bp)
        direction = _state_value(direction) if direction is not None else "column"
        if not isinstance(direction, str) or direction not in VALID_DIRECTIONS:
            direction = "column"

        flexWrap = _state_value(self._flexWrap) or "nowrap"
        if not isinstance(flexWrap, str) or flexWrap not in VALID_FLEX_WRAP:
            flexWrap = "nowrap"

        alignItems = _state_value(self._alignItems) or "stretch"
        if not isinstance(alignItems, str) or alignItems not in VALID_ALIGN_ITEMS:
            alignItems = "stretch"

        justifyContent = _state_value(self._justifyContent) or "flex-start"
        if not isinstance(justifyContent, str) or justifyContent not in VALID_JUSTIFY:
            justifyContent = "flex-start"

        alignContent = _state_value(self._alignContent) or "flex-start"
        if not isinstance(alignContent, str) or alignContent not in VALID_ALIGN_CONTENT:
            alignContent = "flex-start"

        spacing = self._resolve_breakpoint_value(self._spacing, bp)
        spacing = _state_value(spacing) if spacing is not None else 0
        if isinstance(spacing, (int, float)):
            gap_px = int(round(spacing * 8))
        else:
            gap_px = 0

        sx = _state_value(self._sx) if self._sx is not None else {}
        sx = sx if isinstance(sx, dict) else {}
        if "gap" in sx:
            try:
                gap_px = int(sx["gap"])
            except Exception:
                pass
        if "flexDirection" in sx:
            fd = sx.get("flexDirection")
            if isinstance(fd, str) and fd in VALID_DIRECTIONS:
                direction = fd
        if "flexWrap" in sx:
            fw = sx.get("flexWrap")
            if isinstance(fw, str) and fw in VALID_FLEX_WRAP:
                flexWrap = fw
        if "justifyContent" in sx:
            jc = sx.get("justifyContent")
            if isinstance(jc, str) and jc in VALID_JUSTIFY:
                justifyContent = jc
        if "alignItems" in sx:
            ai = sx.get("alignItems")
            if isinstance(ai, str) and ai in VALID_ALIGN_ITEMS:
                alignItems = ai
        if "alignContent" in sx:
            ac = sx.get("alignContent")
            if isinstance(ac, str) and ac in VALID_ALIGN_CONTENT:
                alignContent = ac

        return {
            "direction": direction,
            "flexWrap": flexWrap,
            "gap": int(gap_px),
            "justifyContent": justifyContent,
            "alignItems": alignItems,
            "alignContent": alignContent,
            "margins": (0, 0, 0, 0),
        }

    def _connect_signals(self) -> None:
        _try_connect_state(self._spacing, self._on_layout_prop_changed)
        _try_connect_state(self._direction, self._on_layout_prop_changed)
        _try_connect_state(self._flexWrap, self._on_layout_prop_changed)
        _try_connect_state(self._alignItems, self._on_layout_prop_changed)
        _try_connect_state(self._justifyContent, self._on_layout_prop_changed)
        _try_connect_state(self._alignContent, self._on_layout_prop_changed)
        _try_connect_state(self._sx, self._on_sx_changed)
        _try_connect_state(self._variant, self._on_variant_changed)
        _try_connect_state(self._useFlexGap, self._on_layout_prop_changed)

    def _on_layout_prop_changed(self, *_):
        self.apply_layout()

    def _on_sx_changed(self, *_):
        v = _state_value(self._sx)
        self._sx_dict = v if isinstance(v, dict) else {}
        self.apply_layout()

    def _on_variant_changed(self, *_):
        self._apply_variant()

    def _apply_variant(self):
        v = _state_value(self._variant)
        if v not in VALID_VARIANTS:
            v = None
        self.setProperty("variant", "" if v is None else v)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def _init_children(self, children: Any) -> None:
        ch = _state_value(children) if children is not None else []
        if ch is None:
            ch = []
        if not isinstance(ch, list):
            ch = [ch]

        for idx, w in enumerate(ch):
            if w is None or not isinstance(w, QWidget):
                continue
            key = w.objectName() or f"child_{idx}_{id(w)}"
            sx = getattr(w, "_sx_dict", None) or getattr(w, "_sx", None)
            if _is_state(sx):
                sx = sx.value
            sx = sx if isinstance(sx, dict) else None
            self.addWidget(key, w, sx=sx, _from_children=True)

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, w: int) -> int:
        props = self._compute_props_dict()
        margins = props.get("margins", (0, 0, 0, 0))
        l, t, r, b = margins
        inner_w = max(0, int(w) - (l + r))
        content_h = self.engine.measure_height_for_width(inner_w, self._items, props)
        return int(content_h + t + b)

    def sizeHint(self) -> QSize:
        base_w = self.width() if self.width() > 0 else 240
        return QSize(base_w, self.heightForWidth(base_w))

    @staticmethod
    def _safe_item_sizes(w: QWidget) -> Tuple[QSize, QSize]:
        mw = max(0, int(w.minimumWidth()))
        mh = max(0, int(w.minimumHeight()))
        min_size = QSize(mw, mh)

        sh = w.sizeHint()
        sw = sh.width() if sh.width() > 0 else mw
        shh = sh.height() if sh.height() > 0 else mh
        size_hint = QSize(max(0, sw), max(0, shh))

        # IMPORTANT:
        # - Không “đóng băng” min_size theo width/height hiện tại của widget.
        # - Nếu làm vậy, flexShrink sẽ bị chặn (đặc biệt với nested Stack).
        # - Chỉ fallback cho size_hint khi cần.
        if size_hint.width() == 0 and w.width() > 0:
            size_hint = QSize(w.width(), size_hint.height())
        if size_hint.height() == 0 and w.height() > 0:
            size_hint = QSize(size_hint.width(), w.height())

        return size_hint, min_size

    @staticmethod
    def _parse_item_sx(sx: Optional[dict]) -> Tuple[int, int, int, Optional[str]]:
        if not sx:
            return 0, 0, 1, None
        order = int(sx.get("order", 0))
        fg = int(sx.get("flexGrow", 0))
        fs = int(sx.get("flexShrink", 1))
        al = sx.get("alignSelf")
        al = str(al) if al is not None else None
        return order, fg, fs, al

    def setSx(self, sx: dict) -> None:
        _validate_optional_dict("sx", sx)
        self._sx = sx
        self._sx_dict = sx
        self.apply_layout()

    def setProps(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if k == "spacing":
                _validate_optional_number_or_dict("spacing", v)
                self._spacing = v
            elif k == "direction":
                self._direction = v
            elif k == "flexWrap":
                self._flexWrap = v
            elif k in ("alignItems", "alignItem"):
                self._alignItems = v
            elif k == "justifyContent":
                self._justifyContent = v
            elif k == "alignContent":
                self._alignContent = v
            elif k == "variant":
                self._variant = v
                self._apply_variant()
            elif k == "sx":
                _validate_optional_dict("sx", v)
                self._sx = v
                self._sx_dict = v if isinstance(v, dict) else {}
        self.apply_layout()

    def addWidget(self, key: str, w: QWidget, *, sx: Optional[dict] = None, _from_children: bool = False) -> None:
        print('wg________________', w)
        if w.parent() is not self._container:
            w.setParent(self._container)
        w.show()

        if sx is None:
            sx = getattr(w, "_sx_dict", None)
            sx = sx if isinstance(sx, dict) else None

        if key in (k for k, _ in self._widgets):
            self.removeWidget(key)

        self._widgets.append((key, w))
        self._item_sx[key] = sx or {}

        size_hint, min_size = self._safe_item_sizes(w)
        order, fg, fs, al = self._parse_item_sx(sx)

        self._items.append(
            StackItem(
                key=key,
                size_hint=size_hint,
                min_size=min_size,
                flex_grow=max(0, int(fg)),
                flex_shrink=max(0, int(fs)),
                order=int(order),
                align_self=al,
            )
        )

        if not _from_children:
            self.apply_layout()

    def removeWidget(self, key: str) -> None:
        new_widgets: List[Tuple[str, QWidget]] = []
        new_items: List[StackItem] = []
        for (k, w), it in zip(self._widgets, self._items):
            if k == key:
                try:
                    w.setParent(None)
                except Exception:
                    pass
            else:
                new_widgets.append((k, w))
                new_items.append(it)
        self._widgets = new_widgets
        self._items = new_items
        self._item_sx.pop(key, None)
        self.apply_layout()

    def clear(self) -> None:
        for _, w in self._widgets:
            try:
                w.setParent(None)
            except Exception:
                pass
        self._widgets.clear()
        self._items.clear()
        self._item_sx.clear()
        self.apply_layout()

    def _sync_sizes(self) -> None:
        new_items: List[StackItem] = []
        for (key, w), _it in zip(self._widgets, self._items):
            size_hint, min_size = self._safe_item_sizes(w)
            sx = self._item_sx.get(key) or {}
            order, fg, fs, al = self._parse_item_sx(sx)
            new_items.append(
                StackItem(
                    key=key,
                    size_hint=size_hint,
                    min_size=min_size,
                    flex_grow=max(0, int(fg)),
                    flex_shrink=max(0, int(fs)),
                    order=int(order),
                    align_self=al,
                )
            )
        self._items = new_items

    def apply_layout(self) -> None:
        if not self._widgets:
            return

        # ✅ Guard: container chưa có geometry -> defer layout
        crect = self._container.rect()
        if crect.width() <= 0 or crect.height() <= 0:
            QTimer.singleShot(0, self.apply_layout)
            return

        props = self._compute_props_dict()
        self._sync_sizes()

        if self.auto_height:
            needed_h = self.heightForWidth(self.width())
            self.setMinimumHeight(needed_h)
            self.setMaximumHeight(needed_h)
            self.updateGeometry()

        rects = self.engine.compute(crect, self._items, props)
        for key, w in self._widgets:
            r = rects.get(key)
            if r is not None:
                w.setGeometry(r)


    def showEvent(self, e):
        super().showEvent(e)
        QTimer.singleShot(0, self.apply_layout)

    def eventFilter(self, obj, event):
        if obj is self._container and event.type() == QEvent.Resize:
            QTimer.singleShot(0, self.apply_layout)
        return super().eventFilter(obj, event)