from math import cos, pi

from PySide6.QtWidgets import QGraphicsEffect
from PySide6.QtCore import Property, QPointF, QPoint, Qt, QRectF
from PySide6.QtGui import QPainter, QPixmap, QLinearGradient, QColor, QBrush, QGradient

from qtmui.material.styles import useTheme

class AnimEffect(QGraphicsEffect):
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


    def __init__(self, parent=None, src: str = None, variants: dict = None):
        super().__init__(parent)
        self._src = src
        
        if src:
            self._pixmap = QPixmap(src)
        
        self._opacity = 1.0  # 0.0 → 1.0
        self._angle = 0.0  # độ, -360 → 0 hoặc 0 → 360
        self._offsetX = 0.0
        self._offsetY = 0.0
        self._rotationX = 0.0  # độ, -180 → 0 hoặc 0 → 180
        self._rotationY = 0.0  # độ, -180 → 0 hoặc 0 → 180
        self._scaleX = 1.0
        self._scaleY = 1.0
        self._scale = 1.0
        self.direction = "right"
        
        self._gradient = variants.get("animate", {}).get("gradient")
        self._bgProgress = 0.0
            


    # ############# background image effect ###########
    # def boundingRectFor(self, sourceRect: QRectF) -> QRectF: # background effect
    #     # Override để ngăn chặn size widget thay đổi do effect vẽ ngoài bound.
    #     # Bằng cách return sourceRect, effect bị clip trong bound gốc, không mở rộng size.
    #     return sourceRect

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


    def getScale(self):
        return self._scale

    def setScale(self, v):
        self._scale = v
        self.update()

    scale = Property(float, getScale, setScale)
    
    def getBgProgress(self):
        return self._bgProgress

    def setBgProgress(self, v):
        self._bgProgress = v
        self.update()

    bgProgress = Property(float, getBgProgress, setBgProgress)
    

    def draw(self, painter: QPainter):
        if hasattr(self, "_pixmap"):
            pixmap = self._pixmap
        else:
            pixmap = self.sourcePixmap()
            
        if pixmap.isNull():
            print('pixmap.isNull()')
            return

        painter.save()
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform
        )
        
        ################### opacity ###################
        painter.setOpacity(self._opacity)


        ################### Flip Scale X/Y ###################
        w, h = pixmap.width(), pixmap.height()
        cx, cy = w / 2, h / 2

        # Dịch tâm
        painter.translate(cx, cy)
        # Góc radian
        radX = self._rotationX * pi / 180.0
        radY = self._rotationY * pi / 180.0
        scale_x = cos(radX)
        scale_y = cos(radY)
        # Giữ dấu để flip
        if self._rotationX == 0.0 and self._rotationY == 0.0:
            painter.scale(self._scaleX, self._scaleY)
        else:
            painter.scale(scale_y, scale_x)
        
        # Dịch tâm về lại
        painter.translate(-cx, -cy)
        

        ################### Flip Scale X/Y ###################
        if self._angle != 0.0:
            offset = QPoint()
            pixmap = self.sourcePixmap(Qt.DeviceCoordinates)
            
            cx = pixmap.width() / 2
            cy = pixmap.height() / 2

            painter.translate(QPointF(offset) + QPointF(cx, cy))
            painter.rotate(self._angle)
            painter.translate(-cx, -cy)

            painter.drawPixmap(0, 0, pixmap)
        
        
        ################### background gradient ###################
        if self._gradient:
            self._draw_background_gradient(painter, w, h)
        
        
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
                
            scaled_pix = pixmap.scaled(
                int(w * self._scale), int(h * self._scale),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            # Tính vị trí vẽ để center, rồi thêm pan
            draw_x = (w - scaled_pix.width()) / 2.0 + pan_x
            draw_y = (h - scaled_pix.height()) / 2.0 + pan_y
            
            # Vẽ scaled pixmap tại vị trí điều chỉnh
            # painter.drawPixmap(draw_x, 0, scaled_pix)
            painter.drawPixmap(0, 0, scaled_pix)
            
        
        # Vẽ pixmap
        if not self._angle:
            self.drawSource(painter)
            
        painter.restore()


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