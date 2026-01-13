from __future__ import annotations
import sys
from typing import Any, Dict, List, Optional
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCharts import QChartView, QChart, QPieSeries, QPieSlice, QLegend

# ============================================================
# COPY NGUYÊN TooltipItem & SmartChartView từ ChartDonut
# ============================================================
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QFont, QFontMetrics, QBrush
from PySide6.QtCore import QRectF

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

    def paint(self, painter, *args):
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
        self.owner = None
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.owner and self.owner.current_hover_slice:
            self.owner._update_tooltip_position(event.pos())
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if self.owner:
            self.owner.force_hide_tooltip()
        super().leaveEvent(event)


# ============================================================
# RADIAL BAR CHART WITH DONUT-STYLE TOOLTIP
# ============================================================
class ChartRadialBar(QWidget):
    def __init__(self,
                 series: Optional[List[float]] = None,
                 options: Optional[Dict[str,Any]] = None,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 dir: str = "ltr",
                 type: str = "radialBar",
                 total: Optional[int] = None,
                 parent=None):
        super().__init__(parent)
        
        self.series = series
        self.labels = options.get("labels", [f"Series {i+1}" for i in range(len(self.series))])
        self.colors = options.get("colors")
        self.total_value = sum(self.series)
        self.series_objects = []
        self.current_hover_slice = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Chart
        self.chart = QChart()
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.setContentsMargins(0, 0, 0, 0)

        self.chart_view = SmartChartView(self.chart)
        self.chart_view.owner = self
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Tooltip
        self.tooltip = TooltipItem()
        self.tooltip.hide()
        # self.chart_view.scene().addItem(self.tooltip)
        scene = self.chart_view.scene()
        if scene and not self.tooltip.scene():
            scene.addItem(self.tooltip)
        self.layout.addWidget(self.chart_view)

        if height:
            self.setFixedHeight(height)
        if width:
            self.setFixedWidth(width)
            
        self.build_chart()

    # -----------------------------------------------------
    # BUILD RINGS
    # -----------------------------------------------------
    def build_chart(self):
        base_hole = 0.30
        ring_thickness = 0.15
        
        theme = useTheme()

        for i, value in enumerate(self.series):
            # Background track
            track = QPieSeries()
            track.setHoleSize(base_hole + i * ring_thickness)
            track.setPieSize(base_hole + (i + 1) * ring_thickness)
            track.setPieStartAngle(-90)
            track.setPieEndAngle(270)
            slice_track = QPieSlice("", 100)
            bg = QColor("#D0D0D0"); bg.setAlpha(90)
            slice_track.setBrush(bg)
            slice_track.setPen(Qt.NoPen)
            track.append(slice_track)
            self.chart.addSeries(track)

            # Actual value ring
            series = QPieSeries()
            series.setHoleSize(base_hole + i * ring_thickness)
            series.setPieSize(base_hole + (i + 1) * ring_thickness)
            series.setPieStartAngle(-90)
            series.setPieEndAngle(-90 + 360 * value / self.total_value)

            slice_val = QPieSlice(self.labels[i], value)
            slice_val.setLabelVisible(False)
            col = QColor(self.colors[i] if self.colors and i < len(self.colors) else theme.palette.primary.main)
            slice_val.setBrush(col)
            slice_val.setPen(QPen(col, 2))

            series.append(slice_val)
            slice_val.hovered.connect(self.on_hover(series_index=i, slice_obj=slice_val))

            self.chart.addSeries(series)
            self.series_objects.append(series)

    # -----------------------------------------------------
    # HOVER HANDLER → show tooltip only
    # -----------------------------------------------------
    def on_hover(self, series_index, slice_obj):
        def handle(status):
            if status:
                self.current_hover_slice = slice_obj
                self._show_tooltip(series_index, slice_obj)
            else:
                if self.current_hover_slice == slice_obj:
                    self.force_hide_tooltip()
        return handle

    # -----------------------------------------------------
    # SHOW TOOLTIP
    # -----------------------------------------------------
    def _show_tooltip(self, index, slice_obj):
        label = self.labels[index]
        value = self.series[index]
        percent = value / self.total_value * 100

        self.tooltip.clear()
        self.tooltip.add_line(label, QColor(self.colors[index]))
        self.tooltip.add_line(f"{value} ({percent:.1f}%)", QColor("#cccccc"))
        self.tooltip.show()

    def _update_tooltip_position(self, pos):
        if not self.tooltip.isVisible():
            return
        rect = self.tooltip.boundingRect()
        self.tooltip.setPos(pos.x() - rect.width() / 2,
                            pos.y() - rect.height() - 10)

    def force_hide_tooltip(self):
        self.current_hover_slice = None
        self.tooltip.hide()
        self.tooltip.clear()
