# src/qtmui/material/image.py
from __future__ import annotations

import os
import hashlib
from typing import Optional

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QUrl, Signal, QSize, QRect
from PySide6.QtGui import QPixmap, QPainter, QPalette
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


# Global cache
_pixmap_cache: dict[str, QPixmap] = {}


# Singleton network manager – có parent
_network_manager: Optional[QNetworkAccessManager] = None
def get_network_manager() -> QNetworkAccessManager:
    global _network_manager
    if _network_manager is None:
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        _network_manager = QNetworkAccessManager(app if app else None)
        _network_manager.setTransferTimeout(30000)
    return _network_manager


class Skeleton(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            border-radius: 8px;
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        """)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(40, 40)


class Img(QFrame):
    loaded = Signal()
    error = Signal(str)

    def __init__(
        self,
        src: str = "",
        srcSet: str = None,
        alt: str = "",
        width: int = None,
        height: int = None,
        objectFit: str = "cover",
        loading: str = "lazy",  # lazy | eager
        sx: dict | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.src = src
        self.srcSet = srcSet or src
        self.alt = alt
        self.objectFit = objectFit.lower()
        self.loading = loading.lower()

        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.skeleton = Skeleton(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        # moi them
        # self.label.setBackgroundRole(QPalette.ColorRole.Base)
        # self.label.setSizePolicy(QSizePolicy.Policy.Ignored,
        #                                 QSizePolicy.Policy.Ignored)
        # self.label.setScaledContents(True)
        
        layout.addWidget(self.skeleton)
        layout.addWidget(self.label)


        self.pixmap = QPixmap()
        self.is_loaded = False

        # Chỉ load ngay nếu là eager
        if self.loading == "eager" and src:
            from PySide6.QtCore import QTimer
            QTimer.singleShot(0, self.load)

    def load(self):
        """Public method – được gọi từ ImageList khi vào viewport"""
        if self.is_loaded:
            return

        url = self._resolve_url(self.srcSet or self.src)
        if not url.isValid():
            return

        self.cache_key = hashlib.md5(url.toString().encode()).hexdigest()
        if self.cache_key in _pixmap_cache:
            self._apply_pixmap(_pixmap_cache[self.cache_key])
            return

        self.skeleton.show()
        self.label.hide()

        if url.isLocalFile():
            path = url.toLocalFile()
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                _pixmap_cache[self.cache_key] = pixmap
                self._apply_pixmap(pixmap)
        else:
            # Img tự quản lý network manager
            self.network_manager = QNetworkAccessManager(self)
            self.network_manager.finished.connect(self.handle_reply)
            request = QNetworkRequest(QUrl(url))
            request.setAttribute(QNetworkRequest.CacheLoadControlAttribute, QNetworkRequest.PreferCache)
            self.network_manager.get(request)
          
            # sử dụng global network manager
            # request = QNetworkRequest(QUrl(url))
            # request.setAttribute(QNetworkRequest.CacheLoadControlAttribute, QNetworkRequest.PreferCache)
            # self.network_manager = get_network_manager().get(request)
            # self.network_manager.finished.connect(self.handle_reply)


    def handle_reply(self, reply: QNetworkReply):
        print("Img handle_reply", self.src)
        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                _pixmap_cache[self.cache_key] = pixmap
                self._apply_pixmap(pixmap)
        else:
            print(f"Error: {reply.errorString()}")
        reply.deleteLater()


    def _resolve_url(self, srcSet: str) -> QUrl:
        if not srcSet:
            return QUrl()

        raw = srcSet.split("?")[0]
        if os.path.exists(raw):
            return QUrl.fromLocalFile(raw)
        if srcSet.startswith("file://") or "://" not in srcSet:
            return QUrl(srcSet)

        # Chọn URL tốt nhất theo DPR
        candidates = []
        for part in srcSet.replace(",", " ").split():
            if part.endswith("x"):
                try:
                    mul = float(part[:-1])
                    url = " ".join(part.split()[:-1]).strip()
                    candidates.append((mul, url))
                except:
                    pass
            else:
                candidates.append((1.0, part.strip()))

        if not candidates:
            return QUrl(srcSet.split()[0])

        dpr = self.devicePixelRatioF()
        best_url = max(candidates, key=lambda x: x[0] if x[0] <= dpr + 0.5 else 0)[1]
        return QUrl(best_url)


    def _apply_pixmap(self, pixmap: QPixmap):
        self.pixmap = pixmap
        self._update_display()
        self.skeleton.hide()
        self.label.show()
        self.is_loaded = True
        self.loaded.emit()

    def _update_display(self):
        if self.pixmap.isNull():
            return
        size = self.label.size()
        if size.isEmpty():
            size = QSize(200, 200)

        if self.objectFit == "contain":
            scaled = self.pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        elif self.objectFit == "cover":
            scaled = self.pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            cropped = QPixmap(size)
            cropped.fill(Qt.transparent)
            p = QPainter(cropped)
            r = scaled.rect()
            r.moveCenter(QRect(0, 0, size.width(), size.height()).center())
            p.drawPixmap(r.topLeft(), scaled)
            p.end()
            scaled = cropped
        elif self.objectFit == "fill":
            scaled = self.pixmap.scaled(size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        else:
            scaled = self.pixmap
        self.label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.is_loaded:
            self._update_display()
            
    # def showEvent(self, event):
    #     print(self.src, "showEvent")
    #     return super().showEvent(event)