from __future__ import annotations
from typing import Optional, Union

from PySide6.QtCore import QPointF, Qt, QRectF
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QGraphicsItem
)
from PySide6.QtCharts import (
    QChart, QChartView, QSplineSeries,
    QBarCategoryAxis, QValueAxis,
    QScatterSeries, QLineSeries
)
from PySide6.QtGui import (
    QPen, QPainter, QColor, QFont, QBrush, QFontMetrics
)

from qtmui.material.styles import useTheme


# -----------------------------------------------------
# Custom TooltipItem (marker + text + padding + border)
# -----------------------------------------------------
class TooltipItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lines = []  # [(text, QColor), ...]
        self.padding = 8
        self.bg_color = QColor(20, 20, 20, 230)
        self.border_color = QColor(255, 255, 255, 90)
        self.border_radius = 6
        self.setZValue(99999)
        self._w = 0
        self._h = 0
        self.font = QFont()
        self.font.setPointSize(9)

    def clear(self):
        self.lines = []
        self._w = 0
        self._h = 0

    def add_line(self, text: str, color: QColor):
        self.lines.append((text, color))

        fm = QFontMetrics(self.font)
        w = fm.boundingRect(text).width() + 20  # 20 = marker + spacing
        h = fm.height()

        self._w = max(self._w, w)
        self._h += h

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._w + self.padding * 2, self._h + self.padding * 2)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.setBrush(QBrush(self.bg_color))
        painter.setPen(QPen(self.border_color, 1))
        rect = self.boundingRect()
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)

        # Draw text + marker
        y = self.padding
        fm = painter.fontMetrics()

        for text, color in self.lines:
            # marker circle
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.padding, y + fm.height()/2 - 4, 8, 8)

            # text
            painter.setPen(QPen(QColor("white")))
            painter.drawText(self.padding + 14, y + fm.ascent(), text)

            y += fm.height()


# -----------------------------------------------------
# Custom ChartView for Hover
# -----------------------------------------------------
class HoverChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.setMouseTracking(True)
        self.owner: 'ChartSLine' = None

    def mouseMoveEvent(self, event):
        if self.owner:
            self.owner.handle_hover(event)
        super().mouseMoveEvent(event)


