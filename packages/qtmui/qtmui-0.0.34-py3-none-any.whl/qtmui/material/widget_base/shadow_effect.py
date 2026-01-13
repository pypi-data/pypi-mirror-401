

from typing import List

from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, QPalette

from qtmui.material.system.color_manipulator import rgbaToQColor, hex_string_to_qcolor


class ShadownEffect:
    def __init__(
        self
    ):
      pass
    
    def _setShadownEffect(self, shadow):
      if shadow:
        offset_dx = shadow[0] # 0 - 24
        offset_dy = shadow[1] # 0 - 24
        blur_radius = shadow[2] # 2- 64
        # color_deep = shadow[3] # 2- 64
        
        if not hasattr(self, "_shadow_effect"):
          self._shadow_effect = QGraphicsDropShadowEffect(self)
          
        self._shadow_effect.setOffset(offset_dx, offset_dy)
        self._shadow_effect.setBlurRadius(blur_radius)
        color = self.palette().color(QPalette.ColorRole.ButtonText).name()
        # self._shadow_effect.setColor(rgbaToQColor(color) if self._color else QColor(0, 0, 0, 30 + self._elevation * 5))
        self._shadow_effect.setColor(hex_string_to_qcolor(color))
        self.setGraphicsEffect(self._shadow_effect)


    def _blur_for_elevation(self, elevation: int) -> int:
        """Map elevation (0–24) to shadow blur."""
        return max(2, min(64, elevation * 3))