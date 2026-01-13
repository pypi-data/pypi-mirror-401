from functools import lru_cache
from typing import Callable

TYPES = ['button', 'iconbutton', 'fab', 'checkbox', 'radio']
# COLORS = ['inherit', 'default', 'primary', 'secondary', 'info', 'success', 'warning', 'error']
COLORS = ['default', 'primary', 'secondary', 'info', 'success', 'warning', 'error']
# VARIANTS = ['text', 'contained', 'outlined', 'soft', 'extended', 'softExtended', 'outlined', 'outlinedExtended']
VARIANTS = ['text', 'contained', 'outlined', 'soft']
SIZES = ['small', 'medium', 'large']
MODES = ['Light', 'Dark']

# @lru_cache(maxsize=128)
def _getButtonQss(
  theme, 
  _styledConfig: str="", 
  _variant: str="", 
  _size: str="", 
  _color: str="", 
  _theme_mode: str="", 
  _componentType: str = "Button", 
  _qssKey: str = "",
  get_qss_style: Callable = None
  ):
    
    ownerState = {
        "size": _size,
        "variant": _variant,
        "color": _color,
    }
    
    MuiButton_root = theme.components["MuiButton"].get("styles")["root"](ownerState)
    MuiButton_root_size_qss = get_qss_style(MuiButton_root["size"][_size])
    MuiButton_root_size_textVariant_qss = get_qss_style(MuiButton_root["size"][_size]["textVariant"])
    MuiButton_root_colorStyle_prop_variant_qss = get_qss_style(
        MuiButton_root["colorStyle"][_color]["props"][f"{_variant}Variant"]
    )
    MuiButton_root_colorStyle_prop_variant_slot_hover_qss = get_qss_style(
        MuiButton_root["colorStyle"][_color]["props"][f"{_variant}Variant"]["slots"]["hover"]
    )
    MuiButton_root_colorStyle_prop_variant_slot_checked_qss = get_qss_style(
        MuiButton_root["colorStyle"][_color]["props"][f"{_variant}Variant"]["slots"]["checked"]
    )
    
    IconButton_qss = ""
    Fab_qss = ""
    Checkbox_qss = ""
    Radio_qss = ""
    
    if _componentType == "IconButton":
        # icon_button_qss = get_qss_style(MuiButton_root["iconButton"])
        # icon_button_qss = icon_button_qss.replace("_________object_name_______", f"Button")
        # icon_button_qss = icon_button_qss.replace("MuiButton_root_colorStyle_prop_variant_slot_hover_qss", MuiButton_root_colorStyle_prop_variant_slot_hover_qss)
        # icon_button_qss = icon_button_qss.replace("MuiButton_root_colorStyle_prop_variant_slot_checked_qss", MuiButton_root_colorStyle_prop_variant_slot_checked_qss)
        # icon_button_qss = icon_button_qss.replace("MuiButton_root_size_textVariant_qss", MuiButton_root_size_textVariant_qss)
        # icon_button_qss = f'border-radius: {"15px" if self._size == "small" else "18px" if self._size == "medium" else "24px"};'

        if _color == "inherit":
            color = theme.palette.text.primary
        elif _color == "default":
            color = theme.palette.text.secondary
        elif _color in COLORS:
            color = getattr(theme.palette, _color).main
        else:
            color = theme.palette.text.secondary

        # thiết lập cho IconButton
        IconButton_qss = f"""
            Button{_qssKey} {{
                border-radius: {"15px" if _size == "small" else "18px" if _size == "medium" else "24px"};
                color: {color};
            }}
        """
    elif _componentType == "Fab":
        PyFab_styles_root_size_qss = get_qss_style(theme.components["PyFab"].get("styles")["root"]["props"][f"{_size}Size"])
        Fab_qss = f"""
            Button{_qssKey} {{
                {PyFab_styles_root_size_qss}
            }}
        """
    elif _componentType == "Checkbox":
        ownerState = {
            "size": _size
        }

        # component_styles[f"MuiCheckbox"].get("styleOverrides") or 
        MuiCheckbox = theme.components[f"MuiCheckbox"].get("styles")
        MuiCheckbox_root_qss = get_qss_style(theme.components[f"MuiCheckbox"].get("styles")["root"](ownerState)[_color])
        _text_color = MuiCheckbox["root"](ownerState)[_color]["color"]
        _icon_color = MuiCheckbox["icon"]["color"]

        _indicator_border_width = MuiCheckbox["checkedIndicator"]["border-width"]
        _indicator_border_radius = MuiCheckbox["checkedIndicator"]["border-radius"]
        _indicator_padding = MuiCheckbox["checkedIndicator"]["padding"]

        MuiCheckbox_root_override_qss = ""
        _icon_color_override = None
        _text_color_override = None
        if theme.components[f"MuiCheckbox"].get("styleOverrides"):
            MuiCheckbox_override = theme.components[f"MuiCheckbox"].get("styleOverrides")
            MuiCheckbox_root_override_qss = get_qss_style(MuiCheckbox_override["root"](ownerState)[_color])
            _text_color = MuiCheckbox_override["root"](ownerState)[_color].get("color") or _text_color

            if MuiCheckbox_override.get("icon"):
                _icon_color = MuiCheckbox_override["icon"].get("color") or _icon_color

            if MuiCheckbox_override.get("checkedIndicator"):
                _indicator_border_width = MuiCheckbox["checkedIndicator"].get("border-width") or _indicator_border_width
                _indicator_border_radius = MuiCheckbox["checkedIndicator"].get("border-radius") or _indicator_border_radius
                _indicator_padding = MuiCheckbox["checkedIndicator"].get("padding") or _indicator_padding


        Checkbox_qss = f"""
            Button{_qssKey} {{
                {MuiCheckbox_root_qss}
                {MuiCheckbox_root_override_qss}
                color: {_text_color};
            }}
        """

    elif _componentType == "RadioButton":
        PyRadio_root = theme.components[f"PyRadio"].get("styles")["root"](ownerState)
        PyRadio_root_qss = get_qss_style(PyRadio_root)
        # PyRadio_root_color_qss = PyRadio_root[_color]["color"]

        Radio_qss = f"""
            Button{_qssKey} {{
                {PyRadio_root_qss}
            }}
        """

    stylesheet = f"""
        Button{_qssKey}{{
            {MuiButton_root_size_qss}
            {MuiButton_root_size_textVariant_qss}
            {MuiButton_root_colorStyle_prop_variant_qss}
        }}
        Button{_qssKey}:hover {{
            {MuiButton_root_colorStyle_prop_variant_slot_hover_qss}
        }}
        Button{_qssKey}[selected=true] {{
            {MuiButton_root_colorStyle_prop_variant_slot_checked_qss}
        }}
        {IconButton_qss}
        {Fab_qss}
        {Checkbox_qss}
        {Radio_qss}
    """

    return stylesheet

def generateButtonQss(theme, get_qss_style):
    qss_files_content = ""

    for _type in TYPES:
        for _variant in VARIANTS:
            for _color in COLORS:
                for _size in SIZES:
                    for _mode in MODES:
                        _qssKey = f"[type={_type.lower()}][variant={_variant}][color={_color}][mode={_mode.lower()}]"
                        _theme_mode = _mode.lower()
                        _componentType = "Button"
                        if _type == "iconbutton":
                            _componentType = "IconButton"
                        elif _type == "fab":
                            _componentType = "Fab"
                        elif _type == "checkbox":
                            _componentType = "Checkbox"
                        elif _type == "radio":
                            _componentType = "RadioButton"

                        qss_content = _getButtonQss(
                            theme,
                            _styledConfig="",
                            _variant=_variant,
                            _size=_size,
                            _color=_color,
                            _theme_mode=_theme_mode,
                            _componentType=_componentType,
                            _qssKey=_qssKey,
                            get_qss_style=get_qss_style,
                        )
                        qss_files_content += qss_content

    return qss_files_content