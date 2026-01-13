from dataclasses import dataclass, field
from typing import Callable, Optional, Union, Dict

from ....material.system.color_manipulator import get_contrast_text

# Định nghĩa các class và kiểu dữ liệu cần thiết

@dataclass
class CommonColors:
    black: str = "#000000"
    white: str = "#ffffff"

@dataclass
class Color:
    _50: str = ""
    _100: str = ""
    _200: str = ""
    _300: str = ""
    _400: str = ""
    _500: str = ""
    _600: str = ""
    _700: str = ""
    _800: str = ""
    _900: str = ""

@dataclass
class PaletteColor:
    light: Optional[str] = None
    lighter: Optional[str] = None
    main: str = ""
    dark: Optional[str] = None
    darker: Optional[str] = None
    contrastText: Optional[str] = None

@dataclass
class TypeText:
    primary: str = ""
    secondary: str = ""
    disabled: str = ""

@dataclass
class TypeAction:
    active: str = ""
    hover: str = ""
    hoverOpacity: float = 0.0
    selected: str = ""
    selectedOpacity: float = 0.0
    disabled: str = ""
    disabledBackground: str = ""
    disabledOpacity: float = 0.0
    focus: str = ""
    focusOpacity: float = 0.0
    activatedOpacity: float = 0.0

@dataclass
class TypeBackground:
    default: str = ""
    paper: str = ""
    notched: str = ""
    neutral: str = ""
    navigation: str = ""
    main: str = ""
    second: str = ""
    thirty: str = ""
    content: str = ""
    transparent: str = "transparent"
    
@dataclass
class Palette:
    common: CommonColors
    mode: str
    contrastThreshold: float
    tonalOffset: Union[float, Dict[str, float]]
    primary: PaletteColor
    secondary: PaletteColor
    error: PaletteColor
    warning: PaletteColor
    info: PaletteColor
    success: PaletteColor
    grey: Color
    text: TypeText
    divider: str
    action: TypeAction
    background: TypeBackground
    getContrastText: Callable[[str], str]
    augmentColor: Callable[[Dict], PaletteColor]

# Hàm để tạo ra các màu mặc định

def get_default_primary(mode: str = 'light') -> PaletteColor:
    if mode == 'dark':
        return PaletteColor(main="#90caf9", light="#e3f2fd", dark="#42a5f5")
    return PaletteColor(main="#1976d2", light="#63a4ff", dark="#004ba0")

def get_default_secondary(mode: str = 'light') -> PaletteColor:
    if mode == 'dark':
        return PaletteColor(main="#f48fb1", light="#f8bbd0", dark="#f06292")
    return PaletteColor(main="#dc004e", light="#ff5983", dark="#9a0036")

def get_default_error(mode: str = 'light') -> PaletteColor:
    if mode == 'dark':
        return PaletteColor(main="#ef5350", light="#e57373", dark="#d32f2f")
    return PaletteColor(main="#d32f2f", light="#ef5350", dark="#c62828")

# Hàm tính toán tỷ lệ tương phản


# Hàm để lấy màu chữ tương phản



# Hàm augmentColor

def augment_color(options: Dict) -> PaletteColor:
    color = options.get('color', {})
    if not color.get('main'):
        color['main'] = color.get(500, "")
    if not color['main']:
        raise ValueError(f"MUI: Invalid color. The color object needs to have a `main` property.")
    return PaletteColor(
        main=color['main'],
        light=color.get('light', None),
        lighter=color.get('lighter', None),
        dark=color.get('dark', None),
        darker=color.get('darker', None),
        contrastText=get_contrast_text(color['main'])
    )

def augment_text_color(options: Dict) -> PaletteColor:
    return TypeText(
        primary=options.get('primary', None),
        secondary=options.get('secondary', None),
        disabled=options.get('disabled', None),
    )

# Tạo hàm create_palette để khởi tạo một đối tượng Palette

def create_palette(palette: Dict) -> Palette:
    mode = palette.get('mode', 'light')
    contrastThreshold = palette.get('contrastThreshold', 3)
    tonalOffset = palette.get('tonalOffset', 0.2)

    primary = palette.get('primary', get_default_primary(mode))
    secondary = palette.get('secondary', get_default_secondary(mode))
    error = palette.get('error', get_default_error(mode))

    text = palette.get('text', TypeText(primary="#000000", secondary="#757575", disabled="#bdbdbd"))
    
    grey_colors = Color(
        _50="#FFFFFF",
        _100="#F9FAFB",
        _200="#F4F6F8",
        _300="#DFE3E8",
        _400="#C4CDD5",
        _500="#919EAB",
        _600="#637381",
        _700="#454F5B",
        _800="#212B36",
        _900="#161C24"
    )
    
    return Palette(
        common=CommonColors(),
        mode=mode,
        contrastThreshold=contrastThreshold,
        tonalOffset=tonalOffset,
        primary=augment_color({"color": primary}),
        secondary=augment_color({"color": secondary}),
        error=augment_color({"color": error}),
        warning=augment_color({"color": palette.get('warning', get_default_error(mode))}),
        info=augment_color({"color": palette.get('info', get_default_primary(mode))}),
        success=augment_color({"color": palette.get('success', get_default_primary(mode))}),
        grey=grey_colors,
        text=augment_text_color(palette.get('text')),
        divider="#e0e0e0",
        action=TypeAction(
            active="#000000",
            hover="rgba(0, 0, 0, 0.04)",
            hoverOpacity=0.08,
            selected="rgba(0, 0, 0, 0.08)",
            selectedOpacity=0.08,
            disabled="rgba(0, 0, 0, 0.26)",
            disabledBackground="rgba(0, 0, 0, 0.12)",
            disabledOpacity=0.38,
            focus="rgba(0, 0, 0, 0.12)",
            focusOpacity=0.12,
            activatedOpacity=0.48
        ),
        background=TypeBackground(
            default=palette["background"]["default"], 
            paper=palette["background"]["paper"],
            neutral=palette["background"]["neutral"],
            notched=palette["background"]["notched"],
            navigation=palette["background"]["navigation"],
            main=palette["background"]["main"],
            second=palette["background"]["second"],
            thirty=palette["background"]["thirty"],
            content=palette["background"]["content"]
        ),
        getContrastText=get_contrast_text,
        augmentColor=augment_color
    )

# # # Ví dụ khởi tạo palette
# my_palette = create_palette({
#     'mode': 'light',
#     'primary': {'main': '#1976d2'},
#     'secondary': {'main': '#dc004e'}
# })
