#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Animate Box demo
- Box là QFrame có thể chứa children (Box hoặc widget)
- Mỗi Box có AnimQObject để apply initial và play animate
- Container Box (Box with children) sẽ đọc transition.delayChildren và staggerChildren
  và điều phối play() cho các child theo thứ tự (đặt trong showEvent)
"""

import sys
from typing import Optional, Dict, List, Callable, Union, Any
from math import cos, pi

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

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

