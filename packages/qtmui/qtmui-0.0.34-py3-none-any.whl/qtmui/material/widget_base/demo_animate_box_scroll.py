#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Animate Box demo
- Box là QFrame có thể chứa children (Box hoặc widget)
- Mỗi Box có BoxAnimationController để apply initial và play animate
- Container Box (Box with children) sẽ đọc transition.delayChildren và staggerChildren
  và điều phối play() cho các child theo thứ tự (đặt trong showEvent)
"""

import sys
from typing import Optional, Dict, List, Callable, Union
from math import cos, pi
from PySide6 import QtAsyncio

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from qtmui.material.scroll_bar import Scrollbar


# src/components/animate/get_variant.py
from typing import Dict, Any

# Import tất cả variants đã chuyển đổi
from src.components.animate.variants import (
    varFade,
    varZoom,
    varFlip,
    varSlide,
    varScale,
    varBounce,
    varRotate,
    varBgPan,
    varBgColor,
    varBgKenburns,
)

# ----------------------------------------------------------------------
# Shortcut dictionary – giống hệt file getVariant() trong MUI
# ----------------------------------------------------------------------
VARIANT_MAP: Dict[str, Dict[str, Any]] = {
    # Slide
    "slideInUp": varSlide()["inUp"],
    "slideInDown": varSlide()["inDown"],
    "slideInLeft": varSlide()["inLeft"],
    "slideInRight": varSlide()["inRight"],
    "slideOutUp": varSlide()["outUp"],
    "slideOutDown": varSlide()["outDown"],
    "slideOutLeft": varSlide()["outLeft"],
    "slideOutRight": varSlide()["outRight"],

    # Fade
    "fadeIn": varFade()["in"],
    "fadeInUp": varFade()["inUp"],
    "fadeInDown": varFade()["inDown"],
    "fadeInLeft": varFade()["inLeft"],
    "fadeInRight": varFade()["inRight"],
    "fadeOut": varFade()["out"],
    "fadeOutUp": varFade()["outUp"],
    "fadeOutDown": varFade()["outDown"],
    "fadeOutLeft": varFade()["outLeft"],
    "fadeOutRight": varFade()["outRight"],

    # Zoom
    "zoomIn": varZoom({"distance": 0})["in"],
    "zoomInUp": varZoom({"distance": 80})["inUp"],
    "zoomInDown": varZoom({"distance": 80})["inDown"],
    "zoomInLeft": varZoom({"distance": 240})["inLeft"],
    "zoomInRight": varZoom({"distance": 240})["inRight"],
    "zoomOut": varZoom()["out"],
    "zoomOutLeft": varZoom()["outLeft"],
    "zoomOutRight": varZoom()["outRight"],
    "zoomOutUp": varZoom()["outUp"],
    "zoomOutDown": varZoom()["outDown"],

    # Bounce
    "bounceIn": varBounce()["in"],
    "bounceInUp": varBounce()["inUp"],
    "bounceInDown": varBounce()["inDown"],
    "bounceInLeft": varBounce()["inLeft"],
    "bounceInRight": varBounce()["inRight"],
    "bounceOut": varBounce()["out"],
    "bounceOutUp": varBounce()["outUp"],
    "bounceOutDown": varBounce()["outDown"],
    "bounceOutLeft": varBounce()["outLeft"],
    "bounceOutRight": varBounce()["outRight"],

    # Flip
    "flipInX": varFlip()["inX"],
    "flipInY": varFlip()["inY"],
    "flipOutX": varFlip()["outX"],
    "flipOutY": varFlip()["outY"],

    # Scale
    "scaleInX": varScale()["inX"],
    "scaleInY": varScale()["inY"],
    "scaleOutX": varScale()["outX"],
    "scaleOutY": varScale()["outY"],

    # Rotate
    "rotateIn": varRotate()["in"],
    "rotateOut": varRotate()["out"],

    # Background
    "kenburnsTop": varBgKenburns()["top"],
    "kenburnsBottom": varBgKenburns()["bottom"],
    "kenburnsLeft": varBgKenburns()["left"],
    "kenburnsRight": varBgKenburns()["right"],

    "panTop": varBgPan()["top"],
    "panBottom": varBgPan()["bottom"],
    "panLeft": varBgPan()["left"],
    "panRight": varBgPan()["right"],

    "color2x": varBgColor(),
    "color3x": varBgColor({"colors": ['#19dcea', '#b22cff', '#ea2222']}),
    "color4x": varBgColor({"colors": ['#19dcea', '#b22cff', '#ea2222', '#f5be10']}),
    "color5x": varBgColor({"colors": ['#19dcea', '#b22cff', '#ea2222', '#f5be10', '#3bd80d']}),
}


# ----------------------------------------------------------------------
# Hàm tiện ích – giống hệt getVariant(variant = 'slideInUp')
# ----------------------------------------------------------------------
def getVariant(variant: str = "slideInUp") -> Dict[str, Any]:
    """
    Dùng chỉ bằng tên chuỗi – cực tiện!

    Ví dụ:
        getVariant("zoomInUp")
        getVariant("bounceIn")
        getVariant("kenburnsTop")
    """
    return VARIANT_MAP.get(variant, varSlide()["inUp"])  # fallback về slideInUp nếu không tìm thấy



def chooseEasing(ease_data):
    """Choose QEasingCurve from ease_data. If ease_data is a list (bezier),
    fallback to OutCubic for now. If it's a string, attempt to map.
    """
    # if given as list/tuple -> fallback
    if isinstance(ease_data, (list, tuple)):
        return QEasingCurve(QEasingCurve.Type.OutCubic)
    # if string -> try map common ones
    if isinstance(ease_data, str):
        # minimal mapping, extend if needed
        easing_map = {
            'linear': QEasingCurve.Type.Linear,
            'inQuad': QEasingCurve.Type.InQuad,
            'outQuad': QEasingCurve.Type.OutQuad,
            'inOutQuad': QEasingCurve.Type.InOutQuad,
            'outInQuad': QEasingCurve.Type.OutInQuad,
            'inCubic': QEasingCurve.Type.InCubic,
            'outCubic': QEasingCurve.Type.OutCubic,
            'inOutCubic': QEasingCurve.Type.InOutCubic,
            'outInCubic': QEasingCurve.Type.OutInCubic,
            'inQuart': QEasingCurve.Type.InQuart,
            'outQuart': QEasingCurve.Type.OutQuart,
            'inOutQuart': QEasingCurve.Type.InOutQuart,
            'outInQuart': QEasingCurve.Type.OutInQuart,
            'inQuint': QEasingCurve.Type.InQuint,
            'outQuint': QEasingCurve.Type.OutQuint,
            'inOutQuint': QEasingCurve.Type.InOutQuint,
            'outInQuint': QEasingCurve.Type.OutInQuint,
            'inSine': QEasingCurve.Type.InSine,
            'outSine': QEasingCurve.Type.OutSine,
            'inOutSine': QEasingCurve.Type.InOutSine,
            'outInSine': QEasingCurve.Type.OutInSine,
            'inExpo': QEasingCurve.Type.InExpo,
            'outExpo': QEasingCurve.Type.OutExpo,
            'inOutExpo': QEasingCurve.Type.InOutExpo,
            'outInExpo': QEasingCurve.Type.OutInExpo,
            'inCirc': QEasingCurve.Type.InCirc,
            'outCirc': QEasingCurve.Type.OutCirc,
            'inOutCirc': QEasingCurve.Type.InOutCirc,
            'outInCirc': QEasingCurve.Type.OutInCirc,
            'inElastic': QEasingCurve.Type.InElastic,
            'outElastic': QEasingCurve.Type.OutElastic,
            'inOutElastic': QEasingCurve.Type.InOutElastic,
            'outInElastic': QEasingCurve.Type.OutInElastic,
            'inBack': QEasingCurve.Type.InBack,
            'outBack': QEasingCurve.Type.OutBack,
            'inOutBack': QEasingCurve.Type.InOutBack,
            'outInBack': QEasingCurve.Type.OutInBack,
            'inBounce': QEasingCurve.Type.InBounce,
            'outBounce': QEasingCurve.Type.OutBounce,
            'inOutBounce': QEasingCurve.Type.InOutBounce,
            'outInBounce': QEasingCurve.Type.OutInBounce,
            # fallback cho các easing khác
            'sineCurve': QEasingCurve.Type.SineCurve,
            'cosineCurve': QEasingCurve.Type.CosineCurve,
        }
        t = easing_map.get(ease_data, QEasingCurve.Type.OutCubic)
        return QEasingCurve(t)
    # default
    return QEasingCurve(QEasingCurve.Type.OutCubic)


class AnimEffect(QGraphicsEffect):
    """Flip theo trục X, mô phỏng bằng scaleY = cos(angle)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 1.0  # 0.0 → 1.0
        self._angle = 0.0  # độ, -360 → 0 hoặc 0 → 360
        self._offsetX = 0.0
        self._offsetY = 0.0
        self._rotationX = 0.0  # độ, -180 → 0 hoặc 0 → 180
        self._rotationY = 0.0  # độ, -180 → 0 hoặc 0 → 180
        self._scaleX = 1.0
        self._scaleY = 1.0

    def getOffsetX(self):
        return self._offsetX

    def setOffsetX(self, val):
        self._offsetX = val
        self.update()

    offsetX = Property(float, getOffsetX, setOffsetX)
    
    def getOffsetY(self):
        return self._offsetY

    def setOffsetY(self, val):
        self._offsetY = val
        self.update()

    offsetY = Property(float, getOffsetY, setOffsetY)
    
    def getAngle(self):
        return self._angle

    def setAngle(self, val):
        self._angle = val
        self.update()

    angle = Property(float, getAngle, setAngle)
    
    def getRotationX(self):
        return self._rotationX

    def setRotationX(self, val):
        self._rotationX = val
        self.update()

    rotationX = Property(float, getRotationX, setRotationX)
    
    def getRotationY(self):
        return self._rotationY

    def setRotationY(self, val):
        self._rotationY = val
        self.update()

    rotationY = Property(float, getRotationY, setRotationY)
    
    def getScaleX(self):
        return self._scaleX

    def setScaleX(self, val):
        self._scaleX = val
        self.update()

    scaleX = Property(float, getScaleX, setScaleX)
    
    def getScaleY(self):
        return self._scaleY

    def setScaleY(self, val):
        self._scaleY = val
        self.update()

    scaleY = Property(float, getScaleY, setScaleY)
    
    def getOpacity(self):
        return self._opacity

    def setOpacity(self, val):
        self._opacity = val
        self.update()

    opacity = Property(float, getOpacity, setOpacity)

    def draw(self, painter: QPainter):
        pixmap = self.sourcePixmap()
        if pixmap.isNull():
            return

        painter.save()
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform
        )

        w, h = pixmap.width(), pixmap.height()
        cx, cy = w / 2, h / 2

        ################### Flip Scale X/Y ###################
        # Dịch tâm
        painter.translate(cx, cy)
        # Góc radian
        radX = self._rotationX * pi / 180.0
        radY = self._rotationY * pi / 180.0
        scale_x = cos(radX)
        scale_y = cos(radY)
        # Giữ dấu để flip
        # painter.scale(scale_y, scale_x)
        if self._rotationX == 0.0 and self._rotationY == 0.0:
            painter.scale(self._scaleX, self._scaleY)
        else:
            painter.scale(scale_y, scale_x)
        
        # Dịch tâm về lại
        painter.translate(-cx, -cy)
        ################### end Flip Scale X/Y ###################
        
        painter.setOpacity(self._opacity)
        
        # rotate
        if self._angle != 0.0:
            offset = QPoint()
            pixmap = self.sourcePixmap(Qt.DeviceCoordinates)
            
            cx = pixmap.width() / 2
            cy = pixmap.height() / 2

            painter.translate(QPointF(offset) + QPointF(cx, cy))
            painter.rotate(self._angle)
            painter.translate(-cx, -cy)

            painter.drawPixmap(0, 0, pixmap)
        
        # Vẽ pixmap
        if not self._angle:
            self.drawSource(painter)
        painter.restore()





