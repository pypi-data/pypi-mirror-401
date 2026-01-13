import uuid
from typing import Optional, Callable, Any, Dict, Union

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject,Qt,QEvent
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

class MuiInputBase:
    def __init__(
        self,
        parent=None,
        onMouseEnter: Optional[Callable] = None,  
        onMouseLeave: Optional[Callable] = None,  
        onMousePress: Optional[Callable] = None,  
        onMouseRelease: Optional[Callable] = None,  
        onFocusIn: Optional[Callable] = None,  
        onFocusOut: Optional[Callable] = None,  
        **kwargs
    ):
        self._onMouseEnter = onMouseEnter
        self._onMouseLeave = onMouseLeave
        self._onMousePress = onMousePress
        self._onMouseRelease = onMouseRelease
        self._onFocusIn = onFocusIn
        self._onFocusOut = onFocusOut

    
    def enterEvent(self, event):
        if self._onMouseEnter:
            self._onMouseEnter()
    
    def leaveEvent(self, event):
        if self._onMouseLeave:
            self._onMouseLeave()
    
    def mousePressEvent(self, event):
        if self._onMousePress:
            self._onMousePress()
    
    def mouseReleaseEvent(self, event):
        if self._onMouseRelease:
            self._onMouseRelease()
    
    def focusInEvent(self, event) -> None:
        if self._onFocusIn:
            self._onFocusIn(event)

    def focusOutEvent(self, event) -> None:
        if self._onFocusOut:
            self._onFocusOut(event)
