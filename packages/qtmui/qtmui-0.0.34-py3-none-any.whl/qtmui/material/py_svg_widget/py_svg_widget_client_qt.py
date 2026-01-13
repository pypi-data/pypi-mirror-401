from __future__ import annotations

import warnings
import uuid
from PySide6.QtCore import QByteArray
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QSizePolicy

from qtmui.lib.iconify_client.iconify_client_qt import iconify_client
from qtmui.lib.iconify_client.iconify_cache import svg_cache, cache_key


class PySvgWidget(QSvgWidget):

    def __init__(self, key=None, color=None, flip=None, rotate=None,
                 width=None, height=None, size=None):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))

        self._key = key
        self._color = color
        self._flip = flip
        self._rotate = rotate
        self._width = width
        self._height = height

        self.client = iconify_client()
        self.client.apiFinished.connect(self._on_iconify)
        self.client.apiError.connect(self._on_iconify_error)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        if key:
            self.loadIcon()

    # ---------------------------------------------------------
    def loadIcon(self):
        if not self._key or ":" not in self._key:
            warnings.warn(f"Invalid Iconify key: {self._key}")
            return

        prefix, name = self._key.split(":", 1)

        args = (prefix, name)
        kwargs = {
            "color": self._color,
            "width": self._width,
            "height": self._height,
            "flip": self._flip,
            "rotate": self._rotate,
        }

        self._cache_id = cache_key(args, kwargs, "0")

        cache = svg_cache()
        if self._cache_id in cache:
            self._set_svg(cache[self._cache_id])
            return

        self.client.svg(prefix, name, **kwargs)

    # ---------------------------------------------------------
    def _on_iconify(self, key: str, data: bytes):
        if key != f"svg:{self._cache_id}":
            return

        cache = svg_cache()
        cache[self._cache_id] = data
        self._set_svg(data)

    # ---------------------------------------------------------
    def _on_iconify_error(self, key: str, msg: str):
        if key != f"svg:{self._cache_id}":
            return
        warnings.warn(f"Iconify error for {self._key}: {msg}")
        self._set_svg(b"<svg/>")

    # ---------------------------------------------------------
    def _set_svg(self, data: bytes):
        self.load(QByteArray(data))
        if self._width and self._height:
            self.setFixedSize(self._width, self._height)
