# import threading
# import time
# from typing import Callable, Optional, Union, List, Dict, Any
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit
# from PySide6.QtCore import Signal, QTimer
# from qtmui.material.styles import useTheme
# from qtmui.material.styles.create_theme.theme_reducer import ThemeState
# from ..system.color_manipulator import alpha
# from qtmui.hooks import State
# from ..textfield import TextField
# from ..utils.validate_params import _validate_param

# class Select(QWidget):
#     """
#     A select component, styled like Material-UI Select.

#     The `Select` component allows users to choose one or more options from a dropdown menu. It integrates
#     with the `qtmui` framework, retaining existing parameters, adding new parameters, and aligning with
#     MUI Select props. Inherits from OutlinedInput props.

#     Parameters
#     ----------
#     options : State or List, optional
#         The option elements to populate the select with. Default is [].
#         Can be a `State` object for dynamic updates.
#     renderInput : State or Callable, optional
#         Function to render the input component. Default is None.
#         Can be a `State` object for dynamic updates.
#     autoComplete : State or bool, optional
#         If True, enables autocomplete. Default is False.
#         Can be a `State` object for dynamic updates.
#     autoHighlight : State or bool, optional
#         If True, automatically highlights the first option. Default is False.
#         Can be a `State` object for dynamic updates.
#     autoSelect : State or bool, optional
#         If True, auto-selects value when input loses focus. Default is False.
#         Can be a `State` object for dynamic updates.
#     blurOnSelect : State or bool, optional
#         If True, blurs input after selection. Default is False.
#         Can be a `State` object for dynamic updates.
#     ChipProps : State or Dict, optional
#         Properties for chip elements. Default is None.
#         Can be a `State` object for dynamic updates.
#     classes : State or Dict, optional
#         Override or extend the styles applied to the component. Default is None.
#         Can be a `State` object for dynamic updates.
#     clearIcon : State or QWidget, optional
#         Icon for clear action. Default is None.
#         Can be a `State` object for dynamic updates.
#     clearOnBlur : State or bool, optional
#         If True, clears input on blur. Default is False.
#         Can be a `State` object for dynamic updates.
#     clearOnEscape : State or bool, optional
#         If True, clears input on escape key. Default is False.
#         Can be a `State` object for dynamic updates.
#     clearText : State or str, optional
#         Text for clear button. Default is 'Clear'.
#         Can be a `State` object for dynamic updates.
#     closeText : State or str, optional
#         Text for close button. Default is 'Close'.
#         Can be a `State` object for dynamic updates.
#     children : State or List[QWidget], optional
#         MenuItem elements for the select. Default is None.
#         Can be a `State` object for dynamic updates.
#     componentsProps : State or Dict, optional
#         Props for sub-components. Default is None.
#         Can be a `State` object for dynamic updates.
#     defaultValue : State or Any, optional
#         The default value when not controlled. Default is None.
#         Can be a `State` object for dynamic updates.
#     disableClearable : State or bool, optional
#         If True, disables clear action. Default is False.
#         Can be a `State` object for dynamic updates.
#     disableCloseOnSelect : State or bool, optional
#         If True, keeps popup open after selection. Default is False.
#         Can be a `State` object for dynamic updates.
#     disabled : State or bool, optional
#         If True, disables the component. Default is False.
#         Can be a `State` object for dynamic updates.
#     disabledItemsFocusable : State or bool, optional
#         If True, allows focusing disabled items. Default is False.
#         Can be a `State` object for dynamic updates.
#     disableListWrap : State or bool, optional
#         If True, disables list wrapping. Default is False.
#         Can be a `State` object for dynamic updates.
#     disablePortal : State or bool, optional
#         If True, popup is rendered under parent hierarchy. Default is False.
#         Can be a `State` object for dynamic updates.
#     filterOptions : State or Callable, optional
#         Custom function to filter options. Default is None.
#         Can be a `State` object for dynamic updates.
#     filterSelectedOptions : State or bool, optional
#         If True, hides selected options. Default is False.
#         Can be a `State` object for dynamic updates.
#     forcePopupIcon : State or str, optional
#         Controls popup icon visibility ('auto', 'true', 'false'). Default is 'auto'.
#         Can be a `State` object for dynamic updates.
#     freeSolo : State or bool, optional
#         If True, allows free text input. Default is False.
#         Can be a `State` object for dynamic updates.
#     fullWidth : State or bool, optional
#         If True, input takes full width. Default is False.
#         Can be a `State` object for dynamic updates.
#     getLimitTagsText : State or Callable, optional
#         Label when tags are limited. Default is None.
#         Can be a `State` object for dynamic updates.
#     getOptionDisabled : State or Callable, optional
#         Function to disable options. Default is None.
#         Can be a `State` object for dynamic updates.
#     getOptionKey : State or Callable, optional
#         Function to get option key. Default is None.
#         Can be a `State` object for dynamic updates.
#     getOptionLabel : State or Callable, optional
#         Function to get option label. Default is None.
#         Can be a `State` object for dynamic updates.
#     groupBy : State or Callable, optional
#         Function to group options. Default is None.
#         Can be a `State` object for dynamic updates.
#     handleHomeEndKeys : State or bool, optional
#         If True, enables Home/End key navigation. Default is True.
#         Can be a `State` object for dynamic updates.
#     id : State or str, optional
#         ID for the component. Default is None.
#         Can be a `State` object for dynamic updates.
#     includeInputInList : State or bool, optional
#         If True, highlights input in list. Default is False.
#         Can be a `State` object for dynamic updates.
#     inputValue : State or str, optional
#         Current value of the input. Default is None.
#         Can be a `State` object for dynamic updates.
#     isOptionEqualToValue : State or Callable, optional
#         Function to check if option equals value. Default is None.
#         Can be a `State` object for dynamic updates.
#     label : State or str, optional
#         Label for the input. Default is None.
#         Can be a `State` object for dynamic updates.
#     limitTags : State or int, optional
#         Maximum number of tags. Default is -1.
#         Can be a `State` object for dynamic updates.
#     ListboxComponent : State or type, optional
#         Component for listbox. Default is None.
#         Can be a `State` object for dynamic updates.
#     ListboxProps : State or Dict, optional
#         Props for Listbox. Default is None.
#         Can be a `State` object for dynamic updates.
#     loading : State or bool, optional
#         If True, shows loading state. Default is False.
#         Can be a `State` object for dynamic updates.
#     loadingText : State or str, optional
#         Text shown when loading. Default is 'Loading...'.
#         Can be a `State` object for dynamic updates.
#     multiple : State or bool, optional
#         If True, allows multiple selections. Default is False.
#         Can be a `State` object for dynamic updates.
#     name : State or str, optional
#         Name attribute for input. Default is None.
#         Can be a `State` object for dynamic updates.
#     noOptionsText : State or str, optional
#         Text when no options are available. Default is 'No options'.
#         Can be a `State` object for dynamic updates.
#     open : State or bool, optional
#         If True, shows the component. Default is False.
#         Can be a `State` object for dynamic updates.
#     onChange : State or Callable, optional
#         Callback when a menu item is selected. Default is None.
#         Can be a `State` object for dynamic updates.
#         Signature: (event: Any, child: object) -> None
#     openOnFocus : State or bool, optional
#         If True, opens popup on focus. Default is False.
#         Can be a `State` object for dynamic updates.
#     openText : State or str, optional
#         Text for open icon. Default is 'Open'.
#         Can be a `State` object for dynamic updates.
#     PaperComponent : State or type, optional
#         Component for popup body. Default is None.
#         Can be a `State` object for dynamic updates.
#     PopperComponent : State or type, optional
#         Component for popup positioning. Default is None.
#         Can be a `State` object for dynamic updates.
#     popupIcon : State or QWidget, optional
#         Icon for popup. Default is None.
#         Can be a `State` object for dynamic updates.
#     readOnly : State or bool, optional
#         If True, component is read-only. Default is False.
#         Can be a `State` object for dynamic updates.
#     renderOption : State or Callable, optional
#         Function to render each option. Default is None.
#         Can be a `State` object for dynamic updates.
#     renderTags : State or Callable, optional
#         Function to render selected tags. Default is None.
#         Can be a `State` object for dynamic updates.
#     renderValue : State or Callable, optional
#         Function to render selected value. Default is None.
#         Can be a `State` object for dynamic updates.
#     selectOnFocus : State or bool, optional
#         If True, selects input on focus. Default is True.
#         Can be a `State` object for dynamic updates.
#     selected : State or bool, optional
#         If True, highlights the input. Default is False.
#         Can be a `State` object for dynamic updates.
#     size : State or str, optional
#         Size of the component ('small', 'medium', 'large'). Default is 'medium'.
#         Can be a `State` object for dynamic updates.
#     slotProps : State or Dict, optional
#         Props for slots. Default is None.
#         Can be a `State` object for dynamic updates.
#     slots : State or Dict, optional
#         Components for slots. Default is None.
#         Can be a `State` object for dynamic updates.
#     sx : State, list, dict, Callable, str, or None, optional
#         System prop for CSS overrides. Default is None.
#         Can be a `State` object for dynamic updates.
#     value : State or Any, optional
#         The input value. Default is None.
#         Can be a `State` object for dynamic updates.
#     treeView : State or bool, optional
#         If True, enables tree view mode. Default is False.
#         Can be a `State` object for dynamic updates.
#     autoWidth : State or bool, optional
#         If True, auto-adjusts popover width. Default is False.
#         Can be a `State` object for dynamic updates.
#     defaultOpen : State or bool, optional
#         If True, component is initially open. Default is False.
#         Can be a `State` object for dynamic updates.
#     displayEmpty : State or bool, optional
#         If True, displays value when no items selected. Default is False.
#         Can be a `State` object for dynamic updates.
#     IconComponent : State or QWidget, optional
#         Icon for the arrow. Default is None.
#         Can be a `State` object for dynamic updates.
#     input : State or QWidget, optional
#         Input component. Default is None (uses TextField).
#         Can be a `State` object for dynamic updates.
#     inputProps : State or Dict, optional
#         Attributes for input element. Default is None.
#         Can be a `State` object for dynamic updates.
#     labelId : State or str, optional
#         ID for additional label. Default is None.
#         Can be a `State` object for dynamic updates.
#     MenuProps : State or Dict, optional
#         Props for Menu element. Default is None.
#         Can be a `State` object for dynamic updates.
#     native : State or bool, optional
#         If True, uses native select element. Default is False.
#         Can be a `State` object for dynamic updates.
#     SelectDisplayProps : State or Dict, optional
#         Props for clickable div. Default is None.
#         Can be a `State` object for dynamic updates.
#     variant : State or str, optional
#         Variant of the input ('filled', 'outlined', 'standard'). Default is 'outlined'.
#         Can be a `State` object for dynamic updates.
#     **kwargs
#         Additional keyword arguments passed to the parent `QWidget`,
#         supporting props of OutlinedInput.

