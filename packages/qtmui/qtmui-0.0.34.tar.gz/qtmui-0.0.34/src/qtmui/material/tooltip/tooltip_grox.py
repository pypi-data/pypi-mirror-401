# # coding:utf-8
# from typing import Callable, Optional, Union, Dict, List
# from enum import Enum
# from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QGraphicsDropShadowEffect, QApplication, QWidget, QSizePolicy
# from PyQt5.QtCore import QTimer, Qt, QPoint, QRect, QEvent, QObject, QPropertyAnimation
# from PyQt5.QtGui import QColor, QCursor
# from qtmui.hooks.use_theme import useTheme
# from qtmui.hooks import State
# from ...utils.validate_params import _validate_param
# from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
# from qtmui.i18n.use_translation import translate, i18n
# from ...components.typography import Typography

# def getCurrentScreenGeometry(available=True):
#     """Get current screen geometry."""
#     cursorPos = QCursor.pos()
#     for s in QApplication.screens():
#         if s.geometry().contains(cursorPos):
#             return s.availableGeometry() if available else s.geometry()
#     return QRect(0, 0, 1920, 1080)

# class ToolTipLabel(QLabel):
#     """Label for displaying tooltip content."""
#     def __init__(self, parent: Optional[QWidget]=None, text: str="", maxWidth: float=300):
#         super().__init__(parent=parent)
#         self._text = text
#         self._maxWidth = maxWidth
#         self._init_ui()

#     def _init_ui(self):
#         self.setWindowFlag(Qt.FramelessWindowHint)
#         self.setTextInteractionFlags(Qt.TextSelectableByMouse)
#         self.setObjectName("label_tooltip")
#         self.setMinimumHeight(34)
#         self.setMaximumWidth(self._maxWidth)
#         self.setWordWrap(True)
#         self.setText(self._text)
#         self.adjustSize()

#         self.shadow = QGraphicsDropShadowEffect(self)
#         self.shadow.setBlurRadius(30)
#         self.shadow.setXOffset(0)
#         self.shadow.setYOffset(0)
#         self.shadow.setColor(QColor(0, 0, 0, 80))
#         self.setGraphicsEffect(self.shadow)

#         self.theme = useTheme()
#         self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
#         i18n.langChanged.connect(self.reTranslation)
#         self._set_stylesheet()
#         self.destroyed.connect(self._on_destroyed)

#     def _on_destroyed(self):
#         self.theme.state.valueChanged.disconnect(self._set_stylesheet)
#         i18n.langChanged.disconnect(self.reTranslation)

#     def reTranslation(self):
#         self.setText(translate(self._text) if isinstance(self._text, (str, Callable)) else self._text)
#         self.adjustSize()

#     def _set_stylesheet(self):
#         tooltip_styles = self.theme.components.get("Tooltip", {}).get("styles", {}).get("tooltip", {})
#         qss = get_qss_style(tooltip_styles)
#         self.setStyleSheet(f"QLabel {{ {qss} }}")

# class ToolTipPosition(Enum):
#     """Tooltip position enum."""
#     TOP = 0
#     BOTTOM = 1
#     LEFT = 2
#     RIGHT = 3
#     TOP_LEFT = 4
#     TOP_RIGHT = 5
#     BOTTOM_LEFT = 6
#     BOTTOM_RIGHT = 7
#     LEFT_TOP = 8
#     LEFT_BOTTOM = 9
#     RIGHT_TOP = 10
#     RIGHT_BOTTOM = 11

# class ToolTipPositionManager:
#     """Tooltip position manager."""
#     def position(self, tooltip: 'ToolTip', parent: QWidget) -> QPoint:
#         pos = self._pos(tooltip, parent)
#         rect = getCurrentScreenGeometry()
#         x = max(rect.left(), min(pos.x(), rect.right() - tooltip.width() - 4))
#         y = max(rect.top(), min(pos.y(), rect.bottom() - tooltip.height() - 4))
#         return QPoint(x, y)

#     def _pos(self, tooltip: 'ToolTip', parent: QWidget) -> QPoint:
#         raise NotImplementedError