# ---------------------------
# Controller for single widget
# ---------------------------
class BoxAnimationController(QObject):
    def __init__(self, widget: QWidget, variants: Dict, parent=None):
        super().__init__(parent)
        
        self.widget = widget
        self.variants = variants or {}
        self.anim_group = None

        # Lưu trạng thái gốc (sẽ được set trong apply_initial)
        self.base_pos = None      # QPoint
        self.base_size = None     # QSize
        
        # scale state
        self._scaleX = 1.0
        self._scaleY = 1.0
        
        self.effect = AnimEffect()
        
        self.widget.setGraphicsEffect(self.effect)

        # rotation state

        self._played = False

    def apply_initial(self):
        """Should be called after layout assigned positions (i.e. after show)."""
        initial = self.variants.get("initial", {}) or {}

        self.base_pos = QPoint(self.widget.pos())
        
        self.base_size = self.widget.size()

        # === Rotation X/Y ===
        if "rotationX" in initial:
            self._rotationX = float(initial.get("rotationX", 0.0))
            self.effect.setRotationX(self._rotationX)
                        
        if "rotationY" in initial:
            self._rotationY = float(initial.get("rotationY", 0.0))
            self.effect.setRotationY(self._rotationY)
            
        if "rotation" in initial:
            self._angle = float(initial.get("rotation", 0.0))
            self.effect.setAngle(self._angle)


        # apply initial Y offset if provided (move widget visually from base)
        if "y" in initial:
            try:
                dy = int(initial["y"])
            except Exception:
                dy = 0
            # move widget to base_pos + dy
            self.widget.move(self.base_pos.x(), self.base_pos.y() + dy)
            # print("Applying initial y offset:", dy)
            
        # apply initial Y offset if provided (move widget visually from base)
        if "x" in initial:
            try:
                dx = int(initial["x"])
            except Exception:
                dx = 0
            # move widget to base_pos + dx
            # print("Applying initial x offset:", dx)
            self.widget.move(self.base_pos.x() + dx, self.base_pos.y())


        # === Scale (giả lập bằng resize) ===
        if initial.get("scale") is not None  or initial.get("scaleX") is not None or initial.get("scaleY") is not None:
            scale_x = float(initial.get("scaleX", initial.get("scale", 1.0)))
            scale_y = float(initial.get("scaleY", initial.get("scale", 1.0)))

            if abs(scale_x - 1.0) > 0.01 or abs(scale_y - 1.0) > 0.01:
                new_width = max(1, int(self.base_size.width() * scale_x))
                new_height = max(1, int(self.base_size.height() * scale_y))
                self.widget.resize(new_width, new_height)
                
        # === Scale X/Y ===
        if "scaleX" in initial:
            self._scaleX = float(initial.get("scaleX", 1.0))
            self.effect.setScaleX(self._scaleX)
                        
        if "scaleY" in initial:
            self._scaleY = float(initial.get("scaleY", 1.0))
            self.effect.setScaleY(self._scaleY)
            
        if "scale" in initial:
            self.effect.setScaleX(float(initial.get("scale", 1.0)))
            self.effect.setScaleY(float(initial.get("scale", 1.0)))

                
        if initial.get("opacity") is not None:
            self._opacity = float(initial.get("opacity", 1.0))
            self.effect.setOpacity(self._opacity)

    def play(self, delay_ms: int = 0):
        """Start animate from current widget pos -> base_pos + animate.y (usually base_pos)"""
        if self._played:
            return
        
        self._played = True

        initial = self.variants.get("initial", {}) or {}
        anim_def = self.variants.get("animate", {}) or {}
        if not anim_def:
            return
        
        # Ensure base_pos set (should be set in apply_initial). If not, compute now.
        if self.base_pos is None:
            self.base_pos = QPoint(self.widget.pos())

        transition = anim_def.get("transition", {}) or {}
        duration_sec = transition.get("duration", 0.6)
        # allow duration either seconds (float) or ms (int)
        try:
            duration_ms = int(duration_sec * 1000) if duration_sec < 1000 else int(duration_sec)
        except Exception:
            duration_ms = 600

        ease_data = transition.get("ease", None)

        easing = chooseEasing(ease_data)

        # Build animations
        animations = []

        # position (Y)
        if "y" in anim_def:
            # start is current widget position (probably base_pos + initial_y)
            start_pos = QPoint(self.widget.pos())
            # end is base_pos + animate['y'] (usually animate['y'] == 0)
            try:
                anim_y = int(anim_def.get("y", 0))
            except Exception:
                anim_y = 0
            end_pos = QPoint(self.base_pos.x(), self.base_pos.y() + anim_y)

            pos_anim = QPropertyAnimation(self.widget, b"pos")
            pos_anim.setStartValue(start_pos)
            pos_anim.setEndValue(end_pos)
            pos_anim.setDuration(duration_ms)
            pos_anim.setEasingCurve(easing)
            animations.append(pos_anim)
            
        # position (X)
        if "x" in anim_def:
            # start is current widget position (probably base_pos + initial_x)
            start_pos = QPoint(self.widget.pos())
            # end is base_pos + animate['x'] (usually animate['x'] == 0)
            try:
                anim_x = int(anim_def.get("x", 0))
            except Exception:
                anim_x = 0
            end_pos = QPoint(self.base_pos.x() + anim_x, self.base_pos.y())

            pos_anim = QPropertyAnimation(self.widget, b"pos")
            pos_anim.setStartValue(start_pos)
            pos_anim.setEndValue(end_pos)
            pos_anim.setDuration(duration_ms)
            pos_anim.setEasingCurve(easing)
            animations.append(pos_anim)



        # === Scale (giả lập bằng resize + move để giữ tâm) ===
        if anim_def.get("scale") is not None or anim_def.get("scaleX") is not None or anim_def.get("scaleY") is not None:
            target_scale_x = float(anim_def.get("scaleX", anim_def.get("scale", 1.0)))
            target_scale_y = float(anim_def.get("scaleY", anim_def.get("scale", 1.0)))

            current_w = self.widget.width()
            current_h = self.widget.height()
            target_w = max(1, int(self.base_size.width() * target_scale_x))
            target_h = max(1, int(self.base_size.height() * target_scale_y))

            if current_w != target_w or current_h != target_h:
                # Animation resize
                size_anim = QPropertyAnimation(self.widget, b"size")
                # size_anim.setStartValue(QSize(0,0))
                size_anim.setStartValue(self.widget.size())
                size_anim.setEndValue(QSize(target_w, target_h))
                size_anim.setDuration(duration_ms)
                size_anim.setEasingCurve(easing)
                animations.append(size_anim)

                # # Giữ tâm khi scale → tính toán vị trí mới
                # if anim_def.get("x") is None and anim_def.get("y") is None:
                #     print("Adding center move for scale")
                #     def update_center(value):
                #         progress = size_anim.currentValue().width() / target_w if target_w > 0 else 1.0
                #         new_w = int(self.base_size.width() * target_scale_x * progress)
                #         new_h = int(self.base_size.height() * target_scale_y * progress)
                #         center_x = self.base_pos.x() + self.base_size.width() // 2
                #         center_y = self.base_pos.y() + self.base_size.height() // 2
                #         new_x = center_x - new_w // 2
                #         new_y = center_y - new_h // 2
                #         self.widget.move(new_x, new_y)

                #     size_anim.valueChanged.connect(update_center)

        # scale
        if "scale" in anim_def:
            anim_sclX = QPropertyAnimation(self.effect, b"scaleX")
            anim_sclX.setStartValue(float(initial.get("scale", 1.0)))
            anim_sclX.setEndValue(float(anim_def.get("scale", 1.0)))
            anim_sclX.setDuration(duration_ms)
            anim_sclX.setEasingCurve(easing)
            animations.append(anim_sclX)
            
            anim_sclY = QPropertyAnimation(self.effect, b"scaleY")
            anim_sclY.setStartValue(float(initial.get("scale", 1.0)))
            anim_sclY.setEndValue(float(anim_def.get("scale", 1.0)))
            anim_sclY.setDuration(duration_ms)
            anim_sclY.setEasingCurve(easing)
            animations.append(anim_sclY)
            
        if "scaleX" in anim_def:
            anim_sclX = QPropertyAnimation(self.effect, b"scaleX")
            anim_sclX.setStartValue(float(initial.get("scaleX", self._scaleX)))
            anim_sclX.setEndValue(float(anim_def.get("scaleX", self._scaleX)))
            anim_sclX.setDuration(duration_ms)
            anim_sclX.setEasingCurve(easing)
            animations.append(anim_sclX)
            
        if "scaleY" in anim_def:
            anim_sclY = QPropertyAnimation(self.effect, b"scaleY")
            anim_sclY.setStartValue(float(initial.get("scaleY", self._scaleY)))
            anim_sclY.setEndValue(float(anim_def.get("scaleY", self._scaleY)))
            anim_sclY.setDuration(duration_ms)
            anim_sclY.setEasingCurve(easing)
            animations.append(anim_sclY)
            

        # rotationX
        if "rotationX" in anim_def:
            anim_rotX = QPropertyAnimation(self.effect, b"rotationX")
            anim_rotX.setStartValue(float(initial.get("rotationX", self._rotationX)))
            anim_rotX.setEndValue(float(anim_def.get("rotationX", self._rotationX)))
            anim_rotX.setDuration(duration_ms)
            anim_rotX.setEasingCurve(easing)
            animations.append(anim_rotX)
            

        # rotationY
        if "rotationY" in anim_def:
            anim_rotY = QPropertyAnimation(self.effect, b"rotationY")
            anim_rotY.setStartValue(float(initial.get("rotationY", self._rotationY)))
            anim_rotY.setEndValue(float(anim_def.get("rotationY", self._rotationY)))
            anim_rotY.setDuration(duration_ms)
            anim_rotY.setEasingCurve(easing)
            animations.append(anim_rotY)
            
        # rotation
        if "rotation" in anim_def:
            anim_rotate = QPropertyAnimation(self.effect, b"angle")
            anim_rotate.setStartValue(float(initial.get("rotation", 0.0)))
            anim_rotate.setEndValue(float(anim_def.get("rotation", 0.0)))
            anim_rotate.setDuration(duration_ms)
            anim_rotate.setEasingCurve(easing)
            animations.append(anim_rotate)
            
        # opacity
        if "opacity" in anim_def:
            op_anim = QPropertyAnimation(self.effect, b"opacity")
            op_anim.setStartValue(float(initial.get("opacity", 1.0)))
            op_anim.setEndValue(float(anim_def.get("opacity", 1.0)))
            op_anim.setDuration(duration_ms)
            op_anim.setEasingCurve(easing)
            animations.append(op_anim)
            
        if not animations:
            return

        # group them and play after delay
        self.anim_group = QParallelAnimationGroup(self.widget)
        for a in animations:
            self.anim_group.addAnimation(a)

        if delay_ms <= 0:
            self.anim_group.start(QAbstractAnimation.DeleteWhenStopped)
        else:
            QTimer.singleShot(delay_ms, lambda: self.anim_group.start(QAbstractAnimation.DeleteWhenStopped))



