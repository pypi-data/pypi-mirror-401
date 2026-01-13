import sys
import math
from dataclasses import dataclass, field
from typing import Dict, List, Union, Callable, Optional, Any, Tuple

from PySide6.QtCore import QObject, Property, QVariantAnimation, QEasingCurve
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFont
from PySide6.QtCore import QRectF, Qt

Number = Union[int, float]


# ============================================================
# 0) Helpers: CSS value parsing (px, %, rgba, shorthand...)
# ============================================================
def _to_str(v) -> str:
    return "" if v is None else str(v).strip()

def _parse_px(v, default: float = 0.0) -> float:
    if v is None:
        return default
    if isinstance(v, (int, float)):
        return float(v)
    s = _to_str(v).lower()
    if s.endswith("px"):
        s = s[:-2].strip()
    # allow "12.5"
    try:
        return float(s)
    except ValueError:
        return default

def _parse_percent(v, default: float = 0.0) -> float:
    # returns 0..1
    if v is None:
        return default
    if isinstance(v, (int, float)):
        # if they pass 0.5 treat as ratio
        x = float(v)
        return x if 0.0 <= x <= 1.0 else x / 100.0
    s = _to_str(v).lower()
    if s.endswith("%"):
        try:
            return float(s[:-1].strip()) / 100.0
        except ValueError:
            return default
    try:
        x = float(s)
        return x if 0.0 <= x <= 1.0 else x / 100.0
    except ValueError:
        return default

def _parse_color(v, default: str = "transparent") -> QColor:
    if v is None:
        return QColor(default)
    if isinstance(v, QColor):
        return QColor(v)
    s = _to_str(v)
    c = QColor(s)
    return c if c.isValid() else QColor(default)

def _parse_bool(v, default: bool = False) -> bool:
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    s = _to_str(v).lower()
    if s in ("1", "true", "yes", "on"):
        return True
    if s in ("0", "false", "no", "off"):
        return False
    return default

def _parse_enum(v, allowed: set, default):
    s = _to_str(v).lower()
    return s if s in allowed else default

def _parse_spacing(v, default=(0, 0, 0, 0)) -> Tuple[float, float, float, float]:
    """
    CSS shorthand:
      - 1 value: all
      - 2 values: top/bottom, left/right
      - 3 values: top, left/right, bottom
      - 4 values: top, right, bottom, left
    Accepts number, "12px", "8 12", "8px 12px 4px 2px"
    Returns (top, right, bottom, left)
    """
    if v is None:
        return default
    if isinstance(v, (int, float)):
        x = float(v)
        return (x, x, x, x)

    s = _to_str(v)
    parts = s.replace(",", " ").split()
    nums = [_parse_px(p, None) for p in parts]
    nums = [x for x in nums if x is not None]

    if len(nums) == 1:
        a = nums[0]; return (a, a, a, a)
    if len(nums) == 2:
        a, b = nums; return (a, b, a, b)
    if len(nums) == 3:
        a, b, c = nums; return (a, b, c, b)
    if len(nums) >= 4:
        a, b, c, d = nums[:4]; return (a, b, c, d)
    return default

def _parse_border(v: Any) -> Tuple[float, str, QColor]:
    """
    Supports:
      - "2px solid white"
      - {"width":"2px","style":"solid","color":"white"}
    Returns: (width, style, color)
    """
    if v is None:
        return (0.0, "solid", QColor("transparent"))

    if isinstance(v, dict):
        w = _parse_px(v.get("width"), 0.0)
        style = _parse_enum(v.get("style"), {"none", "solid", "dashed", "dotted"}, "solid")
        c = _parse_color(v.get("color"), "transparent")
        return (w, style, c)

    s = _to_str(v)
    parts = s.split()
    w = 0.0
    style = "solid"
    c = QColor("white")
    for p in parts:
        pl = p.lower()
        if pl.endswith("px"):
            try:
                w = float(pl[:-2])
            except ValueError:
                pass
        elif pl in ("none", "solid", "dashed", "dotted"):
            style = pl
        else:
            cc = QColor(p)
            if cc.isValid():
                c = cc
    return (w, style, c)

def _parse_box_shadow(v: Any):
    """
    Subset: "offsetX offsetY blur spread color"
    Example: "0px 8px 24px 0px rgba(0,0,0,0.25)"
    We'll parse numbers + last token color (best-effort).
    Returns: (ox, oy, blur, spread, color, enabled)
    """
    if v is None:
        return (0.0, 0.0, 0.0, 0.0, QColor("transparent"), False)

    s = _to_str(v)
    parts = s.split()
    nums = []
    col = None
    for p in parts:
        if p.lower().endswith("px") or p.replace(".", "", 1).isdigit():
            nums.append(_parse_px(p, 0.0))
        else:
            # try color
            c = QColor(p)
            if c.isValid():
                col = c

    while len(nums) < 4:
        nums.append(0.0)
    ox, oy, blur, spread = nums[:4]
    color = col if col is not None else QColor(0, 0, 0, 80)
    return (ox, oy, blur, spread, color, True)


