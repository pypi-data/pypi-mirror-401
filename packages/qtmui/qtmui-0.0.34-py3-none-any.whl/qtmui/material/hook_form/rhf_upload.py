from typing import Callable, Optional

from PySide6.QtCore import Property, Slot, Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from ..controller import Controller
from ..box import Box
from ..form_helper_text import FormHelperText
from ..spacer import HSpacer
from ..upload import Upload, UploadBox, UploadAvatar
from qtmui.material.styles import useTheme

from qtmui.hooks import useState

from qtmui.qss_name import *


class RHFUploadAvatar(QWidget):
    valueChanged = Signal(object)

    def __init__(
            self,
            name: str,
            value: Optional[object]= None,
            multiple: bool = False,
            maxSize: Optional[bool] = False,
            onDrop: Optional[Callable] = None,
            onChange: Optional[Callable] = None,
            helperText: str = None,
            height: int = 250,
            ):
        super().__init__()
        self.setLayout(QHBoxLayout())
        # self.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)

        field = None
        control = False
        error = None
        # self._type = type
        self._name = name
        self._value = value
        self._onChange = onChange

        self._state, self._setState = useState(None)

        self.lbl_helper_text = QLabel(self)

        self._upload_avatar = UploadAvatar(
                                    value=value,
                                    onChange=self.handle_avatar_changed,
                                    file='field.value',
                                    error=not error
                                )

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=Box(
                    direction="column",
                    # fixedHeight=height,
                    # sx={"background-color": "red"},
                    children=[
                        Box(
                            # fixedHeight=height,
                            # absolute=True,
                            # # sx={"background-color": "red"},
                            # top=20,
                            # left=0,
                            children=[
                                Box(
                                    direction="column",
                                    children=[
                                        self._upload_avatar,
                                        helperText if isinstance(helperText, QWidget) else FormHelperText(error=error.message if error and hasattr(error, 'message') else helperText)
                                    ]
                                )
                            ]
                        ),
                    ]
                )
            )
        )

    def handle_avatar_changed(self, value):
        self._value = value
        # print(f"Field width name {self._name} has value {self._value}")
        self.valueChanged.emit(self._value)


    def set_value(self, value=None):
        self._value = value
        if self._onChange:
            self._onChange(value)

        self.valueChanged.emit(value)

        self._upload_avatar._set_value(value)
        
        self._setState(self._value)

    @Property(bool)
    def stateSignal(self):
        return self._stateSignal

    @stateSignal.setter
    def stateSignal(self, value):
        self._stateSignal = value
        self._stateSignal.connect(self.state)


    @Slot(object)
    def state(self, state):
        theme = useTheme()
        if self._name == state.get("field"):
            if state.get("error"):
                # self._complete._inputField._set_slot({"slot": "error", "message": state.get("error_message")})
                self.lbl_helper_text.setText(str(state.get("error_message")[0]))
                self.lbl_helper_text.setStyleSheet(f'''
                    padding-left: 8px;
                    font-size: {theme.typography.caption.fontSize};
                    font-weight: {theme.typography.caption.fontWeight};
                    color: {theme.palette.error.main};
                ''')
                if not self.lbl_helper_text.isVisible():
                    self.lbl_helper_text.show()
            else:
                # self._complete._inputField._set_slot({"slot": "valid"})
                self.lbl_helper_text.hide()

class RHFUploadBox(QWidget):
    valueChanged = Signal(object)

    def __init__(
            self,
            name: str,
            value: Optional[object]= None,
            multiple: bool = False,
            helperText: str = None,
            ):
        super().__init__()
        self.setLayout(QVBoxLayout())

        field = None
        control = False
        error = None
        # self._type = type
        self._name = name
        self._value = value

        self.lbl_helper_text = QLabel(self)

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=UploadBox(
                    files=field.value,
                    error=not error
                )
            )
        )

    def _on_change(self, value):
        if int(value) == 0:
            self._value = False
        else:
            self._value = True
        # print(f"Field width name {self._name} has value {self._value}")
        self.valueChanged.emit(self._value)


    @Property(bool)
    def stateSignal(self):
        return self._stateSignal

    @stateSignal.setter
    def stateSignal(self, value):
        self._stateSignal = value
        self._stateSignal.connect(self.state)


    @Slot(object)
    def state(self, state):
        theme = useTheme()
        if self._name == state.get("field"):
            if state.get("error"):
                # self._complete._inputField._set_slot({"slot": "error", "message": state.get("error_message")})
                self.lbl_helper_text.setText(str(state.get("error_message")[0]))
                self.lbl_helper_text.setStyleSheet(f'''
                    padding-left: 8px;
                    font-size: {theme.typography.caption.fontSize};
                    font-weight: {theme.typography.caption.fontWeight};
                    color: {theme.palette.error.main};
                ''')
                if not self.lbl_helper_text.isVisible():
                    self.lbl_helper_text.show()
            else:
                # self._complete._inputField._set_slot({"slot": "valid"})
                self.lbl_helper_text.hide()

class RHFUpload(QWidget):
    valueChanged = Signal(object)

    def __init__(
            self,
            name: str,
            value: Optional[object]= None,
            thumbnail: bool = False,
            multiple: bool = False,
            maxSize: int = None,
            onDrop: Callable = None,
            onDelete: Callable = None,
            onRemove: Callable = None,
            onRemoveAll: Callable = None,
            onUpload: Callable = None,
            helperText: str = None,
            ):
        super().__init__()
        self.setLayout(QVBoxLayout())

        field = {
            "value": []
        }
        control = False
        error = None
        # self._type = type
        self._name = name
        self._value = value

        self.lbl_helper_text = QLabel(self)

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=Upload(
                    multiple=True,
                    accept={ 'image/*': [] },
                    files=field.get('value'),
                    error=not error,
                    helperText=error.get("message") if error and hasattr(error, 'message') else helperText
                )
            )
        )

    def _on_change(self, value):
        if int(value) == 0:
            self._value = False
        else:
            self._value = True
        print(f"Field width name {self._name} has value {self._value}")
        self.valueChanged.emit(self._value)


    @Property(bool)
    def stateSignal(self):
        return self._stateSignal

    @stateSignal.setter
    def stateSignal(self, value):
        self._stateSignal = value
        self._stateSignal.connect(self.state)


    @Slot(object)
    def state(self, state):
        theme = useTheme()
        if self._name == state.get("field"):
            if state.get("error"):
                # self._complete._inputField._set_slot({"slot": "error", "message": state.get("error_message")})
                self.lbl_helper_text.setText(str(state.get("error_message")[0]))
                self.lbl_helper_text.setStyleSheet(f'''
                    padding-left: 8px;
                    font-size: {theme.typography.caption.fontSize};
                    font-weight: {theme.typography.caption.fontWeight};
                    color: {theme.palette.error.main};
                ''')
                if not self.lbl_helper_text.isVisible():
                    self.lbl_helper_text.show()
            else:
                # self._complete._inputField._set_slot({"slot": "valid"})
                self.lbl_helper_text.hide()