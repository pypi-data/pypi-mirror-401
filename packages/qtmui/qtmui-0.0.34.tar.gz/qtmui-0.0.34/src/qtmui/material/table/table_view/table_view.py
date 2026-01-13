# coding: utf-8
import asyncio
import uuid
from typing import  Union, Optional, Dict

from PySide6.QtWidgets import (
    QHeaderView, 
    QWidget, 
    QTableView, 
    QWidget, 
    QHBoxLayout,
)
from PySide6.QtCore import (
    Qt, 
    QModelIndex, 
    Property, 
    Signal,
    QAbstractTableModel,
    QTimer,
    QItemSelection,
)

from typing import TYPE_CHECKING, Callable


from qtmui.utils.translator import getTranslatedText

if TYPE_CHECKING:
    from .table_cell import TableViewCell

from qtmui.hooks import State, useEffect

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.material.styles import useTheme
from ....i18n.use_translation import i18n

from qtmui.material.table.table_head import TableHead

from ...checkbox import Checkbox

from .table_base import TableBase

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
            if self._headLabel[section].get("align") == "center":
                return int(Qt.AlignCenter | Qt.AlignVCenter)
            elif self._headLabel[section].get("align") == "right":
                return int(Qt.AlignRight | Qt.AlignVCenter)
            else:  # left
                return int(Qt.AlignLeft | Qt.AlignVCenter)

    def __init__(self, 
                parent=None, 
                headLabel=None, 
                data=None
                ):
        
        self._headLabel = headLabel
        self._headerLabels = [item.get('label') if item.get('label') is not None else ""  for item in self._headLabel]

        super(AbstractTableModel, self).__init__(parent)

        self._data = data

    def rowCount(self, n=None):
        if isinstance(self._data, list):
            return len(self._data)
        else:
            return 0

    def columnCount(self, n=None):
        return len(self._headLabel)

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

