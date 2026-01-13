from typing import Any, Callable, Dict, Optional, Union

from PySide6.QtWidgets import QFrame, QVBoxLayout

from qtmui.hooks import State
from ..textfield import TextField
from ..chip import Chip

class Select(QFrame):
    """
    A select component, styled like Material-UI Select.

    The `Select` component allows users to choose one or more options from a dropdown menu. It integrates
    with the `qtmui` framework, retaining existing parameters, adding new parameters, and aligning with
    MUI Select props. Inherits from OutlinedInput props.

    Parameters
    ----------

    disabled : State or bool, optional
        If True, disables the component. Default is False.
        Can be a `State` object for dynamic updates.

    **kwargs
        Additional keyword arguments passed to the parent `QWidget`,
        supporting props of OutlinedInput.

    Signals
    -------
    onOpen : Signal
        Emitted when the popup opens.
    onClose : Signal
        Emitted when the popup closes.
    changed : Signal
        Emitted when the value changes.
    setupUi : Signal
        Emitted when UI setup is complete.

    Notes
    -----
    - Existing parameters (53) are retained; 9 new parameters added to align with MUI.
    - Props of OutlinedInput are supported via `inputProps` and `**kwargs`.
    - MUI classes applied: `MuiSelect-root`, `Mui-disabled`.
    - Integrates with `TextField` for input rendering.

    Demos:
    - Select: https://qtmui.com/material-ui/qtmui-select/

    API Reference:
    - Select API: https://qtmui.com/material-ui/api/select/
    """
    def __init__(
        self,
        value: Optional[Union[State, Any]] = None,
        onChange: Optional[Union[State, Callable]] = None,
        # labelId: Optional[Union[State, str]] = None,
        # id: Optional[Union[State, str]] = None,
        label: Optional[Union[State, str]] = None,
        fullWidth: Optional[Union[State, bool]] = False,
        multiple: Optional[Union[State, bool]] = False,
        # native: Optional[Union[State, bool]] = False,
        # autoWidth: Optional[Union[State, bool]] = False,
        defaultValue: Optional[Union[State, object]] = None,
        displayEmpty: Optional[Union[State, bool]] = False,
        # input: Optional[Union[State, Any]] = None,
        inputProps: Optional[Union[State, Dict]] = None,
        renderValue: Optional[Union[State, Callable]] = None,
        # MenuProps: Optional[Union[State, Dict]] = None,
        getOptionLabel: Optional[Union[State, Callable]] = None, # mui react không có prop này, nhưng qtmui cần để render các option
        options: Optional[Union[State, object]] = None, # mui react không có prop này, nhưng qtmui cần để render các option
        open: Optional[Union[State, bool]] = False,
        onOpen: Optional[Union[State, Callable]] = None,
        onClose: Optional[Union[State, Callable]] = None,
        defaultOpen: Optional[Union[State, bool]] = False,
        disabled: Optional[Union[State, bool]] = False,
        error: Optional[Union[State, bool]] = False,
        renderOption: Optional[Union[State, Callable]] = None,
        required: Optional[Union[State, bool]] = False,
        readOnly: Optional[Union[State, bool]] = False,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        size: Optional[Union[State, str]] = "medium", # mui react không có prop này
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Lưu các prop
        self._value = value
        self._onChange = onChange
        # self._labelId = labelId
        # self._id = id
        self._label = label
        self._fullWidth = fullWidth
        self._multiple = multiple
        # self._native = native
        # self._autoWidth = autoWidth
        self._defaultValue = defaultValue
        self._displayEmpty = displayEmpty
        # self._input = input
        self._inputProps = inputProps or {}
        self._renderValue = renderValue
        # self._MenuProps = MenuProps or {}
        self._getOptionLabel = getOptionLabel # mui react không có prop này
        self._options = options or [] # mui react không có prop này
        self._open = open
        self._onOpen = onOpen
        self._onClose = onClose
        self._defaultOpen = defaultOpen
        self._disabled = disabled
        self._error = error
        self._renderOption = renderOption # mui react không có prop này
        self._required = required
        self._readOnly = readOnly
        self._sx = sx
        self._size = size  # mui react không có prop này
        
        self._renderTags = None
        
        if self._multiple:
            self._renderTags = lambda selected, getTagProps: (
                [
                    Chip(
                        **getTagProps(index),
                        key=self._getOptionLabel(option),
                        label=self._getOptionLabel(option),
                        size="small",
                        variant="soft",
                        # onDelete=lambda checked, title = option["title"]: self._on_delete_tag(title)
                    )
                    for index, option in selected.items()
                ]
            )

        self._init_ui()


    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        input_params = {
            "isSlectComponent": True,
            "select": True,
            "value": self._value,
            "onChange": self._onChange,
            # "labelId": self._labelId,
            # "id": self._id,
            "label": self._label,
            "fullWidth": self._fullWidth,
            "multiple": self._multiple,
            # "native": self._native,
            # "autoWidth": self._autoWidth,
            "defaultValue": self._defaultValue,
            # "displayEmpty": self._displayEmpty,
            # "input": self._input,
            "inputProps": self._inputProps,
            "renderValue": self._renderValue,
            # "MenuProps": self._MenuProps,
            "getOptionLabel": self._getOptionLabel,
            "options": self._options,
            "open": self._open,
            "onOpen": self._onOpen,
            "onClose": self._onClose,
            "defaultOpen": self._defaultOpen,
            "disabled": self._disabled,
            "error": self._error,
            "renderOption": self._renderOption,
            "required": self._required,
            "readOnly": self._readOnly,
            "sx": self._sx,
            "size": self._size,
            "renderTags": self._renderTags,
        }

        self._inputField = TextField(**input_params)
        self.layout().addWidget(self._inputField)



