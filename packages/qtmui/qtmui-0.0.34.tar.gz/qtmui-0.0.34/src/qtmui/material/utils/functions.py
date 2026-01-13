import inspect

def _get_fn_args(fn):
    # Kiểm tra số lượng tham số của callback
    sig = inspect.signature(fn)
    # Tạo đối số mặc định nếu không có
    default_args = {
        k: (v.default if v.default is not inspect.Parameter.empty else None)
        for k, v in sig.parameters.items()
    }
    return default_args