class TableView(TableBase, QTableView):
    """ Table view """
    setIndexWidgetSignal = Signal(object)
    removeIndexWidgetSignal = Signal(QModelIndex)

    def __init__(
                self, 
                parent=None,
                fullWidth: bool = True,
                isBorderVisible: bool = False,
                tableHead: TableHead = None,
                children: list = None,
                loading: Optional[Union[bool, State]] = None,
                sortingEnabled: bool = False,
                size: str= None,
                model: object= None,
                dragEnable: Optional[bool]= False,
                dragDropMode: Optional[QTableView.DragDropMode] = None,
                selectionMode: Optional[QTableView.SelectionMode] = None,
                selectionBehavior: Optional[QTableView.SelectionBehavior]= None,
                onSelectionChanged: Optional[Callable]= None,
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
        self._onSelectionChanged = onSelectionChanged
        self._dragDropMode = dragDropMode

        self._header_items = []

        self._last_visible_indexes = []

        # if self._tableHead and isinstance(self._tableHead._numSelected, State):
        #     self._selected, self._setSelected = useMemo(lambda: self._tableHead._numSelected.value, [self._tableHead._numSelected])
        # else:
        #     self._selected, self._setSelected = useState(0)
            

        self._init_ui()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        
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
        self.setMinimumHeight(50)

        if self._sortingEnabled:
            self.setSortingEnabled(True)

        self.theme = useTheme()


        useEffect(
            self._set_stylesheet,
            [self.theme.state]
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
        
  
    def _onSelectionChange(self, selected: QItemSelection, deselected: QItemSelection):
        """Được gọi khi người dùng thay đổi dòng hoặc ô được chọn"""
        indexes = selected.indexes()
        if indexes:
            row = indexes[0].row()
            # print(f"✅ Dòng được chọn: {self.getselectedRowsFast()}", self._tableHead._tableSelectedAction.isVisible())
            if self._tableHead._tableSelectedAction and not self._tableHead._tableSelectedAction.isVisible():
                self._tableHead._tableSelectedAction.setVisible(True)
            
        else:
            # print("❌ Không có dòng nào được chọn")
            if self._tableHead._tableSelectedAction.isVisible():
                self._tableHead._tableSelectedAction.setVisible(False)
        
        if self._onSelectionChanged:
            self._onSelectionChanged(self.getselectedRowsFast())
                
                
    def _onSelectAllChanged(self, checked=None):
        if checked:
            self.selectAll() 
            if not self._tableHead._tableSelectedAction.isVisible():
                self._tableHead._tableSelectedAction.setVisible(True)
            if self._tableHead._onSelectAllRows:
                # self._tableHead._onSelectAllRows(checked, self.getselectedRowsFast())
                self._tableHead._onSelectAllRows(checked)
        else:
            self.clearSelection()
            # self._selected.setValue(False)
            if self._tableHead._tableSelectedAction.isVisible():
                self._tableHead._tableSelectedAction.setVisible(False)
        
            
    def __setup_header(self):
        self._horizontalHeader = self.horizontalHeader()

        for colIndex, headerData in enumerate(self._tableHead._headLabel):
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
        # self._selectAllCheckBox = Checkbox(parent=self._horizontalHeader.viewport(), checked=self._selected, size="small", onChange=self._onSelectAllChanged)
        self._selectAllCheckBox = Checkbox(parent=self._horizontalHeader.viewport(), checked=self._tableHead._numSelected, size="small", onChange=self._onSelectAllChanged)
        # self._selectAllCheckBox = Checkbox(parent=self._horizontalHeader.viewport(), checked=False, size="small", onChange=self._onSelectAllChanged)
        self._horizontalHeader.viewport().setLayout(QHBoxLayout())
        self._horizontalHeader.viewport().layout().setContentsMargins(0,0,0,0)
        if self._tableHead._tableSelectedAction:
            self._horizontalHeader.viewport().layout().addWidget(self._tableHead._tableSelectedAction)
            self._tableHead._tableSelectedAction.setVisible(False)
        self._positionHeaderCheckbox()
        # Khi cột đầu tiên được resize, cập nhật vị trí checkbox
        self._horizontalHeader.sectionResized.connect(lambda idx, oldSize, newSize: self._positionHeaderCheckbox())

    def _set_model_data(self, data=None):
        self.setModel(None)

        if not data:
            data = self._model.value

        self._abstractTableModel = AbstractTableModel(self, headLabel=self._tableHead._headLabel, data=data)
        
        self.setModel(self._abstractTableModel)
        
        self._setup_table_for_visible_indexes()

        self.__setup_header()
        
        if not data:
            self.setMaximumHeight(50) # có dòng này mới hiển thị header
        else:
            self.setMaximumHeight(16777215)
        
        self.viewport().update()

        # # 🔥 Sau khi setModel xong thì selectionModel() mới tồn tại
        if self.selectionModel():
            self.selectionModel().selectionChanged.connect(self._onSelectionChange)
        
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
        self._setup_table_for_visible_indexes()

    def _setup_table_for_visible_indexes(self):
        """
        Hàm này trả về danh sách các chỉ số (index) hiện đang nằm trong vùng hiển thị của QTableView.
        """
        model = self.model()
        if not model:
            return []

        viewport_rect = self.viewport().rect()

        # Xác định hàng đầu tiên và hàng cuối cùng trong vùng nhìn thấy
        first_row = self.rowAt(viewport_rect.top())
        last_row = self.rowAt(viewport_rect.bottom())

        # Xác định cột đầu tiên và cột cuối cùng trong vùng nhìn thấy
        first_col = self.columnAt(viewport_rect.left())
        last_col = self.columnAt(viewport_rect.right())

        # Nếu không tìm thấy, set mặc định
        if first_row == -1: first_row = 0
        if last_row == -1: last_row = model.rowCount() - 1
        if first_col == -1: first_col = 0
        if last_col == -1: last_col = model.columnCount() - 1

        # Lấy danh sách index trong vùng hiển thị (dùng list comprehension)
        visible_indexes = [
            model.index(row, col)
            for row in range(first_row, last_row + 1)
            for col in range(first_col, last_col + 1)
        ]

        for index in self._last_visible_indexes:
            if index not in visible_indexes:
                self.removeIndexWidgetSignal.emit(index)
        # Gửi tín hiệu cập nhật các index hiển thị
        self.setIndexWidgetSignal.emit(visible_indexes)
        self._last_visible_indexes = visible_indexes

        # for index in range(first_row, last_row):
        #     self.setRowHeight(index, self._rowHeight)


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
            QTimer.singleShot(10, lambda widget=widget: asyncio.ensure_future(self._rem(widget, index))) # tránh lỗi ở set_stylesheet

    async def _rem(self, widget, index):
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