#     Signals
#     -------
#     onOpen : Signal
#         Emitted when the popup opens.
#     onClose : Signal
#         Emitted when the popup closes.
#     changed : Signal
#         Emitted when the value changes.
#     setupUi : Signal
#         Emitted when UI setup is complete.

#     Notes
#     -----
#     - Existing parameters (53) are retained; 9 new parameters added to align with MUI.
#     - Props of OutlinedInput are supported via `inputProps` and `**kwargs`.
#     - MUI classes applied: `MuiSelect-root`, `Mui-disabled`.
#     - Integrates with `TextField` for input rendering.

#     Demos:
#     - Select: https://qtmui.com/material-ui/qtmui-select/

#     API Reference:
#     - Select API: https://qtmui.com/material-ui/api/select/
#     """

#     onOpen = Signal()
#     onClose = Signal()
#     changed = Signal(object, object)
#     setupUi = Signal()

#     VALID_SIZES = ['small', 'medium', 'large']
#     VALID_VARIANTS = ['filled', 'outlined', 'standard']
#     VALID_FORCE_POPUP_ICON = ['auto', 'true', 'false']

#     def __init__(
#         self,
#         options: Optional[Union[State, List]] = [],
#         renderInput: Optional[Union[State, Callable]] = None,
#         autoComplete: Union[State, bool] = False,
#         autoHighlight: Union[State, bool] = False,
#         autoSelect: Union[State, bool] = False,
#         blurOnSelect: Union[State, bool] = False,
#         ChipProps: Optional[Union[State, Dict]] = None,
#         classes: Optional[Union[State, Dict]] = None,
#         clearIcon: Optional[Union[State, QWidget]] = None,
#         clearOnBlur: Union[State, bool] = False,
#         clearOnEscape: Union[State, bool] = False,
#         clearText: Union[State, str] = "Clear",
#         closeText: Union[State, str] = "Close",
#         children: Optional[Union[State, List[QWidget]]] = None,
#         componentsProps: Optional[Union[State, Dict]] = None,
#         defaultValue: Optional[Union[State, Any]] = None,
#         disableClearable: Union[State, bool] = False,
#         disableCloseOnSelect: Union[State, bool] = False,
#         disabled: Union[State, bool] = False,
#         disabledItemsFocusable: Union[State, bool] = False,
#         disableListWrap: Union[State, bool] = False,
#         disablePortal: Union[State, bool] = False,
#         filterOptions: Optional[Union[State, Callable]] = None,
#         filterSelectedOptions: Union[State, bool] = False,
#         forcePopupIcon: Union[State, str] = "auto",
#         freeSolo: Union[State, bool] = False,
#         fullWidth: Union[State, bool] = False,
#         getLimitTagsText: Optional[Union[State, Callable]] = None,
#         getOptionDisabled: Optional[Union[State, Callable]] = None,
#         getOptionKey: Optional[Union[State, Callable]] = None,
#         getOptionLabel: Optional[Union[State, Callable]] = None,
#         groupBy: Optional[Union[State, Callable]] = None,
#         handleHomeEndKeys: Union[State, bool] = True,
#         id: Optional[Union[State, str]] = None,
#         includeInputInList: Union[State, bool] = False,
#         inputValue: Optional[Union[State, str]] = None,
#         isOptionEqualToValue: Optional[Union[State, Callable]] = None,
#         label: Optional[Union[State, str]] = None,
#         limitTags: Union[State, int] = -1,
#         ListboxComponent: Optional[Union[State, type]] = None,
#         ListboxProps: Optional[Union[State, Dict]] = None,
#         loading: Union[State, bool] = False,
#         loadingText: Union[State, str] = "Loading...",
#         multiple: Union[State, bool] = False,
#         name: Optional[Union[State, str]] = None,
#         noOptionsText: Union[State, str] = "No options",
#         open: Union[State, bool] = False,
#         onChange: Optional[Union[State, Callable]] = None,
#         openOnFocus: Union[State, bool] = False,
#         openText: Union[State, str] = "Open",
#         PaperComponent: Optional[Union[State, type]] = None,
#         PopperComponent: Optional[Union[State, type]] = None,
#         popupIcon: Optional[Union[State, QWidget]] = None,
#         readOnly: Union[State, bool] = False,
#         renderOption: Optional[Union[State, Callable]] = None,
#         renderTags: Optional[Union[State, Callable]] = None,
#         renderValue: Optional[Union[State, Callable]] = None,
#         selectOnFocus: Union[State, bool] = True,
#         selected: Union[State, bool] = False,
#         size: Union[State, str] = "medium",
#         slotProps: Optional[Union[State, Dict]] = None,
#         slots: Optional[Union[State, Dict]] = None,
#         sx: Optional[Union[State, List, Dict, Callable, str]] = None,
#         value: Optional[Union[State, Any]] = None,
#         treeView: Union[State, bool] = False,
#         autoWidth: Union[State, bool] = False,
#         defaultOpen: Union[State, bool] = False,
#         displayEmpty: Union[State, bool] = False,
#         IconComponent: Optional[Union[State, QWidget]] = None,
#         input: Optional[Union[State, QWidget]] = None,
#         inputProps: Optional[Union[State, Dict]] = None,
#         labelId: Optional[Union[State, str]] = None,
#         MenuProps: Optional[Union[State, Dict]] = None,
#         native: Union[State, bool] = False,
#         SelectDisplayProps: Optional[Union[State, Dict]] = None,
#         variant: Union[State, str] = "outlined",
#         **kwargs
#     ):
#         super().__init__(**kwargs)
#         self.theme = useTheme()
#         self._widget_references = []

