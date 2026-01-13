import uuid

from PySide6.QtWidgets import QVBoxLayout, QFrame

from ..textfield import TextField


from qtmui.qss_name import *

class OutlinedInput(QFrame):
    def __init__(
            self,
            *args,
            **kwargs
            ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "background: red;")) # str multi line
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().addWidget(TextField(*args, **kwargs))
        self.setStyleSheet("background: red;") # str multi line


