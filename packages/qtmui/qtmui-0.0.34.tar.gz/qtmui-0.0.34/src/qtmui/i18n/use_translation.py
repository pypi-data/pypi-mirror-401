from PySide6.QtCore import QObject, Property, Signal

class Locales(QObject):
    langChanged = Signal()

    def __init__(self, lang=None):
        super().__init__()
        self._lang = lang

    def getLang(self) -> dict:
        return self._lang

    def setLang(self, value):
        if self._lang != value:
            self._lang = value
            self.langChanged.emit()

    lang = Property(str, getLang, setLang, notify=langChanged)

i18n = Locales()

def changeLanguage(data: dict):
    i18n.lang = data
    

def translate(t):
    if isinstance(t, str):
        return t
    # print('tttttttttt_________________________', t())
    # print('translate_________________________', i18n.getLang())
    return i18n.getLang().get(t())