#     @staticmethod
#     def make(position: ToolTipPosition):
#         managers = {
#             ToolTipPosition.TOP: TopToolTipManager,
#             ToolTipPosition.BOTTOM: BottomToolTipManager,
#             ToolTipPosition.LEFT: LeftToolTipManager,
#             ToolTipPosition.RIGHT: RightToolTipManager,
#             ToolTipPosition.TOP_LEFT: TopLeftToolTipManager,
#             ToolTipPosition.TOP_RIGHT: TopRightToolTipManager,
#             ToolTipPosition.BOTTOM_LEFT: BottomLeftToolTipManager,
#             ToolTipPosition.BOTTOM_RIGHT: BottomRightToolTipManager,
#             ToolTipPosition.LEFT_TOP: LeftTopToolTipManager,
#             ToolTipPosition.LEFT_BOTTOM: LeftBottomToolTipManager,
#             ToolTipPosition.RIGHT_TOP: RightTopToolTipManager,
#             ToolTipPosition.RIGHT_BOTTOM: RightBottomToolTipManager,
#         }
#         return managers[position]()

# class TopToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() + parent.width() // 2 - tooltip.width() // 2
#         y = pos.y() - tooltip.height() - (10 if tooltip._get_arrow() else 0)
#         return QPoint(x, y)

# class BottomToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() + parent.width() // 2 - tooltip.width() // 2
#         y = pos.y() + parent.height() + (10 if tooltip._get_arrow() else 0)
#         return QPoint(x, y)

# class LeftToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() - tooltip.width() - (10 if tooltip._get_arrow() else 0)
#         y = pos.y() + (parent.height() - tooltip.height()) // 2
#         return QPoint(x, y)

# class RightToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() + parent.width() + (10 if tooltip._get_arrow() else 0)
#         y = pos.y() + (parent.height() - tooltip.height()) // 2
#         return QPoint(x, y)

# class TopLeftToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() - tooltip.layout().contentsMargins().left()
#         y = pos.y() - tooltip.height() - (10 if tooltip._get_arrow() else 0)
#         return QPoint(x, y)

# class TopRightToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() + parent.width() - tooltip.width() + tooltip.layout().contentsMargins().right()
#         y = pos.y() - tooltip.height() - (10 if tooltip._get_arrow() else 0)
#         return QPoint(x, y)

# class BottomLeftToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() - tooltip.layout().contentsMargins().left()
#         y = pos.y() + parent.height() + (10 if tooltip._get_arrow() else 0)
#         return QPoint(x, y)

# class BottomRightToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() + parent.width() - tooltip.width() + tooltip.layout().contentsMargins().right()
#         y = pos.y() + parent.height() + (10 if tooltip._get_arrow() else 0)
#         return QPoint(x, y)

# class LeftTopToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() - tooltip.width() - (10 if tooltip._get_arrow() else 0)
#         y = pos.y()
#         return QPoint(x, y)

# class LeftBottomToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() - tooltip.width() - (10 if tooltip._get_arrow() else 0)
#         y = pos.y() + parent.height() - tooltip.height()
#         return QPoint(x, y)

# class RightTopToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() + parent.width() + (10 if tooltip._get_arrow() else 0)
#         y = pos.y()
#         return QPoint(x, y)

# class RightBottomToolTipManager(ToolTipPositionManager):
#     def _pos(self, tooltip: 'ToolTip', parent: QWidget):
#         pos = parent.mapToGlobal(QPoint())
#         x = pos.x() + parent.width() + (10 if tooltip._get_arrow() else 0)
#         y = pos.y() + parent.height() - tooltip.height()
#         return QPoint(x, y)

# class ToolTip(QFrame):
#     """
#     A tooltip component, styled like Material-UI Tooltip.

#     The `Tooltip` component displays a tooltip with customizable content, position, and behavior,
#     aligning with MUI Tooltip props. Inherits from native component props.

