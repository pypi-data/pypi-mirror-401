# src/qtmui/material/image.py
from __future__ import annotations

import os
import hashlib
import threading
from typing import Optional, Dict

import requests
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal, QObject, QUrl, QSize, QRect, QTimer
from PySide6.QtGui import QPixmap, QPainter


# ----------------------------------------------------------------------
# Global cache + thread-safe session
# ----------------------------------------------------------------------
_pixmap_cache: Dict[str, QPixmap] = {}
_cache_lock = threading.Lock()

_session: Optional[requests.Session] = None
_session_lock = threading.Lock()


def _get_session() -> requests.Session:
    global _session
    if _session is None:
        with _session_lock:
            if _session is None:
                _session = requests.Session()
                _session.headers.update({
                    "User-Agent": "qtmui-image/1.0 (+https://github.com/your-repo)"
                })
    return _session


# ----------------------------------------------------------------------
# Worker signals – giao tiếp từ thread về main thread
# ----------------------------------------------------------------------
class _ImageWorkerSignals(QObject):
    finished = Signal(QPixmap)
    error = Signal(str)


# ----------------------------------------------------------------------
# Skeleton
# ----------------------------------------------------------------------
class Skeleton(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, x2:1,
                    stop:0 #f0f0f0, stop:0.4 #e8e8e8, stop:1 #f0f0f0);
                border-radius: 8px;
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(40, 40)


# ----------------------------------------------------------------------
# Main Img component
# ----------------------------------------------------------------------
class Img(QFrame):
    loaded = Signal()          # Khi ảnh đã hiển thị thành công
    error = Signal(str)        # Khi có lỗi

    def __init__(
        self,
        src: str = "",
        srcSet: str = None,
        alt: str = "",
        width: int = None,
        height: int = None,
        objectFit: str = "cover",      # cover | contain | fill | none
        loading: str = "lazy",         # lazy | eager
        sx: dict | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.src = src
        self.srcSet = srcSet or src
        self.alt = alt
        self.objectFit = objectFit.lower()
        self.loading = loading.lower()

        self.setAttribute(Qt.WA_StyledBackground, True)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.skeleton = Skeleton(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        layout.addWidget(self.skeleton)
        layout.addWidget(self.label)

        self.pixmap: Optional[QPixmap] = None
        self.is_loaded = False
        self._is_loading = False          # ← CỜ NGĂN TẢI TRÙNG
        self._current_task_id = 0

        # Signal nội bộ
        self._worker_signals = _ImageWorkerSignals()
        self._worker_signals.finished.connect(self._apply_pixmap)
        self._worker_signals.error.connect(lambda msg: self.error.emit(msg))

        # Eager loading
        if self.loading == "eager" and src:
            QTimer.singleShot(0, self.load)

    # ------------------------------------------------------------------
    # Public: gọi khi cần tải ảnh (lazy hoặc eager)
    # ------------------------------------------------------------------
    def load(self) -> None:
        if self.is_loaded:
            return

        # ← NGĂN GỌI NHIỀU LẦN KHI ĐANG TẢI
        if self._is_loading:
            return

        url = self._resolve_url(self.srcSet or self.src)
        if not url.isValid():
            self.error.emit("Invalid URL")
            return

        cache_key = hashlib.md5(url.toString().encode("utf-8")).hexdigest()

        # Cache hit → dùng ngay
        with _cache_lock:
            if cache_key in _pixmap_cache:
                self._apply_pixmap(_pixmap_cache[cache_key])
                return

        # Bắt đầu tải → đánh dấu
        self._is_loading = True
        self.skeleton.show()
        self.label.hide()

        # Local file → đồng bộ
        if url.isLocalFile():
            path = url.toLocalFile()
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                with _cache_lock:
                    _pixmap_cache[cache_key] = pixmap
                self._apply_pixmap(pixmap)
            else:
                self.error.emit("Failed to load local file")
            self._is_loading = False
            return

        # Remote → thread
        task_id = self._current_task_id + 1
        self._current_task_id = task_id

        def _download_thread():
            if task_id != self._current_task_id:
                return

            try:
                resp = _get_session().get(url.toString(), timeout=15)
                resp.raise_for_status()
                data = resp.content

                pixmap = QPixmap()
                if pixmap.loadFromData(data):
                    with _cache_lock:
                        _pixmap_cache[cache_key] = pixmap
                    if task_id == self._current_task_id:
                        self._worker_signals.finished.emit(pixmap)
                else:
                    if task_id == self._current_task_id:
                        self._worker_signals.error.emit("Invalid image data")
            except Exception as exc:
                if task_id == self._current_task_id:
                    self._worker_signals.error.emit(str(exc))
            finally:
                # ← LUÔN reset flag khi thread kết thúc
                if task_id == self._current_task_id:
                    self._is_loading = False

        threading.Thread(target=_download_thread, daemon=True).start()

    # ------------------------------------------------------------------
    # Chọn URL tốt nhất từ srcSet (hỗ trợ DPR)
    # ------------------------------------------------------------------
    def _resolve_url(self, srcSet: str) -> QUrl:
        if not srcSet:
            return QUrl()

        raw = srcSet.split("?")[0]
        if os.path.exists(raw):
            return QUrl.fromLocalFile(raw)

        if srcSet.startswith("file://") or "://" not in srcSet:
            return QUrl(srcSet)

        candidates = []
        for part in srcSet.replace(",", " ").split():
            cleaned = part.strip()
            if cleaned.endswith(("x", "X")) and cleaned[:-1].replace(".", "").isdigit():
                try:
                    mul = float(cleaned[:-1])
                    url_part = " ".join(cleaned.split()[:-1]).strip()
                    if url_part:
                        candidates.append((mul, url_part))
                except:
                    pass
            else:
                candidates.append((1.0, cleaned))

        if not candidates:
            return QUrl(srcSet.split()[0])

        dpr = self.devicePixelRatioF()
        best_url = max(candidates, key=lambda x: x[0] if abs(x[0] - dpr) <= 0.6 else 0)[1]
        return QUrl(best_url)

    # ------------------------------------------------------------------
    # Áp dụng pixmap (main thread)
    # ------------------------------------------------------------------
    def _apply_pixmap(self, pixmap: QPixmap) -> None:
        print("Img _apply_pixmap", self.src)
        if pixmap.isNull():
            return

        self.pixmap = pixmap
        self._update_display()

        self.skeleton.hide()
        self.label.show()
        self.is_loaded = True
        self._is_loading = False          # ← Reset flag khi thành công
        self.loaded.emit()

    # ------------------------------------------------------------------
    # Object-fit
    # ------------------------------------------------------------------
    def _update_display(self) -> None:
        if not self.pixmap or self.pixmap.isNull():
            return

        target = self.label.size()
        if target.isEmpty():
            target = QSize(200, 200)

        if self.objectFit == "contain":
            scaled = self.pixmap.scaled(target, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        elif self.objectFit == "cover":
            scaled = self.pixmap.scaled(target, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            cropped = QPixmap(target)
            cropped.fill(Qt.transparent)
            painter = QPainter(cropped)
            rect = scaled.rect()
            rect.moveCenter(QRect(0, 0, target.width(), target.height()).center())
            painter.drawPixmap(rect.topLeft(), scaled)
            painter.end()
            scaled = cropped

        elif self.objectFit == "fill":
            scaled = self.pixmap.scaled(target, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        else:  # none
            scaled = self.pixmap

        self.label.setPixmap(scaled)

    # ------------------------------------------------------------------
    # Resize
    # ------------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.is_loaded:
            self._update_display()

    # ------------------------------------------------------------------
    # Xóa cache toàn cục
    # ------------------------------------------------------------------
    @staticmethod
    def clear_cache() -> None:
        with _cache_lock:
            _pixmap_cache.clear()