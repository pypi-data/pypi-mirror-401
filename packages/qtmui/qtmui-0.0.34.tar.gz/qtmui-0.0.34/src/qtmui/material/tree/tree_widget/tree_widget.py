from typing import Union, Callable
import uuid
from PySide6.QtWidgets import QFrame, QHBoxLayout
from PySide6.QtCore import Signal

from qtmui.hooks import useState

from ...stack import Stack

from ...collapse import Collapse

from ..list import List
from .nav_list import NavList
from .styles import StyledSubheader

from qtmui.qss_name import *

from ..config import navVerticalConfig
from .tree_model import TreeModel

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ....i18n.use_translation import translate, i18n

styles = """
        #{} {{
            border: {};
            margin: {};
            font-weight: {};
            line-height: {};
            font-size: {};
            font-family: {};
            padding: {};
            border-radius: {};
            color:  {};
            background-color: {};
        }}
        #{}::hover {{
            background-color: {};
        }}

"""


class TreeWidget(QFrame):

    dataModelChangedSignal = Signal(bool)

    """
    props: AdditionalProps & {
        /**
        * The Toolbar children, usually a mixture of `IconButton`, `Button` and `Typography`.
        * The Toolbar is a flex container, allowing flex item properties to be used to lay out the children.
        */
        children?: React.ReactNode;
        /**
        * Override or extend the styles applied to the component.
        */
        classes?: Partial<ToolbarClasses>;
        /**
        * If `true`, disables gutter padding.
        * @default false
        */
        disableGutters?: boolean;
        /**
        * The variant to use.
        * @default 'regular'
        */
        variant?: OverridableStringUnion<'regular' | 'dense', ToolbarPropsVariantOverrides>;
        /**
        * The system prop that allows defining system overrides as well as additional CSS styles.
        */
        sx?: SxProps<Theme>;
    };
    defaultComponent: DefaultComponent;
    """
    def __init__(self,
                model: TreeModel = None,
                config: bool = None,
                sx: dict = None,
                children: list = None,
                contentsMargins: int = 0,
                borderLeft: int = None,
                 *args, 
                 **kwargs
                 ):
        super(TreeWidget, self).__init__( *args, **kwargs)


        self._width = width

        self.setObjectName(str(uuid.uuid4()))
        if borderLeft:
            self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), f"border: 0px solid transparent;border-radius: {borderLeft}px;"))
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        # if self._width:
        #     self.setFixedWidth(self._width)
        # self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)

        self._model = model
        self._config = config
        self._sx = sx
        self._children = children

        if model:
            self._model.dataChanged.connect(self.initUI)
            self.initUI()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

        i18n.langChanged.connect(self.reTranslation)
        self.reTranslation()

    def reTranslation(self):
        pass
         
    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        PyTreeWidget_root_qss = get_qss_style(component_styles["PyTreeWidget"].get("styles")["root"])


    def initUI(self):
        self.clear_layouts()
        
        self.layout().addWidget(
            Stack(
                direction="column",
                
                sx={},
                children=list(
                    map(
                        lambda group, index: 
                        Group(
                            open=group.get("open"),
                            key=group.get("subheader", index),
                            items=group["items"],
                            config=navVerticalConfig(self._config)
                        ), 
                        self._model._data, range(len(self._model._data))
                    )
                )
            )
        )

    def clear_layouts(self):
        # Xóa tất cả các widget trong QHBoxLayout
        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

class Group(QFrame):
    def __init__(
            self, 
            key=None, 
            open: bool = False, 
            items: Union[dict, list] = None, 
            config: object = None
            ):
        super().__init__()

        self._key = key
        self._subheader = key
        # self._subheader = None
        self._items = items
        self._config = config

        self._open, self._setOpen = useState(open)

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet('''#{}  {{ {} }};'''.format(self.objectName(), "background: green;"))
        # self.layout().addWidget(QPushButton('kjlkjlkjlkjlk'))
        self.layout().addWidget(
            List(
                disablePadding=True,
                sx={ px: 2 },
                subheader=StyledSubheader(
                    disableGutters=True,
                    disableSticky=True,
                    onClick=self.handleToggle,
                    config=config,
                    text=self._subheader # self._subheader
                )   if self._subheader else None,
                data=[
                    Collapse(isIn=self._open, showToogleButton=False, children=self.renderContent())
                ]   if self._subheader else self.renderContent()
            )
        )

    def handleToggle(self):
        self._setOpen(not self._open)

    def renderContent(self):
        return  [
            NavList(
                key=item["title"] + item["path"],
                data=item,
                depth=1,
                hasChild=bool(item.get("children")),
                config=self._config
            )
            for item in self._items
        ]

