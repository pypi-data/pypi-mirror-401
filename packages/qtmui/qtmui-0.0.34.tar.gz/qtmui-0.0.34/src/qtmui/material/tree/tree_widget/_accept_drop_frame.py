from typing import Callable
from PySide6.QtWidgets import QFrame, QPushButton
from PySide6.QtCore import QEvent, QModelIndex, Qt, QPersistentModelIndex, QTimer, Signal, QSize
from PySide6.QtWidgets import QPushButton, QHBoxLayout

from ...py_tool_button.py_tool_button import PyToolButton
from qtmui.material.styles import useTheme


# https://stackoverflow.com/questions/37797342/pyqt5-mousetracking-not-working

class AcceptDropFrame(QFrame):
    right_clicked = Signal()
    left_clicked = Signal()
    double_clicked = Signal()
    
    def __init__(self, 
                 depth=0,
                 startIcon: PyToolButton = None,
                 selected=False, 
                 onDrop: Callable = None, 
                 value=None):
        super(AcceptDropFrame, self).__init__()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.timeout)

        self._value = value

        theme = useTheme()

        if selected:
          self.setStyleSheet('''
            QFrame {{
              border: 0px solid transparent;
              background-color: {};
              border-radius: 7px;
            }}
            QFrame::hover {{
              background-color: {};
            }}
          '''.format(theme.palette.action.hover, theme.palette.action.hover))
        else:
          self.setStyleSheet('''
            QFrame {{
              border: 0px solid transparent;
              background-color: transparent;
              border-radius: 7px;
            }}
            QFrame::hover {{
              background-color: {};
            }}
          '''.format(theme.palette.action.hover))


        self.is_double = False
        self.is_left_click = True

        self.btn_more = None

        self.installEventFilter(self)

        self._last_index = QPersistentModelIndex()
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.last_drop_row = None

        self._onDrop = onDrop

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(6+9*depth,6,6,6)
        # self.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layout().setSpacing(6)
        self.setFixedHeight(40)

        if startIcon:
          if isinstance(startIcon, dict):
            self.layout().addWidget(startIcon.get("component")(**startIcon.get("props")))

        if depth > 1:
          self.layout().addWidget(PyToolButton(icon=":/baseline/resource_qtmui/baseline/circle.svg", iconSize=QSize(8,8),  fillColor="#888888"))



    def enterEvent(self, event):
        if isinstance(self.btn_more, QPushButton):
          self.btn_more.setVisible(True)

    def leaveEvent(self, event):
        if isinstance(self.btn_more, QPushButton):
          self.btn_more.setVisible(False)


    def eventFilter(self, obj, event):
      index = self._last_index
      if event.type() == QEvent.MouseButtonPress:
        if not self.timer.isActive():
          self.timer.start()

        self.is_left_click = False
        if event.button() == Qt.LeftButton:
          self.is_left_click = True

        return True

      elif event.type() == QEvent.MouseButtonDblClick:
        self.is_double = True
        return True

      if event.type() == QEvent.MouseMove:
        index = event.pos()
      elif event.type() == QEvent.Leave:
        index = QModelIndex()
      elif event.type() == QEvent.MouseButtonRelease:
        index = QModelIndex()
      elif event.type() == QEvent.DragLeave:
        self.setStyleSheet(
          "QFrame::hover"
          "{"
          "color: #6b6b6b;"
          "background-color: rgba(237, 237, 237,0.8);"
          "}"
          'QFrame'
          "{"
          'background-color: transparent;'
          'border: none;'
          "}")

      elif event.type() == QEvent.DragMove:
        pass
      return False

    def timeout(self):
      if self.is_double:
        self.double_clicked.emit()
      else:
        if self.is_left_click:
          self.left_clicked.emit()
        else:
          self.right_clicked.emit()

      self.is_double = False

    def left_click_event(self):
      #print('left clicked')
      pass

    def right_click_event(self):
      #print('right clicked')
      pass

    def double_click_event(self):
      btn = self.sender()
      btnName = btn.objectName()
      #print('double clicked')

    def dragEnterEvent(self, e):
      e.accept()

    def dragMoveEvent(self, event):
      index = event.pos()
      if index != self._last_index:
        self.setStyleSheet(
          "QFrame::hover"
          "{"
          "color: #6b6b6b;"
          "background-color: rgba(237, 237, 237,0.8);"
          "}"
          'QFrame'
          "{"
          'background-color: transparent;'
          'border: none;'
          "}")

    def dropEvent(self, event):
      sender = event.source()
      super().dropEvent(event)

      # selectedRows = sender.getselectedRowsFast()
      
      # #print('selectedRows_____________')
      
      # model = sender.model()

      # arr_id_profile = []
      # for srow in selectedRows:
      #   id = model.index(srow, 1).data()
      #   arr_id_profile.append(int(id))
      
      print("profile______drop_______", sender, "to group", self._value)

      self._onDrop({
        "sender": sender,
        "target": self._value
      })



      self.setStyleSheet(
        "QFrame::hover"
        "{"
        "color: #6b6b6b;"
        "background-color: rgba(237, 237, 237,0.8);"
        "}"
        'QFrame'
        "{"
        'background-color: transparent;'
        'border: none;'
        "}")