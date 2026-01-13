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
# TooltipItem (marker circle + text + border)
# -----------------------------------------------------
class TooltipItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lines = []          # [(text, QColor)]
        self.padding = 8
        self.bg_color = QColor(20, 20, 20, 230)
        self.border_color = QColor(255, 255, 255, 90)
        self.border_radius = 6
        self.font = QFont("Segoe UI", 9)

        self._w = 0
        self._h = 0
        self.setZValue(99999)
        self.hide()

    def clear(self):
        self.lines = []
        self._w = 0
        self._h = 0
        self.hide()

    def add_line(self, text: str, color: QColor):
        self.lines.append((text, color))
        fm = QFontMetrics(self.font)

        # marker = 8px + spacing 6px
        w = fm.horizontalAdvance(text) + 8 + 6
        h = fm.height()

        self._w = max(self._w, w)
        self._h += h

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0,
                      self._w + self.padding * 2,
                      self._h + self.padding * 2)

    def paint(self, painter: QPainter, option, widget=None):
        if not self.lines:
            return

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.font)
        fm = QFontMetrics(self.font)

        # Background
        rect = self.boundingRect()
        painter.setBrush(QBrush(self.bg_color))
        painter.setPen(QPen(self.border_color, 1))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)

        # Content
        y = self.padding

        for text, color in self.lines:
            # --- marker ---
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.padding,
                                y + fm.height() / 2 - 4, 8, 8)

            # --- text ---
            painter.setPen(QPen(QColor("white")))
            painter.drawText(self.padding + 14,
                             y + fm.ascent(), text)

            y += fm.height()


# -----------------------------------------------------
# ChartView with hover + leave
# -----------------------------------------------------
class HoverChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.owner: 'ChartSLine' = None
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.owner:
            self.owner.handle_hover(event)
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if self.owner:
            self.owner.hide_hover()
        super().leaveEvent(event)


# -----------------------------------------------------
# ChartSSpline
# -----------------------------------------------------
class ChartSpline(QWidget):
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

        # Build series
        self._spline_series_list = []
        for item in self._series_input:
            s = QSplineSeries()
            s.setName(item.get("name", ""))

            for idx, y in enumerate(item.get("data", [])):
                s.append(float(idx), float(y))

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

        categories = self._options.get("xaxis", {}).get("categories", None)
        if categories:
            self.axis_x = QBarCategoryAxis()
            self.axis_x.append(categories)
            self.axis_y.setRange(0, max(max(item["data"]) for item in self._series_input))
        else:
            self.axis_x = QValueAxis()

        if self._options.get("xaxis") is None:
            self.chart.legend().setVisible(False)
            self.axis_x.hide()
            self.axis_y.hide()

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

        # Tooltip
        self.tooltip = TooltipItem(self.chart)
        self.tooltip.hide()

        # ChartView
        self.chart_view = HoverChartView(self.chart)
        self.chart_view.owner = self
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        # self.chart_view.scene().addItem(self.tooltip)
        scene = self.chart_view.scene()
        if scene and not self.tooltip.scene():
            scene.addItem(self.tooltip)
        self.layout().addWidget(self.chart_view)

    # -----------------------------------------------------
    # HIDE hover components
    # -----------------------------------------------------
    def hide_hover(self):
        self.tooltip.clear()
        self.hover_line.hide()
        for mk in self.hover_markers:
            mk.hide()

    # -----------------------------------------------------
    # Hover Handler
    # -----------------------------------------------------
    def handle_hover(self, event):
        # lấy tọa độ chuột trong chart view
        pos = event.pos()

        if not self._spline_series_list:
            return

        # map tọa độ chuột về tọa độ chart, lấy giá trị x
        s0 = self._spline_series_list[0]
        chart_pos = self.chart.mapToValue(pos, s0)
        x = chart_pos.x()

        # tìm điểm dữ liệu gần nhất phía bên phải trên trục x
        nearest_x = round(x)
        nearest_x = max(0, min(nearest_x, s0.count() - 1))

        # lấy các điểm y tương ứng nearest_x từ tất cả series
        pts = [s.at(nearest_x) for s in self._spline_series_list]

        # cập nhật vị trí hover markers
        for i, mk in enumerate(self.hover_markers):
            mk.clear()
            mk.append(pts[i])
            mk.show()

        # vertical line cập nhật theo nearest_x
        ymin, ymax = self.axis_y.min(), self.axis_y.max()
        self.hover_line.clear()
        self.hover_line.append(nearest_x, ymin)
        self.hover_line.append(nearest_x, ymax)
        self.hover_line.show()

        # tooltip content
        self.tooltip.clear()

        categories = self._options.get("xaxis", {}).get("categories")
        title = categories[nearest_x] if categories else f"Index {nearest_x}"
        self.tooltip.add_line(title, QColor("#cccccc"))

        for i, s in enumerate(self._spline_series_list):
            self.tooltip.add_line(
                f"{s.name()}: {pts[i].y():.2f}",
                s.pen().color()
            )

        self.tooltip.prepareGeometryChange()

        # tooltip position
        plot_area = self.chart.plotArea()
        ref = self.chart.mapToPosition(QPointF(nearest_x, ymax), s0)
        
        rect = self.tooltip.boundingRect()
        w = rect.width()

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

        pen = QPen(Qt.DashLine)
        pen.setWidthF(0.2)
        pen.setColor(text_color)

        self.axis_x.setGridLineVisible(False)
        self.axis_x.setLabelsBrush(text_color)
        self.axis_x.setLinePen(pen)
        self.axis_x.setLabelsFont(font)

        self.axis_y.setLinePen(Qt.NoPen)
        self.axis_y.setGridLinePen(pen)
        self.axis_y.setLabelsFont(font)

        legend = self.chart.legend()
        legend.setLabelBrush(text_color)

        # series pen
        for idx, s in enumerate(self._spline_series_list):
            p = QPen(primary_color if idx == 0 else QColor(theme.palette.info.main))
            p.setWidth(3)
            s.setPen(p)
