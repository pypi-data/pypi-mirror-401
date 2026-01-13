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
    sig = inspect.signature(callback)
    
    if len(sig.parameters) == 0:
        # Callback không nhận tham số
        for dep in dependencies:
            if isinstance(dep, State):
                # Sử dụng default argument để tránh vấn đề late binding
                dep.valueChanged.connect(lambda value, dep=dep: callback())
    else:
        # Callback nhận ít nhất 1 tham số, truyền vào danh sách giá trị hiện tại của dependencies
        for dep in dependencies:
            if isinstance(dep, State):
                dep.valueChanged.connect(lambda value, dep=dep: callback([d.value for d in dependencies]))
