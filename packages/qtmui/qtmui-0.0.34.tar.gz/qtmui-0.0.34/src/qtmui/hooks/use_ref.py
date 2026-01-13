from typing import Any, Generic, TypeVar, Optional

T = TypeVar('T')

class RefObject(Generic[T]):
    """
    A generic class that simulates React's useRef.
    It holds a mutable value that can be accessed and modified.
    """
    def __init__(self, current: Optional[T] = None):
        self.current: Optional[T] = current

    def __repr__(self):
        return f"RefObject(current={self.current})"

def useRef(initial_value: Optional[T] = None) -> RefObject[T]:
    """
    A function that simulates React's useRef hook.
    It returns a RefObject that holds a mutable value.
    """
    return RefObject(initial_value)