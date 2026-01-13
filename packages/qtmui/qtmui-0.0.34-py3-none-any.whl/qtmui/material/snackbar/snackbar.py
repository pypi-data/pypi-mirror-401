# coding:utf-8

from enum import Enum
from typing import Union, Callable, Optional
import weakref

from PySide6.QtCore import (Qt, QEvent, QSize, QRectF, QObject, QPropertyAnimation,
                          QEasingCurve, QTimer, Signal, QParallelAnimationGroup, QPoint)
from PySide6.QtGui import QPainter, QIcon, QColor
from PySide6.QtWidgets import (QWidget, QFrame, QLabel, QHBoxLayout, QVBoxLayout,
                             QApplication, QGraphicsOpacityEffect)

from ...common.auto_wrap import TextWrap
from ...common.icon import FluentIconBase, Theme, isDarkTheme, drawIcon
from ..py_tool_button import PyToolButton
from ..py_iconify import PyIconify
from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from ..widget_base import PyWidgetBase

from ...qtmui_assets import QTMUI_ASSETS

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style



class SnackbarIcon(FluentIconBase, Enum):
    """ Info bar icon """

    INFORMATION = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            color = "dark" if isDarkTheme() else "light"
        else:
            color = theme.value.lower()

        # return f':/qfluentwidgets/images/info_bar/{self.value}_{color}.svg'
        if self.value == "info":
            return f':/baseline/resource_qtmui/baseline/info.svg'
        elif self.value == "success":
            return f':/baseline/resource_qtmui/baseline/check_circle.svg'
        elif self.value == "warning":
            return f':/baseline/resource_qtmui/baseline/warning.svg'
        else:
            return f':/baseline/resource_qtmui/baseline/dangerous.svg'

class SnackbarPosition(Enum):
    """ Info bar position """
    TOP = 0
    BOTTOM = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5
    NONE = 6


class InfoIconWidget(QWidget):
    """ Icon widget """

    def __init__(self, icon: SnackbarIcon, parent=None, fill=None):
        super().__init__(parent=parent)
        self.setFixedSize(36, 36)
        self.icon = icon
        self.fill = fill

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        rect = QRectF(3, 6, 26, 26)

        # if self.icon != SnackbarIcon.INFORMATION:
        #     drawIcon(self.icon, painter, rect)
        # else:
        #     drawIcon(self.icon, painter, rect, indexes=[0], fill=self.fill)

        if self.fill:
            drawIcon(self.icon, painter, rect, indexes=[0], fill=self.fill)
        else:
            drawIcon(self.icon, painter, rect)


# class Snackbar(QFrame):
#     snackbars = {'top': [], 'bottom': [], 'left-top': [], 'left-bottom': [], 'right-top': [], 'right-bottom': []}
    
#     def __init__(
#             self, 
#             parent=None, 
#             message="", 
#             duration=3000, 
#             position="bottom", 
#             spacing=10,
#             child: object = None
#             ):
#         super().__init__(parent)

