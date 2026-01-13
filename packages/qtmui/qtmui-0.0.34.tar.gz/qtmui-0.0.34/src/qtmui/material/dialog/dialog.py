import uuid
from typing import Optional, Union, Dict, Callable, List, Literal
from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer, QSize, QEvent
from PySide6.QtGui import QColor, QKeyEvent, QResizeEvent
from PySide6.QtWidgets import (
    QVBoxLayout, 
    QSizePolicy, 
    QApplication, 
    QGraphicsDropShadowEffect, 
    QGraphicsOpacityEffect, 
    QWidget, 
    QHBoxLayout, 
    QDialog, 
    QFrame
)

from qtmui.material.framer_motion.frame_motion import FrameMotion
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.widget_base.anim_manager import AnimManager
from qtmui.material.system.color_manipulator import alpha

from qtmui.hooks import State

from ...material.styles import useTheme
from ..widget_base import PyWidgetBase
from ..utils.validate_params import _validate_param

class Dialog(QDialog, PyWidgetBase):
    """
    A dialog component that displays modal or non-modal content with transitions.

    The `Dialog` component is used to display content in a modal or non-modal dialog,
    supporting all props of the Material-UI `Dialog` and `Modal` components, as well
    as additional props for customization.

    Parameters
    ----------
    open : State or bool, optional
        If True, the dialog is shown. Default is False.
        Can be a `State` object for dynamic updates.
    ariaDescribedby : State, str, or None, optional
        The id(s) of the element(s) that describe the dialog. Default is None.
        Can be a `State` object for dynamic updates.
    ariaLabelledby : State, str, or None, optional
        The id(s) of the element(s) that label the dialog. Default is None.
        Can be a `State` object for dynamic updates.
    ariaModal : State or bool, optional
        Informs assistive technologies that the element is modal. Default is True.
        Can be a `State` object for dynamic updates.
    BackdropComponent : State, str, or None, optional
        The component used for the backdrop. Default is None (uses default backdrop).
        Can be a `State` object for dynamic updates. Deprecated, use slots.backdrop instead.
    children : State, QWidget, List[QWidget], or None, optional
        The dialog children, usually sub-components. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    disableEscapeKeyDown : State or bool, optional
        If True, hitting Escape will not fire onClose. Default is False.
        Can be a `State` object for dynamic updates.
    fullScreen : State or bool, optional
        If True, the dialog is full-screen. Default is False.
        Can be a `State` object for dynamic updates.
    fullWidth : State or bool, optional
        If True, the dialog stretches to maxWidth. Default is False.
        Can be a `State` object for dynamic updates.
    maxWidth : State, str, or bool, optional
        Determines the max-width of the dialog ("xs", "sm", "md", "lg", "xl", False).
        Default is "sm". Can be a `State` object for dynamic updates.
    onClose : State, Callable, or None, optional
        Callback fired when the dialog requests to be closed.
        Signature: function(event: object, reason: string) -> None
        Default is None. Can be a `State` object for dynamic updates.
    PaperComponent : State, str, or None, optional
        The component used for the dialog body. Default is None (uses default paper).
        Can be a `State` object for dynamic updates. Deprecated, use slots.paper instead.
    PaperProps : State or dict, optional
        Props applied to the Paper element. Default is None.
        Can be a `State` object for dynamic updates. Deprecated, use slotProps.paper instead.
    scroll : State or str, optional
        Determines the container for scrolling ("body" or "paper"). Default is "paper".
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for each slot (backdrop, container, paper, root, transition). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for each slot (backdrop, container, paper, root, transition). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    TransitionComponent : State, str, or None, optional
        The component used for the transition (e.g., "Fade"). Default is None (uses Fade).
        Can be a `State` object for dynamic updates. Deprecated, use slots.transition instead.
    transitionDuration : State, int, dict, or None, optional
        The duration for the transition (ms or {appear, enter, exit}). Default is None.
        Can be a `State` object for dynamic updates.
    TransitionProps : State or dict, optional
        Props applied to the transition element. Default is None.
        Can be a `State` object for dynamic updates. Deprecated, use slotProps.transition instead.
    parent : QWidget or None, optional
        The parent widget. Default is None (uses mainWindow).
    borderRadius : State or int, optional
        The border radius of the dialog. Default is 10.
        Can be a `State` object for dynamic updates.
    onButtonOkClicked : State, Callable, or None, optional
        Callback fired when the OK button is clicked. Default is None.
        Can be a `State` object for dynamic updates.
    width : State, int, or None, optional
        The fixed width of the dialog. Default is None.
        Can be a `State` object for dynamic updates.
    height : State, int, or None, optional
        The fixed height of the dialog. Default is None.
        Can be a `State` object for dynamic updates.
    title : State, QWidget, str, or None, optional
        The title of the dialog. Default is None.
        Can be a `State` object for dynamic updates.
    transition : State, str, or None, optional
        The transition effect (e.g., "fadeIn"). Default is None.
        Can be a `State` object for dynamic updates.

    Attributes
    ----------
    customSignal : Signal
        Custom signal for dialog events.
    VALID_MAX_WIDTH : list[Union[str, bool]]
        Valid values for `maxWidth`: ["xs", "sm", "md", "lg", "xl", False].
    VALID_SCROLL : list[str]
        Valid values for `scroll`: ["body", "paper"].

    Notes
    -----
    - Props of the `Modal` component are supported (e.g., `open`, `onClose`).
    - Deprecated props (`BackdropComponent`, `PaperComponent`, `PaperProps`, `TransitionComponent`,
      `TransitionProps`) are supported but should be replaced with `slots` and `slotProps`.
    - The `transition` prop is mapped to `TransitionComponent` for compatibility.

    Demos:
    - Dialog: https://qtmui.com/material-ui/qtmui-dialog/

    API Reference:
    - Dialog API: https://qtmui.com/material-ui/api/dialog/
    - Modal API: https://qtmui.com/material-ui/api/modal/
    """

    customSignal = Signal()
    VALID_MAX_WIDTH = ["xs", "sm", "md", "lg", "xl", False]
    VALID_SCROLL = ["body", "paper"]

    def __init__(
        self,
        open: Union[State, bool] = False,
        ariaDescribedby: Optional[Union[State, str]] = None,
        ariaLabelledby: Optional[Union[State, str]] = None,
        ariaModal: Union[State, bool] = True,
        BackdropComponent: Optional[Union[State, str]] = None,
        children: Optional[Union[State, Callable, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        disableEscapeKeyDown: Union[State, bool] = False,
        fullScreen: Union[State, bool] = False,
        fullWidth: Union[State, bool] = False,
        maxWidth: Union[State, str, bool] = 300, # "sm"
        onClose: Optional[Union[State, Callable]] = None,
        PaperComponent: Optional[Union[State, str]] = None,
        PaperProps: Optional[Union[State, Dict]] = None,
        scroll: Union[State, str] = "paper",
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        TransitionComponent: Optional[Union[State, str]] = None,
        transitionDuration: Optional[Union[State, int, Dict[str, int]]] = None,
        TransitionProps: Optional[Union[State, Dict]] = None,
        parent: Optional[QWidget] = None,
        borderRadius: Union[State, int] = 10,
        onButtonOkClicked: Optional[Union[State, Callable]] = None,
        width: Optional[Union[State, int]] = None,
        height: Optional[Union[State, int]] = None,
        title: Optional[Union[State, QWidget, str]] = None,
        transition: Optional[Union[State, str]] = None,
        **kwargs
    ):
        super().__init__(parent or QApplication.instance().mainWindow)
        self.setObjectName(str(id(self)))
        PyWidgetBase._setUpUi(self)
        
        self._kwargs = kwargs
        
        self.hide()
        
        # Set properties with validation
        self._set_open(open)
        self._set_aria_describedby(ariaDescribedby)
        self._set_aria_labelledby(ariaLabelledby)
        self._set_aria_modal(ariaModal)
        self._set_BackdropComponent(BackdropComponent)
        self._set_children(children)
        self._set_classes(classes)
        self._set_disableEscapeKeyDown(disableEscapeKeyDown)
        self._set_fullScreen(fullScreen)
        self._set_fullWidth(fullWidth)
        self._set_maxWidth(maxWidth)
        self._set_onClose(onClose)
        self._set_PaperComponent(PaperComponent)
        self._set_PaperProps(PaperProps)
        self._set_scroll(scroll)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_sx(sx)
        self._set_TransitionComponent(TransitionComponent)
        self._set_transitionDuration(transitionDuration)
        self._set_TransitionProps(TransitionProps)
        self._set_parent(parent)
        self._set_borderRadius(borderRadius)
        self._set_onButtonOkClicked(onButtonOkClicked)
        self._set_width(width)
        self._set_height(height)
        self._set_title(title)
        self._set_transition(transition)

        self._animation = None
    
        self.__init_ui()


    # Setter and Getter methods for all parameters
    # @_validate_param(file_path="qtmui.material.dialog", param_name="open", supported_signatures=Union[State, bool])
    def _set_open(self, value):
        self._open = value

    def _get_open(self):
        return self._open.value if isinstance(self._open, State) else self._open

    @_validate_param(file_path="qtmui.material.dialog", param_name="ariaDescribedby", supported_signatures=Union[State, str, type(None)])
    def _set_aria_describedby(self, value):
        self._aria_describedby = value

    def _get_aria_describedby(self):
        return self._aria_describedby.value if isinstance(self._aria_describedby, State) else self._aria_describedby

    @_validate_param(file_path="qtmui.material.dialog", param_name="ariaLabelledby", supported_signatures=Union[State, str, type(None)])
    def _set_aria_labelledby(self, value):
        self._aria_labelledby = value

    def _get_aria_labelledby(self):
        return self._aria_labelledby.value if isinstance(self._aria_labelledby, State) else self._aria_labelledby

    @_validate_param(file_path="qtmui.material.dialog", param_name="ariaModal", supported_signatures=Union[State, bool])
    def _set_aria_modal(self, value):
        self._aria_modal = value

    def _get_aria_modal(self):
        return self._aria_modal.value if isinstance(self._aria_modal, State) else self._aria_modal

    @_validate_param(file_path="qtmui.material.dialog", param_name="BackdropComponent", supported_signatures=Union[State, str, type(None)])
    def _set_BackdropComponent(self, value):
        self._BackdropComponent = value

    def _get_BackdropComponent(self):
        return self._BackdropComponent.value if isinstance(self._BackdropComponent, State) else self._BackdropComponent

    # @_validate_param(file_path="qtmui.material.dialog", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        # if isinstance(value, list) and not all(isinstance(item, QWidget) for item in value if item is not None):
        #     raise ValueError("children must be a QWidget or a list of QWidgets")
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.dialog", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.dialog", param_name="disableEscapeKeyDown", supported_signatures=Union[State, bool])
    def _set_disableEscapeKeyDown(self, value):
        self._disableEscapeKeyDown = value

    def _get_disableEscapeKeyDown(self):
        return self._disableEscapeKeyDown.value if isinstance(self._disableEscapeKeyDown, State) else self._disableEscapeKeyDown

    @_validate_param(file_path="qtmui.material.dialog", param_name="fullScreen", supported_signatures=Union[State, bool])
    def _set_fullScreen(self, value):
        self._fullScreen = value

    def _get_fullScreen(self):
        return self._fullScreen.value if isinstance(self._fullScreen, State) else self._fullScreen

    @_validate_param(file_path="qtmui.material.dialog", param_name="fullWidth", supported_signatures=Union[State, bool])
    def _set_fullWidth(self, value):
        self._fullWidth = value

    def _get_fullWidth(self):
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    # @_validate_param(file_path="qtmui.material.dialog", param_name="maxWidth", supported_signatures=Union[State, str, bool], valid_values=VALID_MAX_WIDTH)
    def _set_maxWidth(self, value):
        self._maxWidth = value

    def _get_maxWidth(self):
        return self._maxWidth.value if isinstance(self._maxWidth, State) else self._maxWidth

    @_validate_param(file_path="qtmui.material.dialog", param_name="onClose", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClose(self, value):
        self._onClose = value

    def _get_onClose(self):
        return self._onClose.value if isinstance(self._onClose, State) else self._onClose

    @_validate_param(file_path="qtmui.material.dialog", param_name="PaperComponent", supported_signatures=Union[State, str, type(None)])
    def _set_PaperComponent(self, value):
        self._PaperComponent = value

    def _get_PaperComponent(self):
        return self._PaperComponent.value if isinstance(self._PaperComponent, State) else self._PaperComponent

    @_validate_param(file_path="qtmui.material.dialog", param_name="PaperProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_PaperProps(self, value):
        self._PaperProps = value

    def _get_PaperProps(self):
        return self._PaperProps.value if isinstance(self._PaperProps, State) else self._PaperProps

    @_validate_param(file_path="qtmui.material.dialog", param_name="scroll", supported_signatures=Union[State, str], valid_values=VALID_SCROLL)
    def _set_scroll(self, value):
        self._scroll = value

    def _get_scroll(self):
        return self._scroll.value if isinstance(self._scroll, State) else self._scroll

    @_validate_param(file_path="qtmui.material.dialog", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.dialog", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.dialog", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.dialog", param_name="TransitionComponent", supported_signatures=Union[State, str, type(None)])
    def _set_TransitionComponent(self, value):
        self._TransitionComponent = value

    def _get_TransitionComponent(self):
        return self._TransitionComponent.value if isinstance(self._TransitionComponent, State) else self._TransitionComponent

    # @_validate_param(file_path="qtmui.material.dialog", param_name="transitionDuration", supported_signatures=Union[State, int, Dict[str, int], type(None)])
    def _set_transitionDuration(self, value):
        if isinstance(value, dict) and not all(k in ["appear", "enter", "exit"] for k in value):
            raise ValueError("transitionDuration dict must contain 'appear', 'enter', or 'exit' keys")
        self._transitionDuration = value

    def _get_transitionDuration(self):
        return self._transitionDuration.value if isinstance(self._transitionDuration, State) else self._transitionDuration

    @_validate_param(file_path="qtmui.material.dialog", param_name="TransitionProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_TransitionProps(self, value):
        self._TransitionProps = value

    def _get_TransitionProps(self):
        return self._TransitionProps.value if isinstance(self._TransitionProps, State) else self._TransitionProps

    @_validate_param(file_path="qtmui.material.dialog", param_name="parent", supported_signatures=Union[QWidget, type(None)])
    def _set_parent(self, value):
        self._parent = value

    def _get_parent(self):
        return self._parent

    @_validate_param(file_path="qtmui.material.dialog", param_name="borderRadius", supported_signatures=Union[State, int])
    def _set_borderRadius(self, value):
        self._borderRadius = value

    def _get_borderRadius(self):
        return self._borderRadius.value if isinstance(self._borderRadius, State) else self._borderRadius

    @_validate_param(file_path="qtmui.material.dialog", param_name="onButtonOkClicked", supported_signatures=Union[State, Callable, type(None)])
    def _set_onButtonOkClicked(self, value):
        self._onButtonOkClicked = value

    def _get_onButtonOkClicked(self):
        return self._onButtonOkClicked.value if isinstance(self._onButtonOkClicked, State) else self._onButtonOkClicked

    @_validate_param(file_path="qtmui.material.dialog", param_name="width", supported_signatures=Union[State, int, type(None)])
    def _set_width(self, value):
        self._width = value

    def _get_width(self):
        return self._width.value if isinstance(self._width, State) else self._width

    @_validate_param(file_path="qtmui.material.dialog", param_name="height", supported_signatures=Union[State, int, type(None)])
    def _set_height(self, value):
        self._height = value

    def _get_height(self):
        return self._height.value if isinstance(self._height, State) else self._height

    @_validate_param(file_path="qtmui.material.dialog", param_name="title", supported_signatures=Union[State, QWidget, str, type(None)])
    def _set_title(self, value):
        self._title = value

    def _get_title(self):
        return self._title.value if isinstance(self._title, State) else self._title

    @_validate_param(file_path="qtmui.material.dialog", param_name="transition", supported_signatures=Union[State, str, type(None)])
    def _set_transition(self, value):
        self._transition = value

    def _get_transition(self):
        return self._transition.value if isinstance(self._transition, State) else self._transition

    def __init_ui(self):
        
        self._hBoxLayout = QHBoxLayout(self)
        self.windowMask = QWidget(self)
        self.windowMask.setObjectName('windowMask')

        # dialog box in the center of mask, all widgets take it as parent
        self.widget = FrameMotion(parent=self, **self._kwargs)
        # self.widget = FrameMotion(parent=self)
        # self.widget = QFrame(self, objectName='centerWidget')
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        if self._parent:
            self.setGeometry(0, 0, self._parent.width(), self._parent.height())
        elif QApplication.instance().mainWindow:
            self.setGeometry(0, 0, QApplication.instance().mainWindow.width(), QApplication.instance().mainWindow.height())


        c = 0 if useTheme().palette.mode == "dark" else 255
        self.windowMask.resize(self.size())
        self.windowMask.setStyleSheet(f'''
            #windowMask{{
                background:rgba({c}, {c}, {c}, 0.6);
            }}
        ''')

        self._hBoxLayout.addWidget(self.widget)
        
        self.window().installEventFilter(self)
        
        
        if isinstance(self._open, State):
            self._open.valueChanged.connect(self._set_visible)
            if self._open.value == True:
                self._set_visible(self._open.value)

        # self.widget.hide()

        if self._fullScreen:
            self.layout().setContentsMargins(0,50,0,0)
            self.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self._borderRadius = 0
        else:
            self.widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            if self._width:
                self.widget.setFixedWidth(self._width)
            elif self._maxWidth:
                self.widget.setFixedWidth(self._maxWidth)
            if self._height:
                self.widget.setFixedHeight(self._height)


        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self._set_stylesheet)
        # self.destroyed.connect(self._on_destroyed)
        self._set_stylesheet()


    def mousePressEvent(self, event):
        if not self.widget.underMouse():
            self.hide()
        return super().mousePressEvent(event)

    def _set_visible(self, show):
        if show:
            self.show()
        elif show is not None:
            self.hide()

    def _accept(self):
        self.onButtonOkClicked()
        
    def _reject(self):
        self.close()

    def _set_stylesheet(self, component_styled=None):
        
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components


        PyDialog = component_styled["PyDialog"].get("styles")
        PyDialogPaperRootStyles = get_qss_style(PyDialog["paper"]["root"])
        PyDialogPaperFullScreenStyles = get_qss_style(PyDialog["paperFullScreen"])

        PyDialogPaperRootSlotFullScreenStyles = get_qss_style(PyDialog["paper"]["root"]["slots"]["fullScreen"])

        c = 0 if self.theme.palette.mode == "dark" else 255
        
        self.windowMask.setStyleSheet(f'''
            #windowMask{{
                background:rgba({c}, {c}, {c}, 0.6);
            }}
        ''')

        self.widget.setStyleSheet(f"""
            #{self.widget.objectName()} {{
                {PyDialogPaperRootStyles}
                {PyDialogPaperFullScreenStyles if self._fullScreen else ""}
                {PyDialogPaperRootSlotFullScreenStyles if self._fullScreen else ""}
            }}
        """)

        self.setShadowEffect()


    def setShadowEffect(self, blurRadius=60, offset=(0, 10), color=QColor(0, 0, 0, 100)):
        """ add shadow to dialog """
        shadowEffect = QGraphicsDropShadowEffect(self.widget)
        shadowEffect.setBlurRadius(blurRadius)
        shadowEffect.setOffset(*offset)
        shadowEffect.setColor(color)
        self.widget.setGraphicsEffect(None)
        self.widget.setGraphicsEffect(shadowEffect)

    def resizeEvent(self, e):
        self.windowMask.resize(self.size())

    def _setupChildrenAndShow(self):
        """ fade in """
        if not self.widget.layout().count():
            children = []
            if isinstance(self._children, Callable):
                children = self._children()
            elif isinstance(self._children, list):
                children = self._children
                
            self.widget._children = children
            self.widget._update_children()


        if QApplication.instance().mainWindow:
            self.setParent(QApplication.instance().mainWindow)
            self.setGeometry(0, 0, QApplication.instance().mainWindow.width(), QApplication.instance().mainWindow.height())
            if not self.isVisible():
                self.show()
            # if not self.widget.isVisible():
            #     self.widget.show()
                
        self.setShadowEffect()
        


    def showEvent(self, e):
        self.setParent(QApplication.instance().mainWindow)
        QTimer.singleShot(0, self._setupChildrenAndShow)
        super().showEvent(e)
        
    def hideEvent(self, event):
        if self._onClose:
            self._onClose()
        return super().hideEvent(event)

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                re = QResizeEvent(e)
                self.resize(re.size())

        return super().eventFilter(obj, e)