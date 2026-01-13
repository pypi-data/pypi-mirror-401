from typing import Optional, Union, Dict, Callable, List
from PySide6.QtWidgets import QVBoxLayout, QWidget, QApplication, QFrame, QSizePolicy, QSplitter, QGraphicsDropShadowEffect, QSplitterHandle
from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QColor
from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import i18n
from qtmui.hooks import State, useEffect
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..utils.validate_params import _validate_param

class Drawer(QSplitter):
    """
    A component that renders a drawer sliding in from a specified side.

    The `Drawer` component is used to display a panel that slides in from one side of the
    screen, supporting all props of the Material-UI `Drawer` component, as well as additional
    custom props.

    Parameters
    ----------
    parent : QWidget or None, optional
        The parent widget. Default is None.
    title : State or str, optional
        The title of the drawer (custom feature, not part of Material-UI). Default is "Drawer".
        Can be a `State` object for dynamic updates.
    anchor : State or str, optional
        Side from which the drawer will appear ("bottom", "left", "right", "top"). Default is "left".
        Can be a `State` object for dynamic updates.
    anchorEl : State, QWidget, or None, optional
        The anchor element to position the drawer relative to (custom feature, not part of Material-UI).
        Default is None (uses main window).
        Can be a `State` object for dynamic updates.
    children : State, QWidget, List[QWidget], or None, optional
        The content of the component. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    elevation : State or int, optional
        The elevation of the drawer. Default is 16.
        Can be a `State` object for dynamic updates.
    hideBackdrop : State or bool, optional
        If True, the backdrop is not rendered. Default is False.
        Can be a `State` object for dynamic updates.
    ModalProps : State, dict, or None, optional
        Props applied to the Modal element. Default is {}.
        Can be a `State` object for dynamic updates.
    onClose : State, Callable, or None, optional
        Callback fired when the component requests to be closed. Default is None.
        Signature: function(event: object, reason: string) => void
        Can be a `State` object for dynamic updates.
    open : State or bool, optional
        If True, the drawer is shown. Default is False.
        Can be a `State` object for dynamic updates.
    PaperProps : State, dict, or None, optional
        Props applied to the Paper element. Default is {}.
        Deprecated: Use `slotProps.paper` instead.
        Can be a `State` object for dynamic updates.
    SlideProps : State, dict, or None, optional
        Props applied to the Slide element. Default is {}.
        Deprecated: Use `slotProps.transition` instead.
        Can be a `State` object for dynamic updates.
    slotProps : State, dict, or None, optional
        Props used for each slot inside (backdrop, docked, paper, root, transition). Default is {}.
        Can be a `State` object for dynamic updates.
    slots : State, dict, or None, optional
        Components used for each slot inside (backdrop, docked, paper, root, transition). Default is {}.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    transitionDuration : State, int, dict, or None, optional
        Duration for the transition in milliseconds. Default is
        { "enter": theme.transitions.duration.enteringScreen, "exit": theme.transitions.duration.leavingScreen }.
        Can be a `State` object for dynamic updates.
    variant : State, str, or None, optional
        The drawer variant ("permanent", "persistent", "temporary"). Default is "temporary".
        Can be a `State` object for dynamic updates.
    minWidth : State or int, optional
        Minimum width of the drawer (custom feature, not part of Material-UI). Default is 300.
        Can be a `State` object for dynamic updates.
    maxWidth : State or int, optional
        Maximum width of the drawer (custom feature, not part of Material-UI). Default is 600.
        Can be a `State` object for dynamic updates.
    minHeight : State or int, optional
        Minimum height of the drawer (custom feature, not part of Material-UI). Default is 200.
        Can be a `State` object for dynamic updates.
    maxHeight : State or int, optional
        Maximum height of the drawer (custom feature, not part of Material-UI). Default is 400.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        props of the native component (e.g., style, className).

    Attributes
    ----------
    VALID_ANCHOR : list[str]
        Valid values for `anchor`: ["bottom", "left", "right", "top"].
    VALID_VARIANT : list[str]
        Valid values for `variant`: ["permanent", "persistent", "temporary"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `title`, `minWidth`, `maxWidth`, `minHeight`, `maxHeight` parameters are custom features,
      not part of Material-UI's `Drawer`.
    - The `PaperProps` and `SlideProps` props are deprecated; use `slotProps.paper` and
      `slotProps.transition` instead.
    - The `onClose` callback receives an event and a reason ("escapeKeyDown", "backdropClick").

    Demos:
    - Drawer: https://qtmui.com/material-ui/qtmui-drawer/

    API Reference:
    - Drawer API: https://qtmui.com/material-ui/api/drawer/
    """

    VALID_ANCHOR = ["bottom", "left", "right", "top"]
    VALID_VARIANT = ["permanent", "persistent", "temporary"]

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        title: Optional[Union[State, str, Callable]] = "Drawer",
        anchor: Union[State, str] = "right",
        anchorEl: Optional[Union[State, QWidget]] = None,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        elevation: Union[State, int] = 16,
        hideBackdrop: Union[State, bool] = False,
        ModalProps: Optional[Union[State, Dict]] = None,
        onClose: Optional[Union[State, Callable]] = None,
        open: Union[State, bool] = False,
        PaperProps: Optional[Union[State, Dict]] = None,
        SlideProps: Optional[Union[State, Dict]] = None,
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        transitionDuration: Optional[Union[State, int, Dict]] = None,
        variant: Optional[Union[State, str]] = "temporary",
        minWidth: Optional[Union[State, int]] = None,
        maxWidth: Optional[Union[State, int]] = None,
        minHeight: Optional[Union[State, int]] = None,
        maxHeight: Optional[Union[State, int]] = None,
        *args,
        **kwargs
    ):
        super().__init__(parent or QApplication.instance().mainWindow)

        self.setObjectName(f"PyDrawer")

        # Initialize theme
        self.theme = useTheme()

        # Store widget references to prevent Qt deletion
        self._widget_references = []

        # Set properties with validation
        self._set_title(title)
        self._set_anchor(anchor)
        self._set_anchorEl(anchorEl)
        self._set_children(children)
        self._set_classes(classes)
        self._set_elevation(elevation)
        self._set_hideBackdrop(hideBackdrop)
        self._set_ModalProps(ModalProps or {})
        self._set_onClose(onClose)
        self._set_open(open)
        self._set_PaperProps(PaperProps or {})
        self._set_SlideProps(SlideProps or {})
        self._set_slotProps(slotProps or {})
        self._set_slots(slots or {})
        self._set_sx(sx)
        # self._set_transitionDuration(transitionDuration or {
        #     "enter": self.theme.transitions.duration.enteringScreen,
        #     "exit": self.theme.transitions.duration.leavingScreen
        # })
        self._set_variant(variant)
        
        self._set_minWidth(minWidth)
        self._set_maxWidth(maxWidth)
        self._set_minHeight(minHeight)
        self._set_maxHeight(maxHeight)

        self._user_dragging = False

        # Setup UI
        self._init_ui()


    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.drawer", param_name="title", supported_signatures=Union[State, str, Callable])
    def _set_title(self, value):
        """Assign value to title (custom feature)."""
        self._title = value

    def _get_title(self):
        """Get the title value."""
        return self._title.value if isinstance(self._title, State) else self._title

    @_validate_param(file_path="qtmui.material.drawer", param_name="anchor", supported_signatures=Union[State, str], valid_values=VALID_ANCHOR)
    def _set_anchor(self, value):
        """Assign value to anchor."""
        self._anchor = value

    def _get_anchor(self):
        """Get the anchor value."""
        return self._anchor.value if isinstance(self._anchor, State) else self._anchor

    @_validate_param(file_path="qtmui.material.drawer", param_name="anchorEl", supported_signatures=Union[State, QWidget, type(None)])
    def _set_anchorEl(self, value):
        """Assign value to anchorEl (custom feature)."""
        self._anchorEl = value

    def _get_anchorEl(self):
        """Get the anchorEl value."""
        return self._anchorEl.value if isinstance(self._anchorEl, State) else self._anchorEl

    # @_validate_param(file_path="qtmui.material.drawer", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        """Assign value to children and store widget references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.drawer", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.drawer", param_name="elevation", supported_signatures=Union[State, int])
    def _set_elevation(self, value):
        """Assign value to elevation."""
        self._elevation = value

    def _get_elevation(self):
        """Get the elevation value."""
        return self._elevation.value if isinstance(self._elevation, State) else self._elevation

    @_validate_param(file_path="qtmui.material.drawer", param_name="hideBackdrop", supported_signatures=Union[State, bool])
    def _set_hideBackdrop(self, value):
        """Assign value to hideBackdrop."""
        self._hideBackdrop = value

    def _get_hideBackdrop(self):
        """Get the hideBackdrop value."""
        return self._hideBackdrop.value if isinstance(self._hideBackdrop, State) else self._hideBackdrop

    @_validate_param(file_path="qtmui.material.drawer", param_name="ModalProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_ModalProps(self, value):
        """Assign value to ModalProps."""
        self._ModalProps = value

    def _get_ModalProps(self):
        """Get the ModalProps value."""
        return self._ModalProps.value if isinstance(self._ModalProps, State) else self._ModalProps

    @_validate_param(file_path="qtmui.material.drawer", param_name="onClose", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClose(self, value):
        """Assign value to onClose."""
        self._onClose = value

    def _get_onClose(self):
        """Get the onClose value."""
        return self._onClose.value if isinstance(self._onClose, State) else self._onClose

    @_validate_param(file_path="qtmui.material.drawer", param_name="open", supported_signatures=Union[State, bool])
    def _set_open(self, value):
        """Assign value to open."""
        self._open = value

    def _get_open(self):
        """Get the open value."""
        return self._open.value if isinstance(self._open, State) else self._open

    @_validate_param(file_path="qtmui.material.drawer", param_name="PaperProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_PaperProps(self, value):
        """Assign value to PaperProps."""
        self._PaperProps = value

    def _get_PaperProps(self):
        """Get the PaperProps value."""
        return self._PaperProps.value if isinstance(self._PaperProps, State) else self._PaperProps

    @_validate_param(file_path="qtmui.material.drawer", param_name="SlideProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_SlideProps(self, value):
        """Assign value to SlideProps."""
        self._SlideProps = value

    def _get_SlideProps(self):
        """Get the SlideProps value."""
        return self._SlideProps.value if isinstance(self._SlideProps, State) else self._SlideProps

    @_validate_param(file_path="qtmui.material.drawer", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        """Assign value to slotProps."""
        self._slotProps = value

    def _get_slotProps(self):
        """Get the slotProps value."""
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.drawer", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        """Assign value to slots."""
        self._slots = value

    def _get_slots(self):
        """Get the slots value."""
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.drawer", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.drawer", param_name="transitionDuration", supported_signatures=Union[State, int, Dict, type(None)])
    def _set_transitionDuration(self, value):
        """Assign value to transitionDuration."""
        self._transitionDuration = value

    def _get_transitionDuration(self):
        """Get the transitionDuration value."""
        return self._transitionDuration.value if isinstance(self._transitionDuration, State) else self._transitionDuration

    @_validate_param(file_path="qtmui.material.drawer", param_name="variant", supported_signatures=Union[State, str, type(None)], valid_values=VALID_VARIANT)
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant

    @_validate_param(file_path="qtmui.material.drawer", param_name="minWidth", supported_signatures=Union[State, int, None])
    def _set_minWidth(self, value):
        """Assign value to minWidth (custom feature)."""
        self._minWidth = value

    def _get_minWidth(self):
        """Get the minWidth value."""
        return self._minWidth.value if isinstance(self._minWidth, State) else self._minWidth

    @_validate_param(file_path="qtmui.material.drawer", param_name="maxWidth", supported_signatures=Union[State, int, None])
    def _set_maxWidth(self, value):
        """Assign value to maxWidth (custom feature)."""
        self._maxWidth = value

    def _get_maxWidth(self):
        """Get the maxWidth value."""
        return self._maxWidth.value if isinstance(self._maxWidth, State) else self._maxWidth

    @_validate_param(file_path="qtmui.material.drawer", param_name="minHeight", supported_signatures=Union[State, int, None])
    def _set_minHeight(self, value):
        """Assign value to minHeight (custom feature)."""
        self._minHeight = value

    def _get_minHeight(self):
        """Get the minHeight value."""
        return self._minHeight.value if isinstance(self._minHeight, State) else self._minHeight

    @_validate_param(file_path="qtmui.material.drawer", param_name="maxHeight", supported_signatures=Union[State, int, None])
    def _set_maxHeight(self, value):
        """Assign value to maxHeight (custom feature)."""
        self._maxHeight = value

    def _get_maxHeight(self):
        """Get the maxHeight value."""
        return self._maxHeight.value if isinstance(self._maxHeight, State) else self._maxHeight

    def __setupStates(self):
        if isinstance(self._minWidth, State):
            self._minWidth.valueChanged.connect(self.__setupSize)
        if isinstance(self._minHeight, State):
            self._minHeight.valueChanged.connect(self.__setupSize)
        if isinstance(self._maxWidth, State):
            self._maxWidth.valueChanged.connect(self.__setupSize)
        if isinstance(self._maxHeight, State):
            self._maxHeight.valueChanged.connect(self.__setupSize)

    def _init_ui(self):
        self.setObjectName("PyDrawer")
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint) # xài ok
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Cho phép nền trong suốt
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)

        self._frm_content = QFrame(self)
        self._frm_content.setObjectName("contentFrame")
        self._frm_content.setStyleSheet("#contentFrame { border: 1px solid red; }")
        # self._frm_content.setFrameShape(QFrame.StyledPanel)
        self._contentLayout = QVBoxLayout(self._frm_content)
        
        self._overlay = QWidget(self)
        self._overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self._overlay.setAutoFillBackground(False)
        self._overlay.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._overlay.setStyleSheet("background-color: transparent;")
        
        self.setHandleWidth(0)

        # Cho phép or không cho widget collapse
        self.setChildrenCollapsible(True)  # False để không cho widget collapse hết
        self.setOpaqueResize(True)  # True để thay đổi kích thước ngay khi kéo

        self.__setupSize()

        # Thêm children widget vào layout của Drawer
        if self._children is not None:
            if isinstance(self._children, list):
                for widget in self._children:
                    self._contentLayout.addWidget(widget)
            else:
                if isinstance(self._children, QWidget):
                    self._contentLayout.addWidget(self._children)

        if not isinstance(self._open, State):
            raise ValueError("The attribute 'open' only accepts input in the form of State.")
        
        self._open.valueChanged.connect(self._show)

        # Cài đặt event filter để theo dõi sự kiện resize và move
        self.installEventFilter(self)
        if self._anchorEl and isinstance(self._anchorEl, QWidget):
            self._anchorEl.installEventFilter(self)
        QApplication.instance().mainWindow.installEventFilter(self)

        self.theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self._set_stylesheet()

        i18n.langChanged.connect(self.reTranslation)
        
        self.handle(1).installEventFilter(self)
        # self.splitterMoved.connect(lambda: (self.refresh(), self.update()))
        # self.splitterMoved.connect(self.setShadowEffect)
        
        self.__setupStates()

    def __setupSize(self, value=None):
        # Tính toán vị trí của Drawer dựa trên anchor
        if self._anchor == "left":
            self.setOrientation(Qt.Orientation.Horizontal)
            self.addWidget(self._frm_content)
            self.addWidget(self._overlay)
            self.setContentsMargins(1,0,0,0)
            if self._minWidth is not None:
                self.setSizes([self._get_minWidth(), 50])
                self._frm_content.setMinimumWidth(self._get_minWidth())
            if self._maxWidth is not None:
                self._frm_content.setMaximumWidth(self._get_maxWidth())
        elif self._anchor == "right":
            self.setOrientation(Qt.Orientation.Horizontal)
            self.addWidget(self._overlay)
            self.addWidget(self._frm_content)
            # print('self._minWidth______________', self._minWidth)
            self.setContentsMargins(0,0,1,1)
            if self._minWidth is not None:
                self.setSizes([5000, self._get_minWidth()])
                self._frm_content.setMinimumWidth(self._get_minWidth())
            if self._maxWidth is not None:
                self._frm_content.setMaximumWidth(self._get_maxWidth())
        elif self._anchor == "top":
            self.setOrientation(Qt.Orientation.Vertical)
            self.addWidget(self._frm_content)
            self.addWidget(self._overlay)
            self.setContentsMargins(0,1,0,0)
            if self._minHeight is not None:
                self.setSizes([self._get_minHeight(), 50])
                self._frm_content.setMinimumHeight(self._get_minHeight())
            if self._maxHeight is not None:
                self._frm_content.setMaximumHeight(self._get_maxHeight())
        elif self._anchor == "bottom":
            self.setOrientation(Qt.Orientation.Vertical)
            self.addWidget(self._overlay)
            self.addWidget(self._frm_content)
            self.setContentsMargins(0,1,0,0) # cho cạnh ngay ngắn hơn
            if self._minHeight is not None:
                self.setSizes([50, self._get_minHeight()])
                self._frm_content.setMinimumHeight(self._get_minHeight())
            if self._maxHeight is not None:
                self._frm_content.setMaximumHeight(self._get_maxHeight())
        self.update_position()


    def _set_stylesheet(self):
        self.theme = useTheme()
        component_styles = self.theme.components

        ownerState = {
            "anchor": self._anchor,
            "variant": self._variant,
        }

        PyDrawer_root = component_styles[f"PyDrawer"].get("styles")["root"](ownerState)
        PyDrawer_contentFrame = component_styles[f"PyDrawer"].get("styles")["contentFrame"](ownerState)
        PyDrawer_root_qss = get_qss_style(PyDrawer_root)
        PyDrawer_contentFrame_qss = get_qss_style(PyDrawer_contentFrame)


        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx)
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx)
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx
        
        self.setStyleSheet(
            f"""
                #PyDrawer {{
                    {PyDrawer_root_qss}
                    {sx_qss}
                    
                }}
                #contentFrame {{
                    {PyDrawer_contentFrame_qss}
                }}
            """
        )
        
        
        self.setShadowEffect()


    def setShadowEffect(self, blurRadius=60, offset=(0, 10), color=QColor(0, 0, 0, 50)):
        """ add shadow to dialog """
        # print("Setting shadow effect")
        try:
            shadowEffect = QGraphicsDropShadowEffect(self._frm_content)
            shadowEffect.setBlurRadius(blurRadius)
            shadowEffect.setOffset(*offset)
            shadowEffect.setColor(color)
            self._frm_content.setGraphicsEffect(None)
            self._frm_content.setGraphicsEffect(shadowEffect)
        except Exception as e:
            pass

    def reTranslation(self):
        if isinstance(self._title, Callable):
            pass

    def _show(self, state: bool):
        # Cập nhật vị trí của Drawer trước khi hiển thị
        if state and not self.isVisible():
            # self.update_position()
            self.move(-30000, -30000)
            self.setVisible(True)
            self.update_position()
            # self.raise_()
        else:
            self.setVisible(False)

    def _close(self):
        self.setVisible(False)
        if self._onClose:
            self._onClose()

    def hideEvent(self, event):
        if self._onClose:
            self._onClose()
        return super().hideEvent(event)

    # def showDrawer(self):
    #     # print('showwwwwwwwwww drawerrrrrrrrrr')
    #     # Cập nhật vị trí của Drawer trước khi hiển thị
    #     # self.move(-30000, -30000)
    #     self.setVisible(True)
    #     # self.update_position()
    #     QTimer.singleShot(100, self.update_position)
        
    #     # self.raise_()


    def update_position(self):
        # Lấy vị trí và kích thước của anchorEl
        if not self._anchorEl:
            self._anchorEl = QApplication.instance().mainWindow
        # self._anchorEl.update()
        popup_position = self._anchorEl.mapToGlobal(QPoint(0, 0))
        self.setGeometry(popup_position.x(), popup_position.y(), self._anchorEl.width(), self._anchorEl.height())


    def eventFilter(self, source, event):
        if ((event.type() == QEvent.Resize) or (event.type() == QEvent.Move)) and source == self._anchorEl:
            if self.isVisible():
                # self.update_position()
                self.setVisible(False)
                
        if event.type() == QEvent.MouseButtonPress:
            self._user_dragging = True
            if not self._frm_content.underMouse() and not isinstance(source, QSplitterHandle):
                self._user_dragging = False
                self.hide()
                print('source_____________', source)
        elif event.type() == QEvent.MouseButtonRelease and self._user_dragging:
            self._user_dragging = False
            self.refresh()
            self.update()
            
        return super().eventFilter(source, event)
    
