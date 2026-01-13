from __future__ import annotations

import os
import re
import hashlib
from typing import Optional, Callable
from functools import lru_cache

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QUrl, Signal, QSize, QRect, QTimer, QFileInfo
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.utils.data import deep_merge
from qtmui.hooks import State, useEffect
from qtmui.material.styles import useTheme

# ----------------------------------------------------------------------
# Global cache + singleton network manager
# ----------------------------------------------------------------------
_pixmap_cache: dict[str, QPixmap] = {}

_network_manager: Optional[QNetworkAccessManager] = None

def get_network_manager() -> QNetworkAccessManager:
    global _network_manager
    if _network_manager is None:
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        _network_manager = QNetworkAccessManager(app if app else None)
        _network_manager.setTransferTimeout(30000)
    return _network_manager


# ----------------------------------------------------------------------
# Skeleton placeholder
# ----------------------------------------------------------------------
class Skeleton(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, x2:1,
                    stop:0 #f6f7f8, stop:0.4 #edeef1, stop:1 #f6f7f8);
                border-radius: 8px;
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(40, 40)


# ----------------------------------------------------------------------
# Image Component with ratio & rounded clipping support
# ----------------------------------------------------------------------
class Image(QFrame):
    loaded = Signal()
    error = Signal(str)

    def __init__(
        self,
        src: str = "",
        alt: str = "",
        ratio: str | None = None,   # "16/9"
        objectFit: str = "cover",
        loading: str = "eager",
        sx: dict | None = None,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(str(id(self)))

        # store sx and kwargs for style system
        self._sx = sx or {}
        if sx:
            self._setSxDict(sx)

        self._kwargs = kwargs.copy()
        self._setKwargs(self._kwargs)

        self.src = src
        self.alt = alt
        self.ratio = ratio
        self.objectFit = objectFit.lower()
        self.loading = loading.lower()

        # parse ratio value (float width/height)
        self._ratio_value = self._parse_ratio(ratio)

        # default border radius (px). Will be overridden by sx if provided.
        self._border_radius = self._extract_border_radius(self._get_sx())

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.skeleton = Skeleton(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(False)
        # background of label must be transparent to allow rounded composite
        self.label.setAttribute(Qt.WA_TranslucentBackground, True)

        layout.addWidget(self.skeleton)
        layout.addWidget(self.label)

        self.pixmap = QPixmap()
        self.is_loaded = False
        self._is_loading = False
        self._current_reply: Optional[QNetworkReply] = None

        # Pre-set ratio placeholder height
        if self._ratio_value:
            QTimer.singleShot(0, self._apply_ratio_placeholder)

        if self.loading == "eager" and src:
            QTimer.singleShot(0, self.load)

        useEffect(
            lambda: self._setStyleSheet(),
            [useTheme().state]
        )
        self._setStyleSheet()

    # ---------------------------
    # sx utilities
    # ---------------------------
    def _get_sx(self):
        """Assign value from various forms (State, Callable, dict)"""
        sx = self._sx
        if isinstance(sx, State):
            sx = sx.value
        if isinstance(sx, Callable):
            sx = sx()
        return sx or {}

    @classmethod
    def _setSxDict(cls, sx: dict = {}):
        if isinstance(sx, State):
            sx = sx.value
        if isinstance(sx, Callable):
            sx = sx()
        cls.sxDict = sx

    @classmethod
    @lru_cache(maxsize=128)
    def _getStyleSheet(cls, styledConfig: str="Box"):
        theme = useTheme()
        if hasattr(cls, "styledDict"):
            themeComponent = deep_merge(theme.components, cls.styledDict)
        else:
            themeComponent = theme.components

        PyBox_root = themeComponent["PyBox"].get("styles")["root"](cls.ownerState)
        PyBox_root_qss = get_qss_style(PyBox_root, class_name=f"Box")

        return PyBox_root_qss

    @classmethod
    @lru_cache(maxsize=128)
    def _getSxQss(cls, sxStr: str = "", className: str = "PyWidgetBase"):
        sx_qss = get_qss_style(cls.sxDict, class_name=className)
        return sx_qss

    @classmethod
    def _setSx(cls, sx: dict = {}):
        if isinstance(sx, State):
            sx = sx.value
        if isinstance(sx, Callable):
            sx = sx()
        cls.sxDict = sx

    @classmethod
    def _setKwargs(cls, kwargs: dict = {}):
        cls.ownerState = kwargs

    def _setStyleSheet(self):
        sx = self._get_sx()

        sxQss = ""
        if sx:
            sxQss = self._getSxQss(sxStr=str(sx), className=f"#{self.objectName()}")

        stylesheet = f"""
            {sxQss}
        """
        self.label.setStyleSheet(stylesheet)

        # update border radius cache from sx
        self._border_radius = self._extract_border_radius(sx)

    # ---------------------------
    # parse helpers
    # ---------------------------
    def _parse_ratio(self, ratio: Optional[str]) -> Optional[float]:
        if not ratio:
            return None
        try:
            w, h = ratio.split("/")
            w = float(w.strip())
            h = float(h.strip())
            if h == 0:
                return None
            return w / h
        except Exception:
            return None

    def _extract_border_radius(self, sx: dict | None) -> int:
        """
        Try to extract border-radius value from sx dict.
        Accept keys: borderRadius, border-radius, border_radius
        Accept values like: 8, "8px", "8"
        Returns integer pixels (default 8)
        """
        default = 0
        if not sx or not isinstance(sx, dict):
            return default

        candidates = []
        for key in ("borderRadius", "border-radius", "border_radius"):
            if key in sx:
                candidates.append(sx[key])

        if not candidates:
            return default

        val = candidates[0]
        if isinstance(val, (int, float)):
            return int(val * useTheme().spacing.default_spacing)
        if isinstance(val, str):
            # extract number
            m = re.search(r"(\d+)", val)
            if m:
                return int(m.group(1))
        return default

    # ---------------------------------------------------------------
    def _apply_ratio_placeholder(self):
        if not self._ratio_value:
            return
        if self.width() <= 1:
            QTimer.singleShot(10, self._apply_ratio_placeholder)
            return
        h = int(self.width() / self._ratio_value)
        self.setFixedHeight(h)

    # ------------------------------------------------------------------
    # Image loading logic
    # ------------------------------------------------------------------
    def load(self):
        if self.is_loaded or self._is_loading:
            return

        url = self._resolve_url(self.src)

        if not url.isValid():
            self.error.emit("Invalid URL")
            return

        # CACHE
        cache_key = hashlib.md5(url.toString().encode()).hexdigest()
        if cache_key in _pixmap_cache:
            self._apply_pixmap(_pixmap_cache[cache_key])
            return

        self._is_loading = True
        self.skeleton.show()
        self.label.hide()

        # Local File
        if url.isLocalFile():
            path = url.toLocalFile()
            pixmap = QPixmap(path)

            if not pixmap.isNull():
                _pixmap_cache[cache_key] = pixmap
                self._apply_pixmap(pixmap)
            else:
                self.error.emit(f"Failed to load local file: {path}")

            self._is_loading = False
            return

        # Network
        if self._current_reply:
            self._current_reply.abort()
            self._current_reply.deleteLater()

        manager = get_network_manager()
        request = QNetworkRequest(url)
        request.setAttribute(QNetworkRequest.CacheLoadControlAttribute, QNetworkRequest.PreferCache)

        reply = manager.get(request)
        self._current_reply = reply
        reply.finished.connect(self._handle_reply)

    # ------------------------------------------------------------------
    # Network reply handler
    # ------------------------------------------------------------------
    def _handle_reply(self):
        reply = self.sender()
        if reply != self._current_reply:
            return

        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                cache_key = hashlib.md5(reply.url().toString().encode()).hexdigest()
                _pixmap_cache[cache_key] = pixmap
                self._apply_pixmap(pixmap)
            else:
                self.error.emit("Invalid image data")
        elif reply.error() != QNetworkReply.OperationCanceledError:
            self.error.emit(reply.errorString())

        reply.deleteLater()
        self._current_reply = None
        self._is_loading = False

    # ---------------------------------------------------------------
    def _resolve_url(self, src: str) -> QUrl:
        if not src:
            return QUrl()

        # QResource
        if src.startswith(":/"):
            fi = QFileInfo(src)
            if fi.exists():
                return QUrl.fromLocalFile(fi.absoluteFilePath())
            return QUrl()

        # http / https
        if src.startswith("http://") or src.startswith("https://"):
            return QUrl(src)

        # file://
        if src.startswith("file://"):
            return QUrl(src)

        # Local path
        fi = QFileInfo(src)
        if fi.exists():
            return QUrl.fromLocalFile(fi.absoluteFilePath())

        return QUrl()

    # ------------------------------------------------------------------
    def _apply_pixmap(self, pixmap: QPixmap):
        if pixmap.isNull():
            return

        self.pixmap = pixmap
        self.is_loaded = True
        self._is_loading = False

        self.skeleton.hide()
        self.label.show()

        QTimer.singleShot(0, self._update_display)
        self.loaded.emit()

    # ------------------------------------------------------------------
    # Helper: create rounded pixmap mask + composite
    # ------------------------------------------------------------------
    def _rounded_pixmap(self, src_pix: QPixmap, radius: int) -> QPixmap:
        """
        Return a QPixmap same size as src_pix but with rounded corners (alpha).
        """
        if src_pix.isNull():
            return src_pix

        w = src_pix.width()
        h = src_pix.height()

        out = QPixmap(w, h)
        out.fill(Qt.transparent)

        painter = QPainter(out)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRect(0, 0, w, h), radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, src_pix)
        painter.end()
        return out

    # ------------------------------------------------------------------
    # Apply ratio + scale + objectFit + rounded mask
    # ------------------------------------------------------------------
    def _update_display(self):
        if self.pixmap.isNull() or not self.isVisible():
            return

        # update border radius from sx each time in case sx changed
        self._border_radius = self._extract_border_radius(self._get_sx())

        available_width = self.width()
        if available_width <= 1:
            QTimer.singleShot(10, self._update_display)
            return

        # -----------------------
        # 1) RATIO wins
        # -----------------------
        if self._ratio_value:
            new_height = int(available_width / self._ratio_value)
        else:
            original = self.pixmap.size()
            new_height = int(available_width * original.height() / original.width())

        # -----------------------
        # 2) objectFit
        # -----------------------
        if self.objectFit == "cover":
            scaled = self.pixmap.scaled(
                available_width, new_height,
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation,
            )
            # crop center
            cropped = QPixmap(available_width, new_height)
            cropped.fill(Qt.transparent)
            painter = QPainter(cropped)
            x = (scaled.width() - available_width) // 2
            y = (scaled.height() - new_height) // 2
            painter.drawPixmap(0, 0, scaled, x, y, available_width, new_height)
            painter.end()
            final_pixmap = cropped

        elif self.objectFit in ["contain", "none"]:
            final_pixmap = self.pixmap.scaled(
                available_width, new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

        else:  # fill
            final_pixmap = self.pixmap.scaled(
                available_width, new_height,
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation,
            )

        # apply rounded corners
        radius = max(0, int(self._border_radius))
        
        # final_pixmap = final_pixmap.scaledToHeight(new_height - 28)
        if radius > 0:
            final_pixmap = self._rounded_pixmap(final_pixmap, radius)

        # set pixmap
        self.label.setPixmap(final_pixmap)

        # ensure label geometry and widget height matches final image
        if new_height != self.height():
            self.setFixedHeight(new_height)

    # ------------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self._ratio_value:
            self._apply_ratio_placeholder()

        if self.is_loaded:
            QTimer.singleShot(0, self._update_display)

    # ------------------------------------------------------------------
    def __del__(self):
        if self._current_reply:
            self._current_reply.abort()
            self._current_reply.deleteLater()
            self._current_reply = None

    @staticmethod
    def clear_cache():
        _pixmap_cache.clear()
