from typing import Callable
from PySide6.QtCore import QSize, QEvent, Signal, QRect
from PySide6.QtGui import QIcon,  QColor, QBrush
from PySide6.QtWidgets import QStyledItemDelegate, QStyle,  QStyleOptionButton

from .icon import icon_firefox_disabled

from ..utils.icon import icon_base64_to_pixmap


class StyledItemDelegate(QStyledItemDelegate):

    mousePressedSignal = Signal(str)

    def __init__(self, 
                 parent=None,
                 column: int = None,
                 styledOption: object = None,
                 styledOptions: list = None,
                 onMousePressed: Callable = None
                 ):
        super(StyledItemDelegate, self).__init__(parent)
        if onMousePressed is not None:
            self.mousePressedSignal.connect(onMousePressed)
        self.column = column
        self.styledOption = styledOption
        self.styledOptions = styledOptions


    def split_rect(self, rect, num_divisions):
        # Tính toán chiều rộng của mỗi phần chia
        width_per_division = rect.width() // num_divisions
        
        # Tạo danh sách chứa các hình chữ nhật con
        sub_rects = []
        
        # Tạo các hình chữ nhật con
        for i in range(num_divisions):
            if i == 0:
                sub_rect = QRect((rect.left() + i * width_per_division) - 1, rect.top(), width_per_division + 1, rect.height() - 4)
                sub_rects.append(sub_rect)
            if i == 1:
                sub_rect = QRect(rect.left() + i * width_per_division, rect.top(), width_per_division + 1, rect.height() - 4)
                sub_rects.append(sub_rect)
            if i == 2:
                sub_rect = QRect((rect.left() + i * width_per_division) + 1, rect.top(), width_per_division + 1, rect.height() - 4)
                sub_rects.append(sub_rect)
        return sub_rects

    def point_in_rects(self, point, rects):
        for i, rect in enumerate(rects):
            if rect.contains(point):
                return i
        return -1

    def editorEvent(self, event, model, option, index):
        sub_rects = self.split_rect(option.rect, 3)
        test_point = event.pos()

        # print('sub_rects___', sub_rects)

        # Kiểm tra xem test_point có nằm trong hình chữ nhật nào không
        result = self.point_in_rects(test_point, sub_rects)

        if option.state & QStyle.State_MouseOver:
            option.backgroundBrush = QBrush(QColor(211, 211, 211))  # LightGray color

        if index.column() == 10 and event.type() == QEvent.MouseButtonRelease:
            if result != -1:
                if result == 0:
                    self.mousePressedSignal.emit(f"openclose_{index.row()}_{index.column()}")
                if result == 1:
                    self.mousePressedSignal.emit(f"edit_{index.row()}_{index.column()}")
                if result == 2:
                    self.mousePressedSignal.emit(f"delete_{index.row()}_{index.column()}")
                return True
            else:
                print("The point is not in any sub-rectangle.")

        return super().editorEvent(event, model, option, index)

    def paint(self, painter, option, index):
        if index.column() == self.column:  # Assuming the button column is the third column

            styledOption = QStyleOptionButton()
            styledOption.option.rect = option.rect

            styledOption.rect = option.rect
            styledOption.option.icon = QIcon()
            styledOption.option.iconSize = QSize(15, 15)
            styledOption.option.state |= QStyle.State_Enabled
            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_firefox_disabled), QIcon.Normal, QIcon.Off)
            styledOption.option.text = "Open"
            
            painter.save()
            styledOption.style().drawControl(QStyle.CE_PushButton, styledOption.option, painter, styledOption)
            # QApplication.style().drawControl(QStyle.CE_PushButton, opt, painter, self.button)
            painter.restore()

        super(StyledItemDelegate, self).paint(painter, option, index)