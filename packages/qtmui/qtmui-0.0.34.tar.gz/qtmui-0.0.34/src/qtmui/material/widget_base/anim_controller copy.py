from typing import Optional, Dict, List, Callable, Union

from PySide6.QtCore import QObject, QPoint, QSize, QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation, QTimer, Qt, QEasingCurve
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from .anim_effect import AnimEffect
from .anim_easing_curve_type import chooseEasing

class AnimationController(QObject):
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
        
        self.effect = AnimEffect(src=getattr(self.widget, "src"), variants=variants)
        
        self.widget.setGraphicsEffect(self.effect)

        self._played = False

    def apply_initial(self, variants=None):
        """Should be called after layout assigned positions (i.e. after show)."""
        initial = self.variants.get("initial", {}) or {}
        
        self.base_pos = QPoint(self.widget.pos())
        # self.base_pos = QPoint(0, 0)
        
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
        loop_bg_pan = anim_def.get("loop", True)
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
        if anim_def.get("scaleX") is not None or anim_def.get("scaleY") is not None:
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
        if "scale" in anim_def and isinstance(anim_def.get("scale"), float):
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
        elif "scale" in anim_def and isinstance(anim_def.get("scale"), list):
            anim_scl = QPropertyAnimation(self.effect, b"scale")
            anim_scl.setStartValue(float(anim_def["scale"][0]))
            anim_scl.setEndValue(float(anim_def["scale"][1]))
            anim_scl.setDuration(duration_ms)
            anim_scl.setEasingCurve(easing)
            animations.append(anim_scl)
            
            
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
            
        # opacity
        if "gradient" in anim_def:
            gradient_anim = QPropertyAnimation(self.effect, b"bgProgress", parent=self.effect)
            gradient_anim.setStartValue(0.0)
            gradient_anim.setEndValue(1.0)
            gradient_anim.setDuration(duration_ms)
            if loop_bg_pan:
                gradient_anim.setLoopCount(-1)
            gradient_anim.setEasingCurve(easing)
            animations.append(gradient_anim)
            
        if not animations:
            return

        # group them and play after delay
        self.anim_group = QParallelAnimationGroup(self.widget)
        for a in animations:
            self.anim_group.addAnimation(a)

        if delay_ms <= 0:
            self.anim_group.start(QAbstractAnimation.DeleteWhenStopped)
        else:
            # self.anim_group.start()
            QTimer.singleShot(delay_ms, lambda: self.anim_group.start(QAbstractAnimation.DeleteWhenStopped))
            # QTimer.singleShot(delay_ms, lambda: self.anim_group.start())

    def onDestroy(self):
        print('desktroyyyyyyyyyyyyyyyyyyyyyyyyyyy')
