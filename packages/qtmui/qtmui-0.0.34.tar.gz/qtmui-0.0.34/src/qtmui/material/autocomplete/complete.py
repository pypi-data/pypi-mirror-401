import threading
import time
from typing import Optional, Union, Dict, List, Callable, Any
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from PySide6.QtCore import Signal, QTimer
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..system.color_manipulator import alpha
from qtmui.hooks import State
from ..textfield import TextField
from ..utils.validate_params import _validate_param

class Autocomplete(QFrame):
    """
    A component that provides autocompletion functionality with a dropdown list of options.

    The `Autocomplete` component allows users to select one or multiple options from a list,
    with support for free input, custom rendering, and advanced filtering. It is built on top
    of `QWidget` and supports all props of the Material-UI `Autocomplete` component, including
    native component props via `**kwargs`.

    Parameters
    ----------
    options : State or list, optional
        A list of options that will be shown in the Autocomplete. Default is [].
        Can be a `State` object for dynamic updates.
    renderInput : State or Callable, optional
        Render the input component. Signature: function(params: dict) => QWidget.
        Default is None. Can be a `State` object for dynamic updates.
    autoComplete : State or bool, optional
        If True, the completion string appears inline after the input cursor.
        Default is False. Can be a `State` object for dynamic updates.
    autoHighlight : State or bool, optional
        If True, the first option is automatically highlighted. Default is False.
        Can be a `State` object for dynamic updates.
    autoSelect : State or bool, optional
        If True, the selected option becomes the input value on blur. Default is False.
        Can be a `State` object for dynamic updates.
    blurOnSelect : State, str, or bool, optional
        Controls if the input is blurred on selection. Valid values: "mouse", "touch",
        True, False. Default is False. Can be a `State` object for dynamic updates.
    ChipProps : State or dict, optional
        Props applied to the Chip element. Deprecated: Use `slotProps.chip` instead.
        Default is None. Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    clearIcon : State or QWidget, optional
        The icon to display for clearing the input. Default is None.
        Can be a `State` object for dynamic updates.
    clearOnBlur : State or bool, optional
        If True, the input's text is cleared on blur if no value is selected.
        Default is False. Can be a `State` object for dynamic updates.
    clearOnEscape : State or bool, optional
        If True, clears all values when the user presses Escape. Default is False.
        Can be a `State` object for dynamic updates.
    clearText : State or str, optional
        Text for the clear icon button. Default is "Clear".
        Can be a `State` object for dynamic updates.
    closeText : State or str, optional
        Text for the close popup icon button. Default is "Close".
        Can be a `State` object for dynamic updates.
    componentsProps : State or dict, optional
        Props for internal slots. Deprecated: Use `slotProps` instead. Default is None.
        Can be a `State` object for dynamic updates.
    defaultValue : State or Any, optional
        The default value. Default is None (or [] for multiple). Can be a `State` object.
    disableClearable : State or bool, optional
        If True, the input cannot be cleared. Default is False.
        Can be a `State` object for dynamic updates.
    disableCloseOnSelect : State or bool, optional
        If True, the popup stays open after selection. Default is False.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the component is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disabledItemsFocusable : State or bool, optional
        If True, disabled items can be focused. Default is False.
        Can be a `State` object for dynamic updates.
    disableListWrap : State or bool, optional
        If True, the list box does not wrap focus. Default is False.
        Can be a `State` object for dynamic updates.
    disablePortal : State or bool, optional
        If True, the popup is rendered under the parent DOM hierarchy. Default is False.
        Can be a `State` object for dynamic updates.
    filterOptions : State or Callable, optional
        Function to filter options. Signature: function(options: List, state: dict) => List.
        Default is None. Can be a `State` object for dynamic updates.
    filterSelectedOptions : State or bool, optional
        If True, hides selected options from the list. Default is False.
        Can be a `State` object for dynamic updates.
    forcePopupIcon : State, str, or bool, optional
        Controls popup icon visibility. Valid values: "auto", True, False.
        Default is "auto". Can be a `State` object for dynamic updates.
    freeSolo : State or bool, optional
        If True, allows free input not bound to options. Default is False.
        Can be a `State` object for dynamic updates.
    fullWidth : State or bool, optional
        If True, the input takes the full width of its container. Default is False.
        Can be a `State` object for dynamic updates.
    getLimitTagsText : State or Callable, optional
        Function to display truncated tags label. Signature: function(more: int) => str.
        Default is None. Can be a `State` object for dynamic updates.
    getOptionDisabled : State or Callable, optional
        Function to determine if an option is disabled. Signature: function(option: Any) => bool.
        Default is None. Can be a `State` object for dynamic updates.
    getOptionKey : State or Callable, optional
        Function to get the key for an option. Signature: function(option: Any) => str | int.
        Default is None. Can be a `State` object for dynamic updates.
    getOptionLabel : State or Callable, optional
        Function to get the label for an option. Signature: function(option: Any) => str.
        Default is None. Can be a `State` object for dynamic updates.
    groupBy : State or Callable, optional
        Function to group options. Signature: function(option: Any) => str.
        Default is None. Can be a `State` object for dynamic updates.
    handleHomeEndKeys : State or bool, optional
        If True, handles Home/End keys when popup is open. Default is True.
        Can be a `State` object for dynamic updates.
    id : State or str, optional
        ID for the component. Default is None.
        Can be a `State` object for dynamic updates.
    includeInputInList : State or bool, optional
        If True, the input can be highlighted in the list. Default is False.
        Can be a `State` object for dynamic updates.
    inputValue : State or str, optional
        The input value. Default is None.
        Can be a `State` object for dynamic updates.
    isOptionEqualToValue : State or Callable, optional
        Function to compare option with value. Signature: function(option: Any, value: Any) => bool.
        Default is None. Can be a `State` object for dynamic updates.
    label : State or str, optional
        Label for the input. Default is None.
        Can be a `State` object for dynamic updates.
    limitTags : State or int, optional
        Maximum number of visible tags. Default is -1 (no limit).
        Can be a `State` object for dynamic updates.
    ListboxComponent : State or Any, optional
        Component for the listbox. Deprecated: Use `slots.listbox` instead.
        Default is None. Can be a `State` object for dynamic updates.
    ListboxProps : State or dict, optional
        Props for the Listbox. Deprecated: Use `slotProps.listbox` instead.
        Default is None. Can be a `State` object for dynamic updates.
    loading : State or bool, optional
        If True, shows a loading state. Default is False.
        Can be a `State` object for dynamic updates.
    loadingText : State or str, optional
        Text to display when loading. Default is "Loading...".
        Can be a `State` object for dynamic updates.
    multiple : State or bool, optional
        If True, allows multiple selections. Default is False.
        Can be a `State` object for dynamic updates.
    name : State or str, optional
        Name attribute for the input. Default is None.
        Can be a `State` object for dynamic updates.
    noOptionsText : State or str, optional
        Text to display when no options are available. Default is "No options".
        Can be a `State` object for dynamic updates.
    open : State or bool, optional
        If True, the popup is shown. Default is False.
        Can be a `State` object for dynamic updates.
    onChange : State or Callable, optional
        Callback fired when the value changes. Signature: function(event: Any, value: Any, reason: str, details: str) => None.
        Default is None. Can be a `State` object for dynamic updates.
    onClose : State or Callable, optional
        Callback fired when the popup closes. Signature: function(event: Any, reason: str) => None.
        Default is None. Can be a `State` object for dynamic updates.
    onHighlightChange : State or Callable, optional
        Callback fired when the highlighted option changes. Signature: function(event: Any, option: Any, reason: str) => None.
        Default is None. Can be a `State` object for dynamic updates.
    onInputChange : State or Callable, optional
        Callback fired when the input value changes. Signature: function(event: Any, value: str, reason: str) => None.
        Default is None. Can be a `State` object for dynamic updates.
    onOpen : State or Callable, optional
        Callback fired when the popup opens. Signature: function(event: Any) => None.
        Default is None. Can be a `State` object for dynamic updates.
    openOnFocus : State or bool, optional
        If True, the popup opens on input focus. Default is False.
        Can be a `State` object for dynamic updates.
    openText : State or str, optional
        Text for the open popup icon button. Default is "Open".
        Can be a `State` object for dynamic updates.
    PaperComponent : State or Any, optional
        Component for the popup body. Deprecated: Use `slots.paper` instead.
        Default is None. Can be a `State` object for dynamic updates.
    PopperComponent : State or Any, optional
        Component for positioning the popup. Deprecated: Use `slots.popper` instead.
        Default is None. Can be a `State` object for dynamic updates.
    popupIcon : State or QWidget, optional
        Icon for the popup. Default is None.
        Can be a `State` object for dynamic updates.
    readOnly : State or bool, optional
        If True, the component is read-only. Default is False.
        Can be a `State` object for dynamic updates.
    renderGroup : State or Callable, optional
        Function to render group headings. Signature: function(params: dict) => QWidget.
        Default is None. Can be a `State` object for dynamic updates.
    renderOption : State or Callable, optional
        Function to render each option. Signature: function(props: dict, option: Any, state: dict, ownerState: dict) => QWidget.
        Default is None. Can be a `State` object for dynamic updates.
    renderTags : State or Callable, optional
        Function to render selected tags. Deprecated: Use `renderValue` instead.
        Signature: function(value: List, getTagProps: Callable, ownerState: dict) => QWidget.
        Default is None. Can be a `State` object for dynamic updates.
    renderValue : State or Callable, optional
        Function to render selected value(s). Signature: function(value: Any, getItemProps: Callable, ownerState: dict) => QWidget.
        Default is None. Can be a `State` object for dynamic updates.
    selectOnFocus : State or bool, optional
        If True, selects the input text on focus. Default is True.
        Can be a `State` object for dynamic updates.
    selected : State or bool, optional
        If True, the input is visually selected. Default is False.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        Size of the component. Valid values: "small", "medium". Default is "medium".
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for each slot (e.g., chip, clearIndicator, listbox, paper, popper, popupIndicator).
        Default is None. Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for each slot (e.g., listbox, paper, popper). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    value : State or Any, optional
        The value of the Autocomplete. Default is None.
        Can be a `State` object for dynamic updates.
    treeView : State or bool, optional
        If True, enables tree view mode. Default is False.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QWidget` class, supporting
        native component props (e.g., style, className).

    Attributes
    ----------
    VALID_SIZES : list[str]
        Valid values for the `size` parameter: ["small", "medium"].
    VALID_FORCE_POPUP_ICONS : list[str | bool]
        Valid values for the `forcePopupIcon` parameter: ["auto", True, False].
    VALID_BLUR_ON_SELECT : list[str | bool]
        Valid values for the `blurOnSelect` parameter: ["mouse", "touch", True, False].

    Signals
    -------
    onOpen : Signal
        Emitted when the popup opens.
    onClose : Signal
        Emitted when the popup closes.
    onChange : Signal
        Emitted when the value changes.
    onInputChange : Signal
        Emitted when the input value changes.
    onHighlightChange : Signal
        Emitted when the highlighted option changes.
    setupUi : Signal
        Emitted when the UI setup is complete.

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - Deprecated props (`ChipProps`, `componentsProps`, `ListboxComponent`, `ListboxProps`,
      `PaperComponent`, `PopperComponent`, `renderTags`) should be replaced with
      `slotProps.<slot>` and `slots.<slot>`.

    Demos:
    - Autocomplete: https://qtmui.com/material-ui/qtmui-autocomplete/

    API Reference:
    - Autocomplete API: https://qtmui.com/material-ui/api/autocomplete/
    """

    VALID_SIZES = ["small", "medium"]
    VALID_FORCE_POPUP_ICONS = ["auto", True, False]
    VALID_BLUR_ON_SELECT = ["mouse", "touch", True, False]

    def __init__(
        self,
        key: Optional[str] = None,
        options: Optional[Union[State, List]] = None,
        renderInput: Optional[Union[State, Callable]] = None,
        autoComplete: Union[State, bool] = False,
        autoHighlight: Union[State, bool] = False,
        autoSelect: Union[State, bool] = False,
        blurOnSelect: Union[State, str, bool] = False,
        ChipProps: Optional[Union[State, Dict]] = None,
        classes: Optional[Union[State, Dict]] = None,
        clearIcon: Optional[Union[State, QWidget]] = None,
        clearOnBlur: Union[State, bool] = False,
        clearOnEscape: Union[State, bool] = False,
        clearText: Union[State, str] = "Clear",
        closeText: Union[State, str] = "Close",
        componentsProps: Optional[Union[State, Dict]] = None,
        defaultValue: Optional[Union[State, Any]] = None,
        disableClearable: Union[State, bool] = False,
        disableCloseOnSelect: Union[State, bool] = False,
        disabled: Union[State, bool] = False,
        disabledItemsFocusable: Union[State, bool] = False,
        disableListWrap: Union[State, bool] = False,
        disablePortal: Union[State, bool] = False,
        filterOptions: Optional[Union[State, Callable]] = None,
        filterSelectedOptions: Union[State, bool] = False,
        forcePopupIcon: Union[State, str, bool] = "auto",
        freeSolo: Union[State, bool] = False,
        fullWidth: Union[State, bool] = False,
        getLimitTagsText: Optional[Union[State, Callable]] = None,
        getOptionDisabled: Optional[Union[State, Callable]] = None,
        getOptionKey: Optional[Union[State, Callable]] = None,
        getOptionLabel: Optional[Union[State, Callable[[Any], str]]] = None,
        groupBy: Optional[Union[State, Callable[[Any], str]]] = None,
        handleHomeEndKeys: Union[State, bool] = True,
        id: Optional[Union[State, str]] = None,
        includeInputInList: Union[State, bool] = False,
        inputValue: Optional[Union[State, str]] = None,
        isOptionEqualToValue: Optional[Union[State, Callable]] = None,
        label: Optional[Union[str, State, Callable]] = None,
        limitTags: Union[State, int] = -1,
        ListboxComponent: Optional[Union[State, Any]] = None,
        ListboxProps: Optional[Union[State, Dict]] = None,
        loading: Union[State, bool] = False,
        loadingText: Union[State, str] = "Loading...",
        multiple: Union[State, bool] = False,
        name: Optional[Union[State, str]] = None,
        noOptionsText: Union[State, str] = "No options",
        open: Union[State, bool] = False,
        onChange: Optional[Union[State, Callable]] = None,
        onClose: Optional[Union[State, Callable]] = None,
        onHighlightChange: Optional[Union[State, Callable]] = None,
        onInputChange: Optional[Union[State, Callable]] = None,
        onOpen: Optional[Union[State, Callable[[Any], None]]] = None,
        openOnFocus: Union[State, bool] = False,
        openText: Union[State, str] = "Open",
        PaperComponent: Optional[Union[State, Any]] = None,
        PopperComponent: Optional[Union[State, Any]] = None,
        popupIcon: Optional[Union[State, QWidget]] = None,
        readOnly: Union[State, bool] = False,
        renderGroup: Optional[Union[State, Callable]] = None,
        renderOption: Optional[Union[State, Callable]] = None,
        renderTags: Optional[Union[State, Callable]] = None,
        renderValue: Optional[Union[State, Callable]] = None,
        selectOnFocus: Union[State, bool] = True,
        selected: Optional[Union[State, bool]] = False,
        size: Union[State, str] = "medium",
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        value: Optional[Union[State, Any]] = None,
        treeView: Union[State, bool] = False,
        **kwargs
    ):
        super().__init__()
        self._key = key
        self._name = name

        # Thiết lập các thuộc tính với dấu gạch dưới
        self._set_options(options or [])
        self._set_renderInput(renderInput)
        self._set_autoComplete(autoComplete)
        self._set_autoHighlight(autoHighlight)
        self._set_autoSelect(autoSelect)
        self._set_blurOnSelect(blurOnSelect)
        self._set_ChipProps(ChipProps)
        self._set_classes(classes)
        self._set_clearIcon(clearIcon)
        self._set_clearOnBlur(clearOnBlur)
        self._set_clearOnEscape(clearOnEscape)
        self._set_clearText(clearText)
        self._set_closeText(closeText)
        self._set_componentsProps(componentsProps)
        self._set_defaultValue(defaultValue)
        self._set_disableClearable(disableClearable)
        self._set_disableCloseOnSelect(disableCloseOnSelect)
        self._set_disabled(disabled)
        self._set_disabledItemsFocusable(disabledItemsFocusable)
        self._set_disableListWrap(disableListWrap)
        self._set_disablePortal(disablePortal)
        self._set_filterOptions(filterOptions)
        self._set_filterSelectedOptions(filterSelectedOptions)
        self._set_forcePopupIcon(forcePopupIcon)
        self._set_freeSolo(freeSolo)
        self._set_fullWidth(fullWidth)
        self._set_getLimitTagsText(getLimitTagsText)
        self._set_getOptionDisabled(getOptionDisabled)
        self._set_getOptionKey(getOptionKey)
        self._set_getOptionLabel(getOptionLabel)
        self._set_groupBy(groupBy)
        self._set_handleHomeEndKeys(handleHomeEndKeys)
        self._set_id(id)
        self._set_includeInputInList(includeInputInList)
        self._set_inputValue(inputValue)
        self._set_isOptionEqualToValue(isOptionEqualToValue)
        self._set_label(label)
        self._set_limitTags(limitTags)
        self._set_ListboxComponent(ListboxComponent)
        self._set_ListboxProps(ListboxProps)
        self._set_loading(loading)
        self._set_loadingText(loadingText)
        self._set_multiple(multiple)
        self._set_name(name)
        self._set_noOptionsText(noOptionsText)
        self._set_open(open)
        self._set_onChange(onChange)
        self._set_onClose(onClose)
        self._set_onHighlightChange(onHighlightChange)
        self._set_onInputChange(onInputChange)
        self._set_onOpen(onOpen)
        self._set_openOnFocus(openOnFocus)
        self._set_openText(openText)
        self._set_PaperComponent(PaperComponent)
        self._set_PopperComponent(PopperComponent)
        self._set_popupIcon(popupIcon)
        self._set_readOnly(readOnly)
        self._set_renderGroup(renderGroup)
        self._set_renderOption(renderOption)
        self._set_renderTags(renderTags)
        self._set_renderValue(renderValue)
        self._set_selectOnFocus(selectOnFocus)
        self._validate_selected(selected)
        self._set_size(size)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_sx(sx)
        self._set_value(value)
        self._set_treeView(treeView)

        self._state = self._get_value()
        if self._get_fullWidth():
            if not self._get_sx():
                self._set_sx({})
            self._get_sx().update({"width": "100%"})

        self._init_ui()


    # Setter và Getter cho tất cả các tham số
    @_validate_param(file_path="qtmui.material.autocomplete", param_name="options", supported_signatures=Union[State, List, type(None)])
    def _set_options(self, value):
        self._options = value

    def _get_options(self):
        return self._options.value if isinstance(self._options, State) else self._options

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="renderInput", supported_signatures=Union[State, Callable, type(None)])
    def _set_renderInput(self, value):
        self._renderInput = value

    def _get_renderInput(self):
        return self._renderInput.value if isinstance(self._renderInput, State) else self._renderInput

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="autoComplete", supported_signatures=Union[State, bool])
    def _set_autoComplete(self, value):
        self._autoComplete = value

    def _get_autoComplete(self):
        return self._autoComplete.value if isinstance(self._autoComplete, State) else self._autoComplete

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="autoHighlight", supported_signatures=Union[State, bool])
    def _set_autoHighlight(self, value):
        self._autoHighlight = value

    def _get_autoHighlight(self):
        return self._autoHighlight.value if isinstance(self._autoHighlight, State) else self._autoHighlight

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="autoSelect", supported_signatures=Union[State, bool])
    def _set_autoSelect(self, value):
        self._autoSelect = value

    def _get_autoSelect(self):
        return self._autoSelect.value if isinstance(self._autoSelect, State) else self._autoSelect

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="blurOnSelect", supported_signatures=Union[State, str, bool], valid_values=VALID_BLUR_ON_SELECT)
    def _set_blurOnSelect(self, value):
        self._blurOnSelect = value

    def _get_blurOnSelect(self):
        return self._blurOnSelect.value if isinstance(self._blurOnSelect, State) else self._blurOnSelect

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="ChipProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_ChipProps(self, value):
        self._ChipProps = value

    def _get_ChipProps(self):
        return self._ChipProps.value if isinstance(self._ChipProps, State) else self._ChipProps

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="clearIcon", supported_signatures=Union[State, QWidget, type(None)])
    def _set_clearIcon(self, value):
        self._clearIcon = value

    def _get_clearIcon(self):
        return self._clearIcon.value if isinstance(self._clearIcon, State) else self._clearIcon

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="clearOnBlur", supported_signatures=Union[State, bool])
    def _set_clearOnBlur(self, value):
        self._clearOnBlur = value

    def _get_clearOnBlur(self):
        return self._clearOnBlur.value if isinstance(self._clearOnBlur, State) else self._clearOnBlur

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="clearOnEscape", supported_signatures=Union[State, bool])
    def _set_clearOnEscape(self, value):
        self._clearOnEscape = value

    def _get_clearOnEscape(self):
        return self._clearOnEscape.value if isinstance(self._clearOnEscape, State) else self._clearOnEscape

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="clearText", supported_signatures=Union[State, str])
    def _set_clearText(self, value):
        self._clearText = value

    def _get_clearText(self):
        return self._clearText.value if isinstance(self._clearText, State) else self._clearText

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="closeText", supported_signatures=Union[State, str])
    def _set_closeText(self, value):
        self._closeText = value

    def _get_closeText(self):
        return self._closeText.value if isinstance(self._closeText, State) else self._closeText

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="componentsProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_componentsProps(self, value):
        self._componentsProps = value

    def _get_componentsProps(self):
        return self._componentsProps.value if isinstance(self._componentsProps, State) else self._componentsProps

    # @_validate_param(file_path="qtmui.material.autocomplete", param_name="defaultValue", supported_signatures=Union[State, Any, type(None)])
    def _set_defaultValue(self, value):
        self._defaultValue = value

    def _get_defaultValue(self):
        return self._defaultValue.value if isinstance(self._defaultValue, State) else self._defaultValue

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="disableClearable", supported_signatures=Union[State, bool])
    def _set_disableClearable(self, value):
        self._disableClearable = value

    def _get_disableClearable(self):
        return self._disableClearable.value if isinstance(self._disableClearable, State) else self._disableClearable

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="disableCloseOnSelect", supported_signatures=Union[State, bool])
    def _set_disableCloseOnSelect(self, value):
        self._disableCloseOnSelect = value

    def _get_disableCloseOnSelect(self):
        return self._disableCloseOnSelect.value if isinstance(self._disableCloseOnSelect, State) else self._disableCloseOnSelect

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        self._disabled = value

    def _get_disabled(self):
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="disabledItemsFocusable", supported_signatures=Union[State, bool])
    def _set_disabledItemsFocusable(self, value):
        self._disabledItemsFocusable = value

    def _get_disabledItemsFocusable(self):
        return self._disabledItemsFocusable.value if isinstance(self._disabledItemsFocusable, State) else self._disabledItemsFocusable

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="disableListWrap", supported_signatures=Union[State, bool])
    def _set_disableListWrap(self, value):
        self._disableListWrap = value

    def _get_disableListWrap(self):
        return self._disableListWrap.value if isinstance(self._disableListWrap, State) else self._disableListWrap

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="disablePortal", supported_signatures=Union[State, bool])
    def _set_disablePortal(self, value):
        self._disablePortal = value

    def _get_disablePortal(self):
        return self._disablePortal.value if isinstance(self._disablePortal, State) else self._disablePortal

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="filterOptions", supported_signatures=Union[State, Callable, type(None)])
    def _set_filterOptions(self, value):
        self._filterOptions = value

    def _get_filterOptions(self):
        return self._filterOptions.value if isinstance(self._filterOptions, State) else self._filterOptions

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="filterSelectedOptions", supported_signatures=Union[State, bool])
    def _set_filterSelectedOptions(self, value):
        self._filterSelectedOptions = value

    def _get_filterSelectedOptions(self):
        return self._filterSelectedOptions.value if isinstance(self._filterSelectedOptions, State) else self._filterSelectedOptions

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="forcePopupIcon", supported_signatures=Union[State, str, bool], valid_values=VALID_FORCE_POPUP_ICONS)
    def _set_forcePopupIcon(self, value):
        self._forcePopupIcon = value

    def _get_forcePopupIcon(self):
        return self._forcePopupIcon.value if isinstance(self._forcePopupIcon, State) else self._forcePopupIcon

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="freeSolo", supported_signatures=Union[State, bool])
    def _set_freeSolo(self, value):
        self._freeSolo = value

    def _get_freeSolo(self):
        return self._freeSolo.value if isinstance(self._freeSolo, State) else self._freeSolo

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="fullWidth", supported_signatures=Union[State, bool])
    def _set_fullWidth(self, value):
        self._fullWidth = value

    def _get_fullWidth(self):
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="getLimitTagsText", supported_signatures=Union[State, Callable, type(None)])
    def _set_getLimitTagsText(self, value):
        self._getLimitTagsText = value

    def _get_getLimitTagsText(self):
        return self._getLimitTagsText.value if isinstance(self._getLimitTagsText, State) else self._getLimitTagsText

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="getOptionDisabled", supported_signatures=Union[State, Callable, type(None)])
    def _set_getOptionDisabled(self, value):
        self._getOptionDisabled = value

    def _get_getOptionDisabled(self):
        return self._getOptionDisabled.value if isinstance(self._getOptionDisabled, State) else self._getOptionDisabled

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="getOptionKey", supported_signatures=Union[State, Callable, type(None)])
    def _set_getOptionKey(self, value):
        self._getOptionKey = value

    def _get_getOptionKey(self):
        return self._getOptionKey.value if isinstance(self._getOptionKey, State) else self._getOptionKey

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="getOptionLabel", supported_signatures=Union[State, Callable, type(None)])
    def _set_getOptionLabel(self, value):
        self._getOptionLabel = value

    def _get_getOptionLabel(self):
        return self._getOptionLabel.value if isinstance(self._getOptionLabel, State) else self._getOptionLabel

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="groupBy", supported_signatures=Union[State, Callable, type(None)])
    def _set_groupBy(self, value):
        self._groupBy = value

    def _get_groupBy(self):
        return self._groupBy.value if isinstance(self._groupBy, State) else self._groupBy

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="handleHomeEndKeys", supported_signatures=Union[State, bool])
    def _set_handleHomeEndKeys(self, value):
        self._handleHomeEndKeys = value

    def _get_handleHomeEndKeys(self):
        return self._handleHomeEndKeys.value if isinstance(self._handleHomeEndKeys, State) else self._handleHomeEndKeys

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="id", supported_signatures=Union[State, str, type(None)])
    def _set_id(self, value):
        self._id = value

    def _get_id(self):
        return self._id.value if isinstance(self._id, State) else self._id

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="includeInputInList", supported_signatures=Union[State, bool])
    def _set_includeInputInList(self, value):
        self._includeInputInList = value

    def _get_includeInputInList(self):
        return self._includeInputInList.value if isinstance(self._includeInputInList, State) else self._includeInputInList

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="inputValue", supported_signatures=Union[State, str, type(None)])
    def _set_inputValue(self, value):
        self._inputValue = value

    def _get_inputValue(self):
        return self._inputValue.value if isinstance(self._inputValue, State) else self._inputValue

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="isOptionEqualToValue", supported_signatures=Union[State, Callable, type(None)])
    def _set_isOptionEqualToValue(self, value):
        self._isOptionEqualToValue = value

    def _get_isOptionEqualToValue(self):
        return self._isOptionEqualToValue.value if isinstance(self._isOptionEqualToValue, State) else self._isOptionEqualToValue

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="label", supported_signatures=Union[State, str, type(None)])
    def _set_label(self, value):
        self._label = value

    def _get_label(self):
        return self._label.value if isinstance(self._label, State) else self._label

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="limitTags", supported_signatures=Union[State, int])
    def _set_limitTags(self, value):
        self._limitTags = value

    def _get_limitTags(self):
        return self._limitTags.value if isinstance(self._limitTags, State) else self._limitTags

    # @_validate_param(file_path="qtmui.material.autocomplete", param_name="ListboxComponent", supported_signatures=Union[State, Any, type(None)])
    def _set_ListboxComponent(self, value):
        self._ListboxComponent = value

    def _get_ListboxComponent(self):
        return self._ListboxComponent.value if isinstance(self._ListboxComponent, State) else self._ListboxComponent

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="ListboxProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_ListboxProps(self, value):
        self._ListboxProps = value

    def _get_ListboxProps(self):
        return self._ListboxProps.value if isinstance(self._ListboxProps, State) else self._ListboxProps

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="loading", supported_signatures=Union[State, bool])
    def _set_loading(self, value):
        self._loading = value

    def _get_loading(self):
        return self._loading.value if isinstance(self._loading, State) else self._loading

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="loadingText", supported_signatures=Union[State, str])
    def _set_loadingText(self, value):
        self._loadingText = value

    def _get_loadingText(self):
        return self._loadingText.value if isinstance(self._loadingText, State) else self._loadingText

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="multiple", supported_signatures=Union[State, bool])
    def _set_multiple(self, value):
        self._multiple = value

    def _get_multiple(self):
        return self._multiple.value if isinstance(self._multiple, State) else self._multiple

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="name", supported_signatures=Union[State, str, type(None)])
    def _set_name(self, value):
        self._name = value

    def _get_name(self):
        return self._name.value if isinstance(self._name, State) else self._name

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="noOptionsText", supported_signatures=Union[State, str])
    def _set_noOptionsText(self, value):
        self._noOptionsText = value

    def _get_noOptionsText(self):
        return self._noOptionsText.value if isinstance(self._noOptionsText, State) else self._noOptionsText

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="open", supported_signatures=Union[State, bool])
    def _set_open(self, value):
        self._open = value

    def _get_open(self):
        return self._open.value if isinstance(self._open, State) else self._open

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="onChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onChange(self, value):
        self._onChange = value

    def _get_onChange(self):
        return self._onChange.value if isinstance(self._onChange, State) else self._onChange

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="onClose", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClose(self, value):
        self._onClose = value

    def _get_onClose(self):
        return self._onClose.value if isinstance(self._onClose, State) else self._onClose

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="onHighlightChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onHighlightChange(self, value):
        self._onHighlightChange = value

    def _get_onHighlightChange(self):
        return self._onHighlightChange.value if isinstance(self._onHighlightChange, State) else self._onHighlightChange

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="onInputChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onInputChange(self, value):
        self._onInputChange = value

    def _get_onInputChange(self):
        return self._onInputChange.value if isinstance(self._onInputChange, State) else self._onInputChange

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="onOpen", supported_signatures=Union[State, Callable, type(None)])
    def _set_onOpen(self, value):
        self._onOpen = value

    def _get_onOpen(self):
        return self._onOpen.value if isinstance(self._onOpen, State) else self._onOpen

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="openOnFocus", supported_signatures=Union[State, bool])
    def _set_openOnFocus(self, value):
        self._openOnFocus = value

    def _get_openOnFocus(self):
        return self._openOnFocus.value if isinstance(self._openOnFocus, State) else self._openOnFocus

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="openText", supported_signatures=Union[State, str])
    def _set_openText(self, value):
        self._openText = value

    def _get_openText(self):
        return self._openText.value if isinstance(self._openText, State) else self._openText

    # @_validate_param(file_path="qtmui.material.autocomplete", param_name="PaperComponent", supported_signatures=Union[State, Any, type(None)])
    def _set_PaperComponent(self, value):
        self._PaperComponent = value

    def _get_PaperComponent(self):
        return self._PaperComponent.value if isinstance(self._PaperComponent, State) else self._PaperComponent

    # @_validate_param(file_path="qtmui.material.autocomplete", param_name="PopperComponent", supported_signatures=Union[State, Any, type(None)])
    def _set_PopperComponent(self, value):
        self._PopperComponent = value

    def _get_PopperComponent(self):
        return self._PopperComponent.value if isinstance(self._PopperComponent, State) else self._PopperComponent

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="popupIcon", supported_signatures=Union[State, QWidget, type(None)])
    def _set_popupIcon(self, value):
        self._popupIcon = value

    def _get_popupIcon(self):
        return self._popupIcon.value if isinstance(self._popupIcon, State) else self._popupIcon

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="readOnly", supported_signatures=Union[State, bool])
    def _set_readOnly(self, value):
        self._readOnly = value

    def _get_readOnly(self):
        return self._readOnly.value if isinstance(self._readOnly, State) else self._readOnly

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="renderGroup", supported_signatures=Union[State, Callable, type(None)])
    def _set_renderGroup(self, value):
        self._renderGroup = value

    def _get_renderGroup(self):
        return self._renderGroup.value if isinstance(self._renderGroup, State) else self._renderGroup

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="renderOption", supported_signatures=Union[State, Callable, type(None)])
    def _set_renderOption(self, value):
        self._renderOption = value

    def _get_renderOption(self):
        return self._renderOption.value if isinstance(self._renderOption, State) else self._renderOption

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="renderTags", supported_signatures=Union[State, Callable, type(None)])
    def _set_renderTags(self, value):
        self._renderTags = value

    def _get_renderTags(self):
        return self._renderTags.value if isinstance(self._renderTags, State) else self._renderTags

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="renderValue", supported_signatures=Union[State, Callable, type(None)])
    def _set_renderValue(self, value):
        self._renderValue = value

    def _get_renderValue(self):
        return self._renderValue.value if isinstance(self._renderValue, State) else self._renderValue

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="selectOnFocus", supported_signatures=Union[State, bool])
    def _set_selectOnFocus(self, value):
        self._selectOnFocus = value

    def _get_selectOnFocus(self):
        return self._selectOnFocus.value if isinstance(self._selectOnFocus, State) else self._selectOnFocus

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="selected", supported_signatures=Union[State, bool, type(None)])
    def _validate_selected(self, value):
        self._selected = value

    def _get_selected(self):
        return self._selected.value if isinstance(self._selected, State) else self._selected

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="size", supported_signatures=Union[State, str], valid_values=VALID_SIZES)
    def _set_size(self, value):
        self._size = value

    def _get_size(self):
        return self._size.value if isinstance(self._size, State) else self._size

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    # @_validate_param(file_path="qtmui.material.autocomplete", param_name="value", supported_signatures=Union[State, Any, type(None)])
    def _set_value(self, value):
        self._value = value

    def _get_value(self):
        return self._value.value if isinstance(self._value, State) else self._value

    @_validate_param(file_path="qtmui.material.autocomplete", param_name="treeView", supported_signatures=Union[State, bool])
    def _set_treeView(self, value):
        self._treeView = value

    def _get_treeView(self):
        return self._treeView.value if isinstance(self._treeView, State) else self._treeView

    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        input_params = {
            # "label": self._label,
            "key": self._key,
            "select": True,
            "autoComplete": True,
            "disabled": self._disabled,
            "defaultValue": self._defaultValue,
            "fullWidth": self._fullWidth,
            "id": self._id,
            "inputValue": self._inputValue,
            "options": self._options,
            "onChange": self._onChange,
            "onInputChange": self._onInputChange,
            "treeView": self._treeView,
            "multiple": self._multiple,
            "getOptionLabel": self._getOptionLabel,
            "renderOption": self._renderOption,
            "renderTags": self._renderTags,
            "size": self._size,
            "value": self._value,
            # **kwargs
        }
        self._inputField = self._renderInput(input_params)
        self.layout().addWidget(self._inputField)

        self.valueChanged = self._inputField.valueChanged

 
