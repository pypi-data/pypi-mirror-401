from typing import Callable, Dict, Any, Optional, Union

# Định nghĩa kiểu TransformFunction, mô phỏng việc chuyển đổi giá trị dựa trên theme
TransformFunction = Callable[[Any, dict], Any]

# SimpleStyleFunction mô phỏng việc xử lý các thuộc tính style dựa trên prop
class SimpleStyleFunction:
    def __init__(self, func: Callable[[dict], dict]):
        self.func = func

    def __call__(self, props: dict) -> dict:
        return self.func(props)

# Định nghĩa SxConfigRecord, tương tự với định nghĩa trong TypeScript
class SxConfigRecord:
    def __init__(self,
                 css_property: Optional[str] = None,
                 theme_key: Optional[str] = None,
                 transform: Optional[TransformFunction] = None,
                 style: Optional[SimpleStyleFunction] = None):
        """
        :param css_property: Tên thuộc tính CSS hoặc False nếu không áp dụng
        :param theme_key: Khóa truy cập dot trong theme (nếu có)
        :param transform: Hàm chuyển đổi giá trị dựa trên theme
        :param style: Hàm xử lý các thuộc tính style dựa trên props
        """
        self.css_property = css_property
        self.theme_key = theme_key
        self.transform = transform
        self.style = style

# Định nghĩa SxConfig như một mapping giữa tên thuộc tính và SxConfigRecord
SxConfig = Dict[str, SxConfigRecord]

# Hàm xử lý mặc định cho SimpleStyleFunction
def default_style_function(props: dict) -> dict:
    # Đây là nơi bạn có thể xử lý các thuộc tính style dựa trên props
    return {key: value for key, value in props.items()}

# Tạo defaultSxConfig tương tự như defaultSxConfig trong TypeScript
defaultSxConfig: SxConfig = {
    'margin': SxConfigRecord(css_property='margin', transform=lambda value, theme: f"{value}px"),
    'padding': SxConfigRecord(css_property='padding', style=SimpleStyleFunction(default_style_function)),
    'color': SxConfigRecord(css_property='color', theme_key='palette.color', transform=lambda value, theme: theme.get('palette', {}).get('color', value))
}

# Ví dụ sử dụng defaultSxConfig
theme = {'palette': {'color': 'red'}}
sx_config_record = defaultSxConfig.get('color')

# Áp dụng transform function nếu có
if sx_config_record and sx_config_record.transform:
    transformed_value = sx_config_record.transform('blue', theme)
    # print(f"Transformed value: {transformed_value}")  # Kết quả: red (vì lấy từ theme)



"""
theme = {'palette': {'color': 'red'}}
sx_config_record = defaultSxConfig.get('color')

# Áp dụng transform function nếu có
if sx_config_record and sx_config_record.transform:
    transformed_value = sx_config_record.transform('blue', theme)
    print(f"Transformed value: {transformed_value}")  # Kết quả: red (vì lấy từ theme)


"""