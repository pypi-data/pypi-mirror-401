import uuid
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QSizePolicy, QLayout, QScrollArea
from PySide6.QtCore import Qt, QRect, QSize, QPoint, QTimer

from ..chip import Chip

class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self.itemList = []

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Horizontal | Qt.Vertical)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        totalHeight = self.doLayout(rect, False)
        self.parentWidget().setMaximumHeight(totalHeight)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def doLayout(self, rect, testOnly):
        x, y, lineHeight = rect.x(), rect.y(), 0
        minLineHeight = 0

        for item in self.itemList:

            wid = item.widget()
            # if type(wid) is QLineEdit:
            #     continue
            nextX = x + item.sizeHint().width() + self.spacing()
            if nextX - self.spacing() > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + self.spacing()
                nextX = x + item.sizeHint().width() + self.spacing()
                lineHeight = 0
            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())
            minLineHeight = max(minLineHeight, item.sizeHint().height())

        totalHeight = y + lineHeight - rect.y()
        return totalHeight

class MultiSelectFrame(QScrollArea):
    def __init__(self, parent=None, maxHeight=None):
        super().__init__(parent)
        self.maxHeight = maxHeight
        self.grandParent = None
        self.setWidgetResizable(True)
        self.container = QFrame()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setSizePolicy(sizePolicy)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy1)
        self.container.setFrameShape(QFrame.StyledPanel)
        self.setWidget(self.container)
        self.layout = FlowLayout(self.container)
        self.container.setLayout(self.layout)
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet('''#{} QWidget  {{ {} }}'''.format(self.objectName(), "border: none;"))
        self.setStyleSheet('''QWidget {{ {} }}'''.format("border: none;"))
        
    def add_widget(self, widget):
        try:
            widget.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
            self.layout.addWidget(widget)
            self.updateSize()
            QTimer.singleShot(500, self.scrollToBottom)
        except Exception as e:
            print('Opp!!! tags -> addLabel ')

    def remove_all_items(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None and widget is not self.lineEdit:
                widget.deleteLater()
        self.updateSize()

    def remove_item(self, label):
        for item in self.findChildren(Chip):
            if item._label == label:
                item.deleteLater()
        self.updateSize()

    def handleDelete(self):
        pass

    def updateSize(self):
        try:
            width = self.viewport().width()
            total_height = self.layout.heightForWidth(width)
            if self.maxHeight is not None and total_height > self.maxHeight:
                total_height = self.maxHeight
            
            max_label_width = max(item.sizeHint().width() for item in self.layout.itemList if item.widget() is not self.lineEdit)
            min_width = max(self.lineEdit.sizeHint().width(), max_label_width)
            
            self.container.setMinimumWidth(min_width)
            self.setMinimumWidth(min_width)
            self.container.setMaximumHeight(total_height)
            self.setMaximumHeight(total_height)
            self.grandParent.setMinimumHeight(total_height + 50)
            
        except Exception as e:
            print('Opp!!! tags -> updateSise')

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateSize()

    def scrollToBottom(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum() + 100)

class CheckboxGroup(QWidget):
    def __init__(self, context=None, children: list = None):
        super().__init__()
        layout = QVBoxLayout(self)

        self.multi_select_frame = MultiSelectFrame(self, maxHeight=200)  # Set the maxHeight here
        layout.addWidget(self.multi_select_frame)

        for checkbox in children:
            self.multi_select_frame.add_widget(checkbox)

        self.setLayout(layout)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Multi-Select Labels with Flow Layout Example')

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.multi_select_frame.updateSize()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     ex.show()
#     sys.exit(app.exec())
