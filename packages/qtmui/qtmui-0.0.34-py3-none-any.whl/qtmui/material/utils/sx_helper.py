# sx_helper.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Union, Callable
import re

Number = Union[int, float]
Sx = Dict[str, Any]

from qtmui.hooks import State

# =============================================================================
# Core parsing utilities
# =============================================================================

_PX_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*px\s*$", re.IGNORECASE)
_NUM_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*$")
_RGBA_RE = re.compile(
    r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([0-9.]+)\s*)?\)",
    re.IGNORECASE,
)
_HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{8})")


def is_sx(obj: Any) -> bool:
    """Trả True nếu obj là dict-like sx."""
    return isinstance(obj, dict)

def get_sx_dict(sx):
  if isinstance(sx, State):
      sx = sx.value
  else:
      sx = sx

  if isinstance(sx, Callable):
      sx = sx()

  if isinstance(sx, dict):
      return sx
  else:
      return None


def get_str(sx: Optional[Sx], key: str, default: Optional[str] = None) -> Optional[str]:
    """Lấy sx[key] dưới dạng str (nếu không có hoặc không phải str -> default)."""
    if not isinstance(sx, dict):
        return default
    v = sx.get(key, default)
    return v if isinstance(v, str) else default


def get_num(sx: Optional[Sx], key: str, default: Optional[Number] = None) -> Optional[Number]:
    """Lấy sx[key] nếu là int/float, ngược lại default."""
    if not isinstance(sx, dict):
        return default
    v = sx.get(key, default)
    return v if isinstance(v, (int, float)) else default


def parse_px(value: Any, *, default: float = 0.0, clamp_min: Optional[float] = 0.0) -> float:
    """
    Parse giá trị pixel từ:
      - int/float -> px
      - "12px" -> 12
      - "12"   -> 12  (chấp nhận số trần)
    Unit hỗ trợ DUY NHẤT: px (hoặc số trần).

    clamp_min:
      - mặc định 0.0 (không cho âm).
      - nếu None: không clamp.
    """
    if value is None:
        out = float(default)
    elif isinstance(value, (int, float)):
        out = float(value)
    elif isinstance(value, str):
        s = value.strip().lower()
        m = _PX_RE.match(s)
        if m:
            out = float(m.group(1))
        else:
            m = _NUM_RE.match(s)
            if m:
                out = float(m.group(1))
            else:
                out = float(default)
    else:
        out = float(default)

    if clamp_min is not None:
        out = max(clamp_min, out)
    return out


def parse_px_int(value: Any, *, default: int = 0, clamp_min: Optional[int] = 0) -> int:
    """Giống parse_px nhưng trả về int (round)."""
    f = parse_px(value, default=float(default), clamp_min=float(clamp_min) if clamp_min is not None else None)
    i = int(round(f))
    if clamp_min is not None:
        i = max(clamp_min, i)
    return i


def pick_first(sx: Optional[Sx], keys: Sequence[str]) -> Any:
    """
    Lấy value đầu tiên tồn tại trong sx theo thứ tự keys.
    Trả None nếu không có.
    """
    if not isinstance(sx, dict):
        return None
    for k in keys:
        if k in sx and sx[k] is not None:
            return sx[k]
    return None


# =============================================================================
# 4-side helpers: padding / margin
# QSS-like keys only:
#   padding, padding-left/right/top/bottom
#   margin, margin-left/right/top/bottom
# Không xử lý: pl/pr/pt/pb, paddingBottom, ...
# =============================================================================

