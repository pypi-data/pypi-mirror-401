from __future__ import annotations
from typing import Optional, Union

from PySide6.QtCore import QPointF, Qt, QRectF, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsItem
from PySide6.QtCharts import (
    QChart, QChartView,
    QSplineSeries, QAreaSeries,
    QBarCategoryAxis, QValueAxis,
    QScatterSeries, QLineSeries
)
from PySide6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush, QFontMetrics, QLinearGradient, QGradient
)

from qtmui.material.styles import useTheme
from qtmui.hooks import useEffect


# -------------------------------------------------------
# TooltipItem used by ChartArea
# -------------------------------------------------------
class TooltipItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lines = []
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
        # width includes marker (8px) + spacing
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

        rect = self.boundingRect()
        painter.setBrush(QBrush(self.bg_color))
        painter.setPen(QPen(self.border_color, 1))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)

        y = self.padding
        for text, color in self.lines:
            # marker circle
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.padding, y + fm.height() / 2 - 4, 8, 8)
            # text
            painter.setPen(QPen(QColor("white")))
            painter.drawText(self.padding + 14, y + fm.ascent(), text)
            y += fm.height()


# -------------------------------------------------------
# HoverChartView (to forward events to owner)
# -------------------------------------------------------
class HoverChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.owner: 'ChartArea' = None
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.owner:
            self.owner.handle_hover(event)
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if self.owner:
            self.owner.hide_hover()
        super().leaveEvent(event)


