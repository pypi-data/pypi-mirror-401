# coding: utf-8
import uuid
from typing import List, Union, Optional, Dict, TYPE_CHECKING, Callable

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QTableWidget, 
    QHeaderView, 
    QWidget, 
    QTableWidgetItem, 
    QApplication, 
    QTableWidget, 
    QWidget, 
    QTableWidgetItem, 
    QProxyStyle,
    QStyleOption,
    QHBoxLayout,
)
from PySide6.QtCore import (
    Qt, 
    Property, 
    QRect,
)

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from .table_row import TableRow

from qtmui.hooks import useState

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style


from qtmui.material.styles import useTheme
from ....i18n.use_translation import translate, i18n

from .table_base import TableBase


class TableWidget(TableBase, QTableWidget):

    def __init__(
                self,
                fullWidth: bool = True,
                isBorderVisible: bool = False,
                tableHead: list = None,
                children: list = None,
                sortingEnabled: bool = False,
                size: str= None,
                sx: Optional[Union[Callable, str, Dict]]= None
                ):
        super().__init__()

        self._children: list[TableRow] = children
        self._fullWidth = fullWidth
        self._tableHead = tableHead
        self._isBorderVisible = isBorderVisible
        self._sortingEnabled = sortingEnabled
        self._sx = sx

        self._header_items = []

        self._selectedAll, self._setSlectedAll = useState(False)

        self._init_ui()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))

        self.setColumnCount(len(self._tableHead))
        self.verticalHeader().hide()
        self.setViewportMargins(0, 0, 0, 0)

        if self._sortingEnabled:
            self.setSortingEnabled(True)

        self.theme = useTheme()

        self._setup_header()

        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

        i18n.langChanged.connect(self._setup_header)

        self.update_data()



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
                    item = QTableWidgetItem(_cell)
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


