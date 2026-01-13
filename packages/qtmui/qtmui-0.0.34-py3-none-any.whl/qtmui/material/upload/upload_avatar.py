from typing import Callable, Optional
import uuid

from ..system.color_manipulator import alpha

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QVBoxLayout, QLabel, QFileDialog, QFrame
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QCursor, QMouseEvent

from ..typography import Typography
from ..stack import Stack
from ..box import Box
from ..py_svg_widget import PySvgWidget
from ..view import View
from ..image import Image

from qtmui.hooks import useState
from qtmui.material.styles import useTheme


class UploadAvatar(QFrame):
    def __init__(self,
                multiple: bool = None,
                thumbnail: str = None,
                file: str = None,
                files: str = None,
                onDrop:Callable = None,
                onChange:Callable = None,
                onRemove:Callable = None,
                onRemoveAll:Callable = None,
                onUpload:Callable = None,
                error: bool = False,
                value: Optional[str] = None,
                 *args, 
                 **kwargs
                 ):
        super().__init__()
        # super(UploadAvatar, self).__init__( *args, **kwargs)
        self.setObjectName(str(uuid.uuid4()))

        self._multiple = multiple
        self._thumbnail = thumbnail
        self._files = files
        self._onDrop = onDrop
        self._onChange = onChange
        self._onRemove = onRemove
        self._onRemoveAll = onRemoveAll
        self._onUpload = onUpload
        self._value = value

        self.theme = useTheme()

        self._init_ui()

    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().setContentsMargins(0,0,0,0)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        
        self.avatar, self.setAvatar = useState(None)

        if self._value:
            self._set_value()
        else:
            self.setAvatar(
                Stack(
                    alignItems="center",
                    justifyContent="center",
                    children=[
                        PySvgWidget(key="solar:camera-add-bold", width=32, height=32),
                        Typography(text="Upload photo", variant="caption", sx={"color": "palette.text.disabled"})
                    ]
                )
            )

        self.layout().addWidget(
            Box(
                sx={
                    "min-height": 140,
                    "max-height": 140,
                    "min-width": 140,
                    "max-width": 140,
                    "border": f"1px dashed {alpha(self.theme.palette.grey._500, 0.32)}",
                    "border-radius": 71
                },
                children=[
                    Stack(
                        sx={
                            "min-height": 120,
                            "max-height": 120,
                            "min-width": 120,
                            "max-width": 120,
                            "border-radius": 60,
                            "background-color": alpha(self.theme.palette.grey._500, 0.12)
                        },
                        alignItems="center",
                        justifyContent="center",
                        
                        children=[
                            View(
                                content=self.avatar
                            )
                        ]
                    )
                ]
            )
        )


    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.open_file()
        return super().mousePressEvent(event)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png *.jpg *.jpeg);;All Files (*)")
        # self.btn_icon_upload.setIcon(file_name)
        # file_name = file_name.split('/')[-1]
        self._value = file_name
        if self._onChange:
            self._onChange(self._value)

        print('file_name_________', file_name)
        self.setAvatar(
            Image(src=file_name, size=QSize(120, 120), sx={"border-radius": 60})
        )

    def _set_value(self, value=None):
        if value:
            self._value = value

        if self._value:
            print('self._value___________________', self._value)
            self.setAvatar(
                # Image(src="F:/2024/WINDOOR/qtmui/avatar.jpg", size=QSize(120, 120), sx={"border-radius": 60})
                Image(src="http://localhost:3000/media/Screenshot_1.png", size=QSize(120, 120), sx={"border-radius": 60})
            )

        if self._onChange:
            
            self._onChange(self._value)

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
