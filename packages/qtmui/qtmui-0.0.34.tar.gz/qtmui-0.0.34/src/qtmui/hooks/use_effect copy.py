from typing import Callable, Optional, Union
import hashlib
from functools import lru_cache, partial
from PySide6.QtCore import QObject, Signal
from .use_state import State, useState

class Effect(QObject):
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
        deps.valueChanged.connect(setValue)
        return value

# # @lru_cache(maxsize=128)
# def useEffect(callback=None, dependencies=Optional[Union[list, State]])->None:
#     # @lru_cache(maxsize=128)
#     # def get_cache(dependencies):
#     #     return dependencies

#     # dependencies.valueChanged.connect(get_cache)

#     if isinstance(dependencies, list):
#         for state in dependencies:
#          isinstance(state, State) and state.valueChanged.connect(lambda state=state: callback(state))
#     else:
#          isinstance(dependencies, State) and dependencies.valueChanged.connect(lambda state=dependencies: callback(state))

# @lru_cache(maxsize=128)
def useEffect(callback=None, dependencies=Optional[Union[list, State]])->None:
    # @lru_cache(maxsize=128)
    # def get_cache(dependencies):
    #     return dependencies

    # dependencies.valueChanged.connect(get_cache)

    if isinstance(dependencies, list):
        for state in dependencies:
         isinstance(state, State) and state.valueChanged.connect(lambda value, *args, **kwargs: callback(*args, **kwargs))
    else:
         isinstance(dependencies, State) and dependencies.valueChanged.connect(lambda value, *args, **kwargs: callback(*args, **kwargs))
        #  dependencies.valueChanged.emit(dependencies.value)