#     Parameters
#     ----------
#     title : State, str, QWidget, or None, optional
#         Content of the tooltip. Default is ''.
#         Can be a `State` object for dynamic updates.
#     parent : State, QWidget, or None, optional
#         Parent widget. Default is None.
#         Can be a `State` object for dynamic updates.
#     children : State, QWidget, or None, optional
#         Reference element for the tooltip (required in MUI). Default is None.
#         Can be a `State` object for dynamic updates.
#     arrow : State or bool, optional
#         If True, adds an arrow to the tooltip. Default is False.
#         Can be a `State` object for dynamic updates.
#     classes : State or Dict, optional
#         Override or extend styles. Default is None.
#         Can be a `State` object for dynamic updates.
#     components : State or Dict, optional
#         Components for slots (Arrow, Popper, Tooltip, Transition, deprecated). Default is None.
#         Can be a `State` object for dynamic updates.
#     componentsProps : State or Dict, optional
#         Props for slot components (deprecated). Default is None.
#         Can be a `State` object for dynamic updates.
#     describeChild : State or bool, optional
#         If True, title is an accessible description. Default is False.
#         Can be a `State` object for dynamic updates.
#     disableFocusListener : State or bool, optional
#         If True, ignores focus events. Default is False.
#         Can be a `State` object for dynamic updates.
#     disableHoverListener : State or bool, optional
#         If True, ignores hover events. Default is False.
#         Can be a `State` object for dynamic updates.
#     disableInteractive : State or bool, optional
#         If True, tooltip is non-interactive. Default is False.
#         Can be a `State` object for dynamic updates.
#     disableTouchListener : State or bool, optional
#         If True, ignores touch events. Default is False.
#         Can be a `State` object for dynamic updates.
#     enterDelay : State or int, optional
#         Delay before showing tooltip (ms). Default is 100.
#         Can be a `State` object for dynamic updates.
#     enterNextDelay : State or int, optional
#         Delay for next tooltip after one closes (ms). Default is 0.
#         Can be a `State` object for dynamic updates.
#     enterTouchDelay : State or int, optional
#         Delay for touch to show tooltip (ms). Default is 700.
#         Can be a `State` object for dynamic updates.
#     followCursor : State or bool, optional
#         If True, tooltip follows cursor. Default is False.
#         Can be a `State` object for dynamic updates.
#     id : State, str, or None, optional
#         ID for accessibility. Default is None.
#         Can be a `State` object for dynamic updates.
#     leaveDelay : State or int, optional
#         Delay before hiding tooltip (ms). Default is 0.
#         Can be a `State` object for dynamic updates.
#     leaveTouchDelay : State or int, optional
#         Delay after touch ends to hide tooltip (ms). Default is 1500.
#         Can be a `State` object for dynamic updates.
#     onClose : State, Callable, or None, optional
#         Callback when tooltip closes. Default is None.
#         Can be a `State` object for dynamic updates.
#     onOpen : State, Callable, or None, optional
#         Callback when tooltip opens. Default is None.
#         Can be a `State` object for dynamic updates.
#     open : State or bool, optional
#         If True, tooltip is shown. Default is False.
#         Can be a `State` object for dynamic updates.
#     placement : State, str, or None, optional
#         Tooltip placement. Default is 'bottom'.
#         Can be a `State` object for dynamic updates.
#     PopperComponent : State, str, or None, optional
#         Component for popper (deprecated). Default is None.
#         Can be a `State` object for dynamic updates.
#     PopperProps : State or Dict, optional
#         Props for popper (deprecated). Default is None.
#         Can be a `State` object for dynamic updates.
#     slotProps : State or Dict, optional
#         Props for slots (arrow, popper, tooltip, transition). Default is None.
#         Can be a `State` object for dynamic updates.
#     slots : State or Dict, optional
#         Components for slots (arrow, popper, tooltip, transition). Default is None.
#         Can be a `State` object for dynamic updates.
#     sx : State, List, Dict, Callable, or None, optional
#         System prop for CSS overrides. Default is None.
#         Can be a `State` object for dynamic updates.
#     TransitionComponent : State, str, or None, optional
#         Component for transition (deprecated). Default is None.
#         Can be a `State` object for dynamic updates.
#     TransitionProps : State or Dict, optional
#         Props for transition (deprecated). Default is None.
#         Can be a `State` object for dynamic updates.
#     **kwargs
#         Additional keyword arguments passed to QFrame, supporting native props.

