# qtmui/material/widget_base/widget_base.py
import asyncio

from typing import Optional, Callable, Dict, Union

from PySide6.QtWidgets import QGraphicsOpacityEffect, QApplication
from PySide6.QtCore import QEvent, QPropertyAnimation, QEasingCurve, QPoint, QSize, QRunnable, QThreadPool, QTimer
from PySide6.QtGui import QPalette

from qtmui.material.tooltip import ToolTipFilter
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.hooks import State
from qtmui.i18n.use_translation import i18n, translate
from qtmui.errors import PyMuiValidationError

from qtmui.material.utils.validate_params import _validate_param


# Được sử dụng để gen widget async
class WidgetSetter(QRunnable):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    async def run(self):
        self.fn()

class PyWidgetBase:
    def __init__(
        self,
        parent=None,
        onMouseEnter: Optional[Callable] = None,  
        onMouseLeave: Optional[Callable] = None,  
        onMousePress: Optional[Callable] = None,  
        onMouseRelease: Optional[Callable] = None,  
        onFocusIn: Optional[Callable] = None,  
        onFocusOut: Optional[Callable] = None,  
        tooltip: Optional[str] = None,  
        tooltipPlacement: Optional[str] = "top",  
        tooltipLeaveDelay: Optional[int] = 0,
        *args,
        **kwargs
    ):
        self._onMouseEnter = onMouseEnter
        self._onMouseLeave = onMouseLeave
        self._onMousePress = onMousePress
        self._onMouseRelease = onMouseRelease
        self._onFocusIn = onFocusIn
        self._onFocusOut = onFocusOut
        self._tooltip = tooltip
        self._tooltipPlacement = tooltipPlacement
        self._tooltipLeaveDelay = tooltipLeaveDelay

        self._palette_text_color: str = None
        self.component_styles: dict = None
        self._imported = False

        self._sx = None  # sx sẽ được gán bởi các lớp con
        self._child_abs = []  # Danh sách các thành phần con có position: absolute
        self._position = None
        self._left = None
        self._top = None
        self._right = None
        self._bottom = None
        self._relative_to = None
        self._width = None
        self._height = None
        self._width_type = None  # Để lưu kiểu của width ('px', '%', hoặc 'float')
        self._height_type = None  # Để lưu kiểu của height ('px', '%', hoặc 'float')

        self._opacity_value = None
        
        self._thread_pool = QThreadPool.globalInstance()  # Sử dụng thread pool toàn cục
        

    def _setUpUi(self, **kwargs):
        self._onMouseEnter = kwargs.get("onMouseEnter")
        self._onMouseLeave = kwargs.get("onMouseLeave")
        self._onMousePress = kwargs.get("onMousePress")
        self._onMouseRelease = kwargs.get("onMouseRelease")
        self._onFocusIn = kwargs.get("onFocusIn")
        self._onFocusOut = kwargs.get("onFocusOut")
        self._tooltip = kwargs.get("tooltip")
        self._tooltipPlacement = kwargs.get("tooltipPlacement")
        self._tooltipLeaveDelay = kwargs.get("tooltipLeaveDelay") or 0

        self._palette_text_color: str = None
        self.component_styles: dict = None
        self._key = kwargs.get("key")
        self._imported = False

        self._sx_pop_keys = []
        
        # self.__setup_vh_or_vw_height_width() # xử lý height: '100vh' hoặc width: '100vw'
        
    def _do_task_async(self, fn):
        worker = WidgetSetter(fn)
        self._thread_pool.start(QTimer.singleShot(0, lambda: asyncio.ensure_future(worker.run())))  # Chạy setIndexWidget trong thread riêng
        

    def __setup_vh_or_vw_height_width(self): # chỉ dùng được trong nội bộ class/ không gọi được từ class kế thừa nó
        if self._sx:
            if isinstance(self._sx, State):
                __sx = self._sx.value
            else:
                __sx = self._sx
            if isinstance(__sx, Callable):
                __sx = __sx()
            if isinstance(__sx, dict):
                height = __sx.get("height")
                print('height__________________________', height)
                if height and (isinstance(height, str) and height.endswith('vh')):
                    QApplication.instance().mainWindow.sizeChanged.connect(self._update_height_vh_on_mainwindow_resize)

    def _update_height_vh_on_mainwindow_resize(self, new_size: QSize):
        height = new_size.height()
        # Update the height of the widget based on the new main window size
        print('update_height_vh_on_mainwindow_resize__________________________', height)
        # self.setFixedHeight(height) # đệ quy ở đây

    def showEvent(self, duration=10):
        # print(f"showEvent called for {self.objectName()}")
        """Fade in."""
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(0)
        opacityAni.setEndValue(1)
        opacityAni.setDuration(duration)
        opacityAni.setEasingCurve(QEasingCurve.InSine)
        opacityAni.finished.connect(lambda: self.setGraphicsEffect(None))
        opacityAni.start()

    def _installTooltipFilter(self):
        if hasattr(self, "_tooltip") and isinstance(self._tooltip, str) and self._tooltip != "":
            self.installEventFilter(ToolTipFilter(self, self._tooltipLeaveDelay))
            self.setToolTip(self._tooltip)

    def _getTranslatedText(self, input):
        if isinstance(input, Callable):
            return translate(input)
        elif isinstance(input, State):
            if isinstance(input.value, Callable):
                return translate(input.value)
            elif isinstance(input.value, str):
                return input.value
        elif isinstance(input, str):
            return input

    def setupPseudoClasses(self, sx: dict=None):
        '''
            &:hover	Khi rê chuột lên	sx={{ "&:hover": { backgroundColor: "primary.light" } }}
            &:focus	Khi phần tử được focus (vd: input, button)	sx={{ "&:focus": { outline: "2px solid blue" } }}
            &:active	Khi nhấn chuột hoặc đang được kích hoạt	sx={{ "&:active": { transform: "scale(0.98)" } }}
            &:visited	Khi link đã được truy cập	sx={{ "&:visited": { color: "purple" } }}
            &:checked	Với checkbox/radio được chọn	sx={{ "&:checked": { color: "green" } }}
            &:disabled	Khi phần tử bị vô hiệu hóa	sx={{ "&:disabled": { opacity: 0.5 } }}
            &:focus-visible	Focus hiển thị với bàn phím (nhưng không chuột)	sx={{ "&:focus-visible": { outline: "3px solid red" } }}
            &:focus-within	Khi phần tử hoặc con của nó được focus	sx={{ "&:focus-within": { borderColor: "primary.main" } }}
        '''
        if sx:
            hover = sx.get("&:hover")
            focus = sx.get("&:focus")
            enabled = sx.get("&:enabled")
            disabled = sx.get("&:disabled")
            if hover:
                self.hover_qss = get_qss_style(hover)
            if focus:
                self.focus_qss = get_qss_style(focus)
            if enabled:
                self.enabled_qss = get_qss_style(enabled)
            if disabled:
                self.disabled_qss = get_qss_style(disabled)

    def set_styleFn(self, styleFn):
        self.styleFn = styleFn

    # @classmethod
    # @lru_cache(maxsize=128)
    # def _getSxQss(cls, sxStr: str = "", className: str = "PyWidgetBase"):
    #     print("_getSxQss called with sxStr:_______________________________________________")
    #     sx_qss = get_qss_style(cls.sxDict, class_name=className)
    #     return sx_qss

    def _update_component_styles(self, theme, component_styles):
        if component_styles:
            self.component_styles = component_styles
        else:
            self.component_styles = theme.components

    def _on_destroyed(self):
        self.destroyed.connect(lambda obj: self.stylesheet_task.cancel())
        self.destroyed.connect(lambda obj: i18n.langChanged.disconnect(self.reTranslation))
        self.destroyed.connect(lambda obj: self.theme.state.valueChanged.disconnect(self.slot_set_stylesheet))

    def _setup_sx_position(self, sx: Optional[Union[Callable, str, Dict]]):
        # print(f"set_sx called for {self.objectName()} with sx: {sx}")
        """Gán giá trị sx và khởi tạo các thuộc tính liên quan đến định vị."""
        # Ngắt kết nối tín hiệu cũ nếu sx trước đó là State
        # if isinstance(self._sx, State):
        #     try:
        #         self._sx.valueChanged.disconnect(self._on_sx_changed)
        #     except TypeError:
        #         pass

        self._sx = sx

        # Kết nối tín hiệu valueChanged nếu sx là State
        if isinstance(sx, State):
            # print(f"Connecting valueChanged signal for State in {self.objectName()}")
            sx.valueChanged.connect(self._on_sx_changed)

        self._initialize_positioning()

    def _initialize_positioning(self):
        # print(f"_initialize_positioning called for {self.objectName()}")
        """Khởi tạo các thuộc tính liên quan đến vị trí tương đối từ sx."""
        if not self._sx:
            return
        sx = self._sx
        if isinstance(sx, State):
            sx = sx.value
        if isinstance(sx, Callable):
            sx = sx()
        if isinstance(sx, dict):
            self._position = sx.get("position")
            # print(f"Position for {self.objectName()}: {self._position}")
            if self._position == "absolute":
                self._left = sx.get("left")
                self._top = sx.get("top")
                self._right = sx.get("right")
                self._bottom = sx.get("bottom")
                # print(f"Positioning values for {self.objectName()}: left={self._left}, top={self._top}, right={self._right}, bottom={self._bottom}")
                # Giữ lại self._relative_to nếu đã được gán thủ công
                if not hasattr(self, '_relative_to') or self._relative_to is None:
                    self._relative_to = None
                    # Tìm thành phần cha gần nhất có position: relative
                    parent = self.parent()
                    while parent:
                        if isinstance(parent, PyWidgetBase) and parent._position == "relative":
                            parent._add_absolute_child(self)
                            self._relative_to = parent
                            # print(f"Found relative parent for {self.objectName()}: {self._relative_to.objectName() if self._relative_to else None}")
                            break
                        parent = parent.parent()
            else:
                self._position = None
                self._left = None
                self._top = None
                self._right = None
                self._bottom = None
                self._relative_to = None
        else:
            self._position = None
            self._left = None
            self._top = None
            self._right = None
            self._bottom = None
            self._relative_to = None

        # Cập nhật kích thước từ sx sau khi khởi tạo định vị
        # self._update_size_from_sx()


    def _parse_size_value(self, val, parent_size):
        """
        Chuyển đổi giá trị kích thước (height/width) từ dạng % hoặc float (0.1 đến 1) thành pixel.
        - val: Giá trị kích thước (có thể là số, chuỗi dạng '%' hoặc float 0.1-1).
        - parent_size: Kích thước của cha (width hoặc height).
        Trả về giá trị pixel dạng int.
        """
        if isinstance(val, (int, float)):
            if 0 < val <= 1:  # Float từ 0.1 đến 1 được hiểu là tỷ lệ phần trăm
                return int(parent_size * val)
            return int(val)
        if isinstance(val, str):
            val_stripped = val.strip()
            if val_stripped.endswith('%'):
                try:
                    perc = float(val_stripped[:-1])
                    return int(parent_size * (perc / 100.0))
                except ValueError:
                    return 0
            elif val_stripped.endswith('vh'):
                try:
                    perc = float(val_stripped[:-2])
                    return int(parent_size * (perc / 100.0))
                except ValueError:
                    return 0
            elif val_stripped.endswith('vw'):
                try:
                    perc = float(val_stripped[:-2])
                    return int(parent_size * (perc / 100.0))
                except ValueError:
                    return 0
            elif val_stripped.endswith('px'):
                try:
                    px = float(val_stripped[:-2])
                    return int(px)
                except ValueError:
                    return 0
            else:
                try:
                    return int(float(val_stripped))
                except ValueError:
                    return 0
        return 0


    def _update_size_from_sx(self):
        """
        Cập nhật kích thước của widget dựa trên sx (width và height).
        Nếu width/height là dạng % hoặc float (0.1-1), tính toán dựa trên kích thước cha.
        """
        sx = self._sx
        if isinstance(sx, State):
            sx = sx.value
        if isinstance(sx, Callable):
            sx = sx()
        if not isinstance(sx, dict):
            return

        width = sx.get("width")
        height = sx.get("height")
        parent = self.parent()
        parent_width = parent.width() if parent else 0
        parent_height = parent.height() if parent else 0

        if hasattr(self, "_key") and self._key == "box-form-new-edit":
            print(self._key, parent.sizeHint().height())

        # Xử lý width
        if width is not None:
            if isinstance(width, str) and width.endswith('vw'):
                self._width_type = 'vw'
                self._width = width
                # parent_width = QApplication.instance().mainWindow.width()
                if parent_width > 0:
                    new_width = self._parse_size_value(width, parent_width)
                    # self.setFixedWidth(new_width)
                    # self.setMinimumWidth(new_width) # đệ quy ở đây
            elif isinstance(width, str) and width.endswith('%'):
                self._width_type = '%'
                self._width = width
                if parent_width > 0:
                    new_width = self._parse_size_value(width, parent_width)
                    # self.setFixedWidth(new_width)
                    self.setMinimumWidth(new_width)
            elif isinstance(width, float) and 0 < width <= 1:
                self._width_type = 'float'
                self._width = width
                if parent_width > 0:
                    new_width = self._parse_size_value(width, parent_width)
                    # self.setFixedWidth(new_width)
                    self.setMinimumWidth(new_width)
            else:
                self._width_type = 'px'
                self._width = width
                new_width = self._parse_size_value(width, parent_width)
                # self.setFixedWidth(new_width)
                self.setMinimumWidth(new_width)

        # Xử lý height
        if height is not None:
            if isinstance(height, str) and height.endswith('vh'):
                self._height_type = 'vh'
                self._height = height
                parent_height = QApplication.instance().mainWindow.height()
                new_height = self._parse_size_value(height, parent_height)
                # self.setFixedHeight(parent_height)
                # self.setMinimumHeight(parent_height) # đệ quy ở đây
            elif isinstance(height, str) and height.endswith('%'):
                self._height_type = '%'
                self._height = height
                if parent_height > 0:
                    new_height = self._parse_size_value(height, parent_height)
                    # self.setFixedHeight(new_height)
                    self.setMinimumHeight(new_height)
            elif isinstance(height, float) and 0 < height <= 1:
                self._height_type = 'float'
                self._height = height
                if parent_height > 0:
                    new_height = self._parse_size_value(height, parent_height)
                    # self.setFixedHeight(new_height)
                    self.setMinimumHeight(new_height)
            else:
                self._height_type = 'px'
                self._height = height
                new_height = self._parse_size_value(height, parent_height)
                # self.setFixedHeight(new_height)
                self.setMinimumHeight(new_height)


    def __get_sx_dict(self):
        sx = None
        if self._sx:
            if isinstance(self._sx, State):
                sx = self._sx.value
            else:
                sx = self._sx

            if isinstance(sx, Callable):
                sx = sx()

            if isinstance(sx, dict):
                return sx
            else:
                return None

    def __contvert_to_percent_value(self, value):
        width_percent = None

        if value is not None:
            if isinstance(value, (int, float)) and 0 <= value <= 1:
                # Convert 0-1 range to percentage
                width_percent = value * 100
                # print('covaooooooooooooooooooooooooooo', width_percent, self._key if hasattr(self, "_key") else None)
            elif isinstance(value, str) and value.endswith("%"):
                try:
                    width_percent = float(value.strip("%"))
                except ValueError:
                    error = PyMuiValidationError(
                        file_path="self.file_path",
                        param_name="param_name",
                        param_value=value,
                        expected_types=[int],
                        error_type="INVALID_CONDITION",
                        message=f"Parameter does not satisfy the validation condition: check_value"
                    )
                    raise error
                
        return width_percent

    def _get_float_or_percent_sx_value(self, key):
        """
            lấy ra giá trị float hoặc % từ giá trị
        """

        # get dict từ sx
        sx_dict = self.__get_sx_dict()

        if not sx_dict:
            return None
        
        # lấy value theo key
        value = sx_dict.get(key, None)

        # lấy giá trị phần trăm
        percent_value = self.__contvert_to_percent_value(value)
        # if percent_value and 0 < percent_value < 100:
        #     # cập nhật sx pop key
        #     if key not in self._sx_pop_keys:
        #         self._sx_pop_keys.append(key)

        return percent_value

    def _apply_float_and_percent_sx_value(self):
        """
        keys áp dụng:
            + width
            + height

        Note: việc áp dụng các giá trị thông qua hàm này sẽ ghi đè thuộc tính của sx vì nó gọi thông qua resize và painter event
        """
        # print('__handle_float_and_percent_sx_value______________', self)

        # chuong trinh bi cham mot phan o day
        
        parent = self.parent()
        if not parent:
            return

        parent_width = parent.width()
        parent_height = parent.height()

        # Get current dimensions as fallback
        current_width = self.width()
        current_height = self.height()

        # Process width
        new_width = current_width
        width_percent = self._get_float_or_percent_sx_value(key="width")
        if width_percent:
            new_width = int(parent_width * width_percent / 100)

        # if self._key == "kkkkkkkkkkkkkkkkkk":
        #     print('new_parent_wwwwwwwwwwwwwwww', parent, parent_width, new_width)

        # Process height
        new_height = current_height
        height_percent = self._get_float_or_percent_sx_value(key="height")
        if height_percent:
            new_height = int(parent_height * height_percent / 100)

        if not (hasattr(parent, "_flexWrap") and parent._flexWrap):
            self.resize(new_width, new_height)

    def _on_sx_changed(self):
        # print(f"_on_sx_changed called for {self.objectName()}")
        """Xử lý khi giá trị sx thay đổi (dành cho State)."""
        self._initialize_positioning()
        self._update_size_from_sx()  # Cập nhật kích thước nếu sx thay đổi
        self.update_absolute_position()  # Cập nhật vị trí của chính nó
        self.update_absolute_children()  # Cập nhật vị trí của các con




    def _get_position_from_sx(self) -> Optional[str]:
        """Lấy giá trị position từ sx."""
        return self._get_sx_value("position")

    def _get_sx_value(self, key: str) -> Optional[Union[str, int]]:
        """Lấy giá trị của một thuộc tính từ sx."""
        sx = self._sx
        if isinstance(sx, State):
            sx = sx.value
        if isinstance(sx, Callable):
            sx = sx()
        if isinstance(sx, dict):
            return sx.get(key)
        return None

    def _add_absolute_child(self, child: 'PyWidgetBase'):
        """Thêm một thành phần con có position: absolute vào danh sách quản lý."""
        if child not in self._child_abs:
            self._child_abs.append(child)
            child._relative_to = self
            # print(f"Added absolute child {child.objectName()} to {self.objectName()}")
            child.update_absolute_position()

    def _remove_absolute_child(self, child: 'PyWidgetBase'):
        """Xóa một thành phần con khỏi danh sách quản lý."""
        if child in self._child_abs:
            self._child_abs.remove(child)
            child._relative_to = None
            # print(f"Removed absolute child {child.objectName()} from {self.objectName()}")

    def update_absolute_position(self):
        """
        Cập nhật vị trí của thành phần nếu có position: absolute,
        dựa trên thành phần cha gần nhất có position: relative.
        """
        # print(f"update_absolute_position called for {self.objectName()}")
        position = self._get_position_from_sx()
        # print(f"Position in update_absolute_position for {self.objectName()}: {position}")
        if position != "absolute" or not self._relative_to:
            # print(f"Exiting update_absolute_position for {self.objectName()}: position={position}, relative_to={self._relative_to}")
            return

        def parse_value(val, total):
            """
            Hỗ trợ các dạng:
            - Nếu val là số: trả về giá trị đó.
            - Nếu val là chuỗi kết thúc bằng '%': chuyển đổi phần trăm sang pixel.
            - Nếu val là chuỗi kết thúc bằng 'px': chuyển đổi thành số pixel.
            - Nếu val là chuỗi dạng 'xxx% - yyypx' hoặc 'xxx% + yyypx':
                Tách phần % và phần px, tính: int(xxx/100 * total) ± yyy.
            - Nếu không khớp, trả về 0.
            """
            import re
            if isinstance(val, (int, float)):
                return int(val)
            if isinstance(val, str):
                pattern = r'^\s*([-+]?\d+)%\s*([-+])\s*(\d+)px\s*$'
                match = re.match(pattern, val)
                if match:
                    perc_str, sign, px_str = match.groups()
                    try:
                        perc_val = float(perc_str)
                    except ValueError:
                        perc_val = 0
                    try:
                        px_val = float(px_str)
                    except ValueError:
                        px_val = 0
                    if sign == '-':
                        return int(perc_val / 100.0 * total - px_val)
                    else:
                        return int(perc_val / 100.0 * total + px_val)
                
                val_stripped = val.strip()
                if val_stripped.endswith('%'):
                    try:
                        perc = float(val_stripped[:-1])
                    except ValueError:
                        perc = 0
                    return int(perc / 100.0 * total)
                elif val_stripped.endswith('px'):
                    try:
                        px = float(val_stripped[:-2])
                    except ValueError:
                        px = 0
                    return int(px)
                else:
                    try:
                        return int(float(val))
                    except Exception:
                        return 0
            return 0

        # Đặt parent của thành phần absolute là parent của relative_to để tránh trôi nổi khi cuộn chuột
        if self._relative_to and self.parent() and self._relative_to.parent():
            self.setParent(self._relative_to.parent())  # Dòng này đảm bảo khi cuộn chuột không bị trôi nổi
        else:
            # print(f"Exiting update_absolute_position for {self.objectName()}: missing parent - self._relative_to={self._relative_to}, self.parent()={self.parent()}, self._relative_to.parent()={self._relative_to.parent() if self._relative_to else None}")
            return

        relative_to = self._relative_to
        if not relative_to:
            # print(f"No relative_to found for {self.objectName()}")
            return

        # print(f"Relative to for {self.objectName()}: {relative_to.objectName()}")

        # Truy xuất giá trị trực tiếp từ sx thay vì sử dụng các thuộc tính đã lưu trữ
        left = self._get_sx_value("left")
        top = self._get_sx_value("top")
        right = self._get_sx_value("right")
        bottom = self._get_sx_value("bottom")
        # print(f"Positioning values in update_absolute_position for {self.objectName()}: left={left}, top={top}, right={right}, bottom={bottom}")

        # Tính tọa độ x
        if left is not None:
            x = parse_value(left, relative_to.width())
        elif right is not None:
            right_val = parse_value(right, relative_to.width())
            x = relative_to.width() - self.width() - right_val
        else:
            x = 0

        # Tính tọa độ y
        if top is not None:
            y = parse_value(top, relative_to.height())
        elif bottom is not None:
            bottom_val = parse_value(bottom, relative_to.height())
            y = relative_to.height() - self.height() - bottom_val
        else:
            y = 0

        # print(f"Calculated position for {self.objectName()}: x={x}, y={y}")

        # Lấy điểm cục bộ (x, y) của relativeTo và chuyển sang global
        desired_local = QPoint(x, y)
        global_point = relative_to.mapToGlobal(desired_local)
        # print(f"Global point for {self.objectName()}: {global_point}")
        # Chuyển từ global sang hệ tọa độ của parent (mainWindow)
        new_pos = self.parent().mapFromGlobal(global_point)
        # print(f"New position for {self.objectName()}: {new_pos}")
        
        new_pos = self._ajustPositionBaseOnParentMarginValue(new_pos)
        
        self.move(new_pos)
        # Đảm bảo hiển thị thành phần sau khi di chuyển
        if not self.isVisible():
            # print(f"Calling show() for {self.objectName()}")
            self.show()
            pass
        else:
            # print(f"{self.objectName()} is already visible")
            pass

    def _ajustPositionBaseOnParentMarginValue(self, pos):
        if self._relative_to._sx and isinstance(self._relative_to._sx, dict):
            parent_sx = self._relative_to._sx
            margin = parent_sx.get("margin", 0)
            if isinstance(margin, (int, float)):
                pos.setX(pos.x() + int(margin))
                pos.setY(pos.y() + int(margin))
            elif isinstance(margin, str) and margin.endswith("px"):
                try:
                    margin_px = int(float(margin[:-2]))
                    pos.setX(pos.x() + margin_px)
                    pos.setY(pos.y() + margin_px)
                except ValueError:
                    pass
            marginLeft = parent_sx.get("margin-left", 0)
            if isinstance(marginLeft, (int, float)):
                pos.setX(pos.x() + int(marginLeft))
            elif isinstance(marginLeft, str) and marginLeft.endswith("px"):
                try:
                    margin_px = int(float(marginLeft[:-2]))
                    pos.setX(pos.x() + margin_px)
                except ValueError:
                    pass
            marginTop = parent_sx.get("margin-top", 0)
            if isinstance(marginTop, (int, float)):
                pos.setY(pos.y() + int(marginTop))
            elif isinstance(marginTop, str) and marginTop.endswith("px"):
                try:
                    margin_px = int(float(marginTop[:-2]))
                    pos.setY(pos.y() + margin_px)
                except ValueError:
                    pass
        return pos
        


    def update_absolute_children(self):
        """
        Cập nhật vị trí của tất cả thành phần con có position: absolute,
        nếu thành phần cha gần nhất có position: relative là self.
        """
        # print(f"update_absolute_children called for {self.objectName()}")
        for child in self._child_abs:
            # print(f"Processing child {child.objectName()} in update_absolute_children")
            # Sử dụng child._relative_to thay vì tìm closest_relative
            if child._relative_to == self:
                child.update_absolute_position()
            else:
                # print(f"Child {child.objectName()} not updated: _relative_to is {child._relative_to.objectName() if child._relative_to else None}")
                # Xóa child khỏi danh sách quản lý của self nếu _relative_to không phải là self
                self._remove_absolute_child(child)
                if child._relative_to:
                    child._relative_to._add_absolute_child(child)

    def resizeEvent(self, event):
        """Gọi update_absolute_children khi thành phần cha thay đổi kích thước."""

        self._apply_float_and_percent_sx_value()

        # Cập nhật kích thước của chính widget nếu width/height là dạng % hoặc float
        self._update_size_from_sx()

        if self._get_position_from_sx() == "relative":
            self.update_absolute_children()
        if self._get_position_from_sx() == "absolute":
            self.update_absolute_position()

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.update()

    def paintEvent(self, event):
        """Gọi update_absolute_children khi thành phần cha được vẽ lại."""
        # Lấy giá trị opacity từ sx
        opacity = self._get_sx_value("opacity")

        if opacity is not None and not self._opacity_value:
            try:
                self._opacity_value = float(opacity)
                # Đảm bảo opacity nằm trong khoảng hợp lệ (0 đến 1)
                self._opacity_value = max(0.0, min(1.0, self._opacity_value))
            except (ValueError, TypeError):
                self._opacity_value = 1.0

            # Khởi tạo QPainter và áp dụng opacity
            # creating a opacity effect 
            self.opacity_effect = QGraphicsOpacityEffect(self) 
            # setting opacity level 
            self.opacity_effect.setOpacity(self._opacity_value) 
            # adding opacity effect to the label 
            self.setGraphicsEffect(self.opacity_effect) 

            # palette = self.palette()  # lấy palette hiện tại của QPushButton
            # color = palette.color(QPalette.Window)  # lấy màu nền (Window)
            # color.setAlpha(13)  # thiết lập độ trong suốt
            # palette.setColor(QPalette.Window, color)  # áp dụng màu đã alpha cho Text
            # self.setPalette(palette)  # cập nhật lại palette

        if self._get_position_from_sx() == "relative":
            self.update_absolute_children()
        if self._get_position_from_sx() == "absolute":
            self.update_absolute_position()


    def enterEvent(self, event):
        # self.setProperty("slot", "hover")
        # self._setStyleSheet()
        if self._onMouseEnter:
            self._onMouseEnter()

    def leaveEvent(self, event):
        # self.setProperty("slot", "leave")
        # self._setStyleSheet()
        if self._onMouseLeave:
            self._onMouseLeave()

    def mousePressEvent(self, event):
        if self._onMousePress:
            self._onMousePress()

    def mouseReleaseEvent(self, event):
        if self._onMouseRelease:
            self._onMouseRelease()

    def focusInEvent(self, event) -> None:
        # print('widget_base > focusInEvent___________________', self._onFocusIn)
        if self._onFocusIn:
            self._onFocusIn(event)

    def focusOutEvent(self, event) -> None:
        print('vaooooooooooooo888888888888888888888888888888________________')
        if self._onFocusOut:
            self._onFocusOut(event)

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.Type.StyleChange:
            color = self.palette().color(QPalette.ColorRole.ButtonText)
            if not self._imported:
                from ..py_svg_widget import PySvgWidget
            for widget in self.findChildren(PySvgWidget):
                widget._color = color.name()
                if hasattr(widget, "_path"):
                    widget.changeSvg(widget._path)
                elif hasattr(widget, "_key"):
                    widget.changeSvg(widget._key)