# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations

"""..site_packages.qtcompat port of the areachart example from qtmui v1.0"""

from typing import Optional, Union
import sys
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

from qtmui.material.styles import useTheme



class MapChangeTheme(QWebEngineView):
    def __init__(
                self,
                initialViewState: dict = None, 
                *args,
                **kwargs
                ):
        super().__init__(*args, **kwargs)

        self._autorun_set_theme()

 
    def _init_map(self):
        self.theme = useTheme()
        self.setUrl(QUrl("https://minimals.cc/components/extra/map"))


    def _autorun_set_theme(self):
        @store.autorun(lambda state: state.theme.palette)
        def _(palette):
            try:
                self._init_map()
            except Exception as e:
                pass
        if not hasattr(self, "theme"):
            self._init_map()