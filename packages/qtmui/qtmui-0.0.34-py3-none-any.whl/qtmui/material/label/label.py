from typing import Callable, Optional, Union
from PySide6.QtWidgets import QLabel, QWidget, QSizePolicy, QHBoxLayout, QSpacerItem, QPushButton
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPalette
from ..system.color_manipulator import rgba_to_hex, rgb2hex
from qtmui.hooks import State, useEffect

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from ..py_tool_button import PyToolButton
from ..py_iconify import PyIconify, Iconify

from qtmui.i18n.use_translation import translate, i18n

from ..widget_base import PyWidgetBase

class Label(QPushButton, PyWidgetBase):
    """
    Label
    Base container

    Args:
        * Set the text-align on the component.
        * @default 'inherit'
        align?: 'inherit' | 'left' | 'center' | 'right' | 'justify';
        * The content of the component.
        children?: React.ReactNode;
        * Override or extend the styles applied to the component.
        classes?: Partial<TypographyClasses>;
        * If `true`, the text will have a bottom margin.
        * @default false
        gutterBottom?: boolean;
        * If `true`, the text will not wrap, but instead will truncate with a text overflow ellipsis.
        *
        * Note that text overflow can only happen with block or inline-block level elements
        * (the element needs to have a width in order to overflow).
        * @default false
        noWrap?: boolean;
        * If `true`, the element will be a paragraph element.
        * @default false
        paragraph?: boolean;
        * The system prop that allows defining system overrides as well as additional CSS styles.
        sx?: SxProps<Theme>;
        * Applies the theme typography styles.
        * @default 'body1'
        variant?: OverridableStringUnion<Variant | 'inherit', TypographyPropsVariantOverrides>;
        * Alternatively, you can use the `component` prop.
        * @default {
        *   soft: 'soft',
        *   soft: 'soft',
        * }

    Returns:
        new instance of PySyde6.QtWidgets.QFrame
    """
    def __init__(self,  
                 parent=None,
                 id=None,
                 align="left",
                text: Optional[Union[State, str, Callable]] = None,
                 color: str = "textPrimary",
                 classes=None, 
                 gutterBottom=None,
                 noWrap=None,
                 paragraph=None,
                 size: str = "small",
                 sx: str = None,
                 startIcon: Optional[Union[str, PyIconify, Iconify]] = None,
                 endIcon: Optional[Union[str, PyIconify, Iconify]] = None,
                 variant:str="soft",
                 **kwargs
                 ):
        super().__init__(parent, **kwargs)

        self._id = id
        self._align = align
        self._color = color
        self._classes = classes
        self._noWrap = noWrap
        self._gutterBottom = gutterBottom
        self._paragraph = paragraph
        self._sx = sx
        self._text = text
        self._variant = variant
        self._size = size
        self._startIcon = startIcon
        self._endIcon = endIcon

        self._init_ui()


    def _init_ui(self):
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        if isinstance(self._text, State):
            self._text.valueChanged.connect(self.reTranslation)

        if self._startIcon:
            if isinstance(self._startIcon, str):
                self._startIcon = PyIconify(key=self._startIcon)
                self.setIcon(self._startIcon)
            elif isinstance(self._startIcon, PyIconify):
                self.setIcon(self._startIcon)
        elif self._endIcon:
            if isinstance(self._endIcon, str):
                self._endIcon = PyIconify(key=self._endIcon)
                self.setIcon(self._endIcon)
            elif isinstance(self._endIcon, PyIconify):
                self.setIcon(self._endIcon)
            self.setLayoutDirection(Qt.RightToLeft)

        PyWidgetBase._installTooltipFilter(self)

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()
        self._setIcon()

        i18n.langChanged.connect(self.reTranslation)
        self.reTranslation()
        

    def reTranslation(self, value=None):
        self.setText(self._getTranslatedText(self._text))
        self.adjustSize()

    def _set_stylesheet(self):
        theme = useTheme()

        self.setObjectName(f"PyLabel{self._variant.capitalize()}")

        if self._variant == "filled":
            self.setProperty("variant", "filled")
        elif self._variant == "outlined":
            self.setProperty("variant", "outlined")
        else:
            self.setProperty("variant", "soft")

        if self._startIcon:
            self.setProperty("withStartIcon", "true")
        if self._endIcon:
            self.setProperty("withEndIcon", "true")


        # coi lại
        if self._color == "textPrimary" \
        or  self._color == "textSecondary" \
        or  self._color == "textInfo" \
        or  self._color == "textError" \
        or  self._color == "textWarning":
            self._color = self._color.replace("text", "").lower()

        PyLabel_root = theme.components["PyLabel"].get("styles")["root"][self._color]
        PyLabel_root_qss = get_qss_style(PyLabel_root)

        props = PyLabel_root["props"]
        PyLabel_root_filled_qss = get_qss_style(props["variant"]["filled"])
        PyLabel_root_outlined_qss = get_qss_style(props["variant"]["outlined"])
        PyLabel_root_soft_qss = get_qss_style(props["variant"]["soft"])


        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {PyLabel_root_qss}
                }}
                #{self.objectName()}[variant=filled] {{
                    {PyLabel_root_filled_qss}
                }}
                #{self.objectName()}[variant=outlined] {{
                    {PyLabel_root_outlined_qss}
                }}
                #{self.objectName()}[variant=soft] {{
                    {PyLabel_root_soft_qss}
                }}
            """
        )

    def changeEvent(self, event: QEvent):
        if event.type() == event.Type.StyleChange:
            try:
                if self._startIcon or self._endIcon:
                    self._setIcon()
            except Exception as e:
                import traceback
                traceback.print_exc()
        super().changeEvent(event)
        
    def _setIcon(self):

        if self._startIcon and isinstance(self._startIcon, Callable):
            self._startIcon = self._startIcon()

        if isinstance(self._startIcon, Iconify):
            color = self.palette().color(QPalette.ColorRole.ButtonText)
            self._startIcon._color = color.name()
            self.setIcon(self._startIcon.qIcon())#"#919eab"
        elif isinstance(self._endIcon, Iconify):
            color = self.palette().color(QPalette.ColorRole.ButtonText)
            self._endIcon._color = color.name()
            self.setIcon(self._endIcon.qIcon())
            self.setLayoutDirection(Qt.RightToLeft)
        