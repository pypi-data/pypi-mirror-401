import inspect
from typing import Callable, List
from .use_state import State

def useEffect(callback: Callable, dependencies: List[State]) -> None:
    """
    Hook useEffect nhận vào một danh sách các dependency (State).
    Mỗi khi bất kỳ dependency nào thay đổi (phát tín hiệu valueChanged),
    callback sẽ được gọi.

    Nếu callback không nhận tham số, nó được gọi mà không có đối số.
    Nếu callback nhận ít nhất một tham số, một danh sách các giá trị hiện tại của các dependency
    sẽ được truyền vào.
    """
    try:
        sig = inspect.signature(callback)
    except (ValueError, TypeError):
        sig = None
    # Tạo đối số mặc định nếu không có
    default_args = {}
    if sig is not None and len(sig.parameters) > 0:
        default_args = {
            k: (v.default if v.default is not inspect.Parameter.empty else None)
            for k, v in sig.parameters.items()
        }
    for dep in dependencies:
        if isinstance(dep, State):
            dep.valueChanged.connect(lambda *args, **kwargs: callback(**default_args))
        else:
            raise ValueError("Dependencies only accepted State")
