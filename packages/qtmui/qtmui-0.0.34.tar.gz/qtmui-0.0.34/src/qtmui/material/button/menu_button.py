import uuid
from typing import Callable, Optional
from PySide6.QtWidgets import QFrame, QPushButton, QMenu
from PySide6.QtCore import QPoint, Qt, QEvent, QSize, QCoreApplication, QTimer
from PySide6.QtGui import QMouseEvent, QIcon, QCursor

from ...common.icon import FluentIconBase
from .button import Button


# https://stackoverflow.com/questions/37797342/pyqt5-mousetracking-not-working


class MenuButton(Button):
    def __init__(
                self,
                context=None,
                menu: Optional[any] = None,
                icon: str = None,
                aboutToHide: Callable = None,
                *args, **kwargs
                ):
        super().__init__(startIcon=icon or ":/round/resource_qtmui/round/more_vert.svg", *args, **kwargs)
        self._context = context
        self._menu = menu

        self._icon = icon
        self._aboutToHide = aboutToHide

        self.is_open = False
        self.setMouseTracking(True)

        # self.setMenu(menu) # xem lai
        # self.menu = menu
        if aboutToHide:
            self.menu.aboutToHide.connect(self._aboutToHide)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.setStyleSheet('''
            QPushButton::menu-indicator {
                image: none;
            }
        ''')

    # def onMenuHide(self):
    #     QTimer.singleShot(500, self.updateUiOnMenuHide)


    def updateUiOnMenuHide(self):
        if not self._icon:
            self.update_state(False)
        self.is_open = False

    def update_state(self, is_open):
      if self._icon is not None:
        if is_open:
            self.setStyleSheet('''
            QPushButton {
                background-origin: padding;
                background-image: url(":/icons/svg_cache/ri_arrow-up-s-line.svg");
                background-position: right center;
                background-repeat: no-repeat;
                border: 0px solid transparent !important;
                border-right: 5px solid transparent;
                border-bottom: 5px solid transparent;
                border-radius: 4px;
                color: #6b6b6b;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {background-color: transparent;}
            ''')
        else:
            self.setStyleSheet('''
            QPushButton {
                background-origin: padding;
                background-image: url(":/icons/svg_cache/ri_arrow-down-s-line.svg");
                background-position: right center;
                background-repeat: no-repeat;
                border: 0px solid transparent !important;
                border-right: 5px solid transparent;
                border-bottom: 5px solid transparent;
                border-radius: 4px;
                color: #6b6b6b;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {background-color: transparent;}
            ''')


    def open_context_menu(self, point=None):
        if self.is_open == False:
          self.is_open = True
        #   self.update_state(True)
          self.menu().hide()
          point = QPoint(40, - self.get_menu_height() + self.height())
          self.menu().exec(self.mapToGlobal(point))
        else:
          self.menu().hide()
        #   self.update_state(False)
          self.is_open = False

    def get_menu_height(self):
        # Hiển thị menu tại vị trí (-1000, -1000) để nó không hiển thị trên màn hình
        self.menu().popup(self.mapToGlobal(self.pos()) + self.rect().bottomRight() + QPoint(-1000, -1000))
        # Lấy kích thước của menu sau khi nó được hiển thị
        height = self.menu().height()
        return height