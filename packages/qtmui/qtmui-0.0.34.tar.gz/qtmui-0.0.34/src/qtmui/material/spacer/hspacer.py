import uuid
from PySide6.QtWidgets import QSpacerItem, QWidget, QHBoxLayout, QSizePolicy

class HSpacer(QWidget):
    def __init__(
            self, 
            width: int = None,
            expanding: QSizePolicy = None,
            hightLight: bool = False,
            ):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setObjectName(str(uuid.uuid4()))
        if hightLight:
            self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "background: yellow;")) # str multi line
            
        if width is not None:
            self.layout().addItem(QSpacerItem(width, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        else:
            self.layout().addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        if expanding:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
