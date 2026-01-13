from typing import Optional, List
from PySide6.QtWidgets import QLayout, QWidget, QLayoutItem, QLabel, QPushButton, QFrame, QSizePolicy
from PySide6.QtCore import Qt, QRect, QSize, QPoint, QMargins

# Định nghĩa lớp FlowLayout kế thừa từ QLayout để tạo layout tùy chỉnh
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
        init_sx = {"flexBasic": None, "flexGrow": 0, "flexShrink": 1}
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
        if self._children:
            for widget in self._children:
                if isinstance(widget, QWidget):
                    self.addWidget(widget)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

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
        # print(f"Debug: heightForWidth({width}) = {height}")
        return height

    def setGeometry(self, rect):
        # print(f"Debug: setGeometry called with rect={rect}")
        self._current_rect_width = rect.width()
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        left, top, right, bottom = self.getContentsMargins()
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
                # Kiểm tra nếu widget có width dạng % trong _sx
                if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx, dict):
                    width_value = widget._sx.get("width")
                    if isinstance(width_value, str) and width_value.endswith("%"):
                        # Sử dụng kích thước tối thiểu thực sự của widget, không dựa trên setMinimumWidth
                        item_min_width = widget.sizeHint().width()
                    else:
                        item_min_width = item.minimumSize().width()
                else:
                    item_min_width = item.minimumSize().width()
                min_width = max(min_width, item_min_width)
            max_height = max(max_height, item.minimumSize().height())

        size = QSize(min_width + left + right, max_height + top + bottom)
        # print(f"Debug: minimumSize() = {size}")
        return size

    def minimumWidth(self):
        min_width = 0
        left, _, right, _ = self.getContentsMargins()
        
        for item in self._item_list:
            widget = item.widget()
            flow_layouts, non_flow_width = self._find_nearest_flow_layouts(widget)
            if flow_layouts:
                for flow_layout in flow_layouts:
                    item_min_width = flow_layout.minimumWidth()
                    min_width = max(min_width, item_min_width + non_flow_width)
            else:
                # Kiểm tra nếu widget có width dạng % trong _sx
                if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx, dict):
                    width_value = widget._sx.get("width")
                    if isinstance(width_value, str) and width_value.endswith("%"):
                        # Sử dụng kích thước tối thiểu thực sự của widget
                        item_min_width = widget.sizeHint().width()
                    else:
                        item_min_width = item.minimumSize().width()
                else:
                    item_min_width = item.minimumSize().width()
                min_width = max(min_width, item_min_width)
        # print(f"Debug: minimumWidth() = {min_width}")
        return min_width + left + right


    def maximumWidth(self):
        if self._is_calculating_max_width:
            return 0  # Tránh đệ quy bằng cách trả về giá trị mặc định

        self._is_calculating_max_width = True
        total_width = 0
        for i, item in enumerate(self._item_list):
            widget = item.widget()
            flow_layouts, non_flow_width = self._find_nearest_flow_layouts(widget)
            width = non_flow_width
            if flow_layouts:
                for flow_layout in flow_layouts:
                    temp_width = 0
                    for sub_item in flow_layout._item_list:
                        sub_widget = sub_item.widget()
                        temp_width += sub_widget.sizeHint().width()
                        temp_width += flow_layout.spacing()
                    temp_width -= flow_layout.spacing()
                    width += temp_width
            else:
                # Kiểm tra nếu widget có width dạng % trong _sx
                if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx, dict):
                    width_value = widget._sx.get("width")
                    if isinstance(width_value, str) and width_value.endswith("%"):
                        try:
                            percentage = float(width_value.strip("%"))
                            if 0 <= percentage <= 100:
                                # Sử dụng current_rect_width nếu có, nếu không thì dùng sizeHint
                                parent_width = self._current_rect_width if self._current_rect_width > 0 else widget.sizeHint().width()
                                width = int(parent_width * (percentage / 100))
                        except (ValueError, TypeError):
                            width += item.sizeHint().width()
                    else:
                        width += item.sizeHint().width()
                else:
                    width += item.sizeHint().width()
            total_width += width
            if i > 0:
                total_width += self.spacing()
        self._is_calculating_max_width = False
        # print(f"Debug: maximumWidth() = {total_width}")
        left, _, right, _ = self.getContentsMargins()
        max_width = total_width + left + right
        
        return max_width

    def _find_nearest_flow_layouts(self, widget):
        flow_layouts = []
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
                    non_flow_width += child_non_flow_width
                    if i > 0:
                        non_flow_width += self.spacing()
        else:
            non_flow_width += widget.sizeHint().width()

        return flow_layouts, non_flow_width

    def setAlignmentMode(self, align):
        if align in ["flex-start", "center", "flex-end", "space-between", "space-around", "space-evenly"]:
            self._justifyContent = align
        else:
            raise ValueError("Alignment must be 'flex-start', 'center', 'flex-end', 'space-between', 'space-around', or 'space-evenly'")

    def setVerticalAlignmentMode(self, vertical_align):
        if vertical_align in ["flex-start", "center", "flex-end", "baseline", "stretch"]:
            self._alignItems = vertical_align
        else:
            raise ValueError("Vertical alignment must be 'flex-start', 'center', 'flex-end', 'baseline' or 'stretch'")

    def _get_baseline_offset(self, item):
        widget = item.widget()
        if not widget:
            return 0
        width = widget.width() if widget.width() > 0 else item.sizeHint().width()
        height = (widget.layout().heightForWidth(width)
                  if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout)
                  else item.sizeHint().height())
        return height

    def _get_basis(self, item):
        widget = item.widget()
        if widget:
            if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
                basis = widget.layout()._sx.get("flexBasic")
            else:
                basis = widget._sx.get("flexBasic") if hasattr(widget, '_sx') and (widget._sx is not None and widget._sx != "") else None
        return basis if basis is not None else item.sizeHint().width()

    def _get_prop(self, item, name):
        widget = item.widget()
        if hasattr(widget, 'layout') and isinstance(widget.layout(), FlowLayout):
            val = widget.layout()._sx.get(name)
        else:
            val = widget._sx.get(name) if hasattr(widget, '_sx') and (widget._sx is not None and widget._sx != "") else 0
        return int(val) if isinstance(val, (int, float)) else 0

    def _do_layout(self, rect, test_only):
        
        left, top, right, bottom = self.getContentsMargins()
        effective_rect = QRect(rect.x() + left, rect.y() + top, rect.width() - left - right, max(0, rect.height() - top - bottom))
        x = effective_rect.x()
        y = effective_rect.y()
        
        line_height = 0
        spacing = self.spacing()
        line_widgets = []
        line_baseline_info = []
        

        # Duyệt qua từng item để cập nhật chiều rộng dạng % nếu có
        for item in self._item_list:
            widget = item.widget()
            if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx, dict):
                width_value = widget._sx.get("width")
                if isinstance(width_value, str) and width_value.endswith("%"):
                    try:
                        percentage = float(width_value.strip("%"))
                        if 0 <= percentage <= 100:
                            widget._percentage_width = int(rect.width() * (percentage / 100))
                    except (ValueError, TypeError):
                        pass

        # Duyệt qua từng item để sắp xếp
        for item in self._item_list:
            widget = item.widget()
            percentage_width = getattr(widget, '_percentage_width', None)

            # Tính chiều rộng và chiều cao của item
            flow_layouts, non_flow_width = self._find_nearest_flow_layouts(widget)
            if flow_layouts:
                max_width = non_flow_width
                total_height = 0
                for flow_layout in flow_layouts:
                    if not test_only:
                        # flow_layout.setAlignmentMode(flow_layout._justifyContent)
                        flow_layout.setAlignmentMode("flex-start") # thay đổi này làm cho hết lỗi khi Stack cha space-around-between
                        flow_layout.setVerticalAlignmentMode(flow_layout._alignItems)

                    temp_max_width = 0
                    for sub_item in flow_layout._item_list:
                        sub_widget = sub_item.widget()
                        temp_max_width += sub_widget.sizeHint().width()
                        temp_max_width += flow_layout.spacing()
                    temp_max_width -= flow_layout.spacing()
                    flex_shrink = flow_layout._sx.get("flexShrink", 1)

                    remaining_width = rect.width() - (x - rect.x())
                    available_width = min(rect.width(), remaining_width - non_flow_width)

                    if flow_layout._flexWrap == "wrap" and (temp_max_width > rect.width() or temp_max_width > available_width):
                        temp_width = available_width
                        temp_x = 0
                        temp_y = 0
                        temp_line_width = 0
                        temp_max_line_width = 0
                        temp_line_height = 0
                        temp_line_widgets = []
                        temp_line_baselines = []

                        for sub_item in flow_layout._item_list:
                            sub_widget = sub_item.widget()
                            sub_width = sub_item.sizeHint().width()
                            sub_height = sub_item.sizeHint().height()

                            if temp_x + sub_width > temp_width:
                                if temp_line_widgets:
                                    flow_layout._align_line(temp_line_widgets, temp_line_baselines, 0, temp_width, temp_y, temp_line_height, rect.height(), test_only)
                                    temp_max_line_width = max(temp_max_line_width, temp_line_width)
                                temp_y += temp_line_height + spacing
                                temp_x = 0
                                temp_line_width = 0
                                temp_line_height = 0
                                temp_line_widgets = []
                                temp_line_baselines = []

                            if temp_x > 0:
                                temp_x += spacing
                                temp_line_width += spacing
                            temp_line_width += sub_width
                            temp_x += sub_width
                            temp_line_height = max(temp_line_height, sub_height)
                            temp_line_widgets.append((sub_item, QPoint(temp_x - sub_width, temp_y)))
                            temp_line_baselines.append(sub_height)

                        if temp_line_widgets:
                            flow_layout._align_line(temp_line_widgets, temp_line_baselines, 0, temp_width, temp_y, temp_line_height, rect.height(), test_only)
                            temp_max_line_width = max(temp_max_line_width, temp_line_width)
                            temp_y += temp_line_height
                        temp_width = temp_max_line_width
                        temp_height = temp_y
                    else:
                        if flex_shrink > 0 and temp_max_width > available_width and available_width > 0:
                            temp_width = available_width
                            temp_height = flow_layout.heightForWidth(temp_width)
                            if not test_only:
                                flow_layout._do_layout(QRect(0, 0, temp_width, 0), False)
                        else:
                            temp_x = 0
                            temp_y = 0
                            temp_line_width = 0
                            temp_max_line_width = 0
                            temp_line_height = 0
                            temp_line_widgets = []
                            temp_line_baselines = []

                            for sub_item in flow_layout._item_list:
                                sub_widget = sub_item.widget()
                                sub_width = sub_item.sizeHint().width()
                                sub_height = sub_item.sizeHint().height()

                                if temp_x > 0:
                                    temp_x += spacing
                                    temp_line_width += spacing
                                temp_line_width += sub_width
                                temp_x += sub_width
                                temp_line_height = max(temp_line_height, sub_height)
                                temp_line_widgets.append((sub_item, QPoint(temp_x - sub_width, temp_y)))
                                temp_line_baselines.append(sub_height)

                            if temp_line_widgets:
                                flow_layout._align_line(temp_line_widgets, temp_line_baselines, 0, available_width, temp_y, temp_line_height, rect.height(), test_only)
                                temp_max_line_width = max(temp_max_line_width, temp_line_width)
                                temp_y += temp_line_height
                            temp_width = temp_max_line_width
                            temp_height = temp_y

                    max_width = max(max_width, temp_width)
                    total_height = max(total_height, temp_height)

                item_width = max_width + non_flow_width
                item_height = total_height

                if not test_only:
                    widget.setMinimumWidth(item_width)
                    widget.setMaximumWidth(item_width)
                    if self._alignItems == "stretch":
                        widget.setMinimumHeight(rect.height())
                        widget.setMaximumHeight(rect.height())
                        for flow_layout in flow_layouts:
                            flow_layout._do_layout(QRect(0, 0, item_width - non_flow_width, rect.height()), False)
                    else:
                        widget.setMinimumHeight(item_height)
                        widget.setMaximumHeight(item_height)
                    widget.resize(item_width, item_height)
            else:
                item_width = item.sizeHint().width() if percentage_width is None else percentage_width
                item_height = item.sizeHint().height()
                if percentage_width is not None and not test_only:
                    widget.setMinimumWidth(item_width)
                    widget.setMaximumWidth(item_width)

            # Kiểm tra wrap trước khi cập nhật x
            next_x = x + item_width
            if percentage_width is not None or (self._flexWrap == "wrap" and next_x > rect.x() + rect.width() and line_widgets):
                if line_widgets:
                    self._align_line(line_widgets, line_baseline_info, rect.x(), rect.width(), y, line_height, rect.height(), test_only)
                    y += line_height + spacing
                    x = rect.x()
                    line_widgets = []
                    line_baseline_info = []
                    line_height = 0

            # Thêm item vào dòng hiện tại và cập nhật line_height
            line_widgets.append((item, QPoint(x, y)))
            x += item_width + spacing
            baseline_offset = self._get_baseline_offset(item)
            line_baseline_info.append(baseline_offset)
            line_height = max(line_height, item_height)

        if line_widgets:
            self._align_line(line_widgets, line_baseline_info, rect.x(), rect.width(), y, line_height, rect.height(), test_only)

        total_height = y + line_height - effective_rect.y()

        if self._alignItems == "center":
            y_offset = (rect.height() - total_height) // 2
        elif self._alignItems == "flex-end":
            y_offset = rect.height() - total_height
        else:
            y_offset = 0

        if not test_only and y_offset > 0:
            for item in self._item_list:
                geom = item.geometry()
                item.setGeometry(geom.translated(0, y_offset))

        return total_height

    def _align_line(self, line_widgets, baseline_offsets, start_x, total_width, y, line_height, total_height, test_only):
        spacing = self.spacing()
        count = len(line_widgets)
        total_spacing = spacing * (count - 1)
        bases = [self._get_basis(item) for item, _ in line_widgets]
        grows = [self._get_prop(item, "flexGrow") for item, _ in line_widgets]
        shrinks = [self._get_prop(item, "flexShrink") for item, _ in line_widgets]
        total_basis = sum(bases)

        # print(f"Debug: total_width={total_width}, total_basis={total_basis}, total_spacing={total_spacing}")
        # print(f"Debug: bases={bases}, grows={grows}, shrinks={shrinks}")

        fixed_total = 0
        flex_total = 0
        shrink_total = 0
        widths = []

        for i, (item, _) in enumerate(line_widgets):
            widget = item.widget()
            flexGrow = grows[i]
            flexShrink = shrinks[i]
            w = bases[i]
            if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx.get("width"), str) and widget._sx.get("width").endswith("%"):
                try:
                    percentage = float(widget._sx.get("width").strip("%"))
                    if 0 <= percentage <= 100:
                        w = int(total_width * (percentage / 100))
                except (ValueError, TypeError):
                    pass

            if flexGrow:
                widths.append(None)
                flex_total += flexGrow
            else:
                widths.append(w)
                fixed_total += w
                if flexShrink:
                    shrink_total += flexShrink

        # print(f"Debug: fixed_total={fixed_total}, flex_total={flex_total}, shrink_total={shrink_total}, widths={widths}")

        remaining = total_width - fixed_total - total_spacing
        # print(f"Debug: remaining space after fixed items={remaining}")

        if remaining > 0 and flex_total > 0:
            for i in range(len(widths)):
                count = len(line_widgets)
                if widths[i] is None:
                    flexGrow = grows[i]
                    widths[i] = int(remaining * flexGrow / flex_total)
        elif remaining < 0 and shrink_total > 0:
            deficit = -remaining
            for i in range(len(widths)):
                flexShrink = shrinks[i]
                if flexShrink:
                    reduction = int(deficit * flexShrink / shrink_total)
                    widths[i] = max(1, widths[i] - reduction)

        # print(f"Debug: final widths after flexGrow/flexShrink distribution={widths}")

        line_width = sum(widths) + total_spacing
        offset_x = 0
        extra_space = 0

        if self._justifyContent == "center":
            offset_x = (total_width - line_width) // 2 if total_width >= line_width else 0
        elif self._justifyContent == "flex-end":
            offset_x = total_width - line_width if total_width >= line_width else 0
        elif self._justifyContent == "space-between" and len(line_widgets) > 1:
            extra_space = (total_width - line_width) // (len(line_widgets) - 1) if total_width >= line_width else 0
            offset_x = 0
        elif self._justifyContent == "space-around" and len(line_widgets) > 0:
            space = (total_width - line_width) // (len(line_widgets) * 2) if total_width >= line_width else 0
            offset_x = space
            extra_space = space * 2
        elif self._justifyContent == "space-evenly" and len(line_widgets) > 0:
            space = (total_width - line_width) // (len(line_widgets) + 1) if total_width >= line_width else 0
            offset_x = space
            extra_space = space
        else:
            offset_x = 0

        # print(f"Debug: line_width={line_width}, offset_x={offset_x}, extra_space={extra_space}")

        current_x = start_x + offset_x
        max_baseline = max(baseline_offsets) if baseline_offsets else 0

        for i, (item, _) in enumerate(line_widgets):
            widget = item.widget()
            width = widths[i]
            height = item.sizeHint().height()

            if self._alignItems == "center":
                offset_y = max(0, (line_height - height) // 2)
            elif self._alignItems == "flex-end":
                offset_y = max(0, line_height - height)
            elif self._alignItems == "baseline":
                item_baseline = baseline_offsets[i] if i < len(baseline_offsets) else 0
                offset_y = max(0, (max_baseline - item_baseline) // 2)
            elif self._alignItems == "stretch":
                offset_y = 0
                height = total_height
            else:
                offset_y = 0

            # print(f"Debug: Item {i}: width={width}, height={height}, position=(x={current_x}, y={y + offset_y}), offset_y={offset_y}, line_height={line_height}")

            if not test_only:
                item.setGeometry(QRect(QPoint(current_x, y + offset_y), QSize(width, height)))

            current_x += width + spacing
            if self._justifyContent in ["space-between", "space-around", "space-evenly"] and (
                (self._justifyContent != "space-between") or i < len(line_widgets) - 1):
                current_x += extra_space

class FlowContainer(QFrame):
    def __init__(self, children):
        super().__init__()
        self.layout = FlowLayout(self)
        self.setLayout(self.layout)
        # self.setStyleSheet('border: 1px solid red;')
        if not isinstance(children, list):
            raise TypeError(f"Argument 'children' has incorrect type (expected list, got {type(children)})")
        for widget in children:
            self.layout.addWidget(widget)
