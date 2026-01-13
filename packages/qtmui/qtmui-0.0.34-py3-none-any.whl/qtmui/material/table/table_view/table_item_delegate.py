# coding: utf-8
import uuid
from typing import List, Union, Optional, Dict
from ...system.color_manipulator import alpha as _alpha
from ...system.color_manipulator import lighten_hex

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

[
    {
        "icon": "emojione-v1:flag-for-vietnam",
        "label": "Viet Nam",
        "value": "vi"
    },
    {
        "icon": "twemoji:flag-england",
        "label": "England",
        "value": "en"
    },
    {
        "icon": "emojione-v1:flag-for-thailand",
        "label": "Thanland",
        "label": "th"
    },
]

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

    def __createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:

        if index.column() == 2:
            lineEdit = LineEdit()
            lineEdit.setProperty("transparent", False)
            lineEdit.setStyle(QApplication.style())
            lineEdit.setText(option.text)
            lineEdit.setClearButtonEnabled(True)
            adornment = Box(
                children=[
                    lineEdit,
                    Box(
                        absolute=True,
                        direction="row",
                        children=[
                            Button(variant="text", startIcon=PyIconify(key="lsicon:drag-filled"), size="small"),
                            Checkbox(size="small"),
                            HSpacer(),
                            Button(variant="text", startIcon=PyIconify(key="stash:side-peek"), size="small"),
                            Button(variant="text", startIcon=PyIconify(key="mingcute:add-fill"), size="small"),
                        ]
                    )
                ]
            )
            adornment.setParent(parent)
            return adornment
        else:
            lineEdit = LineEdit(parent)
            lineEdit.setProperty("transparent", False)
            lineEdit.setStyle(QApplication.style())
            lineEdit.setText(option.text)
            lineEdit.setClearButtonEnabled(True)
            return lineEdit
        
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        lineEdit = LineEdit(parent)
        lineEdit.setProperty("transparent", False)
        lineEdit.setStyle(QApplication.style())
        lineEdit.setText(option.text)
        lineEdit.setClearButtonEnabled(True)
        return lineEdit
    
    
    def setEditorData(self, editor: QWidget, index: QModelIndex):
        """ Đưa dữ liệu từ model vào editor """
        if isinstance(editor, LineEdit):
            value = index.data(Qt.DisplayRole)  # Lấy dữ liệu từ model
            if value is not None:
                editor.setText(str(value))

    def setModelData(self, editor: QWidget, model, index: QModelIndex):
        """ Lưu dữ liệu từ editor vào model """
        if isinstance(editor, LineEdit):
            model.setData(index, editor.text(), Qt.EditRole)

    # def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
    #     rect = option.rect
    #     y = rect.y() + (rect.height() - editor.height()) // 2
    #     x, w = max(8, rect.x()), rect.width()
    #     if index.column() == 0:
    #         w -= 8

    #     editor.setGeometry(x, y, w, rect.height())

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        """ Định vị editor trong ô """
        editor.setGeometry(option.rect)

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
        painter.setBrush(QBrush(QColor(useTheme().palette.error.main)))
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
        # isDark = isDarkTheme()
        isDark = useTheme().palette.mode == "dark"

        c = 255 if isDark else 0
        alpha = 0
        
        selected = None
        
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

        # if option.state & QStyle.State_Selected:
        #     painter.setBrush(QColor(lighten_hex(useTheme().palette.primary.main, 0.96)))
        # else:
        #     if index.data(Qt.ItemDataRole.BackgroundRole):
        #         painter.setBrush(index.data(Qt.ItemDataRole.BackgroundRole))
        #     else:
        #         painter.setBrush(QColor(c, c, c, alpha))
                
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


