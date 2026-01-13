# src/qtmui/hooks/_effect_runner.py
from typing import Callable, List, Optional
from PySide6.QtCore import QObject
from .use_state import State


class _EffectRunner(QObject):
    def __init__(self, callback: Callable, deps: List[State]):
        super().__init__()
        self.callback = callback
        self.deps = deps or []
        self.cleanup: Optional[Callable] = None
        self.connections = []
        self._setup()

    def _setup(self):
        for dep in self.deps:
            if isinstance(dep, State):
                conn = dep.valueChanged.connect(self.run)
                self.connections.append((dep, conn))
        # self.run()  # lần đầu

    def run(self):
        # Cleanup cũ
        if self.cleanup and callable(self.cleanup):
            try:
                self.cleanup()
            except Exception as e:
                print(f"[useEffect] Cleanup error: {e}")
            self.cleanup = None

        # Chạy mới
        try:
            result = self.callback()
            if callable(result):
                self.cleanup = result
        except Exception as e:
            print(f"[useEffect] Error: {e}")

    def destroy(self):
        if self.cleanup and callable(self.cleanup):
            try:
                self.cleanup()
            except Exception:
                pass

        for dep, conn in self.connections:
            try:
                dep.valueChanged.disconnect(conn)
            except RuntimeWarning as e:
                pass
            
        try:
            self.deleteLater()
        except Exception as e:
            pass