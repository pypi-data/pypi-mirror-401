from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Callable, Union

from .shape import ShapeOptions, Shape
from .create_breakpoints import BreakpointsOptions, Breakpoints
from .create_spacing import SpacingOptions, Spacing
from ..style_function_sx.style_function_sx import SxProps
from ..style_function_sx.default_sx_config import SxConfig
from .apply_styles import ApplyStyles

class Direction:
    ltr = "ltr"
    rtl = "rtl"
# Direction = Union['ltr', 'rtl']


# ThemeOptions dataclass equivalent
@dataclass
class ThemeOptions:
    shape: Optional[ShapeOptions] = None
    breakpoints: Optional[BreakpointsOptions] = None
    direction: Optional[Direction] = 'ltr'
    mixins: Optional[Any] = None
    palette: Optional[Dict[str, Any]] = field(default_factory=dict)
    shadows: Optional[Any] = None
    spacing: Optional[SpacingOptions] = None
    transitions: Optional[Any] = None
    components: Optional[Dict[str, Any]] = field(default_factory=dict)
    typography: Optional[Any] = None
    zIndex: Optional[Dict[str, int]] = field(default_factory=dict)
    unstable_sxConfig: Optional[SxConfig] = None

# Theme dataclass equivalent
@dataclass
class Theme:
    shape: Shape
    breakpoints: Breakpoints
    direction: Direction
    palette: Dict[str, Any]
    shadows: Optional[Any] = None
    spacing: Spacing = field(default_factory=Spacing)
    transitions: Optional[Any] = None
    components: Optional[Dict[str, Any]] = field(default_factory=dict)
    mixins: Optional[Any] = None
    typography: Optional[Any] = None
    zIndex: Optional[Dict[str, int]] = field(default_factory=dict)
    applyStyles: Optional[Callable[[str], ApplyStyles]] = None
    unstable_sxConfig: Optional[SxConfig] = None
    unstable_sx: Optional[Callable[[SxProps], Dict[str, Any]]] = None


def createTheme(options: Optional[ThemeOptions] = None, *args: Any) -> Theme:
    options = options or ThemeOptions()
    
    # Create Shape, Breakpoints, and other components
    shape = Shape() if options.shape is None else options.shape
    breakpoints = Breakpoints() if options.breakpoints is None else options.breakpoints
    
    palette = options.palette or {"mode": "light"}
    direction = options.direction or "ltr"
    shadows = options.shadows
    spacing = Spacing() if options.spacing is None else options.spacing
    typography = options.typography
    zIndex = options.zIndex or {}
    components = options.components or {}
    
    # Create and return the full Theme object
    return Theme(
        shape=shape,
        breakpoints=breakpoints,
        direction=direction,
        palette=palette,
        shadows=shadows,
        spacing=spacing,
        typography=typography,
        zIndex=zIndex,
        components=components,
        applyStyles=None,  # Can be updated later
        unstable_sxConfig=options.unstable_sxConfig,
        unstable_sx=None  # Can be updated later
    )