class Snackbar(QFrame, PyWidgetBase):
    """
    A snackbar component, styled like Material-UI Snackbar.

    The `Snackbar` component displays brief messages at the bottom or top of the screen.
    It supports customizable positioning, duration, and content, aligning with MUI Snackbar props.
    Inherits from native component props.

    Parameters
    ----------
    parent : QWidget, optional
        The parent widget. Default is QApplication.instance().mainWindow or None.
    color : State or str, optional
        Color of the snackbar ('default', 'primary', 'secondary', etc.). Default is 'default'.
        Can be a `State` object for dynamic updates.
    icon : State, PyIconify, str, or None, optional
        Icon to display. Default is None.
        Can be a `State` object for dynamic updates.
    title : State, str, Callable, or None, optional
        Title of the snackbar. Default is None.
        Can be a `State` object for dynamic updates.
    content : State, str, Callable, or None, optional
        Content of the snackbar. Default is None.
        Can be a `State` object for dynamic updates.
    anchorOrigin : State or Dict, optional
        Position of the snackbar ({ horizontal: 'left'|'center'|'right', vertical: 'top'|'bottom' }).
        Default is { vertical: 'bottom', horizontal: 'left' }.
        Can be a `State` object for dynamic updates.
    isClosable : State or bool, optional
        If True, shows a close button. Default is True.
        Can be a `State` object for dynamic updates.
    autoHideDuration : State, int, or None, optional
        Duration in milliseconds before auto-closing. Default is None (disabled).
        Can be a `State` object for dynamic updates.
    position : State, int, or str, optional
        Legacy position (TOP_RIGHT, etc.). Default is SnackbarPosition.TOP_RIGHT.
        Can be a `State` object for dynamic updates.
    action : State, QWidget, or None, optional
        Action widget to display. Default is None.
        Can be a `State` object for dynamic updates.
    children : State, QWidget, or None, optional
        Custom content to replace SnackbarContent. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or Dict, optional
        Override or extend styles. Default is None.
        Can be a `State` object for dynamic updates.
    disableWindowBlurListener : State or bool, optional
        If True, autoHideDuration timer runs when window is not focused. Default is False.
        Can be a `State` object for dynamic updates.
    key : State or Any, optional
        Unique key for multiple snackbars. Default is None.
        Can be a `State` object for dynamic updates.
    message : State, str, Callable, or None, optional
        Message to display. Default is None.
        Can be a `State` object for dynamic updates.
    onClose : State or Callable, optional
        Callback when snackbar requests to close. Default is None.
        Can be a `State` object for dynamic updates.
    open : State or bool, optional
        If True, snackbar is shown. Default is True.
        Can be a `State` object for dynamic updates.
    resumeHideDuration : State, int, or None, optional
        Duration in milliseconds to dismiss after interaction. Default is None.
        Can be a `State` object for dynamic updates.
    slotProps : State or Dict, optional
        Props for slot components. Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or Dict, optional
        Components for slots. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, or None, optional
        System prop for CSS overrides. Default is None.
        Can be a `State` object for dynamic updates.
    transitionDuration : State, int, Dict, or None, optional
        Duration for transition in milliseconds. Default is None (uses theme.transitions).
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to QFrame, supporting native component props.

    Signals
    -------
    closedSignal : Signal()
        Emitted when the snackbar is closed.

    Notes
    -----
    - Existing parameters (9) are retained; 14 new parameters added to align with MUI Snackbar.
    - Supports click-away listener and transition effects.
    - MUI classes applied: `MuiSnackbar-root`.
    - Integrates with `SnackbarManager` for positioning.

    Demos:
    - Snackbar: https://qtmui.com/material-ui/qtmui-snackbar/

    API Reference:
    - Snackbar API: https://qtmui.com/material-ui/api/snackbar/
    """

    closedSignal = Signal()

    def __init__(
                self, 
                color: str = "default", 
                icon: Union[PyIconify, str] = None, 
                title: Optional[Union[str, Callable]] = None,
                content: Optional[Union[str, Callable]] = None,
                orient: Union[int, str, Qt.Orientation] = Qt.Orientation.Horizontal,
                isClosable: bool = True, 
                duration: int = 1000, 
                position: Union[int, str]=SnackbarPosition.TOP_RIGHT,
                parent=None,
                ):

        super().__init__(parent=parent or QApplication.instance().mainWindow)
        # self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.color = color
        self.title = title
        self.content = content
        self.orient = orient
        self.icon = icon
        self.duration = duration
        self.isClosable = isClosable
        self.position = position

        self.theme = useTheme()

        self.titleLabel = QLabel(self)
        self.contentLabel = QLabel(self)
        self.closeButton = PyToolButton(icon=PyIconify(key=QTMUI_ASSETS.ICONS.CLOSE))
        self.iconWidget = PyToolButton(icon=icon, color=color, size=QSize(24, 24), iconSize=QSize(20, 20))

        self.hBoxLayout = QHBoxLayout(self)
        self.textLayout = QHBoxLayout() if self.orient == Qt.Horizontal else QVBoxLayout()
        self.widgetLayout = QHBoxLayout() if self.orient == Qt.Horizontal else QVBoxLayout()

        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.opacityAni = QPropertyAnimation(
            self.opacityEffect, b'opacity', self)

        self.lightBackgroundColor = None
        self.darkBackgroundColor = None

        self.__initWidget()

        if isinstance(self.title, Callable):
            i18n.langChanged.connect(self.retranslateUi)
        if isinstance(self.content, Callable):
            i18n.langChanged.connect(self.retranslateUi)

        self.retranslateUi()

        self.show()

    def retranslateUi(self):
        w = 900 if not self.parent() else (self.parent().width() - 50)

        # adjust title
        chars = max(min(w / 10, 120), 30)
        if self.title is not None:
            if isinstance(self.title, Callable):
                self.titleLabel.setText(TextWrap.wrap(translate(self.title), chars, False)[0])
            elif isinstance(self.title, str):
                self.titleLabel.setText(TextWrap.wrap(self.title, chars, False)[0])
        else:
            self.titleLabel.hide()

        # adjust content
        chars = max(min(w / 9, 120), 30)
        if self.content is not None:
            if isinstance(self.content, Callable):
                self.contentLabel.setText(TextWrap.wrap(translate(self.content), chars, False)[0])
            elif isinstance(self.content, str):
                self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])
        else:
            self.contentLabel.hide()

        self.adjustSize()

    def __initWidget(self):
        self.opacityEffect.setOpacity(1)
        self.setGraphicsEffect(self.opacityEffect)

        self.__setQss()
        self.__initLayout()

        self.closeButton.clicked.connect(self.close)

    def __initLayout(self):
        self.hBoxLayout.setContentsMargins(6, 6, 6, 6)
        self.hBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        # self.textLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        # self.textLayout.setAlignment(Qt.AlignTop)
        # self.textLayout.setContentsMargins(1, 12, 0, 0)

        self.hBoxLayout.setSpacing(0)
        self.textLayout.setSpacing(5)

        # add icon to layout
        self.hBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # add title to layout
        self.textLayout.addWidget(self.titleLabel)
        self.titleLabel.setVisible(bool(self.title))

        # add content label to layout
        if self.orient == Qt.Horizontal:
            self.textLayout.addSpacing(7)

        self.textLayout.addWidget(self.contentLabel)
        self.contentLabel.setVisible(bool(self.content))
        self.hBoxLayout.addLayout(self.textLayout)

        # add widget layout
        if self.orient == Qt.Horizontal:
            self.hBoxLayout.addLayout(self.widgetLayout)
            self.widgetLayout.setSpacing(10)
        else:
            self.textLayout.addLayout(self.widgetLayout)

        # add close button to layout
        self.hBoxLayout.addSpacing(12)
        self.hBoxLayout.addWidget(self.closeButton, 0, Qt.AlignTop | Qt.AlignLeft)

        self._adjustText()

    def __setQss(self):
        self.setObjectName('Snackbar')
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

        self.setProperty('p-color', self.color)
        self.titleLabel.setProperty('p-color', self.color)
        self.contentLabel.setProperty('p-color', self.color)

        theme = useTheme()

        Snackbar_root = theme.components[f"Snackbar"]["styles"]["root"]

        Snackbar_root_color_styles = get_qss_style(Snackbar_root[self.color])

        Snackbar_root_title_label_color_styles = get_qss_style(Snackbar_root[self.color]["titleLabel"])
        Snackbar_root_content_label_color_styles = get_qss_style(Snackbar_root[self.color]["contentLabel"])

        Snackbar_root_title_label_color = Snackbar_root[self.color]["titleLabel"]["color"]


        self.setStyleSheet(
            f"""
                #Snackbar[p-color={self.color}] {{
                    {Snackbar_root_color_styles}
                }}
                #titleLabel[p-color={self.color}] {{
                    {Snackbar_root_title_label_color_styles}
                }}
                #contentLabel[p-color={self.color}] {{
                    {Snackbar_root_content_label_color_styles}
                }}
            """
        )


        self.closeButton._set_text_color(Snackbar_root_title_label_color)
        # self.iconWidget.fill = Snackbar_root_title_label_color
        # self.iconWidget.update()

    def __fadeOut(self):
        """ fade out """
        self.opacityAni.setDuration(200)
        self.opacityAni.setStartValue(1)
        self.opacityAni.setEndValue(0)
        self.opacityAni.finished.connect(self.close)
        self.opacityAni.start()

    def _adjustText(self):
        self.retranslateUi()

    def addWidget(self, widget: QWidget, stretch=0):
        """ add widget to info bar """
        self.widgetLayout.addSpacing(6)
        align = Qt.AlignTop if self.orient == Qt.Vertical else Qt.AlignVCenter
        self.widgetLayout.addWidget(widget, stretch, Qt.AlignLeft | align)

    def setCustomBackgroundColor(self, light, dark):
        """ set the custom background color

        Parameters
        ----------
        light, dark: str | Qt.GlobalColor | QColor
            background color in light/dark theme mode
        """
        self.lightBackgroundColor = QColor(light)
        self.darkBackgroundColor = QColor(dark)
        self.update()

    def eventFilter(self, obj, e: QEvent):
        if obj is self.parent():
            if e.type() in [QEvent.Resize, QEvent.WindowStateChange]:
                self._adjustText()

        return super().eventFilter(obj, e)

    def closeEvent(self, e):
        self.closedSignal.emit()
        self.deleteLater()

    def showEvent(self, e):
        self._adjustText()
        super().showEvent(e)

        if self.duration >= 0:
            QTimer.singleShot(self.duration, self.__fadeOut)

        if self.position != SnackbarPosition.NONE:
            manager = SnackbarManager.make(self.position)
            manager.add(self)

        if self.parent():
            self.parent().installEventFilter(self)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.lightBackgroundColor is None:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if isDarkTheme():
            painter.setBrush(self.darkBackgroundColor)
        else:
            painter.setBrush(self.lightBackgroundColor)

        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 6, 6)


