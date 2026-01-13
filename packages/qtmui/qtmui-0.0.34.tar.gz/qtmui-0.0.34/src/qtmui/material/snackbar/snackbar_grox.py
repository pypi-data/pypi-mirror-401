# from typing import Optional, Union, Callable, Any, Dict
# from PyQt5.QtWidgets import QFrame, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QToolButton, QWidget
# from PyQt5.QtCore import Qt, Signal, QTimer, QEvent, QPropertyAnimation, QGraphicsOpacityEffect, QSize
# from PyQt5.QtGui import QPainter, QColor, QPaintEvent
# from qtmui.hooks.use_theme import useTheme, isDarkTheme
# from ...utils.text import TextWrap, translate
# from ...components.iconify import PyIconify
# from ...components.tool_button import PyToolButton
# from ...utils.snackbar_manager import SnackbarManager, SnackbarPosition
# from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
# from ...utils.validate_params import _validate_param
# import uuid

# class Snackbar(QFrame):
#     """
#     A snackbar component, styled like Material-UI Snackbar.

#     The `Snackbar` component displays brief messages at the bottom or top of the screen.
#     It supports customizable positioning, duration, and content, aligning with MUI Snackbar props.
#     Inherits from native component props.

#     Parameters
#     ----------
#     parent : QWidget, optional
#         The parent widget. Default is QApplication.instance().mainWindow or None.
#     color : State or str, optional
#         Color of the snackbar ('default', 'primary', 'secondary', etc.). Default is 'default'.
#         Can be a `State` object for dynamic updates.
#     icon : State, PyIconify, str, or None, optional
#         Icon to display. Default is None.
#         Can be a `State` object for dynamic updates.
#     title : State, str, Callable, or None, optional
#         Title of the snackbar. Default is None.
#         Can be a `State` object for dynamic updates.
#     content : State, str, Callable, or None, optional
#         Content of the snackbar. Default is None.
#         Can be a `State` object for dynamic updates.
#     anchorOrigin : State or Dict, optional
#         Position of the snackbar ({ horizontal: 'left'|'center'|'right', vertical: 'top'|'bottom' }).
#         Default is { vertical: 'bottom', horizontal: 'left' }.
#         Can be a `State` object for dynamic updates.
#     isClosable : State or bool, optional
#         If True, shows a close button. Default is True.
#         Can be a `State` object for dynamic updates.
#     autoHideDuration : State, int, or None, optional
#         Duration in milliseconds before auto-closing. Default is None (disabled).
#         Can be a `State` object for dynamic updates.
#     position : State, int, or str, optional
#         Legacy position (TOP_RIGHT, etc.). Default is SnackbarPosition.TOP_RIGHT.
#         Can be a `State` object for dynamic updates.
#     action : State, QWidget, or None, optional
#         Action widget to display. Default is None.
#         Can be a `State` object for dynamic updates.
#     children : State, QWidget, or None, optional
#         Custom content to replace SnackbarContent. Default is None.
#         Can be a `State` object for dynamic updates.
#     classes : State or Dict, optional
#         Override or extend styles. Default is None.
#         Can be a `State` object for dynamic updates.
#     disableWindowBlurListener : State or bool, optional
#         If True, autoHideDuration timer runs when window is not focused. Default is False.
#         Can be a `State` object for dynamic updates.
#     key : State or Any, optional
#         Unique key for multiple snackbars. Default is None.
#         Can be a `State` object for dynamic updates.
#     message : State, str, Callable, or None, optional
#         Message to display. Default is None.
#         Can be a `State` object for dynamic updates.
#     onClose : State or Callable, optional
#         Callback when snackbar requests to close. Default is None.
#         Can be a `State` object for dynamic updates.
#     open : State or bool, optional
#         If True, snackbar is shown. Default is True.
#         Can be a `State` object for dynamic updates.
#     resumeHideDuration : State, int, or None, optional
#         Duration in milliseconds to dismiss after interaction. Default is None.
#         Can be a `State` object for dynamic updates.
#     slotProps : State or Dict, optional
#         Props for slot components. Default is None.
#         Can be a `State` object for dynamic updates.
#     slots : State or Dict, optional
#         Components for slots. Default is None.
#         Can be a `State` object for dynamic updates.
#     sx : State, List, Dict, Callable, or None, optional
#         System prop for CSS overrides. Default is None.
#         Can be a `State` object for dynamic updates.
#     transitionDuration : State, int, Dict, or None, optional
#         Duration for transition in milliseconds. Default is None (uses theme.transitions).
#         Can be a `State` object for dynamic updates.
#     **kwargs
#         Additional keyword arguments passed to QFrame, supporting native component props.

