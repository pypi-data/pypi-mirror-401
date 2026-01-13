
from dataclasses import is_dataclass


def merge(*dict_args)-> dict:
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def dataclass_to_dict(obj):
    """Đệ quy chuyển dataclass Palette và các lớp con thành dict."""
    if is_dataclass(obj):
        result = {}
        for k, v in obj.__dict__.items():
            if callable(v):
                # bỏ qua các function
                continue
            result[k] = dataclass_to_dict(v)
        return result
    elif isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [dataclass_to_dict(v) for v in obj]
    else:
        return obj