#         # Set properties with validation
#         self._set_options(options)
#         self._set_renderInput(renderInput)
#         self._set_autoComplete(autoComplete)
#         self._set_autoHighlight(autoHighlight)
#         self._set_autoSelect(autoSelect)
#         self._set_blurOnSelect(blurOnSelect)
#         self._set_ChipProps(ChipProps)
#         self._set_classes(classes)
#         self._set_clearIcon(clearIcon)
#         self._set_clearOnBlur(clearOnBlur)
#         self._set_clearOnEscape(clearOnEscape)
#         self._set_clearText(clearText)
#         self._set_closeText(closeText)
#         self._set_children(children)
#         self._set_componentsProps(componentsProps)
#         self._set_defaultValue(defaultValue)
#         self._set_disableClearable(disableClearable)
#         self._set_disableCloseOnSelect(disableCloseOnSelect)
#         self._set_disabled(disabled)
#         self._set_disabledItemsFocusable(disabledItemsFocusable)
#         self._set_disableListWrap(disableListWrap)
#         self._set_disablePortal(disablePortal)
#         self._set_filterOptions(filterOptions)
#         self._set_filterSelectedOptions(filterSelectedOptions)
#         self._set_forcePopupIcon(forcePopupIcon)
#         self._set_freeSolo(freeSolo)
#         self._set_fullWidth(fullWidth)
#         self._set_getLimitTagsText(getLimitTagsText)
#         self._set_getOptionDisabled(getOptionDisabled)
#         self._set_getOptionKey(getOptionKey)
#         self._set_getOptionLabel(getOptionLabel)
#         self._set_groupBy(groupBy)
#         self._set_handleHomeEndKeys(handleHomeEndKeys)
#         self._set_id(id)
#         self._set_includeInputInList(includeInputInList)
#         self._set_inputValue(inputValue)
#         self._set_isOptionEqualToValue(isOptionEqualToValue)
#         self._set_label(label)
#         self._set_limitTags(limitTags)
#         self._set_ListboxComponent(ListboxComponent)
#         self._set_ListboxProps(ListboxProps)
#         self._set_loading(loading)
#         self._set_loadingText(loadingText)
#         self._set_multiple(multiple)
#         self._set_name(name)
#         self._set_noOptionsText(noOptionsText)
#         self._set_open(open)
#         self._set_onChange(onChange)
#         self._set_openOnFocus(openOnFocus)
#         self._set_openText(openText)
#         self._set_PaperComponent(PaperComponent)
#         self._set_PopperComponent(PopperComponent)
#         self._set_popupIcon(popupIcon)
#         self._set_readOnly(readOnly)
#         self._set_renderOption(renderOption)
#         self._set_renderTags(renderTags)
#         self._set_renderValue(renderValue)
#         self._set_selectOnFocus(selectOnFocus)
#         self._set_selected(selected)
#         self._set_size(size)
#         self._set_slotProps(slotProps)
#         self._set_slots(slots)
#         self._set_sx(sx)
#         self._set_value(value)
#         self._set_treeView(treeView)
#         self._set_autoWidth(autoWidth)
#         self._set_defaultOpen(defaultOpen)
#         self._set_displayEmpty(displayEmpty)
#         self._set_IconComponent(IconComponent)
#         self._set_input(input)
#         self._set_inputProps(inputProps)
#         self._set_labelId(labelId)
#         self._set_MenuProps(MenuProps)
#         self._set_native(native)
#         self._set_SelectDisplayProps(SelectDisplayProps)
#         self._set_variant(variant)

#         self._state = self._value
#         self._init_ui()
#         self._set_stylesheet()

#         self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
#         self.destroyed.connect(self._on_destroyed)
#         self._connect_signals()

#     # Setter and Getter methods
#     @_validate_param(file_path="qtmui.material.select", param_name="options", supported_signatures=Union[State, List, type(None)])
#     def _set_options(self, value):
#         """Assign value to options."""
#         self._options = value

#     def _get_options(self):
#         """Get the options value."""
#         return self._options.value if isinstance(self._options, State) else self._options

#     @_validate_param(file_path="qtmui.material.select", param_name="renderInput", supported_signatures=Union[State, Callable, type(None)])
#     def _set_renderInput(self, value):
#         """Assign value to renderInput."""
#         self._renderInput = value

#     def _get_renderInput(self):
#         """Get the renderInput value."""
#         return self._renderInput.value if isinstance(self._renderInput, State) else self._renderInput

