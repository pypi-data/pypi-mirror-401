# src/qtmui/hooks/use_effect.py
import inspect
from typing import Callable, List, Optional
from PySide6.QtCore import QTimer, QObject
from .use_state import State
from ._effect_context import register_effect
from ._effect_runner import _EffectRunner  # sẽ tạo file này


def useEffect(callback: Callable, dependencies: List[State]) -> None:
    # Lấy component hiện tại từ call stack
    frame = inspect.currentframe().f_back
    component = frame.f_locals.get('self')
    if not component or not isinstance(component, QObject):
        raise RuntimeError("useEffect must be called inside a Section/QObject component")

    runner = _EffectRunner(callback, dependencies)
    register_effect(component, runner)


def useLayoutEffect(callback: Callable, dependencies: List[State]) -> None:
    def wrapped():
        QTimer.singleShot(0, callback)
    useEffect(wrapped, dependencies)