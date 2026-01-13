from dataclasses import dataclass, field, is_dataclass, asdict, replace
from typing import Literal, Optional, Dict, Any, Callable, Union

import threading
from immutable import Immutable
import uuid
from redux import ReducerResult, CompleteReducerResult, BaseAction, BaseEvent, Store
from typing import Callable, Sequence, Optional

from PySide6.QtCore import QPoint, QSize
from PySide6.QtGui import QColor

from qtmui.utils.lodash import merge, dataclass_to_dict

from .shape import ShapeOptions, Shape
from .create_breakpoints import BreakpointsOptions, Breakpoints
from .create_spacing import SpacingOptions, Spacing, create_spacing
from ..style_function_sx.style_function_sx import SxProps
from ..style_function_sx.default_sx_config import SxConfig
from .apply_styles import ApplyStyles
from .typography import Typography
from .palette import palette
from .create_palette import create_palette, Palette
from .create_size import create_size, Sizes
from .create_shadows import create_shadows, Shadows
from .create_root_component_styles import create_root_component_styles


class Direction:
    ltr = "ltr"
    rtl = "rtl"
# Direction = Union['ltr', 'rtl']


# ThemeOptions dataclass equivalent
# @dataclass
class ThemeOptions(Immutable):
    shape: Optional[ShapeOptions] = None
    breakpoints: Optional[BreakpointsOptions] = None
    direction: Optional[Direction] = 'ltr'
    mixins: Optional[Any] = None
    palette: Optional[Dict[str, Any]] = field(default_factory=dict)
    customShadows: Optional[Shadows] = None
    spacing: Optional[SpacingOptions] = None
    createSpacing: Optional[Callable] = None
    transitions: Optional[Any] = None
    components: Optional[Dict[str, Any]] = field(default_factory=dict)
    typography: Optional[Any] = None
    zIndex: Optional[Dict[str, int]] = field(default_factory=dict)
    unstable_sxConfig: Optional[SxConfig] = None
    size: Optional[Dict[str, Any]] = field(default_factory=dict)

class Context(Immutable):
    mainwindow_pos: Optional[ShapeOptions] = None
    mainwindow_size: Optional[ShapeOptions] = None

class Changed(Immutable):
    connect: Optional[object] = None

class Signal(Immutable):
    changed: Optional[Changed] = None

# Cập nhật ThemeState để sử dụng Palette thay vì Dict
# @dataclass(frozen=True)
class ThemeState(Immutable):
    state: Optional[Signal] = None
    context: Context
    shape: Shape
    breakpoints: Breakpoints
    direction: Direction
    palette: Palette  # palette giờ là class Palette thay vì Dict
    customShadows: Optional[Shadows] = None
    spacing: Spacing = field(default_factory=Spacing)
    transitions: Optional[Any] = None
    components: Optional[Dict[str, Any]] = field(default_factory=dict)
    mixins: Optional[Any] = None
    typography: Typography = None
    zIndex: Optional[Dict[str, int]] = field(default_factory=dict)
    applyStyles: Optional[Callable[[str], ApplyStyles]] = None
    unstable_sxConfig: Optional[SxConfig] = None
    unstable_sx: Optional[Callable[[SxProps], Dict[str, Any]]] = None
    size: Optional[Sizes] = create_size()


class CreateThemeAction(BaseAction):
    pass

class ChangePaletteAction(BaseAction):
    mode: Literal['light', 'dark']  # Chỉ cho phép 'light' hoặc 'dark'

class MergeOverideComponentsAction(BaseAction):
    payload: Dict

class UpdateMainwindowPositionAction(BaseAction):
    mainWindowPosition: QPoint

def createTheme(options: Optional[ThemeOptions] = None, *args: Any) -> ThemeState:
    options = options or ThemeOptions()
    
    # Create Shape, Breakpoints, and other components
    context = Context()
    shape = Shape() if options.shape is None else options.shape
    breakpoints = Breakpoints() if options.breakpoints is None else options.breakpoints
    
    palette = options.palette or {"mode": "light"}
    direction = options.direction or "ltr"
    customShadows = options.customShadows
    spacing = Spacing() if options.spacing is None else options.spacing
    typography = options.typography
    zIndex = options.zIndex or {}
    components = options.components or {}
    
    # Create and return the full Theme object
    return ThemeState(
        context=context,
        shape=shape,
        breakpoints=breakpoints,
        direction=direction,
        palette=palette,
        customShadows=customShadows,
        spacing=spacing,
        typography=typography,
        zIndex=zIndex,
        components=components,
        applyStyles=None,  # Can be updated later
        unstable_sxConfig=options.unstable_sxConfig,
        unstable_sx=None  # Can be updated later
    )

def theme_reducer(
    state: ThemeState | None,
    action: BaseAction,
) -> ReducerResult[ThemeState, BaseAction, BaseEvent]:
    if state is None:
        _palette = create_palette(palette("light"))
        state = createTheme(ThemeOptions(
            shape=ShapeOptions(borderRadius=4),
            breakpoints=BreakpointsOptions(),
            palette=_palette,
            typography=Typography(),
            # createSpacing=create_spacing(),  # Sử dụng đối tượng Spacing thay vì SpacingOptions
            spacing=Spacing(),  # Sử dụng đối tượng Spacing thay vì SpacingOptions
            size=create_size(),
            customShadows=create_shadows(_palette)
        ))
        root_component_styles = create_root_component_styles(state)
        return replace(state, components=root_component_styles)


    if isinstance(action, CreateThemeAction):
        pass
    if isinstance(action, ChangePaletteAction):
        _palette = create_palette(palette(action.mode))
        state = replace(
                state, 
                palette=_palette,
                customShadows=create_shadows(_palette)
            )
        root_component_styles = create_root_component_styles(state)
        # print('root_component_stylesf____________', root_component_styles)
        return replace(state, components=root_component_styles)

    if isinstance(action, MergeOverideComponentsAction):
        _palette = action.payload.get("palette")
        _components = action.payload.get("components")
        if _components and isinstance(_components, dict):
            state = replace(state, components=_components)
        if _palette and isinstance(_palette, dict):
            current_palette_dict = dataclass_to_dict(state.palette)
            # merge sâu
            merged_palette = merge(current_palette_dict, _palette)
            # tái tạo lại Palette object
            new_palette = create_palette(merged_palette)
            # print('new_palettet__', merged_palette)
            state = replace(state, palette=new_palette)
    
    if isinstance(action, UpdateMainwindowPositionAction):
        return replace(state, context=replace(state.context, mainwindow_pos=action.mainWindowPosition))

    return state