def _parse_box_shorthand(value: Any) -> Tuple[int, int, int, int]:
    """
    Parse shorthand kiểu CSS box:
      - 1 giá trị: all
      - 2 giá trị: (vertical, horizontal) => top/bottom, left/right
      - 3 giá trị: top, horizontal, bottom
      - 4 giá trị: top, right, bottom, left

    Chỉ hỗ trợ px (hoặc số trần).
    """
    if value is None:
        return 0, 0, 0, 0

    if isinstance(value, (int, float, str)):
        # nếu là str có thể chứa nhiều token
        if isinstance(value, str):
            parts = [p for p in value.replace(",", " ").split() if p.strip()]
            if len(parts) >= 2:
                nums = [parse_px_int(p) for p in parts[:4]]
                if len(nums) == 2:
                    v, h = nums
                    return v, h, v, h
                if len(nums) == 3:
                    t, h, b = nums
                    return t, h, b, h
                if len(nums) >= 4:
                    t, r, b, l = nums[:4]
                    return t, r, b, l
            # single token
            one = parse_px_int(value)
            return one, one, one, one

        one = parse_px_int(value)
        return one, one, one, one

    if isinstance(value, (list, tuple)):
        arr = list(value)
        if len(arr) == 1:
            one = parse_px_int(arr[0])
            return one, one, one, one
        if len(arr) == 2:
            v, h = parse_px_int(arr[0]), parse_px_int(arr[1])
            return v, h, v, h
        if len(arr) == 3:
            t, h, b = parse_px_int(arr[0]), parse_px_int(arr[1]), parse_px_int(arr[2])
            return t, h, b, h
        if len(arr) >= 4:
            t, r, b, l = (parse_px_int(arr[0]), parse_px_int(arr[1]), parse_px_int(arr[2]), parse_px_int(arr[3]))
            return t, r, b, l

    return 0, 0, 0, 0


def get_padding_list_4(sx: Optional[Sx], *, default: Any = 0) -> List[int]:
    """
    Trả về padding dạng list 4 phần tử: [top, right, bottom, left]

    Keys hỗ trợ:
      - "padding"
      - "padding-top", "padding-right", "padding-bottom", "padding-left"
    Priority:
      - các key side-specific override shorthand "padding"

    default:
      - dùng khi sx không có padding.

    Ví dụ:
      sx={"padding":"10px"} -> [10,10,10,10]
      sx={"padding":"8px 12px", "padding-left":"20px"} -> [8,12,8,20]
    """
    
    t, r, b, l = _parse_box_shorthand(pick_first(sx, ["padding"]) or default)

    top = pick_first(sx, ["padding-top"])
    right = pick_first(sx, ["padding-right"])
    bottom = pick_first(sx, ["padding-bottom"])
    left = pick_first(sx, ["padding-left"])



    if top is not None:
        t = parse_px_int(top)
    if right is not None:
        r = parse_px_int(right)
    if bottom is not None:
        b = parse_px_int(bottom)
    if left is not None:
        l = parse_px_int(left)

    return [t, r, b, l]


def get_padding_tuple(sx: Optional[Sx], *, default: Any = 0) -> Tuple[int, int, int, int]:
    """Giống get_padding_list_4 nhưng trả về tuple (t, r, b, l)."""
    p = get_padding_list_4(sx, default=default)
    return p[0], p[1], p[2], p[3]


def get_margin_list_4(sx: Optional[Sx], *, default: Any = 0) -> List[int]:
    """
    Trả về margin dạng [top, right, bottom, left]

    Keys hỗ trợ:
      - "margin"
      - "margin-top", "margin-right", "margin-bottom", "margin-left"
    """
    t, r, b, l = _parse_box_shorthand(pick_first(sx, ["margin"]) or default)

    top = pick_first(sx, ["margin-top"])
    right = pick_first(sx, ["margin-right"])
    bottom = pick_first(sx, ["margin-bottom"])
    left = pick_first(sx, ["margin-left"])

    if top is not None:
        t = parse_px_int(top)
    if right is not None:
        r = parse_px_int(right)
    if bottom is not None:
        b = parse_px_int(bottom)
    if left is not None:
        l = parse_px_int(left)

    return [t, r, b, l]


def get_margin_tuple(sx: Optional[Sx], *, default: Any = 0) -> Tuple[int, int, int, int]:
    """Giống get_margin_list_4 nhưng trả về tuple (t, r, b, l)."""
    m = get_margin_list_4(sx, default=default)
    return m[0], m[1], m[2], m[3]


# =============================================================================
# Border helpers
# QSS-like keys only:
#   border, border-left/right/top/bottom, border-*-width
# Không xử lý: borderLeftWidth camelCase, borderLeft, ...
# =============================================================================

@dataclass(frozen=True)
class BorderSide:
    width: int
    style: str  # "solid" | "dashed" | "dotted" | ...
    color: str  # raw color token string (rgba(...) / #hex / name)


def _parse_border_style(token: str) -> str:
    s = (token or "").strip().lower()
    if "dashed" in s:
        return "dashed"
    if "dotted" in s:
        return "dotted"
    if "solid" in s:
        return "solid"
    return "solid"


