# coding: utf-8
from typing import List, Callable


from PySide6.QtWidgets import (
    QTableWidget, 
    QHeaderView, 
    QWidget, 
    QTableWidgetItem, 
    QTableView, 
    QTableWidget, 
    QWidget, 
    QTableWidgetItem, 
    QProxyStyle,
    QStyleOption,
    QHBoxLayout,
    QApplication,
)
from PySide6.QtCore import (
    Qt, 
    QModelIndex, 
    QRect, 
)

from ...py_iconify import PyIconify
from ....qtmui_assets import QTMUI_ASSETS

from ...checkbox import Checkbox
from ...button import Button
from ...box import Box
from ...spacer import HSpacer


from PySide6.QtGui import QKeyEvent

from ....common.style_sheet import setCustomStyleSheet

from ...widgets.scroll_bar import SmoothScrollDelegate
from ....i18n.use_translation import translate, i18n
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from.table_item_delegate import TableItemDelegate

class TableBase:
    """ Table base class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delegate = TableItemDelegate(self)
        # self.scrollDelagate = SmoothScrollDelegate(self)
        self._isSelectRightClickedRow = False

        # set style sheet
        # FluentStyleSheet.TABLE_VIEW.apply(self)

        self.setShowGrid(False)
        self.setMouseTracking(True)
        self.setAlternatingRowColors(True)
        self.setItemDelegate(self.delegate)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setHighlightSections(False)
        self.verticalHeader().setDefaultSectionSize(38)

        self.entered.connect(lambda i: self._setHoverRow(i.row()))
        self.pressed.connect(lambda i: self._setPressedRow(i.row()))
        self.verticalHeader().sectionClicked.connect(self.selectRow)

        self.setBorderVisible(False)


    def _setup_header(self):
        self._horizontalHeader = self.horizontalHeader()

        for colIndex, headerData in enumerate(self._tableHead):
            if isinstance(headerData.get("label"), Callable):
                header_item = QTableWidgetItem(translate(headerData["label"]), aligment=Qt.AlignmentFlag.AlignLeft)
            else:
                header_item = QTableWidgetItem(headerData.get("label") or "")

            # Cài đặt căn chỉnh cho từng cột
            if headerData.get("align") == "center":
                header_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            elif headerData.get("align") == "right":
                header_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            else:  # left
                header_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.setHorizontalHeaderItem(colIndex, header_item)

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

    def _positionHeaderCheckbox(self):
        # Lấy vùng của cột đầu tiên
        # Tính toán vị trí của cột đầu tiên dựa trên sectionPosition và sectionSize
        x = self._horizontalHeader.sectionPosition(0)
        w = self._horizontalHeader.sectionSize(0)
        h = self._horizontalHeader.height()
        rect = QRect(x, 0, w, h)
        margin = 8
        checkSize = 16
        # Đặt checkbox nằm bên trong header cell, cách mép trái margin
        self._selectAllCheckBox.setGeometry(rect.left() + margin,
                                             rect.top() + (rect.height() - checkSize) // 2 -8,
                                             checkSize,
                                             checkSize)

    def _on_select_all(self, state):
        self.selectAll() 
        if not self._table_toolbar.isVisible():
            self._table_toolbar.show()

    def _on_un_select_all(self, state):
        self._setSlectedAll(False)
        if self._table_toolbar.isVisible():
            self._table_toolbar.hide()

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
                {PyTableWidget_root_qss}
                {sx_qss}
            """
        )
        

    def setBorderVisible(self, isVisible: bool):
        """ set the visibility of border """
        self.setProperty("isBorderVisible", isVisible)
        self.setStyle(QApplication.style())

    def setBorderRadius(self, radius: int):
        """ set the radius of border """
        qss = f"QTableView{{border-radius: {radius}px}}"
        # setCustomStyleSheet(self, qss, qss)

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


 