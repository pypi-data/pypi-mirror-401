# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations

"""..site_packages.qtcompat port of the areachart example from qtmui v1.0"""

from typing import Optional, Union, Callable
import threading
import time
from PySide6.QtWidgets import QVBoxLayout, QStackedWidget, QStackedLayout, QSizePolicy

from ..stack import Stack
from ..box import Box

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .carousel_arrow_index import CarouselArrowIndex

class Carousel(QStackedWidget):
    def __init__(
                self,
                carouselArrowIndex: CarouselArrowIndex = None, 
                children: object = None,
                height: int = None,
                ratio: str = "4/3",
                arrows: bool = False, 
                dots: bool = False, 
                fade: bool = False, 
                rtl: bool = False, 
                autoplay: bool = True, 
                autoplayTime: int = 3, # second
                beforeChange: Callable = None,
                ref: Optional[dict] = None,
                *args,
                **kwargs
                ):
        super().__init__()

        self._carouselArrowIndex = carouselArrowIndex
        self._children = children
        self._height = height
        self._ratio = ratio
        self._arrows = arrows
        self._dots = dots 
        self._fade = fade
        self._rtl = rtl
        self._autoplay = autoplay
        self._autoplayTime = autoplayTime
        self._beforeChange = beforeChange
        self._ref = ref

        if self._carouselArrowIndex:
            self._carouselArrowIndex._index.valueChanged.connect(self._set_current_index)

        self._init_ui()

    
    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setStackingMode(QStackedLayout.StackAll)
        self.layout().setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        if self._height:
            self.setFixedHeight(self._height)

        for child in self._children:
            self.addWidget(child)

        self._render_top_widget()
        if self._carouselArrowIndex:
            self.setCurrentIndex(self._carouselArrowIndex._index.value)
        self.setCurrentWidget(self._top_widget)

        if self._autoplay:
            # auto run logic
            pass

    def _autorun_next(self):
        try:
            while True:
                time.sleep(self._autoplayTime)
                if self.underMouse():
                    continue
                self._carouselArrowIndex._onNext()
        except Exception as e:
            pass

    def _set_current_index(self, index):
        self.setCurrentIndex(index)
        self.setCurrentWidget(self._top_widget)
        self._carouselArrowIndex._set_index_arrow_text(index)

    def _render_top_widget(self):
        self._top_widget = Stack(
            direction="row",
            alignItems="flex-end",
            justifyContent="flex-end",
            children=[
                Box(children=[self._carouselArrowIndex]),
            ]
        )
        self.addWidget(self._top_widget)


    def resizeEvent(self, event):
        # self.setFixedHeight(int(self.width() / float(Fraction(self._ratio))))
        # self.setMinimumHeight(int(self.width() / float(Fraction(self._ratio))))
        return super().resizeEvent(event)

