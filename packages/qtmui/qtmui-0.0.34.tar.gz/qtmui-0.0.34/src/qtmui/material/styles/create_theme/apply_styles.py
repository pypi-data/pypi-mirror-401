from typing import Dict, Callable

# Giả lập đối tượng CSSObject, đại diện cho các thuộc tính CSS
class CSSObject:
    css: str


class ApplyStyles:
    """
    Class ApplyStyles để áp dụng style dựa trên chế độ màu từ theme.
    """
    def __init__(self, theme: Dict[str, Callable[[str], str]]):
        """
        :param theme: Đối tượng theme chứa các phương thức hoặc biến liên quan đến chế độ màu.
        """
        self.theme = theme

    def __call__(self, key: str, styles: CSSObject) -> CSSObject:
        """
        Áp dụng style dựa trên key (chế độ màu) và trả về các thuộc tính CSS tương ứng.
        
        :param key: Chế độ màu (ví dụ: "light", "dark")
        :param styles: Các thuộc tính CSS cần áp dụng
        :return: Các style đã được áp dụng nếu khớp với chế độ màu hoặc một đối tượng trống
        """
        if self.theme.get('vars') and callable(self.theme.get('getColorSchemeSelector')):
            # Lấy selector dựa trên key (ví dụ: 'light' hoặc 'dark')
            selector = self.theme['getColorSchemeSelector'](key).replace(r'(\[[^\]]+\])', '*:where($1)')
            return {selector: styles}
        
        # Nếu chế độ màu của palette khớp với key
        if self.theme.get('palette', {}).get('mode') == key:
            return styles

        # Nếu không khớp, trả về đối tượng trống
        return {}

# # Ví dụ sử dụng ApplyStyles
# theme = {
#     'palette': {'mode': 'dark'},
#     'vars': None,
#     'getColorSchemeSelector': lambda key: f'[data-mui-color-scheme="{key}"]'
# }

# # Khởi tạo ApplyStyles với theme
# apply_styles = ApplyStyles(theme)

# # Áp dụng các style cho chế độ 'dark'
# styles = apply_styles('dark', {'background': '#1c1c1c', 'color': '#fff'})
# print(styles)  # Kết quả: {'[data-mui-color-scheme="dark"]': {'background': '#1c1c1c', 'color': '#fff'}}

