# src/qtmui/hooks/use_state.py
from PySide6.QtCore import QObject, Signal, Property
from typing import TypeVar, Tuple, Callable, Any

T = TypeVar('T')

class State(QObject):
    valueChanged = Signal(object)

    def __init__(self, value: T):
        super().__init__()
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: T):
        if self._value != new_value:
            self._value = new_value
            self.valueChanged.emit(self._value)

    def set_value(self, new_value: T):
        self.value = new_value

    def __getattr__(self, name):
        """
        Forward attribute/method lookup sang self._value
        """
        return getattr(self._value, name)

    def __str__(self):
        return str(self._value)

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return float(self._value)

    def __bool__(self):
        return bool(self._value)

    def __eq__(self, other):
        """

        Args:
            other (_type_): _description_

        Returns:
            _type_: _description_
            
        error: 
            state = State(...)
            message, setMessage = useState(state)   # => _value lại là State
            thì bạn đã tạo State lồng State, khi so sánh hoặc in chuỗi sẽ sinh vòng lặp vô hạn.
        
            - Việc set một state là một state sẽ dẫn tới vòng lặp vô hạn
            @store.autorun(lambda state: state.profile.message)
            def _message(state: str):
                setMessage(message)


        """
        if isinstance(other, State):
            return self._value == other._value   # tránh gọi State.value (vì Property có thể kích hoạt so sánh tiếp)
        return self._value == other

    def __lt__(self, other):
        if isinstance(other, State):
            return self._value < other._value
        return self._value < other

# class State(QObject):
#     valueChanged = Signal(object)

#     def __init__(self, value=None):
#         super().__init__()
#         self._value = value

#     def __getattr__(self, name):
#         """
#         Forward attribute/method lookup sang self._value
#         """
#         return getattr(self._value, name)

#     def get_value(self):
#         return self._value

#     def set_value(self, value):
#         self._value = value
#         self.valueChanged.emit(self._value)

#     value = Property(object, get_value, set_value, notify=valueChanged)

#     def __str__(self):
#         return str(self._value)

#     def __int__(self):
#         return int(self._value)

#     def __float__(self):
#         return float(self._value)

#     def __bool__(self):
#         return bool(self._value)

#     def __eq__(self, other):
#         """

#         Args:
#             other (_type_): _description_

#         Returns:
#             _type_: _description_
            
#         error: 
#             state = State(...)
#             message, setMessage = useState(state)   # => _value lại là State
#             thì bạn đã tạo State lồng State, khi so sánh hoặc in chuỗi sẽ sinh vòng lặp vô hạn.
        
#             - Việc set một state là một state sẽ dẫn tới vòng lặp vô hạn
#             @store.autorun(lambda state: state.profile.message)
#             def _message(state: str):
#                 setMessage(message)


#         """
#         if isinstance(other, State):
#             return self._value == other._value   # tránh gọi State.value (vì Property có thể kích hoạt so sánh tiếp)
#         return self._value == other

#     def __lt__(self, other):
#         if isinstance(other, State):
#             return self._value < other._value
#         return self._value < other

def useState(initial: T | Callable[[], T]) -> Tuple[State, Callable[[T], None]]:
    from inspect import currentframe
    frame = currentframe().f_back
    self_obj = frame.f_locals.get('self')

    if callable(initial) and not isinstance(initial, State):
        initial = initial()

    state = State(initial)
    if hasattr(self_obj, '__states__'):
        self_obj.__states__.append(state)
    return state, state.set_value



def useContext(initialValue, typeCheck=None):
    """
    Hàm useState với hỗ trợ kiểm tra kiểu dữ liệu và giá trị khởi tạo.
    
    Args:
        typeCheck: Kiểu dữ liệu cần kiểm tra (có thể là một hoặc nhiều kiểu).
        initialValue: Giá trị khởi tạo của state.
    """
    # Kiểm tra kiểu dữ liệu của initialValue (nếu typeCheck được cung cấp)
    if typeCheck is not None and not isinstance(initialValue, typeCheck):
        raise TypeError(f"Expected {typeCheck}, but got {type(initialValue)}")
    
    # Tạo đối tượng state với giá trị ban đầu
    context = State(initialValue)
    return context, context.set_value

class ReturnType:
    def __init__(self, value, set_value, toggle):
        self.value = value
        self.set_value = set_value
        self.toggle = toggle

    def onTrue()->None:
        ...
    def onFalse()->None:
        ...
    def onToggle()->None:
        ...
    def toggle()->None:
        ...
    

class UserForm:
    def __init__(self, value, set_value, toggle):
        self.value = value
        self.set_value = set_value
        self.toggle = toggle

    def handleSubmit(self, onSubmit: Callable=None)->Callable:
        ...
    def setValue(self, value: object=None)->None:
        ...
    def formState(self, value: object=None)->dict:
        return {}
    def control(self, value: object=None)->dict:
        ...
    def reset(self)->None:
        ...
    def watch(self)->None:
        ...
    
    

def useForm(resolver: Callable=None, defaultValues: object=None)->UserForm:
    """
    Hàm useBoolean quản lý trạng thái boolean.

    Args:
        initialValue: Giá trị khởi tạo (mặc định là False).
    
    Returns:
        tuple: Một tuple chứa state boolean, hàm set giá trị, và hàm toggle.
    """
    # if not isinstance(initialValue, bool):
    #     raise TypeError(f"Expected a boolean value, but got {type(initialValue)}")

    state = State(defaultValues)

    def toggle():
        """Đảo ngược giá trị của state."""
        state.set_value(not state.get_value())

    def onTrue():
        """Đảo ngược giá trị của state."""
        state.set_value(not state.get_value())

    # return state, state.set_value, toggle
    return UserForm(state, state.set_value, toggle)
