# coding:utf-8
from typing import Optional, Dict, Callable, Union

import sys
import uuid

from PySide6.QtCore import Qt, QSize, QRect, Signal, QByteArray
from PySide6.QtGui import QIcon, QPainter, QColor, QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication, QSizePolicy

from ...common.router import qrouter
from ...common.style_sheet import FluentStyleSheet, isDarkTheme
from ...common.animation import BackgroundAnimationWidget
from .frameless_window import FramelessWindow

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from .stacked_widget import StackedWidget

from ...lib.qframelesswindow import TitleBar, TitleBarBase

from qtmui.material.typography import Typography
from qtmui.material.py_iconify import PyIconify

from qtmui.qtmui_assets import QTMUI_ASSETS
from qtmui.material.styles.global_styles import GLOBAL_STYLES

def iconFromBase64(base64):
  pixmap = QPixmap()
  pixmap.loadFromData(QByteArray.fromBase64(base64.encode()))
  icon = QIcon(pixmap)
  return icon

class FluentWindowBase(BackgroundAnimationWidget, FramelessWindow):
    """ Fluent window base class """

    def __init__(self, parent=None):
        self._isMicaEnabled = False
        self._lightBackgroundColor = QColor(240, 244, 249)
        self._darkBackgroundColor = QColor(32, 32, 32)
        super().__init__(parent=parent)

        self.hBoxLayout = QHBoxLayout(self)
        self.stackedWidget = StackedWidget(self)
        self.stackedWidget.setObjectName("QtMuiStackedWidget")
        self.navigationInterface = None

        # initialize layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget.layout().setContentsMargins(0, 0, 0, 0)
        
        # FluentStyleSheet.FLUENT_WINDOW.apply(self.stackedWidget)

        # enable mica effect on win11
        self.setMicaEffectEnabled(True)

        # show system title bar buttons on macOS
        if sys.platform == "darwin":
            self.setSystemTitleBarButtonVisible(True)

        # qconfig.themeChangedFinished.connect(self._onThemeChangedFinished)



    def switchTo(self, interface: QWidget):
        self.stackedWidget.setCurrentWidget(interface, popOut=False)

    def _onCurrentInterfaceChanged(self, index: int):
        widget = self.stackedWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

        self._updateStackedBackground()

    def _updateStackedBackground(self):
        isTransparent = self.stackedWidget.currentWidget().property("isStackedTransparent")
        if bool(self.stackedWidget.property("isTransparent")) == isTransparent:
            return

        self.stackedWidget.setProperty("isTransparent", isTransparent)
        self.stackedWidget.setStyle(QApplication.style())

    def setCustomBackgroundColor(self, light, dark):
        """ set custom background color

        Parameters
        ----------
        light, dark: QColor | Qt.GlobalColor | str
            background color in light/dark theme mode
        """
        self._lightBackgroundColor = QColor(light)
        self._darkBackgroundColor = QColor(dark)
        self._updateBackgroundColor()

    def _normalBackgroundColor(self):
        if not self.isMicaEffectEnabled():
            return self._darkBackgroundColor if isDarkTheme() else self._lightBackgroundColor

        return QColor(0, 0, 0, 0)

    def _onThemeChangedFinished(self):
        if self.isMicaEffectEnabled():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.backgroundColor)
        painter.drawRect(self.rect())

    def setMicaEffectEnabled(self, isEnabled: bool):
        """ set whether the mica effect is enabled, only available on Win11 """
        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return

        self._isMicaEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self._normalBackgroundColor())

    def isMicaEffectEnabled(self):
        return self._isMicaEnabled

    def systemTitleBarRect(self, size: QSize) -> QRect:
        """ Returns the system title bar rect, only works for macOS

        Parameters
        ----------
        size: QSize
            original system title bar rect
        """
        return QRect(size.width() - 75, 0 if self.isFullScreen() else 9, 75, size.height())

    def setTitleBar(self, titleBar):
        super().setTitleBar(titleBar)

        # hide title bar buttons on macOS
        if sys.platform == "darwin" and self.isSystemButtonVisible() and isinstance(titleBar, TitleBarBase):
            titleBar.minBtn.hide()
            titleBar.maxBtn.hide()
            titleBar.closeBtn.hide()


