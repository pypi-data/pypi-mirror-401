import sys
from PySide6.QtCore import QObject, Property, Signal

class TreeModel(QObject):
    dataChanged = Signal()

    def __init__(self, data=[]):
        super().__init__()
        self._data = data

    def get_data(self):
        return self._data

    def set_data(self, value):
        if self._data != value:
            self._data = value
            self.dataChanged.emit()

    data = Property(str, get_data, set_data, notify=dataChanged)
