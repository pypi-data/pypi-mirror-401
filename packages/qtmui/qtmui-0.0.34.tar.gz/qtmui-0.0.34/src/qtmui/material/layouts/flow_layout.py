from typing import Optional, List, Tuple, Dict
from PySide6.QtWidgets import QLayout, QWidget, QLayoutItem
from PySide6.QtCore import Qt, QRect, QSize, QPoint, QMargins


class FlowLayout(QLayout):
    def __init__(
        self,
        parent=None,
        name="None",
        spacing: int=6,
        margin: tuple=(0,0,0,0),
        flexWrap: str = "wrap",
        alignItems="center",
        justifyContent="space-between",
        children: Optional[List[QWidget]] = None,
        sx=None
    ):
        super().__init__(parent)

        self._name = name
        self._spacing = spacing
        self._margin = margin
        self._onLayout = None
        self._is_calculating_max_width = False

        self.setAlignment(Qt.AlignmentFlag.AlignBaseline)
        self._parent = parent
        self._item_list: List[QLayoutItem] = []
        self._flexWrap = flexWrap
        self._justifyContent = justifyContent
        self._alignItems = alignItems
        self._children = children

        init_sx = {"flexBasic": None, "flexGrow": 0, "flexShrink": 1}
        if sx is not None and isinstance(sx, dict):
            init_sx.update(sx)
        self._sx = init_sx

        self._current_rect_width = 0
        self._init_ui()

    def _init_ui(self):
        if self._parent is not None:
            if self._margin:
                self.setContentsMargins(QMargins(*self._margin))
            else:
                self.setContentsMargins(QMargins(0,0,0,0))
            self.setSpacing(self._spacing)

        if self._children:
            for widget in self._children:
                if isinstance(widget, QWidget):
                    self.addWidget(widget)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        if item:
            self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._do_layout(QRect(0, 0, width, 0), True)
        ##print(f"Debug:: [{self._name}] :: heightForWidth({width}) = {height}")
        return height

    def setGeometry(self, rect):
        ##print(f"Debug:: [{self._name}] :: setGeometry called with rect={rect}")
        self._current_rect_width = rect.width()
        super().setGeometry(rect)
        try:
            self._do_layout(rect, False)
        except Exception as e:
            print(e)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        min_width = 0
        max_height = 0
        for item in self._item_list:
            widget = item.widget()
            flow_layouts, non_flow_width = self._find_nearest_flow_layouts(widget)
            if flow_layouts:
                for flow_layout in flow_layouts:
                    item_min_width = flow_layout.minimumWidth()
                    min_width = max(min_width, item_min_width + non_flow_width)
            else:
                if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx, dict):
                    width_value = widget._sx.get("width")
                    if isinstance(width_value, str) and width_value.endswith("%"):
                        item_min_width = widget.sizeHint().width()
                    else:
                        item_min_width = item.minimumSize().width()
                else:
                    item_min_width = item.minimumSize().width()
                min_width = max(min_width, item_min_width)

            max_height = max(max_height, item.minimumSize().height())

        size = QSize(min_width, max_height)
        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        ##print(f"Debug:: [{self._name}] :: minimumSize() = {size}")
        return size

    def minimumWidth(self):
        min_width = 0
        for item in self._item_list:
            widget = item.widget()
            flow_layouts, non_flow_width = self._find_nearest_flow_layouts(widget)
            if flow_layouts:
                for flow_layout in flow_layouts:
                    item_min_width = flow_layout.minimumWidth()
                    min_width = max(min_width, item_min_width + non_flow_width)
            else:
                if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx, dict):
                    width_value = widget._sx.get("width")
                    if isinstance(width_value, str) and width_value.endswith("%"):
                        item_min_width = widget.sizeHint().width()
                    else:
                        item_min_width = item.minimumSize().width()
                else:
                    item_min_width = item.minimumSize().width()
                min_width = max(min_width, item_min_width)

        m = self.contentsMargins()
        min_width += (m.left() + m.right())
        ##print(f"Debug:: [{self._name}] :: minimumWidth() = {min_width}")
        return min_width

    def _effective_widget_width(self, w: Optional[QWidget], *, ctx: str = "") -> int:
        if not w:
            return 0

        gw = w.width()
        mw = w.minimumSize().width()
        sh = w.sizeHint().width()
        msh = w.minimumSizeHint().width()

        # if sh <= 0 or msh <= 0 or mw < 0:
        #     try:
        #         print(
        #             f"Debug:: [{self._name}] :: _effective_widget_width{('('+ctx+')' if ctx else '')} "
        #             f"widget={w.__class__.__name__}#{w.objectName() or id(w)} "
        #             f"geom_w={gw} min_w={mw} sizeHint_w={sh} minHint_w={msh}"
        #         )
        #     except Exception:
        #         pass

        if gw and gw > 0:
            return int(gw)
        if mw and mw > 0:
            return int(mw)
        if sh and sh > 0:
            return int(sh)
        if msh and msh > 0:
            return int(msh)
        return 0

    def maximumWidth(self):
        if self._is_calculating_max_width:
            return 0

        self._is_calculating_max_width = True
        total = 0
        spacing = self.spacing()

        for i, item in enumerate(self._item_list):
            w = item.widget()
            if not w:
                continue

            if hasattr(w, "layout") and isinstance(w.layout(), FlowLayout):
                child_layout: "FlowLayout" = w.layout()
                w_width = child_layout.maximumWidth()
            else:
                w_width = self._effective_widget_width(w, ctx="maximumWidth.leaf")

            total += max(0, int(w_width))
            if i > 0:
                total += spacing

        m = self.contentsMargins()
        total += (m.left() + m.right())

        self._is_calculating_max_width = False
        ##print(f"Debug:: [{self._name}] :: maximumWidth() = {total}")
        ##print(f"Debug:: [{self._name}] :: maximumWidth() FIXED one-line = {total}")
        return total

    def _find_nearest_flow_layouts(self, widget):
        flow_layouts: List["FlowLayout"] = []
        non_flow_width = 0

        if not widget:
            return flow_layouts, non_flow_width

        if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
            flow_layouts.append(widget.layout())

        elif hasattr(widget, 'layout') and widget.layout():
            for i in range(widget.layout().count()):
                child_item = widget.layout().itemAt(i)
                if child_item and child_item.widget():
                    child_flow_layouts, child_non_flow_width = self._find_nearest_flow_layouts(child_item.widget())
                    flow_layouts.extend(child_flow_layouts)

                    non_flow_width += max(0, int(child_non_flow_width))

                    if i > 0:
                        non_flow_width += self.spacing()

        else:
            non_flow_width += self._effective_widget_width(widget, ctx="find.leaf")

        return flow_layouts, non_flow_width

    def setAlignmentMode(self, align):
        if align in ["flex-start", "center", "flex-end", "space-between", "space-around", "space-evenly"]:
            self._justifyContent = align
        else:
            raise ValueError(
                "Alignment must be 'flex-start', 'center', 'flex-end', 'space-between', 'space-around', or 'space-evenly'"
            )

    def setVerticalAlignmentMode(self, vertical_align):
        if vertical_align in ["flex-start", "center", "flex-end", "baseline", "stretch"]:
            self._alignItems = vertical_align
        else:
            raise ValueError(
                "Vertical alignment must be 'flex-start', 'center', 'flex-end', 'baseline' or 'stretch'"
            )

    def _get_prop(self, item, name):
        widget = item.widget()
        if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
            val = widget.layout()._sx.get(name)
        else:
            val = widget._sx.get(name) if hasattr(widget, '_sx') and (widget._sx is not None and widget._sx != "") else 0
        return int(val) if isinstance(val, (int, float)) else 0

    def _do_layout(self, rect: QRect, test_only: bool) -> int:
        spacing = self.spacing()

        m = self.contentsMargins()
        eff = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())

        if eff.height() < 0:
            eff = QRect(eff.x(), eff.y(), eff.width(), 0)

        ##print(f"Debug:: [{self._name}] :: _do_layout:: eff = {eff}")

        x = eff.x()
        y = eff.y()

        line_height = 0
        line_widgets: List[Tuple[QLayoutItem, QPoint, QSize]] = []

        payload_lines: List[List[str]] = []
        payload_items: Dict[str, QRect] = {}

        def _key(w: QWidget) -> str:
            return w.objectName() or str(id(w))

        def flush_line():
            nonlocal x, y, line_height, line_widgets
            if not line_widgets:
                return

            self._align_line(line_widgets, eff.x(), eff.width(), y, test_only)

            keys: List[str] = []
            for it, _pos, _sz in line_widgets:
                wdg = it.widget()
                k = _key(wdg) if wdg else "None"
                keys.append(k)
                if not test_only:
                    payload_items[k] = QRect(it.geometry())
            payload_lines.append(keys)

            y += line_height + spacing
            x = eff.x()
            line_height = 0
            line_widgets = []

        for item in self._item_list:
            wdg = item.widget()
            if not wdg:
                continue

            flow_layouts, non_flow_width = self._find_nearest_flow_layouts(wdg)

            if flow_layouts:
                # --- FIX A: pre-wrap trước khi đo, tránh available_inner=0 làm đo sai ---
                remaining_width = eff.width() - (x - eff.x())

                # min_required_inner = max(minimumWidth of each flow layout) vì wrapper cần đáp ứng tối thiểu của nội dung
                # (minimumWidth đã bao gồm margins trái/phải của chính layout con)
                try:
                    min_required_inner = 0
                    for fl in flow_layouts:
                        min_required_inner = max(min_required_inner, max(0, int(fl.minimumWidth())))
                except Exception:
                    min_required_inner = 0

                min_required_total = max(0, int(non_flow_width)) + min_required_inner

                if line_widgets and remaining_width < min_required_total:
                    # try:
                    #     print(
                    #         f"Debug:: [{self._name}] :: pre-wrap BEFORE measure item={_key(wdg)} "
                    #         f"remaining_width={remaining_width} min_required_total={min_required_total} "
                    #         f"(non_flow={non_flow_width}, min_inner={min_required_inner})"
                    #     )
                    # except Exception:
                    #     pass
                    flush_line()
                    remaining_width = eff.width() - (x - eff.x())

                available_inner = remaining_width - non_flow_width
                if available_inner < 0:
                    available_inner = 0
                if available_inner > eff.width():
                    available_inner = eff.width()

                max_outer_w = 0
                max_inner_h = 0

                for fl in flow_layouts:
                    one_line_outer = max(0, int(fl.maximumWidth()))
                    min_outer = max(0, int(fl.minimumWidth()))

                    # --- FIX B: luôn clamp theo available_inner (kể cả =0) ---
                    content_outer = min(one_line_outer, available_inner)
                    if content_outer < min_outer:
                        content_outer = min_outer

                    ask_outer = content_outer

                    inner_h = fl.heightForWidth(ask_outer) if fl.hasHeightForWidth() else fl.sizeHint().height()
                    if inner_h <= 0:
                        inner_h = fl.minimumSize().height()
                        if inner_h <= 0:
                            inner_h = 1

                    max_outer_w = max(max_outer_w, content_outer)
                    max_inner_h = max(max_inner_h, inner_h)

                    # try:
                    #     print(
                    #         f"Debug:: [{self._name}] :: flow-child={getattr(fl, '_name', 'child')} "
                    #         f"one_line_outer={one_line_outer} min_outer={min_outer} available_inner={available_inner} "
                    #         f"content_outer={content_outer} ask_outer={ask_outer} => inner_h={inner_h}"
                    #     )
                    # except Exception:
                    #     pass

                item_width = non_flow_width + max_outer_w
                item_height = max_inner_h

                if not test_only:
                    wdg.resize(item_width, item_height)

            else:
                item_width = item.sizeHint().width()
                item_height = item.sizeHint().height()
                if item_height <= 0:
                    item_height = 1

                if not test_only:
                    wdg.resize(item_width, item_height)

            measured_size = QSize(int(item_width), int(item_height))

            # try:
            #     print(
            #         f"Debug:: [{self._name}] :: measure item={_key(wdg)} "
            #         f"flow={'Y' if flow_layouts else 'N'} non_flow_width={non_flow_width} "
            #         f"measured=({measured_size.width()}x{measured_size.height()}) "
            #         f"cursor_x={x - eff.x()} eff_w={eff.width()}"
            #     )
            # except Exception:
            #     pass

            next_x = x + measured_size.width()
            if next_x > (eff.x() + eff.width()) and line_widgets:
                flush_line()

            line_widgets.append((item, QPoint(x, y), measured_size))

            x += measured_size.width() + spacing
            line_height = max(line_height, measured_size.height())

        if line_widgets:
            self._align_line(line_widgets, eff.x(), eff.width(), y, test_only)

            keys: List[str] = []
            for it, _pos, _sz in line_widgets:
                wdg = it.widget()
                k = _key(wdg) if wdg else "None"
                keys.append(k)
                if not test_only:
                    payload_items[k] = QRect(it.geometry())
            payload_lines.append(keys)

        total_height = (y + line_height) - eff.y()
        total_height += (m.top() + m.bottom())

        if (not test_only) and self._onLayout:
            payload = {
                "rect": QRect(rect),
                "props": {
                    "align": getattr(self, "_align", None),
                    "justifyContent": getattr(self, "_justifyContent", None),
                    "spacing": spacing,
                    "margins": (m.left(), m.top(), m.right(), m.bottom()),
                    "items": len(self._item_list),
                },
                "lines": payload_lines,
                "items": payload_items,
            }
            try:
                self._onLayout(payload)
            except Exception:
                pass

        return total_height

    def _align_line(
        self,
        line_widgets: List[Tuple[QLayoutItem, QPoint, QSize]],
        start_x: int,
        total_width: int,
        y: int,
        test_only: bool
    ):
        spacing = self.spacing()
        count = len(line_widgets)
        total_spacing = spacing * (count - 1)

        widths: List[int] = []
        heights: List[int] = []

        line_height = 0
        
        for i, (item, _pos, measured) in enumerate(line_widgets):
            widget = item.widget()
            w = measured.width()
            h = measured.height()

            line_height = max(line_height, h)
            
            if (
                hasattr(widget, '_sx')
                and widget._sx
                and isinstance(widget._sx.get("width"), str)
                and widget._sx.get("width").endswith("%")
            ):
                try:
                    percentage = float(widget._sx.get("width").strip("%"))
                    if 0 <= percentage <= 100:
                        w = int(total_width * (percentage / 100))
                except (ValueError, TypeError):
                    pass

            widths.append(int(w))
            heights.append(int(h))

        line_width = sum(widths) + total_spacing
        offset_x = 0
        extra_space = 0

        if self._justifyContent == "center":
            offset_x = (total_width - line_width) // 2 if total_width >= line_width else 0
        elif self._justifyContent == "flex-end":
            offset_x = total_width - line_width if total_width >= line_width else 0
        elif self._justifyContent == "space-between" and count > 1:
            extra_space = (total_width - line_width) // (count - 1) if total_width >= line_width else 0
            offset_x = 0
        elif self._justifyContent == "space-around" and count > 0:
            space = (total_width - line_width) // (count * 2) if total_width >= line_width else 0
            offset_x = space
            extra_space = space * 2
        elif self._justifyContent == "space-evenly" and count > 0:
            space = (total_width - line_width) // (count + 1) if total_width >= line_width else 0
            offset_x = space
            extra_space = space
        else:
            offset_x = 0

        current_x = start_x + offset_x

        for i, (item, _pos, _measured) in enumerate(line_widgets):
            width = widths[i]
            height = heights[i]
            offset_y = 0

            if self._alignItems == "center":
                offset_y = max(0, (line_height - height) // 2)
            elif self._alignItems == "flex-end":
                offset_y = max(0, line_height - height)
            else:
                offset_y = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(current_x, y + offset_y), QSize(width, height)))

            current_x += width + spacing
            if self._justifyContent in ["space-between", "space-around", "space-evenly"] and (
                (self._justifyContent != "space-between") or i < count - 1
            ):
                current_x += extra_space
