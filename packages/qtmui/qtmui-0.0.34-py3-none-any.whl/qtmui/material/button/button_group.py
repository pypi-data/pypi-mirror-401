import asyncio
from typing import Callable, Dict, Optional, List, Union
import uuid
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QFrame
from PySide6.QtCore import Qt, QTimer
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme

# Import lớp Button từ mã của bạn
from .button import Button
from ..widget_base import PyWidgetBase


class ButtonGroup(QFrame, PyWidgetBase):
    def __init__(
        self,
        key: str = None,
        children: List[Button] = None,  # Danh sách các nút Button
        orientation: Qt.Orientation = Qt.Horizontal,  # Hướng của ButtonGroup (ngang hoặc dọc)
        align: Qt.AlignmentFlag = Qt.AlignCenter,  # Căn chỉnh các nút trong nhóm
        spacing: int = 0,  # Khoảng cách giữa các nút (đặt bằng 0 để border không bị ngắt quãng)
        fullWidth: bool = False,  # Nếu là True, các nút sẽ chiếm toàn bộ chiều rộng của container
        parent: Optional[QWidget] = None,
        variant: str = "contained",
        size: str = "medium",
        color: str = "primary",
        sx: Optional[Union[Callable, str, Dict]]= None,
    ):
        super().__init__()

        self.setObjectName(str(uuid.uuid4()))

        self._children = children if children else []
        self._orientation = orientation
        self.align = align
        self.spacing = spacing
        self.fullWidth = fullWidth
        self._color = color
        self._size = size
        self._variant = variant
        self._sx = sx
        
        self.theme = useTheme()



        # Thiết lập layout dựa trên hướng
        if not self._orientation == "vertical":
            self.setLayout(QHBoxLayout())
        else:
            self.setLayout(QVBoxLayout())

        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(self.spacing)
        self.layout().setAlignment(self.align)

        # Thêm các nút vào nhóm và xử lý border
        for i, button in enumerate(self._children):
            try:
                self.add_button(button, i)
            except Exception as e:
                import traceback
                traceback.print_exc()

        
        self.theme.state.valueChanged.connect(self._onThemeChanged)
        # self._set_stylesheet()
        QTimer.singleShot(0, self._scheduleSetStyleSheet)
        

        self.destroyed.connect(lambda obj: self._onDestroy())

    def _onDestroy(self, obj=None):
        if hasattr(self, "_setupStyleSheet") and self._setupStyleSheet and not self._setupStyleSheet.done():
            self._setupStyleSheet.cancel()

    def _onThemeChanged(self):
        if not self.isVisible():
            return
        QTimer.singleShot(0, self._scheduleSetStyleSheet)

    def _scheduleSetStyleSheet(self):
        self._setupStyleSheet = asyncio.ensure_future(self._lazy_set_stylesheet())

    async def _lazy_set_stylesheet(self):
        self._set_stylesheet()

    def _set_stylesheet(self, component_styled=None):
        theme = useTheme()
        component_styles = theme.components

        borderColor = None
        if self._color != "default":
            borderColor = component_styles["MuiButtonGroup"].get("styles")["root"][self._variant]["first"]["borderColorRender"](self._color)
        else:
            borderColor = component_styles["MuiButtonGroup"].get("styles")["root"][self._variant]["first"]["borderColorDefault"]

        MuiButtonGroup_button_first = component_styles["MuiButtonGroup"].get("styles")["root"][self._variant]["first"]
        MuiButtonGroup_button_first_root_qss = get_qss_style(MuiButtonGroup_button_first)

        MuiButtonGroup_button_first_root_vertical_qss = get_qss_style(MuiButtonGroup_button_first["orientation"]["vertical"])
        MuiButtonGroup_button_first_root_horizontal_qss = get_qss_style(MuiButtonGroup_button_first["orientation"]["horizontal"])

        MuiButtonGroup_button_middle = component_styles["MuiButtonGroup"].get("styles")["root"][self._variant]["middle"]
        MuiButtonGroup_button_middle_root_qss = get_qss_style(MuiButtonGroup_button_middle)
        MuiButtonGroup_button_middle_root_vertical_qss = get_qss_style(MuiButtonGroup_button_middle["orientation"]["vertical"])
        MuiButtonGroup_button_middle_root_horizontal_qss = get_qss_style(MuiButtonGroup_button_middle["orientation"]["horizontal"])

        MuiButtonGroup_button_last = component_styles["MuiButtonGroup"].get("styles")["root"][self._variant]["last"]
        MuiButtonGroup_button_last_root_qss = get_qss_style(MuiButtonGroup_button_last)
        MuiButtonGroup_button_last_root_vertical_qss = get_qss_style(MuiButtonGroup_button_last["orientation"]["vertical"])
        MuiButtonGroup_button_last_root_horizontal_qss = get_qss_style(MuiButtonGroup_button_last["orientation"]["horizontal"])

        borderWidth = ""
        if self._variant == "outlined":
            borderWidth = "border-width: 1px;"

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx

        # child button styles
        for index, button in enumerate(self._children):

            # Xử lý nút đầu và cuối để tạo border-radius
            if index == 0:
                # Đối với nút đầu tiên
                extra_styles = f"""
                    {
                        f'''
                        #{button.objectName()} {{
                            {MuiButtonGroup_button_first_root_qss}
                            {MuiButtonGroup_button_first_root_vertical_qss if self._orientation == "vertical" else MuiButtonGroup_button_first_root_horizontal_qss}
                            {f"border-color: {borderColor}!important;" if borderColor else ""}
                            {borderWidth}
                            {"border-right-width: 0px;" if self._variant == "outlined" and self._orientation != "vertical" else "border-bottom-width: 0px;" if self._variant == "outlined" and self._orientation == "vertical" else ""}
                        }}
                        '''
                    }
                """

            elif index < len(self._children) - 1:
                # Đối với các nút giữa
                extra_styles = f"""
                    {
                        f'''
                        #{button.objectName()} {{
                            {MuiButtonGroup_button_middle_root_qss}
                            {MuiButtonGroup_button_middle_root_vertical_qss if self._orientation == "vertical" else MuiButtonGroup_button_middle_root_horizontal_qss}
                            {f"border-color: {borderColor};" if borderColor else ""}
                            {borderWidth}
                            {"border-right-width: 0px;" if self._variant == "outlined" and self._orientation != "vertical" else "border-bottom-width: 0px;" if self._variant == "outlined" and self._orientation == "vertical" else ""}
                        }}
                        '''
                    }
                """
            else: 
                # nut cuoi
                extra_styles = f"""
                    {
                        f'''
                        #{button.objectName()} {{
                            {MuiButtonGroup_button_last_root_qss}
                            {MuiButtonGroup_button_last_root_vertical_qss if self._orientation == "vertical" else MuiButtonGroup_button_last_root_horizontal_qss}
                            {f"border-color: {borderColor};" if borderColor else ""}
                            {borderWidth}
                        }}
                        '''
                    }
                """

            button.setStyleSheet(button.styleSheet() + extra_styles + sx_qss)
            
    def add_button(self, button: Button, index: int):
        """Thêm một button vào ButtonGroup với xử lý border cho nút đầu và cuối."""
        if self.fullWidth:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        else:
            button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        button._variant = self._variant
        button._color = self._color
        button._size = self._size

        # button._set_stylesheet()
        QTimer.singleShot(0, button._scheduleSetStyleSheet)
        self.layout().addWidget(button)

    def remove_button(self, button: Button):
        """Loại bỏ một button khỏi ButtonGroup."""
        if button in self._children:
            self._children.remove(button)
            self.layout().removeWidget(button)
            button.setParent(None)

    def set_orientation(self, orientation: Qt.Orientation):
        """Thay đổi hướng của ButtonGroup."""
        self._orientation = orientation
        self.setLayout(QVBoxLayout()) if orientation == Qt.Vertical else self.setLayout(QHBoxLayout())
        self.layout().setSpacing(self.spacing)
        self.layout().setAlignment(self.align)

        # Di chuyển lại các button vào layout mới
        for button in self._children:
            self.layout().addWidget(button)

        self.setLayout(self.layout())

    def set_alignment(self, align: Qt.AlignmentFlag):
        """Thay đổi căn chỉnh của ButtonGroup."""
        self.align = align
        self.layout().setAlignment(align)

    def set_spacing(self, spacing: int):
        """Thay đổi khoảng cách giữa các nút."""
        self.spacing = spacing
        self.layout().setSpacing(spacing)

    def set_fullWidth(self, fullWidth: bool):
        """Thay đổi thuộc tính fullWidth cho các nút trong nhóm."""
        self.fullWidth = fullWidth
        for button in self._children:
            if fullWidth:
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            else:
                button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

