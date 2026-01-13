# src/qtmui/hooks/use_effect.py
import inspect
import weakref
from typing import Callable, List, Optional, Any
from PySide6.QtCore import QTimer, QObject
from .use_state import State
from ._effect_context import _get_current_effects

class _EffectRunner(QObject):
    def __init__(self, callback: Callable, deps: List[State]):
        super().__init__()
        self.callback = callback
        self.deps = deps or []
        self.cleanup: Optional[Callable] = None
        self.connections = []
        self._setup()

    def _setup(self):
        # Connect tất cả deps
        for dep in self.deps:
            if isinstance(dep, State):
                conn = dep.valueChanged.connect(self.run)
                self.connections.append((dep, conn))

        # Chạy lần đầu
        # self.run()

    def run(self):
        # Cleanup cũ
        if self.cleanup and callable(self.cleanup):
            try:
                self.cleanup()
            except Exception as e:
                print(f"[useEffect] Cleanup error: {e}")
            self.cleanup = None

        # Chạy callback mới
        try:
            result = self.callback()
            if callable(result):
                self.cleanup = result
        except Exception as e:
            print(f"[useEffect] Callback error: {e}")

    def destroy(self):
        # print('EffectRunnerdestroyed___________________________')
        # Final cleanup
        if self.cleanup and callable(self.cleanup):
            try:
                self.cleanup()
            except Exception as e:
                pass

        # Disconnect tất cả
        for dep, conn in self.connections:
            try:
                dep.valueChanged.disconnect(conn)
            except Exception as e:
                pass
            
        try:
            self.deleteLater()
        except Exception as e:
            pass

def useEffect(callback: Callable, dependencies: List[State]) -> None:
    # print('callback______________', callback)
    runner = _EffectRunner(callback, dependencies)
    _get_current_effects().append(runner)

def useLayoutEffect(callback: Callable, dependencies: List[State]) -> None:
    def wrapper():
        QTimer.singleShot(0, callback)
    useEffect(wrapper, dependencies)