from typing import Callable, Dict, List, Optional, Any
import inspect
from qtmui.hooks import State
from .use_boolean import UseBoolean

class CallbackState:
    """Lớp để lưu trữ trạng thái của callback."""
    def __init__(self):
        self.has_been_called: bool = False
        self.cached_args: List[Any] = []
        self.cached_kwargs: Dict[str, Any] = {}

def useCallback(callback: Callable = None, dependencies: Optional[List[State]] = []) -> Callable:
    """
    Khởi tạo một callback có khả năng cache tham số và gọi lại khi các phụ thuộc thay đổi.
    - callback: Callable - Hàm callback cần được gọi.
    - dependencies: Optional[List[State]] - Danh sách các State phụ thuộc, khi chúng thay đổi, callback sẽ được gọi lại.
    Trả về: Callable - Hàm wrapper để gọi callback với khả năng cache tham số.
    """
    # Kiểm tra số lượng tham số của callback
    sig = inspect.signature(callback)
    # Tạo dictionary chứa các tham số mặc định từ chữ ký của callback
    default_args = {
        k: (v.default if v.default is not inspect.Parameter.empty else None)
        for k, v in sig.parameters.items()
    }

    # Tạo đối tượng để lưu trữ trạng thái của callback
    state = CallbackState()

    # Định nghĩa hàm wrapper để gọi callback và cache tham số
    def wrapper(*args, **kwargs):
        # Cập nhật trạng thái
        state.has_been_called = True
        state.cached_args = list(args)
        state.cached_kwargs = dict(kwargs)
        # Gọi callback với các tham số hiện tại
        return callback(*args, **kwargs)

    # Định nghĩa hàm xử lý khi phụ thuộc thay đổi
    def handle_dependency_change(value, state=state):
        if state.has_been_called:
            # Nếu callback đã được gọi ít nhất một lần, sử dụng tham số đã cache
            callback(*state.cached_args, **state.cached_kwargs)
        else:
            # Nếu chưa được gọi lần nào, gọi callback với các tham số mặc định từ chữ ký
            callback(**default_args)

    # Nếu có các phụ thuộc
    if isinstance(dependencies, list) and len(dependencies):
        for dep in dependencies:
            # Kết nối tín hiệu valueChanged với hàm xử lý
            if isinstance(dep, UseBoolean):
                dep = dep.state
            dep.valueChanged.connect(handle_dependency_change)

    return wrapper