#     @_validate_param(file_path="qtmui.material.select", param_name="autoComplete", supported_signatures=Union[State, bool])
#     def _set_autoComplete(self, value):
#         """Assign value to autoComplete."""
#         self._autoComplete = value

#     def _get_autoComplete(self):
#         """Get the autoComplete value."""
#         return self._autoComplete.value if isinstance(self._autoComplete, State) else self._autoComplete

#     @_validate_param(file_path="qtmui.material.select", param_name="autoHighlight", supported_signatures=Union[State, bool])
#     def _set_autoHighlight(self, value):
#         """Assign value to autoHighlight."""
#         self._autoHighlight = value

#     def _get_autoHighlight(self):
#         """Get the autoHighlight value."""
#         return self._autoHighlight.value if isinstance(self._autoHighlight, State) else self._autoHighlight

#     @_validate_param(file_path="qtmui.material.select", param_name="autoSelect", supported_signatures=Union[State, bool])
#     def _set_autoSelect(self, value):
#         """Assign value to autoSelect."""
#         self._autoSelect = value

#     def _get_autoSelect(self):
#         """Get the autoSelect value."""
#         return self._autoSelect.value if isinstance(self._autoSelect, State) else self._autoSelect

#     @_validate_param(file_path="qtmui.material.select", param_name="blurOnSelect", supported_signatures=Union[State, bool])
#     def _set_blurOnSelect(self, value):
#         """Assign value to blurOnSelect."""
#         self._blurOnSelect = value

#     def _get_blurOnSelect(self):
#         """Get the blurOnSelect value."""
#         return self._blurOnSelect.value if isinstance(self._blurOnSelect, State) else self._blurOnSelect

#     @_validate_param(file_path="qtmui.material.select", param_name="ChipProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_ChipProps(self, value):
#         """Assign value to ChipProps."""
#         self._ChipProps = value

#     def _get_ChipProps(self):
#         """Get the ChipProps value."""
#         return self._ChipProps.value if isinstance(self._ChipProps, State) else self._ChipProps

#     @_validate_param(file_path="qtmui.material.select", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
#     def _set_classes(self, value):
#         """Assign value to classes."""
#         self._classes = value

#     def _get_classes(self):
#         """Get the classes value."""
#         return self._classes.value if isinstance(self._classes, State) else self._classes

#     @_validate_param(file_path="qtmui.material.select", param_name="clearIcon", supported_signatures=Union[State, QWidget, type(None)])
#     def _set_clearIcon(self, value):
#         """Assign value to clearIcon."""
#         self._clearIcon = value

#     def _get_clearIcon(self):
#         """Get the clearIcon value."""
#         return self._clearIcon.value if isinstance(self._clearIcon, State) else self._clearIcon

#     @_validate_param(file_path="qtmui.material.select", param_name="clearOnBlur", supported_signatures=Union[State, bool])
#     def _set_clearOnBlur(self, value):
#         """Assign value to clearOnBlur."""
#         self._clearOnBlur = value

#     def _get_clearOnBlur(self):
#         """Get the clearOnBlur value."""
#         return self._clearOnBlur.value if isinstance(self._clearOnBlur, State) else self._clearOnBlur

#     @_validate_param(file_path="qtmui.material.select", param_name="clearOnEscape", supported_signatures=Union[State, bool])
#     def _set_clearOnEscape(self, value):
#         """Assign value to clearOnEscape."""
#         self._clearOnEscape = value

#     def _get_clearOnEscape(self):
#         """Get the clearOnEscape value."""
#         return self._clearOnEscape.value if isinstance(self._clearOnEscape, State) else self._clearOnEscape

#     @_validate_param(file_path="qtmui.material.select", param_name="clearText", supported_signatures=Union[State, str])
#     def _set_clearText(self, value):
#         """Assign value to clearText."""
#         self._clearText = value

#     def _get_clearText(self):
#         """Get the clearText value."""
#         return self._clearText.value if isinstance(self._clearText, State) else self._clearText

#     @_validate_param(file_path="qtmui.material.select", param_name="closeText", supported_signatures=Union[State, str])
#     def _set_closeText(self, value):
#         """Assign value to closeText."""
#         self._closeText = value

#     def _get_closeText(self):
#         """Get the closeText value."""
#         return self._closeText.value if isinstance(self._closeText, State) else self._closeText

#     @_validate_param(file_path="qtmui.material.select", param_name="children", supported_signatures=Union[State, List[QWidget], type(None)])
#     def _set_children(self, value):
#         """Assign value to children."""
#         self._children = value
#         children = value.value if isinstance(value, State) else value
#         if isinstance(children, list):
#             for child in children:
#                 if not isinstance(child, QWidget):
#                     raise TypeError(f"Each element in children must be a QWidget, got {type(child)}")
#                 self._widget_references.append(child)

#     def _get_children(self):
#         """Get the children value."""
#         return self._children.value if isinstance(self._children, State) else self._children

#     @_validate_param(file_path="qtmui.material.select", param_name="componentsProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_componentsProps(self, value):
#         """Assign value to componentsProps."""
#         self._componentsProps = value

#     def _get_componentsProps(self):
#         """Get the componentsProps value."""
#         return self._componentsProps.value if isinstance(self._componentsProps, State) else self._componentsProps

#     @_validate_param(file_path="qtmui.material.select", param_name="defaultValue", supported_signatures=Union[State, Any, type(None)])
#     def _set_defaultValue(self, value):
#         """Assign value to defaultValue."""
#         self._defaultValue = value

#     def _get_defaultValue(self):
#         """Get the defaultValue value."""
#         return self._defaultValue.value if isinstance(self._defaultValue, State) else self._defaultValue

#     @_validate_param(file_path="qtmui.material.select", param_name="disableClearable", supported_signatures=Union[State, bool])
#     def _set_disableClearable(self, value):
#         """Assign value to disableClearable."""
#         self._disableClearable = value

#     def _get_disableClearable(self):
#         """Get the disableClearable value."""
#         return self._disableClearable.value if isinstance(self._disableClearable, State) else self._disableClearable

#     @_validate_param(file_path="qtmui.material.select", param_name="disableCloseOnSelect", supported_signatures=Union[State, bool])
#     def _set_disableCloseOnSelect(self, value):
#         """Assign value to disableCloseOnSelect."""
#         self._disableCloseOnSelect = value

#     def _get_disableCloseOnSelect(self):
#         """Get the disableCloseOnSelect value."""
#         return self._disableCloseOnSelect.value if isinstance(self._disableCloseOnSelect, State) else self._disableCloseOnSelect

#     @_validate_param(file_path="qtmui.material.select", param_name="disabled", supported_signatures=Union[State, bool])
#     def _set_disabled(self, value):
#         """Assign value to disabled."""
#         self._disabled = value

#     def _get_disabled(self):
#         """Get the disabled value."""
#         return self._disabled.value if isinstance(self._disabled, State) else self._disabled