#     Signals
#     -------
#     closedSignal : Signal()
#         Emitted when the snackbar is closed.

#     Notes
#     -----
#     - Existing parameters (9) are retained; 14 new parameters added to align with MUI Snackbar.
#     - Supports click-away listener and transition effects.
#     - MUI classes applied: `MuiSnackbar-root`.
#     - Integrates with `SnackbarManager` for positioning.

#     Demos:
#     - Snackbar: https://qtmui.com/material-ui/qtmui-snackbar/

#     API Reference:
#     - Snackbar API: https://qtmui.com/material-ui/api/snackbar/
#     """

#     closedSignal = Signal()

#     VALID_COLORS = ['default', 'primary', 'secondary', 'error', 'info', 'success', 'warning']
#     VALID_ANCHOR_HORIZONTAL = ['left', 'center', 'right']
#     VALID_ANCHOR_VERTICAL = ['top', 'bottom']

#     def __init__(
#         self,
#         parent: Optional[QWidget] = None,
#         color: Union[State, str] = "default",
#         icon: Optional[Union[State, PyIconify, str]] = None,
#         title: Optional[Union[State, str, Callable]] = None,
#         content: Optional[Union[State, str, Callable]] = None,
#         anchorOrigin: Union[State, Dict] = {"vertical": "bottom", "horizontal": "left"},
#         isClosable: Union[State, bool] = True,
#         autoHideDuration: Optional[Union[State, int]] = None,
#         position: Union[State, int, str] = SnackbarPosition.TOP_RIGHT,
#         action: Optional[Union[State, QWidget]] = None,
#         children: Optional[Union[State, QWidget]] = None,
#         classes: Optional[Union[State, Dict]] = None,
#         disableWindowBlurListener: Union[State, bool] = False,
#         key: Optional[Union[State, Any]] = None,
#         message: Optional[Union[State, str, Callable]] = None,
#         onClose: Optional[Union[State, Callable]] = None,
#         open: Union[State, bool] = True,
#         resumeHideDuration: Optional[Union[State, int]] = None,
#         slotProps: Optional[Union[State, Dict]] = None,
#         slots: Optional[Union[State, Dict]] = None,
#         sx: Optional[Union[State, List, Dict, Callable]] = None,
#         transitionDuration: Optional[Union[State, int, Dict]] = None,
#         **kwargs
#     ):
#         super().__init__(parent=parent or QApplication.instance().mainWindow, **kwargs)
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.theme = useTheme()
#         self._widget_references = []

#         # Set properties with validation
#         self._set_color(color)
#         self._set_icon(icon)
#         self._set_title(title)
#         self._set_content(content)
#         self._set_anchorOrigin(anchorOrigin)
#         self._set_isClosable(isClosable)
#         self._set_autoHideDuration(autoHideDuration)
#         self._set_position(position)
#         self._set_action(action)
#         self._set_children(children)
#         self._set_classes(classes)
#         self._set_disableWindowBlurListener(disableWindowBlurListener)
#         self._set_key(key)
#         self._set_message(message)
#         self._set_onClose(onClose)
#         self._set_open(open)
#         self._set_resumeHideDuration(resumeHideDuration)
#         self._set_slotProps(slotProps)
#         self._set_slots(slots)
#         self._set_sx(sx)
#         self._set_transitionDuration(transitionDuration)

#         self.__initWidget()
#         self.theme.state.valueChanged.connect(self.__setQss)
#         self.destroyed.connect(self._on_destroyed)
#         self._connect_signals()

