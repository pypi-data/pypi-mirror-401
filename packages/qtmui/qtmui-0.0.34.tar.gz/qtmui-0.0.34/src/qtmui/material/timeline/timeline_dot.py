import uuid
from PySide6.QtWidgets import QVBoxLayout, QFrame
from typing import Union, List, Callable

from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor
from ..avatar import Avatar

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..widget_base import PyWidgetBase

class TimelineDot(QFrame, PyWidgetBase):
    def __init__(self,
                 children=None,  # Nội dung của component (node)
                 classes: dict = None,  # Ghi đè hoặc mở rộng các styles áp dụng cho component (dict)
                 color: Union[str, None] = 'default',  # Màu sắc của dot, mặc định là 'grey'
                 sx: Union[List[Union[Callable, dict, bool]], Callable, dict] = None,  # Thuộc tính hệ thống, thêm CSS bổ sung (array | func | object)
                 variant: str = 'filled'  # Kiểu của dot, có thể là 'filled' hoặc 'outlined', mặc định là 'filled'
                 ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet(f"#{self.objectName()} {{background-color: yellow;}}")

        self._children = children
        self._classes = classes if classes is not None else {}
        self._color = color
        self._sx = sx if sx is not None else []
        self._variant = variant



        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()
        
        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)

        # Khởi tạo giao diện của dot
        self._init_ui()

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()


    def _init_ui(self):
        """Khởi tạo giao diện của TimelineItem."""
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)


        if not self._children:
            self.layout().addWidget(Avatar(size=13, text=" ", color=self._dot_color))
        else:
            self._add_children()

    def retranslateUi(self):
       pass

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        if self._color == None:
            self._dot_color = self.theme.palette.grey._500
        elif self._color.find("#") == -1 and self._color in ['primary', 'secondary', 'info', 'success', 'warning', 'error']:
            self._dot_color = component_styled["PyTimeLine"]["styles"]["dot"][self._color]["color"]
        else:
            self._dot_color = self._color


    def _add_children(self):
        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            for child in self._children:
                if child:
                    self.layout().addWidget(child)