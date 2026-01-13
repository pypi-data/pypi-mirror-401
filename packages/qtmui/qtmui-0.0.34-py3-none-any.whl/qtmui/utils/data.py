from typing import Callable
from functools import wraps
import json

# Hàm để merge dict tương tự lodash.merge
def merge_dicts(*dict_args)-> dict:
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def deep_merge(a, b):
    """
    Gộp hai giá trị a và b.
    - Nếu cả a và b đều là dict, thực hiện gộp sâu các key.
    - Nếu cả a và b đều callable, tạo một hàm mới gọi cả hai hàm và merge kết quả trả về.
    - Ngược lại, ưu tiên giá trị b (giá trị ghi đè).
    """
    # Nếu cả hai đều là dict, gộp chúng theo cách đệ quy:
    if isinstance(a, dict) and isinstance(b, dict):
        result = a.copy()
        for key, value in b.items():
            if key in result:
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    # Nếu cả hai đều callable:
    if callable(a) and callable(b):
        return lambda *args, **kwargs: deep_merge(a(*args, **kwargs), b(*args, **kwargs))
    # Trường hợp còn lại: ưu tiên b (gọi là override)
    return b if b is not None else a


def convert_sx_params_to_str(func):
    @wraps(func)
    def wrapper(sx, *args, **kwargs):
        # Nếu params là dict, chuyển nó thành chuỗi JSON (hoặc sử dụng str() nếu phù hợp)
        if isinstance(sx, dict):
            sx = json.dumps(sx)
        elif isinstance(sx, Callable):
            sx = sx()
            sx = json.dumps(sx)
        else:
            if sx == None:
                sx = ""
        return func(sx, *args, **kwargs)
    return wrapper

def convert_sx_params_to_dict(func):
    @wraps(func)
    def wrapper(sx, *args, **kwargs):
        # Nếu params là dict, chuyển nó thành chuỗi JSON (hoặc sử dụng str() nếu phù hợp)
        if isinstance(sx, str) and sx != "":
            try:
                sx = json.loads(sx)
            except Exception as e:
                print('sxxxxxxxxxx_errrrrrrrrrrrrr', type(sx))
        return func(sx, *args, **kwargs)
    return wrapper