def _extract_color_token(border_str: str) -> str:
    if not isinstance(border_str, str):
        return ""
    m = _RGBA_RE.search(border_str)
    if m:
        return m.group(0)
    m = _HEX_RE.search(border_str)
    if m:
        return m.group(0)
    # fallback: try last token as color name
    parts = [p for p in border_str.replace("/", " ").replace(",", " ").split() if p.strip()]
    if parts:
        # often: "1px solid red"
        return parts[-1]
    return ""


def parse_border_side(value: Any) -> BorderSide:
    """
    Parse một border side từ string kiểu:
      "1px solid rgba(0,0,0,100)"
      "2px dashed #ff00ff"
      "1px solid red"

    Nếu không parse được -> width=0.
    """
    if value is None:
        return BorderSide(width=0, style="solid", color="")

    if isinstance(value, (int, float)):
        return BorderSide(width=parse_px_int(value), style="solid", color="rgba(0,0,0,255)")

    if not isinstance(value, str):
        return BorderSide(width=0, style="solid", color="")

    s = value.strip()
    w = parse_px_int(s)
    style = _parse_border_style(s)
    color = _extract_color_token(s)
    return BorderSide(width=w, style=style, color=color)


def get_border_sides_4(sx: Optional[Sx]) -> Dict[str, BorderSide]:
    """
    Trả về dict 4 cạnh:
      {"top": BorderSide, "right": ..., "bottom": ..., "left": ...}

    Keys hỗ trợ (qss-like):
      - "border" (shorthand)
      - "border-top", "border-right", "border-bottom", "border-left"
      - "border-top-width", ... (nếu có, override width)
    """
    base = parse_border_side(pick_first(sx, ["border"]))

    top = parse_border_side(pick_first(sx, ["border-top"])) if pick_first(sx, ["border-top"]) is not None else base
    right = parse_border_side(pick_first(sx, ["border-right"])) if pick_first(sx, ["border-right"]) is not None else base
    bottom = parse_border_side(pick_first(sx, ["border-bottom"])) if pick_first(sx, ["border-bottom"]) is not None else base
    left = parse_border_side(pick_first(sx, ["border-left"])) if pick_first(sx, ["border-left"]) is not None else base

    # width overrides
    tw = pick_first(sx, ["border-top-width"])
    rw = pick_first(sx, ["border-right-width"])
    bw = pick_first(sx, ["border-bottom-width"])
    lw = pick_first(sx, ["border-left-width"])

    if tw is not None:
        top = BorderSide(width=parse_px_int(tw), style=top.style, color=top.color)
    if rw is not None:
        right = BorderSide(width=parse_px_int(rw), style=right.style, color=right.color)
    if bw is not None:
        bottom = BorderSide(width=parse_px_int(bw), style=bottom.style, color=bottom.color)
    if lw is not None:
        left = BorderSide(width=parse_px_int(lw), style=left.style, color=left.color)

    return {"top": top, "right": right, "bottom": bottom, "left": left}


def get_border_width_list_4(sx: Optional[Sx]) -> List[int]:
    """Trả [top, right, bottom, left] border widths (px)."""
    b = get_border_sides_4(sx)
    return [b["top"].width, b["right"].width, b["bottom"].width, b["left"].width]


def get_border_width_tuple(sx: Optional[Sx]) -> Tuple[int, int, int, int]:
    """Trả (top, right, bottom, left) border widths (px)."""
    x = get_border_width_list_4(sx)
    return x[0], x[1], x[2], x[3]


# =============================================================================
# Border radius helpers (qss-like only)
# Supported:
#   border-radius
#   border-top-left-radius / border-top-right-radius / border-bottom-right-radius / border-bottom-left-radius
# =============================================================================

def get_border_radius_4(sx: Optional[Sx], *, default: Any = 0) -> Dict[str, int]:
    """
    Trả radius 4 góc (px):
      {"tl": int, "tr": int, "br": int, "bl": int}

    Keys:
      - "border-radius"
      - "border-top-left-radius"
      - "border-top-right-radius"
      - "border-bottom-right-radius"
      - "border-bottom-left-radius"
    """
    base = pick_first(sx, ["border-radius"])
    base_r = parse_px_int(base if base is not None else default)

    tl = pick_first(sx, ["border-top-left-radius"])
    tr = pick_first(sx, ["border-top-right-radius"])
    br = pick_first(sx, ["border-bottom-right-radius"])
    bl = pick_first(sx, ["border-bottom-left-radius"])

    return {
        "tl": parse_px_int(tl) if tl is not None else base_r,
        "tr": parse_px_int(tr) if tr is not None else base_r,
        "br": parse_px_int(br) if br is not None else base_r,
        "bl": parse_px_int(bl) if bl is not None else base_r,
    }


