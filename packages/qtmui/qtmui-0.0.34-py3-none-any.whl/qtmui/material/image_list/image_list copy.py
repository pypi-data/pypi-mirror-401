# src/qtmui/material/image_list.py
from __future__ import annotations
import uuid

from PySide6.QtWidgets import (
    QFrame, QScrollArea, QVBoxLayout, QGridLayout,
    QHBoxLayout, QWidget, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QRect

from qtmui.material.styles import useTheme
from qtmui.material.image import Image
from ..image_list_item import ImageListItem
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style


class ImageList(QFrame):
    def __init__(
        self,
        children=None,
        variant="standard",  # standard | quilted | masonry
        cols=3,
        rowHeight=164,
        gap=4,
        sx=None,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(f"ImageList-{str(uuid.uuid4())}")

        self._variant = variant.lower()
        self._cols = max(1, int(cols))
        self._rowHeight = rowHeight
        self._gap = gap
        self._sx = sx or {}
        self._children = children or []
        self._kwargs = {"variant": variant, **kwargs}

        self._init_ui()
        self._apply_style()

        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self._apply_style)

    def _init_ui(self):
        # Tạo container chung
        self.container = QWidget()

        # === TÁCH RIÊNG LOGIC LAYOUT THEO VARIANT ===
        if self._variant == "masonry":
            self._setup_masonry_layout()
        else:
            # standard & quilted dùng QGridLayout
            self.grid_layout = QGridLayout(self.container)
            self.grid_layout.setSpacing(self._gap)
            self.grid_layout.setContentsMargins(self._gap, self._gap, self._gap, self._gap)

            if self._variant == "quilted":
                self._layout_quilted()
            else:
                self._layout_standard()

        # ScrollArea chung
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.container)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll_area)

        self._setup_lazy_load_watcher()

    def _setup_masonry_layout(self):
        """Masonry: xếp theo cột ngắn nhất – giống hệt MUI Masonry"""
        layout = QHBoxLayout(self.container)
        layout.setSpacing(self._gap)
        layout.setContentsMargins(self._gap, self._gap, self._gap, self._gap)

        self.column_layouts = []

        # Tạo các cột
        for _ in range(self._cols):
            col_widget = QWidget()
            col_layout = QVBoxLayout(col_widget)
            col_layout.setSpacing(self._gap)
            col_layout.setAlignment(Qt.AlignTop)
            col_layout.setContentsMargins(0, 0, 0, 0)
            col_widget.setLayout(col_layout)

            self.column_layouts.append(col_layout)
            layout.addWidget(col_widget)

        # Phân phối items vào cột ngắn nhất
        column_heights = [0] * self._cols

        for child in self._children:
            if not isinstance(child, ImageListItem):
                child = ImageListItem(children=[child])

            # Ước lượng chiều cao
            item_rows = getattr(child, "rows", 1) or 1
            estimated_height = item_rows * self._rowHeight

            # Tìm cột ngắn nhất
            shortest_col = column_heights.index(min(column_heights))

            # Thêm vào cột đó
            self.column_layouts[shortest_col].addWidget(child)
            column_heights[shortest_col] += estimated_height + self._gap

    def _layout_standard(self):
        for i, child in enumerate(self._children):
            if not isinstance(child, ImageListItem):
                child = ImageListItem(children=[child])
            row = i // self._cols
            col = i % self._cols
            self.grid_layout.addWidget(child, row, col, 1, 1)
            self.grid_layout.setRowMinimumHeight(row, self._rowHeight)

    def _layout_quilted(self):
        occupied = [[False] * self._cols for _ in range(100)]
        max_row_used = 0

        for child in self._children:
            if not isinstance(child, ImageListItem):
                child = ImageListItem(children=[child])

            item_cols = max(1, getattr(child, "cols", 1) or 1)
            item_rows = max(1, getattr(child, "rows", 1) or 1)

            placed = False
            for row in range(len(occupied)):
                for col in range(self._cols - item_cols + 1):
                    can_place = all(
                        r < len(occupied) and c < self._cols and not occupied[r][c]
                        for r in range(row, row + item_rows)
                        for c in range(col, col + item_cols)
                    )
                    if can_place:
                        self.grid_layout.addWidget(child, row, col, item_rows, item_cols)
                        for r in range(row, row + item_rows):
                            while r >= len(occupied):
                                occupied.append([False] * self._cols)
                            for c in range(col, col + item_cols):
                                occupied[r][c] = True
                        max_row_used = max(max_row_used, row + item_rows)
                        placed = True
                        break
                if placed:
                    break

        for row in range(max_row_used):
            self.grid_layout.setRowMinimumHeight(row, self._rowHeight)
            self.grid_layout.setRowStretch(row, 0)
        for col in range(self._cols):
            self.grid_layout.setColumnStretch(col, 1)

    def _setup_lazy_load_watcher(self):
        self._lazy_timer = QTimer(self)
        self._lazy_timer.setInterval(100)
        self._lazy_timer.timeout.connect(self._check_visible_images)
        self._lazy_timer.start()
        QTimer.singleShot(200, self._check_visible_images)

    def _check_visible_images(self):
        scroll = self.scroll_area
        if not scroll or not scroll.viewport():
            return

        viewport = scroll.viewport()
        viewport_rect = viewport.rect()
        tolerance = 400
        check_rect = viewport_rect.adjusted(-tolerance, -tolerance, tolerance, tolerance)

        for img in self.findChildren(Image):
            if img.loading != "lazy" or img.is_loaded:
                continue

            tl = img.mapTo(viewport, img.rect().topLeft())
            br = img.mapTo(viewport, img.rect().bottomRight())
            img_rect = QRect(tl, br)

            if check_rect.intersects(img_rect):
                img.load()

        if all(getattr(img, "is_loaded", True) or img.loading != "lazy" for img in self.findChildren(Image)):
            self._lazy_timer.stop()

    def _apply_style(self):
        if not self._sx:
            return
        qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
        self.setStyleSheet(qss)