from typing import Callable, Dict
import asyncio
from PySide6.QtCore import QAbstractTableModel, QObject, Signal, Property, QModelIndex, QTimer, QThreadPool, QRunnable
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QScrollBar, QStyledItemDelegate, QPushButton, QTableView, QHBoxLayout, QMainWindow, QFrame, QHeaderView, QApplication

from qtmui.hooks import State
from ..skeleton import Skeleton
from ..box import Box

INDEXS = []
SCROLL_POS = None


class StyledItem(QStyledItemDelegate):
    def __init__(self, parent=None, model=None):
        super(StyledItem, self).__init__(parent)
        self._model = model

    def paint(self, painter, option, index):
        super(StyledItem, self).paint(painter, option, index)
        if not self.parent().indexWidget(index) and not index.parent().isValid():
            pass  # Logic đã được chuyển sang _set_index_widget


class GridViewModel(QAbstractTableModel):
    def __init__(self, parent, data):
        super(GridViewModel, self).__init__(parent)
        self._data = data

    def rowCount(self, n=None):
        return len(self._data)

    def columnCount(self, n=None):
        return len(self._data[0])

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                try:
                    widget_info = self._data[index.row()][index.column()]
                    return widget_info
                except:
                    return None


# Worker để chạy setIndexWidget trong thread riêng
class WidgetSetter(QRunnable):
    def __init__(self):
        super().__init__()

    async def run(self, grid_view, index, widget):
        if not grid_view.indexWidget(index):
            grid_view.setIndexWidget(index, widget)


