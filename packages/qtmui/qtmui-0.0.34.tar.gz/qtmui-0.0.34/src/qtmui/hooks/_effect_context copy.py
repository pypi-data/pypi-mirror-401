# src/qtmui/hooks/_effect_context.py
from typing import List
from PySide6.QtCore import QObject

_CURRENT_EFFECTS: List[QObject] = []

def _get_current_effects() -> List[QObject]:
    global _CURRENT_EFFECTS
    return _CURRENT_EFFECTS

def _cleanup_all_effects():
    global _CURRENT_EFFECTS
    for runner in _CURRENT_EFFECTS[:]:
        runner.destroy()
    _CURRENT_EFFECTS.clear()

# Tự động gọi khi component destroy
def register_component_cleanup(component) -> None:
    def _on_destroy():
        print('Component destroyed, cleaning up effects...', getattr(component, "_key"))
        _cleanup_all_effects()
    component.destroyed.connect(lambda obj: _on_destroy())