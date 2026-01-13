from PySide6.QtWidgets import QApplication, QFrame, QLabel, QVBoxLayout, QWidget, QSizePolicy, QLineEdit, QLayout, QLayoutItem, QScrollArea, QPushButton
from PySide6.QtCore import Qt, QRect, QSize, QPoint, QTimer

class FlowLayout(QLayout):
    def __init__(
                self, 
                parent=None, 
                children=None, 
                margin=0, 
                hSpacing=10, 
                vSpacing=10, 
                alignment=Qt.AlignLeft
                ):
        super().__init__(parent)
        self.itemList = []
        self._children = children
        self.m_hSpace = hSpacing
        self.m_vSpace = vSpacing
        self.alignment = alignment
        self.setContentsMargins(margin, margin, margin, margin)

        if self._children:
            for widget in self._children:
                self.addWidget(widget)

    def __del__(self):
        while self.itemList:
            item = self.itemList.pop()
            item.widget().deleteLater()

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
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
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(2 * margins.top(), 2 * margins.top())
        return size

    def doLayout(self, rect, testOnly):
        x, y, lineHeight = rect.x(), rect.y(), 0
        spaceX, spaceY = self.m_hSpace, self.m_vSpace
        available_width = rect.width()
        row_items = []

        for item in self.itemList:
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                self._alignItems(row_items, available_width, x, y, rect)
                row_items.clear()
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0
            if not testOnly:
                row_items.append(item)
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        if row_items:
            self._alignItems(row_items, available_width, x, y, rect)

        return y + lineHeight - rect.y()

    def _alignItems(self, row_items, available_width, start_x, y, rect):
        total_item_width = sum(item.sizeHint().width() for item in row_items)
        space_between_items = self.m_hSpace * (len(row_items) - 1)
        row_width = total_item_width + space_between_items
        align_x = start_x

        if self.alignment == Qt.AlignCenter:
            align_x = rect.x() + (available_width - row_width) / 2
        elif self.alignment == Qt.AlignRight:
            align_x = rect.x() + available_width - row_width

        for item in row_items:
            item.setGeometry(QRect(QPoint(align_x, y), item.sizeHint()))
            align_x += item.sizeHint().width() + self.m_hSpace

# Example widget that uses the FlowLayout
class FlowWidget(QWidget):
    def __init__(
                self,
                parent=None,
                children=None
                ):
        super().__init__(parent)
        self.layout = FlowLayout(parent=self,alignment=Qt.AlignCenter)
        if children:
            for widget in children:
                self.layout.addWidget(widget)


