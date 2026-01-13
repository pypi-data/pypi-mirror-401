from PySide6.QtCore import QObject


class QtMuiTranslator(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def tr(self, text):
        return lambda: text

class Translator(QtMuiTranslator):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.app = self.tr('app')
        self.text = self.tr('text')
        self.view = self.tr('view')
        self.menus = self.tr('menus')
        self.icons = self.tr('icons')
        self.layout = self.tr('layout')
        self.dialogs = self.tr('dialogs')
        self.scroll = self.tr('scroll')
        self.material = self.tr('material')
        self.dateTime = self.tr('dateTime')
        self.navigation = self.tr('navigation')
        self.basicInput = self.tr('basicInput')
        self.statusInfo = self.tr('statusInfo')
        self.price = self.tr("price")
        self.titleSnackbar = self.tr("title")
        self.snackBarTitle = self.tr("snackBarTitle")
        self.snackBarContent = self.tr("snackBarContent")












































