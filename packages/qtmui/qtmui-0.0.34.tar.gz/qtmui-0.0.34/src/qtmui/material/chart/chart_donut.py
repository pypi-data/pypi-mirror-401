# qtmui/material/chart/chart_donut.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsItem
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, QFontMetrics,
    QLinearGradient, QGradient
)

from qtmui.material.styles import useTheme


# === TooltipItem – Dùng chung với ChartPie (cực đẹp) ===
class TooltipItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lines = []
        self.padding = 10
        self.bg_color = QColor(20, 20, 20, 240)
        self.border_color = QColor(255, 255, 255, 80)
        self.border_radius = 8
        self.font = QFont("Segoe UI", 9)
        self._w = self._h = 0
        self.setZValue(99999)
        self.hide()

    def clear(self):
        self.lines = []
        self._w = self._h = 0
        self.hide()

    def add_line(self, text: str, color: QColor):
        self.lines.append((text, color))
        fm = QFontMetrics(self.font)
        w = fm.horizontalAdvance(text) + 20
        h = fm.height() + 4
        self._w = max(self._w, w)
        self._h += h

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._w + self.padding * 2, self._h + self.padding * 2)

    def paint(self, painter: QPainter, *args):
        if not self.lines:
            return
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.font)
        fm = QFontMetrics(self.font)

        rect = self.boundingRect()
        painter.setBrush(QBrush(self.bg_color))
        painter.setPen(QPen(self.border_color, 1))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)

        y = self.padding
        for text, color in self.lines:
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.padding, y + 2, 8, 8)
            painter.setPen(QPen(QColor("white")))
            painter.drawText(self.padding + 16, y + fm.ascent() + 2, text)
            y += fm.height() + 4


# === SmartChartView – Cập nhật tooltip theo chuột ===
class SmartChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.owner: Optional['ChartDonut'] = None
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.owner and self.owner.current_hover_slice:
            self.owner._update_tooltip_position(event.pos())
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if self.owner:
            self.owner.force_hide_tooltip()
        super().leaveEvent(event)


