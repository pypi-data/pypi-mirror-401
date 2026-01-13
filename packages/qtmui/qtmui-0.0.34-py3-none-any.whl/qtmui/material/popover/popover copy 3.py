from weakref import ref
import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QApplication, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QEvent, QTimer, QPoint, QPropertyAnimation, Signal
from PySide6.QtGui import QCursor, QColor
from qtmui.hooks import State
from ..paper import Paper
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..widget_base import PyWidgetBase
from ..utils.validate_params import _validate_param


class PopoverRef:
    """Reference object for Popover actions."""
    def __init__(self, popover):
        self._popover = ref(popover)
    
    def updatePosition(self):
        """Update the position of the popover."""
        popover = self._popover()
        if popover:
            popover._update_position()

    def setOpen(self, open: bool):
        popover = self._popover()
        if popover:
            popover._set_visible(open)

    def toggle(self):
        popover = self._popover()
        if popover:
            popover._set_visible(not popover.is_visible)


class Popover(QFrame, PyWidgetBase):
    """
    A component that renders a popover, styled like Material-UI Popover.

    The `Popover` component displays content relative to an anchor element, with support for positioning,
    transitions, and backdrop. It integrates with `Paper` and other components in the `qtmui` framework,
    retaining existing parameters (except `parent` and `content`), adding new parameters, and aligning with MUI props.

    Parameters
    ----------
    open : State[bool]
        If True, the popover is shown. Required.
        Can be a `State` object for dynamic updates.
    action : State or Ref, optional
        A ref for imperative actions (supports updatePosition()). Default is None.
        Can be a `State` object for dynamic updates.
    anchorEl : State[QWidget], Callable, or None, optional
        The anchor element or a function returning it. Default is None.
        Can be a `State` object for dynamic updates.
    anchorOrigin : State or dict, optional
        The point on the anchor where the popover attaches. Default is {'vertical': 'top', 'horizontal': 'left'}.
        Can be a `State` object for dynamic updates.
        Options: vertical: ['top', 'center', 'bottom', number]; horizontal: ['left', 'center', 'right', number].
    anchorPosition : State or dict, optional
        The absolute position for the popover ({left: number, top: number}). Default is None.
        Can be a `State` object for dynamic updates.
    anchorReference : State or str, optional
        Determines which anchor prop to use ('anchorEl', 'anchorPosition', 'none'). Default is 'anchorEl'.
        Can be a `State` object for dynamic updates.
    children : State, QWidget, List[QWidget], or None, optional
        The content of the popover. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    container : State, QWidget, Callable, or None, optional
        The container element for the popover. Default is None (uses QApplication.instance().mainWindow).
        Can be a `State` object for dynamic updates.
    disableScrollLock : State or bool, optional
        If True, disables scroll lock behavior. Default is False.
        Can be a `State` object for dynamic updates.
    elevation : State or int, optional
        The elevation of the popover (0-24). Default is 8.
        Can be a `State` object for dynamic updates.
    marginThreshold : State or int, optional
        Minimum distance to window edges in pixels. Default is 16.
        Can be a `State` object for dynamic updates.
    onClose : State or Callable, optional
        Callback fired when the popover requests to close. Default is None.
        Can be a `State` object for dynamic updates.
        Signature: (event: Any, reason: str) -> None
    slotProps : State or dict, optional
        Props for slots ({backdrop, paper, root, transition}). Default is {}.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for slots ({backdrop, paper, root, transition}). Default is {}.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    transformOrigin : State or dict, optional
        The point on the popover that attaches to the anchor. Default is {'vertical': 'top', 'horizontal': 'left'}.
        Can be a `State` object for dynamic updates.
    transitionDuration : State, str, int, or dict, optional
        Duration of the transition ('auto', number, or {appear, enter, exit}). Default is 'auto'.
        Can be a `State` object for dynamic updates.
    spacing : State or int, optional
        Spacing between children (in theme.spacing units). Default is 6.
        Can be a `State` object for dynamic updates.
    offset : State or int, optional
        Additional offset from the anchor in pixels. Default is 0.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the Modal component (e.g., keepMounted).

    Signals
    -------
    opened : Signal
        Emitted when the popover is opened.
    closed : Signal
        Emitted when the popover is closed.

    Notes
    -----
    - Existing parameters `parent` and `content` are removed; all other parameters are retained.
    - New parameters added to align with MUI: `action`, `anchorPosition`, `anchorReference`, `classes`,
      `container`, `disableScrollLock`, `elevation`, `marginThreshold`, `slots`, `transitionDuration`.
    - Props of the Modal component are supported via `**kwargs`.
    - MUI classes applied: `MuiPopover-root`, `MuiPopover-paper`.
    - Integrates with `Paper` for content and supports custom backdrop/transition via `slots`.

    Demos:
    - Popover: https://qtmui.com/material-ui/qtmui-popover/

    API Reference:
    - Popover API: https://qtmui.com/material-ui/api/popover/
    """

    opened = Signal()
    closed = Signal()

    VALID_ANCHOR_POSITIONS = ['top', 'center', 'bottom']
    VALID_ANCHOR_HORIZONTALS = ['left', 'center', 'right']
    VALID_ANCHOR_REFERENCES = ['anchorEl', 'anchorPosition', 'none']
    VALID_VARIANTS = ['elevation', 'outlined']
    VALID_ARROWS = [
        'top-left', 'top-center', 'top-right',
        'bottom-left', 'bottom-center', 'bottom-right',
        'left-top', 'left-center', 'left-bottom',
        'right-top', 'right-center', 'right-bottom'
    ]
    # MUI box-shadow spec (simplified for Qt stylesheet)
    SHADOWS = {
        0: "none",
        1: "0px 2px 1px -1px rgba(0,0,0,0.2), 0px 1px 1px 0px rgba(0,0,0,0.14), 0px 1px 3px 0px rgba(0,0,0,0.12)",
        8: "0px 5px 5px -3px rgba(0,0,0,0.2), 0px 8px 10px 1px rgba(0,0,0,0.14), 0px 3px 14px 2px rgba(0,0,0,0.12)",
        24: "0px 11px 15px -7px rgba(0,0,0,0.2), 0px 24px 38px 3px rgba(0,0,0,0.14), 0px 9px 46px 8px rgba(0,0,0,0.12)"
    }

    def __init__(
        self,
        parent=None,
        open: Optional[Union[State, bool]] = False,
        action: Optional[Union[State, PopoverRef]] = None,
        anchorEl: Optional[Union[State, Callable]] = None,
        anchorOrigin: Union[State, Dict] = {'vertical': 'top', 'horizontal': 'left'},
        anchorPosition: Optional[Union[State, Dict]] = None,
        anchorReference: Union[State, str] = 'anchorEl',
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        container: Optional[Union[State, QWidget, Callable]] = None,
        disableScrollLock: Union[State, bool] = False,
        elevation: Union[State, int] = 8,
        marginThreshold: Union[State, int] = 16,
        onClose: Optional[Union[State, Callable]] = None,
        slotProps: Union[State, Dict] = {},
        slots: Union[State, Dict] = {},
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        transformOrigin: Union[State, Dict] = {'vertical': 'top', 'horizontal': 'left'},
        transitionDuration: Union[State, str, int, Dict] = 'auto',
        spacing: Union[State, int] = 6,
        offset: Union[State, int] = 0,
        *args,
        **kwargs
    ):
        super().__init__(parent=parent)
        self.setObjectName(f"Popover-{str(uuid.uuid4())}")
        PyWidgetBase._setUpUi(self)
        
        

        self.theme = useTheme()
        self._widget_references = []
        self._anchorEl_ref = None
        self.is_visible = False

        # Set properties with validation
        self._set_open(open)
        self._set_action(action)
        self._set_anchorEl(anchorEl)
        self._set_anchorOrigin(anchorOrigin)
        self._set_anchorPosition(anchorPosition)
        self._set_anchorReference(anchorReference)
        self._set_children(children)
        self._set_classes(classes)
        self._set_container(container)
        self._set_disableScrollLock(disableScrollLock)
        self._set_elevation(elevation)
        self._set_marginThreshold(marginThreshold)
        self._set_onClose(onClose)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_sx(sx)
        self._set_transformOrigin(transformOrigin)
        self._set_transitionDuration(transitionDuration)
        self._set_spacing(spacing)
        self._set_offset(offset)
        
        self.hide()
        

        # Effective cached dicts (for quick access)
        # We keep original fields as-is (State or dict), and use _get_* helpers to read them.
        self._effective_anchor_origin = None
        self._effective_transform_origin = None

        self._init_ui()


    # Setter and Getter methods
    # @_validate_param(file_path="qtmui.material.popover",param_name="open",supported_signatures=Union[State, bool])
    def _set_open(self, value):
        """Assign value to open."""
        self._open = value

    def _get_open(self):
        """Get the open value."""
        return self._open.value if isinstance(self._open, State) else self._open

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="action",
        supported_signatures=Union[State, PopoverRef, type(None)]
    )
    def _set_action(self, value):
        """Assign value to action."""
        self._action = value or PopoverRef(self)

    def _get_action(self):
        """Get the action value."""
        return self._action.value if isinstance(self._action, State) else self._action

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="anchorEl",
        supported_signatures=Union[State, Callable, type(None)]
    )
    def _set_anchorEl(self, value):
        """Assign value to anchorEl."""
        self._anchorEl = value

    def _get_anchorEl(self):
        """Get the anchorEl value."""
        anchorEl = self._anchorEl
        if isinstance(anchorEl, State):
            anchorEl = anchorEl.value
        if callable(anchorEl):
            try:
                anchorEl = anchorEl()
            except Exception:
                anchorEl = None
        return anchorEl if isinstance(anchorEl, QWidget) else None

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="anchorOrigin",
        supported_signatures=Union[State, Dict],
        validator=lambda x: (
            isinstance(x, dict) and
            x.get('vertical') in Popover.VALID_ANCHOR_POSITIONS + [int, float] and
            x.get('horizontal') in Popover.VALID_ANCHOR_HORIZONTALS + [int, float]
        ) if isinstance(x, dict) else True
    )
    def _set_anchorOrigin(self, value):
        """Assign value to anchorOrigin."""
        self._anchorOrigin = value
        # set effective snapshot if dict
        if not isinstance(value, State) and isinstance(value, dict):
            self._effective_anchor_origin = value.copy()

    def _get_anchorOrigin(self):
        """Get the anchorOrigin value."""
        # Prefer live State value when provided
        if isinstance(self._anchorOrigin, State):
            val = self._anchorOrigin.value
            if isinstance(val, dict):
                # keep snapshot
                self._effective_anchor_origin = val
                return val
            return val
        # fallback to effective snapshot
        return self._effective_anchor_origin or self._anchorOrigin

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="anchorPosition",
        supported_signatures=Union[State, Dict, type(None)],
        validator=lambda x: (
            isinstance(x, dict) and
            isinstance(x.get('left'), (int, float)) and
            isinstance(x.get('top'), (int, float))
        ) if isinstance(x, dict) else True
    )
    def _set_anchorPosition(self, value):
        """Assign value to anchorPosition."""
        self._anchorPosition = value

    def _get_anchorPosition(self):
        """Get the anchorPosition value."""
        return self._anchorPosition.value if isinstance(self._anchorPosition, State) else self._anchorPosition

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="anchorReference",
        supported_signatures=Union[State, str],
        valid_values=VALID_ANCHOR_REFERENCES
    )
    def _set_anchorReference(self, value):
        """Assign value to anchorReference."""
        self._anchorReference = value

    def _get_anchorReference(self):
        """Get the anchorReference value."""
        return self._anchorReference.value if isinstance(self._anchorReference, State) else self._anchorReference

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="children",
        supported_signatures=Union[State, QWidget, List, type(None)]
    )
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        children = self._children.value if isinstance(self._children, State) else self._children
        return children if isinstance(children, list) else [children] if isinstance(children, QWidget) else []

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="classes",
        supported_signatures=Union[State, Dict, type(None)]
    )
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="container",
        supported_signatures=Union[State, QWidget, Callable, type(None)]
    )
    def _set_container(self, value):
        """Assign value to container."""
        self._container = value

    def _get_container(self):
        """Get the container value."""
        container = self._container
        if isinstance(container, State):
            container = container.value
        if callable(container):
            container = container()
        return container if isinstance(container, QWidget) else QApplication.instance().mainWindow

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="disableScrollLock",
        supported_signatures=Union[State, bool]
    )
    def _set_disableScrollLock(self, value):
        """Assign value to disableScrollLock."""
        self._disableScrollLock = value

    def _get_disableScrollLock(self):
        """Get the disableScrollLock value."""
        return self._disableScrollLock.value if isinstance(self._disableScrollLock, State) else self._disableScrollLock

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="elevation",
        supported_signatures=Union[State, int],
        validator=lambda x: 0 <= x <= 24 if isinstance(x, int) else True
    )
    def _set_elevation(self, value):
        """Assign value to elevation."""
        self._elevation = value

    def _get_elevation(self):
        """Get the elevation value."""
        return self._elevation.value if isinstance(self._elevation, State) else self._elevation

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="marginThreshold",
        supported_signatures=Union[State, int],
        validator=lambda x: x >= 0 if isinstance(x, int) else True
    )
    def _set_marginThreshold(self, value):
        """Assign value to marginThreshold."""
        self._marginThreshold = value

    def _get_marginThreshold(self):
        """Get the marginThreshold value."""
        return self._marginThreshold.value if isinstance(self._marginThreshold, State) else self._marginThreshold

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="onClose",
        supported_signatures=Union[State, Callable, type(None)]
    )
    def _set_onClose(self, value):
        """Assign value to onClose."""
        self._onClose = value

    def _get_onClose(self):
        """Get the onClose value."""
        return self._onClose.value if isinstance(self._onClose, State) else self._onClose

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="slotProps",
        supported_signatures=Union[State, Dict]
    )
    def _set_slotProps(self, value):
        """Assign value to slotProps."""
        self._slotProps = value

    def _get_slotProps(self):
        """Get the slotProps value."""
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="slots",
        supported_signatures=Union[State, Dict]
    )
    def _set_slots(self, value):
        """Assign value to slots."""
        self._slots = value

    def _get_slots(self):
        """Get the slots value."""
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="sx",
        supported_signatures=Union[State, List, Dict, Callable, str, type(None)]
    )
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="transformOrigin",
        supported_signatures=Union[State, Dict],
        validator=lambda x: (
            isinstance(x, dict) and
            x.get('vertical') in Popover.VALID_ANCHOR_POSITIONS + [int, float] and
            x.get('horizontal') in Popover.VALID_ANCHOR_HORIZONTALS + [int, float]
        ) if isinstance(x, dict) else True
    )
    def _set_transformOrigin(self, value):
        """Assign value to transformOrigin."""
        self._transformOrigin = value
        if not isinstance(value, State) and isinstance(value, dict):
            self._effective_transform_origin = value.copy()

    def _get_transformOrigin(self):
        """Get the transformOrigin value."""
        if isinstance(self._transformOrigin, State):
            val = self._transformOrigin.value
            if isinstance(val, dict):
                self._effective_transform_origin = val
                return val
            return val
        return self._effective_transform_origin or self._transformOrigin

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="transitionDuration",
        supported_signatures=Union[State, str, int, Dict],
        validator=lambda x: (
            x == 'auto' or
            isinstance(x, (int, float)) or
            (isinstance(x, dict) and all(k in ['appear', 'enter', 'exit'] for k in x))
        ) if not isinstance(x, State) else True
    )
    def _set_transitionDuration(self, value):
        """Assign value to transitionDuration."""
        self._transitionDuration = value

    def _get_transitionDuration(self):
        """Get the transitionDuration value."""
        duration = self._transitionDuration.value if isinstance(self._transitionDuration, State) else self._transitionDuration
        if duration == 'auto':
            return {'appear': 225, 'enter': 225, 'exit': 195}
        if isinstance(duration, (int, float)):
            return {'appear': duration, 'enter': duration, 'exit': duration}
        return duration

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="spacing",
        supported_signatures=Union[State, int],
        validator=lambda x: x >= 0 if isinstance(x, int) else True
    )
    def _set_spacing(self, value):
        """Assign value to spacing."""
        self._spacing = value

    def _get_spacing(self):
        """Get the spacing value."""
        return self._spacing.value if isinstance(self._spacing, State) else self._spacing

    @_validate_param(
        file_path="qtmui.material.popover",
        param_name="offset",
        supported_signatures=Union[State, int]
    )
    def _set_offset(self, value):
        """Assign value to offset."""
        self._offset = value

    def _get_offset(self):
        """Get the offset value."""
        return self._offset.value if isinstance(self._offset, State) else self._offset
    

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        # anchorEl state already connected in _init_ui to _set_anchor_el (kept as original)
        # open state already connected in _init_ui (kept as original)
        if isinstance(self._anchorOrigin, State):
            # State.valueChanged may emit the new value as arg; accept either signature
            try:
                self._anchorOrigin.valueChanged.connect(self._on_anchorOrigin_change)
            except Exception:
                # fallback for different signal signature
                self._anchorOrigin.valueChanged.connect(lambda *_: self._on_anchorOrigin_change())
        if isinstance(self._transformOrigin, State):
            try:
                self._transformOrigin.valueChanged.connect(self._on_transformOrigin_change)
            except Exception:
                self._transformOrigin.valueChanged.connect(lambda *_: self._on_transformOrigin_change())

    def _on_anchorOrigin_change(self, *args):
        """Called when anchorOrigin State changes."""
        # Update effective cache and reposition
        try:
            self._effective_anchor_origin = self._anchorOrigin.value if isinstance(self._anchorOrigin, State) else self._anchorOrigin
        except Exception:
            # if value passed in args
            if args:
                maybe = args[0]
                if isinstance(maybe, dict):
                    self._effective_anchor_origin = maybe
        # self._update_position()

    def _on_transformOrigin_change(self, *args):
        """Called when transformOrigin State changes."""
        try:
            self._effective_transform_origin = self._transformOrigin.value if isinstance(self._transformOrigin, State) else self._transformOrigin
        except Exception:
            if args:
                maybe = args[0]
                if isinstance(maybe, dict):
                    self._effective_transform_origin = maybe
        # self._update_position()
        
    def _init_ui(self):
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowFlag(Qt.Window | Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setParent(QApplication.instance().mainWindow)
        # self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        self.layout().setSpacing(self._spacing)

        self.frame = QFrame(self)
        # self.frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.frame.setObjectName("PyPopover")
        # self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLayout(QVBoxLayout())
        # self.frame.layout().setContentsMargins(0,0,0,0)

        if self._children:
            for widget in self._children:
                if widget is not None:
                    self.frame.layout().addWidget(widget)

        self.layout().addWidget(self.frame)

        # connect dynamic state signals
        # anchorEl: when anchor element changes, reposition
        if isinstance(self._anchorEl, State):
            try:
                self._anchorEl.valueChanged.connect(self._set_anchor_el)
            except Exception:
                self._anchorEl.valueChanged.connect(lambda value: self._set_anchor_el(anchorEl=value))
            if self._anchorEl.value:
                self._set_anchor_el(anchorEl=self._anchorEl.value)

        # anchorOrigin / transformOrigin state connections
        self._connect_signals()

        # open state (must be State according to original code expectation)
        if self._open:
            if not isinstance(self._open, State):
                raise TypeError("open must be type (State)")
            try:
                self._open.valueChanged.connect(self._set_visible)
            except Exception:
                self._open.valueChanged.connect(lambda v: self._set_visible(v))

        # self.hide()

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        # preserve original destroyed hook if exists in base class
        try:
            self.destroyed.connect(self._on_destroyed)
        except Exception:
            # _on_destroyed may be provided by PyWidgetBase or not; ignore if missing
            pass
        
        QApplication.instance().installEventFilter(self)
        

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _set_visible(self, open):
        print('opennnnnnnnnnnnnnnnnnnn', open)
        if open:
            self.show()
            self.setVisible(True)
            self.is_visible = True
            # reposition when opened
            self._update_position()
            try:
                self.opened.emit()
            except Exception:
                pass
        else:
            self.hide()
            self.is_visible = False
            # call onClose callback if provided
            try:
                oc = self._get_onClose()
                if callable(oc):
                    oc()
            except Exception:
                pass
            try:
                self.closed.emit()
            except Exception:
                pass


    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        PyPopover = component_styled[f"PyPopover"].get("styles")
        PyPopover_root_qss = get_qss_style(PyPopover["root"])

        # self.setStyleSheet(f"#{self.objectName()} {{background-color: tranparent;}}")

        # print('PyPopover_root_qss__________', PyPopover_root_qss)
        self.adjustSize()

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx


        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {PyPopover_root_qss}
                }}

                {sx_qss}
            """
        )
        
        self._setShadowEffect()

    def _setShadowEffect(self, blurRadius=60, offset=(0, 10), color=QColor(0, 0, 0, 100)):
        """ add shadow to dialog """
        # SET DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)

        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)

    def _set_anchor_el(self, anchorEl:QWidget=None):
        print('_set_anchor_el', anchorEl)
        if isinstance(anchorEl, QWidget):
            # self._anchorEl = anchorEl
            # self.__anchorEl = anchorEl
            self.__anchorEl = ref(anchorEl)
            self.installEventFilter(anchorEl)

            self.setParent(QApplication.instance().mainWindow)
            self.window().raise_()

            global_point = anchorEl.mapToGlobal(QPoint(0, anchorEl.height()))
            new_pos = self.parent().mapFromGlobal(global_point)
            
            anchor_rect = anchorEl.geometry()
            pos = self.calculate_position(new_pos, anchor_rect)
            self.move(pos)
            # self.setFixedWidth(200)
            # self.setFixedHeight(100)

            self.show()
            self.setVisible(True)
            self.is_visible = True
            # QApplication.instance().installEventFilter(self)
        else:
            # if anchorEl is None (or not QWidget) just hide or do nothing
            # keep original behavior: hide
            self.hide()
            self.is_visible = False


    def calculate_position(self, anchor_pos, anchor_rect):
        # Calculate anchor origin point
        # anchor_pos is local point in parent coordinate (as used earlier)
        y_anchor = self.get_anchor_vertical(anchor_pos, anchor_rect)
        x_anchor = self.get_anchor_horizontal(anchor_pos, anchor_rect)
        
        # print("checkkkkkkkkkkkk", self._anchorOrigin)
        
        tooltip_size = self.sizeHint()

        # Calculate transform origin point
        y_transform = self.get_transform_vertical(tooltip_size)
        x_transform = self.get_transform_horizontal(tooltip_size)

        x = x_anchor - x_transform
        y = y_anchor - y_transform

        return QPoint(x, y)

    def get_anchor_vertical(self, anchor_pos, anchor_rect):
        origin = self._get_anchorOrigin() or {'vertical': 'top'}
        if origin.get('vertical') == 'bottom':
            return anchor_pos.y() + self._get_offset()
        elif origin.get('vertical') == 'center':
            return anchor_pos.y() - anchor_rect.height() // 2
        else:  # 'top'
            return anchor_pos.y() - anchor_rect.height()

    def get_anchor_horizontal(self, anchor_pos, anchor_rect):
        origin = self._get_anchorOrigin() or {'horizontal': 'left'}
        if origin.get('horizontal') == 'left':
            return anchor_pos.x()
        elif origin.get('horizontal') == 'center':
            return anchor_pos.x() + anchor_rect.width() // 2
        else:  # 'right'
            return anchor_pos.x() + anchor_rect.width()

    def get_transform_vertical(self, tooltip_size):
        transform = self._get_transformOrigin() or {'vertical': 'top'}
        if transform.get('vertical') == 'top':
            return 0
        elif transform.get('vertical') == 'center':
            return tooltip_size.height() // 2
        else:  # 'bottom'
            return tooltip_size.height()

    def get_transform_horizontal(self, tooltip_size):
        transform = self._get_transformOrigin() or {'horizontal': 'left'}
        if transform.get('horizontal') == 'left':
            return 0
        elif transform.get('horizontal') == 'center':
            return tooltip_size.width() // 2
        else:  # 'right'
            return tooltip_size.width()

    def _update_position(self):
        """
        Recalculate position from either anchorEl (preferred) or anchorPosition.
        This is the method PopoverRef.updatePosition() calls.
        """
        try:
            anchorEl = self._get_anchorEl()
            if anchorEl and isinstance(anchorEl, QWidget):
                # compute local anchor base point relative to parent
                global_point = anchorEl.mapToGlobal(QPoint(0, anchorEl.height()))
                parent_widget = self.parent() or QApplication.instance().mainWindow
                new_pos = parent_widget.mapFromGlobal(global_point)
                anchor_rect = anchorEl.geometry()
                pos = self.calculate_position(new_pos, anchor_rect)
                self.move(pos)
                return
            # fallback to anchorPosition dict
            anchor_pos = self._get_anchorPosition()
            if isinstance(anchor_pos, dict):
                left = int(anchor_pos.get('left', 0))
                top = int(anchor_pos.get('top', 0))
                self.move(QPoint(left, top))
        except Exception:
            # swallow errors to avoid crashing callers
            pass

    def hideTooltip(self):
        if self.is_visible:
            self.hide()
            self.is_visible = False

    def enterEvent(self, event):
        if self._slotProps:
            try:
                self._slotProps.get('paper').get("onMouseEnter")()
            except Exception:
                pass
            self.show()
        event.accept()

    def _check_until_ppv_under_mouse(self):
        if not self.underMouse():
            self.hide()
            self.is_visible = False

    def leaveEvent(self, event):
        if self._slotProps:
            try:
                self._slotProps.get('paper').get("onMouseLeave")()
            except Exception:
                pass
        event.accept()

    def check_cursor(self):
        if not self.underMouse():
            self.hideTooltip()

    def hideEvent(self, event):
        print('hide_event___________')
        # if isinstance(self._open, State):
        #     self._open.set_value(False)
        if isinstance(self._anchorEl, State):
            self._anchorEl.set_value(None)
        return super().hideEvent(event)

    def eventFilter(self, obj, event):
        # Kiểm tra nếu người dùng click ra ngoài popover
        # print(event.type())
        # if hasattr(self, '_anchorEl') and obj == self._anchorEl:#  and event.type() == QEvent.Type.Destroy: # event.type() == QEvent.Type.Destroy:
        if event.type() == QEvent.Type.Wheel: # event.type() == QEvent.Type.Destroy:
            self.hide()
            self.is_visible = False
        if event.type() == QEvent.Type.MouseButtonPress:
            if self.is_visible:
                anchorEl = getattr(self, "__anchorEl", None)
                anchor_widget = anchorEl() if callable(anchorEl) else anchorEl
                if anchor_widget and isinstance(anchor_widget, QWidget):
                    if not self.geometry().contains(QCursor.pos()) and not anchor_widget.underMouse():
                        self.hide()
                        self.is_visible = False
                elif not self.underMouse() and self.isVisible():
                    QTimer.singleShot(200, lambda: self._set_visible(False))
                elif not self.underMouse():
                    self.hide()
                    self.is_visible = False
        return super().eventFilter(obj, event)
