from typing import (
    Any,
    Awaitable,
    Callable,
    Concatenate,
    Generic,
    Optional,
    cast,
    overload,
)
import uuid

from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, Property, QObject, QTimer, QEvent, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QPainterPath

from qtmui.hooks import State

from ..system.color_manipulator import get_palette_text_color, hex_string_to_qcolor

from ..widget_base import PyWidgetBase

from qtmui.material.styles import useTheme

class RippleEffect(QObject):
    """Ripple effect handler for button interactions."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._radius = 0
        self._max_radius = 100
        self._opacity = 1.0
        self._center = QPoint(0, 0)

    def radius(self):
        return self._radius

    def setRadius(self, radius):
        self._radius = radius
        self.parent().update()

    def opacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.parent().update()

    def center(self):
        return self._center

    def setCenter(self, center):
        self._center = center

    radius = Property(int, fget=radius, fset=setRadius)
    opacity = Property(float, fget=opacity, fset=setOpacity)
    center = Property(QPoint, fget=center, fset=setCenter)

class MenuItemBase(QPushButton, PyWidgetBase):
    mouseEnterSignal = Signal()
    mouseLeaverSignal = Signal()

    """
    Button cơ bản với hỗ trợ các sự kiện tương tác, hiệu ứng ripple, và các thuộc tính khác.
    """

    def __init__(
        self,
        id: str = None,  # ===========> xem lại
        key: str = None,  # ===========> xem lại
        value: object = None,  # ===========> xem lại
        action: Optional[Callable] = None,  # Tham chiếu hành động bắt buộc. Hiện chỉ hỗ trợ hành động focusVisible().
        centerRipple: bool = False,  # Nếu là True, hiệu ứng ripple sẽ được đặt ở trung tâm. Nó sẽ không bắt đầu tại vị trí tương tác của chuột.
        children: Optional[object] = None,  # Nội dung của component.
        classes: Optional[dict] = None,  # Ghi đè hoặc mở rộng các kiểu được áp dụng cho component.
        component: Optional[object] = None,  # Component sử dụng cho nút gốc. Có thể là chuỗi tên thẻ HTML hoặc một component khác.
        disabled: bool = False,  # Nếu là True, component sẽ bị vô hiệu hóa.
        disableRipple: bool = False,  # Nếu là True, hiệu ứng ripple sẽ bị vô hiệu hóa.
        disableTouchRipple: bool = False,  # Nếu là True, hiệu ứng ripple khi chạm sẽ bị vô hiệu hóa.
        focusRipple: bool = False,  # Nếu là True, button cơ bản sẽ có hiệu ứng ripple khi focus bằng bàn phím.
        focusVisibleClassName: Optional[str] = None,  # Thuộc tính giúp xác định phần tử nào đang có focus từ bàn phím.
        LinkComponent: Optional[object] = None,  # Component dùng để render liên kết khi thuộc tính href được cung cấp.
        onFocusVisible: Optional[Callable] = None,  # Callback gọi khi component được focus bằng bàn phím.
        sx: Optional[object] = None,  # Thuộc tính hệ thống cho phép định nghĩa override hệ thống và các kiểu CSS bổ sung.
        tabIndex: Optional[int] = 0,  # Chỉ số tab để quản lý thứ tự focus khi điều hướng bằng bàn phím.
        TouchRippleProps: Optional[dict] = None,  # Các thuộc tính được áp dụng cho phần tử TouchRipple.
        touchRippleRef: Optional[Callable] = None,  # Tham chiếu tới phần tử TouchRipple.
        tooltip: Optional[str] = None,  # Tham chiếu tới phần tử TouchRipple.
        tooltipMaxWidth: Optional[int] = 300,  # Tham chiếu tới phần tử TouchRipple.
        tooltipPlacement: Optional[str] = "bottom",  # Tham chiếu tới phần tử TouchRipple.
        onBlur: Optional[Callable] = None,  # Callback khi sự kiện mất focus diễn ra.
        onClick: Optional[Callable] = None,  # Callback khi sự kiện click diễn ra.
        onMouseEnter: Optional[Callable] = None,  # Callback khi sự kiện click diễn ra.
        onContextMenu: Optional[Callable] = None,  # Callback khi sự kiện context menu (nhấn chuột phải) diễn ra.
        onFocus: Optional[Callable] = None,  # Callback khi sự kiện focus diễn ra.
        onKeyDown: Optional[Callable] = None,  # Callback khi sự kiện nhấn phím diễn ra.
        onKeyUp: Optional[Callable] = None,  # Callback khi sự kiện nhả phím diễn ra.
        onMouseDown: Optional[Callable] = None,  # Callback khi sự kiện nhấn chuột diễn ra.
        onMouseLeave: Optional[Callable] = None,  # Callback khi sự kiện di chuột ra khỏi component diễn ra.
        onMouseUp: Optional[Callable] = None,  # Callback khi sự kiện nhả chuột diễn ra.
        onDragLeave: Optional[Callable] = None,  # Callback khi sự kiện kéo thả chuột ra khỏi component diễn ra.
        rippleDuration: int = 600,  # Callback khi sự kiện kéo thả chuột ra khỏi component diễn ra.
        rippleTimeout: int = None,  # Callback khi sự kiện kéo thả chuột ra khỏi component diễn ra.
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        if id is not None:
            self.setObjectName(id)
        else:
            self.setObjectName(str(uuid.uuid4()))

        # gán giá trị truyền vào cho các thuộc tính của ButtonBase
        self._value = value
        
        self._action = action
        self._centerRipple = centerRipple
        self._children = children
        self._component = component
        self._classes = classes
        self._disabled = disabled
        self._disableRipple = disableRipple
        self._disableTouchRipple = disableTouchRipple
        self._focusRipple = focusRipple
        self._focusVisibleClassName = focusVisibleClassName
        self._LinkComponent = LinkComponent
        self._onFocusVisible = onFocusVisible
        self._sx = sx
        self._tabIndex = tabIndex
        self._TouchRippleProps = TouchRippleProps
        self._touchRippleRef = touchRippleRef
        self._tooltip = tooltip
        self._tooltipPlacement = tooltipPlacement
        self._rippleDuration = rippleDuration
        self._rippleTimeout = rippleTimeout

        # Gán các callback cho sự kiện tương tác
        self._onBlur = onBlur
        self._onClick = onClick
        self._onMouseEnter = onMouseEnter
        self._onContextMenu = onContextMenu
        self._onFocus = onFocus
        self._onKeyDown = onKeyDown
        self._onKeyUp = onKeyUp
        self._onMouseDown = onMouseDown
        self._onMouseLeave = onMouseLeave
        self._onMouseUp = onMouseUp
        self._onDragLeave = onDragLeave


        # ripple config
        self._color = "#333333"

        self._radius = 0
        self._max_radius = 100
        self._opacity = 1.0
        self._center = QPoint(0, 0)

        # ripple effect config
        self.ripple_effect = RippleEffect(self)
        self.animation = QPropertyAnimation(self.ripple_effect, b"radius")
        self.opacity_animation = QPropertyAnimation(self.ripple_effect, b"opacity")
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.opacity_animation.setEasingCurve(QEasingCurve.OutQuad)

        if self._onClick:
            self.clicked.connect(self._onClick)
        if self._onMouseEnter:
            self.mouseEnterSignal.connect(self._onMouseEnter)
        if self._onMouseLeave:
            self.mouseLeaverSignal.connect(self._onMouseLeave)

        self._connect_signals_to_slots()

        PyWidgetBase._installTooltipFilter(self)

    def _connect_signals_to_slots(self):
        if isinstance(self._disabled, State):
            self._disabled.valueChanged.connect(self._set_enabled)
            self.setEnabled(not self._disabled.value)
        elif isinstance(self._disabled, bool):
            self.setEnabled(not self._disabled)

    def _set_enabled(self, state):
        self.setEnabled(not state)


    def focusInEvent(self, event):
        if self._onFocus:
            self._onFocus(event)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        if self._onBlur:
            self._onBlur(event)
        super().focusOutEvent(event)

    def contextMenuEvent(self, event):
        if self._onContextMenu:
            self._onContextMenu(event)
        super().contextMenuEvent(event)

    def enterEvent(self, event):
        if self._onMouseEnter:
            self.mouseEnterSignal.emit()
        if self._tooltip:
            self.move_tooltip()
            self.tooltipLabel.show()

        return super().enterEvent(event)

    def leaveEvent(self, event):
        if self._onMouseLeave:
            self.mouseLeaverSignal.emit()
        if self._tooltip:
            QTimer.singleShot(500, self._check_tooltip_under_currsor)
        super().leaveEvent(event)

    def _check_tooltip_under_currsor(self):
        if not self.tooltipLabel.underMouse():
            self.tooltipLabel.hide()

    # MOVE TOOLTIP
    # ///////////////////////////////////////////////////////////////
    def move_tooltip(self):
        _margin = 10
        if self._tooltipPlacement == "top-start":
            tooltip_pos_x = 0
            tooltip_pos_y = -(self.tooltipLabel.height() + _margin)
        elif self._tooltipPlacement == "top":
            tooltip_pos_x = int((self.width() - self.tooltipLabel.width())/2)
            tooltip_pos_y = -(self.tooltipLabel.height() + _margin)
        elif self._tooltipPlacement == "top-end":
            tooltip_pos_x = self.width() -self.tooltipLabel.width()
            tooltip_pos_y = -(self.tooltipLabel.height() + _margin)
        elif self._tooltipPlacement == "bottom-start":
            tooltip_pos_x = 0
            tooltip_pos_y = (self.height() + _margin)
        elif self._tooltipPlacement == "bottom":
            tooltip_pos_x = int((self.width() - self.tooltipLabel.width())/2)
            tooltip_pos_y = (self.height() + _margin)
        elif self._tooltipPlacement == "bottom-end":
            tooltip_pos_x = self.width() -self.tooltipLabel.width()
            tooltip_pos_y = (self.height() + _margin)
        elif self._tooltipPlacement == "left-start":
            tooltip_pos_x = -self.tooltipLabel.width() - _margin
            tooltip_pos_y = 0
        elif self._tooltipPlacement == "left":
            tooltip_pos_x = -self.tooltipLabel.width() - _margin
            tooltip_pos_y = self.height()/2 - self.tooltipLabel.height()/2
        elif self._tooltipPlacement == "left-end":
            tooltip_pos_x = -self.tooltipLabel.width() - _margin
            tooltip_pos_y = self.height() - self.tooltipLabel.height()
        elif self._tooltipPlacement == "right-start":
            tooltip_pos_x = self.width() + _margin
            tooltip_pos_y = 0
        elif self._tooltipPlacement == "right":
            tooltip_pos_x = self.width() + _margin
            tooltip_pos_y = self.height()/2 - self.tooltipLabel.height()/2
        elif self._tooltipPlacement == "right-end":
            tooltip_pos_x = self.width() + _margin
            tooltip_pos_y = self.height() - self.tooltipLabel.height()
        else: # bottom
            raise TypeError("Type of tooltipPlacement in ['top-start','top','top-end','bottom-start','bottom','bottom-end','left-start','left','left-end','right-start','right','right-end']")



        print('tooltip_pos_x___', tooltip_pos_x)
        gp = self.mapToGlobal(QPoint(tooltip_pos_x, tooltip_pos_y))
        self.tooltipLabel.move(gp)

    def mousePressEvent(self, event):
        """
        Override mousePressEvent to handle ripple effect and trigger the ripple animation.
        """
        if not self._disableRipple:
            self.ripple_effect.setCenter(event.pos())
            self.ripple_effect._max_radius = max(self.width(), self.height())

            if self._rippleTimeout:
                QTimer.singleShot(self._rippleTimeout, self._run_ripple_animation)
            else:
                self._run_ripple_animation()

            # self.animation.setStartValue(0)
            # self.animation.setEndValue(self.ripple_effect._max_radius)
            # self.animation.setDuration(self._rippleDuration)

            # self.opacity_animation.setStartValue(1.0)
            # self.opacity_animation.setEndValue(0.0)
            # self.opacity_animation.setDuration(self._rippleDuration)

            # self.animation.start()
            # self.opacity_animation.start()

        if self._onMouseDown:
            self._onMouseDown(event)

        super().mousePressEvent(event)

    def _run_ripple_animation(self):
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.ripple_effect._max_radius)
        self.animation.setDuration(self._rippleDuration)

        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.0)
        self.opacity_animation.setDuration(self._rippleDuration)

        self.animation.start()
        self.opacity_animation.start()

    def mouseReleaseEvent(self, event):
        if self._onMouseUp:
            self._onMouseUp(event)
        if event.button() == Qt.LeftButton:
            # self._onClick([event, self._value])
            # self._onClick([event, self._value])
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if self._onKeyDown:
            self._onKeyDown(event)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if self._onKeyUp:
            self._onKeyUp(event)
        super().keyReleaseEvent(event)

    def dragLeaveEvent(self, event):
        if self._onDragLeave:
            self._onDragLeave(event)
        super().dragLeaveEvent(event)


    def paintEvent(self, event):
        if not hasattr(self, "theme") or not self.theme:
            self.theme = useTheme()
        """Handle the painting of the button, including ripple effect if enabled."""
        if not self._disableRipple and self.ripple_effect.opacity > 0:
            try:
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
                painter.setPen(Qt.NoPen)

                clip_path = QPainterPath()
                if self._component == "Radio" or self._component == "Checkbox" or self._component == "IconButton":
                    clip_path.addRoundedRect(0, 0, self.width(), self.height(), self.width()/2, self.height()/2)
                else:
                    clip_path.addRoundedRect(0, 0, self.width(), self.height(), 4, 4)

                painter.setClipPath(clip_path)

                color = hex_string_to_qcolor(get_palette_text_color(self.theme.palette, self._color))
                painter.setBrush(QBrush(color))
                center = self.ripple_effect.center
                painter.drawEllipse(center, self.ripple_effect.radius, self.ripple_effect.radius)

                # Kết thúc vẽ
                painter.end()
            except Exception as e:
                print('button_base -> eventFilter', str(e))
        super().paintEvent(event)

    # Hàm này cho phép bạn đăng ký một callback onClick
    def set_on_click(self, callback):
        self._onClick = callback

    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.MouseButtonPress:
    #         # if not self.timer.isActive():
    #         #   self.timer.start()
    #         if event.button() == Qt.LeftButton:
    #             if self._onClick:
    #                 # self._onClick(self)
    #                 pass

    #     return super().eventFilter(obj, event)


    #   elif event.type() == QEvent.MouseButtonDblClick:
    #     self.is_double = True
    #     return True

    #   if event.type() == QEvent.MouseMove:
    #     index = event.pos()
    #   elif event.type() == QEvent.Leave:
    #     index = QModelIndex()
    #   elif event.type() == QEvent.MouseButtonRelease:
    #     index = QModelIndex()