#     Notes
#     -----
#     - `components`, `componentsProps`, `PopperComponent`, `PopperProps`, `TransitionComponent`, `TransitionProps` are deprecated; use `slotProps` and `slots`.
#     - Supports dynamic updates via State objects.
#     - MUI classes applied: `MuiTooltip-root`.

#     Demos:
#     - Tooltip: https://qtmui.com/material-ui/qtmui-tooltip/

#     API Reference:
#     - Tooltip API: https://qtmui.com/material-ui/api/tooltip/
#     """

#     VALID_PLACEMENTS = [
#         'auto-end', 'auto-start', 'auto', 'bottom-end', 'bottom-start', 'bottom',
#         'left-end', 'left-start', 'left', 'right-end', 'right-start', 'right',
#         'top-end', 'top-start', 'top'
#     ]

#     def __init__(
#         self,
#         title: Union[State, str, QWidget, type(None)]='',
#         parent: Union[State, QWidget, type(None)]=None,
#         children: Union[State, QWidget, type(None)]=None,
#         arrow: Union[State, bool]=False,
#         classes: Optional[Union[State, Dict, type(None)]=None,
#         components: Optional[Union[State, Dict, type(None)]=None,
#         componentsProps: Optional[Union[State, Dict, type(None)]=None,
#         describeChild: Union[State, bool]=False,
#         disableFocusListener: Union[State, bool]=False,
#         disableHoverListener: Union[State, bool]=False,
#         disableInteractive: Union[State, bool]=False,
#         disableTouchListener: Union[State, bool]=False,
#         enterDelay: Union[State, int]=100,
#         enterNextDelay: Union[State, int]=0,
#         enterTouchDelay: Union[State, int]=700,
#         followCursor: Union[State, bool]=False,
#         id: Optional[Union[State, str, type(None)]=None,
#         leaveDelay: Union[State, int]=0,
#         leaveTouchDelay: Union[State, int]=1500,
#         onClose: Optional[Union[State, Callable, type(None)]=None,
#         onOpen: Optional[Union[State, Callable, type(None)]=None,
#         open: Union[State, bool]=False,
#         placement: Optional[Union[State, str, type(None)]='bottom',
#         PopperComponent: Optional[Union[State, str, type(None)]=None,
#         PopperProps: Optional[Union[State, Dict, type(None)]=None,
#         slotProps: Optional[Union[State, Dict, type(None)]=None,
#         slots: Optional[Union[State, Dict, type(None)]=None,
#         sx: Optional[Union[State, List, Dict, Callable, type(None)]=None,
#         TransitionComponent: Optional[Union[State, str, type(None)]=None,
#         TransitionProps: Optional[Union[State, Dict, type(None)]=None,
#         **kwargs
#     ):
#         super().__init__(parent=parent, **kwargs)
#         self.theme = useTheme()
#         self._widget_references = []
#         self.setObjectName(str(id(self)))

#         # Set properties with validation
#         self._set_title(title)
#         self._set_parent(parent)
#         self._set_children(children)
#         self._set_arrow(arrow)
#         self._set_classes(classes)
#         self._set_components(components)
#         self._set_componentsProps(componentsProps)
#         self._set_describeChild(describeChild)
#         self._set_disableFocusListener(disableFocusListener)
#         self._set_disableHoverListener(disableHoverListener)
#         self._set_disableInteractive(disableInteractive)
#         self._set_disableTouchListener(disableTouchListener)
#         self._set_enterDelay(enterDelay)
#         self._set_enterNextDelay(enterNextDelay)
#         self._set_enterTouchDelay(enterTouchDelay)
#         self._set_followCursor(followCursor)
#         self._set_id(id)
#         self._set_leaveDelay(leaveDelay)
#         self._set_leaveTouchDelay(leaveTouchDelay)
#         self._set_onClose(onClose)
#         self._set_onOpen(onOpen)
#         self._set_open(open)
#         self._set_placement(placement)
#         self._set_PopperComponent(PopperComponent)
#         self._set_PopperProps(PopperProps)
#         self._set_slotProps(slotProps)
#         self._set_slots(slots)
#         self._set_sx(sx)
#         self._set_TransitionComponent(TransitionComponent)
#         self._set_TransitionProps(TransitionProps)

