from PySide6.QtWidgets import QVBoxLayout, QWidget

class Layout(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

    def add_widget(self, element: QWidget):
        """Thêm một phần tử giao diện vào trang."""
        if isinstance(element, QWidget):
            self.layout().addWidget(element)
        else:
            print(f"Opp!! element must have type QWidget")

