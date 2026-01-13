from typing import Union, Callable, List

# SpacingArgument có thể là số hoặc chuỗi
SpacingArgument = Union[int, str]

# Spacing có thể nhận nhiều cách gọi khác nhau, tùy thuộc vào số lượng đối số
class Spacing:
    """
    export interface Spacing {
        (): string;
        (value: number): string;
        (topBottom: SpacingArgument, rightLeft: SpacingArgument): string;
        (top: SpacingArgument, rightLeft: SpacingArgument, bottom: SpacingArgument): string;
        (top: SpacingArgument, right: SpacingArgument, bottom: SpacingArgument, left: SpacingArgument): string;
    }
    """
    default_spacing = 6
    def __call__(self, *args: SpacingArgument) -> str:
        # Nếu không có đối số, trả về khoảng cách mặc định
        self.default_spacing = 6
        if len(args) == 0:
            return "6px"  # Giả sử khoảng cách mặc định là 8px
        # Nếu có 1 đối số
        if len(args) == 1:
            return f"{args[0]*self.default_spacing}px".encode('utf-8').decode('utf-8')
        # Nếu có 2 đối số
        if len(args) == 2:
            return f"{args[0]*self.default_spacing}px {args[1]*self.default_spacing}px".encode('utf-8').decode('utf-8')
        # Nếu có 3 đối số
        if len(args) == 3:
            return f"{args[0]*self.default_spacing}px {args[1]*self.default_spacing}px {args[2]*self.default_spacing}px".encode('utf-8').decode('utf-8')
        # Nếu có 4 đối số
        if len(args) == 4:
            return f"{args[0]*self.default_spacing}px {args[1]*self.default_spacing}px {args[2]*self.default_spacing}px {args[3]*self.default_spacing}px".encode('utf-8').decode('utf-8')
        # Nếu có nhiều hơn 4 đối số
        raise ValueError("Too many arguments provided, expected between 0 and 4")

# SpacingOptions có thể là số, một danh sách, hoặc một callable
SpacingOptions = Union[int, List[Union[int, str]], Callable[[Union[int, str]], Union[int, str]]]


def createUnarySpacing(spacingInput: SpacingOptions):
    """
    Chuyển đổi spacing input thành khoảng cách sử dụng một đơn vị khoảng cách mặc định.
    """
    def transform(value: Union[int, str]) -> Union[int, str]:
        if isinstance(value, int):
            return value * spacingInput if isinstance(spacingInput, int) else value
        return value

    return transform


def create_spacing(spacingInput: SpacingOptions = 6) -> Spacing:
    """
    Tạo ra một đối tượng Spacing từ một input spacing cụ thể.
    """
    # Nếu spacingInput đã có mui flag, trả về chính nó
    if isinstance(spacingInput, Spacing):
        return spacingInput

    # Tạo transform function dựa trên input spacing
    transform = createUnarySpacing(spacingInput)

    # Định nghĩa Spacing function
    def spacing(*args: SpacingArgument) -> str:
        if len(args) > 4:
            raise ValueError(f"Too many arguments provided, expected between 0 and 4, got {len(args)}")
        args = args if len(args) > 0 else [1]  # Nếu không có đối số, sử dụng giá trị mặc định
        return " ".join(
            [f"{transform(arg)}px".encode('utf-8').decode('utf-8') if isinstance(transform(arg), int) else transform(arg) for arg in args]
        )
        
    # def intSpacing(*args: SpacingArgument) -> str:
    #     if len(args) > 4:
    #         raise ValueError(f"Too many arguments provided, expected between 0 and 4, got {len(args)}")
    #     args = args if len(args) > 0 else [1]  # Nếu không có đối số, sử dụng giá trị mặc định
    #     return " ".join(
    #         [f"{transform(arg)}px".encode('utf-8').decode('utf-8') if isinstance(transform(arg), int) else transform(arg) for arg in args]
    #     )

    # Gắn mui flag vào spacing
    spacing.mui = True
    return spacing

# # Ví dụ sử dụng createSpacing
# spacing = createSpacing(8)

# # Các cách gọi hàm spacing khác nhau
# print(spacing())                    # Output: "8px"
# print(spacing(4))                   # Output: "32px"
# print(spacing(4, 8))                # Output: "32px 64px"
# print(spacing(4, 8, 16))            # Output: "32px 64px 128px"
# print(spacing(4, 8, 16, 32))        # Output: "32px 64px 128px 256px"