#         self._init_ui()
#         self._set_stylesheet()
#         self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
#         self.destroyed.connect(self._on_destroyed)

#     # Setter and Getter methods
#     @_validate_param(file_path="qtmui.material.tooltip", param_name="title", supported_signatures=Union[State, str, QWidget, type(None)])
#     def _set_title(self, value):
#         self._title = value
#         if isinstance(value, QWidget):
#             self._widget_references.append(value)
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_title(self):
#         return self._title.value if isinstance(self._title, State) else self._title

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="parent", supported_signatures=Union[State, QWidget, type(None)])
#     def _set_parent(self, value):
#         self._parent = value
#         if isinstance(value, QWidget):
#             self._widget_references.append(value)
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_parent(self):
#         return self._parent.value if isinstance(self._parent, State) else self._parent

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="children", supported_signatures=Union[State, QWidget, type(None)])
#     def _set_children(self, value):
#         self._children = value
#         if isinstance(value, QWidget):
#             self._widget_references.append(value)
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_children(self):
#         return self._children.value if isinstance(self._children, State) else self._children

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="arrow", supported_signatures=Union[State, bool])
#     def _set_arrow(self, value):
#         self._arrow = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_arrow(self):
#         return self._arrow.value if isinstance(self._arrow, State) else self._arrow

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
#     def _set_classes(self, value):
#         self._classes = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self._set_stylesheet)