#     @_validate_param(file_path="qtmui.material.select", param_name="disabledItemsFocusable", supported_signatures=Union[State, bool])
#     def _set_disabledItemsFocusable(self, value):
#         """Assign value to disabledItemsFocusable."""
#         self._disabledItemsFocusable = value

#     def _get_disabledItemsFocusable(self):
#         """Get the disabledItemsFocusable value."""
#         return self._disabledItemsFocusable.value if isinstance(self._disabledItemsFocusable, State) else self._disabledItemsFocusable

#     @_validate_param(file_path="qtmui.material.select", param_name="disableListWrap", supported_signatures=Union[State, bool])
#     def _set_disableListWrap(self, value):
#         """Assign value to disableListWrap."""
#         self._disableListWrap = value

#     def _get_disableListWrap(self):
#         """Get the disableListWrap value."""
#         return self._disableListWrap.value if isinstance(self._disableListWrap, State) else self._disableListWrap

#     @_validate_param(file_path="qtmui.material.select", param_name="disablePortal", supported_signatures=Union[State, bool])
#     def _set_disablePortal(self, value):
#         """Assign value to disablePortal."""
#         self._disablePortal = value

#     def _get_disablePortal(self):
#         """Get the disablePortal value."""
#         return self._disablePortal.value if isinstance(self._disablePortal, State) else self._disablePortal

#     @_validate_param(file_path="qtmui.material.select", param_name="filterOptions", supported_signatures=Union[State, Callable, type(None)])
#     def _set_filterOptions(self, value):
#         """Assign value to filterOptions."""
#         self._filterOptions = value

#     def _get_filterOptions(self):
#         """Get the filterOptions value."""
#         return self._filterOptions.value if isinstance(self._filterOptions, State) else self._filterOptions

#     @_validate_param(file_path="qtmui.material.select", param_name="filterSelectedOptions", supported_signatures=Union[State, bool])
#     def _set_filterSelectedOptions(self, value):
#         """Assign value to filterSelectedOptions."""
#         self._filterSelectedOptions = value

#     def _get_filterSelectedOptions(self):
#         """Get the filterSelectedOptions value."""
#         return self._filterSelectedOptions.value if isinstance(self._filterSelectedOptions, State) else self._filterSelectedOptions

#     @_validate_param(file_path="qtmui.material.select", param_name="forcePopupIcon", supported_signatures=Union[State, str], valid_values=VALID_FORCE_POPUP_ICON)
#     def _set_forcePopupIcon(self, value):
#         """Assign value to forcePopupIcon."""
#         self._forcePopupIcon = value

#     def _get_forcePopupIcon(self):
#         """Get the forcePopupIcon value."""
#         return self._forcePopupIcon.value if isinstance(self._forcePopupIcon, State) else self._forcePopupIcon

#     @_validate_param(file_path="qtmui.material.select", param_name="freeSolo", supported_signatures=Union[State, bool])
#     def _set_freeSolo(self, value):
#         """Assign value to freeSolo."""
#         self._freeSolo = value

#     def _get_freeSolo(self):
#         """Get the freeSolo value."""
#         return self._freeSolo.value if isinstance(self._freeSolo, State) else self._freeSolo

#     @_validate_param(file_path="qtmui.material.select", param_name="fullWidth", supported_signatures=Union[State, bool])
#     def _set_fullWidth(self, value):
#         """Assign value to fullWidth."""
#         self._fullWidth = value

#     def _get_fullWidth(self):
#         """Get the fullWidth value."""
#         return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

#     @_validate_param(file_path="qtmui.material.select", param_name="getLimitTagsText", supported_signatures=Union[State, Callable, type(None)])
#     def _set_getLimitTagsText(self, value):
#         """Assign value to getLimitTagsText."""
#         self._getLimitTagsText = value

#     def _get_getLimitTagsText(self):
#         """Get the getLimitTagsText value."""
#         return self._getLimitTagsText.value if isinstance(self._getLimitTagsText, State) else self._getLimitTagsText

#     @_validate_param(file_path="qtmui.material.select", param_name="getOptionDisabled", supported_signatures=Union[State, Callable, type(None)])
#     def _set_getOptionDisabled(self, value):
#         """Assign value to getOptionDisabled."""
#         self._getOptionDisabled = value

#     def _get_getOptionDisabled(self):
#         """Get the getOptionDisabled value."""
#         return self._getOptionDisabled.value if isinstance(self._getOptionDisabled, State) else self._getOptionDisabled

#     @_validate_param(file_path="qtmui.material.select", param_name="getOptionKey", supported_signatures=Union[State, Callable, type(None)])
#     def _set_getOptionKey(self, value):
#         """Assign value to getOptionKey."""
#         self._getOptionKey = value

#     def _get_getOptionKey(self):
#         """Get the getOptionKey value."""
#         return self._getOptionKey.value if isinstance(self._getOptionKey, State) else self._getOptionKey

#     @_validate_param(file_path="qtmui.material.select", param_name="getOptionLabel", supported_signatures=Union[State, Callable, type(None)])
#     def _set_getOptionLabel(self, value):
#         """Assign value to getOptionLabel."""
#         self._getOptionLabel = value

#     def _get_getOptionLabel(self):
#         """Get the getOptionLabel value."""
#         return self._getOptionLabel.value if isinstance(self._getOptionLabel, State) else self._getOptionLabel

#     @_validate_param(file_path="qtmui.material.select", param_name="groupBy", supported_signatures=Union[State, Callable, type(None)])
#     def _set_groupBy(self, value):
#         """Assign value to groupBy."""
#         self._groupBy = value

#     def _get_groupBy(self):
#         """Get the groupBy value."""
#         return self._groupBy.value if isinstance(self._groupBy, State) else self._groupBy

#     @_validate_param(file_path="qtmui.material.select", param_name="handleHomeEndKeys", supported_signatures=Union[State, bool])
#     def _set_handleHomeEndKeys(self, value):
#         """Assign value to handleHomeEndKeys."""
#         self._handleHomeEndKeys = value

#     def _get_handleHomeEndKeys(self):
#         """Get the handleHomeEndKeys value."""
#         return self._handleHomeEndKeys.value if isinstance(self._handleHomeEndKeys, State) else self._handleHomeEndKeys

#     @_validate_param(file_path="qtmui.material.select", param_name="id", supported_signatures=Union[State, str, type(None)])
#     def _set_id(self, value):
#         """Assign value to id."""
#         self._id = value

#     def _get_id(self):
#         """Get the id value."""
#         return self._id.value if isinstance(self._id, State) else self._id

#     @_validate_param(file_path="qtmui.material.select", param_name="includeInputInList", supported_signatures=Union[State, bool])
#     def _set_includeInputInList(self, value):
#         """Assign value to includeInputInList."""
#         self._includeInputInList = value

#     def _get_includeInputInList(self):
#         """Get the includeInputInList value."""
#         return self._includeInputInList.value if isinstance(self._includeInputInList, State) else self._includeInputInList

#     @_validate_param(file_path="qtmui.material.select", param_name="inputValue", supported_signatures=Union[State, str, type(None)])
#     def _set_inputValue(self, value):
#         """Assign value to inputValue."""
#         self._inputValue = value

