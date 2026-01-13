from typing import Literal, Tuple, Union, Dict
import re
from PySide6.QtGui import QColor
import random


# Định nghĩa kiểu ColorFormat
ColorFormat = Literal['rgb', 'rgba', 'hsl', 'hsla', 'color']

# Định nghĩa kiểu ColorSpace
ColorSpace = Literal['srgb', 'display-p3', 'a98-rgb', 'prophoto-rgb', 'rec-2020']

# Định nghĩa kiểu ColorObject
class ColorObject:
    def __init__(
        self,
        type: ColorFormat,
        values: Union[Tuple[int, int, int], Tuple[int, int, int, int]],
        color_space: ColorSpace = 'srgb'
    ):
        self.type = type
        self.values = values
        self.color_space = color_space

    def __repr__(self):
        return f"ColorObject(type={self.type}, values={self.values}, color_space={self.color_space})"


def clamp(value, min_value=0, max_value=1):
    if value < min_value or value > max_value:
        print(f"Warning: The value provided {value} is out of range [{min_value}, {max_value}].")
    return max(min_value, min(max_value, value))

def hexToRgb(color):
    color = color.lstrip('#')
    length = 2 if len(color) >= 6 else 1
    colors = re.findall('.' * length, color)
    if len(colors) == 3:
        return f"rgb({', '.join(str(int(c, 16)) for c in colors)})".encode('utf-8').decode('utf-8')
    elif len(colors) == 4:
        return f"rgba({', '.join(str(int(c, 16)) for c in colors[:3])}, {round(int(colors[3], 16) / 255, 3)})".encode('utf-8').decode('utf-8')
    return ''

def int_to_hex(value):
    hex_value = hex(value)[2:]
    return hex_value if len(hex_value) > 1 else f'0{hex_value}'


# Từ điển chuẩn hóa tên màu CSS → mã hex
CSS_COLOR_NAMES = {
    "black": "#000000",
    "white": "#ffffff",
    "red": "#ff0000",
    "lime": "#00ff00",
    "blue": "#0000ff",
    "yellow": "#ffff00",
    "cyan": "#00ffff",
    "magenta": "#ff00ff",
    "silver": "#c0c0c0",
    "gray": "#808080",
    "maroon": "#800000",
    "olive": "#808000",
    "green": "#008000",
    "purple": "#800080",
    "teal": "#008080",
    "navy": "#000080",
    "orange": "#ffa500",
    "pink": "#ffc0cb",
    "brown": "#a52a2a",
    "gold": "#ffd700",
    "indigo": "#4b0082",
    "violet": "#ee82ee",
    "lightgray": "#d3d3d3",
    "darkgray": "#a9a9a9",
    # bạn có thể thêm các màu khác nếu cần
}


