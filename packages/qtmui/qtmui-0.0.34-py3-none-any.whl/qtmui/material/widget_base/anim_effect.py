from math import cos, pi

from PySide6.QtWidgets import QGraphicsEffect
from PySide6.QtCore import Property, QPointF, QPoint, Qt, QRectF, QTimer
from PySide6.QtGui import (
    QPainter, QPixmap, QLinearGradient, QColor, QBrush, QGradient, QPen,
    QPainterPath,
    QConicalGradient,
)

from qtmui.material.styles import useTheme

from .anim_shadow import ShadowEffect

class AnimEffect(QGraphicsEffect, ShadowEffect):
    """Flip theo trục X, mô phỏng bằng scaleY = cos(angle)."""

    PRESET_COLORS = {
        "ocean": {
            "light": ["#2193b0", "#6dd5ed"],
            "dark": ["#141e30", "#243b55"],
        },
        "sunset": {
            "light": ["#ff512f", "#f09819"],
            "dark": ["#3a1c71", "#d76d77"],
        },
        "forest": {
            "light": ["#11998e", "#38ef7d"],
            "dark": ["#0f2027", "#203a43"],
        },
    }


    def __init__(self, widget=None, style: dict={}, src: str = None, variants: dict = None):
        super().__init__()
        
        # QGraphicsEffect.__init__(self, widget)  # ✅ chắc chắn Qt init
        # ShadowEffect.__init__(self, widget)     # ✅ init mixin
        
        self._initShadow(widget)
        
        
        self._src = src
        self.style = style
        
        if src:
            self._pixmap = QPixmap(src)
        
        self._x = 0.0
        self._y = 0.0
        self._opacity = 1.0  # 0.0 → 1.0
        self._angle = 0.0  # độ, -360 → 0 hoặc 0 → 360
        self._offsetX = 0.0
        self._offsetY = 0.0
        self._rotation = 0.0
        self._rotationX = 0.0  # độ, -180 → 0 hoặc 0 → 180
        self._rotationY = 0.0  # độ, -180 → 0 hoặc 0 → 180
        self._scaleX = 1.0
        self._scaleY = 1.0
        self._scale = 1.0
        self._borderWidth = 0.0
        self._borderRadius = 0.0
        
        self.direction = "right"
        
        self._gradient = variants.get("animate", {}).get("gradient")
        self._bgProgress = 0.0
            
        self._gradientColors = [
            QColor("#ff4545"),
            QColor("#00ff99"),
            QColor("#006aff"),
            QColor("#ff0095"),
            QColor("#ff4545"),
        ]
        
        self._gradientStartAngle = None # QConicalGradient

    # ############# background image effect ###########
    # def boundingRectFor(self, rect: QRectF) -> QRectF:
    #     b = 120
    #     return rect.adjusted(-b, -b, b, b)
    #     return rect.adjusted(0, -380, 0, 0)

    # =====================================================
    # DPR (HiDPI)
    # =====================================================


    def getX(self): 
        return self._x
    
    def setX(self, v): 
        self._x = float(v)
        self.update()
        
    x = Property(float, getX, setX)

    def getY(self): 
        return self._y
    
    def setY(self, v): 
        self._y = float(v)
        self.update()
        
    y = Property(float, getY, setY)

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
    
    def getRotation(self): 
        return self._rotation
    
    def setRotation(self, v): 
        self._rotation = float(v)
        self.update()
        
    rotation = Property(float, getRotation, setRotation)
    
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

    def getScale(self):
        return self._scale

    def setScale(self, v):
        self._scale = v
        self.update()

    scale = Property(float, getScale, setScale)
    
    def getBorderWidth(self):
        return self._borderWidth

    def setBorderWidth(self, v):
        self._borderWidth = v
        self.update()

    borderWidth = Property(float, getBorderWidth, setBorderWidth)

    
    def getBorderRadius(self):
        return self._borderRadius

    def setBorderRadius(self, v):
        self._borderRadius = v
        self.update()

    borderRadius = Property(float, getBorderRadius, setBorderRadius)
    
    def getBgProgress(self):
        return self._bgProgress

    def setBgProgress(self, v):
        self._bgProgress = v
        self.update()

    bgProgress = Property(float, getBgProgress, setBgProgress)
    

    def getGradientColors(self):
        return self._gradientColors

    def setGradientColors(self, v):
        self._gradientColors = v
        self.update()

    gradientColors = Property(float, getGradientColors, setGradientColors)

    def getGradientStartAngle(self):
        return self._gradientStartAngle

    def setGradientStartAngle(self, v):
        self._gradientStartAngle = float(v)
        self.update()

    gradientStartAngle = Property(float, getGradientStartAngle, setGradientStartAngle)

    # ---------------- Resolve colors ----------------
    def _resolve_colors(self, colors):
        if isinstance(colors, str):
            preset = self.PRESET_COLORS.get(colors)
            return preset[useTheme().palette.mode.lower()]
        return list(colors)

    # ---------------- Generate colors ----------------
    def _generate_colors(self):
        steps = self._gradient.get("steps")
        interpolate = self._gradient.get("interpolate")
        colors = self._resolve_colors(self._gradient.get("colors"))
        
        if not steps:
            return colors
        
        start = QColor(colors[0])
        end = QColor(colors[1])

        result = []

        for i in range(steps):
            t = i / (steps - 1)

            if interpolate == "hsl":
                c = QColor.fromHsl(
                    int(start.hslHue() + t * (end.hslHue() - start.hslHue())),
                    int(start.hslSaturation() + t * (end.hslSaturation() - start.hslSaturation())),
                    int(start.lightness() + t * (end.lightness() - start.lightness())),
                )
            else:
                c = QColor(
                    int(start.red() + t * (end.red() - start.red())),
                    int(start.green() + t * (end.green() - start.green())),
                    int(start.blue() + t * (end.blue() - start.blue())),
                )

            result.append(c)

        return result


    def _draw_background_gradient(self, painter: QPainter, w: int, h: int):
        """
        Vẽ background gradient + pan animation
        """
        # colors = self._gradient.get("colors", ["#ee7752", "#e73c7e", "#23a6d5", "#23d5ab"])
        colors = self._generate_colors()
        
        direction = self._gradient.get("direction", "right")
        
        grad = None
        offset = 0.0

        colors_ext = colors + [colors[0]]
        num_intervals = len(colors)

        if direction in ("top", "bottom"):
            fill_factor = 6
            fill_h = h * fill_factor
            fill_w = w
            grad = QLinearGradient(0, 0, 0, fill_h)
            for i in range(len(colors_ext)):
                grad.setColorAt(float(i) / num_intervals, QColor(colors_ext[i]))

            pos = self._bgProgress
            if direction == "top":
                pos = 1 - pos  # reverse for top (pan upwards)
            offset = -pos * fill_h
            grad.setStart(0, offset)
            grad.setFinalStop(0, offset + fill_h)

        else:  # left, right
            fill_factor = 6
            fill_w = w * fill_factor
            fill_h = h
            grad = QLinearGradient(0, 0, fill_w, 0)
            for i in range(len(colors_ext)):
                grad.setColorAt(float(i) / num_intervals, QColor(colors_ext[i]))

            pos = self._bgProgress
            if direction == "left":
                pos = 1 - pos  # reverse for left (pan leftwards)
            offset = -pos * fill_w
            grad.setStart(offset, 0)
            grad.setFinalStop(offset + fill_w, 0)

        if grad:
            grad.setSpread(QGradient.RepeatSpread)
            painter.fillRect(0, 0, w, h, grad)
            

    def draw(self, p: QPainter):
        # p = QPainter(self)
        
        pixmap = self.sourcePixmap()
        
        p.setRenderHint(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        # p.fillRect(pixmap.rect(), QColor("#111"))

        w, h = pixmap.width(), pixmap.height()

        # visibility
        if self.style.visibility == "hidden":
            return

        # Tâm canvas
        # cx, cy = w / 2, h / 2
        cx = pixmap.rect().center().x()
        cy = pixmap.rect().center().y()

        # base rect theo style.width/height
        w0 = self.style.width or 120.0
        h0 = self.style.height or 120.0

        # Combine transform: sx static + motion dynamic
        tx = self.style.translate_x + self.getX()
        ty = self.style.translate_y + self.getY()
        rot = self.style.rotate + self.getRotation()
        sx = self.style.scale_x * self.getScaleX()
        sy = self.style.scale_y * self.getScaleY()
        op = max(0.0, min(1.0, self.style.opacity * self.getOpacity()))


        # Main shape
        p.save()
        p.setOpacity(op)
        p.translate(cx + tx, cy + ty)
        p.rotate(rot)
        p.scale(sx, sy)
        p.translate(-(cx + tx), -(cy + ty))
        

        # rect = QRectF(-w0 / 2, -h0 / 2, w0, h0)

        # background
        # p.setBrush(QBrush(self.style.background_color))
        if self._gradientStartAngle is not None:
            # 1) Gradient border
            _marginLeft = self.style.margin[0]
            _marginTop = self.style.margin[0]
            _marginRight = self.style.margin[0]
            _marginBottom = self.style.margin[0]
            bgRect = QRectF(0 + _marginLeft, 0 + _marginTop, w0 + self.style.border_width * 2, h0 + self.style.border_width * 2)
            _cx = bgRect.center().x()
            _cy = bgRect.center().y()
            grad = QConicalGradient(_cx, _cy, self._gradientStartAngle)
            step = 1.0 / (len(self._gradientColors) - 1)
            for i, col in enumerate(self._gradientColors):
                grad.setColorAt(i * step, col)
            
            # outer_rect = QRectF(pixmap.rect().left() - b, pixmap.rect().top() - b, w + b * 2, h + b * 2 - 100) # ăn theo boundingRectFor
            outer_path = QPainterPath()
            outer_path.addRoundedRect(bgRect, self.style.border_radius, self.style.border_radius)
            p.fillPath(outer_path, grad)

            # 2) Clip inner để border không đè content
            # inner_path = QPainterPath()
            # inner_path.addRoundedRect(pixmap.rect(), self._shadowRadius, self._shadowRadius)
            # p.setClipPath(inner_path)
                
        # border pen style (subset)
        # pen = QPen(self.style.border_color or "red")
        pen = QPen(QColor(self.style.border_color))
        # pen.setWidthF(self.style.border_width)
        pen.setWidthF(self._borderWidth)
        if self.style.border_style == "dashed":
            pen.setStyle(Qt.DashLine)
        elif self.style.border_style == "dotted":
            pen.setStyle(Qt.DotLine)
        elif self.style.border_style == "none":
            pen.setStyle(Qt.NoPen)
        p.setPen(pen)
        

        # p.drawRoundedRect(pixmap.rect(), self.style.border_radius, self.style.border_radius)
        p.drawRoundedRect(pixmap.rect(), self._borderRadius, self._borderRadius)
        
        ################### background gradient ###################
        if self._gradient:
            self._draw_background_gradient(p, w, h)
        
        ################### background ###################
        if self._src:
            progress = self._scale/ 0.1 - 1.0
            pan_x = 0.0
            pan_y = 0.0
            
            pan_amount = 0.1 * h if self.direction in ("top", "bottom") else 0.1 * w

            if self.direction == "top":
                pan_y = - progress * pan_amount  # Dịch image lên (pan to top)
            elif self.direction == "bottom":
                pan_y = progress * pan_amount   # Dịch image xuống
            elif self.direction == "left":
                pan_x = -progress * pan_amount  # Dịch image trái
            elif self.direction == "right":
                pan_x = progress * pan_amount   # Dịch image phải
                
            scaled_pix = self._pixmap.scaled(
                int(w * self._scale), int(h * self._scale),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            # Tính vị trí vẽ để center, rồi thêm pan
            draw_x = (w - scaled_pix.width()) / 2.0 + pan_x
            draw_y = (h - scaled_pix.height()) / 2.0 + pan_y
            
            # Vẽ scaled pixmap tại vị trí điều chỉnh
            # painter.drawPixmap(draw_x, 0, scaled_pix)
            p.drawPixmap(0, 0, scaled_pix)

        # outline (draw outside)
        if self.style.outline_width > 0:
            opn = QPen(self.style.outline_color)
            opn.setWidthF(self.style.outline_width)
            p.setPen(opn)
            p.setBrush(Qt.NoBrush)
            out = pixmap.rect().adjusted(-self.style.outline_width, -self.style.outline_width,
                                self.style.outline_width, self.style.outline_width)
            p.drawRoundedRect(out, self.style.border_radius + self.style.outline_width,
                              self.style.border_radius + self.style.outline_width)


        ##################### SHADOW #####################
        try:
            if self._shadowSpec is not None:
                # 0) Shadow
                
                if self._shadowSpec.inset:
                    self._draw_inset_shadow(p, pixmap.rect(), self._shadowSpec)
                else:
                    # OUTSET: dùng cache (kể cả blur=0)
                    
                    if (self._shadowCachePixmap is None and self._shadowSpec is not None) or self._shadowDirty:
                        if not self._rebuildScheduled:
                            self._rebuildScheduled = True
                            QTimer.singleShot(0, self._rebuild_shadow_cache)

                    if self._shadowCachePixmap is not None:
                        p.drawPixmap(self._shadowCacheRect.topLeft(), self._shadowCachePixmap)


        except Exception as e:
            print('eeeeeeeeeeeeeeee', e)
        ##################### END SHADOW #####################
        
        self.drawSource(p)
        
        p.restore()
        