#     def _get_classes(self):
#         return self._classes.value if isinstance(self._classes, State) else self._classes

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="components", supported_signatures=Union[State, Dict, type(None)])
#     def _set_components(self, value):
#         self._components = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_components(self):
#         return self._components.value if isinstance(self._components, State) else self._components

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="componentsProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_componentsProps(self, value):
#         self._componentsProps = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_componentsProps(self):
#         return self._componentsProps.value if isinstance(self._componentsProps, State) else self._componentsProps

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="describeChild", supported_signatures=Union[State, bool])
#     def _set_describeChild(self, value):
#         self._describeChild = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_describeChild(self):
#         return self._describeChild.value if isinstance(self._describeChild, State) else self._describeChild

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="disableFocusListener", supported_signatures=Union[State, bool])
#     def _set_disableFocusListener(self, value):
#         self._disableFocusListener = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_disableFocusListener(self):
#         return self._disableFocusListener.value if isinstance(self._disableFocusListener, State) else self._disableFocusListener

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="disableHoverListener", supported_signatures=Union[State, bool])
#     def _set_disableHoverListener(self, value):
#         self._disableHoverListener = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_disableHoverListener(self):
#         return self._disableHoverListener.value if isinstance(self._disableHoverListener, State) else self._disableHoverListener

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="disableInteractive", supported_signatures=Union[State, bool])
#     def _set_disableInteractive(self, value):
#         self._disableInteractive = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_disableInteractive(self):
#         return self._disableInteractive.value if isinstance(self._disableInteractive, State) else self._disableInteractive

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="disableTouchListener", supported_signatures=Union[State, bool])
#     def _set_disableTouchListener(self, value):
#         self._disableTouchListener = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_disableTouchListener(self):
#         return self._disableTouchListener.value if isinstance(self._disableTouchListener, State) else self._disableTouchListener

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="enterDelay", supported_signatures=Union[State, int])
#     def _set_enterDelay(self, value):
#         self._enterDelay = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_enterDelay(self):
#         return self._enterDelay.value if isinstance(self._enterDelay, State) else self._enterDelay

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="enterNextDelay", supported_signatures=Union[State, int])
#     def _set_enterNextDelay(self, value):
#         self._enterNextDelay = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_enterNextDelay(self):
#         return self._enterNextDelay.value if isinstance(self._enterNextDelay, State) else self._enterNextDelay

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="enterTouchDelay", supported_signatures=Union[State, int])
#     def _set_enterTouchDelay(self, value):
#         self._enterTouchDelay = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_enterTouchDelay(self):
#         return self._enterTouchDelay.value if isinstance(self._enterTouchDelay, State) else self._enterTouchDelay

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="followCursor", supported_signatures=Union[State, bool])
#     def _set_followCursor(self, value):
#         self._followCursor = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_followCursor(self):
#         return self._followCursor.value if isinstance(self._followCursor, State) else self._followCursor

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="id", supported_signatures=Union[State, str, type(None)])
#     def _set_id(self, value):
#         self._id = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_id(self):
#         return self._id.value if isinstance(self._id, State) else self._id

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="leaveDelay", supported_signatures=Union[State, int])
#     def _set_leaveDelay(self, value):
#         self._leaveDelay = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_leaveDelay(self):
#         return self._leaveDelay.value if isinstance(self._leaveDelay, State) else self._leaveDelay

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="leaveTouchDelay", supported_signatures=Union[State, int])
#     def _set_leaveTouchDelay(self, value):
#         self._leaveTouchDelay = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_leaveTouchDelay(self):
#         return self._leaveTouchDelay.value if isinstance(self._leaveTouchDelay, State) else self._leaveTouchDelay

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="onClose", supported_signatures=Union[State, Callable, type(None)])
#     def _set_onClose(self, value):
#         self._onClose = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_onClose(self):
#         return self._onClose.value if isinstance(self._onClose, State) else self._onClose

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="onOpen", supported_signatures=Union[State, Callable, type(None)])
#     def _set_onOpen(self, value):
#         self._onOpen = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_onOpen(self):
#         return self._onOpen.value if isinstance(self._onOpen, State) else self._onOpen

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="open", supported_signatures=Union[State, bool])
#     def _set_open(self, value):
#         self._open = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_open(self):
#         return self._open.value if isinstance(self._open, State) else self._open

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="placement", supported_signatures=Union[State, str, type(None)], valid_values=VALID_PLACEMENTS)
#     def _set_placement(self, value):
#         self._placement = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_placement(self):
#         placement = self._placement.value if isinstance(self._placement, State) else self._placement
#         return placement if placement in self.VALID_PLACEMENTS else 'bottom'

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="PopperComponent", supported_signatures=Union[State, str, type(None)])
#     def _set_PopperComponent(self, value):
#         self._PopperComponent = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_PopperComponent(self):
#         return self._PopperComponent.value if isinstance(self._PopperComponent, State) else self._PopperComponent

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="PopperProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_PopperProps(self, value):
#         self._PopperProps = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_PopperProps(self):
#         return self._PopperProps.value if isinstance(self._PopperProps, State) else self._PopperProps

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_slotProps(self, value):
#         self._slotProps = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_slotProps(self):
#         return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
#     def _set_slots(self, value):
#         self._slots = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_slots(self):
#         return self._slots.value if isinstance(self._slots, State) else self._slots

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, type(None)])
#     def _set_sx(self, value):
#         self._sx = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self._set_stylesheet)

#     def _get_sx(self):
#         return self._sx.value if isinstance(self._sx, State) else self._sx

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="TransitionComponent", supported_signatures=Union[State, str, type(None)])
#     def _set_TransitionComponent(self, value):
#         self._TransitionComponent = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_TransitionComponent(self):
#         return self._TransitionComponent.value if isinstance(self._TransitionComponent, State) else self._TransitionComponent

#     @_validate_param(file_path="qtmui.material.tooltip", param_name="TransitionProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_TransitionProps(self, value):
#         self._TransitionProps = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self.update_ui)

#     def _get_TransitionProps(self):
#         return self._TransitionProps.value if isinstance(self._TransitionProps, State) else self._TransitionProps

