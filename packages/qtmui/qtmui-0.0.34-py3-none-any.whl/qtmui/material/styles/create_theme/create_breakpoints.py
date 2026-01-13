from typing import Dict, Union

# Các keys cho breakpoints
BREAKPOINT_KEYS = ['xs', 'sm', 'md', 'lg', 'xl']

# Define Breakpoint as Union of str and any overrides (in Python we simplify this to just the string keys)
Breakpoint = str  # In Python, we just define this as str, e.g., 'xs', 'sm', 'md', 'lg', 'xl'

# Define the Breakpoints class
class Breakpoints:
    xs: int
    sm: int
    md: int
    lg: int
    xl: int
    
    def __init__(self, values: Dict[str, int] = None, unit: str = 'px', step: int = 5):
        # Giá trị mặc định cho các breakpoints
        self.values = values or {
            'xs': 0,      # extra-small
            'sm': 600,    # small
            'md': 900,    # medium
            'lg': 1200,   # large
            'xl': 1536    # extra-large
        }
        self.unit = unit
        self.step = step

        self.xs = self.values["xs"]
        self.sm = self.values["sm"]
        self.md = self.values["md"]
        self.lg = self.values["lg"]
        self.xl = self.values["xl"]

    def up(self, key: Union[str, int]) -> str:
        """ Trả về media query theo breakpoint lớn hơn hoặc bằng """
        value = self.values.get(key, key) if isinstance(key, str) else key
        return f"@media (min-width:{value}{self.unit})".encode('utf-8').decode('utf-8')

    def down(self, key: Union[str, int]) -> str:
        """ Trả về media query theo breakpoint nhỏ hơn """
        value = self.values.get(key, key) if isinstance(key, str) else key
        return f"@media (max-width:{value - self.step / 100}{self.unit})".encode('utf-8').decode('utf-8')

    def between(self, start: Union[str, int], end: Union[str, int]) -> str:
        """ Trả về media query theo khoảng giữa hai breakpoints """
        start_value = self.values.get(start, start) if isinstance(start, str) else start
        end_value = self.values.get(end, end) if isinstance(end, str) else end
        return f"@media (min-width:{start_value}{self.unit}) and (max-width:{end_value - self.step / 100}{self.unit})".encode('utf-8').decode('utf-8')

    def only(self, key: str) -> str:
        """ Trả về media query cho chỉ một breakpoint """
        key_index = BREAKPOINT_KEYS.index(key)
        if key_index + 1 < len(BREAKPOINT_KEYS):
            next_key = BREAKPOINT_KEYS[key_index + 1]
            return self.between(key, next_key)
        return self.up(key)

    def not_(self, key: str) -> str:
        """ Trả về media query để loại trừ một breakpoint """
        key_index = BREAKPOINT_KEYS.index(key)
        if key_index == 0:
            return self.up(BREAKPOINT_KEYS[1])
        if key_index == len(BREAKPOINT_KEYS) - 1:
            return self.down(BREAKPOINT_KEYS[key_index])
        return self.between(key, BREAKPOINT_KEYS[key_index + 1]).replace('@media', '@media not all and')


# Define BreakpointsOptions as a subclass of Breakpoints with optional parameters
class BreakpointsOptions(Breakpoints):
    def __init__(self, values: Dict[str, int] = None, unit: str = 'px', step: int = 5):
        super().__init__(values, unit, step)

    def apply(self, options: Dict[str, Union[int, str]] = None):
        """ Hàm để áp dụng các tùy chọn breakpoint """
        if options:
            self.values.update(options.get('values', self.values))
            self.unit = options.get('unit', self.unit)
            self.step = options.get('step', self.step)


# Hàm để tạo đối tượng Breakpoints
def createBreakpoints(options: Dict[str, Union[int, str]] = None) -> Breakpoints:
    breakpoints = BreakpointsOptions()
    if options:
        breakpoints.apply(options)
    return breakpoints


# Ví dụ sử dụng
# breakpoints = createBreakpoints({
#     'values': {'xs': 0, 'sm': 600, 'md': 900, 'lg': 1200, 'xl': 1536},
#     'unit': 'px',
#     'step': 5
# })

# # Sử dụng các phương thức
# print(breakpoints.up('sm'))    # @media (min-width:600px)
# print(breakpoints.down('lg'))  # @media (max-width:1199.95px)
# print(breakpoints.between('sm', 'lg'))  # @media (min-width:600px) and (max-width:1199.95px)
# print(breakpoints.only('md'))  # @media (min-width:900px) and (max-width:1199.95px)
# print(breakpoints.not_('sm'))  # @media not all and (min-width:900px) and (max-width:1199.95px)