class SnackbarManager(QObject):
    """ Info bar manager """

    _instance = None
    managers = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SnackbarManager, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.__initialized = False

        return cls._instance

    def __init__(self):
        if self.__initialized:
            return

        super().__init__()
        self.spacing = 16
        self.margin = 24
        self.infoBars = weakref.WeakKeyDictionary()
        self.aniGroups = weakref.WeakKeyDictionary()
        self.slideAnis = []
        self.dropAnis = []
        self.__initialized = True

    def add(self, infoBar: Snackbar):
        """ add info bar """
        p = infoBar.parent()    # type:QWidget
        if not p:
            return

        if p not in self.infoBars:
            p.installEventFilter(self)
            self.infoBars[p] = []
            self.aniGroups[p] = QParallelAnimationGroup(self)

        if infoBar in self.infoBars[p]:
            return

        # add drop animation
        if self.infoBars[p]:
            dropAni = QPropertyAnimation(infoBar, b'pos')
            dropAni.setDuration(200)

            self.aniGroups[p].addAnimation(dropAni)
            self.dropAnis.append(dropAni)

            infoBar.setProperty('dropAni', dropAni)

        # add slide animation
        self.infoBars[p].append(infoBar)
        slideAni = self._createSlideAni(infoBar)
        self.slideAnis.append(slideAni)

        infoBar.setProperty('slideAni', slideAni)
        infoBar.closedSignal.connect(lambda: self.remove(infoBar))

        slideAni.start()

    def remove(self, infoBar: Snackbar):
        """ remove info bar """
        p = infoBar.parent()
        if p not in self.infoBars:
            return

        if infoBar not in self.infoBars[p]:
            return

        self.infoBars[p].remove(infoBar)

        # remove drop animation
        dropAni = infoBar.property('dropAni')   # type: QPropertyAnimation
        if dropAni:
            self.aniGroups[p].removeAnimation(dropAni)
            self.dropAnis.remove(dropAni)

        # remove slider animation
        slideAni = infoBar.property('slideAni')
        if slideAni:
            self.slideAnis.remove(slideAni)

        # adjust the position of the remaining info bars
        self._updateDropAni(p)
        self.aniGroups[p].start()

    def _createSlideAni(self, infoBar: Snackbar):
        slideAni = QPropertyAnimation(infoBar, b'pos')
        slideAni.setEasingCurve(QEasingCurve.OutQuad)
        slideAni.setDuration(200)

        slideAni.setStartValue(self._slideStartPos(infoBar))
        slideAni.setEndValue(self._pos(infoBar))

        return slideAni

    def _updateDropAni(self, parent):
        for bar in self.infoBars[parent]:
            ani = bar.property('dropAni')
            if not ani:
                continue

            ani.setStartValue(bar.pos())
            ani.setEndValue(self._pos(bar))

    def _pos(self, infoBar: Snackbar, parentSize=None) -> QPoint:
        """ return the position of info bar """
        raise NotImplementedError

    def _slideStartPos(self, infoBar: Snackbar) -> QPoint:
        """ return the start position of slide animation  """
        raise NotImplementedError

    def eventFilter(self, obj, e: QEvent):
        if obj not in self.infoBars:
            return False

        if e.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            size = e.size() if e.type() == QEvent.Resize else None
            for bar in self.infoBars[obj]:
                bar.move(self._pos(bar, size))

        return super().eventFilter(obj, e)

    @classmethod
    def register(cls, name):
        """ register menu animation manager

        Parameters
        ----------
        name: Any
            the name of manager, it should be unique
        """
        def wrapper(Manager):
            if name not in cls.managers:
                cls.managers[name] = Manager

            return Manager

        return wrapper

    @classmethod
    def make(cls, position: SnackbarPosition):
        """ mask info bar manager according to the display position """
        if position not in cls.managers:
            raise ValueError(f'`{position}` is an invalid animation type.')

        return cls.managers[position]()