# =============================================================================
# Size helpers (qss-like only)
# Supported:
#   width/height
#   min-width/min-height
#   max-width/max-height
# Unit: px only
# =============================================================================

@dataclass(frozen=True)
class SizeSpec:
    width: Optional[int] = None
    height: Optional[int] = None
    min_width: Optional[int] = None
    min_height: Optional[int] = None
    max_width: Optional[int] = None
    max_height: Optional[int] = None


def get_size_spec(sx: Optional[Sx]) -> SizeSpec:
    """
    Parse kích thước từ sx theo qss-like keys (px only).
    Không xử lý %, rem, vw, ...
    """
    if not isinstance(sx, dict):
        return SizeSpec()

    w = sx.get("width")
    h = sx.get("height")
    min_w = sx.get("min-width")
    min_h = sx.get("min-height")
    max_w = sx.get("max-width")
    max_h = sx.get("max-height")

    def px_or_none(v: Any) -> Optional[int]:
        if v is None:
            return None
        return parse_px_int(v)

    return SizeSpec(
        width=px_or_none(w),
        height=px_or_none(h),
        min_width=px_or_none(min_w),
        min_height=px_or_none(min_h),
        max_width=px_or_none(max_w),
        max_height=px_or_none(max_h),
    )


# =============================================================================
# Gap / spacing helpers (qss-like-ish)
# Supported:
#   gap, row-gap, column-gap
# Unit: px only
# =============================================================================

@dataclass(frozen=True)
class GapSpec:
    row: int
    col: int


def get_gap_spec(sx: Optional[Sx], *, default: Any = 0) -> GapSpec:
    """
    Parse gap:
      - "gap" -> áp dụng cả row/col
      - "row-gap", "column-gap" override
    """
    g = pick_first(sx, ["gap"])
    base = parse_px_int(g if g is not None else default)

    rg = pick_first(sx, ["row-gap"])
    cg = pick_first(sx, ["column-gap"])

    row = parse_px_int(rg) if rg is not None else base
    col = parse_px_int(cg) if cg is not None else base

    return GapSpec(row=row, col=col)


# =============================================================================
# Color helpers (raw string parsing)
# (Bạn có thể map sang QColor ở module decorator)
# =============================================================================

def is_color_token(s: Any) -> bool:
    """Heuristic: kiểm tra token có vẻ là color (rgba/rgb/#hex hoặc tên)."""
    if not isinstance(s, str):
        return False
    ss = s.strip()
    if _RGBA_RE.search(ss):
        return True
    if _HEX_RE.search(ss):
        return True
    # tên màu: cho phép chữ
    return bool(re.match(r"^[a-zA-Z]+$", ss))


def parse_rgba_string(s: str) -> Optional[Tuple[int, int, int, int]]:
    """
    Parse rgba/rgb -> (r,g,b,a[0..255]).
    a hỗ trợ 0..1 hoặc 0..255.
    """
    if not isinstance(s, str):
        return None
    m = _RGBA_RE.search(s.strip())
    if not m:
        return None
    r = int(m.group(1))
    g = int(m.group(2))
    b = int(m.group(3))
    a_raw = m.group(4)
    if a_raw is None:
        a = 255
    else:
        a_f = float(a_raw)
        a = int(round(a_f * 255)) if a_f <= 1.0 else int(round(a_f))
        a = max(0, min(255, a))
    return r, g, b, a


# =============================================================================
# Background helpers (qss-like)
# Supported:
#   background, background-color
# and linear-gradient(...) (basic)
# =============================================================================

@dataclass(frozen=True)
class LinearGradientSpec:
    direction: str  # "to right" / "to bottom" / "90deg" ...
    color1: str
    color2: str


@dataclass(frozen=True)
class BackgroundSpec:
    kind: str  # "none" | "color" | "linear-gradient"
    color: Optional[str] = None
    linear: Optional[LinearGradientSpec] = None