# ============================================================
# 1) Style model: CSS subset for QtMUI widgets
# ============================================================
@dataclass
class ComputedStyle:
    # size
    width: Optional[float] = None
    height: Optional[float] = None
    min_width: Optional[float] = None
    min_height: Optional[float] = None
    max_width: Optional[float] = None
    max_height: Optional[float] = None

    # box model
    margin: Tuple[float, float, float, float] = (0, 0, 0, 0)   # t r b l
    padding: Tuple[float, float, float, float] = (0, 0, 0, 0)  # t r b l

    # background
    background_color: QColor = field(default_factory=lambda: QColor("transparent"))

    # border
    border_width: float = 0.0
    border_style: str = "solid"     # none/solid/dashed/dotted
    border_color: QColor = field(default_factory=lambda: QColor("transparent"))
    border_radius: float = 0.0      # px only in this subset

    # outline (subset)
    outline_width: float = 0.0
    outline_color: QColor = field(default_factory=lambda: QColor("transparent"))

    # opacity / visibility
    opacity: float = 1.0
    visibility: str = "visible"     # visible/hidden
    overflow: str = "visible"       # visible/hidden

    # transform base from sx (static) + dynamic from variants
    translate_x: float = 0.0
    translate_y: float = 0.0
    rotate: float = 0.0             # degrees
    scale_x: float = 1.0
    scale_y: float = 1.0

    # shadow (subset)
    shadow_enabled: bool = False
    shadow: bool = False
    shadow_ox: float = 0.0
    shadow_oy: float = 0.0
    shadow_blur: float = 0.0
    shadow_spread: float = 0.0
    shadow_color: QColor = field(default_factory=lambda: QColor("transparent"))

    # typography (subset)
    color: QColor = field(default_factory=lambda: QColor("white"))
    font_size: float = 14.0
    font_weight: int = 400
    line_height: float = 1.2
    text_align: str = "left"        # left/center/right

    # misc (subset)
    cursor: str = "default"
    user_select: str = "auto"

    # store unknown props for later extension
    extra: Dict[str, Any] = field(default_factory=dict)