#         if self._get_open():
#             self.show()

#     # Setter and Getter methods
#     @_validate_param(file_path="qtmui.material.snackbar", param_name="color", supported_signatures=Union[State, str], valid_values=VALID_COLORS)
#     def _set_color(self, value):
#         self._color = value

#     def _get_color(self):
#         return self._color.value if isinstance(self._color, State) else self._color

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="icon", supported_signatures=Union[State, PyIconify, str, type(None)])
#     def _set_icon(self, value):
#         self._icon = value
#         if isinstance(value, (PyIconify, str)):
#             self._widget_references.append(self.iconWidget)

#     def _get_icon(self):
#         return self._icon.value if isinstance(self._icon, State) else self._icon

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="title", supported_signatures=Union[State, str, Callable, type(None)])
#     def _set_title(self, value):
#         self._title = value

#     def _get_title(self):
#         return self._title.value if isinstance(self._title, State) else self._title

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="content", supported_signatures=Union[State, str, Callable, type(None)])
#     def _set_content(self, value):
#         self._content = value

#     def _get_content(self):
#         return self._content.value if isinstance(self._content, State) else self._content

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="anchorOrigin", supported_signatures=Union[State, Dict])
#     def _set_anchorOrigin(self, value):
#         self._anchorOrigin = value

#     def _get_anchorOrigin(self):
#         anchor = self._anchorOrigin.value if isinstance(self._anchorOrigin, State) else self._anchorOrigin
#         if not isinstance(anchor, dict) or 'horizontal' not in anchor or 'vertical' not in anchor:
#             return {"vertical": "bottom", "horizontal": "left"}
#         if anchor['horizontal'] not in self.VALID_ANCHOR_HORIZONTAL:
#             anchor['horizontal'] = 'left'
#         if anchor['vertical'] not in self.VALID_ANCHOR_VERTICAL:
#             anchor['vertical'] = 'bottom'
#         return anchor

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="isClosable", supported_signatures=Union[State, bool])
#     def _set_isClosable(self, value):
#         self._isClosable = value

#     def _get_isClosable(self):
#         return self._isClosable.value if isinstance(self._isClosable, State) else self._isClosable

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="autoHideDuration", supported_signatures=Union[State, int, type(None)])
#     def _set_autoHideDuration(self, value):
#         self._autoHideDuration = value

#     def _get_autoHideDuration(self):
#         return self._autoHideDuration.value if isinstance(self._autoHideDuration, State) else self._autoHideDuration

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="position", supported_signatures=Union[State, int, str])
#     def _set_position(self, value):
#         self._position = value

#     def _get_position(self):
#         return self._position.value if isinstance(self._position, State) else self._position

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="action", supported_signatures=Union[State, QWidget, type(None)])
#     def _set_action(self, value):
#         self._action = value
#         if isinstance(value, QWidget):
#             self._widget_references.append(value)

#     def _get_action(self):
#         return self._action.value if isinstance(self._action, State) else self._action

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="children", supported_signatures=Union[State, QWidget, type(None)])
#     def _set_children(self, value):
#         self._children = value
#         if isinstance(value, QWidget):
#             self._widget_references.append(value)

#     def _get_children(self):
#         return self._children.value if isinstance(self._children, State) else self._children

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
#     def _set_classes(self, value):
#         self._classes = value

#     def _get_classes(self):
#         return self._classes.value if isinstance(self._classes, State) else self._classes

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="disableWindowBlurListener", supported_signatures=Union[State, bool])
#     def _set_disableWindowBlurListener(self, value):
#         self._disableWindowBlurListener = value

#     def _get_disableWindowBlurListener(self):
#         return self._disableWindowBlurListener.value if isinstance(self._disableWindowBlurListener, State) else self._disableWindowBlurListener

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="key", supported_signatures=Union[State, Any, type(None)])
#     def _set_key(self, value):
#         self._key = value

#     def _get_key(self):
#         return self._key.value if isinstance(self._key, State) else self._key

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="message", supported_signatures=Union[State, str, Callable, type(None)])
#     def _set_message(self, value):
#         self._message = value

