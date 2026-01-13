# coding: utf-8
import asyncio
import uuid
import time
from typing import List, Union, Optional, Dict

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QTableWidget, 
    QHeaderView, 
    QWidget, 
    QTableWidgetItem, 
    QStyledItemDelegate, 
    QApplication, 
    QStyleOptionViewItem,
    QTableView, 
    QTableWidget, 
    QWidget, 
    QTableWidgetItem, 
    QStyle,
    QStyleOptionButton, 
    QFrame, 
    QVBoxLayout,
    QProxyStyle,
    QStyleOption,
    QCheckBox,
    QHBoxLayout,
    QScrollBar,
    QSizePolicy,
)
from PySide6.QtCore import (
    Qt, 
    QMargins, 
    QModelIndex, 
    QItemSelectionModel, 
    Property, 
    QRectF, 
    QRect,
    Signal,
    QAbstractTableModel,
    QTimer,
    QRunnable,
    QThreadPool,
)
from PySide6.QtGui import QPainter, QColor, QKeyEvent, QPalette, QBrush, QFont

from typing import TYPE_CHECKING, Callable

from qtmui.hooks import State, useState
from qtmui.utils.translator import getTranslatedText

if TYPE_CHECKING:
    from .table_cell import TableViewCell

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from ...widgets.line_edit import LineEdit


from qtmui.material.styles import useTheme
from ....i18n.use_translation import translate, i18n

from ...py_iconify import PyIconify
from ....qtmui_assets import QTMUI_ASSETS

from ...checkbox import Checkbox
from ...button import Button
from ...box import Box
from ...spacer import HSpacer

from .table_base import TableBase
from .table_item_delegate import TableItemDelegate

INDEXS = []
SCROLL_POS = None


