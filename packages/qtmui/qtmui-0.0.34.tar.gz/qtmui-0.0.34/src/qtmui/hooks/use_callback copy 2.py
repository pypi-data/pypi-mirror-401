import inspect
from typing import Callable, List, Optional
from .hook_state import get_hook_state  # hoặc tương đương trong PyMUI của bạn

def useCallback(callback: Callable, dependencies: Optional[List["State"]] = None) -> Callable:
    """
    Trả về một hàm được ghi nhớ. Khi được gọi, hàm sẽ cache lại args/kwargs.
    Khi dependencies thay đổi, callback được gọi lại với args/kwargs cũ.
    """
    hook_state = get_hook_state()
    index = hook_state.next_index()

    # Khởi tạo state hook nếu chưa có
    if index not in hook_state.memo:
        hook_state.memo[index] = {
            "callback": callback,
            "deps": dependencies or [],
            "last_args": None,
            "last_kwargs": None
        }

        # Kết nối sự kiện cho từng dependency
        for dep in hook_state.memo[index]["deps"]:
            dep.valueChanged.connect(lambda _=None, idx=index: _on_dep_changed(idx))

    def _on_dep_changed(idx):
        print('co vaoooooooooooooooo')
        entry = hook_state.memo[idx]
        if entry["last_args"] is not None or entry["last_kwargs"] is not None:
            entry["callback"](*entry["last_args"], **entry["last_kwargs"])

    def memoized_func(*args, **kwargs):
        entry = hook_state.memo[index]
        entry["last_args"] = args
        entry["last_kwargs"] = kwargs
        return entry["callback"](*args, **kwargs)

    return memoized_func