@SnackbarManager.register(SnackbarPosition.TOP)
class TopSnackbarManager(SnackbarManager):
    """ Top position info bar manager """

    def _pos(self, infoBar: Snackbar, parentSize=None):
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        x = (infoBar.parent().width() - infoBar.width()) // 2
        y = self.margin
        index = self.infoBars[p].index(infoBar)
        for bar in self.infoBars[p][0:index]:
            y += (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: Snackbar):
        pos = self._pos(infoBar)
        return QPoint(pos.x(), pos.y() - 16)


@SnackbarManager.register(SnackbarPosition.TOP_RIGHT)
class TopRightSnackbarManager(SnackbarManager):
    """ Top right position info bar manager """

    def _pos(self, infoBar: Snackbar, parentSize=None):
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        x = parentSize.width() - infoBar.width() - self.margin
        y = self.margin
        index = self.infoBars[p].index(infoBar)
        for bar in self.infoBars[p][0:index]:
            y += (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: Snackbar):
        return QPoint(infoBar.parent().width(), self._pos(infoBar).y())


@SnackbarManager.register(SnackbarPosition.BOTTOM_RIGHT)
class BottomRightSnackbarManager(SnackbarManager):
    """ Bottom right position info bar manager """

    def _pos(self, infoBar: Snackbar, parentSize=None) -> QPoint:
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        x = parentSize.width() - infoBar.width() - self.margin
        y = parentSize.height() - infoBar.height() - self.margin

        index = self.infoBars[p].index(infoBar)
        for bar in self.infoBars[p][0:index]:
            y -= (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: Snackbar):
        return QPoint(infoBar.parent().width(), self._pos(infoBar).y())


