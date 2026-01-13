import inspect
from typing import Callable, Optional, List
import hashlib
from functools import lru_cache, partial
from PySide6.QtCore import QObject, Signal
from .use_state import State, useState

class MemoHook(QObject):
    valueChanged = Signal(object)

    def __init__(self):
        super().__init__()
        self.cache = {}

    def _hash_deps(self, deps: List) -> str:
        """
        Tạo hash từ danh sách các dependencies.
        (Ở đây, ta dùng hàm str(deps) để chuyển đổi; nếu dependencies không thể convert sang string an toàn,
         hãy thay đổi hàm này cho phù hợp.)
        """
        return hashlib.md5(str(deps).encode()).hexdigest()

    def use_memo(self, fn: Callable, deps: List) -> any:
        deps_hash = self._hash_deps(deps)
        if deps_hash in self.cache:
            return self.cache[deps_hash]["value"]
        else:
            value = fn()
            self.cache[deps_hash] = {"value": value}
            return value

    def exec(self, fn: Callable, deps: Optional[List[State]]):
        """
        Khởi tạo state dựa trên giá trị tính từ callback (dựa trên dependencies)
        Và kết nối tín hiệu valueChanged của từng dependency để cập nhật state khi có thay đổi.
        """
        if deps:
            # Kiểm tra số lượng tham số của callback
            sig = inspect.signature(fn)
            # Tạo đối số mặc định nếu không có
            default_args = {
                k: (v.default if v.default is not inspect.Parameter.empty else None)
                for k, v in sig.parameters.items()
            }

            value, setValue = useState(fn(**default_args))

            for dep in deps:
                dep.valueChanged.connect(lambda *args, **kwargs: setValue(fn(**default_args)))

        else:
            value, setValue = useState(fn())
        return value

# def useMemo(callback: Callable = None, dependencies: Optional[List[State]] = None) -> State:
#     """
#     Hook useMemo nhận callback và danh sách dependencies.
#     Giá trị trả về sẽ được tính toán lại chỉ khi một trong các dependency thay đổi.
#     """
#     memoHook = MemoHook()
#     value = memoHook.exec(callback, dependencies)
#     return value

def test_useMemo(value):
    # Test case cho hook useMemo
    memoHook = MemoHook()
    result = memoHook.use_memo(lambda: 42, [])
    assert result == 42
    # Kiểm tra cache
    assert memoHook.cache

def test_useMemo_1(value):
    print('test_useMemo_1_________________________', value)

def useMemo(callback: Callable = None, dependencies: Optional[List[State]] = None) -> State:
    """
    Hook useMemo nhận callback và danh sách dependencies.
    Giá trị trả về sẽ được tính toán lại chỉ khi một trong các dependency thay đổi.
    """
    # Kiểm tra số lượng tham số của callback
    sig = inspect.signature(callback)
    # Tạo đối số mặc định nếu không có
    default_args = {
        k: (v.default if v.default is not inspect.Parameter.empty else None)
        for k, v in sig.parameters.items()
    }

    value, setValue = useState(callback(**default_args))

    # if isinstance(dependencies, list) and len(dependencies):
    if isinstance(dependencies, list):
        for dep in dependencies:
            dep.valueChanged.connect(lambda *args, **kwargs: setValue(callback(**default_args)))
    else:
        raise ValueError("Invalid dependencies, dependencies must be a list.")
    return value