from typing import Optional, Union, Callable
from .qtrangeslider._labeled import (
    QRangeSlider,
    
    QDoubleSlider,
    QDoubleRangeSlider,

    QLabeledSlider,
    QLabeledRangeSlider,
    QLabeledDoubleSlider,
    QLabeledDoubleRangeSlider,

)
from PySide6.QtCore import Qt

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.hooks import State

style = """
                QSlider:horizontal {
                        min-height: 24px;
                }

                QSlider::groove:horizontal {
                        height: 4px;
                        background-color: _groove_bg_color_;
                        border-radius: 2px;
                }

                QSlider::sub-page:horizontal {
                        background: _main_color_;
                        height: 4px;
                        border-radius: 2px;
                }

                QSlider::handle:horizontal {
                        border: 1px solid rgb(222, 222, 222);
                        width: 20px;
                        min-height: 24px;
                        margin: -9px 0;
                        border-radius: 11px;
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 _main_color_,
                                stop:0.48 _main_color_,
                                stop:0.55 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::handle:horizontal:hover {
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 _main_color_,
                                stop:0.55 _main_color_,
                                stop:0.65 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::handle:horizontal:pressed {
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 _main_color_,
                                stop:0.4 _main_color_,
                                stop:0.5 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::groove:horizontal:disabled {
                        background-color: _groove_bg_color_;
                }

                QSlider::handle:horizontal:disabled {
                        background-color: #808080;
                        border: 5px solid #cccccc;
                }


                QSlider:vertical {
                        min-width: 24px;
                }

                QSlider::groove:vertical {
                        width: 4px;
                        background-color: _groove_bg_color_;
                        border-radius: 2px;
                }

                QSlider::add-page:vertical {
                        background: _main_color_;
                        width: 4px;
                        border-radius: 2px;
                }

                QSlider::handle:vertical {
                        border: 1px solid rgb(222, 222, 222);
                        height: 20px;
                        min-width: 24px;
                        margin: 0 -9px;
                        border-radius: 11px;
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 _main_color_,
                                stop:0.48 _main_color_,
                                stop:0.55 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::handle:vertical:hover {
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 _main_color_,
                                stop:0.55 _main_color_,
                                stop:0.65 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::handle:vertical:pressed {
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 _main_color_,
                                stop:0.4 _main_color_,
                                stop:0.5 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::groove:vertical:disabled {
                        background-color: _groove_bg_color_;
                }

                QSlider::handle:vertical:disabled {
                        background-color: #808080;
                        border: 5px solid #cccccc;
                }
        """

def getColor(_color: str = "primary", theme=None) -> str:
    if _color == "inherit":
        color = theme.palette.text.primary
    elif _color == "default":
        color = theme.palette.text.secondary
    elif _color in ['primary', 'secondary', 'info', 'success', 'warning', 'error']:
        color = getattr(theme.palette, _color).main
    else:
        color = theme.palette.text.secondary
    return color

class SliderBase:
    
    def _setValue(self, value):
        if value is not None:
            if isinstance(value, State):
                self.setValue(value.value)
            else:
                self.setValue(value)

class RangeSlider(SliderBase, QRangeSlider):
    def __init__(self, color: str = "primary", size: str = "medium", areaLabel: str = "", getAreaLabel: Callable = None, disabled: bool = False, step: Optional[Union[int, float, None]] = 1, orientation: str = "vertical", onChange: Callable = None, value=None, min: int = 0, max: int = 1):
        super().__init__(Qt.Horizontal if orientation == "horizontal" else Qt.Vertical)
        self._orientation = orientation
        # if value is None:
        #     value = (20, 80)
        color = getColor(color, useTheme())
        self.setStyleSheet(style.replace("_main_color_", color).replace("_groove_bg_color_", useTheme().palette.grey._500))
        if onChange:
            self.valueChanged.connect(onChange)
            
        self._setValue(value)
        
            


class MultiHandleRangeSlider(SliderBase, QRangeSlider):
    def __init__(self, color: str = "primary", size: str = "medium", areaLabel: str = "", getAreaLabel: Callable = None, disabled: bool = False, step: Optional[Union[int, float, None]] = 1, orientation: str = "vertical", onChange: Callable = None, min: int = 0, max: int = 200, value=None):
        super().__init__(Qt.Horizontal if orientation == "horizontal" else Qt.Vertical)
        self._orientation = orientation
        # if value is None:
        #     value = (0, 40, 80, 160)
        self.setMinimum(min)
        self.setMaximum(max)
        # self.setValue(value)
        color = getColor(color, useTheme())
        self.setStyleSheet(style.replace("_main_color_", color).replace("_groove_bg_color_", useTheme().palette.grey._500))
        if onChange:
            self.valueChanged.connect(onChange)
            
        self._setValue(value)
        

