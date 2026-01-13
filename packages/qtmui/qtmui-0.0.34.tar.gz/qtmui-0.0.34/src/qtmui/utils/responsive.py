# src/qtmui/utils/responsive.py
from __future__ import annotations
from typing import Dict, Any, Union, List
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRect
from functools import lru_cache

# Breakpoints chuẩn Material-UI (px)
BREAKPOINTS = {
    "xs": 0,
    "sm": 600,
    "md": 900,
    "lg": 1200,
    "xl": 1536,
}

# Thứ tự từ nhỏ đến lớn
BREAKPOINT_KEYS = ["xs", "sm", "md", "lg", "xl"]

@lru_cache(maxsize=1)
def get_current_breakpoint() -> str:
    """
    Trả về breakpoint hiện tại: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
    """
    screen: QRect = QApplication.primaryScreen().availableGeometry()
    width = screen.width()

    for key in reversed(BREAKPOINT_KEYS):
        if width >= BREAKPOINTS[key]:
            return key
    return "xs"

def resolve_responsive_value(
    value: Any,
    theme_spacing: float = 8.0
) -> Any:
    """
    Giải quyết giá trị responsive
    """
    if value is None:
        return None

    # Trường hợp dict responsive
    if isinstance(value, dict):
        current = get_current_breakpoint()
        # Tìm giá trị lớn nhất <= current breakpoint
        for key in BREAKPOINT_KEYS:
            if key in value and BREAKPOINTS[key] <= BREAKPOINTS[current]:
                result = value[key]
                if result is not None:
                    return _normalize_value(result, theme_spacing)
            if key == current:
                break
        return None

    # Trường hợp array shorthand [vertical, horizontal]
    if isinstance(value, (list, tuple)) and len(value) == 2:
        v, h = value
        v = _normalize_value(v, theme_spacing)
        h = _normalize_value(h, theme_spacing)
        return [v, h] if v is not None and h is not None else None

    # Giá trị thường
    return _normalize_value(value, theme_spacing)

def _normalize_value(value: Any, spacing: float) -> Any:
    if isinstance(value, (int, float)):
        return value * spacing
    return value