# ---------------------------
# Box widget
# ---------------------------
class Box(QFrame):
    def __init__(
        self,
        children: Optional[Union[List[QWidget], Callable]] = None,
        initial="initial",
        animate="animate",
        exit="exit",
        variants=None,
        sx: str = "",
        parent=None
    ):
        super().__init__(parent)
        
        
        self.setObjectName(f"Box{id(self)}")
        self._sx = sx or ""
        self.setStyleSheet(f"#{self.objectName()} {{{self._sx}}}")



        # layout to hold children (if any)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(6)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        

        


        self.variants = variants or {}
        self.children_source = children
        self.children_widgets: List[QWidget] = []
        self.child_controllers: List[BoxAnimationController] = []


        # create children if provided (callable for lazy children)
        if callable(self.children_source):
            content = self.children_source()
        else:
            content = self.children_source or []

        for c in content:
            # c might be a Box or plain QWidget
            self.layout().addWidget(c)
            self.children_widgets.append(c)
            child_variants = getattr(c, "variants", {}) or {}
            child_ctrl = BoxAnimationController(c, child_variants)
            self.child_controllers.append(child_ctrl)


        # mark whether we've scheduled children animations already
        self._children_scheduled = False
        self._connected = False

    def find_scroll_area(self) -> Optional[QScrollArea]:
        p = self.parentWidget()
        while p:
            if isinstance(p, QScrollArea):  # Hoặc isinstance(p, Scrollbar) nếu Scrollbar kế thừa QScrollArea
                return p
            p = p.parentWidget()
        return None

    def showEvent(self, event):
        super().showEvent(event)
        # We must schedule apply_initial and play AFTER layout has assigned positions.
        # Use singleShot(0) to run after the event loop processes layout.
        if self.children_widgets and not self._children_scheduled:
            QTimer.singleShot(0, self._schedule_children_animation)
            self._children_scheduled = True

    def _schedule_children_animation(self):
        """Apply initial state for all children and then play them with stagger/delay from this Box variants."""
        # Áp dụng initial cho tất cả children trước
        for ctrl in self.child_controllers:
            ctrl.apply_initial()

        # Kiểm tra nếu container nằm trong QScrollArea (Scrollbar giả sử là subclass của QScrollArea)
        scroll_area = self.find_scroll_area()
        if scroll_area:
            # Kết nối signal nếu chưa
            if not self._connected:
                scroll_area.verticalScrollBar().valueChanged.connect(self._animate_visible_children)
                self._connected = True
            # Trigger initial animation cho các child visible ban đầu
            QTimer.singleShot(0, lambda: self._animate_visible_children(scroll_area.verticalScrollBar().value()))
        else:
            # Không có scroll, play tất cả với stagger như cũ
            animate_def = self.variants.get("animate", {}) or {}
            transition = animate_def.get("transition", {}) or {}
            base_delay = int(transition.get("delayChildren", 0) * 1000)
            stagger = int(transition.get("staggerChildren", 0) * 1000)
            for idx, ctrl in enumerate(self.child_controllers):
                delay_ms = base_delay + idx * stagger
                ctrl.play(delay_ms=delay_ms)

    def _animate_visible_children(self, scroll_pos: int):
        scroll_area = self.find_scroll_area()
        if not scroll_area:
            return

        viewport_h = scroll_area.viewport().height()

        visible_to_play = []
        for idx, ctrl in enumerate(self.child_controllers):
            if ctrl._played:
                continue
            child = self.children_widgets[idx]
            child_y = child.pos().y()  # Vị trí y tương đối với container
            child_h = child.height()
            # Kiểm tra nếu child nằm trong vùng visible (có overlap với viewport)
            if (child_y < scroll_pos + viewport_h) and (child_y + child_h > scroll_pos):
                visible_to_play.append((idx, ctrl))

        if not visible_to_play:
            return

        # Sắp xếp theo thứ tự index để giữ order
        visible_to_play.sort(key=lambda x: x[0])

        # Lấy transition để áp dụng stagger cho batch visible này
        animate_def = self.variants.get("animate", {}) or {}
        transition = animate_def.get("transition", {}) or {}
        stagger = transition.get("staggerChildren", 0)
        stagger_ms = int(stagger * 1000) if stagger < 100 else int(stagger)
        # Không dùng delayChildren cho các batch sau, chỉ stagger nội bộ batch
        delay_ms = 0

        for _, ctrl in visible_to_play:
            ctrl.play(delay_ms=delay_ms)
            delay_ms += stagger_ms


