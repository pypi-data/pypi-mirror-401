import asyncio
from typing import Any, Callable, Optional, Union
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal, Slot, Property, QTimer

from qtmui.hooks import useEffect
from qtmui.hooks import State

from ..button import Button, LoadingButton
from .rhf_submit import SubmitButton
from .rhf_text_field import RHFTextField
from .rhf_autocomplete import RHFAutocomplete
from .rhf_select import RHFSelect
from .rhf_radio_group import RHFRadioGroup
from .rhf_switch import RHFSwitch
from .rhf_rating import RHFRating
from .rhf_checkbox import RHFCheckbox, RHFMultiCheckbox
from .rhf_slider import RHFSlider
from .rhf_upload import RHFUploadAvatar

from .types import ResolverType, UseFormType



class FormProvider(QFrame):
    formState = Signal(dict)
    submitSignal = Signal(object)

    def __init__(
            self, 
            onSubmit: Callable = None, 
            initForm: Optional[State] = None, 
            schema: object = None, 
            children: object = None, 
            methods: UseFormType = None
        ):
        super().__init__()
        self.validator = methods.resolver
        self.methods: UseFormType = methods
        
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.data = {}
        self.none_value = {}
        self.schema = schema
        self.submitCount = 0
        self.submitSignal.connect(onSubmit)
        
        self.initForm = initForm # dành cho các form lớn
        
        self.isReseting = False
        
        if isinstance(children, list):
            for item in children:
                if item is not None:
                    self.layout().addWidget(item)
                    
        if isinstance(initForm, State):
            initForm.valueChanged.connect(self._setup_form)
        else:
            self._setup_form()

        self.methods.state.valueChanged.connect(self.set_form_data)
        
        useEffect(
            self._reset,
            [self.methods.isReset]
        )
        
        self.destroyed.connect(self._onDestroy)

    def _setup_form(self):
        if isinstance(self.initForm, State) and self.initForm.value:
            QTimer.singleShot(0, self._schedule_setup_form)
            QTimer.singleShot(0, self._schedule_set_form_data)
        else:
            QTimer.singleShot(0, self._schedule_setup_form)
            QTimer.singleShot(0, self._schedule_set_form_data)

    def _onDestroy(self, obj=None):
        # Cancel task nếu đang chạy
        self.methods.state.valueChanged.disconnect(self.set_form_data)
        if self._setup_form_task and not self._setup_form_task.done():
            self._setup_form_task.cancel( )
        if self._set_form_data_task and not self._set_form_data_task.done():
            self._set_form_data_task.cancel()
            
    def _schedule_setup_form(self):
        self._setup_form_task = asyncio.ensure_future(self.setup_form())
        
    def _schedule_set_form_data(self):
        self._set_form_data_task = asyncio.ensure_future(self.async_set_form_data(self.methods.state.value))
        
    def _reset(self):
        self.isReseting = True
        if self.methods.isReset.value:
            self.methods.setIsReset(False)
            QTimer.singleShot(0, lambda: asyncio.ensure_future(self.async_set_form_data(self.methods.state.value, reseting=True)))
        self.submitCount = 0
        
    async def setup_form(self):
    # def setup_form(self):
        rhf_fields = []
        for control in self.findChildren(QWidget):
            if type(control) == RHFTextField:
                control.valueChanged.connect(lambda value=control._value, name=control._name: self.on_value_changed(name, value))
                control.stateSignal = self.formState
            elif type(control) == RHFAutocomplete:
                control.valueChanged.connect(lambda value=control._value, name=control._name: self.on_value_changed(name, value))
                control.stateSignal = self.formState
            elif type(control) == RHFSelect:
                control.valueChanged.connect(lambda value=control._value, name=control._name: self.on_value_changed(name, value))
                control.stateSignal = self.formState
            elif type(control) == RHFSwitch:
                control.valueChanged.connect(lambda value=control._value, name=control._name: self.on_value_changed(name, value))
                control.stateSignal = self.formState
            elif type(control) == RHFRating:
                control.valueChanged.connect(lambda value=control._value, name=control._name: self.on_value_changed(name, value))
                control.stateSignal = self.formState
            elif type(control) == RHFCheckbox:
                control.valueChanged.connect(lambda value=control._value, name=control._name: self.on_value_changed(name, value))
                control.stateSignal = self.formState
            elif type(control) == RHFMultiCheckbox:
                control.valueChanged.connect(lambda value=control._value, name=control._name: self.on_value_changed(name, value))
                control.stateSignal = self.formState
            elif type(control) == RHFRadioGroup:
                control.valueChanged.connect(lambda value=control._value, name=control._name: self.on_value_changed(name, value))
                control.stateSignal = self.formState
            elif type(control) == RHFSlider:
                control.valueChanged.connect(lambda value=control._value, name=control._name: self.on_value_changed(name, value))
                control.stateSignal = self.formState
            elif isinstance(control, Button) or isinstance(control, SubmitButton):
                if control._type == "submit":
                    # print('submitiiiiiiiiiiiiiiiii')
                    control.clicked.connect(self._on_submit)
            
            if type(control) in [
                RHFTextField, 
                RHFSelect, 
                RHFAutocomplete, 
                RHFUploadAvatar,
                RHFCheckbox,
                RHFSwitch,
                RHFRating,
                RHFMultiCheckbox,
                RHFRadioGroup,
                RHFSlider,
                ]:
                rhf_fields.append(control)
        self.methods.setFields(rhf_fields)

    def _set_control_value(self, control, value):
        control.set_value(value=value)

    def set_form_data(self, data: Optional[Union[dict, Any]], reseting=False):
        
        for control in self.findChildren(QWidget):
            if type(control) in [
                RHFTextField, 
                RHFSelect, 
                RHFAutocomplete, 
                RHFUploadAvatar,
                RHFCheckbox,
                RHFSwitch,
                RHFRating,
                RHFMultiCheckbox,
                RHFRadioGroup,
                RHFSlider,
                ]:
                if hasattr(control, "_name"):
                    value = data.get(control._name)
                    # print(f"Setting value for control '{control._name}': {value}")
                if value is not None:
                    self._set_control_value(control, value)

        if reseting:
            self.isReseting = False
            
    async def async_set_form_data(self, data: Optional[Union[dict, Any]], reseting=False):
        
        for control in self.findChildren(QWidget):
            if type(control) in [
                RHFTextField, 
                RHFSelect, 
                RHFAutocomplete, 
                RHFUploadAvatar,
                RHFCheckbox,
                RHFSwitch,
                RHFRating,
                RHFMultiCheckbox,
                RHFRadioGroup,
                RHFSlider,
                ]:
                if hasattr(control, "_name"):
                    value = data.get(control._name)
                    # print(f"Setting value for control '{control._name}': {value}")
                if value is not None:
                    self._set_control_value(control, value)

        if reseting:
            self.isReseting = False

    def _on_reset(self):
        self.submitCount = 0

    def _on_submit(self):
        print('_on_submit')
        self.submitCount += 1
        if self.validate():
            self.submitSignal.emit(self.data)

    def get_form_data(self):
        for control in self.findChildren(QWidget):
            if str(type(control)).find('RHF') != -1:
                if control._value is not None:
                    self.data[control._name] = control._value
                else: 
                    if self.data.get(control._name) is not None:
                        del self.data[control._name]
        self.methods.setData(self.data)

    def validate(self, field=None):

        if not self.submitCount:
            # self.get_form_data() # chỗ này làm nặng chương trình
            return False
        self.get_form_data()
        schema = self.validator[0]
        v = self.validator[1]()

        if v.validate(self.data):
            if field:
                self.formState.emit({"field": field, "error": False})
            # self.submitSignal.emit(self.data)
            return True
        else:
            valid_fields = set(schema.keys()) - set(v.errors.keys())
            print(v.errors)
            for field in list(valid_fields):
                self.formState.emit({"field": field, "error": False})

            for field, error in v.errors.items():
                self.formState.emit({"field": field, "error": True, "error_message": error})
            return False

    def on_value_changed(self, name, value):
        if value == Qt.CheckState.Checked:
            value = True
        elif value == Qt.CheckState.Unchecked:
            value = False

        if value is not None:
            self.data[name] = value
        else:
            self.none_value[name] = value
            
        # print(f"Control '{name}' has value: {value}")
        if not self.isReseting:
            self.validate(name)

    # @Slot(object)
    # def set_state(self, state):
    #     for control in self.findChildren(QWidget):
    #         if type(control) == RHFTextField:
    #             if control._name == state.get('field'):
    #                 control.set_error(error)