class DoubleSlider(SliderBase, QDoubleSlider):
    def __init__(self, color: str = "primary", size: str = "medium", areaLabel: str = "", getAreaLabel: Callable = None, disabled: bool = False, step: Optional[Union[int, float, None]] = 1, orientation: str = "vertical", onChange: Callable = None, min: int = 0, max: int = 1, value: float = 0.5):
        super().__init__(Qt.Horizontal if orientation == "horizontal" else Qt.Vertical)
        self._orientation = orientation
        self.setRange(min, max)
        # self.setValue(value)
        # self.setSingleStep(step)
        color = getColor(color, useTheme())
        self.setStyleSheet(style.replace("_main_color_", color).replace("_groove_bg_color_", useTheme().palette.grey._500))
        if onChange:
            self.valueChanged.connect(onChange)
            
        self._setValue(value)


class DoubleRangeSlider(SliderBase, QDoubleRangeSlider):
    def __init__(self, color: str = "primary", size: str = "medium", areaLabel: str = "", getAreaLabel: Callable = None, disabled: bool = False, step: Optional[Union[int, float, None]] = 1, orientation: str = "vertical", onChange: Callable = None, min: int = 0, max: int = 1, value=None):
        super().__init__(Qt.Horizontal if orientation == "horizontal" else Qt.Vertical)
        self._orientation = orientation
        if value is None:
            value = (0.2, 0.8)
        self.setMaximum(max)
        # self.setValue(value)
        color = getColor(color, useTheme())
        self.setStyleSheet(style.replace("_main_color_", color).replace("_groove_bg_color_", useTheme().palette.grey._500))
        if onChange:
            self.valueChanged.connect(onChange)
            
        self._setValue(value)
        

class LabeledSlider(SliderBase, QLabeledSlider):
    def __init__(self, color: str = "primary", size: str = "medium", areaLabel: str = "", getAreaLabel: Callable = None, disabled: bool = False, step: Optional[Union[int, float, None]] = 1, orientation: str = "vertical", onChange: Callable = None, min: int = 0, max: int = 500, value: int = 300):
        super().__init__(Qt.Horizontal if orientation == "horizontal" else Qt.Vertical)
        self._orientation = orientation
        self.setRange(min, max)
        # self.setValue(value)
        color = getColor(color, useTheme())
        self.setStyleSheet(style.replace("_main_color_", color).replace("_groove_bg_color_", useTheme().palette.grey._500))
        if onChange:
            self.valueChanged.connect(onChange)
            
        self._setValue(value)
        

class LabeledRangeSlider(SliderBase, QLabeledRangeSlider):
    def __init__(self, color: str = "primary", size: str = "medium", areaLabel: str = "", getAreaLabel: Callable = None, disabled: bool = False, step: Optional[Union[int, float, None]] = 1, orientation: str = "vertical", onChange: Callable = None, value=None, min: int = 0, max: int = 100):
        super().__init__(Qt.Horizontal if orientation == "horizontal" else Qt.Vertical)
        self._orientation = orientation
        if value is None:
            value = (20, 60)
        # self.setValue(value)
        color = getColor(color, useTheme())
        self.setStyleSheet(style.replace("_main_color_", color).replace("_groove_bg_color_", useTheme().palette.grey._500))
        if onChange:
            self.valueChanged.connect(onChange)
            
        self._setValue(value)
        

class LabeledDoubleSlider(SliderBase, QLabeledDoubleSlider):
    def __init__(self, color: str = "primary", size: str = "medium", areaLabel: str = "", getAreaLabel: Callable = None, disabled: bool = False, step: Optional[Union[int, float, None]] = 1, orientation: str = "vertical", onChange: Callable = None, min: int = 0, max: int = 1, value: float = 0.5, singleStep: Optional[Union[int, float]] = 0.1):
        super().__init__(Qt.Horizontal if orientation == "horizontal" else Qt.Vertical)
        self._orientation = orientation
        self.setRange(min, max)
        # self.setValue(value)
        self.setSingleStep(singleStep)
        color = getColor(color, useTheme())
        self.setStyleSheet(style.replace("_main_color_", color).replace("_groove_bg_color_", useTheme().palette.grey._500))
        if onChange:
            self.valueChanged.connect(onChange)
            
        self._setValue(value)

class LabeledDoubleRangeSlider(SliderBase, QLabeledDoubleRangeSlider):
    def __init__(self, color: str = "primary", size: str = "medium", areaLabel: str = "", getAreaLabel: Callable = None, disabled: bool = False, step: Optional[Union[int, float, None]] = 1, orientation: str = "vertical", onChange: Callable = None, min: int = 0, max: int = 1, value=None, singleStep: Optional[Union[int, float]] = 0.01):
        super().__init__(Qt.Horizontal if orientation == "horizontal" else Qt.Vertical)
        self._orientation = orientation
        if value is None:
            value = (0.2, 0.7)
        self.setRange(min, max)
        self.setSingleStep(singleStep)
        # self.setValue(value)
        color = getColor(color, useTheme())
        self.setStyleSheet(style.replace("_main_color_", color).replace("_groove_bg_color_", useTheme().palette.grey._500))
        if onChange:
            self.valueChanged.connect(onChange)
            
        self._setValue(value)