#     def _get_message(self):
#         return self._message.value if isinstance(self._message, State) else self._message

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="onClose", supported_signatures=Union[State, Callable, type(None)])
#     def _set_onClose(self, value):
#         self._onClose = value

#     def _get_onClose(self):
#         return self._onClose.value if isinstance(self._onClose, State) else self._onClose

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="open", supported_signatures=Union[State, bool])
#     def _set_open(self, value):
#         self._open = value
#         if not self._get_open():
#             self.hide()

#     def _get_open(self):
#         return self._open.value if isinstance(self._open, State) else self._open

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="resumeHideDuration", supported_signatures=Union[State, int, type(None)])
#     def _set_resumeHideDuration(self, value):
#         self._resumeHideDuration = value

#     def _get_resumeHideDuration(self):
#         return self._resumeHideDuration.value if isinstance(self._resumeHideDuration, State) else self._resumeHideDuration

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_slotProps(self, value):
#         self._slotProps = value

#     def _get_slotProps(self):
#         return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
#     def _set_slots(self, value):
#         self._slots = value

#     def _get_slots(self):
#         return self._slots.value if isinstance(self._slots, State) else self._slots

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, type(None)])
#     def _set_sx(self, value):
#         self._sx = value

#     def _get_sx(self):
#         return self._sx.value if isinstance(self._sx, State) else self._sx

#     @_validate_param(file_path="qtmui.material.snackbar", param_name="transitionDuration", supported_signatures=Union[State, int, Dict, type(None)])
#     def _set_transitionDuration(self, value):
#         self._transitionDuration = value

#     def _get_transitionDuration(self):
#         duration = self._transitionDuration.value if isinstance(self._transitionDuration, State) else self._transitionDuration
#         if duration is None:
#             return {
#                 'enter': self.theme.transitions.duration.enteringScreen,
#                 'exit': self.theme.transitions.duration.leavingScreen
#             }
#         return duration

#     def __initWidget(self):
#         self.setObjectName(f'Snackbar_{uuid.uuid4()}')
#         self.titleLabel = QLabel(self)
#         self.contentLabel = QLabel(self)
#         self.closeButton = PyToolButton(icon=Iconify(key="mdi:close"))
#         self.iconWidget = PyToolButton(
#             icon=self._get_icon(),
#             color=self._get_color(),
#             size=QSize(24, 24),
#             iconSize=QSize(20, 20)
#         )

#         self.hBoxLayout = QHBoxLayout(self)
#         self.textLayout = QHBoxLayout() if self._get_anchorOrigin()['vertical'] == 'horizontal' else QVBoxLayout()
#         self.widgetLayout = QHBoxLayout() if self._get_anchorOrigin()['vertical'] == 'horizontal' else QVBoxLayout()

#         self.opacityEffect = QGraphicsOpacityEffect(self)
#         self.opacityAni = QPropertyAnimation(self.opacityEffect, b'opacity', self)
#         self.opacityEffect.setOpacity(1)
#         self.setGraphicsEffect(self.opacityEffect)

#         self.lightBackgroundColor = None
#         self.darkBackgroundColor = None

#         self.__initLayout()
#         self.__setQss()
#         self.retranslateUi()

#         self.closeButton.clicked.connect(self.close)
#         if self._get_isClosable():
#             self.closeButton.show()
#         else:
#             self.closeButton.hide()

#         # Initialize children
#         children = self._get_children()
#         if children:
#             children.setParent(self)
#             self.hBoxLayout.addWidget(children)
#             self._widget_references.append(children)
#             self.titleLabel.hide()
#             self.contentLabel.hide()

#         # Initialize action
#         action = self._get_action()
#         if action:
#             self.addWidget(action)

#     def __initLayout(self):
#         self.hBoxLayout.setContentsMargins(6, 6, 6, 6)
#         self.hBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
#         self.hBoxLayout.setSpacing(0)
#         self.textLayout.setSpacing(5)

#         # Add icon to layout
#         self.hBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignVCenter | Qt.AlignLeft)
#         self.iconWidget.setVisible(bool(self._get_icon()))