#     def _get_inputValue(self):
#         """Get the inputValue value."""
#         return self._inputValue.value if isinstance(self._inputValue, State) else self._inputValue

#     @_validate_param(file_path="qtmui.material.select", param_name="isOptionEqualToValue", supported_signatures=Union[State, Callable, type(None)])
#     def _set_isOptionEqualToValue(self, value):
#         """Assign value to isOptionEqualToValue."""
#         self._isOptionEqualToValue = value

#     def _get_isOptionEqualToValue(self):
#         """Get the isOptionEqualToValue value."""
#         return self._isOptionEqualToValue.value if isinstance(self._isOptionEqualToValue, State) else self._isOptionEqualToValue

#     @_validate_param(file_path="qtmui.material.select", param_name="label", supported_signatures=Union[State, str, type(None)])
#     def _set_label(self, value):
#         """Assign value to label."""
#         self._label = value

#     def _get_label(self):
#         """Get the label value."""
#         return self._label.value if isinstance(self._label, State) else self._label

#     @_validate_param(file_path="qtmui.material.select", param_name="limitTags", supported_signatures=Union[State, int])
#     def _set_limitTags(self, value):
#         """Assign value to limitTags."""
#         self._limitTags = value

#     def _get_limitTags(self):
#         """Get the limitTags value."""
#         return self._limitTags.value if isinstance(self._limitTags, State) else self._limitTags

#     @_validate_param(file_path="qtmui.material.select", param_name="ListboxComponent", supported_signatures=Union[State, type, type(None)])
#     def _set_ListboxComponent(self, value):
#         """Assign value to ListboxComponent."""
#         self._ListboxComponent = value

#     def _get_ListboxComponent(self):
#         """Get the ListboxComponent value."""
#         return self._ListboxComponent.value if isinstance(self._ListboxComponent, State) else self._ListboxComponent

#     @_validate_param(file_path="qtmui.material.select", param_name="ListboxProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_ListboxProps(self, value):
#         """Assign value to ListboxProps."""
#         self._ListboxProps = value

#     def _get_ListboxProps(self):
#         """Get the ListboxProps value."""
#         return self._ListboxProps.value if isinstance(self._ListboxProps, State) else self._ListboxProps

#     @_validate_param(file_path="qtmui.material.select", param_name="loading", supported_signatures=Union[State, bool])
#     def _set_loading(self, value):
#         """Assign value to loading."""
#         self._loading = value

#     def _get_loading(self):
#         """Get the loading value."""
#         return self._loading.value if isinstance(self._loading, State) else self._loading

#     @_validate_param(file_path="qtmui.material.select", param_name="loadingText", supported_signatures=Union[State, str])
#     def _set_loadingText(self, value):
#         """Assign value to loadingText."""
#         self._loadingText = value

#     def _get_loadingText(self):
#         """Get the loadingText value."""
#         return self._loadingText.value if isinstance(self._loadingText, State) else self._loadingText

#     @_validate_param(file_path="qtmui.material.select", param_name="multiple", supported_signatures=Union[State, bool])
#     def _set_multiple(self, value):
#         """Assign value to multiple."""
#         self._multiple = value

#     def _get_multiple(self):
#         """Get the multiple value."""
#         return self._multiple.value if isinstance(self._multiple, State) else self._multiple

#     @_validate_param(file_path="qtmui.material.select", param_name="name", supported_signatures=Union[State, str, type(None)])
#     def _set_name(self, value):
#         """Assign value to name."""
#         self._name = value

#     def _get_name(self):
#         """Get the name value."""
#         return self._name.value if isinstance(self._name, State) else self._name

#     @_validate_param(file_path="qtmui.material.select", param_name="noOptionsText", supported_signatures=Union[State, str])
#     def _set_noOptionsText(self, value):
#         """Assign value to noOptionsText."""
#         self._noOptionsText = value

#     def _get_noOptionsText(self):
#         """Get the noOptionsText value."""
#         return self._noOptionsText.value if isinstance(self._noOptionsText, State) else self._noOptionsText

#     @_validate_param(file_path="qtmui.material.select", param_name="open", supported_signatures=Union[State, bool])
#     def _set_open(self, value):
#         """Assign value to open."""
#         self._open = value

#     def _get_open(self):
#         """Get the open value."""
#         return self._open.value if isinstance(self._open, State) else self._open

#     @_validate_param(file_path="qtmui.material.select", param_name="onChange", supported_signatures=Union[State, Callable, type(None)])
#     def _set_onChange(self, value):
#         """Assign value to onChange."""
#         self._onChange = value

#     def _get_onChange(self):
#         """Get the onChange value."""
#         return self._onChange.value if isinstance(self._onChange, State) else self._onChange

#     @_validate_param(file_path="qtmui.material.select", param_name="openOnFocus", supported_signatures=Union[State, bool])
#     def _set_openOnFocus(self, value):
#         """Assign value to openOnFocus."""
#         self._openOnFocus = value

#     def _get_openOnFocus(self):
#         """Get the openOnFocus value."""
#         return self._openOnFocus.value if isinstance(self._openOnFocus, State) else self._openOnFocus

#     @_validate_param(file_path="qtmui.material.select", param_name="openText", supported_signatures=Union[State, str])
#     def _set_openText(self, value):
#         """Assign value to openText."""
#         self._openText = value

#     def _get_openText(self):
#         """Get the openText value."""
#         return self._openText.value if isinstance(self._openText, State) else self._openText

#     @_validate_param(file_path="qtmui.material.select", param_name="PaperComponent", supported_signatures=Union[State, type, type(None)])
#     def _set_PaperComponent(self, value):
#         """Assign value to PaperComponent."""
#         self._PaperComponent = value

#     def _get_PaperComponent(self):
#         """Get the PaperComponent value."""
#         return self._PaperComponent.value if isinstance(self._PaperComponent, State) else self._PaperComponent

#     @_validate_param(file_path="qtmui.material.select", param_name="PopperComponent", supported_signatures=Union[State, type, type(None)])
#     def _set_PopperComponent(self, value):
#         """Assign value to PopperComponent."""
#         self._PopperComponent = value

#     def _get_PopperComponent(self):
#         """Get the PopperComponent value."""
#         return self._PopperComponent.value if isinstance(self._PopperComponent, State) else self._PopperComponent

#     @_validate_param(file_path="qtmui.material.select", param_name="popupIcon", supported_signatures=Union[State, QWidget, type(None)])
#     def _set_popupIcon(self, value):
#         """Assign value to popupIcon."""
#         self._popupIcon = value

#     def _get_popupIcon(self):
#         """Get the popupIcon value."""
#         return self._popupIcon.value if isinstance(self._popupIcon, State) else self._popupIcon

#     @_validate_param(file_path="qtmui.material.select", param_name="readOnly", supported_signatures=Union[State, bool])
#     def _set_readOnly(self, value):
#         """Assign value to readOnly."""
#         self._readOnly = value

