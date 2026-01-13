from collections.abc import Iterator
from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtCore import QObject


@contextmanager
def signals_blocked(obj: "QObject") -> Iterator[None]:
    """Context manager to temporarily block signals emitted by QObject: `obj`.

    Parameters
    ----------
    obj : QObject
        The QObject whose signals should be blocked.

    Examples
    --------
    ```python
    from PySide6.QtWidgets import QSpinBox
    from superqt import signals_blocked

    spinbox = QSpinBox()
    with signals_blocked(spinbox):
        spinbox.setValue(10)
    ```
    """
    previous = obj.blockSignals(True)
    try:
        yield
    finally:
        obj.blockSignals(previous)
