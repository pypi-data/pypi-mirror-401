from typing import Callable
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QFrame, QToolButton
from PySide6.QtCore import  QSize
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QFont, QBrush


class StyledItem(QWidget):
    def __init__(self, active=False, depth=1, config=None, theme=None, parent=None):
        super().__init__(parent)
        self.active = active
        self.depth = depth
        self.config = config
        self.theme = theme
        self.initUI()

    def initUI(self):
        self.setMinimumHeight(self.config['itemRootHeight'])
        self.setStyleSheet(f'''
            background-color: {"rgba(25, 118, 210, 0.08)" if self.active else "transparent"};
            border-radius: {self.config['itemRadius']}px;
            padding: {self.config['itemPadding']};
            margin-bottom: {self.config['itemGap']}px;
            color: {"#1976d2" if self.active else "#6b7280"};
        ''')

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.active:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(25, 118, 210, 40)))
            painter.drawRoundedRect(self.rect(), self.config['itemRadius'], self.config['itemRadius'])
            painter.end()

class StyledIcon(QToolButton):
    def __init__(self, size=24, parent=None):
        super().__init__(parent)
        self.size = size
        self.initUI()

    def initUI(self):
        self.setFixedSize(QSize(self.size, self.size))
        self.setStyleSheet(f'''
            width: {self.size}px;
            height: {self.size}px;
            align-items: center;
            justify-content: center;
        ''')

class StyledDotIcon(QFrame):
    def __init__(self, active=False, parent=None):
        super().__init__(parent)
        self.active = active
        self.initUI()

    def initUI(self):
        self.setFixedSize(QSize(4, 4))
        self.setStyleSheet(f'''
            background-color: {"#1976d2" if self.active else "#9e9e9e"};
            border-radius: 50%;
        ''')

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.active:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(25, 118, 210)))
            painter.drawEllipse(self.rect())
            painter.end()

class StyledSubheader(QLabel):
    def __init__(
            self, 
            text=None, 
            theme=None, 
            parent=None,
            disableGutters=True,
            disableSticky=True,
            onClick: Callable = None,
            config=None
            ):
        super().__init__(text, parent)
        import uuid
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "background: pink;"))
        self._text = text
        self._config = config
        self._theme = theme
        self._click = onClick
        
        self.initUI()

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self._click()
        return super().mousePressEvent(ev)

    def initUI(self):
        # self.setLayout(QHBoxLayout())
        # self.layout().addWidget(
        #     Box(
        #         direction="row",
        #         children=[
        #             Buton
        #         ]
        #     )
        # )
        self.setText(self._text)
        self.setFont(QFont('Arial', 11, QFont.Bold))
        self.setStyleSheet(f'''
            padding: {self._config['itemPadding']};
            color: {"#9e9e9e"};
            margin-bottom: {self._config['itemGap']}px;
            padding-bottom: 4px;
        ''')

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Example usage of StyledItem
        item_config = {
            'itemGap': 4,
            'itemPadding': '4px 8px 4px 12px',
            'itemRadius': 8,
            'itemRootHeight': 44,
        }

        theme = None  # You can define your theme here

        item = StyledItem(active=True, depth=1, config=item_config, theme=theme)
        layout.addWidget(item)

        # Example usage of StyledIcon
        icon = StyledIcon(size=24)
        layout.addWidget(icon)

        # Example usage of StyledDotIcon
        dot_icon = StyledDotIcon(active=True)
        layout.addWidget(dot_icon)

        # Example usage of StyledSubheader
        subheader = StyledSubheader("Subheader", config=item_config, theme=theme)
        layout.addWidget(subheader)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Styled Widgets Example')
        self.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec())
