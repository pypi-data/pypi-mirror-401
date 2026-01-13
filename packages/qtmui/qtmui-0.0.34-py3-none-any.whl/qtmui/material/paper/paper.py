from typing import Optional, Union, Dict, List, Callable
import uuid

from PySide6.QtWidgets import (
    QFrame, QWidget, QGraphicsDropShadowEffect, QVBoxLayout, QLabel
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Property

from qtmui.material.system.color_manipulator import rgbaToQColor
from qtmui.material.typography import Typography
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style


class Paper(QFrame):
    def __init__(
        self,
        parent=None,
        children: Optional[Union[State, str, QWidget, List[QWidget]]] = None,
        classes=None,
        component: Optional[Union[State, QWidget]] = None,
        elevation: Union[State, int] = 1,
        square: Union[State, bool] = False,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        variant: Union[State, str] = "elevation",
        color=None,
        *args, **kwargs
    ):
        super().__init__(parent)
        self.setObjectName(str(uuid.uuid4()))

        # === Props ===
        self._classes = classes or {}
        self._component = component
        self._elevation = elevation
        self._square = square
        self._sx = sx
        self._variant = variant
        # self._color = QColor(color) if color else None
        self._color = color

        # === Layout ===
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        if children:
            if isinstance(children, list):
                for child in children:
                    if isinstance(child, QWidget):
                        self._layout.addWidget(child)
            elif isinstance(children, str):
                # self._layout.addWidget(Typography(text=children))
                self._layout.addWidget(QLabel(children))

        # === Style ===
        self._shadow_effect = None
        self._update_style()

    # ======================================================
    # =============== Internal Helpers =====================
    # ======================================================

    def _blur_for_elevation(self, elevation: int) -> int:
        """Map elevation (0–24) to shadow blur."""
        return max(2, min(64, elevation * 3))

    def _update_style(self, component_styled=None):
        self.theme = useTheme()
        ownerState = {}
        if not component_styled:
            component_styled = self.theme.components

        PyPaper_root = component_styled["PyPaper"].get("styles")["root"]
        PyPaper_root_qss = get_qss_style(PyPaper_root)
        
        PyPaper_outlined = component_styled["PyPaper"].get("styles")["outlined"]
        PyPaper_outlined_qss = get_qss_style(PyPaper_outlined)
        
        
        # Apply base style
        if self._variant == "outlined":
            self.setProperty("outlined", True)
            
        square_style = ""
        if self._square:
            square_style = "border-radius: 0px;"
            
        color_style = ""
        if self._color:
            color_style = f"background-color: {self._color};"
            
        
        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, State):
                sx = self._sx.value
            elif isinstance(self._sx, Callable):
                sx = self._sx()
            else:
                sx = self._sx

            if isinstance(sx, dict):
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        stylesheet = f"""
            #{self.objectName()} {{
                {PyPaper_root_qss}
                {square_style}
                {color_style}
            }}
            #{self.objectName()}[outlined=true] {{
                {PyPaper_outlined_qss}
            }}
            
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

        # Apply shadow only if variant == elevation and elevation > 0
        if self._variant == "elevation" and self._elevation > 0:
            if not self._shadow_effect:
                self._shadow_effect = QGraphicsDropShadowEffect(self)
            self._shadow_effect.setOffset(0, self._elevation)
            self._shadow_effect.setBlurRadius(self._blur_for_elevation(self._elevation))
            self._shadow_effect.setColor(rgbaToQColor(self._color) if self._color else QColor(0, 0, 0, 30 + self._elevation * 5))
            # self._shadow_effect.setColor(QColor(0, 0, 0, 10 + self._elevation * 3))
            self.setGraphicsEffect(self._shadow_effect)
        else:
            self.setGraphicsEffect(None)

    # ======================================================
    # =============== Getters / Setters ====================
    # ======================================================

    def getElevation(self):
        return self._elevation

    def setElevation(self, value):
        self._elevation = max(0, min(24, value))
        self._update_style()

    elevation = Property(int, getElevation, setElevation)

    def getVariant(self):
        return self._variant

    def setVariant(self, value):
        self._variant = value
        self._update_style()

    variant = Property(str, getVariant, setVariant)

    def getSquare(self):
        return self._square

    def setSquare(self, value: bool):
        self._square = value
        self._radius = 0 if value else 8
        self._update_style()

    square = Property(bool, getSquare, setSquare)

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = QColor(color)
        self._update_style()

    color = Property(QColor, getColor, setColor)

    def getSX(self):
        return self._sx

    def setSX(self, sx):
        self._sx = sx
        self._update_style()

    sx = Property("QVariant", getSX, setSX)
