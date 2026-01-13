import asyncio
from functools import lru_cache
from typing import Optional, Union, Callable, Any, Dict, List
import uuid

from qtmui.hooks import State, useEffect
from ..py_iconify import PyIconify

from qtmui.hooks.use_runable import useRunnable
from PySide6.QtWidgets import QPushButton, QHBoxLayout
from PySide6.QtGui import Qt, QPixmap, QPainter, QPen, QImage, QBrush, QColor
from PySide6.QtCore import Qt, QRect, QSize, QThreadPool, QTimer

from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor
from ..system.color_manipulator import alpha, get_random_flat_ui_color
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ...utils.data import convert_sx_params_to_str, convert_sx_params_to_dict

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n

from ..widget_base import PyWidgetBase
from ..utils.validate_params import _validate_param

class Avatar(QPushButton, PyWidgetBase):
    """
    A component that displays an image, text, or icon in a circular, rounded, or square shape.

    The `Avatar` component is used to represent a user or entity with an image, text, or icon.
    It supports all props of the Material-UI `Avatar` component, including additional props
    for badges, custom text, and click events. Native component props are supported via `**kwargs`.

    Parameters
    ----------
    alt : State or str, optional
        The alt attribute for the img element, used with `src` or `srcSet`. Default is None.
        Can be a `State` object for dynamic updates.
    badge : State or str, optional
        Icon path or color for the badge (e.g., 'primary', 'secondary', or path to image).
        Default is None. Can be a `State` object for dynamic updates.
    borderWidth : State or int, optional
        Width of the border around the avatar. Default is 0.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        Color for the background or text. Supports hex colors or 'default'. Default is 'default'.
        Can be a `State` object for dynamic updates.
    children : State or Any, optional
        Icon or text elements to render inside the avatar if `src` is not set. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or Any, optional
        Component used for the root node (e.g., HTML element or custom component).
        Default is None. Can be a `State` object for dynamic updates.
    customText : State or bool, optional
        If True, renders text as provided instead of capitalizing the first letter.
        Default is False. Can be a `State` object for dynamic updates.
    imgProps : State or dict, optional
        Attributes applied to the img element if displaying an image. Deprecated: Use `slotProps.img` instead.
        Default is None. Can be a `State` object for dynamic updates.
    icon : State or str, optional
        Path to an icon to display if `src` and `text` are not set. Default is None.
        Can be a `State` object for dynamic updates.
    key : State or Any, optional
        Unique key for the component, used for internal purposes. Default is None.
        Can be a `State` object for dynamic updates.
    mediumBadge : State or bool, optional
        If True, displays a larger badge. Default is False.
        Can be a `State` object for dynamic updates.
    onClick : State or Callable, optional
        Callback fired when the avatar is clicked. Signature: function(event: Any) => None.
        Default is None. Can be a `State` object for dynamic updates.
    size : State or int, optional
        Size of the avatar in pixels. Valid values: [24, 32, 40, 56]. Default is 40.
        Can be a `State` object for dynamic updates.
    sizes : State or str, optional
        The sizes attribute for the img element, used for responsive images. Default is None.
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for each slot (e.g., fallback, img, root). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for each slot (e.g., fallback, img, root). Default is None.
        Can be a `State` object for dynamic updates.
    src : State or str, optional
        The src attribute for the img element. Default is None.
        Can be a `State` object for dynamic updates.
    srcSet : State or str, optional
        The srcSet attribute for the img element, used for responsive images.
        Alias: `imageSet`. Default is None. Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        Shape of the avatar. Valid values: 'circular', 'rounded', 'square'. Default is 'circular'.
        Can be a `State` object for dynamic updates.
    text : State or str, optional
        Text to display inside the avatar if `src` is not set. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QPushButton` class, supporting
        native component props (e.g., style, className).

    Attributes
    ----------
    VALID_VARIANTS : list[str]
        Valid values for the `variant` parameter: ["circular", "rounded", "square"].
    VALID_SIZES : list[int]
        Valid values for the `size` parameter: [24, 32, 40, 56].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `imgProps` prop is deprecated; use `slotProps.img` instead.
    - The `srcSet` prop was previously named `imageSet` for backward compatibility.
    - Additional props (`badge`, `borderWidth`, `color`, `customText`, `icon`, `key`, `mediumBadge`,
      `onClick`, `text`) are specific to this implementation and not part of Material-UI `Avatar`.

    Demos:
    - Avatar: https://qtmui.com/material-ui/qtmui-avatar/

    API Reference:
    - Avatar API: https://qtmui.com/material-ui/api/avatar/
    """

    VALID_VARIANTS = ["circular", "rounded", "square"]
    VALID_SIZES = [24, 32, 40, 56]

    def __init__(
        self,
        alt: Optional[Union[State, str]] = None,
        badge: Optional[Union[State, str]] = None,
        borderWidth: Optional[Union[State, int]] = 0,
        color: Union[State, str] = "default",
        children: Optional[Union[State, Any]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, Any]] = None,
        customText: Union[State, bool] = False,
        imgProps: Optional[Union[State, Dict]] = None,
        icon: Optional[Union[State, str]] = None,
        key: Optional[Union[State, Any]] = None,
        mediumBadge: Union[State, bool] = False,
        onClick: Optional[Union[State, Callable[[Any], None]]] = None,
        size: Union[State, int] = 40,
        sizes: Optional[Union[State, str]] = None,
        slotProps: Optional[Union[State, Dict[str, Union[Callable, Dict]]]] = None,
        slots: Optional[Union[State, Dict[str, Any]]] = None,
        src: Optional[Union[State, str]] = None,
        srcSet: Optional[Union[State, str]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        variant: Union[State, str] = "circular",
        text: Optional[Union[State, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Set properties with validation
        self._set_alt(alt)
        self._set_badge(badge)
        self._set_borderWidth(borderWidth)
        self._set_color(color)
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_customText(customText)
        self._set_imgProps(imgProps)
        self._set_icon(icon)
        self._set_key(key)
        self._set_mediumBadge(mediumBadge)
        self._set_onClick(onClick)
        self._set_size(size)
        self._set_sizes(sizes)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_src(src)
        self._set_srcSet(srcSet)
        self._set_sx(sx)
        self._set_variant(variant)
        self._set_text(text)

        self._init_ui()
        self._set_stylesheet()

        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()

        self.theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self.destroyed.connect(self._on_destroyed)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        # Connect onClick to clicked signal
        if self._get_onClick():
            self.clicked.connect(self._get_onClick())

    # Setter and Getter methods for all parameters
    @_validate_param(file_path="qtmui.material.avatar", param_name="alt", supported_signatures=Union[State, str, type(None)])
    def _set_alt(self, value):
        self._alt = value

    def _get_alt(self):
        return self._alt.value if isinstance(self._alt, State) else self._alt

    @_validate_param(file_path="qtmui.material.avatar", param_name="badge", supported_signatures=Union[State, str, type(None)])
    def _set_badge(self, value):
        self._badge = value

    def _get_badge(self):
        return self._badge.value if isinstance(self._badge, State) else self._badge

    @_validate_param(file_path="qtmui.material.avatar", param_name="borderWidth", supported_signatures=Union[State, int, type(None)])
    def _set_borderWidth(self, value):
        self._borderWidth = value

    def _get_borderWidth(self):
        return self._borderWidth.value if isinstance(self._borderWidth, State) else self._borderWidth

    # @_validate_param(file_path="qtmui.material.avatar", param_name="color", supported_signatures=Union[State, str])
    def _set_color(self, value):
        self._color = value

    def _get_color(self):
        return self._color.value if isinstance(self._color, State) else self._color

    # @_validate_param(file_path="qtmui.material.avatar", param_name="children", supported_signatures=Union[State, Any, type(None)])
    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.avatar", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    # @_validate_param(file_path="qtmui.material.avatar", param_name="component", supported_signatures=Union[State, Any, type(None)])
    def _set_component(self, value):
        self._component = value

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.avatar", param_name="customText", supported_signatures=Union[State, bool])
    def _set_customText(self, value):
        self._customText = value

    def _get_customText(self):
        return self._customText.value if isinstance(self._customText, State) else self._customText

    @_validate_param(file_path="qtmui.material.avatar", param_name="imgProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_imgProps(self, value):
        self._imgProps = value

    def _get_imgProps(self):
        return self._imgProps.value if isinstance(self._imgProps, State) else self._imgProps

    @_validate_param(file_path="qtmui.material.avatar", param_name="icon", supported_signatures=Union[State, str, PyIconify, type(None)])
    def _set_icon(self, value):
        self._icon = value

    def _get_icon(self):
        return self._icon.value if isinstance(self._icon, State) else self._icon

    # @_validate_param(file_path="qtmui.material.avatar", param_name="key", supported_signatures=Union[State, Any, type(None)])
    def _set_key(self, value):
        self._key = value

    def _get_key(self):
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.avatar", param_name="mediumBadge", supported_signatures=Union[State, bool])
    def _set_mediumBadge(self, value):
        self._mediumBadge = value

    def _get_mediumBadge(self):
        return self._mediumBadge.value if isinstance(self._mediumBadge, State) else self._mediumBadge

    @_validate_param(file_path="qtmui.material.avatar", param_name="onClick", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClick(self, value):
        self._onClick = value

    def _get_onClick(self):
        return self._onClick.value if isinstance(self._onClick, State) else self._onClick

    # @_validate_param(file_path="qtmui.material.avatar", param_name="size", supported_signatures=Union[State, int, str], valid_values=VALID_SIZES)
    def _set_size(self, value):
        self._size = value

    def _get_size(self):
        return self._size.value if isinstance(self._size, State) else self._size

    @_validate_param(file_path="qtmui.material.avatar", param_name="sizes", supported_signatures=Union[State, str, type(None)])
    def _set_sizes(self, value):
        self._sizes = value

    def _get_sizes(self):
        return self._sizes.value if isinstance(self._sizes, State) else self._sizes

    @_validate_param(file_path="qtmui.material.avatar", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value or {}

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.avatar", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value or {}

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.avatar", param_name="src", supported_signatures=Union[State, str, type(None)])
    def _set_src(self, value):
        self._src = value

    def _get_src(self):
        return self._src.value if isinstance(self._src, State) else self._src

    @_validate_param(file_path="qtmui.material.avatar", param_name="srcSet", supported_signatures=Union[State, str, type(None)])
    def _set_srcSet(self, value):
        self._srcSet = value

    def _get_srcSet(self):
        return self._srcSet.value if isinstance(self._srcSet, State) else self._srcSet

    @_validate_param(file_path="qtmui.material.avatar", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.avatar", param_name="variant", supported_signatures=Union[State, str], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        self._variant = value

    def _get_variant(self):
        return self._variant.value if isinstance(self._variant, State) else self._variant

    @_validate_param(file_path="qtmui.material.avatar", param_name="text", supported_signatures=Union[State, str, type(None)])
    def _set_text(self, value):
        self._text = value

    def _get_text(self):
        return self._text.value if isinstance(self._text, State) else self._text

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))

        if not self._color:
            self._color = "default"

        if self._color.find("#") != -1:
            self._text_avatar_color = self._color
            self._color = "default"
        else:
            self._text_avatar_color = get_random_flat_ui_color()

        if isinstance(self._size, int):
            self.setFixedSize(self._size, self._size)
        elif isinstance(self._size, QSize):
            self.setFixedSize(self._size)

    def retranslateUi(self):
        if self._customText:
            if isinstance(self._text, Callable):
                self.setText(translate(self._text))
            else:
                self.setText(self._text)
        elif self._text:
            self.setText(str(self._text[0]).capitalize())

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        if self._variant == "circular":
            self.setProperty("variant", "circular")
        elif self._variant == "rounded":
            self.setProperty("variant", "rounded")
        else: # square
            self.setProperty("variant", "square")

        if not self._src and not self._text and self._icon:
            self.setIcon(self._icon)
            icon_size = self._size/2
            self.setIconSize(QSize(icon_size, icon_size))

        ownerState = {
            "size": int(self._size)
        }

        PyAlert_root = component_styled["PyAvatar"].get("styles")["root"](ownerState)[self._color]
        PyAlert_root_qss = get_qss_style(PyAlert_root)
        PyAlert_root_prop_variant_circular = get_qss_style(PyAlert_root["props"]["circularVariant"])
        PyAlert_root_prop_variant_rounded = get_qss_style(PyAlert_root["props"]["roundedVariant"])
        PyAlert_root_prop_variant_square = get_qss_style(PyAlert_root["props"]["squareVariant"])

        PyAlert_root_prop_has_icon_qss = ""
        if not self._src and not self._text and self._icon:
            PyAlert_root_prop_has_icon_qss = get_qss_style(PyAlert_root["props"]["hasIcon"])

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

        stylesheet = f"""
            #{self.objectName()} {{
                {PyAlert_root_qss}
                {PyAlert_root_prop_has_icon_qss}
            }}
            #{self.objectName()}[variant=circular] {{
                {PyAlert_root_prop_variant_circular}
            }}
            #{self.objectName()}[variant=rounded] {{
                {PyAlert_root_prop_variant_rounded}
            }}
            #{self.objectName()}[variant=square] {{
                {PyAlert_root_prop_variant_square}
            }}
            #{self.objectName()}[variant=square] {{
                {PyAlert_root_prop_variant_square}
            }}
                
            {sx_qss}
            
        """

        self.setStyleSheet(stylesheet)


    def paintEvent(self, event):

        if not hasattr(self, "theme"):
            self.theme = useTheme()

        if self._src:
            pixmap = QPixmap(self._src)
            scaled_pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  

            pen = QPen(Qt.white)
            pen.setWidth(self._borderWidth) 
            if self._borderWidth:
                painter.setPen(pen)
            else:
                painter.setPen(Qt.NoPen)

            brush = QBrush()
            brush.setStyle(Qt.Dense2Pattern)
            brush.setTexture(scaled_pixmap)
            painter.setBrush(brush)

            painter.drawRoundedRect(self.rect(), self._size, self._size)
        elif self._text:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  

            painter.setPen(Qt.NoPen)
            # brush = QBrush(self.theme.palette.primary.lighter if self._customText else QColor(self._background_color))
            brush = QBrush(QColor(self._text_avatar_color))
            painter.setBrush(brush)
            painter.drawRoundedRect(self.rect(), self._size, self._size)

            text_rect = painter.boundingRect(self.rect(), Qt.AlignmentFlag.AlignVCenter, self.text())
            text_rect = QRect(self.rect().left() + (self.rect().width()-text_rect.width())/2, 0, text_rect.width(), self.height())
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(Qt.white, 1))
            painter.drawText(text_rect, Qt.AlignVCenter, self.text())


        super().paintEvent(event)

        if self._badge:
            if self._badge in ['primary', 'secondary', 'info', 'success', 'warning', 'error']:
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing) 
                brush = QBrush(QColor(getattr(self.theme.palette, self._badge).main))
                painter.setBrush(brush)
                painter.drawRoundedRect(self._size*3/4,self._size*3/4,self._size/4,self._size/4,self._size/8,self._size/8)
            else:
                if self._mediumBadge:
                    pixmap = QPixmap(self._badge)
                    scaled_pixmap = pixmap.scaled(self._size/2,self._size/2, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                    painter = QPainter(self)
                    painter.setRenderHint(QPainter.Antialiasing) 
                    brush = QBrush()
                    brush.setStyle(Qt.Dense2Pattern)
                    brush.setTexture(scaled_pixmap)
                    painter.setBrush(brush)
                    painter.drawRoundedRect(self._size*2/4,self._size*2/4,self._size/2,self._size/2,self._size/4,self._size/4)
                else:
                    pixmap = QPixmap(self._badge)
                    scaled_pixmap = pixmap.scaled(self._size/4,self._size/4, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                    painter = QPainter(self)
                    painter.setRenderHint(QPainter.Antialiasing) 
                    brush = QBrush()
                    brush.setTexture(scaled_pixmap)
                    painter.setBrush(brush)
                    painter.drawRoundedRect(self._size*3/4,self._size*3/4,self._size/4,self._size/4,self._size/8,self._size/8)

            painter.end()