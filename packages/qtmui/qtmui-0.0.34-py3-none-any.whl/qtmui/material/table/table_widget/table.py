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

from .table_widget import TableWidget
from .table_view import TableView

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