# -----------------------------------------------------
# ChartSLine
# -----------------------------------------------------
class ChartSLine(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        type: str = "line",
        series: object = None,
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        options: object = None,
        key: str = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._series_input = series or []
        self._options = options or {}
        self._width = width
        self._height = height

        self._init_chart()

        theme = useTheme()
        theme.state.valueChanged.connect(self._apply_theme)
        self._apply_theme()

    # -----------------------------------------------------
    # INIT CHART
    # -----------------------------------------------------
    def _init_chart(self):
        if self._height:
            self.setFixedHeight(self._height)
        if self._width:
            self.setFixedWidth(self._width)

        # Series
        self._spline_series_list = []
        for item in self._series_input:
            s = QSplineSeries()
            s.setName(item.get("name", ""))
            for idx, y in enumerate(item.get("data", [])):
                s.append(QPointF(float(idx), float(y)))
            self._spline_series_list.append(s)

        # Chart
        self.chart = QChart()
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignTop)

        for s in self._spline_series_list:
            self.chart.addSeries(s)

        # Axes
        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%d")

        categories = self._options.get("xaxis", {}).get("categories")
        if categories:
            self.axis_x = QBarCategoryAxis()
            self.axis_x.append(categories)
            self.axis_y.setRange(0, max(max(item["data"]) for item in self._series_input))
        else:
            self.axis_x = QValueAxis()

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        for s in self._spline_series_list:
            s.attachAxis(self.axis_x)
            s.attachAxis(self.axis_y)

        # Hover markers
        self.hover_markers = []
        for s in self._spline_series_list:
            mk = QScatterSeries()
            mk.setMarkerShape(QScatterSeries.MarkerShapeCircle)
            mk.setMarkerSize(12)
            mk.setColor(QColor(s.pen().color()))
            mk.setBorderColor(QColor("#ffffff"))
            mk.hide()
            self.chart.addSeries(mk)
            mk.attachAxis(self.axis_x)
            mk.attachAxis(self.axis_y)
            self.hover_markers.append(mk)

        # Vertical line
        self.hover_line = QLineSeries()
        self.hover_line.setPen(QPen(QColor("#8888ff"), 1, Qt.DashLine))
        self.hover_line.hide()
        self.chart.addSeries(self.hover_line)
        self.hover_line.attachAxis(self.axis_x)
        self.hover_line.attachAxis(self.axis_y)

        # TooltipItem mới
        self.tooltip = TooltipItem(self.chart)
        self.tooltip.hide()

        # ChartView
        self.chart_view = HoverChartView(self.chart)
        self.chart_view.owner = self
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.chart_view.scene().addItem(self.tooltip)

        self.layout().addWidget(self.chart_view)

    # -----------------------------------------------------
    # Hover Handler
    # -----------------------------------------------------
    def handle_hover(self, event):
        pos = event.pos()

        if not self._spline_series_list:
            return

        s0 = self._spline_series_list[0]
        chart_pos = self.chart.mapToValue(pos, s0)
        x = chart_pos.x()

        nearest_x = round(x)
        nearest_x = max(0, min(nearest_x, s0.count() - 1))

        # Collect points
        points = []
        for s in self._spline_series_list:
            points.append(s.at(nearest_x))

        # Update markers
        for i, mk in enumerate(self.hover_markers):
            mk.clear()
            mk.append(points[i])
            mk.show()

        # Vertical line
        ymin, ymax = self.axis_y.min(), self.axis_y.max()
        self.hover_line.clear()
        self.hover_line.append(nearest_x, ymin)
        self.hover_line.append(nearest_x, ymax)
        self.hover_line.show()

        # Tooltip
        self.tooltip.clear()

        # Title
        title = (
            self._options.get("xaxis", {}).get("categories", [f"Index {nearest_x}"])[nearest_x]
        )
        self.tooltip.add_line(title, QColor("#cccccc"))

        # Data rows
        for idx, s in enumerate(self._spline_series_list):
            self.tooltip.add_line(
                f"{s.name()}: {points[idx].y():.2f}",
                s.pen().color()
            )

        self.tooltip.prepareGeometryChange()

        # Position tooltip
        plot_area = self.chart.plotArea()
        ref = self.chart.mapToPosition(QPointF(nearest_x, ymax), s0)

        rect = self.tooltip.boundingRect()
        w = rect.width()
        h = rect.height()

        if ref.x() < plot_area.center().x():
            tx = ref.x() + 15
        else:
            tx = ref.x() - w - 25

        ty = ref.y() + 10

        self.tooltip.setPos(tx, ty)
        self.tooltip.show()

    # -----------------------------------------------------
    # Apply Theme
    # -----------------------------------------------------
    def _apply_theme(self):
        theme = useTheme()

        text_color = QColor(theme.palette.text.secondary)
        primary_color = QColor(theme.palette.primary.main)

        self.chart.setTitleBrush(text_color)

        font = QFont()
        font.setPointSize(8)
        font.setWeight(QFont.Weight(600))

        pen = QPen(Qt.PenStyle.DashLine)
        pen.setWidthF(0.2)
        pen.setColor(text_color)

        self.axis_x.setGridLineVisible(False)
        self.axis_x.setLabelsBrush(text_color)
        self.axis_x.setLinePen(pen)
        self.axis_x.setLabelsFont(font)

        self.axis_y.setLinePen(Qt.PenStyle.NoPen)
        self.axis_y.setGridLinePen(pen)
        self.axis_y.setLabelsFont(font)

        legend = self.chart.legend()
        legend.setLabelBrush(text_color)

        # Series Pen
        for idx, s in enumerate(self._spline_series_list):
            pen2 = QPen(primary_color if idx == 0 else QColor(theme.palette.info.main))
            pen2.setWidth(3)
            s.setPen(pen2)
