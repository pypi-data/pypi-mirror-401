import uuid

from PySide6.QtWidgets import QStackedWidget, QStackedLayout, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Property, Slot
from ...material.hook_form.rhf_masonry_radio_group import RHFMasonryRadioGroup
from qtmui.material.styles import useTheme

styles = '''   
    QFrame  {{
        border-radius: {};
        background-color:{};
    }}

    QFrame:hover  {{
    }}
'''

class RHFStackedRadioGroup(QStackedWidget):
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
                 name: str,
                 stackingMode: QStackedLayout = None,
                 children: list[QWidget] = None,
        ):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        self._name = name
        self._value = None

        if isinstance(children, list) and len(children) > 0:
            for widget in children:
                self.addWidget(widget)

        if stackingMode:
            self.layout().setStackingMode(stackingMode)


        self.lbl_helper_text = QLabel(self)
        self.lbl_helper_text.setFixedHeight(14)
        self.lbl_helper_text.setStyleSheet('padding-left: 8px;')
        self.lbl_helper_text.setText("sssssssss")
        self.layout().addWidget(self.lbl_helper_text)

        # self.setup_ui()

    def show_child(self, type, id):
        for item in self.findChildren(type):
            if hasattr(item, "_id"):
                if item._id == id:
                    self.setCurrentWidget(item)

    def setup_ui(self):
        visible_count = 0
        for item in self.findChildren(RHFMasonryRadioGroup):
            item.valueChanged.connect(self.set_value)
            if item._value is None:
                pass
                # raise AttributeError("Must contain checked=True in one of the elements of the options property.")
            if item._isVisible:
                self.setCurrentWidget(item)
                self._value = item._value
                visible_count += 1
        if visible_count > 1:
            pass
            # raise AttributeError("At least one AutoComplete must have the isVisible attribute set to True.")

    def set_value(self, value):
        print('show_even  ===> set_value')
        self._value = value

    @Property(bool)
    def stateSignal(self):
        return self._stateSignal

    @stateSignal.setter
    def stateSignal(self, value):
        self._stateSignal = value
        self._stateSignal.connect(self.state)


    @Slot(object)
    def state(self, state):
        if self._name == state.get("field"):
            if state.get("error"):
                self.set_state({"status": "invalid", "message": state.get("error_message")})
                self.lbl_helper_text.setText(str(state.get("error_message")))
                self.lbl_helper_text.setStyleSheet(f'padding-left: 8px;color: {useTheme().palette.error.main};')