#     def _get_readOnly(self):
#         """Get the readOnly value."""
#         return self._readOnly.value if isinstance(self._readOnly, State) else self._readOnly

#     @_validate_param(file_path="qtmui.material.select", param_name="renderOption", supported_signatures=Union[State, Callable, type(None)])
#     def _set_renderOption(self, value):
#         """Assign value to renderOption."""
#         self._renderOption = value

#     def _get_renderOption(self):
#         """Get the renderOption value."""
#         return self._renderOption.value if isinstance(self._renderOption, State) else self._renderOption

#     @_validate_param(file_path="qtmui.material.select", param_name="renderTags", supported_signatures=Union[State, Callable, type(None)])
#     def _set_renderTags(self, value):
#         """Assign value to renderTags."""
#         self._renderTags = value

#     def _get_renderTags(self):
#         """Get the renderTags value."""
#         return self._renderTags.value if isinstance(self._renderTags, State) else self._renderTags

#     @_validate_param(file_path="qtmui.material.select", param_name="renderValue", supported_signatures=Union[State, Callable, type(None)])
#     def _set_renderValue(self, value):
#         """Assign value to renderValue."""
#         self._renderValue = value

#     def _get_renderValue(self):
#         """Get the renderValue value."""
#         return self._renderValue.value if isinstance(self._renderValue, State) else self._renderValue

#     @_validate_param(file_path="qtmui.material.select", param_name="selectOnFocus", supported_signatures=Union[State, bool])
#     def _set_selectOnFocus(self, value):
#         """Assign value to selectOnFocus."""
#         self._selectOnFocus = value

#     def _get_selectOnFocus(self):
#         """Get the selectOnFocus value."""
#         return self._selectOnFocus.value if isinstance(self._selectOnFocus, State) else self._selectOnFocus

#     @_validate_param(file_path="qtmui.material.select", param_name="selected", supported_signatures=Union[State, bool])
#     def _set_selected(self, value):
#         """Assign value to selected."""
#         self._selected = value

#     def _get_selected(self):
#         """Get the selected value."""
#         return self._selected.value if isinstance(self._selected, State) else self._selected

#     @_validate_param(file_path="qtmui.material.select", param_name="size", supported_signatures=Union[State, str], valid_values=VALID_SIZES)
#     def _set_size(self, value):
#         """Assign value to size."""
#         self._size = value

#     def _get_size(self):
#         """Get the size value."""
#         return self._size.value if isinstance(self._size, State) else self._size

#     @_validate_param(file_path="qtmui.material.select", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_slotProps(self, value):
#         """Assign value to slotProps."""
#         self._slotProps = value

#     def _get_slotProps(self):
#         """Get the slotProps value."""
#         return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

#     @_validate_param(file_path="qtmui.material.select", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
#     def _set_slots(self, value):
#         """Assign value to slots."""
#         self._slots = value

#     def _get_slots(self):
#         """Get the slots value."""
#         return self._slots.value if isinstance(self._slots, State) else self._slots

#     @_validate_param(file_path="qtmui.material.select", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
#     def _set_sx(self, value):
#         """Assign value to sx."""
#         self._sx = value

#     def _get_sx(self):
#         """Get the sx value."""
#         return self._sx.value if isinstance(self._sx, State) else self._sx

#     @_validate_param(file_path="qtmui.material.select", param_name="value", supported_signatures=Union[State, Any, type(None)])
#     def _set_value(self, value):
#         """Assign value to value."""
#         self._value = value
#         self._state = value

#     def _get_value(self):
#         """Get the value value."""
#         return self._value.value if isinstance(self._value, State) else self._value

#     @_validate_param(file_path="qtmui.material.select", param_name="treeView", supported_signatures=Union[State, bool])
#     def _set_treeView(self, value):
#         """Assign value to treeView."""
#         self._treeView = value

#     def _get_treeView(self):
#         """Get the treeView value."""
#         return self._treeView.value if isinstance(self._treeView, State) else self._treeView

#     @_validate_param(file_path="qtmui.material.select", param_name="autoWidth", supported_signatures=Union[State, bool])
#     def _set_autoWidth(self, value):
#         """Assign value to autoWidth."""
#         self._autoWidth = value

#     def _get_autoWidth(self):
#         """Get the autoWidth value."""
#         return self._autoWidth.value if isinstance(self._autoWidth, State) else self._autoWidth

#     @_validate_param(file_path="qtmui.material.select", param_name="defaultOpen", supported_signatures=Union[State, bool])
#     def _set_defaultOpen(self, value):
#         """Assign value to defaultOpen."""
#         self._defaultOpen = value

#     def _get_defaultOpen(self):
#         """Get the defaultOpen value."""
#         return self._defaultOpen.value if isinstance(self._defaultOpen, State) else self._defaultOpen

#     @_validate_param(file_path="qtmui.material.select", param_name="displayEmpty", supported_signatures=Union[State, bool])
#     def _set_displayEmpty(self, value):
#         """Assign value to displayEmpty."""
#         self._displayEmpty = value

#     def _get_displayEmpty(self):
#         """Get the displayEmpty value."""
#         return self._displayEmpty.value if isinstance(self._displayEmpty, State) else self._displayEmpty

#     @_validate_param(file_path="qtmui.material.select", param_name="IconComponent", supported_signatures=Union[State, QWidget, type(None)])
#     def _set_IconComponent(self, value):
#         """Assign value to IconComponent."""
#         self._IconComponent = value

#     def _get_IconComponent(self):
#         """Get the IconComponent value."""
#         return self._IconComponent.value if isinstance(self._IconComponent, State) else self._IconComponent

#     @_validate_param(file_path="qtmui.material.select", param_name="input", supported_signatures=Union[State, QWidget, type(None)])
#     def _set_input(self, value):
#         """Assign value to input."""
#         self._input = value

#     def _get_input(self):
#         """Get the input value."""
#         return self._input.value if isinstance(self._input, State) else self._input

#     @_validate_param(file_path="qtmui.material.select", param_name="inputProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_inputProps(self, value):
#         """Assign value to inputProps."""
#         self._inputProps = value

#     def _get_inputProps(self):
#         """Get the inputProps value."""
#         return self._inputProps.value if isinstance(self._inputProps, State) else self._inputProps

#     @_validate_param(file_path="qtmui.material.select", param_name="labelId", supported_signatures=Union[State, str, type(None)])
#     def _set_labelId(self, value):
#         """Assign value to labelId."""
#         self._labelId = value

#     def _get_labelId(self):
#         """Get the labelId value."""
#         return self._labelId.value if isinstance(self._labelId, State) else self._labelId

#     @_validate_param(file_path="qtmui.material.select", param_name="MenuProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_MenuProps(self, value):
#         """Assign value to MenuProps."""
#         self._MenuProps = value

#     def _get_MenuProps(self):
#         """Get the MenuProps value."""
#         return self._MenuProps.value if isinstance(self._MenuProps, State) else self._MenuProps