#     def _init_ui(self):
#         # Clear existing layout
#         if self.layout():
#             while self.layout().count():
#                 item = self.layout().takeAt(0)
#                 if item.widget():
#                     item.widget().deleteLater()

#         # Initialize layout
#         self.setLayout(QHBoxLayout())
#         self.layout().setContentsMargins(8, 6, 8, 6)
#         self.container = QFrame(self)
#         self.containerLayout = QHBoxLayout(self.container)
#         self.containerLayout.setContentsMargins(0, 0, 0, 0)
#         self.layout().addWidget(self.container)

#         # Initialize title
#         title = self._get_title()
#         if isinstance(title, str) and title:
#             self.label = ToolTipLabel(self, text=title)
#             self.containerLayout.addWidget(self.label)
#             self._widget_references.append(self.label)
#         elif isinstance(title, QWidget):
#             self.label = title
#             self.label.setParent(self.container)
#             self.containerLayout.addWidget(self.label)
#         else:
#             self.label = None

#         # Initialize arrow
#         if self._get_arrow():
#             self.arrow_widget = QWidget(self)
#             self.arrow_widget.setFixedSize(10, 10)
#             self.arrow_widget.setObjectName("arrow")
#             self.layout().addWidget(self.arrow_widget)
#             self._widget_references.append(self.arrow_widget)

#         # Set attributes
#         self.setAttribute(Qt.WA_TransparentForMouseEvents, self._get_disableInteractive())
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

#         # Initialize opacity animation
#         self.opacityAni = QPropertyAnimation(self, b'windowOpacity', self)
#         self.opacityAni.setDuration(150)

#         # Initialize timer
#         self.timer = QTimer(self)
#         self.timer.setSingleShot(True)
#         self.timer.timeout.connect(self.hide)

#         # Install event filter on children
#         children = self._get_children()
#         if isinstance(children, QWidget):
#             self.filter = ToolTipFilter(children, self)
#             children.installEventFilter(self.filter)
#             self._widget_references.append(children)

#         # Set open state
#         if self._get_open():
#             self.show()

#     def _set_stylesheet(self):
#         tooltip_styles = self.theme.components.get("Tooltip", {}).get("styles", {})
#         root_qss = get_qss_style(tooltip_styles.get("root", {}))

#         # Handle classes
#         classes = self._get_classes() or {}
#         classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}")

#         # Handle sx
#         sx = self._get_sx()
#         sx_qss = ""
#         if sx:
#             if isinstance(sx, (list, dict)):
#                 sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
#             elif isinstance(sx, Callable):
#                 sx_result = sx()
#                 if isinstance(sx_result, (list, dict)):
#                     sx_qss = get_qss_style(sx_result, class_name=f"#{self.objectName()}")
#                 elif isinstance(sx_result, str):
#                     sx_qss = sx_result
#             elif isinstance(sx, str) and sx != "":
#                 sx_qss = sx

#         # Arrow style
#         arrow_qss = ""
#         if self._get_arrow():
#             placement = self._get_placement()
#             arrow_style = {
#                 "bottom": "border-bottom: 5px solid transparent; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 5px solid black;",
#                 "top": "border-top: 5px solid transparent; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 5px solid black;",
#                 "left": "border-left: 5px solid transparent; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-right: 5px solid black;",
#                 "right": "border-right: 5px solid transparent; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-left: 5px solid black;"
#             }.get(placement.split('-')[0], "")
#             arrow_qss = f"#{self.objectName()} #arrow {{ {arrow_style} }}"

#         self.setStyleSheet(f"""
#             #{self.objectName()} {{
#                 {root_qss}
#                 {classes_qss}
#             }}
#             {arrow_qss}
#             {sx_qss}
#         """)

#     def showEvent(self, e):
#         if self._get_onOpen():
#             self._get_onOpen()(e)
#         self.opacityAni.setStartValue(0)
#         self.opacityAni.setEndValue(1)
#         self.opacityAni.start()
#         self.timer.stop()
#         if self._get_leaveDelay() > 0:
#             self.timer.start(self._get_leaveDelay() + self.opacityAni.duration())
#         super().showEvent(e)