def parse_sx(sx: dict) -> ComputedStyle:
    st = ComputedStyle()

    # sizing
    if "width" in sx: st.width = _parse_px(sx.get("width"), None)
    if "height" in sx: st.height = _parse_px(sx.get("height"), None)
    if "minWidth" in sx or "min-width" in sx:
        st.min_width = _parse_px(sx.get("minWidth", sx.get("min-width")), None)
    if "minHeight" in sx or "min-height" in sx:
        st.min_height = _parse_px(sx.get("minHeight", sx.get("min-height")), None)
    if "maxWidth" in sx or "max-width" in sx:
        st.max_width = _parse_px(sx.get("maxWidth", sx.get("max-width")), None)
    if "maxHeight" in sx or "max-height" in sx:
        st.max_height = _parse_px(sx.get("maxHeight", sx.get("max-height")), None)

    # spacing
    if "margin" in sx: st.margin = _parse_spacing(sx.get("margin"), st.margin)
    if "padding" in sx: st.padding = _parse_spacing(sx.get("padding"), st.padding)

    # background
    if "background" in sx:
        # allow "background" as a color in this subset
        st.background_color = _parse_color(sx.get("background"), "transparent")
    if "background-color" in sx:
        st.background_color = _parse_color(sx.get("background-color"), "transparent")
    if "bgcolor" in sx:
        st.background_color = _parse_color(sx.get("bgcolor"), "transparent")

    # border
    if "border" in sx:
        bw, bstyle, bc = _parse_border(sx.get("border"))
        st.border_width, st.border_style, st.border_color = bw, bstyle, bc
    if "border-width" in sx: st.border_width = _parse_px(sx.get("border-width"), st.border_width)
    if "border-style" in sx: st.border_style = _parse_enum(sx.get("border-style"), {"none","solid","dashed","dotted"}, st.border_style)
    if "border-color" in sx: st.border_color = _parse_color(sx.get("border-color"), "transparent")

    if "border-radius" in sx: st.border_radius = _parse_px(sx.get("border-radius"), st.border_radius)
    if "borderRadius" in sx: st.border_radius = _parse_px(sx.get("borderRadius"), st.border_radius)
    
    # outline
    if "outline" in sx:
        # accept "2px solid red" as outline too
        ow, _, oc = _parse_border(sx.get("outline"))
        st.outline_width, st.outline_color = ow, oc
    if "outline-width" in sx: st.outline_width = _parse_px(sx.get("outline-width"), st.outline_width)
    if "outline-color" in sx: st.outline_color = _parse_color(sx.get("outline-color"), "transparent")

    # opacity / visibility / overflow
    if "opacity" in sx: st.opacity = float(sx.get("opacity"))
    if "visibility" in sx: st.visibility = _parse_enum(sx.get("visibility"), {"visible","hidden"}, st.visibility)
    if "overflow" in sx: st.overflow = _parse_enum(sx.get("overflow"), {"visible","hidden"}, st.overflow)

    # box-shadow
    if "box-shadow" in sx:
        ox, oy, blur, spread, col, enabled = _parse_box_shadow(sx.get("box-shadow"))
        st.shadow_enabled = enabled
        st.shadow_ox, st.shadow_oy, st.shadow_blur, st.shadow_spread, st.shadow_color = ox, oy, blur, spread, col
        st.shadow = sx.get("box-shadow")

    # transform base (static)
    if "translateX" in sx: st.translate_x = _parse_px(sx.get("translateX"), st.translate_x)
    if "translateY" in sx: st.translate_y = _parse_px(sx.get("translateY"), st.translate_y)
    if "rotate" in sx: st.rotate = float(sx.get("rotate"))
    if "scaleX" in sx: st.scale_x = float(sx.get("scaleX"))
    if "scaleY" in sx: st.scale_y = float(sx.get("scaleY"))
    if "scale" in sx:
        sc = float(sx.get("scale"))
        st.scale_x = sc
        st.scale_y = sc

    # typography
    if "color" in sx: st.color = _parse_color(sx.get("color"), "white")
    if "fontSize" in sx or "font-size" in sx:
        st.font_size = _parse_px(sx.get("fontSize", sx.get("font-size")), st.font_size)
    if "fontWeight" in sx or "font-weight" in sx:
        try:
            st.font_weight = int(float(sx.get("fontWeight", sx.get("font-weight"))))
        except Exception:
            pass
    if "lineHeight" in sx or "line-height" in sx:
        try:
            st.line_height = float(sx.get("lineHeight", sx.get("line-height")))
        except Exception:
            pass
    if "textAlign" in sx or "text-align" in sx:
        st.text_align = _parse_enum(sx.get("textAlign", sx.get("text-align")), {"left","center","right"}, st.text_align)

    # misc
    if "cursor" in sx: st.cursor = _to_str(sx.get("cursor"))
    if "userSelect" in sx or "user-select" in sx:
        st.user_select = _parse_enum(sx.get("userSelect", sx.get("user-select")), {"auto","none"}, st.user_select)

    # unknown props keep
    known = {
        "width","height","minWidth","min-width","minHeight","min-height","maxWidth","max-width","maxHeight","max-height",
        "margin","padding","background","background-color","bgcolor",
        "border","border-width","border-style","border-color","border-radius","borderRadius",
        "outline","outline-width","outline-color",
        "opacity","visibility","overflow",
        "box-shadow",
        "translateX","translateY","rotate","scale","scaleX","scaleY",
        "color","fontSize","font-size","fontWeight","font-weight","lineHeight","line-height","textAlign","text-align",
        "cursor","userSelect","user-select"
    }
    for k, v in sx.items():
        if k not in known:
            st.extra[k] = v

    return st


# ============================================================
# 2) Variants compiler (keyframes + cubic-bezier easing)
# ============================================================
@dataclass
class KeyframeTrack:
    times: List[float]
    values: List[Number]

def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def _sample_track(track: KeyframeTrack, p: float) -> float:
    times = track.times
    vals = track.values
    for i in range(len(times) - 1):
        t0, t1 = times[i], times[i + 1]
        if p <= t1 or i == len(times) - 2:
            v0, v1 = float(vals[i]), float(vals[i + 1])
            if t1 == t0:
                return v1
            local = (p - t0) / (t1 - t0)
            local = max(0.0, min(1.0, local))
            return _lerp(v0, v1, local)
    return float(vals[-1])

