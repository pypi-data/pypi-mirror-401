# qtmui/material/chart/chart_bar.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from PySide6.QtCore import Qt, QPointF, QRectF, QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsItem, QGraphicsSceneHoverEvent
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QPercentBarSeries,
    QBarSet, QBarCategoryAxis, QValueAxis
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, QFontMetrics, QLinearGradient, QGradient
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


class HoverChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.owner: Optional['ChartBar'] = None
        self.setMouseTracking(True)

    def leaveEvent(self, event):
        if self.owner:
            self.owner.hide_tooltip()
        super().leaveEvent(event)


class ChartBar(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        type: str = "bar",
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
        self.current_hover_index = -1

        self._init_chart()

        theme = useTheme()
        theme.state.valueChanged.connect(self._apply_theme)
        self._apply_theme()

    def _normalize_series(self, raw) -> List[Dict[str, Any]]:
        if not raw:
            return []
        if isinstance(raw, (list, tuple)) and all(isinstance(x, (int, float)) for x in raw):
            return [{"name": "Series 1", "data": list(raw)}]
        if isinstance(raw, (list, tuple)) and all(isinstance(x, dict) for x in raw):
            return [{"name": x.get("name", f"Series {i+1}"), "data": x.get("data", [])} for i, x in enumerate(raw)]
        raise ValueError("series must be List[int/float] or List[dict(name=..., data=...)]")


    def _shrink_categories(self, full_categories):
        """Rút gọn categories dài giống ApexCharts, tự skip giá trị không hợp lệ"""
        if not full_categories:
            return []

        result = []
        n = len(full_categories)

        def format_dt(dt):
            """Format 2011-01-01 → Jan '11, nếu không hợp lệ thì trả về '' """
            if not dt or not isinstance(dt, str):
                return ""

            # Chuỗi phải >= 10 ký tự: YYYY-MM-DD
            if len(dt) < 10:
                return ""

            try:
                year = int(dt[0:4])
                month = int(dt[5:7])
                qd = QDate(year, month, 1)
                if not qd.isValid():
                    return ""
                return qd.toString("MMM ''yy")
            except Exception:
                return ""

        for i in range(n):
            # chỉ show một số tick chính
            if i in (0, n//3, n//2, (n*2)//3, n-1):
                result.append(format_dt(full_categories[i]))
            else:
                result.append("")

        return result


    def _init_chart(self):
        if self._height: self.setFixedHeight(self._height)
        if self._width:  self.setFixedWidth(self._width)

        self.bar_series = QPercentBarSeries() if self._options.get("chart", {}).get("stacked", False) else QBarSeries()

        self.bar_sets = []
        self.colors = []
        palette_names = ["primary", "secondary", "success", "warning", "error", "info"]

        for idx, item in enumerate(self._series):
            name = item.get("name", f"Series {idx + 1}")
            data = [float(v) for v in item.get("data", [])]

            bar_set = QBarSet(name)
            bar_set.append(data)

            color_key = palette_names[idx % len(palette_names)]
            color = getattr(useTheme().palette, color_key).main
            qcolor = QColor(color)
            self.colors.append(qcolor)

            bar_set.setBrush(QBrush(qcolor))
            pen = QPen(QColor("#ffffff"))
            pen.setWidth(2)
            bar_set.setPen(pen)

            # Chỉ cần bắt hover vào, không cần xử lý status=False nữa
            bar_set.hovered.connect(self._on_bar_hovered)

            self.bar_sets.append(bar_set)
            self.bar_series.append(bar_set)

        self.chart = QChart()
        self.chart.addSeries(self.bar_series)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignTop)
        self.chart.setAnimationOptions(QChart.NoAnimation)
        self.chart.setBackgroundRoundness(12)

        self.categories = self._options.get("xaxis", {}).get("categories") or self._options.get("categories", [])

        self.axis_x = QBarCategoryAxis()
        if self.categories:
            self.axis_x.append(self.categories)
            # full = self.categories
            # short = self._shrink_categories(full)
            # self.axis_x.append(short)
            
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.bar_series.attachAxis(self.axis_x)
        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%.0f")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.bar_series.attachAxis(self.axis_y)
            
        # if self._options.get("xaxis") is None:
        if self.categories == []:
            self.chart.legend().setVisible(False)
            self.axis_x.hide()
            self.axis_y.hide()

        self.tooltip = TooltipItem(self.chart)
        self.tooltip.hide()

        # Dùng custom view để bắt leaveEvent
        self.chart_view = HoverChartView(self.chart)
        self.chart_view.owner = self
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        # self.chart_view.scene().addItem(self.tooltip)
        scene = self.chart_view.scene()
        if scene and not self.tooltip.scene():
            scene.addItem(self.tooltip)
        self.layout().addWidget(self.chart_view)

    def _on_bar_hovered(self, status: bool, index: int):
        if not status:
            return  # Bỏ qua False – sẽ xử lý bằng leaveEvent

        self.current_hover_index = index

        # Tâm nhóm cột chính xác
        group_center_x = index + 0.5
        point_in_value = QPointF(group_center_x, self.axis_y.max() * 0.1)
        center_pos = self.chart.mapToPosition(point_in_value, self.bar_series)

        # Tooltip content
        self.tooltip.clear()
        title = self.categories[index] if self.categories and index < len(self.categories) else f"Col {index}"
        self.tooltip.add_line(title, QColor("#cccccc"))

        for i, bar_set in enumerate(self.bar_sets):
            value = bar_set.at(index) if index < bar_set.count() else 0
            self.tooltip.add_line(f"{bar_set.label()}: {value:,.0f}", self.colors[i])

        # Căn giữa tooltip
        rect = self.tooltip.boundingRect()
        plot_area = self.chart.plotArea()

        tx = center_pos.x() - rect.width() / 2
        tx = max(plot_area.left() + 10, min(tx, plot_area.right() - rect.width() - 10))
        ty = plot_area.top() + 10

        self.tooltip.setPos(tx, ty)
        self.tooltip.show()

    def hide_tooltip(self):
        """Gọi khi chuột rời khỏi toàn bộ chart"""
        self.current_hover_index = -1
        self.tooltip.clear()
        self.update()

    def _apply_theme(self):
        theme = useTheme()

        grad = QLinearGradient(0, 0, 0, 1)
        grad.setCoordinateMode(QGradient.ObjectBoundingMode)
        grad.setColorAt(0.0, QColor(theme.palette.background.paper))
        grad.setColorAt(1.0, QColor(theme.palette.background.main))
        self.chart.setBackgroundBrush(QBrush(grad))

        text_color = QColor(theme.palette.text.secondary)
        divider = QColor(theme.palette.divider)

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

        palette_names = ["primary", "secondary", "success", "warning", "error", "info"]
        for i, bar_set in enumerate(self.bar_sets):
            color_key = palette_names[i % len(palette_names)]
            color = getattr(theme.palette, color_key).main
            bar_set.setBrush(QBrush(QColor(color)))
            self.colors[i] = QColor(color)

        self.chart_view.update()