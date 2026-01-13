from qtmui.material.styles import useTheme
from PySide6.QtWidgets import QHBoxLayout, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from ..styles.create_theme.components.get_qss_styles import get_qss_style

from ..py_svg_widget import PySvgWidget
from ..widget_base.widget_base import PyWidgetBase


class ListItemIcon(QFrame, PyWidgetBase):
    def __init__(self, 
                 children=None,
                 **kwargs
                ):
        super().__init__(**kwargs)
        # self.setObjectName("PyListItemIcon")
        self._setUpUi()

        # Gán các prop thành thuộc tính của class
        self.kwargs = kwargs

        self._children = children

        self._init_ui()

        self.theme = useTheme()
        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self.destroyed.connect(self._on_destroyed)
        self._set_stylesheet()


    def _init_ui(self):

        # Layout cơ bản cho icon
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # self.setFixedWidth(24)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True) # Điều này cho phép các sự kiện chuột (bao gồm hover) có thể đi qua và được lắng nghe bởi QPushButton.
        self.theme = useTheme()

        # Thêm các children (nếu có)
        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            for child in self._children:
                self.layout().addWidget(child)
        else:
            # self.layout().addWidget(PySvgWidget(color=self.theme.palette.primary.main, **self.kwargs))
            self.layout().addWidget(PySvgWidget(**self.kwargs))


    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()
        self._update_component_styles(self.theme, component_styled)

        ownerState = {
            **self.kwargs
        }

        # print('________00000000000', self.styleFn(self.theme))

        PyListItemIcon_root = self.component_styles[f"PyListItemIcon"].get("styles")["root"](ownerState)
        PyListItemIcon_root_qss = get_qss_style(PyListItemIcon_root)


        self.setStyleSheet(
            f"""
                ListItemIcon {{
                    {PyListItemIcon_root_qss}
                }}
            """
        )
        
        
        
