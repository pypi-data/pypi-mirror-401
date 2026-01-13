from __future__ import annotations

from typing import Callable, Optional, Union, List, Dict
import random

from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PySide6.QtGui import QPainter, QColor, QBrush

from qtmui.hooks import State
from qtmui.material.styles import useTheme


class ChartPie(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        series: Optional[List[Dict]] = None,  # Danh sách dict với các key: "label", "value"
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        options: Optional[Dict] = None,
        key: str = None,
        title: Optional[Union[State, str, Callable]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._series = series or []
        self._options = options or {}
        self._title = title
        self._height = height
        self._width = width

        self._init_pie_chart()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _init_pie_chart(self):
        self.theme = useTheme()

        if self._width:
            self.setFixedWidth(self._width)
        if self._height:
            self.setFixedHeight(self._height)

        # Tạo biểu đồ dạng pie (full pie, không có lỗ giữa)
        series = QPieSeries()

        # Tính tổng giá trị để tính % cho từng phần
        total_value = sum(item.get("value", 0) for item in self._series)
        for index, data in enumerate(self._series):
            label = data.get("label", "")
            value = data.get("value", 0)
            slice = QPieSlice(label, value)
            percentage = (value / total_value * 100) if total_value > 0 else 0
            # Đặt nhãn theo định dạng "Tên: xx.x%"
            # slice.setLabel(f"{label}: {percentage:.1f}%")
            slice.setLabel(f"{percentage:.1f}%")
            # Đặt nhãn bên trong phần (giữa của slice)
            slice.setLabelPosition(QPieSlice.LabelInsideHorizontal)
            # slice.setLabelPosition(QPieSlice.LabelInsideNormal)
            # slice.setLabelPosition(QPieSlice.LabelOutside)
            slice.setLabelVisible(True)
            # Gán màu cho slice (theo thứ tự trong danh sách màu)
            # color = QColor(colors[index % len(colors)])
            palette_color = getattr(self.theme.palette, ["primary", "secondary", "error", "success", "info"][random.randint(0, 4)])
            random_color = getattr(self.theme.palette, ["primary", "secondary", "error", "success", "info"][index if index < 4 else random.randint(0, 4)]).main
            # random_color = getattr(palette_color, ["main", "dark", "darker", "light", "lighter"][random.randint(0, 4)])
            color = QColor(random_color)
            # color = QColor(self.theme.palette.info.main)
            slice.setColor(color)
            series.append(slice)

        # Để tạo hình “nón” (cone) – phần dữ liệu kéo từ tâm ra ngoài – ta không đặt hole,
        # nghĩa là chart hiển thị full pie (không có lỗ giữa)
        series.setHoleSize(0.0) # 0.6

        # Tạo chart, thêm series và đặt title (nếu có)
        self.chart = QChart()
        self.chart.addSeries(series)
        if self._title:
            self.chart.setTitle(self._title)
        # Hiển thị legend ở dưới chart
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.legend().show()

        # Tạo chart view để hiển thị chart với hiệu ứng mượt mà
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout().addWidget(self.chart_view)

    def _set_stylesheet(self):
        """
        Áp dụng các tùy chỉnh giao diện cho biểu đồ dựa trên theme.
        """
        theme = useTheme()
        text_color = QColor(theme.palette.text.secondary)
        self.chart.setTitleBrush(QBrush(text_color))
        self.chart.setBackgroundBrush(QBrush(QColor(theme.palette.background.paper)))
        self.chart.setBackgroundRoundness(10)
