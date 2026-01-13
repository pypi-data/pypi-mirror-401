from typing import List, Dict, Optional, Union, Callable
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Property, Slot, Signal

from qtmui.hooks import useState
from qtmui.hooks import State, useEffect
from qtmui.material.styles import useTheme
from ..form_control_label import FormControlLabel
from ..controller import Controller
from ..typography import Typography
from ..box import Box
from ..checkbox import Checkbox
from ..utils.validate_params import _validate_param


class RHFCheckbox(QFrame):
    valueChanged = Signal(object)

    def __init__(
            self,
            name: str,
            value: object = None,
            checked: bool = False,
            label: str = None,
            error: bool = False,
            helperText: str = None,
            ):
        super().__init__()

        self._name = name
        self._value = value

        self._state, self._setState = useState(None)

        self._stateSignal = None

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        # self.setStyleSheet('background: red;')

        field = {
            "value": "checkbox value demooooooo"
        }

        control = False

        if checked:
            self._value = True
        else:
            self._value = False


        self.lbl_helper_text = QLabel(self)

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=Box(
                    children=[
                        FormControlLabel(
                            label=label, 
                            # hightLight=True,
                            checked=field.get("value"),
                            control=Checkbox(
                                checked=checked, onChange=self.set_value,
                            )
                        ),
                        self.lbl_helper_text
                    ]
                )

            )
        )

    def set_value(self, value):
        self._value = value
        print(f"Field width name {self._name} has value {self._value}")
        self.valueChanged.emit(self._value)

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



class RHFMultiCheckbox(QFrame):
    """
    A component that renders a group of checkboxes integrated with FormProvider, similar to Material-UI's RHFMultiCheckbox.

    Parameters
    ----------
    name : str
        The name of the field in the form.
    label : str, optional
        The label for the checkbox group.
    options : List[Dict[str, any]]
        List of options with 'label' and 'value' keys (e.g., [{'label': 'Option 1', 'value': '1'}, ...]).
    row : bool, optional
        If True, checkboxes are displayed horizontally. Default is False (vertical).
    spacing : int, optional
        Spacing between checkboxes in pixels. Default is 0.
    helperText : str, optional
        Helper text to display below the checkbox group.
    sx : Dict, optional
        Custom styles for the component.
    stateSignal : Signal, optional
        Signal to receive form state updates (e.g., errors) from FormProvider.
    """

    valueChanged = Signal(object)

    def __init__(
        self,
        name: str,
        label: Optional[Union[str, State, Callable]]=None,
        options: List[Dict[str, any]] = None,
        row: bool = False,
        spacing: int = 0,
        helperText: Optional[str] = None,
        sx: Optional[Dict] = None,
        *args, **kwargs
    ):
        super().__init__()
        self.setObjectName(f"RHFMultiCheckbox_{name}")

        self._name = name
        self._label = label
        self._options = options or []
        self._row = row
        self._spacing = spacing
        self._helperText = helperText
        self._sx = sx or {}
        self._value = []  # Danh sách giá trị đã chọn
        self._error = False
        self._error_message = None
        self._stateSignal = None

        self.theme = useTheme()
        self._init_ui()
        # self._set_stylesheet()

        # if self.stateSignal:
        #     self.stateSignal.connect(self._on_form_state_changed)


    def _init_ui(self):
        """Khởi tạo giao diện với nhãn, nhóm checkbox, và helper text."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        content_layout = QHBoxLayout() if self._row else QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignLeft) if self._row else content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(int(self._spacing))

        self.setLayout(layout)

        # Thêm nhãn nếu có
        if self._label:
            label_widget = Typography(text=self._label, sx={"color": "palette.text.secondary"})
            label_widget.setObjectName(f"{self.objectName()}_label")
            layout.addWidget(label_widget)

        # Thêm các checkbox
        for option in self._options:
            checkbox = Checkbox(
                value=option["value"],
                checked=option["value"] in self._value,
                onChange=self._on_checkbox_change
            )
            form_control_label = FormControlLabel(
                label=option["label"],
                control=checkbox
            )
            content_layout.addWidget(form_control_label)

        layout.addLayout(content_layout)

        # Thêm helper text hoặc error
        self.lbl_helper_text = QLabel(self._helperText or "")
        self.lbl_helper_text.setObjectName(f"{self.objectName()}_helper")
        layout.addWidget(self.lbl_helper_text)

    # def _set_stylesheet(self):
    #     """Áp dụng styles từ theme và sx."""
    #     try:
    #         component_styles = self.theme.components
    #         label_style = get_qss_style(component_styles.get("MuiFormLabel", {}).get("styles", {}).get("root", {}))
    #         helper_style = get_qss_style(component_styles.get("MuiFormHelperText", {}).get("styles", {}).get("root", {}))
    #         if self._error:
    #             helper_style += f"color: {self.theme.palette.error.main};"

    #         stylesheet = f"""
    #             #{self.objectName()}_label {{
    #                 {label_style}
    #                 font-size: 12px;
    #                 margin-bottom: {self._spacing}px;
    #             }}
    #             #{self.objectName()}_helper {{
    #                 {helper_style}
    #                 font-size: 12px;
    #                 margin-top: {self._spacing}px;
    #             }}
    #         """
    #         self.setStyleSheet(stylesheet)
    #     except Exception as e:
    #         print(f"Error setting stylesheet: {e}")

    def _on_checkbox_change(self, data):
        """Xử lý sự kiện thay đổi checkbox."""
        value, checked = data[0], data[1]
        if checked:
            if value not in self._value:
                self._value.append(value)
        else:
            if value in self._value:
                self._value.remove(value)
        self.valueChanged.emit(self._value)
        print(f"RHFMultiCheckbox '{self._name}' value changed: {self._value}")

    # def _on_form_state_changed(self, state: Dict):
    #     """Xử lý cập nhật trạng thái form từ FormProvider."""
    #     if state.get("field") == self._name:
    #         self._error = state.get("error", False)
    #         self._error_message = state.get("error_message", "")
    #         self._helper_label.setText(self._error_message or self._helperText or "")
    #         self._set_stylesheet()

    def set_value(self, value: List[any]):
        """Cập nhật giá trị từ FormProvider."""
        self._value = value or []
        for control in self.findChildren(Checkbox):
            control.setChecked(control._value in self._value)
        self.valueChanged.emit(self._value)
        self.update()

    def get_value(self):
        """Lấy giá trị hiện tại."""
        return self._value
    

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