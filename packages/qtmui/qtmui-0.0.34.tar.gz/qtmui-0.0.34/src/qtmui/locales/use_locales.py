import sys
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QMainWindow, QWidget
from PySide6.QtCore import QObject, Property, Signal, Slot


from src.i18n.use_translation import changeLanguage
from src.i18n.use_translation import changeLanguage as changeLanguageDevMode

from .config_lang import defaultLang, allLangs

changeLanguage(defaultLang)

def setCurrentLanguage(key: str):
    currentLang = allLangs.get(key)
    # print('currentLang_____________________________', currentLang)
    changeLanguage(currentLang)
    changeLanguageDevMode(currentLang)

# class useLocales(QObject):
#     langChanged = Signal()

#     def __init__(self, lang=None):
#         super().__init__()
#         if not lang:
#             self._lang = defaultLang
#         else:
#             self._lang = lang


#     def get_lang(self):
#         return self._lang

#     def set_lang(self, lang):
#         if self._lang != lang:
#             self._lang = lang
#             self.langChanged.emit()

#     def onChangeLang(self, lang):
#         if self._lang != lang:
#             self._lang = lang
#             self.langChanged.emit()

#     lang = Property(str, get_lang, onChangeLang, notify=langChanged)