# === ChartDonut – HOÀN HẢO NHƯ CHARTPIE ===
class ChartDonut(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        type: str = "donut",
        series: Optional[Union[List[float], List[int]]] = None,
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        options: Optional[Dict[str, Any]] = None,
        key: Optional[str] = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._raw_series = series or []
        self._options = options or {}
        self._width = width
        self._height = height

        self.current_hover_slice: Optional[QPieSlice] = None
        self._init_chart()

        theme = useTheme()
        theme.state.valueChanged.connect(self._apply_theme)
        self._apply_theme()

    def _init_chart(self):
        if self._height: self.setFixedHeight(self._height)
        if self._width:  self.setFixedWidth(self._width)

        self.pie_series = QPieSeries()

        # Lấy labels và donut size từ options
        labels = self._options.get("labels", [f"Item {i+1}" for i in range(len(self._raw_series))])
        donut_size = self._options.get("plotOptions", {}).get("pie", {}).get("donut", {}).get("size", "65%")
        # Chuyển % → float
        if isinstance(donut_size, str) and donut_size.endswith("%"):
            donut_size = float(donut_size.rstrip("%")) / 100
        else:
            donut_size = 0.65

        self.pie_series.setHoleSize(1.0)
        self.pie_series.setHoleSize(donut_size)

        total = sum(self._raw_series)
        self.colors = []
        palette_names = ["primary", "secondary", "success", "warning", "error", "info"]

        for idx, value in enumerate(self._raw_series):
            label = labels[idx] if idx < len(labels) else f"Item {idx+1}"
            percentage = (value / total * 100) if total > 0 else 0

            slice = QPieSlice(label, value)
            slice.setLabel(f"{percentage:.1f}%")
            slice.setLabelVisible(self._options.get("dataLabels", {}).get("enabled", True))
            slice.setLabelPosition(QPieSlice.LabelInsideHorizontal)

            color_key = palette_names[idx % len(palette_names)]
            color = getattr(useTheme().palette, color_key).main
            qcolor = QColor(color)
            self.colors.append(qcolor)
            slice.setBrush(QBrush(qcolor))

            # Stroke (viền trắng)
            if self._options.get("stroke", {}).get("show", True):
                pen = QPen(QColor("#ffffff"))
                pen.setWidth(3)
                slice.setPen(pen)
            else:
                slice.setPen(Qt.NoPen)

            # Hover signal
            slice.hovered.connect(self._on_slice_hovered)
            self.pie_series.append(slice)

        # Chart setup
        self.chart = QChart()
        self.chart.addSeries(self.pie_series)
        self.chart.setAnimationOptions(QChart.NoAnimation)
        self.chart.setBackgroundRoundness(16)

        # Legend
        legend_opt = self._options.get("legend", {})
        legend = self.chart.legend()
        legend.setVisible(legend_opt.get("show", True) != False)
        pos = legend_opt.get("position", "bottom").lower()
        align_map = {"top": Qt.AlignTop, "bottom": Qt.AlignBottom, "left": Qt.AlignLeft, "right": Qt.AlignRight}
        legend.setAlignment(align_map.get(pos, Qt.AlignBottom))

        # Tooltip
        self.tooltip = TooltipItem()
        self.tooltip.hide()

        # View
        self.chart_view = SmartChartView(self.chart)
        self.chart_view.owner = self
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        # self.chart_view.scene().addItem(self.tooltip)
        scene = self.chart_view.scene()
        if scene and not self.tooltip.scene():
            scene.addItem(self.tooltip)
        self.layout().addWidget(self.chart_view)

    def _on_slice_hovered(self, status: bool):
        slice: QPieSlice = self.sender()

        if status:
            self.current_hover_slice = slice
            self._show_tooltip()
        else:
            if self.current_hover_slice == slice:
                self.current_hover_slice = None
                self.hide_tooltip()

    def _show_tooltip(self):
        if not self.current_hover_slice:
            return

        slice = self.current_hover_slice
        index = self.pie_series.slices().index(slice)
        value = self._raw_series[index]
        label = self._options.get("labels", [f"Item {i+1}" for i in range(len(self._raw_series))])[index]
        total = sum(self._raw_series)
        percentage = (value / total * 100) if total > 0 else 0

        self.tooltip.clear()
        self.tooltip.add_line(label, self.colors[index])
        self.tooltip.add_line(f"{value:,.0f} ({percentage:.1f}%)", QColor("#cccccc"))

        self.tooltip.show()
        # Vị trí sẽ được cập nhật bởi mouseMoveEvent

    def _update_tooltip_position(self, pos: QPointF):
        if not self.tooltip.isVisible():
            return

        rect = self.tooltip.boundingRect()
        tx = pos.x() - rect.width() / 2
        ty = pos.y() - rect.height() - 10

        self.tooltip.setPos(tx, ty)

    def force_hide_tooltip(self):
        self.current_hover_slice = None
        self.tooltip.hide()
        self.tooltip.clear()

    def hide_tooltip(self):
        self.tooltip.hide()
        self.tooltip.clear()

    def _apply_theme(self):
        theme = useTheme()

        # Background gradient
        grad = QLinearGradient(0, 0, 0, 1)
        grad.setCoordinateMode(QGradient.ObjectBoundingMode)
        grad.setColorAt(0.0, QColor(theme.palette.background.paper))
        grad.setColorAt(1.0, QColor(theme.palette.background.main))
        self.chart.setBackgroundBrush(QBrush(grad))

        # Text color
        text_color = QColor(theme.palette.text.secondary)
        self.chart.setTitleBrush(text_color)
        self.chart.legend().setLabelBrush(text_color)

        # Update slice colors
        palette_names = ["primary", "secondary", "success", "warning", "error", "info"]
        for i, slice in enumerate(self.pie_series.slices()):
            color_key = palette_names[i % len(palette_names)]
            color = getattr(theme.palette, color_key).main
            slice.setBrush(QBrush(QColor(color)))
            self.colors[i] = QColor(color)

        self.chart_view.update()