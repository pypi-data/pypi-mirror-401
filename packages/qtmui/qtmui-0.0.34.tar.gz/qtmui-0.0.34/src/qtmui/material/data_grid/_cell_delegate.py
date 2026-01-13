from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import QRect, QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyleOptionButton, QStyle

from ..utils.icon import icon_base64_to_pixmap

from ._base_button_delegate import DelegateButton
from .icon import icon_base_64_data, icon_chrome_closed, icon_chrome_opened, icon_chrome_opening_closing, icon_profile_edit, icon_profile_delete

BUTTON_SIZE_X = 100  # Size of each button
BUTTON_SIZE_Y = 25  # Size of each button


class CellDelegate(QStyledItemDelegate):

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

        super(CellDelegate, self).paint(painter, option, index)

