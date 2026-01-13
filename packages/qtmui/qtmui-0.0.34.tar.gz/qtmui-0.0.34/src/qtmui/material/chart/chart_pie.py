# qtmui/material/chart/chart_pie.py
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


class SmartChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.owner: Optional['ChartPie'] = None
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.owner and self.owner.current_hover_slice:
            # DÙNG event.pos() → CHÍNH XÁC TUYỆT ĐỐI, CẬP NHẬT MỖI FRAME
            self.owner._update_tooltip_position(event.pos())
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if self.owner:
            self.owner.force_hide_tooltip()
        super().leaveEvent(event)


class ChartPie(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        type: str = "pie",
        series: Optional[Union[List[Dict[str, Any]], List[float], List[int]]] = None,
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        options: Optional[Dict[str, Any]] = None,
        key: Optional[str] = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._type = type.lower()
        self._raw_series = series or []
        self._options = options or {}
        self._width = width
        self._height = height

        self._series = self._normalize_series(self._raw_series)
        self.current_hover_slice: Optional[QPieSlice] = None

        self._init_chart()

        theme = useTheme()
        theme.state.valueChanged.connect(self._apply_theme)
        self._apply_theme()

    def _normalize_series(self, raw) -> List[Dict[str, Any]]:
        if not raw:
            return []
        if isinstance(raw, (list, tuple)) and all(isinstance(x, (int, float)) for x in raw):
            labels = self._options.get("labels", [f"Item {i+1}" for i in range(len(raw))])
            return [{"label": labels[i] if i < len(labels) else f"Item {i+1}", "value": float(v)}
                    for i, v in enumerate(raw)]
        if isinstance(raw, (list, tuple)) and all(isinstance(x, dict) for x in raw):
            return [{"label": x.get("label", f"Item {i+1}"), "value": float(x.get("value", 0))}
                    for i, x in enumerate(raw)]
        raise ValueError("series must be List[int/float] or List[dict(label=..., value=...)]")

    def _init_chart(self):
        if self._height: self.setFixedHeight(self._height)
        if self._width:  self.setFixedWidth(self._width)

        self.pie_series = QPieSeries()
        self.pie_series.setHoleSize(0.4 if self._type == "donut" else 0.0)

        total = sum(item["value"] for item in self._series)
        self.colors = []
        palette_names = ["primary", "secondary", "success", "warning", "error", "info"]

        for idx, item in enumerate(self._series):
            label = item["label"]
            value = item["value"]
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

            if not self._options.get("stroke", {}).get("show", True):
                slice.setPen(Qt.NoPen)
            else:
                pen = QPen(QColor("#ffffff"))
                pen.setWidth(2)
                slice.setPen(pen)

            slice.hovered.connect(self._on_slice_hovered)
            self.pie_series.append(slice)

        self.chart = QChart()
        self.chart.addSeries(self.pie_series)
        self.chart.setAnimationOptions(QChart.NoAnimation)
        self.chart.setBackgroundRoundness(12)

        legend_opt = self._options.get("legend", {})
        legend = self.chart.legend()
        legend.setVisible(legend_opt.get("show", True) != False)
        pos = legend_opt.get("position", "bottom").lower()
        align_map = {"top": Qt.AlignTop, "bottom": Qt.AlignBottom, "left": Qt.AlignLeft, "right": Qt.AlignRight}
        legend.setAlignment(align_map.get(pos, Qt.AlignBottom))

        self.tooltip = TooltipItem()
        self.tooltip.hide()

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
            self._show_tooltip_for_current_slice()
        else:
            if self.current_hover_slice == slice:
                self.current_hover_slice = None
                self.hide_tooltip()

    def _show_tooltip_for_current_slice(self):
        if not self.current_hover_slice:
            return

        slice = self.current_hover_slice
        index = self.pie_series.slices().index(slice)
        item = self._series[index]
        value = item["value"]
        total = sum(s["value"] for s in self._series)
        percentage = (value / total * 100) if total > 0 else 0

        self.tooltip.clear()
        self.tooltip.add_line(item["label"], self.colors[index])
        self.tooltip.add_line(f"{value:,.0f} ({percentage:.1f}%)", QColor("#cccccc"))

        self.tooltip.show()
        # Không cần setPos ở đây → để mouseMoveEvent lo

    def _update_tooltip_position(self, pos: QPointF):
        """Cập nhật vị trí tooltip theo vị trí chuột từ event → MƯỢT NHƯ BƠ"""
        if not self.tooltip.isVisible():
            return

        rect = self.tooltip.boundingRect()
        tx = pos.x() - rect.width() / 2
        ty = pos.y() - rect.height() - 10  # trên đầu chuột 10px

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

        grad = QLinearGradient(0, 0, 0, 1)
        grad.setCoordinateMode(QGradient.ObjectBoundingMode)
        grad.setColorAt(0.0, QColor(theme.palette.background.paper))
        grad.setColorAt(1.0, QColor(theme.palette.background.main))
        self.chart.setBackgroundBrush(QBrush(grad))

        text_color = QColor(theme.palette.text.secondary)
        self.chart.setTitleBrush(text_color)
        self.chart.legend().setLabelBrush(text_color)

        palette_names = ["primary", "secondary", "success", "warning", "error", "info"]
        for i, slice in enumerate(self.pie_series.slices()):
            color_key = palette_names[i % len(palette_names)]
            color = getattr(theme.palette, color_key).main
            slice.setBrush(QBrush(QColor(color)))
            self.colors[i] = QColor(color)

        self.chart_view.update()