from PySide6.QtWidgets import (
    QApplication, QListView, QFrame, QHBoxLayout, QLabel, QCheckBox, QWidget, QVBoxLayout, QStyledItemDelegate, QComboBox
)
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QSize

from typing import List
import sys

# ------------------------------
# Custom Widget Item
# ------------------------------
class CustomMenuItem(QFrame):
    def __init__(self, children: List[QWidget]):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        for widget in children:
            layout.addWidget(widget)


# ------------------------------
# Data model
# ------------------------------
class MyListModel(QAbstractListModel):
    def __init__(self, data):
        super().__init__()
        self._data = data  # mỗi item là dict: {'selected': bool}

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.UserRole:
            return self._data[index.row()]
        return None

    def toggle_selected(self, index: QModelIndex):
        row = index.row()
        self._data[row]["selected"] = not self._data[row]["selected"]
        self.dataChanged.emit(index, index, [Qt.UserRole])


# ------------------------------
# Delegate để tạo widget custom
# ------------------------------
class MyItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, model=None):
        super(MyItemDelegate, self).__init__(parent)
        self._model = model

    def createEditor(self, parent, option, index):
        item_data = index.model().data(index, Qt.UserRole)
        row = index.row()
        selected = item_data.get("selected", False)

        print(row)

        # Widget hiển thị
        editor = CustomMenuItem([
            QCheckBox(checked=selected),
            QLabel(f"Item {row}")
        ])
        editor.setParent(parent)
        return editor

    def paint(self, painter, option, index):
        super(MyItemDelegate, self).paint(painter, option, index)
        if not self.parent().indexWidget(index) and not index.parent().isValid():

            item_data = index.model().data(index, Qt.UserRole)

            index_row = index.row()
            index_col = index.column()

            selected = item_data.get("selected", False)

            editor = CustomMenuItem([
                QCheckBox(checked=selected),
                QLabel(f"Item {index_row}")
            ])
            self.parent().setIndexWidget(index, editor)

    def sizeHint(self, option, index):
        return QSize(200, 32)


class Select(QComboBox):
    def __init__():
        super().__init__()


# ------------------------------
# Main Window
# ------------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Dữ liệu mẫu
        data = [{"selected": True} for _ in range(10)]

        # Model & View
        self.model = MyListModel(data)
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.setItemDelegate(MyItemDelegate(parent=self.list_view))
        self.list_view.setEditTriggers(QListView.AllEditTriggers)  # luôn hiển thị widget custom

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.list_view)
        layout.addWidget(self.list_view)

        # Cho phép click để toggle selected
        self.list_view.clicked.connect(self.on_item_clicked)

    def on_item_clicked(self, index: QModelIndex):
        self.model.toggle_selected(index)


# ------------------------------
# App
# ------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 400)
    window.show()
    sys.exit(app.exec())
