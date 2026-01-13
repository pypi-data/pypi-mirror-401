# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations

"""..site_packages.qtcompat port of the areachart example from qtmui v1.0"""

from typing import Optional, Union
import sys
from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout

from .map_change_theme import MapChangeTheme

from .map_widget import MapWindow

class Map(QWidget):
    def __init__(
                self,
                initialViewState: dict = None, 
                *args,
                **kwargs
                ):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        map = MapChangeTheme(
            initialViewState=initialViewState,
        )

        # map = MapWindow()
        self.layout().addWidget(map)