class GridView(QTableView):
    setIndexWidgetSignal = Signal(object)
    removeIndexWidgetSignal = Signal(QModelIndex)

    def __init__(
            self,
            model: State,
            columnCount=None,
            rowHeight=50,
            skeleton: Callable = None,
            sm=1,
            md=2,
            lg=3,
            xl=4
    ):
        super(GridView, self).__init__()
        self._rowHeight = rowHeight
        self._columnCount = columnCount
        self._skeleton = skeleton
        self.sm = sm
        self.md = md
        self.lg = lg
        self.xl = xl

        self.model_data = []
        self._last_visible_indexes = []

        if self._columnCount:
            self.columnsToShow = self._columnCount
        else:
            self.columnsToShow = sm

        self._model: State = model
        self._thread_pool = QThreadPool.globalInstance()  # Sử dụng thread pool toàn cục
        self.worker = WidgetSetter()

        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setDragEnabled(False)
        self.setAcceptDrops(False)

        self._model.valueChanged.connect(self._set_model_data)
        self._set_stylesheet()

        self.setIndexWidgetSignal.connect(self._set_index_widget)
        self.removeIndexWidgetSignal.connect(self._remove_index_widget)

        self._setup_model()

    def _setup_model(self):
        data = self._split_data_by_breakpoint()
        self._gridViewModel = GridViewModel(self, data=data)
        self.setModel(self._gridViewModel)

        self._set_all_column_stretch_mode()
        self._thread_setup_table_for_visible_indexes()
        self.viewport().update()

    def _thread_setup_table_for_visible_indexes(self):
        global SCROLL_POS
        scroll_position = self.verticalScrollBar().value()
        if SCROLL_POS == scroll_position:
            return
        SCROLL_POS = scroll_position
        self._setup_table_for_visible_indexes()

    def _setup_table_for_visible_indexes(self):
        model = self.model()
        if not model:
            return

        viewport_rect = self.viewport().rect()
        first_row = self.rowAt(viewport_rect.top())
        last_row = self.rowAt(viewport_rect.bottom())
        first_col = self.columnAt(viewport_rect.left())
        last_col = self.columnAt(viewport_rect.right())

        if first_row == -1: first_row = 0
        if last_row == -1: last_row = model.rowCount() - 1
        if first_col == -1: first_col = 0
        if last_col == -1: last_col = model.columnCount() - 1

        visible_indexes = [
            model.index(row, col)
            for row in range(first_row, last_row + 1)
            for col in range(first_col, last_col + 1)
        ]

        for index in self._last_visible_indexes:
            if index not in visible_indexes:
                self.removeIndexWidgetSignal.emit(index)

        self.setIndexWidgetSignal.emit(visible_indexes)
        self._last_visible_indexes = visible_indexes

    def _remove_index_widget(self, index):
        if self.indexWidget(index):
            self.indexWidget(index).deleteLater()
            self.setIndexWidget(index, None)

    def _set_index_widget(self, indexes):
        index_rows = []
        new_visible_indexes = []
        for index in indexes:
            try:
                if not self.indexWidget(index) and not index.parent().isValid():
                    index_row = index.row()
                    index_col = index.column()
                    if index_row not in index_rows:
                        index_rows.append(index_row)

                    new_visible_indexes.append(f"{index_row}{index_col}")

                    widget_info = self.model_data[index_row][index_col]
                    widget = None
                    if isinstance(widget_info, Callable):
                        widget = widget_info()
                    elif isinstance(widget_info, Dict):
                        widget = widget_info["component"](**widget_info["renderProps"])

                    if widget:
                        # self.setIndexWidget(index, widget) # Không làm tăng RAM
                        self._thread_pool.start(QTimer.singleShot(0, lambda index=index, widget=widget: asyncio.ensure_future(self.worker.run(self, index, widget))))  # Chạy setIndexWidget trong thread riêng

                    for row in index_rows:
                        self.setRowHeight(row, self._rowHeight)
            except Exception as e:
                print(f"Error in _set_index_widget: {e}")


    def _set_stylesheet(self):
        self.setStyleSheet("""
            QTableView {
                padding: 0px;
                border: none;
                gridline-color: transparent;
                color: transparent;
            }
            QTableView::item {
                padding-left: 0px;
                padding-right: 0px;
            }
            QTableView::item:selected {
                background-color: transparent;
                color: transparent;
            }
            QTableView::section {
                background-color: transparent;
                text-align: left;
            }
            QTableView::horizontalHeader {
                background-color: transparent;
            }
            QTableView::section:horizontal {
                background-color: transparent;
                padding: 0px;
                border: 1px solid transparent !important;
                border-bottom: 1px solid transparent !important;
            }
            QTableView::section:vertical {
                border: 1px solid transparent;
            }
            QTableView .QScrollBar:horizontal {
                border: none;
                background: transparent;
                border-radius: 0px;
            }
        """)

    def _set_model_data(self, _data):
        data = self._split_data_by_breakpoint()
        self._gridViewModel = GridViewModel(self, data=data)
        self.setModel(self._gridViewModel)
        self._set_all_column_stretch_mode()
        self._setup_table_for_visible_indexes()
        self.viewport().update()

    def _split_data_by_breakpoint(self):
        data = self._model.value
        new_data = []
        temp_row = []

        for i, item in enumerate(data):
            temp_row.append(item)
            if len(temp_row) == self.columnsToShow:
                new_data.append(temp_row)
                temp_row = []

        if temp_row:
            new_data.append(temp_row)

        for i in range(self.columnsToShow):
            self.setItemDelegateForColumn(i, StyledItem(self, new_data))

        self.model_data = new_data
        return new_data

    def _set_all_column_stretch_mode(self):
        for i in range(self.columnsToShow):
            self.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    def resizeEvent(self, event):
        width = self.width()
        if width < 600:
            self.columnsToShow = self.sm
        elif width < 960:
            self.columnsToShow = self.md
        elif width < 1280:
            self.columnsToShow = self.lg
        else:
            self.columnsToShow = self.xl

        if self._columnCount:
            self.columnsToShow = self._columnCount

        self._set_model_data(self._model)
        super().resizeEvent(event)

    def wheelEvent(self, event):
        super().wheelEvent(event)
        self._thread_setup_table_for_visible_indexes()

