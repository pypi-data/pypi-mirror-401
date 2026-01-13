import asyncio
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QWidget, QScrollArea, QSizePolicy, QApplication, QLabel
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QRunnable, QTimer, QThreadPool
import uuid

from qtmui.hooks import State

class WidgetSetter(QRunnable):
    def __init__(self, cls, children):
        super().__init__()
        self.cls= cls
        self.children=children

    async def run(self):
        for index, widget in enumerate(self.children):
            await asyncio.sleep(0.1)
            # print(f"add widget {index} before: ", self.cls.widgetContents.height())
            self.cls.vlayout.addWidget(widget)
            self.cls.widgetContents.adjustSize()
            self.cls.scroll_area.widget().adjustSize()
            self.cls.adjustSize()
            self.cls.scroll_area.setFixedHeight(self.cls.widgetContents.height())
            self.cls.setFixedHeight(self.cls.widgetContents.height())
            self.cls.parent().setFixedHeight(self.cls.widgetContents.height())
            self.cls.widgetContents.parent().setFixedHeight(self.cls.widgetContents.height())
            self.cls.parent().parent().setFixedHeight(self.cls.widgetContents.height())
            self.cls.adjustSize()
            self.cls.parent().adjustSize()
            self.cls.parent().updateGeometry()
            self.cls.updateGeometry()
            self.cls.scroll_area.adjustSize()
            self.cls.scroll_area.updateGeometry()
            print('self.cls', self.cls.widgetContents.parent().height(), self.cls.scroll_area.height(), self.cls.parent().height(), self.cls.height(), self.cls.scroll_area.widget().height(), self.cls.parent().parent().height())
            # print(f"add widget {index} after: ", self.cls.widgetContents.height())

    
class MenuScrollArea(QFrame):

    def __init__(self,  
                sx: dict = None,
                maxWidth: int = None,
                defaultWidth: int = None,
                hightLight: bool = None,
                backgroundColor: str = None,
                children: list = None,
                fullWidth: bool = False,
                spacing=6,
                border: str = '',
                borderForNav: bool = None,
        ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(spacing)
        self._border = border
        
        # self._thread_pool = QThreadPool.globalInstance()  # Sử dụng thread pool toàn cục
        
        self.scroll_area = QScrollArea(self)
        self.layout().addWidget(self.scroll_area)

        self.scroll_area.setWidgetResizable(True)
        self.widgetContents = QWidget(self.scroll_area)

        self.vlayout = QVBoxLayout(self.widgetContents)
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setSpacing(3)
        
        self.scroll_area.setWidget(self.widgetContents)
            

        if backgroundColor is not None:
            if isinstance(backgroundColor, State):
                backgroundColor.valueChanged.connect(self._set_background)
                self._set_background(backgroundColor.value)
            else:
                self._set_background(background=backgroundColor)

        if maxWidth is not None:
            self.setMaximumWidth(maxWidth)

        if defaultWidth is not None:
            self.resize(defaultWidth, self.height())

        if isinstance(children, list) and len(children) > 0:
            for item in children:
                if isinstance(item, QWidget):
                    self.vlayout.addWidget(item)
                    # self._add_child_fast(item)
                    # print('itemmmmmmmmmmmmm', item)

        # self.worker = WidgetSetter(self, children)
        # self._thread_pool.start(QTimer.singleShot(0, lambda: asyncio.ensure_future(self.worker.run())))


        if fullWidth:
            self.setFullWidth()

        # self.installEventFilter(self)
        self._set_stylesheet()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

    def _add_child_fast(self, widget):
        self._thread_pool.start(QTimer.singleShot(0, lambda widget=widget: asyncio.ensure_future(self.worker.run())))  # Chạy setIndexWidget trong thread riêng

    def _set_stylesheet(self):
        # print('_set_background__________container', background)
        # print('_set_background___________border', self._border)
        self.setStyleSheet(f"""

            QWidget {{
                background-color: transparent;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: rgb(249, 249, 249);
                height: 4px;
                margin: 0px 21px 0 21px;
                border-radius: 0px;
            }}

            QScrollBar::handle:horizontal {{
                background: rgb(227, 227, 227);
                min-width: 25px;
                border-radius: 0px
            }}

            QScrollBar::add-line:horizontal {{
                border: none;
                background: rgb(227, 227, 227);
                width: 20px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }}

            QScrollBar::sub-line:horizontal {{
                border: none;
                background: transparent;
                width: 20px;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }}

            QScrollBar::up-arrow:horizontal,
            QScrollBar::down-arrow:horizontal {{
                background: none;
            }}

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {{
                background: none;
            }}

            QScrollBar:vertical {{
                border: none;
                background: rgb(249, 249, 249);
                width: 4px;
                margin: 21px 0 21px 0;
                border-radius: 0px;
            }}

            QScrollBar::handle:vertical {{
                background: rgb(227, 227, 227);
                min-height: 25px;
                border-radius: 0px;
            }}


            QScrollBar::add-line:vertical {{
                border: none;
                background: transparent;
                height: 20px;
                border-bottom-left-radius: 0px; 
                border-bottom-right-radius: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}

            QScrollBar::sub-line:vertical {{
                border: none;
                background: transparent;
                height: 20px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}

            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {{
                background: none;
            }}

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)

    def _set_background(self, background):
        self.setStyleSheet(self.styleSheet() + f"""
            #{self.objectName()} {{
                background-color: {background};
                {self._border}
            }}
        """)


    def setFullWidth(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(0)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.Resize:
    #         self.adjustWidth()
    #     return super().eventFilter(obj, event)

    def adjustWidth(self):
        screen_size = QGuiApplication.primaryScreen().size()
        screen_width = screen_size.width()
        if screen_width < 576:
            self.setMaximumWidth(screen_width)
        elif screen_width < 768:
            self.setMaximumWidth(540)
        elif screen_width < 992:
            self.setMaximumWidth(720)
        elif screen_width < 1200:
            self.setMaximumWidth(960)
        elif screen_width < 1400:
            self.setMaximumWidth(1140)
        else:
            self.setMaximumWidth(1320)