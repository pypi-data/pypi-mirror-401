import uuid
from PySide6.QtWidgets import QHBoxLayout, QFrame
from PySide6.QtCore import QTimer

from qtmui.hooks import useState
from ...box import Box

from .nav_item import NavItem
from ...stack import Stack
from ...collapse import Collapse

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ....i18n.use_translation import translate, i18n

class NavRef:
    def __init__(self):
        self.current = None


class NavList(QFrame):
    def __init__(
            self, 
            key, 
            data, 
            depth, 
            hasChild, 
            config,
            ):
        super().__init__()
        self._key = key
        self._data = data
        self._depth = depth
        self._hasChild = hasChild
        self._config = config

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "background: pink;"))

        self._navRef = NavRef()
        self._open, self._setOpen = useState(not self._data.get('open'))
        self._active = False
        self._externalLink = "lin/link"
        # self._nav_item._popover = None

        self.layout().addWidget(
            Box(
                direction="column",
                children=[self.createNavItem()]
            )
        )

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

        PyTreeWidgetList_root_qss = get_qss_style(component_styles["PyTreeWidgetList"].get("styles")["root"])

    def createNavItem(self):
        # print('0000000_____________________', self._data.get('onClick'))
        self._nav_item =NavItem(
            ref=self._navRef,
            item=self._data,
            depth=self._depth,
            open=self._open,
            onActionButtonClicked=self._data.get('onActionButtonClicked'),
            # onClick=self._data.get('onClick'),
            onClick=self.handleToggle,
            onDrop=self._data.get('onDrop'),
            active=self._active,
            externalLink=self._externalLink,
            onMouseEnter=self.handleOpen,
            onMouseLeave=self.handleClose,
            config=self._config,
            child=self.createCollapse() if self._hasChild else None
        )
        return self._nav_item

    def handleToggle(self, data=None):
        self._setOpen(not self._open.value)
        if self._data.get('onClick'):
            self._data.get('onClick')(self._data.get('id'))

    def createCollapse(self):
        collapse = Collapse(
            isIn=self._open,
            showToogleButton=False,
            unmountOnExit=True,
            child=NavSubList(data=self._data.get('children'),  depth=self._depth, config=self._config)
        )
        return collapse

    def handleOpen(self):
        self._open = True
        if self._nav_item._popover:
            self._nav_item._popover.show()

    def handleClose(self):
        if not self._nav_item._popover or not self._nav_item._popover.underMouse():
            self._open = False
            if self._nav_item._popover:
                QTimer.singleShot(100, self.checkNavRef)

    def checkNavRef(self):
        for item in self._nav_item._popover.navSubList._children:
            if item._nav_item._popover is not None:
                if item._nav_item._popover.isVisible() or self._nav_item._popover.underMouse():
                    # item._nav_item._popover.setStyleSheet('border: 1px solid red;')
                    return QTimer.singleShot(100, self.checkNavRef)
        self._nav_item._popover.hide()
        

def NavSubList(data, depth, config):
    return Stack(
        direction="column",
        spacing=1,
        children=[
            NavList(
                key=_list["title"] + _list["path"],
                data=_list,
                depth=depth + 1,
                hasChild=bool(_list.get("children")),
                config=config
            ) 
            for _list in data
        ]
    )
