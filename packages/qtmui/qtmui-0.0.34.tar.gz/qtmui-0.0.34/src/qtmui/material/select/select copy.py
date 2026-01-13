import asyncio
from functools import lru_cache
import inspect
import threading
import uuid
import time
from typing import Optional, Callable, Any, Dict, Union, List

from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPlainTextEdit, QLineEdit, QApplication, QStyledItemDelegate, \
        QSizePolicy, QPushButton, QSpinBox, QDoubleSpinBox, QGraphicsOpacityEffect, QFrame, QGroupBox
from PySide6.QtCore import Qt, QPoint, Signal, QDate, QTime, QTimer, QEvent, QSize
from PySide6.QtGui import QCursor

from qtmui.hooks import State
from qtmui.utils.translator import getTranslatedText
from ..li import Li

from ..menu import Menu
from ..menu_item import MenuItem

from .flow_layout import FlowLayout
from .tags_view import TagsView

from ..picker import DatePicker, TimePicker, AMTimePicker, ZhDatePicker, CalendarPicker, ColorPicker

from qtmui.hooks import useState

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from ..utils._misc import signals_blocked
from ..utils.functions import _get_fn_args

from ...qtmui_assets import QTMUI_ASSETS

from ..py_iconify import PyIconify

from .py_line_edit import PyLineEdit
from .py_line_edit_multiple import PyLineEditMultiple
from .py_plaintext_edit import PyPlainTextEdit
from .py_plaintext_edit_multiple import PyPlainTextEditMultiple

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from ..widget_base import PyWidgetBase

from ..utils.validate_params import _validate_param