#         # Add title to layout
#         self.textLayout.addWidget(self.titleLabel)
#         self.titleLabel.setVisible(bool(self._get_title()))

#         # Add content label to layout
#         if self._get_anchorOrigin()['vertical'] == 'horizontal':
#             self.textLayout.addSpacing(7)
#         self.textLayout.addWidget(self.contentLabel)
#         self.contentLabel.setVisible(bool(self._get_content() or self._get_message()))
#         self.hBoxLayout.addLayout(self.textLayout)

#         # Add widget layout
#         if self._get_anchorOrigin()['vertical'] == 'horizontal':
#             self.hBoxLayout.addLayout(self.widgetLayout)
#             self.widgetLayout.setSpacing(10)
#         else:
#             self.textLayout.addLayout(self.widgetLayout)

#         # Add close button to layout
#         self.hBoxLayout.addSpacing(12)
#         self.hBoxLayout.addWidget(self.closeButton, 0, Qt.AlignTop | Qt.AlignLeft)

#         self._adjustText()

#     def __setQss(self):
#         self.titleLabel.setObjectName('titleLabel')
#         self.contentLabel.setObjectName('contentLabel')

#         self.setProperty('p-color', self._get_color())
#         self.titleLabel.setProperty('p-color', self._get_color())
#         self.contentLabel.setProperty('p-color', self._get_color())

#         # Handle theme styles
#         component_styled = self.theme.components
#         snackbar_styles = component_styled.get("Snackbar", {}).get("styles", {})
#         root_styles = snackbar_styles.get("root", {})
#         root_qss = get_qss_style(root_styles)
#         title_label_styles = snackbar_styles.get("titleLabel", {})
#         title_label_qss = get_qss_style(title_label_styles)
#         content_label_styles = snackbar_styles.get("contentLabel", {})
#         content_label_qss = get_qss_style(content_label_styles)

#         # Handle classes
#         classes = self._get_classes()
#         classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}") if classes else ""

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

#         # Apply MUI classes
#         mui_classes = ["MuiSnackbar-root"]

#         stylesheet = f"""
#             #{self.objectName()} {{
#                 {root_qss}
#                 {classes_qss}
#                 background: transparent;
#             }}
#             #titleLabel {{
#                 {title_label_qss}
#             }}
#             #contentLabel {{
#                 {content_label_qss}
#             }}
#             {sx_qss}
#         """
#         self.setStyleSheet(stylesheet)

#         title_label_color = snackbar_styles.get("titleLabel", {}).get("color", "#000000")
#         self.closeButton._set_text_color(title_label_color)

#     def retranslateUi(self):
#         w = 900 if not self.parent() else (self.parent().width() - 50)
#         chars = max(min(w / 9, 120), 30)

#         # Adjust title
#         title = self._get_title()
#         if title:
#             if isinstance(title, Callable):
#                 self.titleLabel.setText(TextWrap.wrap(translate(title), chars, False)[0])
#             elif isinstance(title, str):
#                 self.titleLabel.setText(TextWrap.wrap(title, chars, False)[0])
#         else:
#             self.titleLabel.hide()

#         # Adjust content or message
#         content = self._get_content() or self._get_message()
#         if content:
#             if isinstance(content, Callable):
#                 self.contentLabel.setText(TextWrap.wrap(translate(content), chars, False)[0])
#             elif isinstance(content, str):
#                 self.contentLabel.setText(TextWrap.wrap(content, chars, False)[0])
#         else:
#             self.contentLabel.hide()

#         self.adjustSize()

#     def __fadeOut(self):
#         duration = self._get_transitionDuration()
#         exit_duration = duration.get('exit', self.theme.transitions.duration.leavingScreen) if isinstance(duration, dict) else duration or 200
#         self.opacityAni.setDuration(exit_duration)
#         self.opacityAni.setStartValue(1)
#         self.opacityAni.setEndValue(0)
#         self.opacityAni.finished.connect(self.close)
#         self.opacityAni.start()