#     @_validate_param(file_path="qtmui.material.select", param_name="native", supported_signatures=Union[State, bool])
#     def _set_native(self, value):
#         """Assign value to native."""
#         self._native = value

#     def _get_native(self):
#         """Get the native value."""
#         return self._native.value if isinstance(self._native, State) else self._native

#     @_validate_param(file_path="qtmui.material.select", param_name="SelectDisplayProps", supported_signatures=Union[State, Dict, type(None)])
#     def _set_SelectDisplayProps(self, value):
#         """Assign value to SelectDisplayProps."""
#         self._SelectDisplayProps = value

#     def _get_SelectDisplayProps(self):
#         """Get the SelectDisplayProps value."""
#         return self._SelectDisplayProps.value if isinstance(self._SelectDisplayProps, State) else self._SelectDisplayProps

#     @_validate_param(file_path="qtmui.material.select", param_name="variant", supported_signatures=Union[State, str], valid_values=VALID_VARIANTS)
#     def _set_variant(self, value):
#         """Assign value to variant."""
#         self._variant = value

#     def _get_variant(self):
#         """Get the variant value."""
#         return self._variant.value if isinstance(self._variant, State) else self._variant

#     def _init_ui(self):
#         """Initialize the UI based on props."""
#         self.setLayout(QVBoxLayout())
#         self.layout().setContentsMargins(0, 0, 0, 0)
#         self.layout().setSpacing(self.theme.spacing(1))

#         # Clear previous widgets
#         self._widget_references.clear()
#         while self.layout().count():
#             item = self.layout().takeAt(0)
#             if item.widget():
#                 item.widget().setParent(None)

#         # Determine initial value
#         initial_value = self._get_value() if self._get_value() is not None else self._get_defaultValue()

#         # Create input field
#         input_params = {
#             "label": self._get_label(),
#             "select": True,
#             "autoComplete": self._get_autoComplete(),
#             "disabled": self._get_disabled(),
#             "defaultValue": initial_value,
#             "fullWidth": self._get_fullWidth(),
#             "id": self._get_id(),
#             "options": self._get_options(),
#             "onChange": self._on_input_change,
#             "treeView": self._get_treeView(),
#             "multiple": self._get_multiple(),
#             "getOptionLabel": self._get_getOptionLabel(),
#             "renderOption": self._get_renderOption(),
#             "renderTags": self._get_renderTags(),
#             "renderValue": self._get_renderValue(),
#             "size": self._get_size(),
#             "value": initial_value,
#             "variant": self._get_variant(),
#             **(self._get_inputProps() or {})
#         }
#         self._inputField = self._get_input() or (self._get_renderInput()(input_params) if self._get_renderInput() else TextField(**input_params))
#         self.layout().addWidget(self._inputField)
#         self._widget_references.append(self._inputField)

#         # Set initial open state
#         if self._get_defaultOpen() and not self._get_open():
#             self._set_open(True)
#             self.onOpen.emit()

#         # Start timer to check input field setup
#         QTimer.singleShot(0, self._check_input_field)

#     def _check_input_field(self):
#         """Check if input field is ready and emit setupUi signal."""
#         if hasattr(self._inputField, "_lineEdit"):
#             self.setupUi.emit()
#         else:
#             QTimer.singleShot(200, self._check_input_field)

#     def _setup_ui(self):
#         """Setup UI after input field is ready."""
#         if isinstance(self._inputField, TextField):
#             if isinstance(self._state, State):
#                 self._inputField._lineEdit.setText(self._state.value or "")
#                 self._state.valueChanged.connect(self._update_input_text)
#             elif self._state is not None:
#                 self._inputField._lineEdit.setText(str(self._state))

#         if self._get_selected():
#             self._apply_selected_style()

#         if hasattr(self._inputField, "valueChanged"):
#             self._inputField.valueChanged.connect(self._on_input_change)

#     def _update_input_text(self):
#         """Update input text when state changes."""
#         value = self._state.value or ""
#         if isinstance(self._inputField._lineEdit, QLineEdit):
#             self._inputField._lineEdit.setText(value)
#         else:
#             self._inputField._lineEdit.setPlainText(value)

#     def _on_input_change(self, value, child=None):
#         """Handle input value change."""
#         self._set_value(value)
#         self.changed.emit(None, child)
#         if self._get_onChange():
#             self._get_onChange()(None, child)

#     def _apply_selected_style(self):
#         """Apply styles when selected."""
#         theme = useTheme()
#         active_border = theme.palette.primary.main
#         hover_background = alpha(theme.palette.primary.main, 0.08)
#         self._inputField.setStyleSheet(f"""
#             QComboBox {{
#                 border-color: {active_border};
#             }}
#         """)

#     def _set_stylesheet(self, component_styled=None):
#         """Set the stylesheet for the Select."""
#         self.theme = useTheme()
#         component_styled = component_styled or self.theme.components
#         select_styles = component_styled.get("Select", {}).get("styles", {})
#         root_styles = select_styles.get("root", {})
#         root_qss = get_qss_style(root_styles)

#         # Handle sx
#         sx = self._get_sx()
#         sx_qss = ""
#         if sx:
#             if isinstance(sx, (list, dict)):
#                 sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
#             elif isinstance(sx, Callable):
#                 sx_result = sx()
#                 if isinstance(sx_result, (list, dict)):
#                     sx_qss = get_qss_style(sx_result, class_name=f"#{self.objectName()}")
#                 elif isinstance(sx_result, str):
#                     sx_qss = sx_result
#             elif isinstance(sx, str) and sx != "":
#                 sx_qss = sx

#         # Handle classes
#         classes = self._get_classes()
#         classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}") if classes else ""

#         # Handle slotProps
#         slot_props = self._get_slotProps() or {}
#         slot_props_qss = get_qss_style(slot_props.get('root', {}).get('sx', {}), class_name=f"#{self.objectName()}")

#         # Apply MUI classes
#         mui_classes = ["MuiSelect-root"]
#         if self._get_disabled():
#             mui_classes.append("Mui-disabled")

#         stylesheet = f"""
#             #{self.objectName()} {{
#                 {root_qss}
#                 {classes_qss}
#                 {slot_props_qss}
#                 background: transparent;
#             }}
#             {sx_qss}
#         """
#         self.setStyleSheet(stylesheet)

#     def _connect_signals(self):
#         """Connect valueChanged signals of State parameters to their slots."""
#         if isinstance(self._options, State):
#             self._options.valueChanged.connect(self._on_options_changed)
#         if isinstance(self._renderInput, State):
#             self._renderInput.valueChanged.connect(self._on_renderInput_changed)
#         if isinstance(self._autoComplete, State):
#             self._autoComplete.valueChanged.connect(self._on_autoComplete_changed)
#         if isinstance(self._autoHighlight, State):
#             self._autoHighlight.valueChanged.connect(self._on_autoHighlight_changed)
#         if isinstance(self._autoSelect, State):
#             self._autoSelect.valueChanged.connect(self._on_autoSelect_changed)
#         if isinstance(self._blurOnSelect, State):
#             self._blurOnSelect.valueChanged.connect