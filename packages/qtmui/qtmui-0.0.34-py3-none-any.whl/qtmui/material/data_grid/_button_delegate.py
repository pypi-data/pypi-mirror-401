from PySide6.QtWidgets import  QStyledItemDelegate, QStyleOptionButton, QStyle
from PySide6.QtCore import Qt, QRect, QSize, QEvent, Signal
from PySide6.QtGui import QPainter, QIcon, QPixmap, QColor
from PySide6.QtSvg import QSvgRenderer

from ..utils.icon import icon_base64_to_pixmap

from ._base_button_delegate import DelegateButton
from .icon import icon_base_64_data, icon_chrome_closed, icon_chrome_opened, icon_chrome_opening_closing, icon_profile_edit, icon_profile_delete

BUTTON_SIZE_X = 100  # Size of each button
BUTTON_SIZE_Y = 25  # Size of each button


class ButtonDelegate(QStyledItemDelegate):

    delegateButtonPressed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.delegateButtonPressed.connect(parent.cellButtonClicked)
        self.button = DelegateButton()


    def paint(self, painter, option, index):
        if index.column() == 10:  # Assuming the button column is the third column
            buttons = [("Open", "Blac.png"), ("Edit", "Blac.png"), ("Delete", "Blac.png")]  # Define your button labels and icons
            button_count = len(buttons)
            total_button_width = button_count * BUTTON_SIZE_X
            width = option.rect.width()
            start_x = option.rect.x() + (width - total_button_width) // 2

            profile_state = index.data()

            # painter.setBrush
            # is_open_btn_hover:
            #     painter.setBrush(hover)

            for i, (button_label, icon_path) in enumerate(buttons):
                button_rect = QRect(start_x + i * BUTTON_SIZE_X, option.rect.y(), BUTTON_SIZE_X, BUTTON_SIZE_Y)
                opt = QStyleOptionButton()
                opt.initFrom(self.button)

                opt.rect = button_rect
                opt.icon = QIcon()
                opt.iconSize = QSize(15, 15)
                opt.state |= QStyle.State_Enabled
                # opt.features = QStyleOptionButton.DefaultButton
                # option.features = QStyleOptionButton.DefaultButton
                
                if i == 0:
                    if profile_state == "opening":
                        opt.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_opening_closing), QIcon.Normal, QIcon.Off)
                        opt.text = "Opening"
                    elif profile_state == "closing":
                        opt.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_opening_closing), QIcon.Normal, QIcon.Off)
                        opt.text = "Closing"
                    elif profile_state == "closed":
                        opt.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_closed), QIcon.Normal, QIcon.Off)
                        opt.text = "Open"
                    elif profile_state == "opened":
                        opt.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_opened), QIcon.Normal, QIcon.Off)
                        opt.text = "Close"
                    else:
                        opt.icon.addPixmap(icon_base64_to_pixmap(icon_chrome_closed), QIcon.Normal, QIcon.Off)
                        opt.text = "Open"
                elif i == 1:
                        opt.icon.addPixmap(icon_base64_to_pixmap(icon_profile_edit), QIcon.Normal, QIcon.Off)
                        opt.text = "Edit"
                elif i == 2:
                        opt.icon.addPixmap(icon_base64_to_pixmap(icon_profile_delete), QIcon.Normal, QIcon.Off)
                        opt.text = "Delete"
                painter.save()
                self.button.style().drawControl(QStyle.CE_PushButton, opt, painter, self.button)
                # QApplication.style().drawControl(QStyle.CE_PushButton, opt, painter, self.button)
                painter.restore()
            return

        super(ButtonDelegate, self).paint(painter, option, index)


    def svg_to_pixmap(self, svg_filename: str, width: int, height: int, color: QColor) -> QPixmap:
        renderer = QSvgRenderer(svg_filename)
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)  # this is the destination, and only its alpha is used!
        painter.setCompositionMode(
            painter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return pixmap

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
    
    def _buttonRect(self, optionRect):
        return QRect(
            optionRect.x() + 8, 
            optionRect.y() + (optionRect.height() - 24) // 2, 
            24, 24
        )

    def editorEvent(self, event, model, option, index):
        sub_rects = self.split_rect(option.rect, 3)
        test_point = event.pos()

        # print('sub_rects___', sub_rects)

        # Kiểm tra xem test_point có nằm trong hình chữ nhật nào không
        result = self.point_in_rects(test_point, sub_rects)

        if index.column() == 10 and event.type() == QEvent.MouseButtonRelease:
            if result != -1:
                if result == 0:
                    self.delegateButtonPressed.emit(f"openclose_{index.row()}_{index.column()}")
                if result == 1:
                    self.delegateButtonPressed.emit(f"edit_{index.row()}_{index.column()}")
                if result == 2:
                    self.delegateButtonPressed.emit(f"delete_{index.row()}_{index.column()}")
                return True
            else:
                print("The point is not in any sub-rectangle.")

        return super().editorEvent(event, model, option, index)