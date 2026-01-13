from __future__ import annotations
from typing import Optional, Union
from math import pi, cos, sin
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QGradient, QLinearGradient, QPainter, QColor, QBrush, QFont, QPen, QPainterPath


from qtmui.material.styles import useTheme

class ChartRadialBar1(QWidget):
    def __init__(
        self,
        series: list = None,
        total: int = None,
        options: dict = None,
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._series = series or []
        self._total = total
        self._options = options
        self._width = int(width) if width else 200
        self._height = int(height) if height else 200
        self.percentage = 0
        self.theme = useTheme()
        
        self.setMinimumSize(self._width, self._height)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._init_widget()

        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _init_widget(self):
        if self._width:
            self.setFixedWidth(self._width)

        if self._height:
            self.setFixedHeight(self._height)
        self._add_center_label()

    def upd(self, data: list):
         self._series = data
         self.update()


    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), self.theme.palette.background.paper)

        # Calculate the drawing rectangle
        rect = self.rect().adjusted(8, 8, -8, -8)  # reduce for pen width
        side = min(rect.width(), rect.height())
        x = rect.x() + (rect.width() - side) / 2
        y = rect.y() + (rect.height() - side) / 2
        draw_rect = QRectF(x, y, side, side)

        start_angle = 270 - 180  # Start at top (12 o'clock -> 270 - 90 degrees)
        pen_width = 8
        gap = 6  # Gap between arcs
        num_arcs = len(self._series)
        for i, (_, value, color) in enumerate(self._series):
             
                end_angle = -(value / self._total) * 360 if self._total > 0 else 0  # Negative for clockwise
                path = QPainterPath()
                center = draw_rect.center()
                
                #Calculate the radius for the current arc
                current_radius = draw_rect.width()/2 - ((num_arcs - i -1) * (pen_width + gap) + pen_width/2)
                
                #Calculate the rectangle containing the current arc.
                arc_rect = QRectF(
                   center.x() - current_radius,
                   center.y() - current_radius,
                   current_radius * 2,
                   current_radius * 2
                )
                path.moveTo(center.x(), center.y())


                # Create an arc from center to edge.
                path.arcMoveTo(arc_rect, start_angle)
                path.arcTo(arc_rect, start_angle, end_angle)

                pen = QPen()
                pen.setCapStyle(Qt.FlatCap)
                pen.setColor(QColor(getattr(self.theme.palette, color).main))
                pen.setWidth(pen_width)
                p.strokePath(path, pen)




    def _add_center_label(self):
        if self._total is None:
            return

        # Create the label for 'Total'
        total_label = QLabel("Total", self)
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet(f"color: {self.theme.palette.text.secondary};")

        # Create the label for the total value
        self.total_value_label = QLabel(str(self._total), self)
        self.total_value_label.setAlignment(Qt.AlignCenter)
        self.total_value_label.setStyleSheet(f"color: {self.theme.palette.text.primary}; font-size: 14px; font-weight: bold;")

        # Create a layout to place both labels in the center
        center_layout = QVBoxLayout()
        center_layout.addWidget(total_label)
        center_layout.addWidget(self.total_value_label)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter) # Add AlignVCenter

        # Create a wrapper widget
        center_widget = QWidget(self)
        center_widget.setLayout(center_layout)

        # Add the widget to the main layout
        self.layout().addWidget(center_widget)
        self.layout().setAlignment(Qt.AlignCenter)  # Center the wrapper widget

        #  The text should now be perfectly centered

        # Adjust the size of label when the chart size changes.
        self.resizeEvent = lambda event: self._update_center_label_position(center_widget)

    def _update_center_label_position(self, center_widget):
       
        # Calculate the drawing rectangle
        rect = self.rect().adjusted(8, 8, -8, -8)  # reduce for pen width
        side = min(rect.width(), rect.height())
        x = rect.x() + (rect.width() - side) / 2
        y = rect.y() + (rect.height() - side) / 2
        draw_rect = QRectF(x, y, side, side)
        
        center_widget.setGeometry(QRectF(
            draw_rect.x(), 
            draw_rect.y(),
            draw_rect.width(),
            draw_rect.height()
        ).toRect())


    def _set_stylesheet(self):
        self.theme = useTheme()
        self.update()
        if hasattr(self, "total_value_label"):
            self.total_value_label.setStyleSheet(f"color: {self.theme.palette.text.primary}; font-size: 14px; font-weight: bold;")
