from PySide6.QtWidgets import (QMenu, QVBoxLayout)

class CustomMenu(QMenu):
    def __init__(
                self,
                parent = None,
                context = None,
                content: object = None,
                configs: object = None
                ):
        super().__init__(parent)
        self._context = context
        
        self._content = content
        self._configs = configs
        # self.setMinimumSize(400, 500)
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        if self._content:
            self.layout().addWidget(self._content)
        # else:
        #     for config in self._configs:
        #         self.layout().addWidget(Button(text=config.get("label"), variant="soft", text="inherit", fullWidth=True, onClick=config.get("label")))


