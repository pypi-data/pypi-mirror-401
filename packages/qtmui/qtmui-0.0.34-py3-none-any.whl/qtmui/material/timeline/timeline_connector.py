import uuid
from PySide6.QtWidgets import QFrame, QHBoxLayout
from PySide6.QtCore import Qt
from typing import Union, List, Callable

from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..widget_base import PyWidgetBase

from ..divider import Divider

class TimelineConnector(QFrame, PyWidgetBase):
    def __init__(self,
                 align: str = 'inherit',  # Căn chỉnh văn bản trên component, mặc định là 'inherit'
                 children=None,  # Nội dung của component (node)
                 classes: dict = None,  # Ghi đè hoặc mở rộng các styles áp dụng cho component (dict)
                 color: Union[str, None] = 'textPrimary',  # Màu sắc của component, có thể là một màu tùy chỉnh
                 component: str = 'div',  # Phần tử HTML hoặc component root được sử dụng
                 gutterBottom: bool = False,  # Nếu true, văn bản sẽ có một margin ở dưới
                 noWrap: bool = False,  # Nếu true, văn bản sẽ không xuống dòng, mà sẽ cắt và thêm dấu '...' nếu quá dài
                 paragraph: bool = False,  # Thuộc tính bị deprecated, nếu true, phần tử sẽ là một phần tử paragraph
                 sx: Union[List[Union[Callable, dict, bool]], Callable, dict] = None,  # Thuộc tính hệ thống, thêm CSS bổ sung
                 variant: str = 'body1',  # Áp dụng các kiểu typography theo theme
                 variantMapping: dict = None  # Ánh xạ thuộc tính variant thành các kiểu phần tử HTML tương ứng
                 ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))

        self._align = align
        self._children = children
        self._classes = classes if classes is not None else {}
        self._color = color
        self._component = component
        self._gutterBottom = gutterBottom
        self._noWrap = noWrap
        self._paragraph = paragraph
        self._sx = sx if sx is not None else []
        self._variant = variant
        self._variantMapping = variantMapping if variantMapping is not None else {
            'h1': 'h1', 'h2': 'h2', 'h3': 'h3', 'h4': 'h4', 'h5': 'h5', 'h6': 'h6',
            'subtitle1': 'h6', 'subtitle2': 'h6', 'body1': 'p', 'body2': 'p', 'inherit': 'p'
        }


        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)

        self._init_ui()

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _init_ui(self):
        """Khởi tạo giao diện của TimelineConnector."""
        self.setFixedHeight(40)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(Qt.AlignCenter)

        self.layout().addWidget(Divider(orientation="vertical"))

    def retranslateUi(self):
       pass

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        if self._color == "textPrimary":
            self._label_color = self.theme.palette.text.primary
        else:
            self._label_color = self.theme.components["PyTimeLine"]["styles"]["connector"][self._color]["color"]

    def _getAlignment(self, align: str) -> Qt.AlignmentFlag:
        """Trả về căn chỉnh tương ứng cho QLabel."""
        alignment_mapping = {
            'center': Qt.AlignCenter,
            'inherit': Qt.AlignLeft,  # 'inherit' mặc định là trái
            'justify': Qt.AlignJustify,
            'left': Qt.AlignLeft,
            'right': Qt.AlignRight
        }
        return alignment_mapping.get(align, Qt.AlignLeft)


