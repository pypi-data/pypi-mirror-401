class ComponentSizes:
    """
    Class chứa các kích thước mặc định cho component.
    """
    small = 26
    medium = 34
    large = 42
    extra_large = 48
    tiny = 18
    huge = 64
    fload_label_height = 10

    @classmethod
    def get_size(cls, size: str) -> str:
        """
        Trả về kích thước theo tên.
        """
        if hasattr(cls, size):
            return f"{getattr(cls, size)}px".encode('utf-8').decode('utf-8')
        else:
            raise ValueError(f"Kích thước '{size}' không tồn tại trong ComponentSizes.")


class LayoutSizes:
    """
    Class chứa các kích thước mặc định cho layout.
    """
    small = 8
    medium = 16
    large = 32
    extra_large = 64

    @classmethod
    def get_size(cls, size: str) -> str:
        """
        Trả về kích thước theo tên.
        """
        if hasattr(cls, size):
            return f"{getattr(cls, size)}px".encode('utf-8').decode('utf-8')
        else:
            raise ValueError(f"Kích thước '{size}' không tồn tại trong LayoutSizes.")


class Sizes:
    """
    Class chính quản lý các nhóm kích thước như component và layout.
    """
    def __init__(self):
        self.component = ComponentSizes()
        self.layout = LayoutSizes()

    @classmethod
    def get_component_size(cls, size: str) -> str:
        """
        Trả về kích thước của component.
        """
        return cls().component.get_size(size)

    @classmethod
    def get_layout_size(cls, size: str) -> str:
        """
        Trả về kích thước của layout.
        """
        return cls().layout.get_size(size)


# # Giả định cấu trúc của store._state.theme.custom.size để chứa kích thước tùy chỉnh
# class Store:
#     def __init__(self):
#         # Cấu trúc state giả định
#         self._state = {
#             'theme': {
#                 'custom': {
#                     'size': {
#                         'component': {
#                             'small': '36px',  # Custom size cho small component
#                             'medium': '44px',  # Custom size cho medium component
#                         },
#                         'layout': {
#                             'large': '40px'  # Custom size cho large layout
#                         }
#                     }
#                 }
#             }
#         }


# store = Store()  # Khởi tạo store với dữ liệu tùy chỉnh


# Hàm tạo size
def create_size(component_or_layout: str=None, size: str=None) -> Sizes:
    """
    Tạo kích thước dựa trên cấu hình tùy chỉnh nếu có, nếu không thì sử dụng mặc định.
    
    :param component_or_layout: "component" hoặc "layout"
    :param size: "small", "medium", "large", v.v.
    :return: kích thước cuối cùng được tính toán
    """

    return Sizes()


    # Truy cập kích thước tùy chỉnh từ store
    custom_sizes = store._state['theme']['custom']['size'].get(component_or_layout, {})

    # Kiểm tra xem kích thước có được định nghĩa trong cấu hình tùy chỉnh hay không
    if size in custom_sizes:
        return custom_sizes[size]  # Trả về kích thước tùy chỉnh

    # Nếu không có cấu hình tùy chỉnh, trả về kích thước mặc định
    if component_or_layout == "component":
        return Sizes.get_component_size(size)
    elif component_or_layout == "layout":
        return Sizes.get_layout_size(size)
    else:
        raise ValueError(f"'{component_or_layout}' không hợp lệ, chỉ có thể là 'component' hoặc 'layout'.")
    

'''
# Ví dụ sử dụng create_size

# Trả về kích thước tùy chỉnh cho component (small)
print(create_size('component', 'small'))  # Output: "36px" (custom size)

# Trả về kích thước mặc định cho component (large)
print(create_size('component', 'large'))  # Output: "48px" (default size)

# Trả về kích thước tùy chỉnh cho layout (large)
print(create_size('layout', 'large'))     # Output: "40px" (custom size)

# Trả về kích thước mặc định cho layout (medium)
print(create_size('layout', 'medium'))    # Output: "16px" (default size)
'''