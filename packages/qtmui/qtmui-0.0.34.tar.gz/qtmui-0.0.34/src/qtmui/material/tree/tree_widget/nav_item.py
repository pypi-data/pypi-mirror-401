from typing import Callable, Optional
import uuid
from PySide6.QtWidgets import QHBoxLayout, QFrame, QSizePolicy, QPushButton, QSpacerItem
from PySide6.QtCore import  QEvent, QTimer, QPoint, QSize

from qtmui.hooks import State
from ...box import Box
from ...button import Button
from ._accept_drop_frame import AcceptDropFrame
from ...popover import Popover

from ...py_iconify import PyIconify

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ....i18n.use_translation import translate, i18n

from ....qtmui_assets import QTMUI_ASSETS

class NavItem(QFrame):
    def __init__(
            self, 
                ref=None,
                item: object = None,
                depth: int = None,
                open: Optional[State] = False,
                active: bool = False,
                externalLink: str = None,
                onActionButtonClicked: Callable = None,
                onClick: Callable = None,
                onDrop: Callable = None,
                onMouseEnter: Callable = None,
                onMouseLeave: Callable = None,
                config: dict = None,
                popover: object = None,
                child: object = None,
                selected: bool = False
            ):
        super().__init__()
        self._ref = ref
        self._item = item
        self._depth = depth
        self._open = open
        self._active = active
        self._externalLink = externalLink
        self._onMouseEnter = onMouseEnter
        self._onMouseLeave = onMouseLeave
        self._onActionButtonClicked = onActionButtonClicked
        self._onClick = onClick
        self._config = config
        self._popover: Popover = popover
        self._child: Popover = child
        self._selected: bool = selected

        sub_item = depth != 1
        deep_sub_item = depth > 2

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "background: red;"))

        if popover is not None:
            popover.anchorEl = self
            # print(self._item.get("title"))
            self.accept_drop_frame = Button(
                    fullWidth=True,
                    text=self._item.get("title"), 
                    variant="soft", color="primary", 
                    startIcon=self._item.get("icon"), 
                    endIcon=":/baseline/resource_qtmui/baseline/keyboard_arrow_down.svg" 
                )
            self.accept_drop_frame.setMouseTracking(True)
            self.accept_drop_frame.installEventFilter(self)

            if self._item.get("compornentRender") is not None:
                component = self._item.get("compornentRender")["callable"](self._item.get("compornentRender")["data"])
                self.accept_drop_frame.setLayout(QHBoxLayout())
                self.accept_drop_frame.layout().setContentsMargins(0,0,0,0)
                self.accept_drop_frame.layout().addWidget(component)
        else: # child is not None

            self.accept_drop_frame = AcceptDropFrame(startIcon=self._item.get("icon"), depth=depth, selected=self._item.get("selected"), value=self._item.get("id"), onDrop=self._item.get("onDrop"))

            if self._item.get("compornentRender") is not None:
                # print('compornentRender______________________________')
                component = self._item.get("compornentRender")["callable"](self._item.get("compornentRender")["data"])
                self.accept_drop_frame.setLayout(QHBoxLayout())
                self.accept_drop_frame.layout().setContentsMargins(0,0,0,0)
                try:
                    self.accept_drop_frame.layout().addWidget(component)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    # print(component)
            else:


                self.btn_item_text = QPushButton(self._item.get("title"))
                self.btn_item_text.setStyleSheet("text-align: left;background-color: transparent;")

                if self._onClick is not None:
                    self.btn_item_text.clicked.connect(lambda checked, id=self._item.get("id"): onClick(id))
                    self.accept_drop_frame.left_clicked.connect(lambda id=self._item.get("id"): onClick(id))
                
                # active toogle function
                self.btn_item_text.clicked.connect(lambda: self.togle_collapse())
                self.accept_drop_frame.left_clicked.connect(lambda: self.togle_collapse()) 


                # self.btn_item_action = QPushButton("+") # NavItemActionButton
                # self.btn_item_action.setFixedSize(QSize(30, 30))

                # if self._onActionButtonClicked is not None:
                #     self.btn_item_action.clicked.connect(lambda id=self._item.get("id"): onActionButtonClicked(id))
                # else:
                #     self.btn_togle_collapse.hide()
                #     self.btn_item_action.hide()

                # self.accept_drop_frame.btn_more = QPushButton()
                # self.accept_drop_frame.btn_more.setIcon(FluentIconBase().icon_(path=":/IconBold/resources/IconBold/More Square.svg", color=self._theme.grey.grey_500))
                # self.accept_drop_frame.btn_more.setFixedSize(QSize(23, 23))

                # if self._item.get("actionMenuItems") is not None:
                #     self.accept_drop_frame.btn_more.setMenu(
                #         CustomMenu(
                #             parent=self.accept_drop_frame.btn_more,
                #             content=Box(
                #                 direction="column",
                #                 children=[
                #                     Button(text=config.get("label"), variant="soft", value=self._item.get("id"), fullWidth=True, onClick=config.get("action"))
                #                     for config in self._item.get("actionMenuItems")
                #                 ]   
                #             )
                #         )
                #     )

                #     self.accept_drop_frame.btn_more.setContextMenuPolicy(Qt.CustomContextMenu)
                #     self.accept_drop_frame.btn_more.setStyleSheet('''
                #         QPushButton::menu-indicator {{
                #             image: none;
                #             width: 0px;
                #         }}
                #         QPushButton {{
                #             border: none;
                #             background-color: none;              
                #         }}
                #         QPushButton::hover {{
                #             border: none;
                #             background-color: {};              
                #         }}
                #     '''.format(self._theme.action.hover))

                # else:
                #     self.accept_drop_frame.btn_more.setVisible(False)

                self.accept_drop_frame.layout().addWidget(self.btn_item_text)
                
                if self._item.get("info") is not None:
                    # self._item.get("info").setParent(None)
                    self.accept_drop_frame.layout().addWidget(self._item.get("info")['component'](**self._item.get("info")['props']))
                    # self.accept_drop_frame.layout().addWidget(Label(text=f'3', color="error"))

                self.accept_drop_frame.layout().addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

                # print('self._item.getaction_____________', self._item.get("action"))
                if self._item.get("action") is not None:
                    # self._item.get("info").setParent(None)
                    # self.accept_drop_frame.layout().addWidget(self._item.get("action")['component'](**self._item.get("action")['renderProps'](self._item.get("action")['options'])))
                    self.accept_drop_frame.layout().addWidget(self._item.get("action")['renderAction'](self._item.get("action")))

                if self._child:
                    if not self._item.get("disableToggle"):
                        self.btn_togle_collapse = QPushButton()
                        self.btn_togle_collapse.setFixedSize(QSize(30, 30))
                        self.btn_togle_collapse.clicked.connect(lambda: self.togle_collapse())
                        self.accept_drop_frame.layout().addWidget(self.btn_togle_collapse)

                        if self._selected:
                            icon = PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_UP)
                            self.btn_togle_collapse.setIcon(icon)
                        else:
                            self.btn_togle_collapse.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_RIGHT))

        
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        self.layout().addWidget(
            Box(
                direction="column",
                children=[
                    self.accept_drop_frame,
                    self._child if self._child is not None else None
                ]
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

        PyTreeWidgetItem_root_qss = get_qss_style(component_styles["PyTreeWidgetItem"].get("styles")["root"])

    def togle_collapse(self):
        if self._child is not None:
            self._open.valueChanged.emit(self._open.value)
            if self._open.value:
                # self._child.hide()
                # self._open.dataChanged.emit(False)
                icon = PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_RIGHT)
                self.btn_togle_collapse.setIcon(icon)
            else:
                # self._child.show()
                # self._open.dataChanged.emit(True)
                icon = PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_UP)
                self.btn_togle_collapse.setIcon(icon)

    def eventFilter(self, source, event):
        if self._popover is None:
            return super().eventFilter(source, event)

        if source == self.button:
            if event.type() == QEvent.Enter:
                pos = self.button.mapToGlobal(QPoint(0, self.button.height()))
                rect = self.button.geometry()
                self._popover.showTooltip(pos, rect)
            elif event.type() == QEvent.Leave:
                if not self._popover.underMouse():
                    QTimer.singleShot(100, self.check_cursor)
        return super().eventFilter(source, event)

    def check_cursor(self):
        if self._popover is None:
            return
        
        if not self._popover.underMouse() and not self.button.underMouse():
            self._popover.hideTooltip()