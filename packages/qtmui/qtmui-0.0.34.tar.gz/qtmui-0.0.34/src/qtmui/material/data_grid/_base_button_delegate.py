from PySide6.QtWidgets import QPushButton

class DelegateButton(QPushButton):
    def __init__(self, parent=None):
        super(DelegateButton, self).__init__(parent)

        # self.setLayout(QHBoxLayout())
        size = 50
        self.setFixedSize(size, size)
        self.setStyleSheet("""
            QPushButton{
                background-color: rgb(237, 237, 237);
                height: 30px;
                border: 0px solid transparent;
                border-radius: 4px;
                margin-left: 2px;
                color: #6b6b6b;
            }
            QPushButton:hover {
                background-color: rgb(227, 227, 227);
            }
            """)
