import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()           # Ghi lại thời điểm bắt đầu
        result = func(*args, **kwargs)     # Thực hiện hàm
        end_time = time.time()             # Ghi lại thời điểm kết thúc
        elapsed = end_time - start_time    # Tính thời gian chạy
        print(f"_______________Function______________ '{func.__name__}' executed in {elapsed:.4f} seconds")
        return result
    return wrapper