def hexToRgb(hex_color: str):
    """Chuyển mã hex → rgb tuple."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join([c * 2 for c in hex_color])
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgb({r}, {g}, {b})"


def decomposeColor(color: Union[str, Dict]) -> Dict:
    """Phân tích mọi dạng màu: tên, hex, rgb, rgba, hsl, hsla, hoặc color()."""
    color = str(color).strip().lower()

    # --- 1️⃣ Nếu là tên màu CSS chuẩn (vd: "red", "blue") ---
    if color in CSS_COLOR_NAMES:
        return decomposeColor(CSS_COLOR_NAMES[color])

    # --- 2️⃣ Nếu là mã hex ---
    if color.startswith("#"):
        return decomposeColor(hexToRgb(color))

    # --- 3️⃣ Nếu là dạng rgb(), rgba(), hsl(), hsla(), color() ---
    marker = color.find("(")
    if marker == -1:
        raise ValueError(f"Unsupported color format: {color}")

    color_type = color[:marker].strip()
    values = color[marker + 1 : -1].split(",")

    if color_type not in ["rgb", "rgba", "hsl", "hsla", "color"]:
        raise ValueError(f"Unsupported color type: {color_type}")

    # Xử lý từng giá trị (loại bỏ % nếu có)
    parsed_values = []
    for v in values:
        v = v.strip()
        if v.endswith("%"):
            parsed_values.append(float(v[:-1]))  # bỏ ký hiệu %
        else:
            try:
                parsed_values.append(float(v))
            except ValueError:
                parsed_values.append(v)  # nếu là string (vd 'none')

    return {
        "type": color_type,
        "values": parsed_values
    }


def recomposeColor(color):
    color_type = color['type']
    values = color['values']
    
    if color_type.startswith('rgb'):
        values = [int(v) for v in values[:3]] + values[3:]
    elif color_type.startswith('hsl'):
        values[1] = f"{values[1]}%"
        values[2] = f"{values[2]}%"
    
    return f"{color_type}({', '.join(map(str, values))})".encode('utf-8').decode('utf-8')

def hslToRgb(color):
    """
    Chuyển đổi màu HSL sang RGB.
    """
    color = decomposeColor(color)
    values = color["values"]
    h = values[0]
    s = values[1] / 100
    l = values[2] / 100

    a = s * min(l, 1 - l)

    def f(n):
        k = (n + h / 30) % 12
        return l - a * max(min(k - 3, 9 - k, 1), -1)

    rgb = [
        round(f(0) * 255),
        round(f(8) * 255),
        round(f(4) * 255),
    ]

    if color["type"] == "hsla":
        rgb.append(values[3])  # Thêm alpha nếu là HSLA

    return recomposeColor({
        "type": "rgba" if color["type"] == "hsla" else "rgb",
        "values": rgb,
    })



def rgbToHex(color):
    decomposed = decomposeColor(color)
    return '#' + ''.join(int_to_hex(int(v)) for v in decomposed['values'][:3])

def rgb2hex(r_or_color: Union[tuple, int], g: int = 0, b: int = 0, a: int = 0) -> str:
    """Convert rgb color to hex color.

    :param r_or_color: The 'red' value or a color tuple.
    :param g: The 'green' value.
    :param b: The 'blue' value.
    :param a: The 'alpha' value.
    :return: The converted hexadecimal color.
    """

    if type(r_or_color).__name__ == "tuple": r, g, b = r_or_color[:3]
    else: r = r_or_color
    hex = '%02x%02x%02x' % (int(r), int(g), int(b))
    return hex

def rgbaToQColor(rgba_string):
    rgba_values = rgba_string.strip("rgba()").split(", ")
    rgba_values = [float(value.strip()) for value in rgba_values]

    if len(rgba_values) == 4:
        red = rgba_values[0] / 255.0
        green = rgba_values[1] / 255.0
        blue = rgba_values[2] / 255.0
        alpha = rgba_values[3]

        return QColor.fromRgbF(red, green, blue, alpha)
    return None

def getLuminance(color):
    decomposed = decomposeColor(color)
    rgb = decomposed['values'][:3]
    rgb = [v / 255 for v in rgb]
    rgb = [(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4) for v in rgb]
    return round(0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2], 3)

def getContrastRatio(foreground, background):
    lum_a = getLuminance(foreground)
    lum_b = getLuminance(background)
    return (max(lum_a, lum_b) + 0.05) / (min(lum_a, lum_b) + 0.05)

def alpha_tuple(color, value):
    decomposed = decomposeColor(color)
    value = clamp(value)
    decomposed['values'].append(value)
    return recomposeColor(decomposed)

def alpha(color, value):
    decomposed_color = decomposeColor(color)
    value = clamp(value)

    # Kiểm tra nếu chưa có giá trị alpha, thêm nó vào
    if len(decomposed_color['values']) == 3:
        decomposed_color['values'].append(value)  # Thêm kênh alpha mới
    else:
        decomposed_color['values'][3] = value  # Cập nhật kênh alpha hiện có
    
    if decomposed_color['type'] == 'rgb' or decomposed_color['type'] == 'hsl':
        decomposed_color['type'] += 'a'  # Chuyển đổi sang rgba hoặc hsla
    
    return recomposeColor(decomposed_color)


def darken(color, coefficient):
    decomposed = decomposeColor(color)
    coefficient = clamp(coefficient)
    
    for i in range(3):
        decomposed['values'][i] *= (1 - coefficient)
    
    return recomposeColor(decomposed)

def lighten(color, coefficient):
    decomposed = decomposeColor(color)
    coefficient = clamp(coefficient)
    
    for i in range(3):
        decomposed['values'][i] += (255 - decomposed['values'][i]) * coefficient
    
    return recomposeColor(decomposed)

def emphasize(color, coefficient=0.15):
    return darken(color, coefficient) if getLuminance(color) > 0.5 else lighten(color, coefficient)

def blend(background, overlay, opacity, gamma=1.0):
    def blend_channel(bg, ov):
        return round((bg ** (1 / gamma) * (1 - opacity) + ov ** (1 / gamma) * opacity) ** gamma)
    
    background_color = decomposeColor(background)
    overlay_color = decomposeColor(overlay)
    
    blended = [blend_channel(bg, ov) for bg, ov in zip(background_color['values'][:3], overlay_color['values'][:3])]
    
    return recomposeColor({'type': 'rgb', 'values': blended})

def hex_string_to_qcolor(hex_string: str):
    # Loại bỏ dấu '#' nếu có
    if hex_string.startswith('#'):
        hex_string = hex_string[1:]

    # Đảm bảo độ dài hợp lệ
    if len(hex_string) not in (6, 8):
        raise ValueError("Invalid hex color string length")

    # Tách giá trị RGB và alpha nếu có
    r = int(hex_string[0:2], 16)
    g = int(hex_string[2:4], 16)
    b = int(hex_string[4:6], 16)
    a = int(hex_string[6:8], 16) if len(hex_string) == 8 else 50

    return QColor(r, g, b, a)

def get_palette_text_color(palette, color):
    if color == 'primary':
        return palette.text.primary
    elif color == 'secondary':
        return palette.text.secondary
    # Thêm các màu khác ở đây
    return '#000000'  # Màu mặc định nếu không tìm thấy


def lighten_hex(hex_color, value):
    def _clamp(value, min_value=0, max_value=255):
        """Giữ giá trị trong khoảng từ min_value đến max_value."""
        return max(min_value, min(max_value, value))

    def _hexToRgb(_hex_color):
        """Chuyển mã màu hex thành RGB."""
        _hex_color = _hex_color.lstrip('#')
        return tuple(int(_hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _rgbToHex(rgb):
        """Chuyển từ RGB thành mã màu hex."""
        return '#{:02x}{:02x}{:02x}'.format(_clamp(rgb[0]), _clamp(rgb[1]), _clamp(rgb[2]))
    """Làm nhạt màu hex và trả về kết quả dưới dạng mã hex."""
    # Chuyển hex sang RGB
    rgb = _hexToRgb(hex_color)

    # Làm sáng màu bằng cách tăng giá trị RGB
    lightened_rgb = tuple(_clamp(int(c + (255 - c) * value)) for c in rgb)

    # Chuyển ngược lại sang hex
    return _rgbToHex(lightened_rgb)


def interpolate_color(start_color: str, end_color: str, factor: float) -> str:
    """Nội suy màu từ start_color đến end_color dựa trên giá trị factor từ 0 đến 1."""
    start_color = start_color.lstrip('#')
    end_color = end_color.lstrip('#')

    # Tách thành giá trị RGB
    start_rgb = [int(start_color[i:i+2], 16) for i in (0, 2, 4)]
    end_rgb = [int(end_color[i:i+2], 16) for i in (0, 2, 4)]

    # Tính giá trị màu nội suy
    interpolated_rgb = [
        int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * factor) for i in range(3)
    ]

    return '#{:02X}{:02X}{:02X}'.format(*interpolated_rgb)

def generate_color_palette(start_color: str, end_color: str, steps: int) -> list:
    """Tạo dải màu từ start_color đến end_color với số lượng bước colors."""
    return [interpolate_color(start_color, end_color, i / (steps - 1)) for i in range(steps)]


def get_contrast_text(background, contrast_threshold=3):
    """Trả về màu văn bản có độ tương phản cao nhất với nền."""
    dark_text = "#ffffff"
    light_text = "#000000"

    contrast_text = dark_text if getContrastRatio(background, dark_text) >= contrast_threshold else light_text
    
    # Kiểm tra độ tương phản nếu môi trường không phải production
    contrast = getContrastRatio(background, contrast_text)
    if contrast < 3:
        print(f"The contrast ratio of {contrast}:1 for {contrast_text} on {background} falls below the WCAG recommended minimum contrast ratio of 3:1.")
    
    return contrast_text


def rgba_to_hex(r=None, g=None, b=None, a=None, rgba=None):
    if rgba:
        rgba = str(rgba).replace("rgba(", "").replace(")", "").strip(" ").split(',')
        r, g, b, a = int(rgba[0]), int(rgba[1]), int(rgba[2]), int(rgba[3])
    """
    Chuyển đổi giá trị RGBA thành chuỗi mã màu hex.
    Tham số:
        r (int): Giá trị đỏ (0-255)
        g (int): Giá trị xanh lá cây (0-255)
        b (int): Giá trị xanh dương (0-255)
        a (int): Giá trị alpha (0-255)
    Trả về:
        str: Chuỗi mã màu hex tương ứng.
    """
    # Kiểm tra giá trị đầu vào
    for val in (r, g, b, a):
        if not (isinstance(val, int) and 0 <= val <= 255):
            raise ValueError("Các giá trị RGBA phải là số nguyên từ 0 đến 255.")
    return '#{:02x}{:02x}{:02x}{:02x}'.format(r, g, b, a)


def get_flat_ui_color_hex(color_name):
    flat_ui_colors = {
        "turquoise": "#1abc9c",
        "green_sea": "#16a085",
        "emerald": "#2ecc71",
        "nephritis": "#27ae60",
        "peter_river": "#3498db",
        "belize_hole": "#2980b9",
        "amethyst": "#9b59b6",
        "wisteria": "#8e44ad",
        "wet_asphalt": "#34495e",
        "midnight_blue": "#2c3e50",
        "sunflower": "#f1c40f",
        "orange": "#f39c12",
        "carrot": "#e67e22",
        "pumpkin": "#d35400",
        "alizarin": "#e74c3c",
        "pomegranate": "#c0392b",
        "clouds": "#ecf0f1",
        "silver": "#bdc3c7",
        "concrete": "#95a5a6",
        "asbestos": "#7f8c8d"
    }
    
    # Trả về mã màu hex hoặc None nếu không tìm thấy màu
    return flat_ui_colors.get(color_name.lower(), None)

def get_random_flat_ui_color():
    flat_ui_colors = [
        "#1abc9c",  # Turquoise
        "#16a085",  # Green Sea
        "#2ecc71",  # Emerald
        "#27ae60",  # Nephritis
        "#3498db",  # Peter River
        "#2980b9",  # Belize Hole
        "#9b59b6",  # Amethyst
        "#8e44ad",  # Wisteria
        "#34495e",  # Wet Asphalt
        "#2c3e50",  # Midnight Blue
        "#f1c40f",  # Sunflower
        "#f39c12",  # Orange
        "#e67e22",  # Carrot
        "#d35400",  # Pumpkin
        "#e74c3c",  # Alizarin
        "#c0392b",  # Pomegranate
        "#ecf0f1",  # Clouds
        "#bdc3c7",  # Silver
        "#95a5a6",  # Concrete
        "#7f8c8d",  # Asbestos
    ]
    
    return random.choice(flat_ui_colors)

# # Ví dụ sử dụng:
# color_hex = get_flat_ui_color_hex("turquoise")
# print(color_hex)  # Output: #1abc9c

# # Màu đầu và màu cuối
# start_color = '#161C24'  # Màu đầu
# end_color = '#212B36'    # Màu cuối

# # Tạo dải màu gồm 4 màu (main, secondary, thirty, content)
# palette = generate_color_palette(start_color, end_color, 4)

# # In kết quả
# for i, color in enumerate(palette, 1):
#     print(f"Màu {i}: {color}")

# Example usage
# color1 = '#ff5733'
# color2 = '#333333'
# print(rgbToHex('rgb(255, 87, 51)'))
# print(darken(color1, 0.2))

# print(get_contrast_text('#004B50'))
