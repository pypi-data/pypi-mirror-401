from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QSize

from .page import Page
    
class MainWindow(QMainWindow):

    def __init__(self, page: Page):
        super().__init__()
        self.setWindowTitle("Pyact")
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(QSize(1200, 900))

        self.page = page

        if isinstance(page, Page):
            self.setCentralWidget(page)
        else:
            raise TypeError("Opp!!. page must have the type QWidget")
        
        self.show()

    def closeEvent(self, event):
        print('close________')
        return super().closeEvent(event)


