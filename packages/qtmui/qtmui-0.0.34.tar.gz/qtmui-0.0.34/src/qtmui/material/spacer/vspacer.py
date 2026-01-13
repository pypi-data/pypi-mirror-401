from PySide6.QtWidgets import QSpacerItem, QWidget, QVBoxLayout, QSizePolicy

class VSpacer(QWidget):
    def __init__(self, height: int = None):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        if height is not None:
            self.layout().addItem(QSpacerItem(0, height, QSizePolicy.Minimum, QSizePolicy.Fixed))
        else:
            self.layout().addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))