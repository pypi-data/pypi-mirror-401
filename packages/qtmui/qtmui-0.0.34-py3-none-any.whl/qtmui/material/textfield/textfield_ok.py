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
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.utils.data import deep_merge
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

from .py_combobox import PyComboBox
from .py_date_edit import PyDateEdit
from .py_date_time_edit import PyDateTimeEdit
from .py_dial import PyDial
from .py_double_spinbox import PyDoubleSpinBox
from .py_font_combobox import PyFontComboBox
from .tf_line_edit import TFLineEdit
from .tf_line_edit_multiple import TFLineEditMultiple
from .py_plaintext_edit import PyPlainTextEdit
from .py_plaintext_edit_multiple import PyPlainTextEditMultiple
from .py_spin_box import PySpinBox
from .py_text_edit import PyTextEdit
from .py_time_edit import PyTimeEdit


from ..widget_base import PyWidgetBase

from ..utils.validate_params import _validate_param

class TextField(QGroupBox):

    showPlaceholder = Signal()
    valueChanged = Signal(object)
    updatePopupPosition = Signal()
    createMenu = Signal()
    renderSearchMenuItems = Signal(object)
    
    updateStyleSheet = Signal(object)

    VALID_COLORS = ['primary', 'secondary', 'error', 'info', 'success', 'warning']
    VALID_MARGINS = ['dense', 'none', 'normal']
    VALID_SIZES = ['medium', 'small']
    VALID_VARIANTS = ['filled', 'outlined', 'standard']

    def __init__(
        self,
        key: str= None,
        autoComplete: Optional[Union[State, bool, str]] = None,
        autoFocus: Optional[Union[State, bool]] = False,
        autoWidth: Optional[Union[State, bool]] = False, # chỉ dùng cho Select
        classes: Optional[Union[State, Dict]] = None,
        color: Optional[Union[State, str]] = "primary",
        defaultOpen: Optional[Union[State, bool]] = False, # chỉ dùng cho Select
        defaultValue: Optional[Union[State, object]] = None,
        disabled: Optional[Union[State, bool]] = False,
        error: Optional[Union[State, bool]] = False,
        FormHelperTextProps: Optional[Union[State, Dict]] = None,
        fullWidth: Optional[Union[State, bool]] = False,
        helperText: Optional[Union[State, str]] = None,
        id: Optional[Union[State, str]] = None,
        InputLabelProps: Optional[Union[State, Dict]] = None,
        inputProps: Optional[Union[State, Dict]] = None,
        InputProps: Optional[Union[State, Dict]] = None,
        inputRef: Optional[Union[State, object]] = None,
        inputValue: Optional[Union[State, object]] = None,
        label: Optional[Union[State, str, Callable]] = None,
        max: Optional[Union[State, int, float]] = None,
        margin: Optional[Union[State, str]] = "none",
        maxRows: Optional[Union[State, int, str]] = None,
        min: Optional[Union[State, int, float]] = None,
        minRows: Optional[Union[State, int, str]] = None,
        multiline: Optional[Union[State, bool]] = False,
        multiple: Optional[Union[State, bool]] = False,
        menuHeight: Optional[Union[State, int]] = 400,
        name: Optional[Union[State, str]] = None,
        getOptionLabel: Optional[Union[State, Callable]] = None,
        open: Optional[Union[State, bool]] = False, # chỉ dùng cho Select
        onOpen: Optional[Union[State, Callable]] = None, # chỉ dùng cho Select
        onClose: Optional[Union[State, Callable]] = None, # chỉ dùng cho Select
        onChange: Optional[Union[State, Callable]] = None,
        onInputChange: Optional[Union[State, Callable]] = None,
        onMousePress: Optional[Union[State, Callable]] = None,
        options: Optional[Union[State, object]] = None,
        hiddenLabel: Optional[Union[State, bool]] = False,
        placeholder: Optional[Union[State, str]] = None,
        required: Optional[Union[State, bool]] = False,
        rows: Optional[Union[State, int, str]] = None,
        select: Optional[Union[State, bool]] = False,
        selected: Optional[Union[State, bool]] = False,
        selectOptions: Optional[Union[State, List]] = None,
        SelectProps: Optional[Union[State, Dict]] = None,
        size: Optional[Union[State, str]] = "medium",
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        step: Optional[Union[State, int, float]] = None,
        renderSelectOptions: Optional[Union[State, Callable]] = None,
        renderOption: Optional[Union[State, Callable]] = None,
        renderValue: Optional[Union[State, Callable]] = None,
        renderTags: Optional[Union[State, Callable]] = None,
        readOnly: Optional[Union[State, bool]] = False, # chỉ dùng cho Select
        type: Optional[Union[State, str]] = "text",
        treeView: Optional[Union[State, bool]] = False,
        value = None,
        variant: Optional[Union[State, str]] = "outlined",
        asynRenderQss: Optional[Union[State, bool]] = False,
        *args, **kwargs
    ) -> None:
        # super().__init__(*args, **kwargs)
        super().__init__()
        
        self._kwargs = {
            **kwargs,
            "variant": variant,
            "size": size,
        }
        
        self._setKwargs(self._kwargs)
        
        self.setObjectName(str(uuid.uuid4()))
        start_time = time.time()

        self._key = key
        
        if self._key == "proxyTypekyyyyyyyyyyyyyyyyy":
            print('ProfileTextField__________________', self._key)

        self._key = key
        self._autoComplete = autoComplete
        self._autoFocus = autoFocus
        self._classes = classes
        self._color = color
        self._defaultValue = defaultValue
        self._disabled = disabled
        self._error = error
        self._FormHelperTextProps = FormHelperTextProps
        self._fullWidth = fullWidth
        self._helperText = helperText
        self._id = id
        self._InputLabelProps = InputLabelProps
        self._inputProps = inputProps
        self._InputProps = InputProps
        self._inputRef = inputRef
        self._inputValue = inputValue
        self._label = label
        self._max = max
        self._margin = margin
        self._maxRows = maxRows
        self._min = min
        self._minRows = minRows
        self._multiline = multiline
        self._multiple = multiple
        self._menuHeight = menuHeight
        self._name = name
        self._getOptionLabel = getOptionLabel
        self._onChange = onChange
        self._onInputChange = onInputChange
        self._onMousePress = onMousePress
        self._options = options
        self._hiddenLabel = hiddenLabel
        self._placeholder = placeholder
        self._required = required
        self._rows = rows
        self._select = select
        self._selected = selected
        self._selectOptions = selectOptions
        self._SelectProps = SelectProps
        self._size = size
        self._slotProps = slotProps
        self._slots = slots
        self._sx = sx
        self._step = step
        self._renderSelectOptions = renderSelectOptions
        self._renderOption = renderOption
        self._renderValue = renderValue
        self._renderTags = renderTags
        self._type = type
        self._treeView = treeView
        self._value = value
        self._variant = variant
        
        self._asynRenderQss = asynRenderQss

        if self._fullWidth:
            if not self._sx:
                self._sx = {}
            self._sx.update({"width": "100%"}) # lý do tại sao đặt ở đây thì fullWidth mới có tác dụng thì chưa rõ

        if self._sx:
            self._setSxDict(self._sx)

        self.__init_ui()
        
        end_time = time.time()
        
        # print("time_loading_textfield___________________________", (end_time - start_time)/0.00013971328735351562)


    def _connect_signals_props(self):
        if isinstance(self._value, State):
            self._value.valueChanged.connect(self._set_data)

    def __init_ui(self):
        self._init_done = False
        self._data = None

        self._connect_signals_props()

        self.theme = useTheme()
        
        i18n.langChanged.connect(self._set_translated_label)

        if self._fullWidth:
            if not self._sx:
                self._sx = {}
            self._sx.update({"width": "100%"})


        self._tagsWidget = None
        self._selected_options = {}
        self._inputFieldHasFocusIn = False


        self._inputField = None
        self._popup = None
        self._popupShowing = False
        self._btnSelect = None

        self._isDateTimeType = self._type == "date" or self._type == "time" or self._type == "date-time" or self._type == "color"

        self._menu = None
        self._menuItems, self._setMenuItems = useState([])
        
        self.renderSearchMenuItems.connect(self._render_search_menu_items)


        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        
        self._focused, self._setFocused = useState(False)
        self._hovered, self._setHovered = useState(False)
        
        self._focused.valueChanged.connect(self._set_focused_prop)

        if self._type == "int":
            self._inputField: PySpinBox = PySpinBox
            # self._inputField.setValue = self._set_spinbox_value
        elif self._type == "float":
            self._inputField: PyDoubleSpinBox = PyDoubleSpinBox
        elif self._type == "date-time":
            self._inputField: PyDateTimeEdit = PyDateTimeEdit
        elif self._type == "date":
            self._inputField: PyDateEdit = PyDateEdit
        elif self._type == "time":
            self._inputField: PyTimeEdit = PyTimeEdit
        else: # email, password, select
            if self._multiline:
                self._inputField: PyPlainTextEdit = PyPlainTextEdit
            elif self._multiple:
                if self._renderTags:
                    self._inputField: PyPlainTextEditMultiple = PyPlainTextEditMultiple
                else:
                    self._inputField: TFLineEdit = TFLineEdit
            else:
                self._inputField: TFLineEdit = TFLineEdit

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
        )


        if self._type == "date":
            self._inputField.dateChanged.connect(self._set_date_picker)
        elif self._type == "time":
            self._inputField.timeChanged.connect(self._set_time_picker)
        elif self._type == "color":
            pass
        elif  self._type == "text" or self._select: # có thể lỗi ở đây
            # chỗ này nhằm mục đích tạo ra tính năng search autocomplete
            self._inputField.textChanged.connect(self._on_text_changed)

        self.layout().addWidget(self._inputField)

        self._setup_input_props()
        self._setupy_input_type()

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
        # self._setStyleSheet()
        if self._asynRenderQss:
            self.updateStyleSheet.connect(self._update_stylesheet)
        else:
            self._setStyleSheet()
        
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
            print('self._selected_options______________', self._selected_options)
            self.tags = self._renderTags(self._selected_options, self.getTagProps)
            # self.tags = self._renderTags(self._defaultValue, self.getTagProps)
            self._setFlowLayout(FlowLayout(self, children=self.tags + [self._inputFieldMultiple]))
            
    def _scheduleSetStyleSheet(self):
        self._setupStyleSheet = asyncio.ensure_future(self._lazy_setStyleSheet())

    async def _lazy_setStyleSheet(self):
        self._setStyleSheet()
        
    def _scheduleSetupSelectMode(self):
        self._setupSelectMode = asyncio.ensure_future(self._lazy_setupSelectMode())

    async def _lazy_setupSelectMode(self):
        self._setup_select_mode()

    def _scheduleCraeteMenu(self):
        self._setupMenu = asyncio.ensure_future(self._lazy_create_menu())

    async def _lazy_create_menu(self):
        self._create_menu()

    def _setup_select_mode(self):
        if self._select:
            self.updatePopupPosition.connect(self._update_popup_position)

            # đặt ở đây để có _selectedKeys truyền cho TFLineEditMultiple => setup placeholder đúng
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
            # self.action_frame.setStyleSheet("border: 1px solid red;")
            # self.setup_action_frame_and_adornment()

            if self._multiple:
                if self._renderTags:
                    self._inputFieldMultiple = TFLineEditMultiple(
                        textField=self,
                        label=self._label,
                        placeholder=self._placeholder, 
                        size=self._size, 
                        selectedKeys=self._selectedKeys,
                        onMouseEnter=self.onMouseEnter,
                        onMouseLeave=self.onMouseLeave,
                        onFocusIn=self.onFocusInMultiple,
                        onFocusOut=self.onFocusOut,
                        onMouseRelease=self.onMouseRelease,
                        onChange=self.onChange,
                    )
                    self._inputFieldMultiple.textChanged.connect(self._on_text_changed)
                    self._inputFieldMultiple.installEventFilter(self)
                    self._flowLayout, self._setFlowLayout = useState(FlowLayout(self, [self._inputFieldMultiple]))
                    self._flow_layout_view = TagsView(content=self._flowLayout)
                    self._flow_layout_view.layout().setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self._inputField.setReadOnly(True)
                    self._inputField.setLayout(QHBoxLayout())
                    self._inputField.layout().setContentsMargins(0,0,54,0)
                    self._inputField.setPlaceholderText("")
                    self._inputField.layout().addWidget(self._flow_layout_view)

                elif self._renderValue:
                    self._inputField.setText(self._renderValue(self._data))

                if isinstance(self._renderOption, State):
                    self._renderOption.valueChanged.connect(self._create_menu)
            else:
                if not self._isDateTimeType and not isinstance(self._inputField, QSpinBox)  and not isinstance(self._inputField, QDoubleSpinBox):
                    pass

            if self._options and not self._getOptionLabel:
                raise AttributeError("Opp!! 'getOptionLabel' is required attribute!")
            
            if self._InputProps and self._InputProps.get("type") == "search":
                self._btn_clear_text= QPushButton()
                self._btn_clear_text.setFixedSize(24, 24)
                self._btn_clear_text.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.CLOSE))
                self._btn_clear_text.setCursor(Qt.PointingHandCursor)
                self._btn_clear_text.clicked.connect(self._on_clear_text)
                self._btn_clear_text.hide()
                hlo_action_frame.addWidget(self._btn_clear_text)
                self._btn_clear_text.hide()
            else:
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
            if self._isDateTimeType:
                self._btnSelect.hide()
                self._btnSelect.setIconSize(QSize(24, 24))
                
            self._btnSelect.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_DOWN))
            self._btnSelect.clicked.connect(self._btn_select_toggle_popup)
            hlo_action_frame.addWidget(self._btnSelect)

            self._inputField.installEventFilter(self)

            if hasattr(self, '_flow_layout_view'):
                self._flow_layout_view.mousePressEvent = self.onMultipleInputFieldClicked
                
            self.setup_action_frame_and_adornment() # cần thiết khi không async setup stylesheet
            
    @classmethod
    def _setSxDict(cls, sx: dict = {}):
        cls.sxDict = sx
        
    @classmethod
    def _setKwargs(cls, kwargs: dict = {}):
        cls.ownerState = kwargs

    @classmethod
    @lru_cache(maxsize=128)
    def _getSxQss(cls, sxStr: str = "", className: str = "TextField"):
        sx_qss = get_qss_style(cls.sxDict, class_name=className)
        return sx_qss
    

    # @timer
    def _setStyleSheet(self):
        theme = useTheme()
        
        if self._multiple:
            MuiAutocomplete_styles = theme.components["MuiAutocomplete"].get("styles")
            MuiAutocomplete_styles_root_multiple_min_height = MuiAutocomplete_styles.get("root")["@multiple"]["min-height"]
            MuiAutocomplete_styles_root_multiple_with_chip_min_height = MuiAutocomplete_styles.get("root")["@multiple"]["@chip"]["min-height"]
            if self._renderTags:
                self.setMinimumHeight(MuiAutocomplete_styles_root_multiple_with_chip_min_height)
            else:
                self.setMinimumHeight(MuiAutocomplete_styles_root_multiple_min_height)
        
        self.setProperty("variant", self._variant)
        
        if not self._data:
            self.setProperty("hasValue", False)
        else:
            self.setProperty("hasValue", True)

        
        if self._renderTags:
            _renderTags = "True"
        else:
            _renderTags = "False"

        if hasattr(self, "styledDict"):
            styledConfig = str(self.styledDict)
        else:
            styledConfig = "TextField"
            
        stylesheet = self._getStylesheet(styledConfig, self._variant, self._size, theme.palette.mode, str(self._multiple), str(self._multiline), _renderTags, str(self._focused.value))
        
        sxQss = ""
        if self._sx:
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")
            # sxQss = self._getSxQss(sxStr=str(self._sx), className=f"TextField")
        
        stylesheet = f"""
            {stylesheet}
            {sxQss}
        """

        self.setStyleSheet(stylesheet)


    @classmethod
    @lru_cache(maxsize=128)
    def _getStylesheet(cls, styledConfig: str, _variant: str, _size: str, _theme_mode: str, _multiple: str, _multiline: str, _renderTags:str, _focused: str):
        """Set the stylesheet for the Box."""
        
        theme = useTheme()
        if hasattr(cls, "styledDict"):
            themeComponent = deep_merge(theme.components, cls.styledDict)
        else:
            themeComponent = theme.components
            
        # print("getttttttttttttttttttttttttttttttttttt..................")

        # Chung cho toàn bộ input
        MuiInput = themeComponent["MuiInput"].get("styles")
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
        MuiInput_inputField_prop_filledVariant_size_qss = ""
        if _variant == "filled":
            MuiInput_inputField_prop_filledVariant_size_qss = get_qss_style(MuiInput_inputField["props"]["filledVariant"][_size])

        MuiInputSize = themeComponent["MuiInputSize"]["styles"][f"{_size}"]
        MuiInputSize_qss = get_qss_style(MuiInputSize)

        MuiInputSize_not_multiple_qss = get_qss_style(MuiInputSize["no-multiple"])
        MuiInputSize_no_multiple_height = MuiInputSize["no-multiple"]["height"]

        # thiết lập tuỳ theo variant
        MuiVariantInput = themeComponent[f"Mui{_variant.capitalize()}Input"].get("styles")
        MuiVariantInput_root = MuiVariantInput.get("root")
        MuiVariantInput_root_qss = get_qss_style(MuiVariantInput_root)
        MuiVariantInput_root_slot_hovered_qss = get_qss_style(MuiVariantInput_root["slots"]["hover"])
        MuiVariantInput_root_slot_focused_qss = get_qss_style(MuiVariantInput_root["slots"]["focus"])
        
        MuiVariantInput_inputField_root = MuiVariantInput.get("inputField")["root"]
        MuiVariantInput_inputField_root_qss = get_qss_style(MuiVariantInput_inputField_root)

        MuiVariantInput_root_prop_hasStartAdornment_qss = ""
        if MuiVariantInput_inputField_root.get("props"):
            MuiVariantInput_root_prop_hasStartAdornment_qss = get_qss_style(MuiVariantInput_inputField_root["props"]["hasStartAdornment"])

        MuiInputSize = themeComponent["MuiInputSize"]["styles"][f"{_size}"]
        MuiInputSize_qss = get_qss_style(MuiInputSize)
        
        MuiFilledInput_title_qss = ""
        if _variant == "filled":
            MuiFilledInput_title_qss = get_qss_style(MuiVariantInput["title"])

        # print('MuiInputSize_qss______________', MuiInputSize_qss)

        _________object_name_______ = "_________object_name_______"


        input_base_stylesheet = f"""
                TextField {{
                    {MuiInput_root_qss}
                    {MuiInputSize_qss}
                    {MuiInputSize_not_multiple_qss if not (_multiple=="True" and _renderTags=="True") and not _multiline=="True" else ""}
                }}

                TextField QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QFontComboBox,
                QLineEdit, QPlainTextEdit, QSpinBox, QTextEdit, QTimeEdit {{
                    {MuiInput_inputField_qss}
                }}
                TextField[multipleHasValue=true] QPlainTextEdit {{
                    {MuiInput_inputField_prop_multiple_qss}
                }}
                TextField QPlainTextEdit, QTextEdit{{
                    {MuiInput_inputField_prop_multiline_qss}
                }}
                TextField QPlainTextEdit{{
                    min-height: 40px;
                }}
                TextField::title {{
                    {MuiInput_title_qss}
                    {MuiFilledInput_title_qss}
                }}
                TextField[focused=true]::title {{
                    {MuiInput_title_slot_focused_qss}
                }}
                TextField[error=true]::title {{
                    {MuiInput_title_slot_error_qss}
                }}
                TextField[disabled=true]::title {{
                    {MuiInput_title_slot_disabled_qss}
                }}
            """

        _variant_stylesheet = f"""
                TextField[variant={_variant}] {{
                    {MuiVariantInput_root_qss}
                    {MuiInputSize_qss}
                }}
                TextField[variant={_variant}]  QLineEdit, QPlainTextEdit, QTextEdit {{
                    {MuiVariantInput_inputField_root_qss}
                }}
                TextField[outlinedHasStartAdornment=true]  QLineEdit, QPlainTextEdit, QTextEdit {{
                    {MuiVariantInput_root_prop_hasStartAdornment_qss}
                }}
                TextField[hovered=true] {{
                    {MuiVariantInput_root_slot_hovered_qss}
                }}
                TextField[focused=true] {{
                    {MuiVariantInput_root_slot_focused_qss}
                }}
                TextField[focused=true] QLineEdit, QPlainTextEdit, QTextEdit {{
                    {MuiInput_inputField_prop_filledVariant_size_qss}
                }}
                TextField[hasValue=true] QLineEdit, QPlainTextEdit, QTextEdit {{
                    {MuiInput_inputField_prop_filledVariant_size_qss}
                }}
            """
        
        return input_base_stylesheet + _variant_stylesheet

    def _render_stylesheet(self):
        _theme_mode = useTheme().palette.mode
        self.setProperty("variant", self._variant)
        if self._renderTags:
            _renderTags = "True"
        else:
            _renderTags = "False"

        stylesheet = self._getStylesheet(self._variant, self._size, _theme_mode, str(self._multiple), str(self._multiline), _renderTags )
        
        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx
                
        self.updateStyleSheet.emit(stylesheet + sx_qss)

    def _update_stylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)

    def _create_menu(self):
        print("_create_menu called")

        if not self._menu:
            self._menu = Menu(
                maxHeight=self._menuHeight,
                children=self._menuItems
            )

        if isinstance(self._renderOption, State): # dành cho Select, option được tạo luôn khi gọi renderOption
            if isinstance(self._renderOption.value, Callable):
                self._selectOptions = self._renderOption.value()
                for option in self._selectOptions:
                    if isinstance(option, Li):
                        option._set_selected_keys(self._selectedKeys)
                        option._set_on_changed(self._selected_change)

        elif self._selectOptions and len(self._selectOptions) and isinstance(self._selectOptions[0], QWidget):
            for option in self._selectOptions:
                if isinstance(option, MenuItem):
                    if hasattr(self, '_selectedKeys'):
                        option._set_selected_keys(self._selectedKeys)
                    option._set_on_changed(self._selected_change)

        elif self._options:
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
      
            
    def onFocusIn(self, event=None):
        self._setFocused(True)
        self._show_label()

        if hasattr(self, '_inputFieldMultiple'):
                self._inputFieldMultiple.setFocus(Qt.OtherFocusReason)
            
    def onFocusInMultiple(self, event=None):
        self.onFocusIn(event)

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
        
        if hasattr(self, '_inputFieldMultiple') and QApplication.widgetAt(QCursor.pos()) is self._inputFieldMultiple:
            try:
                QTimer.singleShot(0, lambda: self._inputFieldMultiple.setFocus(Qt.OtherFocusReason))
            except Exception as e:
                print(f"Error setting focus: {e}")
            return
        
        self._setFocused(False)
        print('onFocusOut______________77777777777_______')
        

        # nếu inputValue hiện tại không nằm trong options thì clear nó đi
        if self._select:
            if self._multiple:
                if len(self._selectedKeys.value) == 0:
                    self._inputFieldMultiple.setText("")
                    self._inputFieldMultiple._set_placer_holder_text()
                    self._hide_label()
            else:
                if isinstance(self._inputField, TFLineEdit):
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
                    if isinstance(self._inputField, TFLineEdit):
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

        # if self._data is None:
        if not self._data:
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
        if self._onMousePress:
            self._onMousePress()
        if self._select:
            if not self._isDateTimeType and not isinstance(self._inputField, QPlainTextEdit):
                if self._inputField.selectedText() != "":
                    return

    def onMultipleInputFieldClicked(self, event=None):
        if self._onMousePress:
            self._onMousePress()
        if self._select:
            if not self._isDateTimeType and not isinstance(self._inputField, QPlainTextEdit):
                if self._inputField.selectedText() != "":
                    return
            self._toggle_popup()

    def onChange(self, value=None):
        # nếu là select thì chưa set_value
        if not self._select:
            self._set_data(value, setText=False)


    def _set_state(self, stateValue: dict):
        value = stateValue.get("value")
        state = stateValue.get("state")

    def _set_data(self, value=None, valueChanged=True, setText=True):
        
        _selected_options = self._selected_options.copy()
        
        for key, val in _selected_options.items():
            if isinstance(value, list) and val not in value:
                del self._selected_options[key]
                
        if isinstance(value, State):
            self._data = value.value
        else:
            self._data = value

        if self._type == "int":
            pass
        if self._type == "int": # PySpinBox
            pass
        elif self._type == "float":
            pass
        elif self._type == "date-time":
            pass
        elif self._type == "date":
            pass
        elif self._type == "time":
            pass
        elif self._multiline:
            pass
        elif self._multiple:
            if self._data is not None:
                self._set_multiple_has_value_prop(True)
            else:
                self._set_multiple_has_value_prop(False)

        else: # email, password, select
            pass
            # if self._multiline or self._multiple:
            #     self._inputField = PyPlainTextEdit
            # else: # TFLineEdit
            #     if self._data is not None:
            #         if self._variant == "filled":
            #             self._set_filled_has_value_prop(True) # làm cho inputField padding top 1 khoảng cho giống mui JS
            #     else:
            #         if self._variant == "filled":
            #             self._set_filled_has_value_prop(False) # làm cho inputField padding top 1 khoảng cho giống mui JS

        if value is not None: # value == "" cũng vào đây
            if self._data != "":
                self._show_label()

        if valueChanged:
            self.valueChanged.emit(self._data)

        if setText:
            self._set_text()

    def _set_text(self): # value
        if self._data == None:
            if self._type == "text":
                if isinstance(self._inputField, QPlainTextEdit):
                    self._inputField.setPlainText("")
                elif isinstance(self._inputField, QLineEdit):
                    self._inputField.setText("")
            return
        
        if self._data == "" and not self._select:
            if isinstance(self._inputField, QPlainTextEdit):
                self._inputField.setPlainText("")
            elif isinstance(self._inputField, QLineEdit):
                self._inputField.setText("")
            return

        if self._select:
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
                    self._inputField.setText(self._renderValue(self._data))

        else:
            if self._multiline:
                if isinstance(self._data, dict):
                    if self._getOptionLabel:
                        text = self._getOptionLabel(self._data)
                        self._inputField.setPlainText(text)
                else:
                    self._inputField.setPlainText(str(self._data))
            else:
                if isinstance(self._data, dict):
                    if self._getOptionLabel:
                        text = self._getOptionLabel(self._data)
                        self._inputField.setText(text)
                else:
                    if self._type == "date":
                        if isinstance(self._data, str):
                            with signals_blocked(self._inputField):
                                self._inputField.setDate(QDate.fromString(self._data, self._inputField.displayFormat()))
                        else:
                            self._inputField.setDate(self._data)
                    elif self._type == "time":
                        if isinstance(self._data, str):
                            self._inputField.setTime(QTime.fromString(self._data, self._inputField.displayFormat()))
                        else:
                            self._inputField.setTime(self._data)
                    elif self._type == "int":
                        self._inputField.setValue(int(self._data)) 
                    elif self._type == "float":
                        self._inputField.setValue(float(self._data)) 
                    else:
                        if isinstance(self._inputField, QPlainTextEdit):
                            self._inputField.setPlainText(self._data) 
                        if isinstance(self._inputField, QLineEdit):
                            self._inputField.setText(str(self._data)) 


    def _set_slot(self, data):
        if data.get("slot") == "error":
            self._inputField.setProperty("p-error", "true")
        elif data.get("slot") == "valid":
            self._inputField.setProperty("p-error", "false")

    def _on_text_changed(self, s=None):
        # print("s: ", s)
        
        if not self._init_done:
            return

        # Callback khi input thay đổi. Lấy dữ liệu người dùng gõ tuỳ ý mà chưa cần chọn ngay để kiểm soát hoàn toàn quá trình lọc, reset, hoặc validation.
        if self._onInputChange:
            self._onInputChange(s)

        if not self._autoComplete:
            return
        
        if s is None:
            return
        
        if s == "":
            self._selected_options = {}

        if self._InputProps and self._InputProps.get("type") == "search":
            # thay doi icon clear text
            pass
        
        if self._multiline:
            if self._inputField.toPlainText() == "":
                self._btn_clear_text.hide()
            else:
                self._btn_clear_text.show()
        elif self._multiple:
            if self._inputFieldMultiple.text() == "":
                self._btn_clear_text.hide()
            else:
                self._btn_clear_text.show() 
        else:
            if self._inputField.text() == "":
                self._btn_clear_text.hide()
            else:
                self._btn_clear_text.show() 

        # tìm kiếm các key phù hợp kết quả tìm kiếm
        currentValue = None
        if isinstance(self._data, dict):
            if self._getOptionLabel:
                currentValue = self._getOptionLabel(self._data)
        else:
            currentValue = self._data

        # if s != currentValue and self._InputProps and self._InputProps.get("type") == "search":
        if s != currentValue or s == "" and self._init_done:
            search_options_results = []
            if self._options:
                for option in self._options:
                    if isinstance(option, dict):
                        if self._getOptionLabel:
                            key = self._getOptionLabel(option)
                            if s in key:
                                search_options_results.append(option)
                    else:
                        key = option
                        if s in key:
                            search_options_results.append(option)

            self.renderSearchMenuItems.emit(search_options_results)

        if self._error:
            self._error = None
            
        if self._init_done:
            self._show_popup()

    def _render_search_menu_items(self, search_options_results):
        search_menu_items = []
        if len(search_options_results):
            for _option in search_options_results:
                # props = {'text': self._getOptionLabel(_option)}
                props = {}
                option = self._renderOption(props, _option)
                if isinstance(option, Li):
                    option._set_selected_keys(self._selectedKeys)
                    option._set_on_changed(self._selected_change)
                search_menu_items.append(option)
            if not len(search_menu_items):
                search_menu_items = [Li(key="No options", selected=True, value=">>>>>>No options")]
        else:
            search_menu_items = [Li(text="No options", selected=True, value=">>>>>>No options")]
            
        self._setMenuItems(search_menu_items)

    def validate_type_int(self):
        # Kiểm tra tính hợp lệ của min và max
        if self._min is not None and self._max is not None:
            if not isinstance(self._min, int) or not isinstance(self._max, int):
                raise ValueError("Both 'min' and 'max' must be integers.")
            if self._max < self._min:
                raise ValueError("'max' must be greater than or equal to 'min'.")
        else:
            raise ValueError("Both 'min' and 'max' required.")
        return True

    def _setupy_input_type(self):
        if self._type == "int":
            if self._min:
                if not isinstance(self._min, int):
                    raise ValueError("'min' must be integer.")
                self._inputField.setMinimum(self._min)
            if self._max:
                if not isinstance(self._max, int):
                    raise ValueError("'max' must be integer.")
                self._inputField.setMaximum(self._max)
            if self._min and self._max:
                if self._max < self._min:
                    raise ValueError("'max' must be greater than or equal to 'min'.")
            if self._step:
                if not isinstance(self._step, int):
                    raise ValueError("'step' must be integer.")
                self._inputField.setSingleStep(self._step)
        elif self._type == "float":
            if self._min:
                if not isinstance(self._min, float):
                    raise ValueError("'min' must be float.")
                self._inputField.setMinimum(self._min)
            if self._max:
                if not isinstance(self._max, float):
                    raise ValueError("'max' must be float.")
                self._inputField.setMaximum(self._max)
            if self._min and self._max:
                if self._max < self._min:
                    raise ValueError("'max' must be greater than or equal to 'min'.")
            if self._step:
                if not isinstance(self._step, int) or not isinstance(self._step, float):
                    raise ValueError("'step' must be number (int or float).")
                self._inputField.setSingleStep(self._step)

        elif self._type == "password":
            self._inputField.setEchoMode(QLineEdit.Password) 
        elif self._type == "email":
            pass

    def _set_date_picker(self, date: QDate):
        if isinstance(self.startAdornment, DatePicker) or isinstance(self.startAdornment, ZhDatePicker):
            self.startAdornment.setDate(date)
            self._data = date.toString()
            self.valueChanged.emit(self._data)

    def _set_time_picker(self, time: QTime):
        if isinstance(self.startAdornment, TimePicker) or isinstance(self.startAdornment, AMTimePicker):
            self.startAdornment.setTime(time)
            self._data = time.toString()
            self.valueChanged.emit(self._data)

    def _setup_input_props(self):
        if self._InputProps:
            if self._InputProps.get('startAdornment') and isinstance(self._InputProps.get('startAdornment'), QWidget):
                self.startAdornment = self._InputProps.get('startAdornment')
                self.layout().insertWidget(0, self.startAdornment)
                self._set_prop_has_start_adornment(True)
                self._inputField.setProperty('has-start-adornment', "true")
                if isinstance(self.startAdornment, DatePicker) or isinstance(self.startAdornment, ZhDatePicker):
                    self.startAdornment.dateChanged.connect(self._set_data)
                    if isinstance(self.startAdornment, ZhDatePicker):
                        self._inputField.setDisplayFormat("yyyy/MM/dd")
                    else:
                        self._inputField.setDisplayFormat("dd/MM/yyyy")
                    
                if isinstance(self.startAdornment, AMTimePicker) or isinstance(self.startAdornment, TimePicker):
                    self.startAdornment.timeChanged.connect(self._set_data)
                    if isinstance(self.startAdornment, AMTimePicker):
                        self._inputField.setDisplayFormat(f"hh:mm{'{}'.format(':ss') if self.startAdornment.isSecondVisible() else ''} ap")
                    else:
                        self._inputField.setDisplayFormat(f"hh:mm{'{}'.format(':ss') if self.startAdornment.isSecondVisible() else ''}")

            if self._InputProps.get('endAdornment') and isinstance(self._InputProps.get('endAdornment'), QWidget):
                self.endAdornment = self._InputProps.get('endAdornment')
                self.layout().insertWidget(-1, self.endAdornment)

    def _on_clear_text(self):
        self._onClearText = True

        if self._multiple:
            self._setSelectedKeys([])
            self._btn_clear_text.hide()
            self._selected_options = {}
            self._set_data([])
            self._setFlowLayout(FlowLayout(self, children=[self._inputFieldMultiple]))
        elif self._multiline:
            self._set_data("")
            self._inputField.setPlainText("")
        elif self._type == "date":
            self._set_data(None)
            self._inputField.setDate(QDate.currentDate())
        elif self._type == "time":
            self._set_data(None)
            self._inputField.setTime(QTime.currentTime())
        elif self._type == "int":
            self._set_data(None)
            self._inputField.setValue(0)
        elif self._type == "float":
            self._set_data(None)
            self._inputField.setValue(0.0)
        elif self._select:
            self._set_data(None)
            self._inputField.setText("")
        else: # text, email, password
            self._set_data("")
            self._inputField.setText("")
            
        self._btn_clear_text.hide()
        QTimer.singleShot(0, lambda: self._inputField.setFocus(Qt.OtherFocusReason))
        
        if self._onChange:
            self._onChange(self._data)
            
        if self._onInputChange:
            self._onInputChange("")
        

    def _update_popup_position(self):
        if hasattr(self, "_popup") and self._popup is not None:
            popup_position = self.mapToGlobal(QPoint(0, self.height()))
            self._popup.setGeometry(popup_position.x(), popup_position.y(), self.width(), 50)


    def _hide_popup(self):
        if self._select:
            if self._popup and self._popup.isVisible():
                self._popup.setVisible(False)
            if self._isDateTimeType:
                icon = PyIconify(key=QTMUI_ASSETS.ICONS.CALENDAR)
            else:
                icon = PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_DOWN)

            if self._btnSelect:
                self._btnSelect.setIcon(icon)
        self._popupShowing = False


    def _btn_select_toggle_popup(self, e=None):
        if self._popup and self._popupShowing:
            print('__btn_select_toggle_popup_______________hide_popup')
            self._hide_popup()
        else:
            print('__btn_select_toggle_popup______________show_popup')
            self._show_popup()

    def _toggle_popup(self, e=None):
        if self._select and not self._popupShowing:
            self._show_popup()
            return
        if self._select and (self._data or self._data == "") and self._inputField.hasFocus():
            return
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
            # self._popup.setStyleSheet(f"#{self._popup.objectName()} {{background: transparent;border: 2px solid red;}}")

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

        if self._isDateTimeType:
            icon = PyIconify(key=QTMUI_ASSETS.ICONS.CALENDAR)
        else:
            icon = PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_UP)
        self._btnSelect.setIcon(icon)
        self._popupShowing = True
        

    def _on_menu_item_selected(self, key):
        self._hide_popup()
        self._data = key

    def _about_to_hide(self):
        self._popupShowing = False


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
            self._setFlowLayout(FlowLayout(self, children=self.tags + [self._inputFieldMultiple]))
        else:
            self._selected_options.pop(key)
            self.tags = self._renderTags(self._selected_options, self.getTagProps)
            self._setFlowLayout(FlowLayout(self, children=self.tags + [self._inputFieldMultiple]))

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
        self._setStyleSheet()
        
    def _set_multiple_has_value_prop(self, state):
        self.setProperty("multipleHasValue", state)
        
    def _set_prop_has_start_adornment(self, state:bool):
        self.setProperty("hasStartAdornment", state)

    def setup_action_frame_and_adornment(self):
        if self._InputProps and self._InputProps.get('startAdornment') and isinstance(self._InputProps.get('startAdornment'), QWidget):
            pass
        if self._InputProps and self._InputProps.get('endAdornment') and isinstance(self._InputProps.get('endAdornment'), QWidget):
            pass
        
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
    
    def showEvent(self, event):
        if self._asynRenderQss:
            threading.Thread(target=self._render_stylesheet, args=(), daemon=True).start()
        return super().showEvent(event)
    
    def eventFilter(self, obj, event):
        if self._select:
            if obj == self._inputField or hasattr(self, '_inputFieldMultiple') and obj == self._inputFieldMultiple:
                if event.type() == QEvent.MouseButtonPress:
                    self._show_popup()
            elif self._popup and self._popup.isVisible():
                if event.type() == QEvent.MouseButtonPress and not self.underMouse():
                    if not self._popup.geometry().contains(event.globalPos()):
                        self._hide_popup()
                elif event.type() == QEvent.Wheel and ((not self.underMouse() and not self._popup.underMouse()) or obj == self._inputField):
                    self._hide_popup()
            
        return super().eventFilter(obj, event)

