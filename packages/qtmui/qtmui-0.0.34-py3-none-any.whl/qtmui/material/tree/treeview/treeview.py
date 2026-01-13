from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING, Union

from .treeview_model import TreeViewModel

class TreeView(QTreeView):

    def __init__(self, 
                 model: Union[TreeViewModel] = None, # QFileSystemModel
                 rootIndexPath: str = '/path/to/your/project', # QFileSystemModel
                 ):
        super().__init__()

        # Thiết lập model tệp hệ thống
        self._model = model

        # Thiết lập model
        self.setModel(self._model)

        # Thiết lập root path (thư mục gốc) hiển thị
        self.setRootIndex(self._model.index(rootIndexPath))

        # Các tính năng giống VSCode
        self.setAlternatingRowColors(True)  # Hàng xen kẽ màu
        self.setAnimated(True)              # Hiệu ứng mở rộng / thu gọn
        self.setIndentation(20)             # Mức độ thụt lề của các mục
        self.setSortingEnabled(True)        # Cho phép sắp xếp
        self.sortByColumn(0, Qt.AscendingOrder)  # Sắp xếp theo tên tệp
        self.setHeaderHidden(True)          # Ẩn tiêu đề cột giống VSCode
        self.setExpandsOnDoubleClick(True)  # Mở rộng thư mục khi double click
        self.setSelectionMode(QTreeView.ExtendedSelection)  # Chọn nhiều mục
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Kích hoạt menu ngữ cảnh

