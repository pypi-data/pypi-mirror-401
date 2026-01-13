import uuid
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QApplication
from PySide6.QtGui import QCursor, Qt, QIcon
from PySide6.QtCore import Signal, QSize

from qtmui.material.styles import useTheme
# IMPORT FUNCTIONS
from qtmui.hooks import State
# ///////////////////////////////////////////////////////////////
from  ...common.functions import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from ...common.json_settings import Settings

# IMPORT DIV
# ///////////////////////////////////////////////////////////////
from .py_div import PyDiv

# IMPORT BUTTON
# ///////////////////////////////////////////////////////////////
from .py_title_button import PyTitleButton

# GLOBALS
# ///////////////////////////////////////////////////////////////
_is_maximized = False
_old_size = QSize()

# PY TITLE BAR
# Top bar with move application, maximize, restore, minimize,
# close buttons and extra buttons
# ///////////////////////////////////////////////////////////////
class TitleBar(QFrame):
    # SIGNALS
    clicked = Signal(object)
    released = Signal(object)

    def __init__(
        self,
        logo_image = "logo_top_100x22.svg",
        logo_width = 100,
        buttons = None,
        dark_one = "rgb(249, 249, 249)",
        bgColor = "rgb(249, 249, 249)",
        div_color = "rgb(249, 249, 249)",
        btn_bgColor = "rgb(249, 249, 249)",
        btn_bgColor_hover = "rgb(242, 242, 242)",
        btn_bgColor_pressed = "rgb(242, 242, 242)",
        icon_color = "#c3ccdf",
        icon_color_hover = "#dce1ec",
        icon_color_pressed = "#edf0f5",
        icon_color_active = "#f5f6f9",
        context_color = "#6c99f4",
        text_foreground = "#8a95aa",
        radius = 8,
        font_family = "Segoe UI",
        title_size = 10,
        is_custom_title_bar = True,
        maximumHeight: int = 40,
        children=None
    ):
        super().__init__()

        settings = Settings()
        self.settings = settings.items


        # PARAMETERS
        self._logo_image = logo_image
        self._dark_one = dark_one
        self._bgColor = bgColor
        self._div_color = div_color
        self._btn_bgColor = btn_bgColor
        self._btn_bgColor_hover = btn_bgColor_hover
        self._btn_bgColor_pressed = btn_bgColor_pressed  
        self._context_color = context_color
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._font_family = font_family
        self._title_size = title_size
        self._text_foreground = text_foreground
        self._is_custom_title_bar = is_custom_title_bar
        self._radius = radius

        self.setMaximumHeight(maximumHeight)


        # SETUP UI
        self.setup_ui()

        if bgColor is not None:
            if isinstance(bgColor, State):
                bgColor.valueChanged.connect(self._set_stylesheet)
                self._set_stylesheet(bgColor.value)
            else:
                self._set_stylesheet(background=bgColor)


        # SET LOGO AND WIDTH
        self.top_logo.setMinimumWidth(logo_width)
        self.top_logo.setMaximumWidth(logo_width)
        #self.top_logo.setPixmap(Functions.set_svg_image(logo_image))

        # MOVE WINDOW / MAXIMIZE / RESTORE
        # ///////////////////////////////////////////////////////////////
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if QApplication.instance().mainWindow.isMaximized():
                self.maximize_restore()
                #self.resize(_old_size)
                curso_x = QApplication.instance().mainWindow.pos().x()
                curso_y = event.globalPos().y() - QCursor.pos().y()
                QApplication.instance().mainWindow.move(curso_x, curso_y)
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                QApplication.instance().mainWindow.move(QApplication.instance().mainWindow.pos() + event.globalPos() - QApplication.instance().mainWindow.dragPos)
                QApplication.instance().mainWindow.dragPos = event.globalPos()
                event.accept()

        # MOVE APP WIDGETS
        if is_custom_title_bar:
            self.top_logo.mouseMoveEvent = moveWindow
            self.div_1.mouseMoveEvent = moveWindow
            self.title_label.mouseMoveEvent = moveWindow
            children.mouseMoveEvent = moveWindow
            self.div_2.mouseMoveEvent = moveWindow
            self.div_3.mouseMoveEvent = moveWindow

        # MAXIMIZE / RESTORE
        if is_custom_title_bar:
            self.top_logo.mouseDoubleClickEvent = self.maximize_restore
            self.div_1.mouseDoubleClickEvent = self.maximize_restore
            self.title_label.mouseDoubleClickEvent = self.maximize_restore
            children.mouseDoubleClickEvent = self.maximize_restore
            self.div_2.mouseDoubleClickEvent = self.maximize_restore

        # ADD WIDGETS TO TITLE BAR
        # ///////////////////////////////////////////////////////////////
        # self.bg_layout.addWidget(self.top_logo)
        # self.bg_layout.addWidget(self.div_1)
        self.bg_layout.addWidget(children)
        self.bg_layout.addWidget(self.div_2)

        # ADD BUTTONS BUTTONS
        # ///////////////////////////////////////////////////////////////
        # Functions
        self.minimize_button.released.connect(lambda: QApplication.instance().mainWindow.showMinimized())
        self.maximize_restore_button.released.connect(lambda: self.maximize_restore())
        self.close_button.released.connect(lambda: QApplication.instance().mainWindow.close())

        # Extra BTNs layout
        self.bg_layout.addLayout(self.custom_buttons_layout)

        # ADD Buttons
        if is_custom_title_bar:            
            self.bg_layout.addWidget(self.minimize_button)
            self.bg_layout.addWidget(self.maximize_restore_button)
            self.bg_layout.addWidget(self.close_button)

        # self._autorun_set_theme()

    def _set_stylesheet(self, background=None):
        if isinstance(self._bgColor, State):
            self.bg.setStyleSheet(f"""
                #{self.bg.objectName()} {{
                    background-color: {self._bgColor.value};
                    border-radius: {self._radius}px;
                }}
            """)

        else:
            self.bg.setStyleSheet(f"""
                #{self.bg.objectName()} {{
                    background-color: {self._bgColor};
                    border-radius: {self._radius}px;
                }}
            """)

    # ///////////////////////////////////////////////////////////////
    def add_menus(self, parameters):
        if parameters != None and len(parameters) > 0:
            for parameter in parameters:
                _btn_icon = Functions.set_svg_icon(parameter['btn_icon'])
                _btn_id = parameter['btn_id']
                _btn_tooltip = parameter['btn_tooltip']
                _is_active = parameter['is_active']

                self.menu = PyTitleButton(
                    QApplication.instance().mainWindow,
                    btn_id = _btn_id,
                    tooltip_text = _btn_tooltip,
                    dark_one = self._dark_one,
                    bgColor = self._bgColor,
                    bgColor_hover = self._btn_bgColor_hover,
                    bgColor_pressed = self._btn_bgColor_pressed,
                    icon_color = self._icon_color,
                    icon_color_hover = self._icon_color_active,
                    icon_color_pressed = self._icon_color_pressed,
                    icon_color_active = self._icon_color_active,
                    context_color = self._context_color,
                    text_foreground = self._text_foreground,
                    icon_path = _btn_icon,
                    is_active = _is_active
                )
                self.menu.clicked.connect(self.btn_clicked)
                self.menu.released.connect(self.btn_released)

                # ADD TO LAYOUT
                self.custom_buttons_layout.addWidget(self.menu)

            # ADD DIV
            if self._is_custom_title_bar:
                self.custom_buttons_layout.addWidget(self.div_3)

    # TITLE BAR MENU EMIT SIGNALS
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        self.clicked.emit(self.menu)
    
    def btn_released(self):
        self.released.emit(self.menu)

    # SET TITLE BAR TEXT
    # ///////////////////////////////////////////////////////////////
    def set_title(self, title):
        self.title_label.setText(title)

    # MAXIMIZE / RESTORE
    # maximize and restore parent window
    # ///////////////////////////////////////////////////////////////
    def maximize_restore(self, e = None):
        global _is_maximized
        global _old_size
        
        # CHANGE UI AND RESIZE GRIP
        def change_ui():
            if _is_maximized:
                # QApplication.instance().mainWindow.ui.central_widget_layout.setContentsMargins(0,0,0,0)
                # QApplication.instance().mainWindow.ui.window.set_stylesheet(border_radius = 0, border_size = 0)
                icon = QIcon()
                icon.addFile(u":/title_bar/resource_qtmui/title_bar/icon_restore.svg", QSize(), QIcon.Normal, QIcon.Off)
                self.maximize_restore_button.setIcon(icon)
                # self.maximize_restore_button.set_icon(
                #     Functions.set_svg_icon("icon_restore.svg")
                # )
            else:
                # QApplication.instance().mainWindow.ui.central_widget_layout.setContentsMargins(10,10,10,10)
                # QApplication.instance().mainWindow.ui.window.set_stylesheet(border_radius = 10, border_size = 2)
                icon = QIcon()
                icon.addFile(u":/title_bar/resource_qtmui/title_bar/icon_maximize.svg", QSize(), QIcon.Normal, QIcon.Off) # :/baseline/resource_qtmui/baseline/filter_none.svg
                self.maximize_restore_button.setIcon(icon)
                # self.maximize_restore_button.set_icon(
                #     Functions.set_svg_icon("icon_maximize.svg")
                # )

        # CHECK EVENT
        if QApplication.instance().mainWindow.isMaximized():
            _is_maximized = False
            QApplication.instance().mainWindow.showNormal()
            change_ui()
        else:
            _is_maximized = True
            _old_size = QSize(QApplication.instance().mainWindow.width(), QApplication.instance().mainWindow.height())
            QApplication.instance().mainWindow.showMaximized()
            change_ui()

    # SETUP APP
    # ///////////////////////////////////////////////////////////////
    def setup_ui(self):
        # ADD MENU LAYOUT
        self.title_bar_layout = QVBoxLayout(self)
        self.title_bar_layout.setContentsMargins(0,0,0,0)

        # ADD BG
        self.bg = QFrame()
        self.bg.setObjectName(str(uuid.uuid4()))

        # ADD BG LAYOUT
        self.bg_layout = QHBoxLayout(self.bg)
        self.bg_layout.setContentsMargins(0,0,0,0)
        self.bg_layout.setSpacing(0)

        # DIVS
        self.div_1 = PyDiv(self._div_color)
        self.div_2 = PyDiv(self._div_color)
        self.div_3 = PyDiv(self._div_color)

        # LEFT FRAME WITH MOVE APP
        self.top_logo = QLabel()
        self.top_logo_layout = QVBoxLayout(self.top_logo)
        self.top_logo_layout.setContentsMargins(0,0,0,0)
        # self.logo_svg = QSvgWidget()
        # self.logo_svg.load(Functions.set_svg_image(self._logo_image))
        # self.top_logo_layout.addWidget(self.logo_svg, Qt.AlignCenter, Qt.AlignCenter)

        # TITLE LABEL
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignVCenter)
        self.title_label.setStyleSheet(f'font: {self._title_size}pt "{self._font_family}"')

        # CUSTOM BUTTONS LAYOUT
        self.custom_buttons_layout = QHBoxLayout()
        self.custom_buttons_layout.setContentsMargins(0,0,0,0)
        self.custom_buttons_layout.setSpacing(3)


        # MINIMIZE BUTTON
        self.minimize_button = QPushButton()
        self.minimize_button.setFixedSize(QSize(44, 44))
        icon = QIcon()
        icon.addFile(u":/title_bar/resource_qtmui/title_bar/icon_minimize.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_button.setIcon(icon)
        self.minimize_button.setIconSize(QSize(12, 12))
        self.minimize_button.setStyleSheet("""
            QPushButton  {
                background: transparent;
            }
            QPushButton:hover  {
                background: rgb(237, 237, 237);
            }
        """)

        # MAXIMIZE / RESTORE BUTTON
        self.maximize_restore_button = QPushButton()
        self.maximize_restore_button.setFixedSize(QSize(44, 44))
        icon = QIcon()
        icon.addFile(u":/title_bar/resource_qtmui/title_bar/icon_restore.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.maximize_restore_button.setIcon(icon)
        self.maximize_restore_button.setIconSize(QSize(12, 12))
        self.maximize_restore_button.setStyleSheet("""
            QPushButton  {
                background: transparent;
            }
            QPushButton:hover  {
                background: rgb(237, 237, 237);
            }
        """)
        # CLOSE BUTTON
        self.close_button = QPushButton()
        self.close_button.setFixedSize(QSize(44, 44))
        icon = QIcon()
        icon.addFile(u":/title_bar/resource_qtmui/title_bar/icon_close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.close_button.setIcon(icon)
        self.close_button.setIconSize(QSize(12, 12))
        self.close_button.setStyleSheet("""
            QPushButton  {
                background: transparent;
            }
            QPushButton:hover  {
                background: rgb(250, 192, 192);
            }
        """)
        # ADD TO LAYOUT
        self.title_bar_layout.addWidget(self.bg)

    def _autorun_set_theme(self):
        @store.autorun(lambda state: state.theme)
        def _(theme):
            try:
                self._set_stylesheet()
            except Exception as e:
                print('_autorun_set_theme_tooltip_____', str(e))