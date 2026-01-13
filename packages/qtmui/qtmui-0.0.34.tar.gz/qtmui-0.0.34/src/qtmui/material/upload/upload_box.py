import uuid
from typing import Optional, Callable
from PySide6.QtWidgets import QVBoxLayout, QFileDialog, QFrame, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor, QMouseEvent

from ..typography import Typography
from ..box import Box
from ..py_iconify import PyIconify, Iconify
from ..py_svg_widget import PySvgWidget
from ...qtmui_assets import QTMUI_ASSETS
from ..button.button import Button
from qtmui.material.styles import useTheme



styles = """
        #{} {{
            border: {};
            margin: {};
            font-weight: {};
            line-height: {};
            font-size: {};
            font-family: {};
            padding: {};
            border-radius: {};
            color:  {};
            background-color: {};
        }}
        #{}::hover {{
            background-color: {};
        }}

"""


class UploadBox(QFrame):
# class Chip(QWidget):
    """
    Button
    Base Chip

    Args:
        key?: 'filled' | 'outlined' | 'outlined' | 'soft'
        severity?: str = 'info' | 'success' | 'warning' | 'error'
        variant?: 'filled' | 'outlined' | 'outlined' | 'soft'
        size?: str = 'small' | 'medium' | 'large'
        sx: str = QSS string
            {
                color: red;
                backroud: none;
            }
        justifyContent: "space-around" | "space-between" | "space-evenly" | "stretch" | "center" | "end" | "flex-end" | "flex-start" | "start"

    Returns:
        new instance of Button
    """
    def __init__(self,
                files: str = None,
                onDrop: Optional[Callable] = None,
                error: object = None,
                placeholder: object = None,
                sx: object = None,
                 *args, 
                 **kwargs
                 ):
        super().__init__()

        self._files = files
        self._onDrop = onDrop
        self._error = error
        self._placeholder = placeholder
        self._sx = sx

        self._init_ui()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.layout().addWidget(
            Box(
                direction="column",
                children=[
                    self._placeholder if self._placeholder else
                    Box(
                        children=[
                            Box(
                                direction="row",
                                children=[
                                    Button(
                                        variant="soft", 
                                        text="Upload", 
                                        icon=Iconify(key=QTMUI_ASSETS.ICONS.CLOUD_UPLOAD_BOLD, color=useTheme().palette.primary.main, size=QSize(200, 200)), 
                                        onClick=self.open_file
                                    ),
                                    Box(
                                        direction="column",
                                        children=[
                                            Typography(text="Allowed *.jpeg, *.jpg, *.png, *.gif", variant="h6"),
                                            Typography(text="Max size of 3 Mb", variant="h6")
                                        ]
                                    )
                                ]
                            ),
                            Typography(text="", variant="h5")
                        ]
                    )
                ]
            )
        )


        # self.setStyleSheet(styles.format(
        #     self.objectName(),
        #     self._border,
        #     self._margin,
        #     self._fontWeight,
        #     self._lineHeight,
        #     self._fontSize,
        #     self._fontFamily,
        #     self._padding,
        #     self._borderRadius,
        #     self._textColor, 
        #     self._backgroundColor,
        #     self.objectName(),
        #     self._hoverBackgroundColor
        # ))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.open_file()
        return super().mousePressEvent(event)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        self.lbl_file_info.setText(file_name)

    def format_size(self, bytes):
        """
        Hàm này nhận đầu vào là số byte và trả về chuỗi định dạng kích thước tương ứng
        dưới dạng byte, KB, MB hoặc GB.
        """
        if bytes < 1024:
            return f"{bytes} B"
        elif bytes < 1024**2:
            kb = bytes / 1024
            return f"{kb:.2f} KB"
        elif bytes < 1024**3:
            mb = bytes / 1024**2
            return f"{mb:.2f} MB"
        else:
            gb = bytes / 1024**3
            return f"{gb:.2f} GB"