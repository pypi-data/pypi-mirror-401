from PySide6.QtWidgets import QFrame, QHBoxLayout, QTableWidgetItem


class TableWidgetItem(QTableWidgetItem):
    def __init__(
                self,
                selected: bool = False,
                text: str = ""
                ):
        super().__init__()
        self.setText(text)
