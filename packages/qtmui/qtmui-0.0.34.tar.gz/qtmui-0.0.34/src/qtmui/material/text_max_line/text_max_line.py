import uuid
from typing import Callable, Optional, List, Union

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from PySide6.QtWidgets import QSizePolicy, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QTextOption, QTextLayout
from qtmui.material.styles.create_theme.typography import TypographyStyle
from ..widget_base import PyWidgetBase


from qtmui.hooks import State

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n

class TextMaxLine(QLabel, PyWidgetBase):
    def __init__(self,  
                line: int = 1,
                asLink: bool =  None, 
                align: str =  "left",  # "left" | "center" | "right"
                persistent: bool = None,
                href: str = "#",
                children: Optional[List] = None,
                variant: str = "body2", # "button" | "caption" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "subtitle1" | "subtitle2" | "body1" | "body2" | "overline"
                text: Optional[Union[str, State, Callable]] = None,
                wordWrap: bool = False,
                sx: object = False,
                 ):
        super().__init__()

        self._line = line
        self._asLink = asLink
        self._align = align
        self._persistent = persistent
        self._href = href
        self._children = children
        self._variant = variant
        self._text = text
        self._wordWrap = wordWrap
        self._sx = sx

        self._init_ui()


    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))

        if self._wordWrap:
            self.setWordWrap(True)

        if self._line > 1:
            self.setWordWrap(True)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        if self._align == "left":
            self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        elif self._align == "center":
            self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        else:
            self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


        if isinstance(self._text, State):
            self._text.valueChanged.connect(self.reTranslation)

        i18n.langChanged.connect(self.reTranslation)
        self.reTranslation()

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)
        
    def showEvent(self, e):
        """ fade in """
        PyWidgetBase.showEvent(self, duration=200)
        super().showEvent(e)

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def reTranslation(self, value=None):
        if value:
            if isinstance(value, Callable):
                text = translate(value)
            else:
                text = value
        else:
            if isinstance(self._text, State):
                if isinstance(self._text, Callable):
                    text = translate(self._text.value)
                else:
                    text = self._text
            else:
                if isinstance(self._text, Callable):
                    text = translate(self._text.value)
                else:
                    text = self._text

        self.adjustSize()
        self.original_text = text
        # self.setText(self._text)
        if not self._asLink:
            self.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Cho phép chọn văn bản

        if self._wordWrap:
            if self._asLink:
                self.setText('<a href="{0}">{1}</a>'.format(self._href, self.original_text))
                self.setOpenExternalLinks(True)  # Cho phép mở liên kết ngoài khi nhấp
            else:
                self.setText(self.original_text)
        else:
            if self._line == 1:
                self.update_ellipsis()
            else:
                self.update_ellipsis_multiline()
        

    def update_ellipsis(self):
        """Cập nhật văn bản với dấu `...` nếu kích thước QLabel vượt quá phần tử cha."""

        # Lấy chiều rộng khả dụng của QLabel
        available_width = self.width()
        metrics = QFontMetrics(self.font())

        # Cắt ngắn văn bản với elidedText
        elided_text = metrics.elidedText(self.original_text, Qt.ElideRight, available_width)
        
        # Cập nhật nội dung QLabel
        if self._asLink:
            self.setText('<a href="{0}">{1}</a>'.format(self._href, elided_text))
            self.setOpenExternalLinks(True)  # Cho phép mở liên kết ngoài khi nhấp
        else:
            self.setText(elided_text)


    def update_ellipsis_multiline(self):
        """Cập nhật văn bản với dấu `...` nếu vượt quá số dòng tối đa hoặc kích thước QLabel."""
        font_metrics = QFontMetrics(self.font())
        available_width = self.width()

        # Tùy chọn văn bản (word wrap + elide right)
        option = QTextOption()
        option.setWrapMode(QTextOption.WordWrap)

        # Sử dụng QTextLayout để tách dòng
        layout = QTextLayout(self.original_text, self.font())
        layout.setTextOption(option)
        layout.beginLayout()

        lines = []
        total_height = 0
        line_spacing = font_metrics.lineSpacing()

        # Phân chia văn bản thành các dòng
        for _ in range(self._line):
            line = layout.createLine()
            if not line.isValid():
                break
            line.setLineWidth(available_width)
            line_text = self.original_text[line.textStart():line.textStart() + line.textLength()]
            lines.append(line_text)
            total_height += line_spacing

            # Nếu vượt quá chiều cao của QLabel
            if total_height > self.height():
                lines[-1] = font_metrics.elidedText(lines[-1], Qt.ElideRight, available_width)
                break

        layout.endLayout()

        # Nếu số dòng vượt quá `max_lines`, thêm dấu `...` vào dòng cuối
        if len(lines) == self._line:
            last_line = lines[-1]
            elided_last_line = font_metrics.elidedText(last_line, Qt.ElideRight, available_width - 50)
            lines[-1] = elided_last_line

        # Cập nhật nội dung QLabel
        if self._asLink:
            # self.setText(f'<a href="{self._href}">{"\n".join(lines)}</a>')
            self.setText('<a href="{0}">{1}</a>'.format(self._href, chr(10).join(lines)))
            self.setOpenExternalLinks(True)  # Cho phép mở liên kết ngoài khi nhấp
        else:
            self.setText(chr(10).join(lines))


    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        typography_style: TypographyStyle = getattr(self.theme.typography, self._variant)
        typography_qss = typography_style.to_qss_props()

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

        PyTextMaxLine_root = self.theme.components["PyTextMaxLine"].get("styles")["root"]
        line_height = int(PyTextMaxLine_root["line-height"].replace("px", ""))

        if not self._wordWrap:
            self.setStyleSheet(f"""
                #{self.objectName()} {{
                    color: {self.theme.palette.text.primary};
                    max-height: {line_height*self._line}px; /* Giới hạn chiều cao */
                    {typography_qss}
                }}
                    
                {sx_qss}

            """)
        else:
            self.setStyleSheet(f"""
                #{self.objectName()} {{
                    color: {self.theme.palette.text.primary};
                    {typography_qss}
                }}

                {sx_qss}

            """)


    def resizeEvent(self, event):
        """Hàm được gọi khi kích thước của cửa sổ thay đổi."""
        super().resizeEvent(event)
        if not self._wordWrap:
            if self._line == 1:
                self.update_ellipsis()
            else:
                self.update_ellipsis_multiline()