def _cubic_bezier_ease(x1: float, y1: float, x2: float, y2: float, x: float) -> float:
    x = max(0.0, min(1.0, x))

    def bx(t: float) -> float:
        u = 1.0 - t
        return 3*u*u*t*x1 + 3*u*t*t*x2 + t*t*t

    def by(t: float) -> float:
        u = 1.0 - t
        return 3*u*u*t*y1 + 3*u*t*t*y2 + t*t*t

    def dbx(t: float) -> float:
        u = 1.0 - t
        return 3*u*u*x1 + 6*u*t*(x2 - x1) + 3*t*t*(1.0 - x2)

    t = x
    for _ in range(8):
        f = bx(t) - x
        d = dbx(t)
        if abs(d) < 1e-6:
            break
        t_next = t - f / d
        if t_next < 0.0 or t_next > 1.0:
            break
        t = t_next

    lo, hi = 0.0, 1.0
    for _ in range(12):
        mid = (lo + hi) * 0.5
        if bx(mid) < x:
            lo = mid
        else:
            hi = mid
    t = (lo + hi) * 0.5

    return max(0.0, min(1.0, by(t)))


class Timeline:
    def __init__(self, duration_ms: int, loop_count: int, easing: Union[QEasingCurve, List[float]]):
        self.duration_ms = duration_ms
        self.loop_count = loop_count
        self.easing = easing
        self.tracks: Dict[str, KeyframeTrack] = {}

    def add_track(self, name: str, times: List[float], values: List[Number]):
        if len(times) != len(values):
            raise ValueError(f"Track '{name}': times({len(times)}) != values({len(values)})")
        if len(times) < 2:
            raise ValueError(f"Track '{name}': need >=2 keyframes")
        if abs(times[0] - 0.0) > 1e-9 or abs(times[-1] - 1.0) > 1e-9:
            raise ValueError(f"Track '{name}': times must start at 0 and end at 1")
        for i in range(1, len(times)):
            if times[i] < times[i - 1]:
                raise ValueError(f"Track '{name}': times must be non-decreasing")
        self.tracks[name] = KeyframeTrack(times=times, values=values)

    def _ease(self, p: float) -> float:
        p = max(0.0, min(1.0, p))
        if isinstance(self.easing, QEasingCurve):
            return self.easing.valueForProgress(p)
        if isinstance(self.easing, list) and len(self.easing) == 4:
            x1, y1, x2, y2 = map(float, self.easing)
            return _cubic_bezier_ease(x1, y1, x2, y2, p)
        return p

    def sample(self, progress_0_1: float) -> Dict[str, float]:
        p = self._ease(float(progress_0_1))
        return {k: float(_sample_track(t, p)) for k, t in self.tracks.items()}


def compile_variant_timeline(
    variants: dict,
    variant_key: str,
    apply_fn: Callable[[Dict[str, float]], None],
    parent: Optional[QObject] = None,
) -> QVariantAnimation:
    node = variants.get(variant_key, {}) or {}
    trans = node.get("transition", {}) or {}

    dur = trans.get("duration", 1.0)
    # duration: float <= 20 => seconds; else treat as ms
    if isinstance(dur, (int, float)):
        duration_ms = int(round(float(dur) * 1000)) if float(dur) <= 20 else int(round(float(dur)))
    else:
        duration_ms = 1000

    count = trans.get("count", 1)
    loop = -1 if str(count).lower() in ("infinite", "-1") else int(count)

    ease = trans.get("ease", "easeInOut")
    if isinstance(ease, list) and len(ease) == 4 and all(isinstance(x, (int, float)) for x in ease):
        easing: Union[QEasingCurve, List[float]] = [float(x) for x in ease]
    else:
        s = str(ease).lower()
        easing = QEasingCurve(QEasingCurve.Linear) if s == "linear" else QEasingCurve(QEasingCurve.InOutQuad)

    times = trans.get("times", None)
    if isinstance(times, list) and len(times) >= 2 and all(isinstance(x, (int, float)) for x in times):
        times = [float(x) for x in times]
        if abs(times[0] - 0.0) > 1e-9 or abs(times[-1] - 1.0) > 1e-9:
            times = None
    else:
        times = None

    timeline = Timeline(duration_ms=duration_ms, loop_count=loop, easing=easing)

    for prop, vals in node.items():
        if prop == "transition":
            continue
        if not isinstance(vals, list) or len(vals) < 2:
            continue

        if times is not None and len(times) == len(vals):
            local_times = times
        else:
            n = len(vals)
            local_times = [i / (n - 1) for i in range(n)]

        # ensure endpoints
        if local_times[0] != 0.0:
            local_times = [0.0] + local_times
            vals = [vals[0]] + vals
        if local_times[-1] != 1.0:
            local_times = local_times + [1.0]
            vals = vals + [vals[-1]]

        timeline.add_track(prop, local_times, vals)

    anim = QVariantAnimation(parent=parent)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setDuration(timeline.duration_ms)
    anim.setLoopCount(timeline.loop_count)

    def on_changed(v):
        apply_fn(timeline.sample(float(v)))

    anim.valueChanged.connect(on_changed)
    return anim
