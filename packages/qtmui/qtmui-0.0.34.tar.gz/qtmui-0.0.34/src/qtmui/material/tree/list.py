import uuid
import sys
from PySide6.QtWidgets import QApplication, QListView, QVBoxLayout, QWidget, QStyledItemDelegate, QLabel, QListWidget, QListWidgetItem, QStyle
from PySide6.QtCore import QStringListModel, Qt, QSize
from PySide6.QtGui import QPainter, QColor, QBrush

from ..button import Button

class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Custom paint code
        painter.save()

        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(QColor("#a8d5e2")))  # Background color when selected
        else:
            painter.setBrush(QBrush(QColor("#e2f0f4")))  # Default background color

        painter.drawRect(option.rect)
        
        text = index.data(Qt.DisplayRole)
        painter.setPen(QColor("#333333"))
        painter.drawText(option.rect, Qt.AlignLeft | Qt.AlignVCenter, text)

        painter.restore()

    # def sizeHint(self, option, index):
    #     # Custom size hint
    #     return QSize(200, 40)

class List(QWidget):
    def __init__(
                self, 
                subheader=None, 
                data=None, 
                sx: dict = None, 
                direction: str = None, 
                disablePadding: bool = None, 
                parent=None
                ):
        super().__init__(parent)


        self.subheader = subheader
        self.data = data
        self.sx = sx
        self.sx = sx
        self.direction = direction
        self.disablePadding = disablePadding
        self.list_view = None

        self.initUi()

    def initUi(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet('''#{}  {{ {} }};'''.format(self.objectName(), "background: pink;"))
        # self.setStyleSheet("""
        #     QListView {
        #         background-color: pink;
        #         border: 0px solid #dddddd;
        #     }
        #     QListView::item {
        #         padding: 10px;
        #         margin: 5px;
        #     }
        #     QListView::item:selected {
        #         background-color: #a8d5e2;
        #         color: #ffffff;
        #     }
        # """)

        # if not self.subheader:
        #     self.list_view = QListView()
        #     self.layout().addWidget(self.list_view)

        if isinstance(self.data, list):
            if all(isinstance(item, str) for item in self.data):
                self.setStringData(self.data)
            elif all(isinstance(item, QWidget) for item in self.data):
                self.setWidgetData(self.data)

    def setStringData(self, data):
        self.model = QStringListModel()
        self.model.setStringList(data)
        self.list_view.setModel(self.model)

    def setWidgetData(self, data):
        if not self.subheader:
            # self.widget_list = QListWidget()
            # for widget in data:
            #     item = QListWidgetItem(self.widget_list)
            #     self.widget_list.setItemWidget(item, widget)
            # layout = QVBoxLayout(self.list_view)
            # self.list_view.setItemDelegate(CustomDelegate(self))
            # layout.addWidget(self.widget_list)
            # self.list_view.setLayout(layout)

            for widget in data:
                self.layout().addWidget(widget)
        else:
            # add subheader
            # self.layout().addWidget(Button(text=self.subheader, variant="soft", color="primary", onClick=self.toogle_collapse))
            self.layout().addWidget(self.subheader)
            # add content widget
            for widget in data:
                self.layout().addWidget(widget)

    def toogle_collapse(self):
        pass


