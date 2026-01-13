from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import (
    QPolarChart, QChartView, QLineSeries, QCategoryAxis, QValueAxis
)
from PySide6.QtGui import QColor, QPen, QBrush, QFont
from PySide6.QtCore import Qt, QPointF


class ChartRadar(QWidget):
    """
    ChartRadar — triển khai Radar Chart theo style ApexCharts + MUI
    Nhận:
        - series: [{"name": str, "data": [...]}, ...]
        - options: dict của useChart
        - height: chiều cao widget
    """

    def __init__(
        self, 
        series, 
        options, 
        height=320, 
        width=320, 
        parent=None
    ):
        super().__init__(parent)

        self.series_data = series
        self.options = options
        self.categories = options["xaxis"]["categories"]

        self.colors = options["colors"]
        self.stroke_width = options.get("stroke", {}).get("width", 2)
        self.fill_opacity = int(options.get("fill", {}).get("opacity", 0.48) * 255)

        self.setFixedHeight(height)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # -----------------------------------
        # 1. Tạo PolarChart
        # -----------------------------------
        self.chart = QPolarChart()
        self.chart.setAnimationOptions(QPolarChart.AllAnimations)

        # Legend
        if "legend" in options:
            lg = options["legend"]
            pos = lg.get("position", "bottom")
            if pos == "bottom":
                self.chart.legend().setAlignment(Qt.AlignBottom)
            elif pos == "top":
                self.chart.legend().setAlignment(Qt.AlignTop)

        # -----------------------------------
        # 2. ChartView
        # -----------------------------------
        self.view = QChartView(self.chart)
        self.view.setRenderHint(self.view.renderHints() | self.view.renderHints().Antialiasing)
        layout.addWidget(self.view)

        # -----------------------------------
        # 3. Trục góc (Angular Axis)
        # -----------------------------------
        angle_axis = QCategoryAxis()
        angle_axis.setStartValue(0)

        step = 360 / len(self.categories)
        angle = 0

        label_colors = options["xaxis"]["labels"]["style"]["colors"]

        for i, label in enumerate(self.categories):
            angle_axis.append(label, angle)
            angle += step

        # Áp màu label
        axis_font = QFont()
        angle_axis.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        self.chart.addAxis(angle_axis, QPolarChart.PolarOrientationAngular)

        # -----------------------------------
        # 4. Trục bán kính
        # -----------------------------------
        radius_axis = QValueAxis()
        radius_axis.setRange(0, self._compute_max_value(series))
        radius_axis.setLabelFormat("%d")
        self.chart.addAxis(radius_axis, QPolarChart.PolarOrientationRadial)

        # -----------------------------------
        # 5. Tạo series
        # -----------------------------------
        for i, s in enumerate(series):
            self._add_series(i, s, angle_axis, radius_axis)

    # ------------------------------------------------------------------
    def _compute_max_value(self, series):
        return max(max(s["data"]) for s in series)

    # ------------------------------------------------------------------
    def _add_series(self, index, s, angle_axis, radius_axis):
        name = s.get("name", f"Series {index+1}")
        values = s["data"]

        # ----------------------
        # Lấy màu theo index
        # ----------------------
        color = QColor(self.colors[index % len(self.colors)])

        # ----------------------
        # Tạo LineSeries
        # ----------------------
        line = QLineSeries()
        line.setName(name)

        # Line color + stroke width
        pen = QPen(color, self.stroke_width)
        pen.setCosmetic(True)
        line.setPen(pen)

        # BẮT BUỘC để Qt áp màu series
        line.setColor(color)

        # Polygon fill
        fill_color = QColor(color)
        fill_color.setAlpha(self.fill_opacity)
        line.setBrush(QBrush(fill_color))

        # Điểm: Qt yêu cầu dạng (angle, radius)
        step_angle = 360 / len(values)
        angle = 0

        for v in values:
            line.append(QPointF(angle, v))
            angle += step_angle

        # nối điểm đầu = polygon
        line.append(QPointF(0, values[0]))

        # Đảm bảo Qt vẽ polygon (nếu không Qt chỉ vẽ line)
        line.setPointsVisible(False)

        # Thêm vào chart
        self.chart.addSeries(line)
        line.attachAxis(angle_axis)
        line.attachAxis(radius_axis)
