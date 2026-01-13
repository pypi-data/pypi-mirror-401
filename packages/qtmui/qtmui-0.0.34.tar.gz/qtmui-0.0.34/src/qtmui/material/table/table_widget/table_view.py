# coding: utf-8
import uuid
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
)
from PySide6.QtCore import (
    Qt, 
    QMargins, 
    QModelIndex, 
    QItemSelectionModel, 
    Property, 
    QRectF, 
    QRect,
)
from PySide6.QtGui import QPainter, QColor, QKeyEvent, QPalette, QBrush, QFont

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from .table_row import TableRow

from qtmui.hooks import useState

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style


from qtmui.material.styles import useTheme
from ....i18n.use_translation import translate, i18n

from ....common.font import getFont
from ....common.style_sheet import isDarkTheme, FluentStyleSheet, themeColor, setCustomStyleSheet
from ...widgets.check_box import CheckBoxIcon
from ...widgets.line_edit import LineEdit
from ...py_iconify import PyIconify
from ...widgets.scroll_bar import SmoothScrollDelegate
from ....qtmui_assets import QTMUI_ASSETS

from ...checkbox import Checkbox
from ...button import Button
from ...box import Box
from ...spacer import HSpacer

from .table_base import TableBase

class TableView(TableBase, QTableView):
    """ Table view """

    def __init__(
                self, 
                parent=None,
                fullWidth: bool = True,
                isBorderVisible: bool = False,
                tableHead: list = None,
                children: list = None,
                sortingEnabled: bool = False,
                size: str= None,
                sx: Optional[Union[Callable, str, Dict]]= None
                ):
        super().__init__(parent)
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

    def isSelectRightClickedRow(self):
        return self._isSelectRightClickedRow

    def setSelectRightClickedRow(self, isSelect: bool):
        self._isSelectRightClickedRow = isSelect

    selectRightClickedRow = Property(bool, isSelectRightClickedRow, setSelectRightClickedRow)