class Select(QGroupBox):

    showPlaceholder = Signal()
    valueChanged = Signal(object)
    updatePopupPosition = Signal()
    createMenu = Signal()
    renderSearchMenuItems = Signal(object)

    VALID_COLORS = ['primary', 'secondary', 'error', 'info', 'success', 'warning']
    VALID_MARGINS = ['dense', 'none', 'normal']
    VALID_SIZES = ['medium', 'small']
    VALID_VARIANTS = ['filled', 'outlined', 'standard']

    def __init__(
        self,
        key: str= None,
        autoWidth: Optional[Union[State, bool]] = False, # chỉ dùng cho Select
        color: Optional[Union[State, str]] = "primary",
        defaultOpen: Optional[Union[State, bool]] = False, # chỉ dùng cho Select
        defaultValue: Optional[Union[State, object]] = None,
        disabled: Optional[Union[State, bool]] = False,
        children: Optional[Union[State, list]] = None,
        error: Optional[Union[State, bool]] = False,
        fullWidth: Optional[Union[State, bool]] = False,
        helperText: Optional[Union[State, str]] = None,
        id: Optional[Union[State, str]] = None,
        label: Optional[Union[State, str, Callable]] = None,
        multiple: Optional[Union[State, bool]] = False,
        menuHeight: Optional[Union[State, int]] = 400,
        name: Optional[Union[State, str]] = None,
        getOptionLabel: Optional[Union[State, Callable]] = None,
        open: Optional[Union[State, bool]] = False, # chỉ dùng cho Select
        onOpen: Optional[Union[State, Callable]] = None, # chỉ dùng cho Select
        onClose: Optional[Union[State, Callable]] = None, # chỉ dùng cho Select
        onChange: Optional[Union[State, Callable]] = None,
        options: Optional[Union[State, object]] = None,
        hiddenLabel: Optional[Union[State, bool]] = False,
        placeholder: Optional[Union[State, str]] = None,
        required: Optional[Union[State, bool]] = False,
        size: Optional[Union[State, str]] = "medium",
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        step: Optional[Union[State, int, float]] = None,
        renderSelectOptions: Optional[Union[State, Callable]] = None,
        renderOption: Optional[Union[State, Callable]] = None,
        renderValue: Optional[Union[State, Callable]] = None,
        renderTags: Optional[Union[State, Callable]] = None,
        readOnly: Optional[Union[State, bool]] = False, # chỉ dùng cho Select
        value = None,
        variant: Optional[Union[State, str]] = "outlined",
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.setObjectName(str(uuid.uuid4()))
        start_time = time.time()

        self._key = key
        
        if self._key == "proxyTypekyyyyyyyyyyyyyyyyy":
            print('ProfileTextField__________________', self._key)

        self._key = key
        self._color = color
        self._defaultValue = defaultValue
        self._disabled = disabled
        self._error = error
        self._fullWidth = fullWidth
        self._helperText = helperText
        self._id = id
        self._label = label
        self._multiple = multiple
        self._menuHeight = menuHeight
        self._name = name
        self._getOptionLabel = getOptionLabel
        self._onChange = onChange
        self._options = options
        self._hiddenLabel = hiddenLabel
        self._placeholder = placeholder
        self._required = required
        self._size = size
        self._sx = sx
        self._step = step
        self._renderSelectOptions = renderSelectOptions
        self._renderOption = renderOption
        self._renderValue = renderValue
        self._renderTags = renderTags
        self._value = value
        self._variant = variant

        self.__init_ui()
        
        end_time = time.time()
        
        # print("time_loading_textfield___________________________", (end_time - start_time)/0.00013971328735351562)


    def _connect_signals_props(self):
        if isinstance(self._value, State):
            self._value.valueChanged.connect(self._set_data)

    def __init_ui(self):
        self._init_done = False

        self._connect_signals_props()

        self.theme = useTheme()
        
        i18n.langChanged.connect(self._set_translated_label)

        if self._fullWidth:
            if not self._sx:
                self._sx = {}
            self._sx.update({"width": "100%"})

        self._data = None

        self._tagsWidget = None
        self._selected_options = {}
        self._inputFieldHasFocusIn = False


        self._inputField = None
        self._popup = None
        self._btnSelect = None

        self._menu = None
        self._menuItems, self._setMenuItems = useState([])
        
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        
        self._focused, self._setFocused = useState(False)
        self._hovered, self._setHovered = useState(False)

        if self._multiple:
            self._inputField: PyPlainTextEditMultiple = PyPlainTextEditMultiple
        else:
            self._inputField: PyLineEdit = PyLineEdit

        self._inputField = self._inputField(
            label=self._label,
            onMouseEnter=self.onMouseEnter,
            onMouseLeave=self.onMouseLeave,
            onFocusIn=self.onFocusIn,
            onFocusOut=self.onFocusOut,
            onMouseRelease=self.onMouseRelease,
            onChange=self.onChange,
            variant=self._variant,
            size=self._size,
            sx=f"""
                QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QFontComboBox,
                QLineEdit, QPlainTextEdit, QSpinBox, QTextEdit, QTimeEdit {{
                    border: none;
                    width: 100%;
                    background-color: transparent;
                    padding-left: 8px;
                }}
                QPlainTextEdit {{
                    border: none;
                    width: 100%;
                    min-height: 22px;
                    background-color: transparent;
                    padding-left: 5px;
                }}
            """
        )

        self.setMinimumHeight(44)
        
        self._inputField.setReadOnly(True)
        self._inputField.setCursor(Qt.PointingHandCursor)

        self.layout().addWidget(self._inputField)

        if self._defaultValue is not None:
            self._set_data(self._defaultValue, setText=True)

        if self._value is not None:
            self._set_data( self._value, setText=True)

        if self._disabled:
            self.setEnabled(False)

        PyWidgetBase._installTooltipFilter(self)


        # ASYN INIT
        QTimer.singleShot(0, self._scheduleSetupSelectMode)
        
        # chỗ này nghiên cứu lại kỹ hơn, chưa kiểm định lỗi, ít khi menu dài tới hàm trăm phần tử, nên k nhất thiết load trước
        # QTimer.singleShot(500, self._scheduleCraeteMenu) 

        self.theme.state.valueChanged.connect(self._onThemeChanged)
        # QTimer.singleShot(0, self._scheduleSetStyleSheet)
        self._set_stylesheet()
        
        if self._multiple:
            QTimer.singleShot(0, self._scheduleSetupDefaultTags)
            
        self.destroyed.connect(lambda obj: self._onDestroy())
        
        self._init_done = True

    def _onDestroy(self, obj=None):
        # Cancel task nếu đang chạy
        if hasattr(self, "_setupDefaultTags") and self._setupDefaultTags and not self._setupDefaultTags.done():
            self._setupDefaultTags.cancel()
        if hasattr(self, "_setupStyleSheet") and self._setupStyleSheet and not self._setupStyleSheet.done():
            self._setupStyleSheet.cancel()
        if hasattr(self, "_setupSelectMode") and self._setupSelectMode and not self._setupSelectMode.done():
            self._setupSelectMode.cancel()
        if hasattr(self, "_setupMenu") and self._setupMenu and not self._setupMenu.done():
            self._setupMenu.cancel()
            
    def _onThemeChanged(self):
        if not self.isVisible():
            return
        QTimer.singleShot(0, self._scheduleSetStyleSheet)
            
    def _scheduleSetupDefaultTags(self):
        self._setupDefaultTags = asyncio.ensure_future(self._lazySetupDefautTags())

    async def _lazySetupDefautTags(self):
        if self._defaultValue:
            for option in self._defaultValue:
                key = self._getOptionLabel(option)
                self._selected_options.update({key: option})
            self.tags = self._renderTags(self._selected_options, self.getTagProps)
            self._setFlowLayout(FlowLayout(self, children=self.tags))
            
    def _scheduleSetStyleSheet(self):
        self._setupStyleSheet = asyncio.ensure_future(self._lazy_set_stylesheet())

    async def _lazy_set_stylesheet(self):
        self._set_stylesheet()
        
    def _scheduleSetupSelectMode(self):
        self._setupSelectMode = asyncio.ensure_future(self._lazy_setupSelectMode())

    async def _lazy_setupSelectMode(self):
        self._setup_select_mode()

    def _scheduleCraeteMenu(self):
        self._setupMenu = asyncio.ensure_future(self._lazy_create_menu())

    async def _lazy_create_menu(self):
        self._create_menu()

    def _setup_select_mode(self):
        self.updatePopupPosition.connect(self._update_popup_position)

        # đặt ở đây để có _selectedKeys truyền cho PyLineEditMultiple => setup placeholder đúng
        if self._options:
            self._selectedKeys, self._setSelectedKeys = useState(self._options[0] if isinstance(self._options[0], str) else self._options[0].get("value") or "")

            if self._multiple:
                if self._defaultValue:
                    selectedKeys = ["has_defaultValue"] # để thiết lập placeholder cho đúng
                    self._selectedKeys, self._setSelectedKeys = useState(selectedKeys)
            else:
                self._selectedKeys, self._setSelectedKeys = useState(
                    self._options[0] if isinstance(self._options[0], str) 
                    else self._getOptionLabel(self._options[0]) if self._getOptionLabel else self._options[0].get("value") or ""
                )
        elif self._renderOption: # cho Select - select thi k render tag ma render text value
            self._selectedKeys, self._setSelectedKeys = useState(self._data)

        elif self._selectOptions: 
            self._selectedKeys, self._setSelectedKeys = useState(self._data)

        self.action_frame = QWidget(self)
        self.action_frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        hlo_action_frame = QHBoxLayout(self.action_frame)
        hlo_action_frame.setContentsMargins(0,0,0,0)
        self.action_frame.setFixedWidth(54)
        self.action_frame.layout().setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        if self._multiple:
            
            if self._renderTags:
                self._flowLayout, self._setFlowLayout = useState(FlowLayout(self, []))
                self._flow_layout_view = TagsView(content=self._flowLayout)
                self._flow_layout_view.layout().setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self._inputField.setReadOnly(True)
                self._inputField.setLayout(QHBoxLayout())
                self._inputField.layout().setContentsMargins(0,0,54,0)
                self._inputField.setPlaceholderText("")
                self._inputField.layout().addWidget(self._flow_layout_view)
                self._flow_layout_view.mousePressEvent = self.onFlowlayoutMousePressEvent

            elif self._renderValue:
                if self._data:
                    self._inputField.setPlainText(self._renderValue(self._data))

            if isinstance(self._renderOption, State):
                self._renderOption.valueChanged.connect(self._create_menu)


        if self._options and not self._getOptionLabel:
            raise AttributeError("Opp!! 'getOptionLabel' is required attribute!")
        
        self._btn_clear_text= QPushButton()
        self._btn_clear_text.setFixedSize(24, 24)
        self._btn_clear_text.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.CLOSE))
        self._btn_clear_text.setCursor(Qt.PointingHandCursor)
        self._btn_clear_text.clicked.connect(self._on_clear_text)
        self._btn_clear_text.hide()
        hlo_action_frame.addWidget(self._btn_clear_text)
        self._btn_clear_text.hide()
        self._btn_clear_text.setFocusPolicy(Qt.NoFocus)
        self._btn_clear_text.setAttribute(Qt.WA_ShowWithoutActivating, True)

        self._btnSelect = QPushButton()
        self._btnSelect.setCursor(Qt.PointingHandCursor)
        self._btnSelect.setFixedSize(24, 24)
            
        self._btnSelect.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_DOWN))
        self._btnSelect.clicked.connect(self._btn_select_toggle_popup)
        hlo_action_frame.addWidget(self._btnSelect)

        self._inputField.installEventFilter(self)
        
        self.setup_action_frame_and_adornment()
        

    # @timer
    def _set_stylesheet(self, component_styled=None):
        _theme_mode = useTheme().palette.mode
        self.setProperty("variant", self._variant)
        if self._renderTags:
            _renderTags = "True"
        else:
            _renderTags = "False"

        stylesheet = self._get_stylesheet(self._variant, self._size, _theme_mode, str(self._multiple),  _renderTags )
        stylesheet = stylesheet.replace("_________object_name_______", self.objectName())
        self.setStyleSheet(stylesheet)

    @classmethod
    @lru_cache(maxsize=128)
    def _get_stylesheet(cls, _variant: str, _size: str, _theme_mode: str, _multiple: str,  _renderTags:str):
        """Set the stylesheet for the Box."""
        theme = useTheme()

        # Chung cho toàn bộ input
        MuiInput = theme.components["MuiInput"].get("styles")
        MuiInput_root = MuiInput.get("root")
        MuiInput_root_qss = get_qss_style(MuiInput_root)
        MuiInput_title = MuiInput.get("title")
        MuiInput_title_qss = get_qss_style(MuiInput_title)
        MuiInput_title_slot_focused_qss = get_qss_style(MuiInput_title["slots"]["focused"])
        MuiInput_title_slot_error_qss = get_qss_style(MuiInput_title["slots"]["error"])
        MuiInput_title_slot_disabled_qss = get_qss_style(MuiInput_title["slots"]["disabled"])
        MuiInput_inputField = MuiInput.get("inputField")
        MuiInput_inputField_qss = get_qss_style(MuiInput_inputField)
        MuiInput_inputField_prop_multiline_qss = get_qss_style(MuiInput_inputField["props"]["multiline"][f"{_size}"])
        MuiInput_inputField_prop_multiple_qss = get_qss_style(MuiInput_inputField["props"]["multiple"])

        MuiInputSize = theme.components["MuiInputSize"]["styles"][f"{_size}"]
        MuiInputSize_qss = get_qss_style(MuiInputSize)

        MuiInputSize_not_multiple_qss = get_qss_style(MuiInputSize["no-multiple"])
        MuiInputSize_no_multiple_height = MuiInputSize["no-multiple"]["height"]

        # thiết lập tuỳ theo variant
        PyVariantInput = theme.components[f"Py{_variant.capitalize()}Input"].get("styles")
        PyVariantInput_root = PyVariantInput.get("root")
        PyVariantInput_root_qss = get_qss_style(PyVariantInput_root)
        PyVariantInput_root_slot_hovered_qss = get_qss_style(PyVariantInput_root["slots"]["hover"])
        PyVariantInput_root_slot_focused_qss = get_qss_style(PyVariantInput_root["slots"]["focus"])
        
        PyVariantInput_inputField_root = PyVariantInput.get("inputField")["root"]
        PyVariantInput_inputField_root_qss = get_qss_style(PyVariantInput_inputField_root)

        PyVariantInput_root_prop_hasStartAdornment_qss = ""
        if PyVariantInput_inputField_root.get("props"):
            PyVariantInput_root_prop_hasStartAdornment_qss = get_qss_style(PyVariantInput_inputField_root["props"]["hasStartAdornment"])

        MuiInputSize = theme.components["MuiInputSize"]["styles"][f"{_size}"]
        MuiInputSize_qss = get_qss_style(MuiInputSize)

        # print('MuiInputSize_qss______________', MuiInputSize_qss)

        _________object_name_______ = "_________object_name_______"


        input_base_stylesheet = f"""
                #{_________object_name_______} {{
                    {MuiInput_root_qss}
                    {MuiInputSize_qss}
                }}

                #{_________object_name_______} QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QFontComboBox,
                QLineEdit, PyPlainTextEdit, QSpinBox, QTextEdit, QTimeEdit {{
                    {MuiInput_inputField_qss}
                }}
                #{_________object_name_______}[multipleHasValue=true] QPlainTextEdit {{
                    {MuiInput_inputField_prop_multiple_qss}
                }}

                #{_________object_name_______} QPlainTextEdit{{
                    min-height: 40px;
                }}
                #{_________object_name_______}::title {{
                    {MuiInput_title_qss}
                }}
                #{_________object_name_______}[focused=true]::title {{
                    {MuiInput_title_slot_focused_qss}
                }}
                #{_________object_name_______}[error=true]::title {{
                    {MuiInput_title_slot_error_qss}
                }}
                #{_________object_name_______}[disabled=true]::title {{
                    {MuiInput_title_slot_disabled_qss}
                }}
            """

        _variant_stylesheet = f"""
                #{_________object_name_______}[variant={_variant}] {{
                    {PyVariantInput_root_qss}
                    {MuiInputSize_qss}
                }}
                #{_________object_name_______}[variant={_variant}]  QLineEdit, QPlainTextEdit, QTextEdit {{
                    {PyVariantInput_inputField_root_qss}
                }}
                #{_________object_name_______}[outlinedHasStartAdornment=true]  QLineEdit, QPlainTextEdit, QTextEdit {{
                    {PyVariantInput_root_prop_hasStartAdornment_qss}
                }}
                #{_________object_name_______}[hovered=true] {{
                    {PyVariantInput_root_slot_hovered_qss}
                }}
                #{_________object_name_______}[focused=true] {{
                    {PyVariantInput_root_slot_focused_qss}
                }}
            """
        
        return input_base_stylesheet + _variant_stylesheet


    def _create_menu(self):
        print("_create_menu called")

        try:
            if not self._menu:
                self._menu = Menu(
                    maxHeight=self._menuHeight,
                    children=self._menuItems
                )

            if self._options:
                self._selectOptions = []
                for _option in self._options:
                    props = {}
                    option = self._renderOption(props, _option)

                    if isinstance(option, Li):
                        option._set_selected_keys(self._selectedKeys)
                        option._set_on_changed(self._selected_change)
                    self._selectOptions.append(option)

            elif self._renderOption and isinstance(self._renderOption, Callable):
                self._selectOptions = self._renderOption(**(_get_fn_args(self._renderOption)))
                for option in self._selectOptions:
                    if isinstance(option, Li):
                        option._set_selected_keys(self._selectedKeys)
                        option._set_on_changed(self._selected_change)

            self._setMenuItems(self._selectOptions)
        except Exception as e:
            print(f"Error creating menu: {e}")
        
    def onFocusIn(self, event=None):
        self._setFocused(True)
        self._show_label()
        if self._variant == "filled":
            self._set_filled_foucusin_prop(True)

    def onFocusOut(self, event=None):
        print('onFocusOut______________5555555_______')
        
        # dành cho thiết lập khi nhấn vào nút clear hay select
        if hasattr(self, '_btn_clear_text') and QApplication.widgetAt(QCursor.pos()) is self._btn_clear_text:
            try:
                QTimer.singleShot(0, lambda: self._inputField.setFocus(Qt.OtherFocusReason))
            except Exception as e:
                print(f"Error setting focus: {e}")
            return

        if hasattr(self, '_btnSelect') and QApplication.widgetAt(QCursor.pos()) is self._btnSelect:
            try:
                QTimer.singleShot(0, lambda: self._inputField.setFocus(Qt.OtherFocusReason))
            except Exception as e:
                print(f"Error setting focus: {e}")
            return
        
        self._setFocused(False)
        print('onFocusOut______________77777777777_______')
        

        # nếu inputValue hiện tại không nằm trong options thì clear nó đi
        if self._multiple:
            if len(self._selectedKeys.value) == 0:
                self._hide_label()
        else:
            if isinstance(self._inputField, PyLineEdit):
                current_input_value = self._inputField.text()
            elif isinstance(self._inputField, PyPlainTextEdit):
                current_input_value = self._inputField.toPlainText()
                
            option_values = []
            options = self._options
            if options:
                for option in options:
                    label = option
                    if self._getOptionLabel:
                        label = self._getOptionLabel(option)
                    option_values.append(label.lower())
            if current_input_value.lower() not in option_values:
                self._set_data(None)
                if isinstance(self._inputField, PyLineEdit):
                    self._inputField.setText("")
                elif isinstance(self._inputField, PyPlainTextEdit):
                    self._inputField.setPlainText("")
                self._inputField._set_placer_holder_text()
            else:
                # set lại data dựa trên inputValue
                for option in options:
                    label = option
                    if self._getOptionLabel:
                        label = self._getOptionLabel(option)
                    if label.lower() == current_input_value.lower():
                        self._set_data(option)
                        self._inputField.setText(label)
                        break

        if self._data is None:
            if self._variant == "filled":
                self._set_filled_foucusin_prop(False)
            self._hide_label()

        if not self.underMouse():
            if hasattr(self, "_btn_clear_text") and self._btn_clear_text.isVisible():
                self._btn_clear_text.setVisible(False)


    def onMouseEnter(self, event=None):
        self._setHovered(True)
        if self._data:
            if hasattr(self, "_btn_clear_text") and not self._btn_clear_text.isVisible():
                self._btn_clear_text.setVisible(True)
        
    def onMouseLeave(self, event=None):
        self._setHovered(False)

    def onMouseRelease(self, event=None):
        pass

    def onFlowlayoutMousePressEvent(self, event=None):
        self._toggle_popup()
        

    def onChange(self, value=None):
        # nếu là select thì chưa set_value
        self._set_data(value, setText=False)


    def _set_data(self, value=None, valueChanged=True, setText=True):
        
        _selected_options = self._selected_options.copy()
        
        for key, val in _selected_options.items():
            if isinstance(value, list) and val not in value:
                del self._selected_options[key]
                
        if isinstance(value, State):
            self._data = value.value
        else:
            self._data = value

        if self._multiple:
            if self._data is not None:
                self._set_multiple_has_value_prop(True)
            else:
                self._set_multiple_has_value_prop(False)
        else:
            if self._data is not None:
                if self._variant == "filled":
                    self._set_filled_has_value_prop(True) # làm cho inputField padding top 1 khoảng cho giống mui JS
            else:
                if self._variant == "filled":
                    self._set_filled_has_value_prop(False) # làm cho inputField padding top 1 khoảng cho giống mui JS

        if value is not None: # value == "" cũng vào đây
            if self._data != "":
                self._show_label()

        if valueChanged:
            self.valueChanged.emit(self._data)

        if setText:
            self._set_text()

    def _set_text(self): # value
        if not self._multiple: # multiple thì set tag không cần set text
            if isinstance(self._data, dict):
                if self._getOptionLabel:
                    text = self._getOptionLabel(self._data)
                    self._inputField.setText(str(text))
            else:
                if self._getOptionLabel:
                    for option in self._options:
                        if isinstance(option, dict):
                            if self._getOptionLabel(option) == self._data: # options khong phai dạng value label
                                text = self._getOptionLabel(option)
                                self._inputField.setText(str(text))
                                break
                        elif isinstance(option, str):
                            if option == self._data:
                                text = self._getOptionLabel(option)
                                self._inputField.setText(str(text))
                                break
                else:
                    self._inputField.setText(str(self._data))

        else: # multiple
            if self._renderValue:
                if isinstance(self._inputField, PyPlainTextEditMultiple):
                    self._inputField.setPlainText(self._renderValue(self._data))
            else:
                self._inputField.setText(self._renderValue(self._data))

    def _set_slot(self, data):
        if data.get("slot") == "error":
            self._inputField.setProperty("p-error", "true")
        elif data.get("slot") == "valid":
            self._inputField.setProperty("p-error", "false")

    def _update_popup_position(self):
        if hasattr(self, "_popup") and self._popup is not None:
            popup_position = self.mapToGlobal(QPoint(0, self.height()))
            self._popup.setGeometry(popup_position.x(), popup_position.y(), self.width(), 50)


    def _hide_popup(self):
        if self._popup and self._popup.isVisible():
            self._popup.setVisible(False)
        icon = PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_DOWN)

        if self._btnSelect:
                self._btnSelect.setIcon(icon)
        self._popupShowing = False

    def _on_clear_text(self, e=None):
        pass

    def _btn_select_toggle_popup(self, e=None):
        if self._popup and self._popupShowing:
            print('__btn_select_toggle_popup_______________hide_popup')
            self._hide_popup()
        else:
            print('__btn_select_toggle_popup______________show_popup')
            self._show_popup()

    def _toggle_popup(self, e=None):
        if self._popup and self._popupShowing:
            self._hide_popup()
        else:
            self._show_popup()

    def _show_popup(self, search=None):
        
        if not self._menu:
            self._create_menu()
        
        if self._popup and self._popupShowing:
            return

        if not self._popup:
            self._popup = QFrame(self)
            self._popup.setFocusPolicy(Qt.NoFocus)
            self._popup.setAttribute(Qt.WA_ShowWithoutActivating, True)
            self._popup.setWindowFlags(Qt.Window |  Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
            self._popup.setAttribute(Qt.WA_TranslucentBackground, True) # Enable translucent background => setStyleSheet ko có tác dụng gì
            QApplication.instance().installEventFilter(self)
            self._popup.setObjectName(str(uuid.uuid4()))
            self._popup.setLayout(QVBoxLayout())
            self._popup.layout().setContentsMargins(0,0,9,9)
            self._popup.layout().addWidget(self._menu)
            self._popup.setAutoFillBackground(False)
            self._popup.setStyleSheet(f"#{self._popup.objectName()} {{background: transparent;border: 2px solid red;}}")

        # Lấy điểm cục bộ (x, y) của relativeTo và chuyển sang global
        global_point = self.mapToGlobal(QPoint(0, self.height()))
        
        # tính toán vị trí hiển thị popup
        main_window_pos_y = QApplication.instance().mainWindow.height()
        self_pos_y = global_point.y()
        
        self._popup.move(-3000, -3000) # di chuyển tạm để lấy kích thước
        self._popup.setVisible(True)

        if (main_window_pos_y - self_pos_y) < self._menu.height():
            global_point.setY(global_point.y() - self.height() - self._menu.height())
        
        self._popup.move(global_point)
        self._popup.setMinimumWidth(self.width())

        self._menu.setVisible(True)

        icon = PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_UP)
        self._btnSelect.setIcon(icon)
        self._popupShowing = True
        

    def _on_menu_item_selected(self, key):
        self._hide_popup()
        self._data = key


    def getTagProps(self, index):
        return {"onDelete": lambda key=index: self._on_tag_deleted(key)}

    def _on_tag_deleted(self, index):
        self._selected_change(index)

    def _update_selected_options(self, key=None, option=None):
        """
        Hàm này nhằm cập nhật giá trị self._selected_options cho Select
        """
        if key not in list(self._selected_options.values()):
            self._selected_options.update({key: key})
        else:
            self._selected_options.pop(key)

    def _setup_tags(self, key=None, option=None):
        if key:
            for _option in self._options:
                if self._getOptionLabel(_option) == key:
                    option = _option
                    break
        else:
            if option:
                if isinstance(option, dict):
                    key = self._getOptionLabel(option)

        if option not in self._selected_options.values():
            try:
                self._selected_options.update({key: option})
                self.tags = self._renderTags(self._selected_options, self.getTagProps)
            except Exception as e:
                import traceback
                traceback.print_exc()
            self._setFlowLayout(FlowLayout(self, children=self.tags))
        else:
            self._selected_options.pop(key)
            self.tags = self._renderTags(self._selected_options, self.getTagProps)
            self._setFlowLayout(FlowLayout(self, children=self.tags))

    def _selected_change(self, data):

        if isinstance(data, dict):
            key = data.get("value")
            value = data.get("value")
        else:
            key = data
            value = data

        if self._multiple:
            # for delete option item
            if key in self._selectedKeys.value:
                selected_keys = self._selectedKeys.value.copy()
                selected_keys.remove(key)
                self._setSelectedKeys(selected_keys)
                if self._renderTags:
                    self._setup_tags(key=key)
                elif self._renderValue:
                    self._update_selected_options(key)
                values = []
                for selected_option in self._selected_options.values():
                    values.append(selected_option)

                self._set_data(values)

                if self._onChange:
                    self._onChange(self._data)

                if self._renderValue:
                    self._inputField.setText(self._renderValue(self._data))

                return
            
            if self._renderTags: # cho Autocomplete - render tag
                self._setup_tags(key=key, option=key)
            else: # cho Select
                self._update_selected_options(key)
            
            keys = []
            values = []
            for selected_option in self._selected_options.values():
                if isinstance(selected_option, dict):
                    values.append(selected_option)
                    if self._getOptionLabel:
                        key = self._getOptionLabel(selected_option)
                        keys.append(key)
                elif isinstance(selected_option, str):
                    values.append(selected_option)
                    keys.append(selected_option)

            self._setSelectedKeys(keys)
            self._set_data(values)

            if self._onChange:
                self._onChange(self._data)

            if self._renderValue:
                self._inputField.setText(self._renderValue(self._data))

            self._hide_popup()
        else: # not multiple
            self._setSelectedKeys(key)
            self._set_data(value)
            self._selected_options.update({key: key})                
            self._hide_popup()

            # Call onChange with the new value
            if self._onChange:
                # self._onChange(data) # contronled state mode không đúng, nhận vào list mà onchange lại là dict
                self._onChange(self._data)
                
        if self._menu:
            for item in self._menu.findChildren(Li):
                item.show()

    def _show_label(self):
        if not self._hiddenLabel:
            self._set_translated_label()

    def _set_translated_label(self):
        if not self._hiddenLabel:
            self.setTitle(getTranslatedText(self._label))

    def _hide_label(self):
        print('_hide_label')
        self.setTitle("")

    def _set_hovered_prop(self):
        if self._disabled:
            return
        if isinstance(self._hovered, State):
            self.setProperty("hovered", self._hovered.value)
        elif isinstance(self._hovered, bool):
            self.setProperty("hovered", self._hovered)
        
    def _set_focused_prop(self):
        if isinstance(self._focused, State):
            self.setProperty("focused", self._focused.value)
        elif isinstance(self._focused, bool):
            self.setProperty("focused", self._focused)
        
    def _set_multiple_has_value_prop(self, state):
        self.setProperty("multipleHasValue", state)
        
    def _set_filled_has_value_prop(self, state:bool):
        self.setProperty("filledHasValue", state)

    def _set_filled_foucusin_prop(self, state:bool):
        self.setProperty("filledHasValue", state)

    def _set_prop_has_start_adornment(self, state:bool):
        self.setProperty("hasStartAdornment", state)

    def setup_action_frame_and_adornment(self):
        if hasattr(self, 'action_frame'):
            self.action_frame.move(self.width() - self.action_frame.width(), (self.height() + 6 - self.action_frame.height()) // 2)
            if not self.action_frame.isVisible():
                self.action_frame.show()

    def leaveEvent(self, event):
        if not self.underMouse() and not self._inputField.hasFocus():
            if hasattr(self, "_btn_clear_text") and self._btn_clear_text.isVisible():
                self._btn_clear_text.setVisible(False)
        return super().leaveEvent(event)

    def resizeEvent(self, event):
        self.setup_action_frame_and_adornment()
        return super().resizeEvent(event)
    
    def eventFilter(self, obj, event):
        if obj == self._inputField:
            if event.type() == QEvent.MouseButtonPress:
                self._show_popup()
        elif self._popup and self._popup.isVisible():
            if event.type() == QEvent.MouseButtonPress and not self.underMouse():
                if not self._popup.geometry().contains(event.globalPos()):
                    self._hide_popup()
            elif event.type() == QEvent.Wheel and ((not self.underMouse() and not self._popup.underMouse()) or obj == self._inputField):
                self._hide_popup()
            
        return super().eventFilter(obj, event)

