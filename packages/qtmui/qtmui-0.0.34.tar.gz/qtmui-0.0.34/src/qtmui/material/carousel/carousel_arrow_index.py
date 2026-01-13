# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations

"""..site_packages.qtcompat port of the areachart example from qtmui v1.0"""

import uuid
from typing import Optional, Union, Callable
from PySide6.QtWidgets import QFrame, QHBoxLayout


from ..button import IconButton
from ..typography import Typography
from ..box import Box
from ..spacer import VSpacer
from qtmui.hooks import useState, useEffect
from ..system.color_manipulator import alpha
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from ..py_iconify import PyIconify, Iconify
from ...qtmui_assets import QTMUI_ASSETS

from qtmui.material.styles import useTheme

class CarouselArrowIndex(QFrame):
    def __init__(
                self,
                index: object = None, # "line" | "area" | "bar" | "pie" | "donut" | "radialBar" | "scatter" | "bubble" | "heatmap" | "candlestick" | "boxPlot" | "radar" | "polarArea" | "rangeBar" | "rangeArea" | "treemap"
                setCurrentIndex: object = None, # "line" | "area" | "bar" | "pie" | "donut" | "radialBar" | "scatter" | "bubble" | "heatmap" | "candlestick" | "boxPlot" | "radar" | "polarArea" | "rangeBar" | "rangeArea" | "treemap"
                total: int = None, # "line" | "area" | "bar" | "pie" | "donut" | "radialBar" | "scatter" | "bubble" | "heatmap" | "candlestick" | "boxPlot" | "radar" | "polarArea" | "rangeBar" | "rangeArea" | "treemap"
                onNext: Callable = None, 
                onPrev: Callable = None, 
                sx: dict = None,
                *args,
                **kwargs
                ):
        super().__init__(*args, **kwargs)
        self.setObjectName(str(uuid.uuid4()))
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(4,4,4,4)

        self._index = index
        self._setCurrentIndex = setCurrentIndex
        self._total = total
        self._onNext = onNext
        self._onPrev = onPrev
        self._sx = sx

        self._indexText, self._setIndexText = useState(f"{self._index.value}/{self._total}")

        self._init_ui()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()


    def _init_ui(self):

        # self.layout().addWidget(IconButton(icon=Iconify(key=QTMUI_ASSETS.ICONS.ARROW_LEFT), onClick=self._onPrev, color="default"))
        self.layout().addWidget(IconButton(icon=Iconify(key="ri:arrow-left-s-line"), onClick=self._onPrev, color="default"))
        self.layout().addWidget(
            Box(
                children=[
                    VSpacer(),
                    Typography(text=self._indexText, variant="button", sx={"color": "palette.common.white"}),
                    VSpacer()
                ]
            )
        )
        # self.layout().addWidget(IconButton(icon=Iconify(key=QTMUI_ASSETS.ICONS.ARROW_RIGHT), onClick=self._onNext, color="default"))
        self.layout().addWidget(IconButton(icon=Iconify(key="ri:arrow-right-s-line"), onClick=self._onNext, color="default"))


    def _set_stylesheet(self):
        theme = useTheme()

        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    border: 0px solid transparent;
                    border-radius: 8px;
                    background-color: {alpha(theme.palette.grey._900, 0.7)};
                    {get_qss_style(self._sx) if self._sx else ""}
                }}
                #{self.objectName()}:hover {{
                    border: 0px solid transparent;
                    border-radius: 8px;
                    background-color: {alpha(theme.palette.grey._900, 0.7)};
                }}
            """
        )

    def _set_index_arrow_text(self, value=None):
        self._setIndexText(f"{str(value)}/{self._total}")
 

