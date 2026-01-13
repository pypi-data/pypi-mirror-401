from qtmui.hooks import useState, State
from dataclasses import dataclass

from typing import Callable, Dict
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QMainWindow, QWidget, QLineEdit
from PySide6.QtCore import QObject, Property, Signal



@dataclass
class Boolean:
  state: State
  onTrue: Callable
  onFalse: Callable
  onToggle: Callable
  toggle: Callable

class UseBoolean(QObject): # 

    def __init__(self, initValue=None):
        super().__init__()
        self.state, self.setState = useState(initValue)

    def onTrue(self, *args, **kwargs):
        self.setState(True)

    def onFalse(self):
        """Đặt lại trạng thái mở về None."""
        self.setState(False)

    def onToggle(self):
        """Đặt lại trạng thái mở về None."""
        if self.state.value:
            self.setState(False)
        else:
            self.setState(True)


def useBoolean(initValue=None) -> Boolean:
    """
    Hàm này trả về một instance của Popover,
    tương tự như cách bạn sử dụng hook trong React.
    """
    return UseBoolean(initValue)



# quickEdit = useBoolean(False)


