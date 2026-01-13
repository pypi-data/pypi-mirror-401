# coding: utf-8
import uuid
from typing import List, Union, Optional, Dict

from PySide6.QtWidgets import (QTableWidget, QHeaderView, QWidget, QTableWidgetItem, QStyledItemDelegate, QApplication, QStyleOptionViewItem,
                             QTableView, QTableWidget, QWidget, QTableWidgetItem, QStyle,
                             QStyleOptionButton, QFrame, QVBoxLayout)
from PySide6.QtCore import Qt, QMargins, QModelIndex, QItemSelectionModel, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QKeyEvent, QPalette, QBrush, QFont

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from .table_row import TableRow

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.material.styles import useTheme
from ....i18n.use_translation import translate, i18n

from ....common.font import getFont
from ....common.style_sheet import isDarkTheme, FluentStyleSheet, themeColor, setCustomStyleSheet
from ...widgets.check_box import CheckBoxIcon
from ...widgets.line_edit import LineEdit
from ...widgets.scroll_bar import SmoothScrollDelegate


class TableItemDelegate(QStyledItemDelegate):

    def __init__(self, parent: QTableView):
        super().__init__(parent)
        self.margin = 2
        self.hoverRow = -1
        self.pressedRow = -1
        self.selectedRows = set()

    def setHoverRow(self, row: int):
        # print('setHoverRow__________', row)
        self.hoverRow = row

    def setPressedRow(self, row: int):
        self.pressedRow = row

    def setSelectedRows(self, indexes: List[QModelIndex]):
        self.selectedRows.clear()
        for index in indexes:
            self.selectedRows.add(index.row())
            if index.row() == self.pressedRow:
                self.pressedRow = -1

    def sizeHint(self, option, index):
        # increase original sizeHint to accommodate space needed for border
        size = super().sizeHint(option, index)
        size = size.grownBy(QMargins(0, self.margin, 0, self.margin))
        return size

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        lineEdit = LineEdit(parent)
        lineEdit.setProperty("transparent", False)
        lineEdit.setStyle(QApplication.style())
        lineEdit.setText(option.text)
        lineEdit.setClearButtonEnabled(True)
        return lineEdit

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        rect = option.rect
        y = rect.y() + (rect.height() - editor.height()) // 2
        x, w = max(8, rect.x()), rect.width()
        if index.column() == 0:
            w -= 8

        editor.setGeometry(x, y, w, rect.height())

    def _drawBackground(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        """ draw row background """
        r = 5
        if index.column() == 0:
            rect = option.rect.adjusted(4, 0, r + 1, 0)
            painter.drawRoundedRect(rect, r, r)
        elif index.column() == index.model().columnCount(index.parent()) - 1:
            rect = option.rect.adjusted(-r - 1, 0, -4, 0)
            painter.drawRoundedRect(rect, r, r)
        else:
            rect = option.rect.adjusted(-1, 0, 1, 0)
            painter.drawRect(rect)

    def _drawIndicator(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        """ draw indicator """
        y, h = option.rect.y(), option.rect.height()
        ph = round(0.35*h if self.pressedRow == index.row() else 0.257*h)
        painter.setBrush(QBrush(QColor(useTheme().palette.primary.main)))
        painter.drawRoundedRect(4, ph + y, 3, h - 2*ph, 1.5, 1.5)

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)

        # font
        option.font = index.data(Qt.FontRole) or getFont(13)

        # text color
        textColor = Qt.white if isDarkTheme() else Qt.black
        textBrush = index.data(Qt.ForegroundRole)   # type: QBrush
        if textBrush is not None:
            textColor = textBrush.color()

        option.palette.setColor(QPalette.Text, textColor)
        option.palette.setColor(QPalette.HighlightedText, textColor)

    def paint(self, painter, option, index):
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)

        # set clipping rect of painter to avoid painting outside the borders
        painter.setClipping(True)
        painter.setClipRect(option.rect)

        # call original paint method where option.rect is adjusted to account for border
        option.rect.adjust(0, self.margin, 0, -self.margin)

        # draw highlight background
        isHover = self.hoverRow == index.row()
        isPressed = self.pressedRow == index.row()
        isAlternate = index.row() % 2 == 0 and self.parent().alternatingRowColors()
        isDark = isDarkTheme()

        c = 255 if isDark else 0
        alpha = 0

        if index.row() not in self.selectedRows:
            if isPressed:
                alpha = 9 if isDark else 6
            elif isHover:
                alpha = 12
            elif isAlternate:
                alpha = 5
        else:
            if isPressed:
                alpha = 15 if isDark else 9
            elif isHover:
                alpha = 25
            else:
                alpha = 17

        if index.data(Qt.ItemDataRole.BackgroundRole):
            painter.setBrush(index.data(Qt.ItemDataRole.BackgroundRole))
        else:
            painter.setBrush(QColor(c, c, c, alpha))

        self._drawBackground(painter, option, index)

        # draw indicator
        if index.row() in self.selectedRows and index.column() == 0 and self.parent().horizontalScrollBar().value() == 0:
            self._drawIndicator(painter, option, index)

        if index.data(Qt.CheckStateRole) is not None:
            self._drawCheckBox(painter, option, index)

        painter.restore()
        super().paint(painter, option, index)

    def _drawCheckBox(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()
        checkState = Qt.CheckState(index.data(Qt.ItemDataRole.CheckStateRole))

        isDark = isDarkTheme()

        r = 4.5
        x = option.rect.x() + 15
        y = option.rect.center().y() - 9.5
        rect = QRectF(x, y, 19, 19)

        if checkState == Qt.CheckState.Unchecked:
            painter.setBrush(QColor(0, 0, 0, 26) if isDark else QColor(0, 0, 0, 6))
            painter.setPen(QColor(255, 255, 255, 142) if isDark else QColor(0, 0, 0, 122))
            painter.drawRoundedRect(rect, r, r)
        else:
            painter.setPen(QColor(useTheme().palette.primary.main))
            painter.setBrush(QColor(useTheme().palette.primary.main))
            painter.drawRoundedRect(rect, r, r)

            if checkState == Qt.CheckState.Checked:
                CheckBoxIcon.ACCEPT.render(painter, rect)
            else:
                CheckBoxIcon.PARTIAL_ACCEPT.render(painter, rect)

        painter.restore()



class TableBase:
    """ Table base class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delegate = TableItemDelegate(self)
        self.scrollDelagate = SmoothScrollDelegate(self)
        self._isSelectRightClickedRow = False

        # set style sheet
        # FluentStyleSheet.TABLE_VIEW.apply(self)

        self.setShowGrid(False)
        self.setMouseTracking(True)
        self.setAlternatingRowColors(True)
        self.setItemDelegate(self.delegate)
        self.setSelectionBehavior(TableWidget.SelectRows)
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setHighlightSections(False)
        self.verticalHeader().setDefaultSectionSize(38)

        self.entered.connect(lambda i: self._setHoverRow(i.row()))
        self.pressed.connect(lambda i: self._setPressedRow(i.row()))
        self.verticalHeader().sectionClicked.connect(self.selectRow)

        self.setBorderVisible(True)

    def setBorderVisible(self, isVisible: bool):
        """ set the visibility of border """
        self.setProperty("isBorderVisible", isVisible)
        # self.setStyle(QApplication.style())

    def setBorderRadius(self, radius: int):
        """ set the radius of border """
        qss = f"QTableView{{border-radius: {radius}px}}"
        setCustomStyleSheet(self, qss, qss)

    def _setHoverRow(self, row: int):
        """ set hovered row """
        self.delegate.setHoverRow(row)
        self.viewport().update()

    def _setPressedRow(self, row: int):
        """ set pressed row """
        self.delegate.setPressedRow(row)
        self.viewport().update()

    def _setSelectedRows(self, indexes: List[QModelIndex]):
        self.delegate.setSelectedRows(indexes)
        self.viewport().update()

    def leaveEvent(self, e):
        QTableView.leaveEvent(self, e)
        self._setHoverRow(-1)

    def resizeEvent(self, e):
        QTableView.resizeEvent(self, e)
        self.viewport().update()

    def keyPressEvent(self, e: QKeyEvent):
        QTableView.keyPressEvent(self, e)
        self.updateSelectedRows()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton or self._isSelectRightClickedRow:
            return QTableView.mousePressEvent(self, e)

        index = self.indexAt(e.pos())
        if index.isValid():
            self._setPressedRow(index.row())

        QWidget.mousePressEvent(self, e)

    def mouseReleaseEvent(self, e):
        QTableView.mouseReleaseEvent(self, e)
        self.updateSelectedRows()

        if self.indexAt(e.pos()).row() < 0 or e.button() == Qt.RightButton:
            self._setPressedRow(-1)

    def setItemDelegate(self, delegate: TableItemDelegate):
        self.delegate = delegate
        super().setItemDelegate(delegate)

    def selectAll(self):
        QTableView.selectAll(self)
        self.updateSelectedRows()

    def selectRow(self, row: int):
        QTableView.selectRow(self, row)
        self.updateSelectedRows()

    def clearSelection(self):
        QTableView.clearSelection(self)
        self.updateSelectedRows()

    def setCurrentIndex(self, index: QModelIndex):
        QTableView.setCurrentIndex(self, index)
        self.updateSelectedRows()

    def updateSelectedRows(self):
        self._setSelectedRows(self.selectedIndexes())

class CustomHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

        self.theme = useTheme()

        # Màu nền của header
        self._headerBackgroundColor = QColor(self.theme.palette.background.paper)  # Màu nền
        # Màu của border
        self._borderColor = QColor(0, 0, 0)  # Màu đường viền
        self._borderWidth = 2  # Độ dày của đường viền

    def _set_theme(self):
        self.theme = useTheme()
        self._headerBackgroundColor = QColor(self.theme.palette.background.paper)  # Màu nền


    def paintSection(self, painter, rect, logicalIndex):
        # Lấy tiêu đề của cột
        title = self.model().headerData(logicalIndex, self.orientation())

        painter.save()

        # Tô màu nền cho header
        painter.setBrush(self._headerBackgroundColor)
        painter.fillRect(rect, self._headerBackgroundColor)

        # Cài đặt màu sắc cho viền
        painter.setPen(self._borderColor)
        painter.setBrush(Qt.NoBrush)

        # Vẽ viền trên bên trái
        painter.setPen(QColor(0, 0, 0))  # Màu viền cho phần này
        painter.drawLine(rect.left(), rect.top(), rect.left() + self._borderWidth, rect.top())  # Border trên trái
        painter.drawLine(rect.left(), rect.top(), rect.left(), rect.top() + self._borderWidth)  # Border trái trên

        # Vẽ viền trên bên phải
        painter.drawLine(rect.right(), rect.top(), rect.right() - self._borderWidth, rect.top())  # Border trên phải
        painter.drawLine(rect.right(), rect.top(), rect.right(), rect.top() + self._borderWidth)  # Border phải trên

        # Vẽ đường viền xung quanh (toàn bộ header)
        painter.setPen(self._borderColor)
        painter.drawRect(rect)  # Vẽ đường viền chung cho header

        # Vẽ tiêu đề của cột, căn giữa
        textRect = rect
        textRect.setLeft(rect.left() + 5)  # Thêm khoảng cách bên trái để tránh dính vào cạnh
        textRect.setRight(rect.right() - 5)  # Thêm khoảng cách bên phải

        # Vẽ văn bản tiêu đề của cột
        painter.setPen(self.palette().color(self.foregroundRole()))
        painter.setFont(self.font())
        painter.drawText(textRect, Qt.AlignLeft | Qt.AlignVCenter, title)

        painter.restore()

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        
        # Tô màu nền của header
        painter.fillRect(rect, self._headerBackgroundColor)

        # Vẽ tiêu đề của cột
        title = self.model().headerData(logicalIndex, self.orientation(), Qt.DisplayRole)
        if title:
            painter.setPen(QColor(self.theme.palette.text.primary))
            font = self.font()
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignLeft, title)
            painter.drawLine(rect.right(), rect.top(), rect.right(), rect.bottom())  # Border trên phải


        painter.restore()

class TableWidget(TableBase, QTableWidget):
    def __init__(
                self,
                fullWidth: bool = True,
                isBorderVisible: bool = True,
                tableHead: list = None,
                children: list = None,
                size: str= None,
                sx: Optional[Union[Callable, str, Dict]]= None
                ):
        super().__init__()

        self._children: list[TableRow] = children
        self._fullWidth = fullWidth
        self._tableHead = tableHead
        self._isBorderVisible = isBorderVisible
        self._sx = sx

        self._custom_header = None
        self._header_items = []

        self._init_ui()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))

        self.setColumnCount(len(self._tableHead))
        self.verticalHeader().hide()
        self.setViewportMargins(0, 0, 0, 0)

        self.theme = useTheme()

        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()

        self._horizontalHeader = self.horizontalHeader()
        # Kết nối tín hiệu sectionClicked của horizontal header để xử lý checkbox ở cột đầu tiên
        # self._horizontalHeader.sectionClicked.connect(self._on_select_all)

        
        for index, item in enumerate(self._tableHead):
            # if item.get('resizeMode') == "ResizeToContents":
            #     self._horizontalHeader.setSectionResizeMode(index, QHeaderView.ResizeToContents)
            # if item.get('resizeMode') == "Fixed":
            #     self._horizontalHeader.setSectionResizeMode(index, QHeaderView.Fixed)
            #     self.setColumnWidth(index, item.get('width'))
            # if item.get('resizeMode') == "Stretch":
            #     self._horizontalHeader.setSectionResizeMode(index, QHeaderView.Stretch)
            # if item.get('columnHidden') == True:
            #     self.setColumnHidden(index, True)



            if item.get('width'):
                self._horizontalHeader.setSectionResizeMode(index, QHeaderView.Fixed)
                self.setColumnWidth(index, item.get('width'))
            else:
                if item.get('columnHidden') == True:
                    self.setColumnHidden(index, True)
                elif item.get('resizeMode') == "ResizeToContents":
                    self._horizontalHeader.setSectionResizeMode(index, QHeaderView.ResizeToContents)
                else:
                    self._horizontalHeader.setSectionResizeMode(index, QHeaderView.Stretch)

        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

        self.update_data()

    def retranslateUi(self):
        # Cài đặt các tiêu đề cột và căn chỉnh
        self.headerLabels = []

        for colIndex, headerData in enumerate(self._tableHead):
            self.headerLabels.append(headerData.get("label") or "")
            # Cài đặt tiêu đề cột
            if isinstance(headerData.get("label"), Callable):
                header_item = QTableWidgetItem(translate(headerData["label"]))
            else:
                header_item = QTableWidgetItem(headerData.get("label") or "")

            # header_item.setBackground(QBrush(QColor("#FF0000")))  # Đỏ
            
            # Nếu là cột đầu tiên, thêm thuộc tính checkable và đặt trạng thái mặc định là Unchecked
            if colIndex == 0:
                # header_item.setFlags(header_item.flags() | Qt.ItemIsUserCheckable)
                header_item.setFlags(Qt.ItemIsSelectable)
                header_item.setCheckState(Qt.Unchecked)
                
            # # Cài đặt căn chỉnh cho từng cột
            # if headerData.get("align") == "center":
            #     header_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            # elif headerData.get("align") == "right":
            #     header_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            # else:  # center
            #     header_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.setHorizontalHeaderItem(colIndex, header_item)
            # self._header_items.append(header_item)

            # self.viewport().update()

        # self.setHorizontalHeaderLabels(self.headerLabels)
        # self._custom_header = CustomHeaderView(Qt.Horizontal, self)
        # self.setHorizontalHeader(self._custom_header)

    def _set_stylesheet(self, _theme=None):
        self.theme = useTheme()
        component_styles = self.theme.components

        if self._isBorderVisible:
            self.setProperty("isBorderVisible", True)
            self.setStyle(QApplication.style())

        PyTableWidget_root_qss = component_styles["PyTableWidget"].get("styles")["root"]

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx)
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx)
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx


        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {PyTableWidget_root_qss}
                    {sx_qss}
                }}
            """
        )

        if self._custom_header:
            self._custom_header._set_theme()
            # self._custom_header.update()
            self.viewport().update()
            # self._custom_header.headerDataChanged.emit(Qt.Horizontal, 0, self.columnCount() - 1)
            self._custom_header.headerDataChanged(Qt.Horizontal, 0, self.columnCount() - 1)



        # if len(self._header_items):
        #     for header_item in self._header_items:
        #         if isinstance(header_item, QTableWidgetItem):
        #             # header_item.setBackground(QBrush(self.theme.palette.primary.main))
        #             header_item.setForeground(QBrush(QColor(self.theme.palette.primary.main)))  # Đỏ
        #             self.viewport().update()


    # def _on_select_all(self, logicalIndex):
    #     # Chỉ xử lý sự kiện click cho cột đầu tiên (checkbox)
    #     if logicalIndex == 0:
    #         item = self.horizontalHeaderItem(0)
    #         if item.checkState() == Qt.Checked:
    #             item.setCheckState(Qt.Unchecked)
    #             self.selectAll()
    #             # self.selectAll.emit(False)
    #         else:
    #             item.setCheckState(Qt.Checked)
    #             self.selectAll()
    #             # self.selectAll.emit(True)


    def update_data(self, rows=None):
        if rows is not None:
            self._children = rows
        if self._children is None:
            return
        self.setRowCount(len(self._children))

        for rowIndex, row in enumerate(self._children):
            cells = self._children[rowIndex]._data
            for column, _cell in enumerate(cells):
                if isinstance(_cell, QWidget):
                    self.setCellWidget(rowIndex, column, _cell)
                elif isinstance(_cell, Callable):
                    data = _cell()
                    if isinstance(data, str):
                        item = QTableWidgetItem(data)
                        self.setItem(rowIndex, column, item)
                    elif isinstance(data, QWidget):
                        if hasattr(data, "_indexRow"):
                            data._indexRow = rowIndex
                        self.setCellWidget(rowIndex, column, data)
                else:
                    # Thay đổi màu văn bản của các hàng chẵn và lẻ
                    item = QTableWidgetItem(_cell)
                    # item.setForeground(QBrush(QColor(self.theme.palette.grey._700 if self.theme.palette.mode == "light" else self.theme.palette.grey._100)))  # Đỏ
                    # if rowIndex % 2 == 0:  # Dòng chẵn
                    #     item.setForeground(QBrush(self.theme.palette.text.secondary))  # Đỏ
                    # else:  # Dòng lẻ
                    #     item.setForeground(QBrush(QColor(0, 0, 255)))  # Xanh dương
                    self.setItem(rowIndex, column, item)

        self.resizeRowsToContents()

    def setCurrentCell(self, row: int, column: int, command=None):
        self.setCurrentItem(self.item(row, column), command)

    def setCurrentItem(self, item: QTableWidgetItem, command=None):
        if not command:
            super().setCurrentItem(item)
        else:
            super().setCurrentItem(item, command)

        self.updateSelectedRows()

    def setCurrentCell(self, row: int, column: int, command=None):
        self.setCurrentItem(self.item(row, column), command)

    def setCurrentItem(self, item: QTableWidgetItem, command=None):
        if not command:
            super().setCurrentItem(item)
        else:
            super().setCurrentItem(item, command)

        self.updateSelectedRows()

    def isSelectRightClickedRow(self):
        return self._isSelectRightClickedRow

    def setSelectRightClickedRow(self, isSelect: bool):
        self._isSelectRightClickedRow = isSelect

    selectRightClickedRow = Property(bool, isSelectRightClickedRow, setSelectRightClickedRow)


class TableView(TableBase, QTableView):
    """ Table view """

    def __init__(self, parent=None):
        super().__init__(parent)

    def isSelectRightClickedRow(self):
        return self._isSelectRightClickedRow

    def setSelectRightClickedRow(self, isSelect: bool):
        self._isSelectRightClickedRow = isSelect

    selectRightClickedRow = Property(bool, isSelectRightClickedRow, setSelectRightClickedRow)


class Table(QFrame):
    def __init__(
                self,
                **kwargs
                ):
        super().__init__()

        self._kwargs = kwargs

        self._children = kwargs.get("children")
        self._sx = kwargs.get("sx")

        self._init_ui()

    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        if self._kwargs.get("tableHead"):
            self.layout().addWidget(
                TableWidget(**self._kwargs)
            )

        elif self._children:
            for widget in self._children:
                self.layout().addWidget(widget)

    def _set_style_sheet(self):
        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx)
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx)
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx


        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {sx_qss}
                }}
            """
        )