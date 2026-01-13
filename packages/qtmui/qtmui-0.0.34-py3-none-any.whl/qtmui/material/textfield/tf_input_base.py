from typing import Optional, Callable

class TFInputBase:
    def __init__(
        self,
        parent=None,
        onMouseEnter: Optional[Callable] = None,  
        onMouseLeave: Optional[Callable] = None,  
        onMousePress: Optional[Callable] = None,  
        onMouseRelease: Optional[Callable] = None,  
        onFocusIn: Optional[Callable] = None,  
        onFocusOut: Optional[Callable] = None,  
        tooltip: Optional[str] = None,  
        tooltipPlacement: Optional[str] = "top",  
        tooltipLeaveDelay: Optional[int] = 0,
        *args,
        **kwargs
    ):
        self._onMouseEnter = onMouseEnter
        self._onMouseLeave = onMouseLeave
        self._onMousePress = onMousePress
        self._onMouseRelease = onMouseRelease
        self._onFocusIn = onFocusIn
        self._onFocusOut = onFocusOut
        self._tooltip = tooltip
        self._tooltipPlacement = tooltipPlacement
        self._tooltipLeaveDelay = tooltipLeaveDelay

    def _setUpUi(self, **kwargs):
        self._onMouseEnter = kwargs.get("onMouseEnter")
        self._onMouseLeave = kwargs.get("onMouseLeave")
        self._onMousePress = kwargs.get("onMousePress")
        self._onMouseRelease = kwargs.get("onMouseRelease")
        self._onFocusIn = kwargs.get("onFocusIn")
        self._onFocusOut = kwargs.get("onFocusOut")


    def enterEvent(self, event):
        # self.setProperty("slot", "hover")
        # self._setStyleSheet()
        if self._onMouseEnter:
            self._onMouseEnter()

    def leaveEvent(self, event):
        # self.setProperty("slot", "leave")
        # self._setStyleSheet()
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