#     def _adjustText(self):
#         self.retranslateUi()
#         anchor = self._get_anchorOrigin()
#         if anchor['vertical'] == 'top':
#             self.move(self.x(), 20)
#         else:
#             self.move(self.x(), self.parent().height() - self.height() - 20)
#         if anchor['horizontal'] == 'center':
#             self.move((self.parent().width() - self.width()) // 2, self.y())
#         elif anchor['horizontal'] == 'right':
#             self.move(self.parent().width() - self.width() - 20, self.y())

#     def addWidget(self, widget: QWidget, stretch=0):
#         self.widgetLayout.addSpacing(6)
#         align = Qt.AlignTop if self._get_anchorOrigin()['vertical'] == 'vertical' else Qt.AlignVCenter
#         self.widgetLayout.addWidget(widget, stretch, Qt.AlignLeft | align)
#         self._widget_references.append(widget)

#     def setCustomBackgroundColor(self, light, dark):
#         self.lightBackgroundColor = QColor(light)
#         self.darkBackgroundColor = QColor(dark)
#         self.update()

#     def eventFilter(self, obj, e: QEvent):
#         if obj is self.parent():
#             if e.type() in [QEvent.Resize, QEvent.WindowStateChange]:
#                 self._adjustText()
#         elif e.type() == QEvent.MouseButtonPress and obj is not self and not self.isAncestorOf(obj):
#             if self._get_onClose():
#                 self._get_onClose()(e, "clickaway")
#             self.close()
#         return super().eventFilter(obj, e)

#     def closeEvent(self, e):
#         self.closedSignal.emit()
#         if self._get_onClose():
#             self._get_onClose()(e, "timeout")
#         self._widget_references.clear()
#         self.deleteLater()

#     def showEvent(self, e):
#         self._adjustText()
#         super().showEvent(e)

#         duration = self._get_autoHideDuration()
#         if duration is not None and duration >= 0:
#             if self._get_disableWindowBlurListener() or self.parent().isActiveWindow():
#                 QTimer.singleShot(duration, self.__fadeOut)

#         position = self._get_position()
#         if position != SnackbarPosition.NONE:
#             manager = SnackbarManager.make(position)
#             manager.add(self)

#         if self.parent():
#             self.parent().installEventFilter(self)
#             QApplication.instance().installEventFilter(self)

#     def mousePressEvent(self, e):
#         resume_duration = self._get_resumeHideDuration()
#         if resume_duration is not None and resume_duration >= 0:
#             QTimer.singleShot(resume_duration, self.__fadeOut)

#     def paintEvent(self, e: QPaintEvent):
#         super().paintEvent(e)
#         if self.lightBackgroundColor is None:
#             return

#         painter = QPainter(self)
#         painter.setRenderHints(QPainter.Antialiasing)
#         painter.setPen(Qt.NoPen)
#         painter.setBrush(self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor)
#         rect = self.rect().adjusted(1, 1, -1, -1)
#         painter.drawRoundedRect(rect, 6, 6)

#     def _connect_signals(self):
#         if isinstance(self._title, State):
#             self._title.valueChanged.connect(self.retranslateUi)
#         if isinstance(self._content, State):
#             self._content.valueChanged.connect(self.retranslateUi)
#         if isinstance(self._message, State):
#             self._message.valueChanged.connect(self.retranslateUi)
#         if isinstance(self._open, State):
#             self._open.valueChanged.connect(lambda: self.show() if self._get_open() else self.hide())
#         if isinstance(self._color, State):
#             self._color.valueChanged.connect(self.__setQss)
#         if isinstance(self._sx, State):
#             self._sx.valueChanged.connect(self.__setQss)
#         if isinstance(self._classes, State):
#             self._classes.valueChanged.connect(self.__setQss)
#         if isinstance(self._anchorOrigin, State):
#             self._anchorOrigin.valueChanged.connect(self._adjustText)
#         if isinstance(self._isClosable, State):
#             self._isClosable.valueChanged.connect(lambda: self.closeButton.show() if self._get_isClosable() else self.closeButton.hide())

#     def _on_destroyed(self):
#         self._widget_references.clear()