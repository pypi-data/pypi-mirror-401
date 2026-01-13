

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize, QCoreApplication, QEvent, Signal, QRect
from PySide6.QtGui import QMovie, QIcon, Qt, QColor
from PySide6.QtWidgets import QStyledItemDelegate, QStyle, QApplication, QStyleOptionButton, QPushButton

from ...utils.icon import icon_base64_to_pixmap

class StyledOptionButton(QPushButton):
    def __init__(
            self, 
            parent=None,
            name: str = None,
            iconBase64: object = None,
            size: QSize = QSize(50, 50),
            iconSize: QSize = QSize(15, 15)
            ):
        super(StyledOptionButton, self).__init__(parent)

        # self.setLayout(QHBoxLayout())
        self.setFixedSize(size)

        self.option = QStyleOptionButton()
        self.option.icon.addPixmap(icon_base64_to_pixmap(iconBase64), QIcon.Normal, QIcon.Off)
        self.option.iconSize = iconSize

        # rgb(227, 227, 227)
        
        self.setStyleSheet("""
            QPushButton{
                background-color: rgb(237, 237, 237);
                max-height: 30px;
                min-height: 30px;
                border: 0px solid transparent;
                border-radius: 4px;
                margin-left: 2px;
                color: #6b6b6b;
            }
            QPushButton::hover {
                border: 2px solid red;
                background-color: red;
            }
            """)
        self.option.initFrom(self)

