from typing import Callable, Optional
import hashlib
from functools import lru_cache, partial
from PySide6.QtCore import QObject, Signal
from .use_state import State, useState

class MemoHook(QObject):
    valueChanged = Signal(object)
    def __init__(self):
        self.cache = {}

    def _hash_deps(self, deps):
        return hashlib.md5(str(deps).encode()).hexdigest()

    def use_memo(self, fn, deps):
        deps_hash = self._hash_deps(deps)
        if deps_hash in self.cache:
            cached_value = self.cache[deps_hash]
            return cached_value["value"]
        else:
            value = fn()
            self.cache = {deps_hash: {"value": value}}
            return deps
        
    def exec(self, fn: Callable, deps: Optional[State]):
        value, setValue = useState(fn(deps))
        deps.valueChanged.connect(setValue) # nguyên mẫu, tuy nhiên hoạt động tốt với form, xem lại
        # deps.valueChanged.connect(lambda: setValue(fn(deps)))
        return value

# @lru_cache(maxsize=128)
def useMemo(callback=None, dependencies=None)->State:
    # @lru_cache(maxsize=128)
    # def get_cache(dependencies):
    #     return dependencies

    # dependencies.valueChanged.connect(get_cache)
    memoHook = MemoHook()
    value = memoHook.exec(callback, dependencies)
    return value



