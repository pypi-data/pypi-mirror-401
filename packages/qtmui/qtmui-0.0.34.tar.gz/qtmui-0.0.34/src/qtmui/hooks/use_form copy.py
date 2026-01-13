from .use_state import useState, State
from dataclasses import dataclass

from typing import Callable, Dict
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QMainWindow, QWidget, QLineEdit
from PySide6.QtCore import QObject, Property, Signal



# @dataclass
# class UseFormType:
#   state: State
#   handleSubmit: Callable
#   setValue: Callable
#   formState: Callable
# #   formState: dict
#   control: dict
#   watch: Callable -> State...
#   reset: Callable
#   resolver: Callable

@dataclass
class UseFormType:
    state: State
    handleSubmit: Callable[..., any]
    setValue: Callable[..., any]
    formState: Callable[..., any]
    control: dict
    watch: Callable[..., dict]
    reset: Callable[..., any]
    resolver: Callable[..., any]

class UseForm(QObject): # 
    controlChanged = Signal(object)
    stateChanged = Signal(object)

    def __init__(self, resolver=None, values: dict=None):
        super().__init__()
        if isinstance(values, State):
            self.state: State = values
            self.data, self.setData = useState(self.state.value)
        elif isinstance(values, dict):
            self.state, _ = useState(values)
            self.data, self.setData = useState(self.state.value)

        self.resolver = resolver

    def handleSubmit(self, *args, **kwargs):
        self.setData(True)

    def setValue(self):
        """Đặt lại trạng thái mở về None."""
        self.setData(False)

    def watch(self):
        """In ra fromState."""
        # print(self.state)
        return self.state.value

    def reset(self):
        """In ra fromState."""
        self.setData({})

    # def getFormState(self):
    #     return self.formState

    # def setFormState(self, value):
    #     self.formState = value
    #     # self.stateChanged.emit(self.formState)

    def getControl(self):
        return self.control

    def formState(self):
        return self.state
    
    def control(self):
        return self.state

    def setControl(self, value):
        self.control = value
        self.controlChanged.emit(self.control)

    # formState = Property(object, getFormState, setFormState, notify=stateChanged)
    # control = Property(object, getControl, setControl, notify=controlChanged)
 
def useForm(resolver: Callable=None, values: object=None)->UseFormType:
    """
    Hàm này trả về một instance của Popover,
    tương tự như cách bạn sử dụng hook trong React.
    """
    return UseForm(resolver, values)



# quickEdit = useBoolean(False)


