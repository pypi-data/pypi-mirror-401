from functools import wraps


import inspect
from typing import Callable, Optional, List
import hashlib
from functools import lru_cache, partial
from PySide6.QtCore import QObject, Signal
from .use_state import State, useState


def useCallback(callback: Callable = None, dependencies: Optional[List[State]] = []) -> Callable:
        """
        Khởi tạo state dựa trên giá trị tính từ callback (dựa trên dependencies)
        Và kết nối tín hiệu valueChanged của từng dependency để cập nhật state khi có thay đổi.
        """
        # Kiểm tra số lượng tham số của callback
        sig = inspect.signature(callback)
        # Tạo đối số mặc định nếu không có
        default_args = {
            k: (v.default if v.default is not inspect.Parameter.empty else None)
            for k, v in sig.parameters.items()
        }

        # value, setValue = useState(callback(**default_args))

        if isinstance(dependencies, list) and len(dependencies):
            for dep in dependencies:
                dep.valueChanged.connect(lambda default_args=default_args, *args, **kwargs: callback(**default_args))
        return callback


# def useCallback(callback, dependencies):
#     cache = {'value': None, 'dependencies': None}
    
#     @wraps(callback)
#     def wrapper(*args, **kwargs):
#         if cache['dependencies'] is None or cache['dependencies'] != dependencies:
#             cache['value'] = callback(*args, **kwargs)
#             cache['dependencies'] = dependencies[:]
#         return cache['value']
    
#     return wrapper




# # Giả lập các hằng số và đối tượng router
# LOGINPATHS = {'email': '/login/email', 'google': '/login/google'}
# router = {
#     'path': '/current/path',
#     'replace': lambda href: print(f"Redirecting to {href}"),
#     'setChecked': lambda value: print(f"Checked set to {value}")
# }

# # Trạng thái và phương pháp giả lập
# authenticated = False
# method = 'email'

# def check(authenticated, method, router):
#     if not authenticated:
#         searchParams = f"returnTo={router['path']}"
#         loginPath = LOGINPATHS[method]
#         href = f"{loginPath}?{searchParams}"
#         router['replace'](href)
#     else:
#         router['setChecked'](True)

# # Các dependencies mà hàm useCallback cần
# dependencies = [authenticated, method, router]

# # Gọi useCallback để tạo hàm được cache
# cachedCheck = useCallback(check, dependencies)

# # Sử dụng hàm được cache
# cachedCheck(authenticated, method, router)

# messesQuer(1, 2, 3, 4) 

# reduxThunk 
# async 

