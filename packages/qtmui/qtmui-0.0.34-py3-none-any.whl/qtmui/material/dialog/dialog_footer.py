from PySide6.QtWidgets import QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, QPushButton
from PySide6.QtCore import QCoreApplication

class DialogFooter(QFrame):
    """
    DialogFooter
    DialogFooter for dialog

    Args:
        align: "left" | "right"

    Returns:
        new instance of PySyde6.QtWidgets.QFrame
    """
    def __init__(
            self, 
            parent=None,
            align: str = "right"
        ):
        super().__init__(parent)
        self.setLayout(QHBoxLayout())
        self.btn_cancel = QPushButton(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.btn_cancel.clicked.connect(parent.hide_dialog)
        self.btn_ok = QPushButton(QCoreApplication.translate("MainWindow", u"Ok", None))
        self.btn_ok.clicked.connect(parent.accept)

        if align == "left":
            self.layout().addWidget(self.btn_cancel)
            self.layout().addWidget(self.btn_ok)
            self.layout().addItem(QSpacerItem(448, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        else:
            self.layout().addItem(QSpacerItem(448, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            self.layout().addWidget(self.btn_cancel)
            self.layout().addWidget(self.btn_ok)