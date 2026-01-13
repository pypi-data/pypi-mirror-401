from dataclasses import dataclass, field
from typing import Optional

# Define ShapeOptions
@dataclass
class ShapeOptions:
    borderRadius: Optional[float] = None  # ShapeOptions là Partial, có thể không có đầy đủ các thuộc tính của Shape

# Define Shape
@dataclass
class Shape:
    borderRadius: int = 4  # Giá trị mặc định là 4.0, giống như trong MUI

# Function to merge shape options with default shape
def createShape(options: Optional[ShapeOptions] = None) -> Shape:
    # Nếu không có options, trả về đối tượng Shape mặc định
    if options is None:
        return Shape()
    
    # Tạo shape mới dựa trên options được cung cấp (Partial<Shape>)
    borderRadius = options.borderRadius if options.borderRadius is not None else 4
    
    return Shape(borderRadius=borderRadius)

# # Khởi tạo một shape mặc định
# default_shape = createShape()

# # Ví dụ về shape với các tùy chọn
# custom_shape = createShape(ShapeOptions(borderRadius=8.0))

# print(default_shape)  # Kết quả: Shape(borderRadius=4.0)
# print(custom_shape)   # Kết quả: Shape(borderRadius=8.0)
