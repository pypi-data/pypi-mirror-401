from typing import Any, Callable, Dict, Optional
from .use_state import useState, State
from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal

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
    fields: State

# Context toàn cục để lưu trữ UseForm instance
class FormContext(QObject):
    _instance = None

    @classmethod
    def setInstance(cls, instance: 'UseForm'):
        cls._instance = instance

    @classmethod
    def getInstance(cls) -> Optional['UseForm']:
        return cls._instance

# Định nghĩa lại UseForm để tương thích với context
class UseForm(QObject):
    controlChanged = Signal(object)
    stateChanged = Signal(object)

    def __init__(self, resolver=None, values=None):
        super().__init__()
        if isinstance(values, State):
            self.state: State = values
        elif isinstance(values, dict):
            self.state, _ = useState(values)
        self.data, self.setData = useState(self.state.value)
        self.resolver = resolver
        self.fields, self.setFields = useState([])
        self.isReset, self.setIsReset = useState(False)
        FormContext.setInstance(self)  # Lưu instance vào context

    def handleSubmit(self, *args, **kwargs):
        self.setData(True)

    def setValue(self, name: str, value: Any):
        current_data = self.state.value.copy()
        current_data[name] = value
        self.setData(current_data)

    def watch(self) -> State:
        return self.data

    def reset(self):
        self.setData({})
        self.setIsReset(True)

    def formState(self) -> State:
        return self.state

    def control(self) -> Dict[str, Any]:
        return self.state.value

def useForm(resolver: Callable=None, values: object=None)->UseFormType:
    """
    Hàm này trả về một instance của Popover,
    tương tự như cách bạn sử dụng hook trong React.
    """
    return UseForm(resolver, values)


@dataclass
class UseFormContextType:
    # state: State
    # handleSubmit: Callable[..., any]
    # setValue: Callable[..., any]
    # formState: Callable[..., any]
    # control: dict
    # watch: Callable[..., dict]
    # reset: Callable[..., any]
    # resolver: Callable[..., any]
    control: Optional[Any]
    setValue: Callable[..., any]
    watch: Callable[..., dict]
    resetField: Callable[..., any]

# Hàm useFormContext
def useFormContext() -> UseFormContextType:
    instance = FormContext.getInstance()
    if not instance:
        raise ValueError("useFormContext must be used within a FormProvider")
    # return UseFormType(
    #     state=instance.state,
    #     handleSubmit=instance.handleSubmit,
    #     setValue=instance.setValue,
    #     formState=instance.formState,
    #     control=instance.control,
    #     watch=instance.watch,
    #     reset=instance.reset,
    #     resolver=instance.resolver,
    # )
    context = UseFormContextType(
        control=instance,
        setValue=instance.setValue,
        watch=instance.watch,
        resetField=instance.reset,
    )
    return context


