from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel
from PySide6.QtCore import Qt

class TreeViewModel(QFileSystemModel):
    def __init__(self, 
                 path, # QFileSystemModel
                 **kwargs
                 ):
        super().__init__(**kwargs)

        # Thiết lập model tệp hệ thống
        self.setRootPath(path)  # Gán root cho model (ví dụ: thư mục dự án)

