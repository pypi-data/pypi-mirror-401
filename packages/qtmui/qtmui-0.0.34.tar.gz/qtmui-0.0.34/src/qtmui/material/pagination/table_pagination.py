import uuid
from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal
from typing import Callable, Optional, Union
from qtmui.hooks import State
from qtmui.hooks import useEffect, useState

from ..stack import Stack
from ..typography import Typography
from ..button import IconButton
from ..select import Select
from ..py_iconify import Iconify
from ..textfield import TextField
from ..menu_item import MenuItem

from src.locales.translator import Translator
t = Translator()

# Định nghĩa lớp TablePagination kế thừa từ QWidget
class TablePagination(QFrame):
    # Định nghĩa tín hiệu để thông báo khi page hoặc rowsPerPage thay đổi
    pageChanged = Signal(int)  # Tín hiệu khi page thay đổi
    rowsPerPageChanged = Signal(int)  # Tín hiệu khi rowsPerPage thay đổi

    def __init__(
        self,
        count: State,  # Tổng số hàng (items)
        page: State,  # Trang hiện tại (bắt đầu từ 0)
        onPageChange: Callable[[int], None],  # Hàm callback khi page thay đổi
        rowsPerPage: State,  # Số hàng trên mỗi trang
        onRowsPerPageChange: Callable[[int], None],  # Hàm callback khi rowsPerPage thay đổi
        children: Optional[Union[list, QWidget]] = None,  # Widget cha, mặc định là None
        rowsPerPageOptions: Optional[Union[list, QWidget]] = None  # Widget cha, mặc định là None
    ) -> None:
        # Gọi hàm khởi tạo của lớp cha QWidget
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))

        # Lưu các thuộc tính vào instance
        self.count: State = count  # Tổng số hàng
        self.page: State = page  # Trang hiện tại
        self.rowsPerPage: State = rowsPerPage  # Số hàng trên mỗi trang
        self.onPageChange: Callable[[int], None] = onPageChange  # Callback khi page thay đổi
        self.onRowsPerPageChange: Callable[[int], None] = onRowsPerPageChange  # Callback khi rowsPerPage thay đổi

        def get_total_page():
            if isinstance(count, State):
                count_value = count.value
            else:
                count_value = count
            if isinstance(self.rowsPerPage, State):
                rowsPerPage_value = self.rowsPerPage.value
            else:
                rowsPerPage_value = self.rowsPerPage
            total_page = (count_value + int(rowsPerPage_value) - 1) // int(rowsPerPage_value) if int(rowsPerPage_value) > 0 else 1
            return total_page
        
        self.totalPages, self.setTotalPages = useState(get_total_page())

        # print('_____________99999999', type(self.count), type(self.rowsPerPage))
        useEffect(
            lambda: _update_ui(),
            [self.count, self.rowsPerPage]
        )

        # Tính tổng số trang

        # Thiết lập giao diện
        """Thiết lập giao diện cho TablePagination.
        Phương thức này không nhận tham số và không trả về giá trị."""
        # Tạo layout chính (ngang) cho TablePagination
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Đặt lề về 0
        layout.setSpacing(10)  # Đặt khoảng cách giữa các widget

        self.previous_enable, self.set_previous_enable = useState(self.page.value > 0)
        self.next_enable, self.set_next_enable = useState(self.page.value < self.totalPages.value - 1)


        def _handle_prev_page() -> None:
            """Xử lý sự kiện nhấn nút Previous.
            Phương thức này không nhận tham số và không trả về giá trị."""
            # Nếu không ở trang đầu, giảm page đi 1
            if self.page.value > 0:
                # Gửi tín hiệu pageChanged
                self.onPageChange(self.page.value - 1)
                # Cập nhật giao diện
            _update_ui()

        def _handle_next_page() -> None:
            """Xử lý sự kiện nhấn nút Next.
            Phương thức này không nhận tham số và không trả về giá trị."""
            # Nếu không ở trang cuối, tăng page lên 1
            print('_handel_next_page_________________', self.page.value, self.totalPages.value)
            if self.page.value < self.totalPages.value - 1:
                # Gửi tín hiệu pageChanged
                self.onPageChange(self.page.value + 1)
                # Cập nhật giao diện
            _update_ui()

        def _update_ui():
            """Cập nhật giao diện của TablePagination.
            Phương thức này không nhận tham số và không trả về giá trị."""
            self.setTotalPages(get_total_page())
            # Cập nhật nhãn hiển thị phạm vi hàng
            start = self.page.value * int(self.rowsPerPage.value) + 1
            end = min((self.page.value + 1) * int(self.rowsPerPage.value), self.count.value)
            set_range_label(f"{start}-{end} of {self.count.value}")
            # print("_update_ui_____________", self.count.value)

            # Cập nhật trạng thái nút Previous và Next
            self.set_previous_enable(self.page.value > 0)
            self.set_next_enable(self.page.value < self.totalPages.value - 1)


        # Nhãn hiển thị phạm vi hàng hiện tại
        start = self.page.value * int(self.rowsPerPage.value) + 1  # Hàng bắt đầu
        end = min((self.page.value + 1) * int(self.rowsPerPage.value), self.count.value)  # Hàng kết thúc
        range_label, set_range_label = useState(f"{start}-{end} of {self.count.value}")


        layout.addWidget(
            Stack(
                direction="row",
                alignItems="center",
                justifyContent="space-between",
                children=[
                    *(children if isinstance(children, list) else []),
                    *[
                        Stack(
                            direction="row",
                            alignItems="center",
                            justifyContent="flex-end",
                            spacing=1,
                            sx={"padding-right": 1},
                            children=[
                                # Typography(text=t.rowsPerPage),
                                Typography(text="row per page"),
                                TextField(
                                    key="iccccccccccccccccccccccc",
                                    select=True,
                                    size="small",
                                    hiddenLabel=True,
                                    value=self.rowsPerPage,
                                    # defaultValue=self.rowsPerPage.value,
                                    onChange=onRowsPerPageChange,
                                    selectOptions=[
                                        MenuItem(key=option, value=option, text=str(option))
                                        for option in rowsPerPageOptions or [5, 10, 25]
                                    ]
   
                                ),
                                Typography(text=range_label),
                                IconButton(
                                    size="small",
                                    enable=self.previous_enable,
                                    icon=Iconify(key="grommet-icons:form-previous"), 
                                    onClick=_handle_prev_page
                                ),
                                IconButton(
                                    enable=self.next_enable,
                                    size="small",
                                    icon=Iconify(key="grommet-icons:form-next"), 
                                    onClick=_handle_next_page
                                )
                            ]
                        )
                    ]
                ]
            )
        )


