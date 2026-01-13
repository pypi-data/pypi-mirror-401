import asyncio
from typing import Optional, Union, Callable, Any, Dict, List
import uuid

from qtmui.hooks import State, useEffect
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import Qt, QPixmap, QPainter, QPen, QBrush, QColor, QFont
from PySide6.QtCore import Qt, QRect, QSize, QByteArray, QTimer
from PySide6.QtSvg import QSvgRenderer

from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor

from ..system.color_manipulator import alpha
from ...common.icon import writeSvg
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from ..py_tool_button.py_tool_button import PyToolButton
from ..widget_base import PyWidgetBase

from ...qtmui_assets import QTMUI_ASSETS

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from ..utils.validate_params import _validate_param

class Badge(QPushButton, PyWidgetBase):
    """
    A component that displays a badge relative to a child node, with customizable content and positioning.

    The `Badge` component is used to highlight additional information, such as notifications or status,
    relative to a child component. It supports all props of the Material-UI `Badge` component, including
    additional props for icons, keys, and text. Native component props are supported via `**kwargs`.

    Parameters
    ----------
    anchorOrigin : State or dict, optional
        The anchor position of the badge. Must contain `vertical` ("top" or "bottom") and
        `horizontal` ("left" or "right"). Default is {"vertical": "top", "horizontal": "right"}.
        Can be a `State` object for dynamic updates.
    badgeContent : State or Any, optional
        The content rendered within the badge (e.g., text, number, or component). Default is None.
        Can be a `State` object for dynamic updates.
    children : State or Any, optional
        The node relative to which the badge is added. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color of the badge. Valid values: "default", "primary", "secondary", "error", "info",
        "success", "warning". Default is "default". Can be a `State` object for dynamic updates.
    component : State or Any, optional
        Component used for the root node (e.g., HTML element or custom component).
        Default is None. Can be a `State` object for dynamic updates.
    components : State or dict, optional
        Components used for each slot (e.g., Badge, Root). Deprecated: Use `slots` instead.
        Default is None. Can be a `State` object for dynamic updates.
    componentsProps : State or dict, optional
        Extra props for slot components (e.g., badge, root). Deprecated: Use `slotProps` instead.
        Default is None. Can be a `State` object for dynamic updates.
    invisible : State or bool, optional
        If True, the badge is invisible. Default is False.
        Can be a `State` object for dynamic updates.
    icon : State or str, optional
        Path to an SVG icon to display in the badge. Default is None.
        Can be a `State` object for dynamic updates.
    max : State or int, optional
        Maximum count to show in the badge. Default is 99.
        Can be a `State` object for dynamic updates.
    overlap : State or str, optional
        Shape the badge overlaps. Valid values: "circular", "rectangular". Default is "rectangular".
        Can be a `State` object for dynamic updates.
    key : State or str, optional
        Unique key for the component, used for internal purposes. Default is None.
        Can be a `State` object for dynamic updates.
    showZero : State or bool, optional
        If True, displays the badge when `badgeContent` is 0. Default is False.
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for each slot (e.g., badge, root). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for each slot (e.g., badge, root). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        Variant of the badge. Valid values: "dot", "standard". Default is "standard".
        Can be a `State` object for dynamic updates.
    text : State or str, optional
        Text to display in the badge. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QPushButton` class, supporting
        native component props (e.g., style, className).

    Attributes
    ----------
    VALID_VARIANTS : list[str]
        Valid values for the `variant` parameter: ["dot", "standard"].
    VALID_COLORS : list[str]
        Valid values for the `color` parameter: ["default", "primary", "secondary", "error",
        "info", "success", "warning"].
    VALID_OVERLAP : list[str]
        Valid values for the `overlap` parameter: ["circular", "rectangular"].
    VALID_ANCHOR_VERTICAL : list[str]
        Valid values for `anchorOrigin.vertical`: ["top", "bottom"].
    VALID_ANCHOR_HORIZONTAL : list[str]
        Valid values for `anchorOrigin.horizontal`: ["left", "right"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `components` and `componentsProps` props are deprecated; use `slots` and `slotProps` instead.
    - Additional props (`icon`, `key`, `text`) are specific to this implementation and not part of
      Material-UI `Badge`.

    Demos:
    - Badge: https://qtmui.com/material-ui/qtmui-badge/

    API Reference:
    - Badge API: https://qtmui.com/material-ui/api/badge/
    """

    VALID_VARIANTS = ["dot", "standard"]
    VALID_COLORS = ["default", "primary", "secondary", "error", "info", "success", "warning"]
    VALID_OVERLAP = ["circular", "rectangular"]
    VALID_ANCHOR_VERTICAL = ["top", "bottom"]
    VALID_ANCHOR_HORIZONTAL = ["left", "right"]

    def __init__(
        self,
        anchorOrigin: Union[State, Dict[str, str]] = None,
        badgeContent: Optional[Union[State, Any]] = None,
        children: Optional[Union[State, Any]] = None,
        classes: Optional[Union[State, Dict]] = None,
        color: Union[State, str] = "default",
        component: Optional[Union[State, Any]] = None,
        components: Optional[Union[State, Dict]] = None,
        componentsProps: Optional[Union[State, Dict]] = None,
        invisible: Union[State, bool] = False,
        icon: Optional[Union[State, str]] = None,
        max: Union[State, int] = 99,
        overlap: Union[State, str] = "rectangular",
        key: Optional[Union[State, str]] = None,
        showZero: Union[State, bool] = False,
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        variant: Union[State, str] = "standard",
        text: Optional[Union[str, State, Callable]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Set properties with validation
        self._set_anchorOrigin(anchorOrigin)
        self._set_badgeContent(badgeContent)
        self._set_children(children)
        self._set_classes(classes)
        self._set_color(color)
        self._set_component(component)
        self._set_components(components)
        self._set_componentsProps(componentsProps)
        self._set_invisible(invisible)
        self._set_icon(icon)
        self._set_max(max)
        self._set_overlap(overlap)
        self._set_key(key)
        self._set_showZero(showZero)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_sx(sx)
        self._set_variant(variant)
        self._set_text(text)

        self._size = 32

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

    # Setter and Getter methods for all parameters
    @_validate_param(file_path="qtmui.material.badge", param_name="anchorOrigin", supported_signatures=Union[State, Dict, type(None)])
    def _set_anchorOrigin(self, value):
        if value is None:
            value = {"vertical": "top", "horizontal": "right"}
        if isinstance(value, dict):
            if value.get("vertical") not in self.VALID_ANCHOR_VERTICAL:
                raise ValueError(f"anchorOrigin.vertical must be one of {self.VALID_ANCHOR_VERTICAL}")
            if value.get("horizontal") not in self.VALID_ANCHOR_HORIZONTAL:
                raise ValueError(f"anchorOrigin.horizontal must be one of {self.VALID_ANCHOR_HORIZONTAL}")
        self._anchorOrigin = value

    def _get_anchorOrigin(self):
        return self._anchorOrigin.value if isinstance(self._anchorOrigin, State) else self._anchorOrigin

    # @_validate_param(file_path="qtmui.material.badge", param_name="badgeContent", supported_signatures=Union[State, Any, type(None)])
    def _set_badgeContent(self, value):
        self._badgeContent = value

    def _get_badgeContent(self):
        return self._badgeContent.value if isinstance(self._badgeContent, State) else self._badgeContent

    # @_validate_param(file_path="qtmui.material.badge", param_name="children", supported_signatures=Union[State, Any, type(None)])
    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.badge", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.badge", param_name="color", supported_signatures=Union[State, str], valid_values=VALID_COLORS)
    def _set_color(self, value):
        self._color = value

    def _get_color(self):
        return self._color.value if isinstance(self._color, State) else self._color

    # @_validate_param(file_path="qtmui.material.badge", param_name="component", supported_signatures=Union[State, Any, type(None)])
    def _set_component(self, value):
        self._component = value

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.badge", param_name="components", supported_signatures=Union[State, Dict, type(None)])
    def _set_components(self, value):
        self._components = value or {}

    def _get_components(self):
        return self._components.value if isinstance(self._components, State) else self._components

    @_validate_param(file_path="qtmui.material.badge", param_name="componentsProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_componentsProps(self, value):
        self._componentsProps = value or {}

    def _get_componentsProps(self):
        return self._componentsProps.value if isinstance(self._componentsProps, State) else self._componentsProps

    @_validate_param(file_path="qtmui.material.badge", param_name="invisible", supported_signatures=Union[State, bool])
    def _set_invisible(self, value):
        self._invisible = value

    def _get_invisible(self):
        return self._invisible.value if isinstance(self._invisible, State) else self._invisible

    @_validate_param(file_path="qtmui.material.badge", param_name="icon", supported_signatures=Union[State, str, type(None)])
    def _set_icon(self, value):
        self._icon = value

    def _get_icon(self):
        return self._icon.value if isinstance(self._icon, State) else self._icon

    @_validate_param(file_path="qtmui.material.badge", param_name="max", supported_signatures=Union[State, int])
    def _set_max(self, value):
        self._max = value

    def _get_max(self):
        return self._max.value if isinstance(self._max, State) else self._max

    @_validate_param(file_path="qtmui.material.badge", param_name="overlap", supported_signatures=Union[State, str], valid_values=VALID_OVERLAP)
    def _set_overlap(self, value):
        self._overlap = value

    def _get_overlap(self):
        return self._overlap.value if isinstance(self._overlap, State) else self._overlap

    @_validate_param(file_path="qtmui.material.badge", param_name="key", supported_signatures=Union[State, str, type(None)])
    def _set_key(self, value):
        self._key = value

    def _get_key(self):
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.badge", param_name="showZero", supported_signatures=Union[State, bool])
    def _set_showZero(self, value):
        self._showZero = value

    def _get_showZero(self):
        return self._showZero.value if isinstance(self._showZero, State) else self._showZero

    @_validate_param(file_path="qtmui.material.badge", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value or {}

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.badge", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value or {}

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.badge", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    # @_validate_param(file_path="qtmui.material.badge", param_name="variant", supported_signatures=Union[State, str], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        self._variant = value

    def _get_variant(self):
        return self._variant.value if isinstance(self._variant, State) else self._variant

    @_validate_param(file_path="qtmui.material.badge", param_name="text", supported_signatures=Union[State, str, type(None)])
    def _set_text(self, value):
        self._text = value

    def _get_text(self):
        return self._text.value if isinstance(self._text, State) else self._text

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))
        if self._children:
            self.setFixedSize(QSize(self._size, self._size))
        else:
            if self._badgeContent and len(self._badgeContent) > 1:
                self.setFixedHeight(self._size)
            elif self._text:
                self.setFixedHeight(self._size)
            else:
                self.setFixedSize(QSize(self._size, self._size))


    def retranslateUi(self):
        if self._text:
            if isinstance(self._text, Callable):
                self.setText(translate(self._text))
            else:
                self.setText(self._text)


    def _get_variant_icon(self, variant):
        icons = {
            "online": QTMUI_ASSETS.ICONS.ONLINE,
            "alway": QTMUI_ASSETS.ICONS.ALWAY,
            "busy": QTMUI_ASSETS.ICONS.BUSY,
            "offline": QTMUI_ASSETS.ICONS.OFFLINE,
        }
        return icons[variant]
    
    def _get_variant_color(self, variant):
        icons = {
            "online": "#05c46b",
            "alway": "#00d8d6",
            "busy": "#ff5e57",
            "offline": "#d2dae2"
        }
        return icons[variant]


    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        MuiFormControlLabel = component_styled[f"MuiFormControlLabel"].get("styles")
        MuiFormControlLabelRootStyle = get_qss_style(MuiFormControlLabel["label"])

        ownerState = {
            "size": self._size
        }

        PyBadge = component_styled[f"PyBadge"].get("styles")
        PyBadge_root = PyBadge["root"](ownerState)[self._color]
        PyBadge_root_qss = get_qss_style(PyBadge_root)
        PyBadge_root_prop_has_icon_qss = get_qss_style(PyBadge_root["props"]["hasIcon"])
        PyBadge_root_prop_has_text_qss = get_qss_style(PyBadge_root["props"]["hasText"])

        self._text_color = PyBadge_root.get("color")
        self._background_color = PyBadge_root.get("background-color")

        if self._variant in ["alway", "online", "busy", "offline"]:
            self._status_variant_color = PyBadge_root["props"][f"{self._variant}Variant"]["color"]

        if self._icon:
            self.setProperty("hasIcon", "true")
        if self._text:
            self.setProperty("hasText", "true")

        if self._variant == "online":
            self.setProperty("variant", "offline")
        elif self._variant == "busy":
            self.setProperty("variant", "busy")
        elif self._variant == "offline":
            self.setProperty("variant", "offline")
        elif self._variant == "alway":
            self.setProperty("variant", "alway")
        else: # invisible
            self.setProperty("variant", "invisible")

        if self._text == "Typography":
            print('self._text_color________', self._text_color)

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
            #{self.objectName()}[hasIcon=true] {{
                {PyBadge_root_prop_has_icon_qss}
            }}
            #{self.objectName()}[hasText=true] {{
                color: {self._text_color};
                {PyBadge_root_prop_has_text_qss}
            }}
            #{self.objectName()}[variant=online] {{
            }}
            #{self.objectName()}[variant=busy] {{
            }}
            #{self.objectName()}[variant=offline] {{
            }}
            #{self.objectName()}[variant=alway] {{
            }}
            #{self.objectName()}[variant=invisible] {{
            }}

            {sx_qss}

        """
        self.setStyleSheet(stylesheet)
        self.update()

    def paintEvent(self, event):
        if not hasattr(self, "theme") or not hasattr(self, "_background_color"):
            self._set_stylesheet()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self._variant:
            if self._variant in ["alway", "online", "busy", "offline"]:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(QColor(Qt.gray)))
                painter.drawRoundedRect(0,0,self._size,self._size,self._size/2,self._size/2)

                # Thay đổi màu fill của SVG thành màu mong muốn
                # updated_svg_content = change_svg_color(svg_content, self._text_color)
                updated_svg_content = writeSvg(self._get_variant_icon(self._variant), fill=self._status_variant_color)
                # Tạo QByteArray từ nội dung SVG đã thay đổi
                svg_data = QByteArray(updated_svg_content.encode("utf-8"))
                # Sử dụng QSvgRenderer để render SVG với màu mới
                svg_renderer = QSvgRenderer(svg_data)
                svg_renderer.render(painter, QRect(self._size*3.2/5,self._size*3.2/5,self._size*2/5,self._size*2/5))  # Vẽ SVG vào button
                # painter.drawRoundedRect(self._size*2/4,self._size*2/4,self._size/2,self._size/2,self._size/4,self._size/4)
        if self._children:
            # Render button khác thành một QPixmap
            pixmap = QPixmap(QSize(self._size, self._size))  # Tạo QPixmap có kích thước như button khác
            self._children.render(pixmap)  # Render button khác vào QPixmap
            # Vẽ QPixmap của button khác lên button hiện tại
            # painter.drawPixmap(QRect(0, 0, pixmap.width(), pixmap.height()), pixmap)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(Qt.darkYellow)))
            if self._overlap == "circular":
                painter.drawRoundedRect(0,0,self._size,self._size,self._size/2,self._size/2)
            else:
                painter.drawRect(QRect(self._size/8, self._size/8, pixmap.width()-self._size/4, pixmap.height()-self._size/4))

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(self._background_color)))
            painter.drawRoundedRect(self._size*3/4,0,self._size/4,self._size/4,self._size/8,self._size/8)
        else:
            badge_w = 0
            if self._badgeContent and len(self._badgeContent) > 1:
                badge_w = len(self._badgeContent) * 5
            self.setMinimumWidth(self._size + badge_w)

            badge_pos_x_text_mode = 0
            if self._text and len(self._text) > 1:
                badge_pos_x_text_mode = len(self._text) * 6

                self.setMinimumWidth(self._size + badge_pos_x_text_mode)

            if self._icon:
                pixmap = QPixmap(self._icon)
                scaled_pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                # painter.setPen(Qt.NoPen)
                # brush = QBrush(QColor("#000000"))
                # brush.setStyle(Qt.Dense2Pattern)
                # brush.setTexture(scaled_pixmap)
                # painter.setBrush(brush)
                # painter.drawRoundedRect(self.rect(), self._size, self._size)

                # draw giữ nguyên màu sgv
                # painter.drawPixmap(self.rect(), scaled_pixmap)



                # Thay đổi màu fill của SVG thành màu mong muốn
                # updated_svg_content = change_svg_color(svg_content, self._text_color)
                updated_svg_content = writeSvg(self._icon, fill=self.theme.palette.text.secondary)
                # Tạo QByteArray từ nội dung SVG đã thay đổi
                svg_data = QByteArray(updated_svg_content.encode("utf-8"))
                # Sử dụng QSvgRenderer để render SVG với màu mới
                svg_renderer = QSvgRenderer(svg_data)
                svg_renderer.render(painter, self.rect().adjusted(5,5,-badge_w-5,-5))  # Vẽ SVG vào button

            if self._variant == "dot":
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(QColor(self._background_color)))
                painter.drawRoundedRect(self._size*3/4+badge_pos_x_text_mode,0,self._size/4,self._size/4,self._size/8,self._size/8)

            elif self._badgeContent:
                painter.setPen(Qt.NoPen)
                brush = QBrush(QColor(self._background_color))
                painter.setBrush(brush)
                painter.drawRoundedRect(self._size/2,0,self._size/2+badge_w,self._size/2,self._size/4,self._size/4)

                # Ghi đè font-size của QPushButton cha
                custom_font = QFont(self.font())  # Lấy font của QPushButton cha
                custom_font.setPointSize(10)  # Thay đổi kích thước font, ví dụ: 12px
                painter.setFont(custom_font)  # Áp dụng font mới cho painter

                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(Qt.white, 1))
                painter.drawText(QRect(self._size*3/4 - self._size/8,0,self._size/2+badge_w,self._size/2), Qt.AlignVCenter, self._badgeContent)

        super().paintEvent(event)
