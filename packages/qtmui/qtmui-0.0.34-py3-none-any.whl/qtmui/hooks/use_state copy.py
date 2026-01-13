from typing import Callable
from PySide6.QtCore import QObject, Property, Signal


class State(QObject):
    valueChanged = Signal(object)

    def __init__(self, value=None):
        super().__init__()
        self._value = value

    def __getattr__(self, name):
        """
        Forward attribute/method lookup sang self._value
        """
        return getattr(self._value, name)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        self.valueChanged.emit(self._value)

    value = Property(object, get_value, set_value, notify=valueChanged)

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


def useState(initialValue, typeCheck=None):
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
    state = State(initialValue)
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
    

# def useBoolean(initialValue=False)->ReturnType:
#     """
#     Hàm useBoolean quản lý trạng thái boolean.

#     Args:
#         initialValue: Giá trị khởi tạo (mặc định là False).
    
#     Returns:
#         tuple: Một tuple chứa state boolean, hàm set giá trị, và hàm toggle.
#     """
#     if not isinstance(initialValue, bool):
#         raise TypeError(f"Expected a boolean value, but got {type(initialValue)}")

#     state = State(initialValue)

#     def toggle():
#         """Đảo ngược giá trị của state."""
#         state.set_value(not state.get_value())

#     def onTrue():
#         """Đảo ngược giá trị của state."""
#         state.set_value(not state.get_value())

#     # return state, state.set_value, toggle
#     return ReturnType(state, state.set_value, toggle)

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

# # Tạo state
# _checkedKeys, _setCheckedKeys = useState([0])

# # Kết nối tín hiệu để in giá trị mới khi state thay đổi
# _checkedKeys.valueChanged.connect(print)

# # Cập nhật state đúng cách
# checkedKeysList = _checkedKeys.get_value()  # Lấy danh sách hiện tại
# checkedKeysList.remove(0)  # Thay đổi danh sách
# _setCheckedKeys(checkedKeysList)  # Cập nhật state với danh sách mới

# # # Kiểm tra bằng cách chạy ứng dụng ..site_packages.qtcompat (nếu cần)
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     window = QWidget()
# #     layout = QVBoxLayout()
    
# #     # Các thành phần khác của UI
# #     window.setLayout(layout)
# #     window.show()
# #     sys.exit(app.exec())



"""
À, mình hiểu rồi 👍.

Lỗi của bạn đến từ việc `useState` luôn trả về một `State` object, mà khi bạn dùng:

```python
if message.find("Create profile group") != -1:
```

thì Python nghĩ `message` là một `State`, chứ không phải `str`.

---

### Giải pháp 1: Luôn unwrap `.value`

Bạn có thể bắt buộc khi dùng `message` phải gọi:

```python
if message.value.find("Create profile group") != -1:
```

Cách này rõ ràng nhưng hơi dài dòng.

---

### Giải pháp 2: Override `__getattr__`

Bạn có thể sửa class `State` để "bọc" giá trị bên trong, và forward mọi method đến `_value`.

Ví dụ:

```python
class State(QObject):
    valueChanged = Signal(object)

    def __init__(self, value=None):
        super().__init__()
        self._value = value

    def __getattr__(self, name):
        # Forward attribute/method lookup sang self._value
        return getattr(self._value, name)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        self.valueChanged.emit(self._value)

    value = Property(object, get_value, set_value, notify=valueChanged)

    def __str__(self):
        return str(self._value)

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return float(self._value)

    def __bool__(self):
        return bool(self._value)

    def __eq__(self, other):
        return self._value == (other.value if isinstance(other, State) else other)

    def __lt__(self, other):
        return self._value < (other.value if isinstance(other, State) else other)
```

Giờ thì:

```python
message, setMessage = useState("")
if message.find("Create profile group") != -1:
    ...
```

👉 chạy được luôn, vì `.find` sẽ được forward sang `str`.

---

### Giải pháp 3: Generic + Type Hint

Nếu muốn **ép kiểu ngay từ khi khai báo**, bạn có thể dùng **Generics** trong Python typing:

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class State(QObject, Generic[T]):
    valueChanged = Signal(object)

    def __init__(self, value: T):
        super().__init__()
        self._value: T = value

    def get_value(self) -> T:
        return self._value

    def set_value(self, value: T):
        self._value = value
        self.valueChanged.emit(self._value)

    value = Property(object, get_value, set_value, notify=valueChanged)

def useState(initialValue: T) -> tuple[State[T], Callable[[T], None]]:
    state = State(initialValue)
    return state, state.set_value
```

Giờ nếu bạn dùng:

```python
message, setMessage = useState("")  # type: State[str], Callable[[str], None]
```

thì IDE (PyCharm, VSCode) sẽ hiểu `message` là `State[str]`, và bạn sẽ được gợi ý `.value` là `str`.

---

✅ Nếu muốn code ngắn gọn như React (`message.find(...)`) thì chọn **Giải pháp 2 (override `__getattr__`)**.
✅ Nếu muốn an toàn về type-check thì chọn **Giải pháp 3 (Generic)**.

---

Bạn muốn mình viết một phiên bản kết hợp cả **type-safe (Generic)** lẫn **forward method (để gọi trực tiếp `message.find`)**, để vừa ngắn gọn vừa an toàn, không?


"""