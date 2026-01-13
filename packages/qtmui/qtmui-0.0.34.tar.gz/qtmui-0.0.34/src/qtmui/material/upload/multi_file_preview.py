from typing import Callable, Union, Optional, List
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame, QPushButton, QSizePolicy, QVBoxLayout, QSpacerItem
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from ..button.icon_button import IconButton
from ..py_iconify import PyIconify, Iconify
from ...qtmui_assets import QTMUI_ASSETS

class MultiFilePreview(QFrame):
    def __init__(self,
                 thumbnail: bool = False,
                 files: Optional[List[List[Union[str, int]]]] = None,
                 onRemove: Optional[Callable] = None,
                 sx: Optional[dict] = None,
                 *args, **kwargs):
        super(MultiFilePreview, self).__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self._thumbnail = thumbnail
        self._files = files or []
        self._onRemove = onRemove
        self.sx = sx or {}

        self.renderPreviews()
    
    def renderPreviews(self):
        for file in self._files:
            self.addFilePreview(file)
    
    def addFilePreview(self, file):
        file_name = file
        file_size = 1000
        frm_file_info = QWidget()
        hlo_frm_file_info = QHBoxLayout(frm_file_info)
        hlo_frm_file_info.setContentsMargins(0, 0, 0, 0)

        # File Icon
        btn_icon = QPushButton()
        btn_icon.setStyleSheet('border: none; background: none;')
        btn_icon.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.UPLOAD_FILE, color="#000000"))
        btn_icon.setIconSize(QSize(32, 32))
        hlo_frm_file_info.addWidget(btn_icon)

        # File Info
        lbl_title = QLabel(file_name)
        lbl_size = QLabel(self.format_size(file_size))
        
        file_info_layout = QVBoxLayout()
        file_info_layout.addWidget(lbl_title)
        file_info_layout.addWidget(lbl_size)
        hlo_frm_file_info.addLayout(file_info_layout)
        hlo_frm_file_info.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Remove Button
        btn_remove = IconButton(
            onClick=lambda f=file: self.removeFilePreview(f),
            edge="end",
            size="small",
            icon=Iconify(key=QTMUI_ASSETS.ICONS.CLOSE)
        )
        hlo_frm_file_info.addWidget(btn_remove)
        
        self.layout().addWidget(frm_file_info)
    
    def removeFilePreview(self, file):
        if file in self._files:
            self._files.remove(file)
            if self._onRemove:
                self._onRemove(file)
            self.renderPreviews()
    
    @staticmethod
    def format_size(bytes):
        if bytes < 1024:
            return f"{bytes} B"
        elif bytes < 1024**2:
            return f"{bytes / 1024:.2f} KB"
        elif bytes < 1024**3:
            return f"{bytes / 1024**2:.2f} MB"
        else:
            return f"{bytes / 1024**3:.2f} GB"
