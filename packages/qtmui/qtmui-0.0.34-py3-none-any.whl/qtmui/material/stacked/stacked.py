from typing import Optional, Union
from qtmui.hooks import State
from PySide6.QtWidgets import QStackedWidget, QStackedLayout, QWidget, QVBoxLayout

styles = '''   
    QFrame  {{
        border-radius: {};
        background-color:{};
    }}

    QFrame:hover  {{
    }}
'''

class Stacked(QStackedWidget):
    """
    Box
    Base container

    Args:
        stackingMode: QStackedLayout
        children: list[QWidget]

    Returns:
        new instance of PySyde6.QtWidgets.QStackedWidget
    """
    def __init__(self,  
                 id: str = None,
                 key: object = None,
                 index: Optional[Union[State, int]] = 0,
                 stackingMode: QStackedLayout = None,
                 children: list[QWidget] = None,
        ):
        super().__init__()
        
        self._index = index
        self._stackingMode = stackingMode
        self._children = children
        
        self._initUI()
        
    def _connectSignals(self):
        if isinstance(self._index, State):
            self._index.valueChanged.connect(self.setCurrentIndex)

    def _setDefaultIndex(self):
        if isinstance(self._index, State) and self._index.value is not None:
            self.setCurrentIndex(self._index.value)

    def _initUI(self):


        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        if isinstance(self._children, list) and len(self._children) > 0:
            for widget in self._children:
                self.addWidget(widget)
            self.setCurrentWidget(self._children[0])

        if self._stackingMode:
            self.layout().setStackingMode(self._stackingMode)

        self._setDefaultIndex()
        self._connectSignals()

    def show_child(self, type, name):
        for item in self.findChildren(type):
            if hasattr(item, "_name"):
                if item._name == name:
                    self.setCurrentWidget(item)
