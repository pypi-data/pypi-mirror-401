from typing import Callable
from .qss_properties import QssProperties
from qtmui.material.styles import useTheme
from functools import lru_cache


def camel_to_kebab_case(s):
    """
    Chuyển đổi chuỗi từ camelCase sang kebab-case.
    """
    return ''.join(['-' + c.lower() if c.isupper() else c for c in s]).lstrip('-')

def resolve_theme_value(theme, value):
    """
    Giải quyết giá trị theme từ chuỗi dạng 'palette.primary.main', 'text.secondary', 'background.paper', v.v.
    """
    if isinstance(value, str) and value.startswith("palette."):
        parts = value.split(".")
        theme_value = theme

        for part in parts:
            theme_value = getattr(theme_value, part, None)
            if theme_value is None:
                return None  # Trả về None nếu không tìm thấy giá trị

        # print('theme_value_______________', theme_value)
        return theme_value
    return value






def convert_sx_params_to_str(func):
    @wraps(func)
    def wrapper(sx, *args, **kwargs):
        # Nếu params là dict, chuyển nó thành chuỗi JSON (hoặc sử dụng str() nếu phù hợp)
        if isinstance(sx, dict):
            sx = json.dumps(sx)
        elif isinstance(sx, Callable):
            sx = sx()
            sx = json.dumps(sx)
        else:
            if sx == None:
                sx = ""
        return func(sx, *args, **kwargs)
    return wrapper

def convert_sx_params_to_dict(func):
    @wraps(func)
    def wrapper(sx, *args, **kwargs):
        # Nếu params là dict, chuyển nó thành chuỗi JSON (hoặc sử dụng str() nếu phù hợp)
        if isinstance(sx, str) and sx != "":
            try:
                sx = json.loads(sx)
            except Exception as e:
                print('sxxxxxxxxxx_errrrrrrrrrrrrr', type(sx))
        return func(sx, *args, **kwargs)
    return wrapper



@convert_sx_params_to_str
@lru_cache(maxsize=None)
@convert_sx_params_to_dict
def get_qss_style(sx: dict):
    """
    Hàm tạo chuỗi CSS từ dictionary các tham số.
    """
    if isinstance(sx, str):
        return sx
    theme = useTheme()
    css_lines = []

    for key, value in sx.items():
        # Chuyển key từ camelCase sang kebab-case
        css_key = camel_to_kebab_case(key)

        # Kiểm tra nếu key tồn tại trong QssProperties
        if css_key in QssProperties.__dict__.values():
            # Xử lý giá trị theme (palette., text., background.)
            if isinstance(value, str) and (
                value.startswith("text.") 
                or value.startswith("background.")
                or value.startswith("primary.")
                or value.startswith("secondary.")
                or value.startswith("info.")
                or value.startswith("warning.")
                or value.startswith("error.")
                ):
                value = f"palette.{value}"

                # print('value__resolveeeeeeeeeeeee', value)

            value = resolve_theme_value(theme, value)
            # print('value__resolveeeeeeeeeeeee', value)

            # Xử lý margin và padding X/Y thành hai thuộc tính riêng
            if css_key == "mb" or \
                css_key == "display" or \
                css_key == "flex-shrink" or \
                css_key == "flex-grow" or \
                css_key == "align-items" or \
                css_key == "flex-direction" or \
                css_key == "align-self" or \
                css_key == "z-index" or \
                css_key == "display":
                # print('mbbbbbbbbbbbbbbb')
                continue
            if css_key == "marginX" or css_key == "mx":
                css_lines.append(f"margin-left: {value};")
                css_lines.append(f"margin-right: {value};")
            elif css_key == "marginY" or css_key == "my":
                css_lines.append(f"margin-top: {value};")
                css_lines.append(f"margin-bottom: {value};")
            elif css_key == "paddingX" or css_key == "px":
                css_lines.append(f"padding-left: {value};")
                css_lines.append(f"padding-right: {value};")
            elif css_key == "paddingY" or css_key == "py":
                css_lines.append(f"padding-top: {value};")
                css_lines.append(f"padding-bottom: {value};")
            elif css_key == "width" and str(value).find("%") == -1:
                css_lines.append(f"min-width: {value};")
                css_lines.append(f"max-width: {value};")
            elif css_key == "height" and str(value).find("%") == -1:
                css_lines.append(f"min-height: {value};")
                css_lines.append(f"max-height: {value};")
            else:
                css_lines.append(f"{css_key}: {value};")

    # Kết hợp các dòng CSS thành chuỗi
    return "\n    ".join(css_lines)

def _get_sx_qss(sx):
    sx_qss = ""
    if sx:
        if isinstance(sx, dict):
            sx_qss = get_qss_style(sx)
        elif isinstance(sx, Callable):
            sx = sx()
            if isinstance(sx, dict):
                sx_qss = get_qss_style(sx)
            elif isinstance(sx, str):
                sx_qss = sx
        elif isinstance(sx, str) and sx != "":
            sx_qss = sx
    return sx_qss


_get_sx_qss(
    {
        "color": "red", 
        "background-color": lambda theme: theme.palette.background.main
    }
)