# ---------------------------
# Demo MainWindow
# ---------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Box Animation Container Demo")
        self.setGeometry(100, 100, 800, 600)

        container = Box(
            sx="""
                background-color: lightgrey;
                padding: 12px;
            """,
            variants={
                "animate": {
                    "transition": {
                        "staggerChildren": 0.15,
                        "delayChildren": 0.05,
                    },
                }
            },
            children=[
                # child Boxes (items) — each Box can have its own variants
                Box(
                    sx="""
                        background-color: coral;
                        min-height: 80px;
                        min-width: 480px;
                        max-width: 480px;
                    """,
                    # variants=getVariant("slideInUp"),
                    # variants=getVariant("slideInDown"),
                    variants=getVariant("slideInLeft"),
                    # variants=getVariant("slideInRight"),
                    # variants=getVariant("slideOutUp"),
                    # variants=getVariant("slideOutDown"),
                    # variants=getVariant("slideOutLeft"),
                    # variants=getVariant("slideOutRight"),
                    # variants=getVariant("fadeIn"),
                    # variants=getVariant("fadeInUp"),
                    # variants=getVariant("fadeInDown"),
                    # variants=getVariant("fadeInLeft"),
                    # variants=getVariant("fadeInRight"),
                    # variants=getVariant("fadeOut"),
                    # variants=getVariant("fadeOutUp"),
                    # variants=getVariant("fadeOutDown"),
                    # variants=getVariant("fadeOutLeft"),
                    # variants=getVariant("fadeOutRight"),
                    # variants=getVariant("zoomIn"),
                    # variants=getVariant("zoomInUp"),
                    # variants=getVariant("zoomInDown"),
                    # variants=getVariant("zoomInLeft"),
                    # variants=getVariant("zoomInRight"),
                    # variants=getVariant("zoomOut"),
                    # variants=getVariant("zoomOutUp"),
                    # variants=getVariant("zoomOutDown"),
                    # variants=getVariant("zoomOutLeft"),
                    # variants=getVariant("zoomOutRight"),
                    # variants=getVariant("bounceIn"),
                    # variants=getVariant("bounceInUp"),
                    # variants=getVariant("bounceInDown"),
                    # variants=getVariant("bounceInLeft"),
                    # variants=getVariant("bounceInRight"),
                    # variants=getVariant("bounceOut"),
                    # variants=getVariant("bounceOutUp"),
                    # variants=getVariant("bounceOutDown"),
                    # variants=getVariant("bounceOutLeft"),
                    # variants=getVariant("bounceOutRight"),
                    # variants=getVariant("flipInX"),
                    # variants=getVariant("flipInY"),
                    # variants=getVariant("flipOutX"),
                    # variants=getVariant("flipOutY"),
                    # variants=getVariant("scaleInX"),
                    # variants=getVariant("scaleInY"),
                    # variants=getVariant("scaleOutX"),
                    # variants=getVariant("scaleOutY"),
                    # variants=getVariant("rotateIn"),
                    # variants=getVariant("rotateOut"),
                )
                for _ in range(50)
            ]
        )

        self.setCentralWidget(Scrollbar(children=[container]))
        # self.setCentralWidget(Scrollbar(children=[QPushButton('ooooooooooooo')]))


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # sys.exit(app.exec())
    QtAsyncio.run(handle_sigint=True)
    