def parse_linear_gradient(value: Any) -> Optional[LinearGradientSpec]:
    """
    Parse string:
      linear-gradient(to right, c1, c2)
      linear-gradient(to bottom, c1, c2)
      linear-gradient(90deg, c1, c2)

    Chỉ lấy 2 màu đầu tiên.
    """
    if not isinstance(value, str):
        return None
    s = value.strip()
    if not s.lower().startswith("linear-gradient(") or not s.endswith(")"):
        return None

    inner = s[len("linear-gradient("):-1].strip()
    parts = [p.strip() for p in inner.split(",") if p.strip()]
    if len(parts) < 2:
        return None

    direction = "to bottom"
    colors = parts

    first = parts[0].lower()
    if first.startswith("to ") or first.endswith("deg"):
        direction = parts[0]
        colors = parts[1:]

    if len(colors) < 2:
        return None

    return LinearGradientSpec(direction=direction, color1=colors[0], color2=colors[1])


def get_background_spec(sx: Optional[Sx]) -> BackgroundSpec:
    """
    Lấy background:
      - background
      - background-color
    Nếu là linear-gradient(...) -> kind=linear-gradient
    Ngược lại treat như color token string.
    """
    v = pick_first(sx, ["background", "background-color"])
    if v is None:
        return BackgroundSpec(kind="none")

    lg = parse_linear_gradient(v)
    if lg:
        return BackgroundSpec(kind="linear-gradient", linear=lg)

    if isinstance(v, str):
        return BackgroundSpec(kind="color", color=v.strip())

    # non-str fallback: try numeric -> rgba black
    if isinstance(v, (int, float)):
        return BackgroundSpec(kind="color", color=str(v))

    return BackgroundSpec(kind="none")


# =============================================================================
# Merge / normalize helpers
# =============================================================================

def merge_sx(*sx_list: Optional[Sx]) -> Sx:
    """
    Merge nhiều sx dict theo thứ tự:
      merge_sx(base, override1, override2)
    Quy tắc: key sau ghi đè key trước (shallow merge).
    """
    out: Dict[str, Any] = {}
    for sx in sx_list:
        if isinstance(sx, dict):
            out.update(sx)
    return out


def only_qss_keys(sx: Optional[Sx], allowed_prefixes: Optional[Sequence[str]] = None) -> Sx:
    """
    Lọc sx chỉ giữ các key dạng qss-like (có dấu '-') hoặc thuộc allowed_prefixes.
    Mục tiêu: tách custom keys khỏi qss keys nếu cần.

    allowed_prefixes:
      ví dụ ["padding", "margin", "border", "background", "min-", "max-", "row-", "column-"]
    """
    if not isinstance(sx, dict):
        return {}
    if allowed_prefixes is None:
        allowed_prefixes = ["padding", "margin", "border", "background", "min-", "max-", "row-", "column-", "gap", "width", "height"]

    out: Dict[str, Any] = {}
    for k, v in sx.items():
        if "-" in k:
            out[k] = v
            continue
        for p in allowed_prefixes:
            if k == p or k.startswith(p):
                out[k] = v
                break
    return out


# =============================================================================
# Convenience: convert to Qt-friendly formats (without importing Qt)
# =============================================================================

def padding_to_qmargins_args(sx: Optional[Sx], *, default: Any = 0) -> Tuple[int, int, int, int]:
    """
    Trả (left, top, right, bottom) để bạn gọi QMargins(l,t,r,b).
    Lưu ý Qt order: left, top, right, bottom.
    """
    t, r, b, l = get_padding_tuple(sx, default=default)
    return l, t, r, b


def margin_to_qmargins_args(sx: Optional[Sx], *, default: Any = 0) -> Tuple[int, int, int, int]:
    """Trả (left, top, right, bottom) cho QMargins."""
    t, r, b, l = get_margin_tuple(sx, default=default)
    return l, t, r, b



"""
Gợi ý cách dùng trong code của bạn
1) Padding cho layout
from qtmui.lib.sx_helper import padding_to_qmargins_args

l, t, r, b = padding_to_qmargins_args(sx, default=0)
layout.setContentsMargins(l, t, r, b)

2) Border widths để bù nội dung (nếu bạn cần)
from qtmui.lib.sx_helper import get_border_width_tuple

top, right, bottom, left = get_border_width_tuple(sx)

3) Background spec để StyleDecorator render
from qtmui.lib.sx_helper import get_background_spec
bg = get_background_spec(sx)
if bg.kind == "linear-gradient":
    # bg.linear.direction, bg.linear.color1, bg.linear.color2
"""