#     def hideEvent(self, e):
#         if self._get_onClose():
#             self._get_onClose()(e)
#         self.timer.stop()
#         super().hideEvent(e)

#     def adjustPos(self, widget):
#         placement = self._get_placement()
#         position_map = {
#             'top': ToolTipPosition.TOP,
#             'bottom': ToolTipPosition.BOTTOM,
#             'left': ToolTipPosition.LEFT,
#             'right': ToolTipPosition.RIGHT,
#             'top-start': ToolTipPosition.TOP_LEFT,
#             'top-end': ToolTipPosition.TOP_RIGHT,
#             'bottom-start': ToolTipPosition.BOTTOM_LEFT,
#             'bottom-end': ToolTipPosition.BOTTOM_RIGHT,
#             'left-start': ToolTipPosition.LEFT_TOP,
#             'left-end': ToolTipPosition.LEFT_BOTTOM,
#             'right-start': ToolTipPosition.RIGHT_TOP,
#             'right-end': ToolTipPosition.RIGHT_BOTTOM
#         }
#         position = position_map.get(placement, ToolTipPosition.BOTTOM)
#         manager = ToolTipPositionManager.make(position)
#         self.move(manager.position(self, widget))

#     def update_ui(self):
#         self._init_ui()
#         self._set_stylesheet()

#     def _on_destroyed(self):
#         self._widget_references.clear()

#     def setText(self, text: str):
#         self._set_title(text)
#         self.update_ui()

#     def setDuration(self, duration: int):
#         self._set_leaveDelay(duration)
#         self.update_ui()

# class ToolTipFilter(QObject):
#     """Event filter for tooltip interactions."""
#     def __init__(self, parent: QWidget, tooltip: 'ToolTip'):
#         super().__init__(parent=parent)
#         self._parent = parent
#         self._tooltip = tooltip
#         self.isEnter = False
#         self.timer = QTimer(self)
#         self.timer.setSingleShot(True)
#         self.timer.timeout.connect(self.showToolTip)
#         self.lastClosed = 0

#     def eventFilter(self, obj: QObject, e: QEvent) -> bool:
#         if e.type() == QEvent.ToolTip:
#             return True
#         elif e.type() in [QEvent.Hide, QEvent.Leave]:
#             self.hideToolTip()
#         elif e.type() == QEvent.Enter and not self._tooltip._get_disableHoverListener():
#             self.isEnter = True
#             if self._canShowToolTip():
#                 delay = self._tooltip._get_enterDelay()
#                 if self.lastClosed:
#                     delay = max(delay, self._tooltip._get_enterNextDelay())
#                 self.timer.start(delay)
#         elif e.type() == QEvent.MouseButtonPress and not self._tooltip._get_disableTouchListener():
#             self.isEnter = True
#             if self._canShowToolTip():
#                 self.timer.start(self._tooltip._get_enterTouchDelay())
#         elif e.type() == QEvent.FocusIn and not self._tooltip._get_disableFocusListener():
#             self.isEnter = True
#             if self._canShowToolTip():
#                 self.timer.start(self._tooltip._get_enterDelay())
#         elif e.type() == QEvent.MouseMove and self._tooltip._get_followCursor():
#             self.adjustPos(QCursor.pos())

#         return super().eventFilter(obj, e)

#     def showToolTip(self):
#         if not self.isEnter or not self._canShowToolTip():
#             return
#         self._tooltip.adjustPos(self._parent)
#         self._tooltip.show()

#     def hideToolTip(self):
#         self.isEnter = False
#         self.timer.stop()
#         self._tooltip.hide()
#         self.lastClosed = QTimer.singleShot(0, lambda: None).remainingTime()

#     def adjustPos(self, cursor_pos: QPoint):
#         if self._tooltip.isVisible():
#             self._tooltip.move(cursor_pos.x() - self._tooltip.width() // 2, cursor_pos.y() - self._tooltip.height() - 10)

#     def _canShowToolTip(self) -> bool:
#         title = self._tooltip._get_title()
#         return (isinstance(title, str) and title) or isinstance(title, QWidget)