# qtmui/logging.py
import logging
import os
from typing import Optional
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Lấy biến DEBUG từ môi trường
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Thiết lập logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("qtmui.log"),  # Ghi log vào file
        logging.StreamHandler()  # Hiển thị log trên console
    ]
)

def get_logger(name: str) -> logging.Logger:
    """Tạo và trả về một logger với tên cụ thể."""
    return logging.getLogger(name)

# Định nghĩa các loại log
class LogType:
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUCCESS = "success"

# Mã màu ANSI
LOG_COLORS = {
    LogType.ERROR: "\033[91m",    # Red
    LogType.WARNING: "\033[93m",  # Yellow
    LogType.INFO: "\033[94m",     # Blue
    LogType.SUCCESS: "\033[92m",  # Green
    "RESET": "\033[0m",
}

def print_log(code: str, message: str, log_type: str = LogType.INFO, detail_message: Optional[str] = None):
    """In log với màu sắc tương ứng với loại log."""
    color = LOG_COLORS.get(log_type, LOG_COLORS["RESET"])
    info_color = LOG_COLORS[LogType.INFO]
    reset = LOG_COLORS["RESET"]
    # In phần chính của thông điệp với màu tương ứng
    print(f"{color}[{log_type.upper()}] {code}: {message}{reset}", end="")
    # Nếu có detail_message, in với màu INFO
    if detail_message:
        print(f"\n{info_color}{detail_message}{reset}")
    else:
        print()  # Xuống dòng nếu không có detail_message