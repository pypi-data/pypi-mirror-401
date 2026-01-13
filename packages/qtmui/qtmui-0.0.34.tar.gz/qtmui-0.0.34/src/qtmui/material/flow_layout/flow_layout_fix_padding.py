from typing import Optional, List
from PySide6.QtWidgets import QLayout, QWidget, QLayoutItem, QSizePolicy, QFrame
from PySide6.QtCore import Qt, QRect, QSize, QPoint, QMargins

class FlowLayout(QLayout):
    def __init__(
            self,
            parent=None,
            alignment=Qt.AlignmentFlag.AlignCenter,
            flexWrap: str = "wrap",
            alignItems="center",
            justifyContent="space-between",
            children: Optional[List[QWidget]] = None,
            sx=None
    ):
        super().__init__(parent)

        self.setAlignment(Qt.AlignmentFlag.AlignBaseline)
        self._parent = parent
        self._item_list = []
        self._flexWrap = flexWrap
        self._justifyContent = justifyContent
        self._alignItems = alignItems
        self._children = children
        self._laying_out = False
        
        init_sx = {"flexBasic": None, "flexGrow": 0, "flexShrink": 1, "padding": "8px"}
        if sx is not None and isinstance(sx, dict):
            init_sx.update(sx)
        self._sx = init_sx
        self._current_rect_width = 0
        self._init_ui()

        self.setSizeConstraint(QLayout.SetMinimumSize)
        self._parent.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def _init_ui(self):
        if self._parent is not None:
            margin = self.getPaddingFromSx()
            self.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
            print(f"Debug: _init_ui - contentsMargins set to {margin}")
            if self._parent.parent():
                print(f"Debug: _init_ui - parent.parent() size = {self._parent.parent().size().width()}x{self._parent.parent().size().height()}")

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
            print(f"Debug: addItem - Added widget {item.widget()}")
            if self._parent.parent():
                print(f"Debug: addItem - parent.parent() size = {self._parent.parent().size().width()}x{self._parent.parent().size().height()}")
            self.invalidate()

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
        return Qt.Orientation(Qt.Horizontal)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        left, top, right, bottom = self.getContentsMargins()
        effective_width = max(0, width - left - right)
        height = self._do_layout(QRect(0, 0, effective_width, 0), True)
        print(f"Debug: heightForWidth - input width={width}, effective_width={effective_width}, height={height + top + bottom}")
        if self._parent.parent():
            print(f"Debug: heightForWidth - parent.parent() size = {self._parent.parent().size().width()}x{self._parent.parent().size().height()}")
        return height + top + bottom

    def setGeometry(self, rect):
        if self._laying_out:
            print("Debug: setGeometry - Skipping due to reentrant call")
            return
        self._current_rect_width = rect.width()
        super().setGeometry(rect)
        self._do_layout(rect, False)
        print(f"Debug: setGeometry - rect={rect}, width={rect.width()}, height={rect.height()}")
        if self._parent.parent():
            print(f"Debug: setGeometry - parent.parent() size = {self._parent.parent().size().width()}x{self._parent.parent().size().height()}")

    def sizeHint(self):
        return self.minimumSize()

    def getPaddingFromSx(self):
        padding = 8
        if self._sx and isinstance(self._sx, dict):
            padding_value = self._sx.get("padding", 8)
            if isinstance(padding_value, (int, float)):
                padding = padding_value
            elif isinstance(padding_value, str) and padding_value.endswith("px"):
                try:
                    padding = int(padding_value[:-2])
                except ValueError:
                    padding = 8
        paddingTop = self._sx.get("padding-top", padding)
        paddingBottom = self._sx.get("padding-bottom", padding)
        paddingLeft = self._sx.get("padding-left", padding)
        paddingRight = self._sx.get("padding-right", padding)
        print(f"Debug: getPaddingFromSx - padding=(left={paddingLeft}, top={paddingTop}, right={paddingRight}, bottom={paddingBottom})")
        return (paddingLeft, paddingTop, paddingRight, paddingBottom)

    def _calculate_unwrapped_width(self):
        total = 0
        spacing = self.spacing()
        for item in self._item_list:
            widget = item.widget()
            if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
                total += widget.layout()._calculate_unwrapped_width()
            else:
                total += item.sizeHint().width()
            total += spacing
        total -= spacing if len(self._item_list) > 0 else 0
        return total

    def minimumSize(self):
        left, top, right, bottom = self.getContentsMargins()
        min_width = 0
        max_height = 0
        total_width_no_wrap = self._calculate_unwrapped_width()
        for item in self._item_list:
            widget = item.widget()
            item_width = item.sizeHint().width()
            item_height = item.sizeHint().height()
            if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
                item_width = widget.layout().minimumWidth()
                item_height = widget.layout().heightForWidth(item_width)
            min_width = max(min_width, item_width)
            max_height = max(max_height, item_height)
        min_width = max(min_width, total_width_no_wrap // len(self._item_list) if len(self._item_list) > 0 else 0)
        size = QSize(min_width + left + right, max_height + top + bottom)
        print(f"Debug: minimumSize - size={size.width()}x{size.height()}, total_width_no_wrap={total_width_no_wrap}")
        return size

    def minimumWidth(self):
        left, _, right, _ = self.getContentsMargins()
        min_width = 0
        total_width_no_wrap = self._calculate_unwrapped_width()
        for item in self._item_list:
            widget = item.widget()
            item_width = item.sizeHint().width()
            if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
                item_width = widget.layout().minimumWidth()
            min_width = max(min_width, item_width)
        min_width = max(min_width, total_width_no_wrap // len(self._item_list) if len(self._item_list) > 0 else 0)
        print(f"Debug: minimumWidth - min_width={min_width + left + right}, total_width_no_wrap={total_width_no_wrap}")
        return min_width + left + right

    def maximumWidth(self):
        if hasattr(self, '_is_calculating_max_width') and self._is_calculating_max_width:
            print("Debug: maximumWidth - Skipping recursive call")
            return 0
        self._is_calculating_max_width = True
        left, _, right, _ = self.getContentsMargins()
        total_width = self._calculate_unwrapped_width()
        max_width = total_width + left + right
        self._is_calculating_max_width = False
        print(f"Debug: maximumWidth - max_width={max_width}")
        return max_width

    def _find_nearest_flow_layouts(self, widget):
        flow_layouts = []
        non_flow_width = 0
        if not widget:
            return flow_layouts, non_flow_width

        if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
            flow_layouts.append(widget.layout())
        else:
            non_flow_width += widget.sizeHint().width()
        return flow_layouts, non_flow_width

    def setAlignmentMode(self, align):
        if align in ["flex-start", "center", "flex-end", "space-between", "space-around", "space-evenly"]:
            self._justifyContent = align
        else:
            raise ValueError("Alignment must be one of 'flex-start', 'center', 'flex-end', 'space-between', 'space-around', 'space-evenly'")

    def setVerticalAlignmentMode(self, vertical_align):
        if vertical_align in ["flex-start", "center", "flex-end", "baseline", "stretch"]:
            self._alignItems = vertical_align
        else:
            raise ValueError("Vertical alignment must be one of 'flex-start', 'center', 'flex-end', 'baseline', 'stretch'")

    def _get_baseline_offset(self, item):
        widget = item.widget()
        if not widget:
            return 0
        width = widget.width() if widget.width() > 0 else item.sizeHint().width()
        height = item.sizeHint().height()
        if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
            height = widget.layout().heightForWidth(width)
        return height

    def _get_basis(self, item):
        widget = item.widget()
        basis = widget._sx.get("flexBasic") if hasattr(widget, '_sx') and widget._sx else None
        return basis if basis is not None else item.sizeHint().width()

    def _get_prop(self, item, name):
        widget = item.widget()
        val = widget._sx.get(name) if hasattr(widget, '_sx') and widget._sx else 0
        return int(val) if isinstance(val, (int, float)) else 0

    def _do_layout(self, rect, test_only):
        if self._laying_out:
            print("Debug: _do_layout - Skipping due to reentrant call")
            return 0
        self._laying_out = True

        left, top, right, bottom = self.getContentsMargins()
        effective_rect = QRect(rect.x() + left, rect.y() + top, rect.width() - left - right, max(0, rect.height() - top - bottom))
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0
        spacing = self.spacing()
        line_widgets = []
        line_baseline_info = []
        available_width = effective_rect.width()
        current_line_width = 0
        temp_max_width = self._calculate_unwrapped_width()

        print(f"Debug: _do_layout - rect={rect}, effective_rect={effective_rect}, margins=(left={left}, top={top}, right={right}, bottom={bottom})")
        print(f"Debug: _do_layout - flow_layout available_width={available_width}, temp_max_width={temp_max_width}")
        if self._parent.parent():
            print(f"Debug: _do_layout - parent.parent() size = {self._parent.parent().size().width()}x{self._parent.parent().size().height()}")

        for item in self._item_list:
            widget = item.widget()
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Giãn width cho widget con
            item_width = max(item.minimumSize().width(), available_width - current_line_width)
            item_height = item.sizeHint().height()
            if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
                sub_unwrapped_width = widget.layout()._calculate_unwrapped_width()
                item_width = max(widget.layout().minimumWidth(), min(available_width - current_line_width, sub_unwrapped_width))
                item_height = widget.layout().heightForWidth(item_width)
                if not test_only:
                    widget.layout()._do_layout(QRect(0, 0, item_width, item_height), False)

            next_x = current_line_width + item_width
            if self._flexWrap == "wrap" and next_x > available_width and line_widgets:
                self._align_line(line_widgets, line_baseline_info, effective_rect.x(), available_width, y, line_height, effective_rect.height(), test_only)
                y += line_height + spacing
                x = effective_rect.x()
                line_widgets = []
                line_baseline_info = []
                line_height = 0
                current_line_width = 0

            line_widgets.append((item, QPoint(x + current_line_width, y)))
            current_line_width += item_width + spacing
            line_height = max(line_height, item_height)
            line_baseline_info.append(item_height)

            print(f"Debug: _do_layout - widget {widget} at (x={x + current_line_width - item_width - spacing}, y={y}), width={item_width}, height={item_height}")

        if line_widgets:
            self._align_line(line_widgets, line_baseline_info, effective_rect.x(), available_width, y, line_height, effective_rect.height(), test_only)

        total_height = y + line_height - effective_rect.y()
        print(f"Debug: _do_layout - total_height={total_height}, effective_rect.height={effective_rect.height()}")

        if self._alignItems == "center" and not test_only:
            y_offset = (effective_rect.height() - total_height) // 2 if effective_rect.height() > total_height else 0
            for item in self._item_list:
                geom = item.geometry()
                item.setGeometry(geom.translated(0, y_offset))
                print(f"Debug: _do_layout - Adjusted widget {item.widget()} to y={geom.y() + y_offset}")

        self._laying_out = False
        return total_height

    def _align_line(self, line_widgets, baseline_offsets, start_x, total_width, y, line_height, total_height, test_only):
        spacing = self.spacing()
        count = len(line_widgets)
        total_spacing = spacing * (count - 1)
        line_width = 0
        for item, _ in line_widgets:
            line_width += item.sizeHint().width()
        line_width += total_spacing

        offset_x = 0
        extra_space = 0
        if self._justifyContent == "center":
            offset_x = (total_width - line_width) // 2 if total_width >= line_width else 0
        elif self._justifyContent == "flex-end":
            offset_x = total_width - line_width if total_width >= line_width else 0
        elif self._justifyContent == "space-between" and count > 1:
            extra_space = (total_width - line_width) // (count - 1) if total_width >= line_width else 0
        elif self._justifyContent == "space-around" and count > 0:
            extra_space = (total_width - line_width) // (count * 2) if total_width >= line_width else 0
            offset_x = extra_space
        elif self._justifyContent == "space-evenly" and count > 0:
            extra_space = (total_width - line_width) // (count + 1) if total_width >= line_width else 0
            offset_x = extra_space

        current_x = start_x + offset_x
        for i, (item, _) in enumerate(line_widgets):
            widget = item.widget()
            width = item.sizeHint().width()
            height = item.sizeHint().height()
            if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
                width = widget.layout().maximumWidth()
                height = widget.layout().heightForWidth(width)

            if self._alignItems == "center":
                offset_y = (line_height - height) // 2
            elif self._alignItems == "flex-end":
                offset_y = line_height - height
            else:
                offset_y = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(current_x, y + offset_y), QSize(width, height)))
                print(f"Debug: _align_line - widget {widget} set to geometry=(x={current_x}, y={y + offset_y}, width={width}, height={height})")

            current_x += width + spacing + extra_space

class FlowContainer(QFrame):
    def __init__(self, children):
        super().__init__()
        self.layout = FlowLayout(self, sx={"padding": "8px"})
        self.setLayout(self.layout)
        if not isinstance(children, list):
            raise TypeError(f"Argument 'children' has incorrect type (expected list, got {type(children)})")
        for widget in children:
            self.layout.addWidget(widget)