class FluentTitleBar(TitleBar):
    """ Fluent title bar"""

    def __init__(
                self, 
                parent,
                title,
                sx: Optional[Union[Callable, str, Dict]]= None,
                ):
        super().__init__(parent)

        self._sx = sx

        # self.setFixedHeight(32)
        self.setFixedHeight(45)

        self.setObjectName("PyTitleBar")

        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setStyleSheet('margin-left: 9px;')
        self.iconLabel.setFixedSize(27, 18)
        self.hBoxLayout.insertWidget(0, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = Typography(
            text=title, 
            sx={
                'padding-bottom': '1px',
                'padding-left': '2px',
                'font-weight': 600,
                'color': 'palette.text.secondary'
            }
        )
        # self.titleLabel.setStyleSheet('background-color: transparent;padding-bottom: 2px;padding-left: 9px;font-weight: 700;')
        self.titleLabel.setFixedHeight(32)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.insertWidget(1, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        # self.window().windowTitleChanged.connect(self.setTitle)

        # self.vBoxLayout = QVBoxLayout()
        # self.buttonLayout = QHBoxLayout()
        # self.buttonLayout.setSpacing(0)
        # self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        # # self.buttonLayout.setAlignment(Qt.AlignTop)
        # self.buttonLayout.setAlignment(Qt.AlignCenter)
        # self.buttonLayout.addWidget(self.minBtn)
        # self.buttonLayout.addWidget(self.maxBtn)
        # self.buttonLayout.addWidget(self.closeBtn)
        # self.vBoxLayout.addLayout(self.buttonLayout)
        # self.vBoxLayout.addStretch(1)
        # self.hBoxLayout.addLayout(self.vBoxLayout, 0)
        
        self.frmButtons = QWidget(self)
        self.buttonLayout = QHBoxLayout(self.frmButtons)
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        # self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.setAlignment(Qt.AlignCenter)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.hBoxLayout.addWidget(self.frmButtons)

        # FluentStyleSheet.FLUENT_WINDOW.apply(self)
        self.theme = useTheme()
        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()


    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        PyTitleBar_root = component_styles[f"PyTitleBar"].get("styles")["root"]
        PyTitleBar_root_qss = get_qss_style(PyTitleBar_root)

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx)
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx)
                elif isinstance(sx, str):
                    sx_qss = sx

        self.setStyleSheet(
            f"""
                #PyTitleBar {{
                    {PyTitleBar_root_qss}
                    {sx_qss}
                }}
            """
        )

    def _setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.setFixedHeight(32)
        # self.titleLabel.setFixedWidth(100)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class QtMuiWindow(FluentWindowBase):
    """ Fluent window """
    sizeChanged = Signal(QSize)

    def __init__(self, parent=None, title="QtMui"):
        super().__init__(parent)
        QApplication.instance().mainWindow = self

        self._titleBar = FluentTitleBar(self, title=title)
        self.setTitleBar(self._titleBar)
        self.setObjectName(str(uuid.uuid4()))

        self._create_title_bar_content_frame()

        self.widgetLayout = QHBoxLayout()

        # initialize layout
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)

        self.widgetLayout.addWidget(self.stackedWidget)
        self.widgetLayout.setContentsMargins(0, 45, 0, 0) # chỗ này để cách title bar
        
        self.titleBar.raise_()
        
        self.setStyleSheet(GLOBAL_STYLES)
        self.setWindowIcon(iconFromBase64("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"))
        

    def setTitle(self, title:str):
        self._titleBar._setTitle(title=title)
        

    def _create_title_bar_content_frame(self):
        self._content_frame = QWidget()
        self._content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._content_frame.setStyleSheet('background-color: transparent;')
        self._hlo_content_frame = QHBoxLayout(self._content_frame)
        self._hlo_content_frame.setContentsMargins(0,0,0,0)
        self._titleBar.hBoxLayout.insertWidget(2, self._content_frame)

    def setHeader(self, widget: QWidget):
        self._hlo_content_frame.addWidget(widget)

    def setCentralWidget(self, widget: QWidget):
        # self._hlo_content_frame.addWidget(widget)
        self.stackedWidget.addWidget(widget)

    def resizeEvent(self, e):
        self.sizeChanged.emit(self.size())
        return super().resizeEvent(e)

    # def resizeEvent(self, e):
    #     print('nut__________preview_next')
        # self.titleBar.move(46, 0)
        # self.titleBar.resize(self.width()-46, self.titleBar.height())


class MSFluentTitleBar(FluentTitleBar):

    def __init__(self, parent):
        super().__init__(parent)
        self.hBoxLayout.insertSpacing(0, 20)
        self.hBoxLayout.insertSpacing(2, 2)


class MSFluentWindow(FluentWindowBase):
    """ Fluent window in Microsoft Store style """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(MSFluentTitleBar(self))

        # initialize layout
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackedWidget, 1)

        self.titleBar.raise_()
        self.titleBar.setAttribute(Qt.WA_StyledBackground)




class SplitTitleBar(TitleBar):

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 12)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.titleLabel.setObjectName('titleLabel')
        # self.window().windowTitleChanged.connect(self.setTitle)

        FluentStyleSheet.FLUENT_WINDOW.apply(self)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class SplitFluentWindow(QtMuiWindow):
    """ Fluent window with split style """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(SplitTitleBar(self))

        if sys.platform == "darwin":
            self.titleBar.setFixedHeight(48)

        self.widgetLayout.setContentsMargins(0, 0, 0, 0)

        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)


class FluentBackgroundTheme:
    """ Fluent background theme """
    DEFAULT = (QColor(243, 243, 243), QColor(32, 32, 32))   # light, dark
    DEFAULT_BLUE = (QColor(240, 244, 249), QColor(25, 33, 42))
