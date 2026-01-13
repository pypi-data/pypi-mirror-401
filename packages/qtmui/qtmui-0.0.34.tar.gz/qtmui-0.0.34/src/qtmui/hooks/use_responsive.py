import sys
from typing import Any, Optional
from qtmui.material.styles import useTheme
from .use_media_query import useMediaQuery
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSize
from qtmui.hooks import useState, State

def get_screen_size() -> tuple[int, int]:
    """
    Lấy kích thước màn hình chính của ứng dụng.

    Returns:
        Tuple gồm (width, height) của màn hình.
    """
    # Nếu đã có QApplication instance, sử dụng nó; nếu không, tạo mới
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Lấy màn hình chính
    screen = app.primaryScreen()
    size = screen.size()
    return size.width(), size.height()


# def useMediaQuery(query_str: str) -> bool:
#     """
#     Giả lập hook kiểm tra media query.
#     Trong thực tế, bạn có thể dựa vào kích thước cửa sổ hoặc các điều kiện môi trường khác.
#     Ở đây, ta chỉ in ra chuỗi query và trả về False làm giá trị mặc định.
#     """
#     print(f"Evaluating media query: {query_str}")
#     # Ví dụ: trả về True nếu query_str chứa 'min-width' và giá trị nhỏ hơn 800,
#     # bạn có thể thay đổi logic kiểm tra theo nhu cầu.
#     if "min-width" in query_str:
#         # Giả sử màn hình hiện tại có chiều rộng 1024px
#         current_width = 1024
#         # Tách giá trị số từ chuỗi, ví dụ: "(min-width: 800px)" -> 800
#         try:
#             value = int(query_str.split(":")[1].split("px")[0].strip())
#             return current_width >= value
#         except Exception:
#             return False
#     return False


def ___useResponsive(size: int, query: str, start: Optional[Any] = None, end: Optional[Any] = None) -> State:
    """
    Mô phỏng hook useResponsive trong React.
    
    Args:
        query (str): Kiểu query: 'up', 'down', 'between', hoặc các giá trị khác (được hiểu là 'only').
        start (Optional[Any]): Giá trị breakpoint bắt đầu.
        end (Optional[Any]): Giá trị breakpoint kết thúc (dùng cho query 'between').
    
    Returns:
        bool: Kết quả của media query.
    
    Ví dụ:
        use_responsive('up', 'md')
        use_responsive('between', 'md', 'lg')
    """

    theme = useTheme()
    
    media_up = useMediaQuery(theme.breakpoints.up(start)) if start is not None else False
    media_down = useMediaQuery(theme.breakpoints.down(start)) if start is not None else False
    media_between = useMediaQuery(theme.breakpoints.between(start, end)) if start is not None and end is not None else False
    media_only = useMediaQuery(theme.breakpoints.only(start)) if start is not None else False

    if query == 'up':
        return media_up
    elif query == 'down':
        return media_down
    elif query == 'between':
        return media_between
    else:
        return media_only


def useResponsive(query: str, start: Optional[Any] = None, end: Optional[Any] = None):
    """
    Mô phỏng hook useResponsive trong React dựa vào kích thước của mainWindow.
    
    Args:
        query (str): Kiểu query: 'up', 'down', 'between', hoặc các giá trị khác (được hiểu là 'only').
        start (Optional[Any]): Giá trị breakpoint bắt đầu (ví dụ: 'md', và theme.breakpoints.md là một số).
        end (Optional[Any]): Giá trị breakpoint kết thúc (dùng cho query 'between').
    
    Returns:
        State: Một state chứa kết quả boolean của media query.
    
    Ví dụ:
        useResponsive('up', 'md')
        useResponsive('between', 'md', 'lg')
    """
    state, setState = useState(False)
    main_window = QApplication.instance().mainWindow  # Giả sử mainWindow đã được gán cho instance của QApplication
    current_width = main_window.width()

    theme = useTheme()
    start_breakpoint = getattr(theme.breakpoints, start) if start else None
    end_breakpoint = getattr(theme.breakpoints, end) if end else None

    def compare(width: int) -> bool:
        if query == 'up':
            return start_breakpoint is not None and width >= start_breakpoint
        elif query == 'down':
            return start_breakpoint is not None and width <= start_breakpoint
        elif query == 'between':
            if start_breakpoint is not None and end_breakpoint is not None:
                return start_breakpoint <= width <= end_breakpoint
            else:
                return False
        else:  # Trường hợp 'only' hoặc giá trị khác
            return start_breakpoint is not None and width == start_breakpoint

    # Cập nhật state ban đầu dựa trên kích thước hiện tại
    setState(compare(current_width))

    # Định nghĩa callback xử lý sự thay đổi kích thước mainWindow
    def on_size_changed(new_size):
        new_width = new_size.width()
        setState(compare(new_width))

    # Kết nối signal sizeChanged của mainWindow để cập nhật state khi kích thước thay đổi
    main_window.sizeChanged.connect(on_size_changed)

    return state

# # Ví dụ sử dụng
# if __name__ == "__main__":
#     print("Responsive up 800:", use_responsive('up', 800))
#     print("Responsive down 800:", use_responsive('down', 800))
#     print("Responsive between 600 and 1200:", use_responsive('between', 600, 1200))
#     print("Responsive only 800:", use_responsive('only', 800))