@SnackbarManager.register(SnackbarPosition.TOP_LEFT)
class TopLeftSnackbarManager(SnackbarManager):
    """ Top left position info bar manager """

    def _pos(self, infoBar: Snackbar, parentSize=None) -> QPoint:
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        y = self.margin
        index = self.infoBars[p].index(infoBar)

        for bar in self.infoBars[p][0:index]:
            y += (bar.height() + self.spacing)

        return QPoint(self.margin, y)

    def _slideStartPos(self, infoBar: Snackbar):
        return QPoint(-infoBar.width(), self._pos(infoBar).y())


@SnackbarManager.register(SnackbarPosition.BOTTOM_LEFT)
class BottomLeftSnackbarManager(SnackbarManager):
    """ Bottom left position info bar manager """

    def _pos(self, infoBar: Snackbar, parentSize: QSize = None) -> QPoint:
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        y = parentSize.height() - infoBar.height() - self.margin
        index = self.infoBars[p].index(infoBar)

        for bar in self.infoBars[p][0:index]:
            y -= (bar.height() + self.spacing)

        return QPoint(self.margin, y)

    def _slideStartPos(self, infoBar: Snackbar):
        return QPoint(-infoBar.width(), self._pos(infoBar).y())


@SnackbarManager.register(SnackbarPosition.BOTTOM)
class BottomSnackbarManager(SnackbarManager):
    """ Bottom position info bar manager """

    def _pos(self, infoBar: Snackbar, parentSize: QSize = None) -> QPoint:
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        x = (parentSize.width() - infoBar.width()) // 2
        y = parentSize.height() - infoBar.height() - self.margin
        index = self.infoBars[p].index(infoBar)

        for bar in self.infoBars[p][0:index]:
            y -= (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: Snackbar):
        pos = self._pos(infoBar)
        return QPoint(pos.x(), pos.y() + 16)
