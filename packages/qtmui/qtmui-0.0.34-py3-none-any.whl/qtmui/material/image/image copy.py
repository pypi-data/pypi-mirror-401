# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations
import asyncio
from functools import lru_cache

"""..site_packages.qtcompat port of the areachart example from qtmui v1.0"""
from fractions import Fraction

from typing import Optional, Union, Callable
from PySide6.QtWidgets import QLabel, QGraphicsDropShadowEffect, QHBoxLayout, QFrame, QSizePolicy
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import QSize, QThreadPool, QTimer
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme

from ..widget_base import PyWidgetBase


class Image(QLabel, PyWidgetBase):
    def __init__(
                self,
                key: str = None, # "4/3" | "3/4" | "6/4" | "4/6" | "16/9" | "9/16" | "21/9" | "9/21" | "1/1"
                ratio: str = '4/3', # "4/3" | "3/4" | "6/4" | "4/6" | "16/9" | "9/16" | "21/9" | "9/21" | "1/1"
                src: str = None,
                sx: Optional[Union[str, dict]] = {},
                height: Optional[int] = None,
                width: Optional[int] = None,
                size: Optional[QSize] = None,
                *args,
                **kwargs
                ):
        super().__init__(*args, **kwargs)

        self._key = key
        self._ratio = ratio
        self._src = src
        self._size = size
        self._height = height
        self._width = width
        self._sx = sx

        self._init_ui()

        self.theme = useTheme()
        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self.destroyed.connect(self._on_destroyed)
        self._set_stylesheet()
        

    def _init_ui(self):
        if self._src.endswith(".png"):
            self.setPixmap(QPixmap(self._src))

        if self._tooltip:
            PyWidgetBase._installTooltipFilter(self)
            self.setToolTip(self._tooltip)

        self._hBoxLayout = QHBoxLayout(self)
        self.widget = QFrame(self)

        if self._width:
            height = int(float(Fraction(self._ratio)) / self._width)
            self.setFixedWidth(self._width)
            self.setFixedHeight(height)
        elif self._height:
            height = int(float(Fraction(self._ratio)) * self._height)
            # self.setFixedWidth(width)
            self.setFixedHeight(height)
            # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        if self._size:
            if isinstance(self._size, int):
                self.setFixedSize(QSize(self._size, self._size))
            elif isinstance(self._size, QSize):
                self.setFixedSize(self._size)

        self.adjustSize()


    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

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

        stylesheet = f"""
            QLabel {{
                padding: 0px;
                background-image: url("{self._src}");
                background-repeat: no-repeat;
                background-position: center;
            }}

            {sx_qss}

        """

        self.setStyleSheet(stylesheet)
        self.setShadowEffect()

    #     QTimer.singleShot(100, lambda: asyncio.ensure_future(self._on_setup_done()))

    # async def _on_setup_done(self):
    #     if not self.isVisible():
    #         self.show()

    def showEvent(self, e):
        """ fade in """
        PyWidgetBase.showEvent(self)
        super().showEvent(e)

    def setShadowEffect(self, blurRadius=60, offset=(0, 10), color=QColor(0, 0, 0, 150)):
        """ add shadow to dialog """
        shadowEffect = QGraphicsDropShadowEffect(self.widget)
        shadowEffect.setBlurRadius(blurRadius)
        shadowEffect.setOffset(*offset)
        shadowEffect.setColor(color)
        self.widget.setGraphicsEffect(None)
        self.widget.setGraphicsEffect(shadowEffect)

    def resizeEvent(self, event):
        if not self._size and not self._width and not self._height:
            if not self._src.endswith(".png"):
                if self._height:
                    self.setFixedHeight(self._height)
                else:
                    self.setFixedHeight(int(self.width() / float(Fraction(self._ratio))))
        return super().resizeEvent(event)
