# qtmui/utils/validate_params.py
from typing import Any, Optional, Union, Dict, List, get_args, get_origin

from qtmui.errors import PyMuiValidationError
from qtmui.hooks import State
from PySide6.QtWidgets import QWidget

# Hàm kiểm tra số nguyên dương (positive integer)
def validate_positive_integer(param_name: str, value: Optional[Union[int, State]], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là số nguyên dương hoặc State chứa số nguyên dương.
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'columns').
    :param value: Giá trị cần kiểm tra (có thể là int hoặc State chứa int).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if not isinstance(actual_value, int) or actual_value <= 0:
            return "Parameter '" + str(param_name) + "' must be a positive integer, but got '" + str(actual_value) + "'"
    elif not isinstance(actual_value, int) or actual_value <= 0:
        return "Parameter '" + str(param_name) + "' must be a positive integer, but got '" + str(actual_value) + "'"
    return None

# Hàm kiểm tra số dương (positive number)
def validate_positive_number(param_name: str, value: Optional[Union[int, float, State]], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là số dương (lớn hơn 0) hoặc State chứa số dương.
    :param param_name: Tên của tham số cần kiểm tra.
    :param value: Giá trị cần kiểm tra (có thể là int, float hoặc State chứa int/float).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if not isinstance(actual_value, (int, float)) or actual_value <= 0:
            return "Parameter '" + str(param_name) + "' must be a positive number, but got '" + str(actual_value) + "'"
    elif not isinstance(actual_value, (int, float)) or actual_value <= 0:
        return "Parameter '" + str(param_name) + "' must be a positive number, but got '" + str(actual_value) + "'"
    return None

# Hàm kiểm tra số không âm (non-negative number)
def validate_non_negative_number(param_name: str, value: Optional[Union[int, float, State]], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là số không âm (0 hoặc lớn hơn) hoặc State chứa số không âm.
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'spacing').
    :param value: Giá trị cần kiểm tra (có thể là int, float hoặc State chứa int/float).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if not isinstance(actual_value, (int, float)) or actual_value < 0:
            return "Parameter '" + str(param_name) + "' must be a non-negative number, but got '" + str(actual_value) + "'"
    elif not isinstance(actual_value, (int, float)) or actual_value < 0:
        return "Parameter '" + str(param_name) + "' must be a non-negative number, but got '" + str(actual_value) + "'"
    return None

# Hàm kiểm tra spacing (khoảng cách)
def validate_spacing(param_name: str, value: Optional[Union[int, Dict, State]], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là số không âm, dict chứa số không âm, hoặc State chứa giá trị như vậy.
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'spacing').
    :param value: Giá trị cần kiểm tra (có thể là int, dict hoặc State chứa int/dict).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if isinstance(actual_value, dict):
            for key, val in actual_value.items():
                if not isinstance(val, (int, float)) or val < 0:
                    return "Value of parameter '" + str(param_name) + "' for breakpoint '" + str(key) + "' must be a non-negative number, but got '" + str(val) + "'"
        elif not isinstance(actual_value, (int, float)) or actual_value < 0:
            return "Parameter '" + str(param_name) + "' must be a non-negative number or dict containing non-negative numbers, but got '" + str(actual_value) + "'"
    elif isinstance(value, dict):
        for key, val in value.items():
            if not isinstance(val, (int, float)) or val < 0:
                return "Value of parameter '" + str(param_name) + "' for breakpoint '" + str(key) + "' must be a non-negative number, but got '" + str(val) + "'"
    elif not isinstance(actual_value, (int, float)) or actual_value < 0:
        return "Parameter '" + str(param_name) + "' must be a non-negative number or dict containing non-negative numbers, but got '" + str(actual_value) + "'"
    return None

# Hàm kiểm tra sx (style tùy chỉnh)
def validate_sx(param_name: str, value: Optional[Union[State, str, Dict]], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là dict, str, hoặc State chứa một trong các kiểu này.
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'sx').
    :param value: Giá trị cần kiểm tra (có thể là dict, str hoặc State chứa kiểu tương ứng).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if not isinstance(actual_value, (dict, str)):
            return "Parameter '" + str(param_name) + "' must be a dict, str, or State containing one of these types, but got '" + str(actual_value) + "'"
    elif not isinstance(actual_value, (dict, str)):
        return "Parameter '" + str(param_name) + "' must be a dict, str, or State containing one of these types, but got '" + str(actual_value) + "'"
    return None

# Hàm kiểm tra giá trị boolean
def validate_bool(param_name: str, value: Optional[Union[bool, State]], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là boolean hoặc State chứa boolean.
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'container').
    :param value: Giá trị cần kiểm tra (có thể là bool hoặc State chứa bool).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if not isinstance(actual_value, bool):
            return "Parameter '" + str(param_name) + "' must be a boolean or State containing a boolean, but got '" + str(actual_value) + "'"
    elif not isinstance(actual_value, bool):
        return "Parameter '" + str(param_name) + "' must be a boolean or State containing a boolean, but got '" + str(actual_value) + "'"
    return None

# Hàm kiểm tra chuỗi
def validate_string(param_name: str, value: Optional[Union[str, State]], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là chuỗi hoặc State chứa chuỗi.
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'key').
    :param value: Giá trị cần kiểm tra (có thể là str hoặc State chứa str).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if not isinstance(actual_value, str):
            return "Parameter '" + str(param_name) + "' must be a string or State containing a string, but got '" + str(actual_value) + "'"
    elif not isinstance(actual_value, str):
        return "Parameter '" + str(param_name) + "' must be a string or State containing a string, but got '" + str(actual_value) + "'"
    return None

# Hàm kiểm tra giá trị nằm trong danh sách cho phép
def validate_choice(param_name: str, value: Optional[Union[str, State]], valid_values: List[str], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là một trong các giá trị hợp lệ hoặc State chứa giá trị hợp lệ.
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'wrap').
    :param value: Giá trị cần kiểm tra (có thể là str hoặc State chứa str).
    :param valid_values: Danh sách các giá trị hợp lệ (ví dụ: ["wrap", "nowrap", "wrap-reverse"]).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if not isinstance(actual_value, str) or actual_value not in valid_values:
            return "Parameter '" + str(param_name) + "' must be one of " + str(list(valid_values)) + ", but got '" + str(actual_value) + "'"
    elif not isinstance(actual_value, str) or actual_value not in valid_values:
        return "Parameter '" + str(param_name) + "' must be one of " + str(list(valid_values)) + ", but got '" + str(actual_value) + "'"
    return None

# Hàm kiểm tra dict chứa số nguyên dương
def validate_dict_with_positive_integers(param_name: str, value: Optional[Union[Dict, State]], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là dict hoặc State chứa dict, với các giá trị là số nguyên dương.
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'size').
    :param value: Giá trị cần kiểm tra (có thể là dict hoặc State chứa dict).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if not isinstance(actual_value, dict):
            return "Parameter '" + str(param_name) + "' must be a dict or State containing a dict, but got '" + str(actual_value) + "'"
        for key, val in actual_value.items():
            if val is not None and (not isinstance(val, int) or val <= 0):
                return "Value of parameter '" + str(param_name) + "' for breakpoint '" + str(key) + "' must be a positive integer, but got '" + str(val) + "'"
    elif not isinstance(actual_value, dict):
        return "Parameter '" + str(param_name) + "' must be a dict or State containing a dict, but got '" + str(actual_value) + "'"
    else:
        for key, val in value.items():
            if val is not None and (not isinstance(val, int) or val <= 0):
                return "Value of parameter '" + str(param_name) + "' for breakpoint '" + str(key) + "' must be a positive integer, but got '" + str(val) + "'"
    return None

# Hàm kiểm tra children (các phần tử con)
def validate_children(param_name: str, value: Optional[Union[str, list, QWidget, State]], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là str, list, QWidget, hoặc State chứa một trong các kiểu này.
    Nếu là list, các phần tử phải là QWidget.
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'children').
    :param value: Giá trị cần kiểm tra (có thể là str, list, QWidget hoặc State chứa kiểu tương ứng).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if not isinstance(actual_value, (str, list)):
            return "Parameter '" + str(param_name) + "' must be a str, list, or State containing one of these types, but got '" + str(actual_value) + "'"
        if isinstance(actual_value, list):
            for child in actual_value:
                if child is not None and not isinstance(child, QWidget):
                    return "Each element in list '" + str(param_name) + "' must be a QWidget, but got '" + str(child) + "'"
    elif not isinstance(actual_value, (str, list, QWidget)):
        return "Parameter '" + str(param_name) + "' must be a str, list, QWidget, or State containing one of these types, but got '" + str(actual_value) + "'"
    if isinstance(value, list):
        for child in value:
            if child is not None and not isinstance(child, QWidget):
                return "Each element in list '" + str(param_name) + "' must be a QWidget, but got '" + str(child) + "'"
    return None

# Hàm kiểm tra divider (dùng trong Stack)
def validate_divider(param_name: str, value: Optional[Union[QWidget, bool, State]], allow_none: bool = True, **kwargs) -> Optional[str]:
    """
    Kiểm tra tham số có phải là QWidget, bool, hoặc State chứa một trong các kiểu này.
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'divider').
    :param value: Giá trị cần kiểm tra (có thể là QWidget, bool hoặc State chứa kiểu tương ứng).
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :return: Thông điệp lỗi nếu có, hoặc None nếu hợp lệ.
    """
    if allow_none and value is None:
        return None
    actual_value = value.value if isinstance(value, State) else value
    if isinstance(value, State):
        if not isinstance(actual_value, (QWidget, bool)):
            return "Parameter '" + str(param_name) + "' must be a QWidget, bool, or State containing one of these types, but got '" + str(actual_value) + "'"
    elif not isinstance(actual_value, (QWidget, bool)):
        return "Parameter '" + str(param_name) + "' must be a QWidget, bool, or State containing one of these types, but got '" + str(actual_value) + "'"
    return None

# Decorator để áp dụng validation cho tham số
def validate_param(validator_func, param_name, allow_none=True, **kwargs):
    """
    Decorator để kiểm tra tham số trước khi gán giá trị.
    :param validator_func: Hàm kiểm tra được sử dụng (ví dụ: validate_spacing).
    :param param_name: Tên của tham số cần kiểm tra (ví dụ: 'spacing').
    :param allow_none: Cho phép giá trị None hay không (mặc định là True).
    :param kwargs: Các tham số bổ sung để truyền vào hàm kiểm tra (ví dụ: valid_values).
    """
    def decorator(func):
        def wrapper(self, value):
            # Tạo một dict chứa các tham số cần thiết cho validator_func
            validator_kwargs = kwargs.copy()
            validator_kwargs["allow_none"] = allow_none  # Truyền allow_none vào validator_func
            actual_value = value.value if isinstance(value, State) else value
            error_message = validator_func(param_name=param_name, value=value, **validator_kwargs)
            if error_message:
                error_type = "INVALID_VALUE" if "must be one of" in error_message else "INVALID_TYPE"
                expected_types = None
                expected_values = validator_kwargs.get("valid_values", None)
                if error_type == "INVALID_TYPE":
                    if validator_func == validate_sx:
                        expected_types = [dict, str]
                    elif validator_func == validate_bool:
                        expected_types = bool
                    elif validator_func == validate_string:
                        expected_types = str
                    elif validator_func == validate_positive_integer:
                        expected_types = int
                    elif validator_func == validate_positive_number:
                        expected_types = [int, float]
                    elif validator_func == validate_non_negative_number:
                        expected_types = [int, float]
                    elif validator_func == validate_spacing:
                        expected_types = [int, float, dict]
                    elif validator_func == validate_dict_with_positive_integers:
                        expected_types = dict
                    elif validator_func == validate_children:
                        expected_types = [str, list, QWidget]
                    elif validator_func == validate_divider:
                        expected_types = [QWidget, bool]
                # raise ValidationError(
                #     component_name=self.__class__.__name__,
                #     param_name=param_name,
                #     value=actual_value,
                #     message=error_message,
                #     expected_types=expected_types,
                #     expected_values=expected_values,
                #     error_type=error_type
                # )
            return func(self, value)
        return wrapper
    return decorator

def _validate_param(file_path: str, param_name: str, supported_signatures: Union[type, List[type], str], valid_values: Optional[List[Any]] = None, validator: Optional[callable] = None):
    """Decorator để kiểm tra tham số trước khi gán giá trị."""
    def decorator(func):
        def wrapper(self, value):
            # Xử lý giá trị thực tế nếu là State
            actual_value = value.value if isinstance(value, State) else value

            # Xử lý supported_signatures dạng Union
            if get_origin(supported_signatures) is Union:
                supported_types = get_args(supported_signatures)
            else:
                supported_types = supported_signatures if isinstance(supported_signatures, (list, tuple)) else [supported_signatures]

            # Kiểm tra kiểu dữ liệu
            if not isinstance(actual_value, tuple(supported_types)):
                error = PyMuiValidationError(
                    file_path=file_path,
                    param_name=param_name,
                    param_value=actual_value,
                    expected_types=supported_signatures,
                    expected_values=valid_values,
                    error_type="INVALID_TYPE"
                )
                raise error

            # Kiểm tra giá trị hợp lệ nếu có
            if valid_values is not None and not isinstance(value, State):
                if actual_value not in valid_values:
                    error = PyMuiValidationError(
                        file_path=file_path,
                        param_name=param_name,
                        param_value=actual_value,
                        expected_types=supported_signatures,
                        expected_values=valid_values,
                        error_type="INVALID_VALUE"
                    )
                    raise error

            # Nếu là State, kiểm tra giá trị của State
            if isinstance(value, State):
                if not isinstance(actual_value, tuple(supported_types)):
                    error = PyMuiValidationError(
                        file_path=file_path,
                        param_name=param_name,
                        param_value=actual_value,
                        expected_types=supported_signatures,
                        expected_values=valid_values,
                        error_type="INVALID_TYPE"
                    )
                    raise error
                if valid_values is not None and actual_value not in valid_values:
                    error = PyMuiValidationError(
                        file_path=file_path,
                        param_name=param_name,
                        param_value=actual_value,
                        expected_types=supported_signatures,
                        expected_values=valid_values,
                        error_type="INVALID_VALUE"
                    )
                    raise error

            # Kiểm tra điều kiện tùy chỉnh (validator) nếu có
            if validator is not None:
                check_value = value.value if isinstance(value, State) else value
                if not validator(check_value):
                    error = PyMuiValidationError(
                        file_path=file_path,
                        param_name=param_name,
                        param_value=check_value,
                        expected_types=supported_signatures,
                        error_type="INVALID_CONDITION",
                        message="Parameter '" + str(param_name) + "' does not satisfy the validation condition: " + str(check_value)
                    )
                    raise error

            return func(self, value)
        return wrapper
    return decorator