from PySide6.QtWidgets import QFrame, QVBoxLayout, QApplication
from PySide6.QtCore import QSize

from ..alert.alert import Alert
from ..button import Button
from ..py_tool_button.py_tool_button import Iconify
from ..snackbar import Snackbar
from ..box import Box
from ..stack import QStack
from ..typography import Typography

class IconBox(QFrame):
    def __init__(self, context=None, path:str=None):
        super().__init__()

        self._context = context

        text = str(path.split("/")[-1].split('.')[0][:7] + '..').capitalize()

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(
            Box(
                children=[
                    Button(
                        # variant="text",
                        size="large",
                        variant="soft",
                        startIcon=Iconify(icon=path, size=QSize(32, 32), fillColor="#919EAB"),
                        # startIcon=Iconify(icon=path, pixmap=True,width=20, height=20, fillColor="#919EAB"),
                        onClick=lambda icon_p = path: self._copy_to_clipboard(icon_p),
                        tooltip=path
                    ),
                    Typography(text=f"{text} ", align="center", variant="caption", color="#919EAB")
                ]
            )
        )

    def _copy_to_clipboard(self, icon_p):
        # Tạo đối tượng clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(icon_p)
        self._create_snackbar(f"Đã sao chép vào clipboard: {icon_p}")

    def _create_snackbar(self, message):
        snackbar = Snackbar(
            self._context, 
            message=message, 
            duration=3000, 
            position="top", 
            spacing=6,
            child=Alert(
                text="Đã sao chép vào clipboard"
            ),
        )
        snackbar.showSnackbar(self._context, spacing=6)