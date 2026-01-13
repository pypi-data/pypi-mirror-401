# coding:utf-8
from typing import Callable
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QEvent
from PySide6.QtGui import QColor, QResizeEvent
from PySide6.QtWidgets import (QDialog, QGraphicsDropShadowEffect, QApplication, QMainWindow,
                             QGraphicsOpacityEffect, QHBoxLayout, QWidget, QFrame)

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style


class DialogBase(QDialog):
    """ Dialog box base class with a mask """

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__()

        self._parent = parent
        self._sx = kwargs.get("sx")

        self._init_ui()



    def _init_ui(self):
        self._hBoxLayout = QHBoxLayout(self)
        self.windowMask = QWidget(self)
        self.windowMask.setObjectName('windowMask')

        # dialog box in the center of mask, all widgets take it as parent
        self.widget = QFrame(self, objectName='centerWidget')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        if self._parent:
            self.setGeometry(0, 0, self._parent.width(), self._parent.height())
        elif QApplication.instance().mainWindow:
            self.setGeometry(0, 0, QApplication.instance().mainWindow.width(), QApplication.instance().mainWindow.height())


        c = 0 if useTheme().palette.mode == "dark" else 255
        self.windowMask.resize(self.size())
        self.windowMask.setStyleSheet(f'''
            #windowMask{{
                background:rgba({c}, {c}, {c}, 0.6);
            }}
        ''')

        self._hBoxLayout.addWidget(self.widget)
        
        self.setShadowEffect()

        self.window().installEventFilter(self)

        # self._set_stylesheet()

    def _set_stylesheet(self, component_styled=None):
        
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        c = 0 if self.theme.palette.mode == "dark" else 255

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx

        # self.windowMask.setStyleSheet(f'''
        #     #windowMask{{
        #         background:rgba({c}, {c}, {c}, 0.6);
        #     }}

        #     {sx_qss}

        # ''')

        self.windowMask.setStyleSheet(f'''
            #windowMask{{
                background:red;
            }}

            {sx_qss}

        ''')
        
        self.setShadowEffect()


    def setShadowEffect(self, blurRadius=60, offset=(0, 10), color=QColor(0, 0, 0, 100)):
        """ add shadow to dialog """
        shadowEffect = QGraphicsDropShadowEffect(self.widget)
        shadowEffect.setBlurRadius(blurRadius)
        shadowEffect.setOffset(*offset)
        shadowEffect.setColor(color)
        self.widget.setGraphicsEffect(None)
        self.widget.setGraphicsEffect(shadowEffect)

    def setMaskColor(self, color: QColor):
        """ set the color of mask """
        self.windowMask.setStyleSheet(f'''
            #windowMask{{
                background: rgba({color.red()}, {color.blue()}, {color.green()}, {color.alpha()});
            }}
        ''')

    def showEvent(self, e):
        """ fade in """
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(0)
        opacityAni.setEndValue(1)
        opacityAni.setDuration(200)
        opacityAni.setEasingCurve(QEasingCurve.InSine)
        opacityAni.finished.connect(lambda: self.setGraphicsEffect(None))
        opacityAni.start()
        super().showEvent(e)

    def done(self, code):
        """ fade out """
        self.widget.setGraphicsEffect(None)
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(1)
        opacityAni.setEndValue(0)
        opacityAni.setDuration(100)
        opacityAni.finished.connect(lambda: self._onDone(code))
        opacityAni.start()

    def _onDone(self, code):
        self.setGraphicsEffect(None)
        QDialog.done(self, code)

    def resizeEvent(self, e):
        self.windowMask.resize(self.size())

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                re = QResizeEvent(e)
                self.resize(re.size())

        return super().eventFilter(obj, e)