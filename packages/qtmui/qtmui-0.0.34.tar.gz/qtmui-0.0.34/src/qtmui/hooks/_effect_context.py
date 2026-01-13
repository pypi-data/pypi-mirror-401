# src/qtmui/hooks/_effect_context.py
from __future__ import annotations
from typing import List, TYPE_CHECKING
from PySide6.QtCore import QObject
import weakref

if TYPE_CHECKING:
    from ._effect_runner import _EffectRunner  # tránh circular import


# Mỗi component sẽ có thuộc tính riêng: __effect_runners__
def _get_effect_runners(component: QObject) -> List[_EffectRunner]:
    """
    Lấy danh sách effect runners của component hiện tại.
    Tự động tạo nếu chưa có.
    """
    attr_name = "__qtmui_effect_runners__"
    if not hasattr(component, attr_name):
        # Dùng list bình thường (không weakref) vì runner tự deleteLater()
        setattr(component, attr_name, [])
    return getattr(component, attr_name)


def register_effect(component: QObject, runner: _EffectRunner) -> None:
    """
    Đăng ký một effect runner vào component hiện tại
    """
    runners = _get_effect_runners(component)
    runners.append(runner)

    # Tự động cleanup khi component bị destroy
    # Chỉ connect 1 lần duy nhất
    if len(runners) == 1:
        def _on_destroyed():
            runners_copy = list(runners)  # tránh modify while iterating
            for r in runners_copy:
                r.destroy()
            runners.clear()

        # Dùng weakref để tránh reference cycle
        weak_component = weakref.ref(component)
        def _safe_cleanup():
            comp = weak_component()
            if comp is not None:
                _on_destroyed()

        component.destroyed.connect(lambda obj: _safe_cleanup())


def cleanup_component_effects(component: QObject) -> None:
    """Gọi thủ công nếu cần (hiếm khi dùng)"""
    runners = getattr(component, "__qtmui_effect_runners__", None)
    if runners is not None:
        for r in list(runners):
            r.destroy()
        runners.clear()