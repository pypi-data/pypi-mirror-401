from math import cos, pi

from PySide6.QtWidgets import QGraphicsEffect
from PySide6.QtCore import Property, QPointF, QPoint, Qt, QRectF
from PySide6.QtGui import QPainter, QPixmap

class AnimEffect(QGraphicsEffect):
    """Flip theo trục X, mô phỏng bằng scaleY = cos(angle)."""

    def __init__(self, parent=None, src: str = None):
        super().__init__(parent)
        self._src = src
        
        if src:
            print('vvvvvvvvvvvvvvvvvvv')
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
        # print('src_________________', src)
        

            

        # self._progress = 0.0  # 0 → 1

    # ############# background effect ###########
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
    

    def draw(self, painter: QPainter):
        # if hasattr(self, "_pixmap"):
        #     pixmap = self._pixmap
        # else:
            
        pixmap = self.sourcePixmap()
            
        if pixmap.isNull():
            print('pixmap.isNull()')
            return

        painter.save()
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform
        )
        
        ################### opacity ###################
        # painter.setOpacity(1)
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
        # painter.scale(scale_y, scale_x)
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
        
        ################### background ###################
        # print('self._src__________', self._src)
        if self._src:
            # print('self.scale_________', self._scale)
            
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
                # int(w * self._scale), int(h * self._scale),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            # Tính vị trí vẽ để center, rồi thêm pan
            draw_x = (w - scaled_pix.width()) / 2.0 + pan_x
            draw_y = (h - scaled_pix.height()) / 2.0 + pan_y
            
            # print("draw_x_____________", draw_x)

            # Vẽ scaled pixmap tại vị trí điều chỉnh
            # painter.drawPixmap(draw_x, 0, scaled_pix)
            painter.drawPixmap(0, 0, scaled_pix)
            
        
        # Vẽ pixmap
        if not self._angle:
            self.drawSource(painter)
            
        painter.restore()


        # painter.drawPixmap(0, 0, self._pixmap)
        # print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        # painter.restore()
        # self.drawSource(painter)

