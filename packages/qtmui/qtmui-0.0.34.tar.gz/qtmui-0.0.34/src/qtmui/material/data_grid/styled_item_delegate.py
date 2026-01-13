from typing import Callable
from PySide6.QtCore import QSize, QEvent, Signal, QRect
from PySide6.QtGui import QIcon, QColor, QBrush
from PySide6.QtWidgets import QStyledItemDelegate, QStyle

from .icon import icon_chrome_closed, icon_chrome_opened, icon_chrome_opening_closing, \
    icon_profile_edit, icon_profile_delete, icon_chrome_disabled, icon_firefox_closed, icon_firefox_opened, icon_firefox_opening_closing, icon_firefox_disabled

from ..utils.icon import icon_base64_to_pixmap


BUTTON_SIZE_X = 100  # Size of each button
BUTTON_SIZE_Y = 25  # Size of each button

class StyledItemDelegate(QStyledItemDelegate):
    
    """
    Stack
    Base container

    Args:
        column: index of column
        gap: int
        sx: str = QSS string
            {
                color: red;
                backroud: none;
            }
        alignItems: "space-around" | "space-between" | "space-evenly" | "stretch" | "center" | "end" | "flex-end" | "flex-start" | "start"
        justifyContent: "space-around" | "space-between" | "space-evenly" | "stretch" | "center" | "end" | "flex-end" | "flex-start" | "start"
        flexWrap: "wrap" | "no-wrap"

    Returns:
        new instance of PySyde6.QtWidgets.QFrame
    """

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
            print('eoooooooooooooooooooooooooooeeeeeeeeeeee')
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
            # buttons = [("Open", "Blac.png"), ("Edit", "Blac.png"), ("Delete", "Blac.png")]  # Define your button labels and icons
            items_count = len(self.styledOptions)
            total_button_width = items_count * BUTTON_SIZE_X
            width = option.rect.width()
            start_x = option.rect.x() + (width - total_button_width) // 2

            profile_state = index.data()

            for i, styledOption in enumerate(self.styledOptions):

                _rect = QRect(start_x + i * BUTTON_SIZE_X, option.rect.y(), BUTTON_SIZE_X, BUTTON_SIZE_Y)
                
                styledOption.option.rect = _rect

                styledOption.rect = _rect
                styledOption.option.icon = QIcon()
                styledOption.option.iconSize = QSize(15, 15)
                styledOption.option.state |= QStyle.State_Enabled
                # styledOption.features = QStyleOptionButton.DefaultButton
                # option.features = QStyleOptionButton.DefaultButton
                
                if i == 0:
                    if profile_state.find('cbrowser') != -1:
                        if profile_state.find('|') != -1:
                            profile_state = profile_state.split("|")[1]
                        if profile_state == "opening":
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_opening_closing), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Opening"
                        elif profile_state == "closing":
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_opening_closing), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Closing"
                        elif profile_state == "closed":
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_closed), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Open"
                        elif profile_state == "opened":
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_opened), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Close"
                        elif profile_state == "opened_other_device":
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_disabled), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Open"
                        else:
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_closed), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Open"
                    else:
                        if profile_state.find('|') != -1:
                            profile_state = profile_state.split("|")[1]
                        if profile_state == "opening":
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_firefox_opening_closing), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Opening"
                        elif profile_state == "closing":
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_firefox_opening_closing), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Closing"
                        elif profile_state == "closed":
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_firefox_closed), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Open"
                        elif profile_state == "opened":
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_firefox_opened), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Close"
                        elif profile_state == "opened_other_device":
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_firefox_disabled), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Open"
                        else:
                            styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_firefox_closed), QIcon.Normal, QIcon.Off)
                            styledOption.option.text = "Open"
                elif i == 1:
                        styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_profile_edit), QIcon.Normal, QIcon.Off)
                        styledOption.option.text = "Edit"
                elif i == 2:
                        styledOption.option.icon.addPixmap(icon_base64_to_pixmap(icon_profile_delete), QIcon.Normal, QIcon.Off)
                        styledOption.option.text = "Delete"
                painter.save()
                styledOption.style().drawControl(QStyle.CE_PushButton, styledOption.option, painter, styledOption)
                # QApplication.style().drawControl(QStyle.CE_PushButton, opt, painter, self.button)
                painter.restore()
            return

        super(StyledItemDelegate, self).paint(painter, option, index)