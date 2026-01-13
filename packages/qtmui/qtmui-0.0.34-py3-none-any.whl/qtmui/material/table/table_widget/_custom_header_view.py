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

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.material.styles import useTheme
from ....i18n.use_translation import translate, i18n

from ....common.font import getFont
from ....common.style_sheet import isDarkTheme, FluentStyleSheet, themeColor, setCustomStyleSheet
from ...widgets.check_box import CheckBoxIcon
from ...widgets.line_edit import LineEdit
from ...py_iconify import PyIconify
from ...widgets.scroll_bar import SmoothScrollDelegate
from ...._____assets import ASSETS

from ...checkbox import Checkbox
from ...button import Button
from ...box import Box


class CustomHeaderViewCheckbox(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.theme = useTheme()
        # Màu nền của header
        self._headerBackgroundColor = QColor(self.theme.palette.background.content)
        # Màu của border
        self._borderColor = QColor(0, 0, 0)
        self._borderWidth = 2
        # Thuộc tính trạng thái checkbox (mặc định Off)
        self._checkboxChecked = False

    def _set_theme(self):
        self.theme = useTheme()
        self._headerBackgroundColor = QColor(self.theme.palette.background.content)

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()

        # Vẽ đường viền xung quanh header section
        painter.setPen(self._borderColor)
        painter.drawRect(rect)

        # Nếu là cột thứ nhất, vẽ thêm checkbox trước tiêu đề
        if logicalIndex == 0:
            # Xác định kích thước và vị trí của checkbox
            constMargin = 5
            checkBoxSize = 16
            checkBoxRect = QRect(rect.left() + constMargin,
                                 rect.top() + (rect.height() - checkBoxSize) // 2,
                                 checkBoxSize,
                                 checkBoxSize)

            # Tạo QStyleOptionButton cho checkbox
            option = QStyleOptionButton()
            option.rect = checkBoxRect
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self._checkboxChecked:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off

            # Vẽ checkbox
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

            # Điều chỉnh vùng vẽ tiêu đề để không bị che bởi checkbox
            textRect = QRect(checkBoxRect.right() + constMargin,
                             rect.top(),
                             rect.width() - checkBoxRect.width() - 2 * constMargin,
                             rect.height())
        else:
            # Với các cột khác, sử dụng toàn bộ rect cho tiêu đề
            textRect = rect

        # Lấy tiêu đề từ model
        title = self.model().headerData(logicalIndex, self.orientation(), Qt.DisplayRole)
        if title:
            painter.setPen(QColor(self.theme.palette.text.primary))
            font = self.font()
            font.setBold(True)
            painter.setFont(font)
            # Vẽ tiêu đề căn giữa theo chiều dọc và căn trái theo chiều ngang
            painter.drawText(textRect, Qt.AlignLeft | Qt.AlignVCenter, str(title))

        painter.restore()


class CustomHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

        self.theme = useTheme()

        # Màu nền của header
        self._headerBackgroundColor = QColor(self.theme.palette.background.content)  # Màu nền
        # Màu của border
        self._borderColor = QColor(0, 0, 0)  # Màu đường viền
        self._borderWidth = 2  # Độ dày của đường viền

    def _set_theme(self):
        self.theme = useTheme()
        self._headerBackgroundColor = QColor(self.theme.palette.background.content)  # Màu nền

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        
        # Tô màu nền của header
        # painter.setBrush(self._headerBackgroundColor)
        # painter.fillRect(rect, self._headerBackgroundColor)

        # Vẽ đường viền xung quanh (toàn bộ header)
        # painter.setPen(self._borderColor)
        # painter.drawRect(rect)  # Vẽ đường viền chung cho header

        # Vẽ tiêu đề của cột, căn giữa
        # textRect = rect
        # textRect.setLeft(rect.left() + 5)  # Thêm khoảng cách bên trái để tránh dính vào cạnh
        # textRect.setRight(rect.right() - 5)  # Thêm khoảng cách bên phải
        title = self.model().headerData(logicalIndex, self.orientation(), Qt.DisplayRole)
        if title:
            painter.setPen(QColor(self.theme.palette.text.primary))
            font = self.font()
            font.setBold(True)
            painter.setFont(font)
            # painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, title)
            # painter.drawLine(rect.right(), rect.top(), rect.right(), rect.bottom())  # Border trên phải

        painter.restore()