# -------------------------------------------------------
# ChartArea: QSplineSeries + QAreaSeries, tooltip, hover
# -------------------------------------------------------
class ChartArea(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        type: str = "area",
        series: object = None,
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        options: object = None,
        key: str = None,
        *args, **kwargs
    ):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        
        self._mix_type = (type == "mixed")

        # normalize series input
        self._series_input = series or []  # expect list[{"name": str, "data": [numbers]}]
        self._options = options or {}
        self._width = width
        self._height = height

        self._init_area_chart()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _init_area_chart(self):
        # sizing
        if self._height:
            self.setFixedHeight(self._height)
        if self._width:
            self.setFixedWidth(self._width)

        # Normalize and collect all data arrays, convert to floats
        all_series_data = []
        for item in self._series_input:
            if isinstance(item, dict):
                data = item.get("data", []) or []
            else:
                data = item or []
            all_series_data.append([float(v) for v in data])

        # Compute global max across all series (fix for your issue)
        max_val = max((max(d) for d in all_series_data), default=0)

        # Build spline series (QSplineSeries) and separate visible line series for each input
        # We'll create:
        #   - upper_spline (QSplineSeries) used as upper series for area (smoothed)
        #   - line_spline  (QSplineSeries) used to draw the stroke (also smoothed)
        self._spline_list = []       # visible line splines
        self._upper_list = []        # splines used as upper for area
        self._area_items = []        # tuples (upper, baseline, area, line)

        for idx, item in enumerate(self._series_input):
            name = item.get("name", "") if isinstance(item, dict) else ""
            data = all_series_data[idx]

            # create smoothed upper spline (for area)
            upper = QSplineSeries()
            for i, y in enumerate(data):
                upper.append(QPointF(float(i), float(y)))

            # create line spline (for stroke). Use a separate object so we can control legend names.
            line = QSplineSeries()
            if not self._mix_type:
                line.hide()
            for i, y in enumerate(data):
                line.append(QPointF(float(i), float(y)))
            line.setName("")  # avoid duplicate legend entries; area will carry the name

            # create baseline spline (y=0) with same x coordinates
            baseline = QSplineSeries()
            for i in range(upper.count()):
                pt = upper.at(i)
                baseline.append(QPointF(pt.x(), 0.0))

            # create area from upper and baseline
            area = QAreaSeries(upper, baseline)
            area.setName(name)  # area shown in legend

            # collect (do not attach axes here)
            self._spline_list.append(line)
            self._upper_list.append(upper)
            self._area_items.append((upper, baseline, area, line))

        # Create chart and add series (areas and lines)
        self.chart = QChart()
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignTop)

        # Axes
        categories = self._options.get("xaxis", {}).get("categories", None)
        if categories:
            from PySide6.QtCharts import QBarCategoryAxis
            self.axis_x = QBarCategoryAxis()
            self.axis_x.append(categories)
            self.axis_y = QValueAxis()
            self.axis_y.setRange(0, max_val)
        else:
            self.axis_x = QValueAxis()
            self.axis_y = QValueAxis()
            self.axis_y.setRange(0, max_val)

        # Add axes to chart first (so attachAxis can find them)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        # Add each area and its line to the chart and attach axes immediately after addSeries
        for upper, baseline, area, line in self._area_items:
            # add area first (so legend shows area), then attach axes for area
            self.chart.addSeries(area)
            # attachAxis immediately after addSeries to avoid "Series not in the chart" warning
            try:
                area.attachAxis(self.axis_x)
                area.attachAxis(self.axis_y)
            except Exception:
                # Qt can be finicky if chart is still updating; schedule small defer as fallback
                QTimer.singleShot(0, lambda a=area: (a.attachAxis(self.axis_x), a.attachAxis(self.axis_y)))

            # add the stroke line and attach its axes
            self.chart.addSeries(line)
            try:
                line.attachAxis(self.axis_x)
                line.attachAxis(self.axis_y)
            except Exception:
                QTimer.singleShot(0, lambda l=line: (l.attachAxis(self.axis_x), l.attachAxis(self.axis_y)))

        # Hover markers (one per input series)
        self.hover_markers = []
        for idx, line in enumerate(self._spline_list):
            mk = QScatterSeries()
            mk.setMarkerShape(QScatterSeries.MarkerShapeCircle)
            mk.setMarkerSize(10)
            # initial color use line's pen color (will sync in theme)
            mk.setColor(QColor("#00e5ff"))
            mk.setBorderColor(QColor("#ffffff"))
            mk.hide()
            self.chart.addSeries(mk)
            # attach axes after adding series
            try:
                mk.attachAxis(self.axis_x)
                mk.attachAxis(self.axis_y)
            except Exception:
                QTimer.singleShot(0, lambda m=mk: (m.attachAxis(self.axis_x), m.attachAxis(self.axis_y)))
            self.hover_markers.append(mk)

        # Vertical hover line
        self.hover_line = QLineSeries()
        self.hover_line.setPen(QPen(QColor("#8888ff"), 1, Qt.DashLine))
        self.hover_line.hide()
        self.chart.addSeries(self.hover_line)
        try:
            self.hover_line.attachAxis(self.axis_x)
            self.hover_line.attachAxis(self.axis_y)
        except Exception:
            QTimer.singleShot(0, lambda: (self.hover_line.attachAxis(self.axis_x), self.hover_line.attachAxis(self.axis_y)))

        # Tooltip item (custom QGraphicsItem)
        self.tooltip = TooltipItem(self.chart)
        self.tooltip.hide()

        # ChartView (use custom to forward mouse events)
        self.chart_view = HoverChartView(self.chart)
        self.chart_view.owner = self
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Add tooltip into the view's scene only if it's not already added
        scene = self.chart_view.scene()
        if scene and not self.tooltip.scene():
            scene.addItem(self.tooltip)

        self.layout().addWidget(self.chart_view)

    def hide_hover(self):
        # hide tooltip, markers, line
        self.tooltip.clear()
        self.tooltip.hide()
        self.hover_line.hide()
        for mk in self.hover_markers:
            mk.hide()

    def handle_hover(self, event):
        if not self._spline_list:
            return

        pos = event.pos()
        # use first line (spline) to map viewport pos -> value coords
        reference_series = self._spline_list[0] if self._spline_list else None
        if reference_series is None:
            return

        chart_pos = self.chart.mapToValue(pos, reference_series)
        x_float = chart_pos.x()
        # nearest integer index
        nearest_idx = round(x_float)
        # clamp index within 0..count-1 (use first upper to determine count)
        total_points = self._area_items[0][0].count() if self._area_items else 0
        nearest_idx = max(0, min(nearest_idx, max(0, total_points - 1)))

        # collect points for each upper/list
        pts = []
        for upper, baseline, area, line in self._area_items:
            if nearest_idx < upper.count():
                pts.append(upper.at(nearest_idx))
            else:
                pts.append(QPointF(nearest_idx, 0.0))

        # update hover markers and sync their colors to corresponding line/area
        for i, mk in enumerate(self.hover_markers):
            mk.clear()
            if i < len(pts):
                mk.append(pts[i])
            # sync color: use pen color of visible line (which we style later in theme)
            color = self._spline_list[i].pen().color() if i < len(self._spline_list) else QColor("#00e5ff")
            mk.setColor(color)
            mk.show()

        # update vertical line
        ymin, ymax = self.axis_y.min(), self.axis_y.max()
        self.hover_line.clear()
        self.hover_line.append(nearest_idx, ymin)
        self.hover_line.append(nearest_idx, ymax)
        self.hover_line.show()

        # tooltip content
        self.tooltip.clear()
        categories = self._options.get("xaxis", {}).get("categories")
        title = categories[nearest_idx] if categories and nearest_idx < len(categories) else f"Index {nearest_idx}"
        self.tooltip.add_line(title, QColor("#cccccc"))

        for idx, (upper, baseline, area, line) in enumerate(self._area_items):
            # get display name from area.name() (we set it earlier)
            display_name = area.name() or (self._series_input[idx].get("name") if isinstance(self._series_input[idx], dict) else "")
            value_text = f"{display_name}: {pts[idx].y():.2f}"
            color = line.pen().color()  # color of line (we'll style it in theme)
            self.tooltip.add_line(value_text, color)

        # prepare geometry
        self.tooltip.prepareGeometryChange()

        # position tooltip near the vertical line: use mapToPosition to convert a value to pixel pos
        ref = self.chart.mapToPosition(QPointF(nearest_idx, ymax), reference_series)
        plot_area = self.chart.plotArea()
        center_x = plot_area.left() + plot_area.width() / 2

        rect = self.tooltip.boundingRect()
        w = rect.width()
        # place to right or left depending on which half
        if ref.x() < center_x:
            tx = ref.x() + 15
        else:
            tx = ref.x() - w - 20
        ty = ref.y() + 10

        self.tooltip.setPos(tx, ty)
        self.tooltip.show()

    def _set_stylesheet(self):
        # unify style with your SplineChart implementation
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

        # X axis style
        try:
            self.axis_x.setGridLineVisible(False)
            self.axis_x.setLabelsBrush(text_color)
            self.axis_x.setLinePen(pen)
            self.axis_x.setLabelsFont(font)
        except Exception:
            pass

        # Y axis style
        try:
            self.axis_y.setLinePen(Qt.NoPen)
            self.axis_y.setGridLinePen(pen)
            self.axis_y.setLabelsFont(font)
        except Exception:
            pass

        legend = self.chart.legend()
        legend.setLabelBrush(text_color)

        # style area and line series consistently
        for idx, (upper, baseline, area, line) in enumerate(self._area_items):
            color = primary_color if idx == 0 else QColor(theme.palette.info.main)

            # 1. Đường viền mượt: dùng line (QSplineSeries) để vẽ stroke
            pen_line = QPen(color)
            pen_line.setWidth(3)                    # độ dày viền
            pen_line.setCapStyle(Qt.RoundCap)       # bo tròn đầu cuối (đẹp hơn)
            pen_line.setJoinStyle(Qt.RoundJoin)     # bo góc khi dữ liệu gấp khúc
            line.setPen(pen_line)

            # 2. Ẩn hoàn toàn đường viền của upper series (không cần thiết)
            upper.setPen(QPen(Qt.NoPen))            # hoặc width=0

            # 3. QUAN TRỌNG: Tắt hoàn toàn border của QAreaSeries
            area.setPen(Qt.NoPen)  # nếu để width > 0 thì Qt sẽ vẽ border zigzag!!! 

            # Fill area bằng gradient (giữ nguyên)
            grad = QLinearGradient(0, 0, 0, 1)
            grad.setCoordinateMode(QGradient.ObjectBoundingMode)
            grad.setColorAt(0.0, color.lighter(140))
            grad.setColorAt(1.0, color.darker(180))
            area.setBrush(QBrush(grad))

        # sync hover marker colors with line pens
        for i, mk in enumerate(self.hover_markers):
            if i < len(self._spline_list):
                mk.setColor(self._spline_list[i].pen().color())
                mk.setBorderColor(QColor("#ffffff"))
