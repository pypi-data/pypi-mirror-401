from typing import Dict, Any
import contextvars

# Biến toàn cục lưu hook context hiện tại
_current_hook_context = contextvars.ContextVar("current_hook_context")

class HookState:
    def __init__(self):
        self.memo: Dict[int, Any] = {}  # lưu dữ liệu từng hook theo index
        self._hook_index = 0

    def reset(self):
        """Reset hook index về 0 trước mỗi lần render"""
        self._hook_index = 0

    def next_index(self) -> int:
        """Trả index hiện tại, sau đó tăng"""
        index = self._hook_index
        self._hook_index += 1
        return index

    def get(self, index: int) -> Any:
        return self.memo.get(index)

    def set(self, index: int, value: Any):
        self.memo[index] = value

# Hàm lấy hook state hiện tại
def get_hook_state() -> HookState:
    try:
        return _current_hook_context.get()
    except LookupError:
        hs = HookState()
        _current_hook_context.set(hs)
        return hs

# Hàm đặt hook context (gọi ở đầu mỗi lần render component)
def set_current_hook_context(state: HookState):
    _current_hook_context.set(state)