class AbstractTableModel(QAbstractTableModel):
    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return getTranslatedText(self._headerLabels[section])
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return f"{section + 1}"
        
        if role == Qt.TextAlignmentRole:
            # Cài đặt căn chỉnh cho từng cột
            if self._tableHead[section].get("align") == "center":
                return int(Qt.AlignCenter | Qt.AlignVCenter)
            elif self._tableHead[section].get("align") == "right":
                return int(Qt.AlignRight | Qt.AlignVCenter)
            else:  # left
                return int(Qt.AlignLeft | Qt.AlignVCenter)

    def __init__(self, 
                parent=None, 
                tableHead=None, 
                data=None
                ):
        
        self._tableHead = tableHead
        self._headerLabels = [item.get('label') if item.get('label') is not None else ""  for item in tableHead]

        super(AbstractTableModel, self).__init__(parent)

        self._data = data

    def rowCount(self, n=None):
        if isinstance(self._data, list):
            return len(self._data)
        else:
            return 0

    def columnCount(self, n=None):
        return len(self._tableHead)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled

    def data(self, index, role=Qt.ForegroundRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.EditRole:
                try:
                    widget_info = self._data[index.row()][index.column()]
                    return widget_info
                except Exception as e:
                    print('eeeeeeeeeee', e)
                    return ""
            # if role == Qt.ItemDataRole.DisplayRole or role == Qt.EditRole:
            #     if index.column() == 1 or index.column() == 13:
            #         return # khong set text content cho column co widget
            #     try:
            #         value = str(self._data[index.row()][index.column()])
            #     except:
            #         value = None
            #     pass
            #         return value or ""

class ChunkVisibleIndexesRunnable(QRunnable):
    chunkIndexesCalculated = Signal(list, list)  # Signal emit visible_indexes_chunk, to_remove_indexes_chunk

    def __init__(self, table_view, start_row, end_row, first_col, last_col):
        super().__init__()
        self.table_view = table_view
        self.start_row = start_row
        self.end_row = end_row
        self.first_col = first_col
        self.last_col = last_col

    def run(self):
        model = self.table_view.model()
        if not model:
            self.chunkIndexesCalculated.emit([], [])
            return

        # Tính toán index cho chunk rows
        visible_indexes_chunk = []
        for row in range(self.start_row, self.end_row + 1):
            for col in range(self.first_col, self.last_col + 1):
                visible_indexes_chunk.append(model.index(row, col))

        # Tính toán các index cần remove cho chunk (dựa trên _last_visible_indexes toàn cục)
        to_remove_indexes_chunk = [idx for idx in self.table_view._last_visible_indexes if idx.row() >= self.start_row and idx.row() <= self.end_row and idx not in visible_indexes_chunk]

        self.chunkIndexesCalculated.emit(visible_indexes_chunk, to_remove_indexes_chunk)

class TableView(TableBase, QTableView):
    """ Table view """
    setIndexWidgetSignal = Signal(object)
    removeIndexWidgetSignal = Signal(QModelIndex)
    chunkIndexesCalculated = Signal(list, list)

    def __init__(
                self, 
                parent=None,
                fullWidth: bool = True,
                isBorderVisible: bool = False,
                tableHead: list = None,
                children: list = None,
                loading: Optional[Union[bool, State]] = None,
                sortingEnabled: bool = False,
                size: str= None,
                model: object= None,
                dragEnable: Optional[bool]= False,
                dragDropMode: Optional[QTableView.DragDropMode] = None,
                selectionMode: Optional[QTableView.SelectionMode] = None,
                selectionBehavior: Optional[QTableView.SelectionBehavior]= None,
                maxHeight: Optional[int] = None,
                rowHeight: int= 40,
                sx: Optional[Union[dict, State]] = None,
                ):
        super().__init__(parent)
        self._children: list = children
        self._loading = loading
        self._fullWidth = fullWidth
        self._tableHead = tableHead
        self._isBorderVisible = isBorderVisible
        self._sortingEnabled = sortingEnabled
        self._rowHeight = rowHeight
        self._sx = sx
        self._model: State = model
        self._maxHeight: int = maxHeight
        
        self._dragEnable = dragEnable
        self._selectionMode = selectionMode
        self._selectionBehavior = selectionBehavior
        self._dragDropMode = dragDropMode

        self._header_items = []

        self._last_visible_indexes = []

        self._selectedAll, self._setSlectedAll = useState(False)


        self._thread_pool = QThreadPool.globalInstance()  # Sử dụng QThreadPool toàn cục
        self._thread_pool.setMaxThreadCount(max(4, self._thread_pool.maxThreadCount()))  # Đặt tối thiểu 4 luồng

        self._min_chunk_size = 50  # Kích thước chunk tối thiểu, điều chỉnh dựa trên số hàng lớn

        self._init_ui()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        
        if isinstance(self._loading, State):
            self._loading.valueChanged.connect(self._onLoading)
            self._onLoading()

        if self._dragEnable:
            self.setDragEnabled(True)
            if self._selectionMode:
                self.setSelectionMode(self._selectionMode)
            if self._selectionBehavior:
                self.setSelectionBehavior(self._selectionBehavior)
            if self._dragDropMode:
                self.setDragDropMode(self._dragDropMode)


        self.verticalHeader().hide()
        self.setViewportMargins(0, 0, 0, 0)

        if self._sortingEnabled:
            self.setSortingEnabled(True)

        self.theme = useTheme()


        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()


        # table view from gridview
        self.model_data = self._model.value


        # for i in range(len(self.model_data[0])):
        #     # self.setItemDelegateForColumn(i, StyledItem(self))
        #     self.setItemDelegateForColumn(i, TableItemDelegate(self))

        i18n.langChanged.connect(self.__setup_header)

        self.setIndexWidgetSignal.connect(self._set_index_widget)
        self.removeIndexWidgetSignal.connect(self._remove_index_widget)

        self._model.valueChanged.connect(self._set_model_data)
        self._set_model_data(self.model_data)

        scrollbar = self.verticalScrollBar()
        scrollbar.sliderReleased.connect(self.onScrollReleased)

        self.__setup_header()

        # Kết nối signal từ runnable
        # self.chunkIndexesCalculated = Signal(list, list)  # Signal cho visible_indexes_chunk và to_remove_indexes_chunk
        self.chunkIndexesCalculated.connect(self._collect_chunk_results)

    def _onLoading(self, isLoading=None):
        if isinstance(self._loading, State):
            if self._loading.value:
                self.setMaximumHeight(50) # có dòng này mới hiển thị header
                self.viewport().update()
            else:
                self.setMaximumHeight(16777215)
                self.viewport().update()
  

    def __setup_header(self):
        self._horizontalHeader = self.horizontalHeader()

        for colIndex, headerData in enumerate(self._tableHead):
            if headerData.get('width'):
                self._horizontalHeader.setSectionResizeMode(colIndex, QHeaderView.Fixed)
                self.setColumnWidth(colIndex, headerData.get('width'))
            else:
                if headerData.get('columnHidden') == True:
                    self.setColumnHidden(colIndex, True)
                elif headerData.get('resizeMode') == "ResizeToContents":
                    self._horizontalHeader.setSectionResizeMode(colIndex, QHeaderView.ResizeToContents)
                elif headerData.get('resizeMode') == "Stretch":
                    self._horizontalHeader.setSectionResizeMode(colIndex, QHeaderView.Stretch)
                else:
                    self._horizontalHeader.setSectionResizeMode(colIndex, QHeaderView.Interactive)


        # Thêm QCheckBox vào header của cột đầu tiên
        self._selectAllCheckBox = Checkbox(parent=self._horizontalHeader.viewport(), checked=self._selectedAll, size="small", onChange=self._on_select_all)
        self._horizontalHeader.viewport().setLayout(QHBoxLayout())
        self._horizontalHeader.viewport().layout().setContentsMargins(0,0,0,0)
        self._table_toolbar = Box(
            sx={"background-color": self.theme.palette.primary.lighter},
            direction="row",
            children=[
                Checkbox(size="small", onChange=self._on_un_select_all, color="primary", checked=True),
                HSpacer(),
                Button(startIcon=PyIconify(key=QTMUI_ASSETS.ICONS.TRASH), size="small", color="primary")
            ]
        )
        self._table_toolbar.hide()
        self._horizontalHeader.viewport().layout().addWidget(self._table_toolbar)
        self._positionHeaderCheckbox()
        # Khi cột đầu tiên được resize, cập nhật vị trí checkbox
        self._horizontalHeader.sectionResized.connect(lambda idx, oldSize, newSize: self._positionHeaderCheckbox())

    def _set_model_data(self, data=None):
        # self._clear_index_widgets()
        self.setModel(None)

        if not data:
            data = self._model.value

        self._abstractTableModel = AbstractTableModel(self, tableHead=self._tableHead, data=data)
        self.setModel(self._abstractTableModel)
        self._thread_setup_table_for_visible_indexes()

        self.__setup_header()
        self.viewport().update()
        
        # model = self.model()
        # model.rowsInserted.connect(lambda *args: self.updateTableViewHeight(self))
        # model.rowsRemoved.connect(lambda *args: self.updateTableViewHeight(self))
        # model.layoutChanged.connect(lambda: self.updateTableViewHeight(self))


    def onScrollReleased(self) -> None:
        self._thread_setup_table_for_visible_indexes()

    def wheelEvent(self, event) -> None:
        super().wheelEvent(event)
        self._thread_setup_table_for_visible_indexes()
    
    def _thread_setup_table_for_visible_indexes(self):
        global SCROLL_POS

        scroll_position = self.verticalScrollBar().value()
        if SCROLL_POS == scroll_position:
            return
        SCROLL_POS = scroll_position

        viewport_rect = self.viewport().rect()

        # Xác định hàng đầu tiên và hàng cuối cùng trong vùng nhìn thấy
        first_row = self.rowAt(viewport_rect.top())
        last_row = self.rowAt(viewport_rect.bottom())

        # Xác định cột đầu tiên và cột cuối cùng trong vùng nhìn thấy
        first_col = self.columnAt(viewport_rect.left())
        last_col = self.columnAt(viewport_rect.right())

        # Nếu không tìm thấy, set mặc định
        if first_row == -1: first_row = 0
        if last_row == -1: last_row = self.model().rowCount() - 1 if self.model() else 0
        if first_col == -1: first_col = 0
        if last_col == -1: last_col = self.model().columnCount() - 1 if self.model() else 0

        num_rows = last_row - first_row + 1

        # Tính toán chunk size động dựa trên số row và số luồng
        num_threads = self._thread_pool.maxThreadCount()
        if num_rows < self._min_chunk_size * 2:  # Nếu số row nhỏ, không chia chunk, chạy trực tiếp
            self._calculate_visible_indexes_directly(first_row, last_row, first_col, last_col)
            return

        # Chia chunk thông minh: chunk_size tối thiểu _min_chunk_size, số chunk <= num_threads
        chunk_size = max(self._min_chunk_size, num_rows // num_threads)
        num_chunks = max(1, num_rows // chunk_size + (1 if num_rows % chunk_size > 0 else 0))

        start_row = first_row
        self._pending_chunks = num_chunks
        self._visible_indexes_chunks = []
        self._to_remove_indexes_chunks = []

        for i in range(num_chunks):
            end_row = min(start_row + chunk_size - 1, last_row)
            runnable = ChunkVisibleIndexesRunnable(self, start_row, end_row, first_col, last_col)
            runnable.chunkIndexesCalculated.connect(self._collect_chunk_results)
            self._thread_pool.start(runnable)
            start_row = end_row + 1

    def _calculate_visible_indexes_directly(self, first_row, last_row, first_col, last_col):
        model = self.model()
        if not model:
            return

        visible_indexes = []
        for row in range(first_row, last_row + 1):
            for col in range(first_col, last_col + 1):
                visible_indexes.append(model.index(row, col))

        to_remove_indexes = [idx for idx in self._last_visible_indexes if idx not in visible_indexes]

        for index in to_remove_indexes:
            self.removeIndexWidgetSignal.emit(index)

        # Gửi tín hiệu cập nhật các index hiển thị
        self.setIndexWidgetSignal.emit(visible_indexes)
        self._last_visible_indexes = visible_indexes

    def _collect_chunk_results(self, visible_indexes_chunk, to_remove_indexes_chunk):
        self._visible_indexes_chunks.extend(visible_indexes_chunk)
        self._to_remove_indexes_chunks.extend(to_remove_indexes_chunk)

        self._pending_chunks -= 1
        if self._pending_chunks == 0:
            # Khi tất cả chunks hoàn thành, xử lý remove và emit
            for index in self._to_remove_indexes_chunks:
                self.removeIndexWidgetSignal.emit(index)

            # Gửi tín hiệu cập nhật các index hiển thị
            self.setIndexWidgetSignal.emit(self._visible_indexes_chunks)
            self._last_visible_indexes = self._visible_indexes_chunks

    def _clear_index_widgets(self):
        if self.model():
            for row in range(self.model().rowCount()):
                for col in range(self.model().columnCount()):
                    index = self.model().index(row, col)
                    widget = self.indexWidget(index)
                    if widget:
                        # widget.deleteLater()  # Giải phóng bộ nhớ
                        QTimer.singleShot(110, lambda: asyncio.ensure_future(widget.deleteLater()))
                        self.setIndexWidget(index, None)

    def _remove_index_widget(self, index):
        if self.indexWidget(index):
            widget = self.indexWidget(index)
            # QTimer.singleShot(10, lambda widget=widget: asyncio.ensure_future(self._rem(widget, index))) # tránh lỗi ở set_stylesheet
            self._rem(widget, index)

    def _rem(self, widget, index):
        # self.indexWidget(index).deleteLater()
        widget.deleteLater()
        self.setIndexWidget(index, None)

    def _set_index_widget(self, indexs):

        index_rows = []
        totalRowsHeight = 0

        for index in indexs:
            index_row = index.row()
            if index_row not in index_rows:
                index_rows.append(index_row)
            if not self.indexWidget(index) and not index.parent().isValid():
                widget_info = self._model.value[index_row][index.column()]
                widget = None
                if isinstance(widget_info, Callable):
                    widget: TableViewCell = widget_info()
                    widget._indexRow = index_row
                    # print('widget_text________', widget._text)
                    widget.indexRow.connect(self._setHoverRow)
                elif isinstance(widget_info, Dict):
                    widget = widget_info["component"](**widget_info["renderProps"])
                elif isinstance(widget_info, str):
                    pass
                if isinstance(widget, QWidget):
                    self.setIndexWidget(index, widget)


        if self._maxHeight:
            for row in index_rows:
                ## self.setRowHidden(row, True)
                self.resizeRowToContents(row)
                totalRowsHeight += self.rowHeight(row)
            
            if self.height() < self._maxHeight:
                headerHeight = self.horizontalHeader().height()
                self.setFixedHeight(headerHeight + totalRowsHeight)


    ############### fluent funcs
    def isSelectRightClickedRow(self):
        return self._isSelectRightClickedRow

    def setSelectRightClickedRow(self, isSelect: bool):
        self._isSelectRightClickedRow = isSelect

    def getselectedRowsFast(self):
        selectedRows = []
        # for item in self.selectedItems():
        for item in self.selectedIndexes():
            if item.row() not in selectedRows:
                selectedRows.append(item.row())
            selectedRows.sort()
        return selectedRows


    selectRightClickedRow = Property(bool, isSelectRightClickedRow, setSelectRightClickedRow)