from typing import Dict
from PySide6.QtWidgets import QVBoxLayout, QFrame, QListView, QAbstractItemView, QLabel, QFrame, QScrollArea, QWidget, QSizePolicy
from PySide6.QtCore import Qt, QStringListModel, QEvent, QPoint, QRect
import sys
from PySide6.QtGui import QFocusEvent


class ListView(QListView):
    def __init__(
                self, 
                parent_frame, 
                context, 
                fullWidth: bool = None, 
                children: list = None
                ):
        super().__init__(parent_frame)
        self.parent_frame = parent_frame
        self.context = context
        # self.setModel(QStringListModel(options))

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        # Tạo một vùng cuộn
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Thiết lập kích thước chính sách
        if fullWidth:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        else:
            self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
            self.scroll_area.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Tạo một widget để đặt bên trong vùng cuộn
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # Thêm một số nội dung vào widget
        for item in children:
            self.content_layout.addWidget(item)
        
        self.update_height()

        # Thêm widget nội dung vào vùng cuộn
        self.scroll_area.setWidget(self.content_widget)
        
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)


    def update_height(self):
        # Cập nhật kích thước của vùng cuộn dựa trên kích thước của phần tử con
        content_widget_size = self.content_widget.sizeHint()
        self.scroll_area.setMaximumHeight(content_widget_size.height())

