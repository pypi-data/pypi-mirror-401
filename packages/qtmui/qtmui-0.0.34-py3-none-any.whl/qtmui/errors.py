# qtmui/errors.py
from typing import Dict, List, Optional, Union, get_origin, get_args

class PyMuiErrorCodes:
    INVALID_TYPE = "PME-1000"
    INVALID_VALUE = "PME-1001"
    INVALID_CONDITION = "PME-1002"

class PyMuiError(Exception):
    def __init__(self, code: str, message: str, details: Optional[Dict] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        full_message = "PyMuiError [" + str(code) + "]:\n" + str(message)
        super().__init__(full_message)

    def __str__(self):
        return str(self.message)

class PyMuiValidationError(PyMuiError):
    def __init__(
        self,
        file_path: str,
        param_name: str,
        param_value: any,
        expected_types: Union[type, List[type], str],
        expected_values: Optional[List[any]] = None,
        error_type: str = "INVALID_TYPE",
        message: Optional[str] = None
    ):
        code = {
            "INVALID_TYPE": PyMuiErrorCodes.INVALID_TYPE,
            "INVALID_VALUE": PyMuiErrorCodes.INVALID_VALUE,
            "INVALID_CONDITION": PyMuiErrorCodes.INVALID_CONDITION
        }.get(error_type, PyMuiErrorCodes.INVALID_TYPE)

        # Chuẩn hóa expected_types thành chuỗi để hiển thị
        if get_origin(expected_types) is Union:
            types_list = get_args(expected_types)
            types_str = "Union[" + ", ".join(str(type_name.__name__) for type_name in types_list) + "]"
        elif isinstance(expected_types, (list, tuple)):
            types_str = ", ".join(str(type_name.__name__) for type_name in expected_types)
        elif isinstance(expected_types, type):
            types_str = str(expected_types.__name__)
        else:
            types_str = str(expected_types)

        # Chuẩn hóa expected_values thành chuỗi dạng "value1" | "value2" | ...
        if expected_values:
            values_str = " | ".join('"' + str(val) + '"' for val in expected_values)
        else:
            values_str = "N/A"

        # Tạo thông điệp lỗi theo cấu trúc chuyên nghiệp
        if message is None:
            if error_type == "INVALID_TYPE":
                message = "Invalid argument type received"
            elif error_type == "INVALID_VALUE":
                message = "Invalid argument value received"
            else:
                message = "Validation failed for parameter '" + str(param_name) + "'"

        # Tạo phần chính của thông điệp
        self.main_message = (
            "PyMuiError [" + str(code) + "]:\n" +
            "  File: '" + str(file_path) + "'\n" +
            "  Message: " + str(message)
        )

        # Tạo phần chi tiết (Detail) với giá trị
        self.detail_message = (
            "Details:\n" +
            "  Parameter: '" + str(param_name) + "'\n" +
            "  Received: " + str(param_value) + "\n" +
            "  Expected Types: " + str(types_str) + "\n" +
            "  Expected Values: " + str(values_str)
        )

        full_message = self.main_message + "\n" + self.detail_message
        details = {
            "param_name": param_name,
            "param_value": param_value,
            "param_type": "unknown",  # Loại bỏ type(param_value).__name__
            "expected_types": types_str,
            "expected_values": values_str
        }
        super().__init__(code, full_message, details)

    def get_main_message(self):
        """Trả về phần chính của thông điệp lỗi (không bao gồm Detail)."""
        return self.main_message

    def get_detail_message(self):
        """Trả về phần chi tiết của thông điệp lỗi."""
        return self.detail_message