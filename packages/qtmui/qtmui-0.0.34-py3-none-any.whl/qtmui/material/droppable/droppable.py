from typing import Callable, Optional, List, Union, Dict
import uuid
from PySide6.QtCore import QEvent, QModelIndex, Qt, QPersistentModelIndex, QTimer, Signal, QSize
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QFrame, QVBoxLayout, QWidget

from qtmui.hooks import State
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

# https://stackoverflow.com/questions/37797342/pyqt5-mousetracking-not-working

class Droppable(QFrame):
    right_clicked = Signal()
    left_clicked = Signal()
    double_clicked = Signal()
    
    def __init__(
            self, 
            onDrop: Callable = None, 
            onDragMove: Callable = None, 
            children: Optional[Union[State, List]] = None,
            sx: Optional[Union[State, Dict, Callable, str]] = None,
                 
        ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.timeout)

        # self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self._sx = sx
        
        self._children = children

        self.is_double = False
        self.is_left_click = True

        self.btn_more = None

        self.theme = useTheme()

        self.installEventFilter(self)

        self._last_index = QPersistentModelIndex()
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.last_drop_row = None

        self._onDrop = onDrop

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(6)
        
        if self._children:
          if isinstance(self._children, State):
            if self._children.value:
              self.layout().addWidget(self._children.value)
          elif isinstance(self._children, list):
            for child in self._children:
                if isinstance(child, QWidget):
                    self.layout().addWidget(child)
              
        self._set_stylesheet()

    def enterEvent(self, event):
        if isinstance(self.btn_more, QPushButton):
          self.btn_more.setVisible(True)

    def leaveEvent(self, event):
        if isinstance(self.btn_more, QPushButton):
          self.btn_more.setVisible(False)

    def mouseReleaseEvent(self, event):
      # self._parent._on_nav_item_clicked()
      return super().mouseReleaseEvent(event)

    # def eventFilter(self, obj, event):
    #     try:
    #         index = self._last_index  # Biến index được sử dụng làm tham chiếu.
            
    #         # Kiểm tra sự kiện chuột nhấn.
    #         if event.type() == QEvent.MouseButtonPress:
    #             if not self.timer.isActive():
    #                 self.timer.start()
                
    #             self.is_left_click = (event.button() == Qt.LeftButton)
    #             return True  # Bắt sự kiện, không chuyển tiếp.

    #         # Kiểm tra sự kiện chuột nhấn đúp.
    #         elif event.type() == QEvent.MouseButtonDblClick:
    #             self.is_double = True
    #             return True  # Bắt sự kiện, không chuyển tiếp.

    #         # Kiểm tra sự kiện chuột di chuyển.
    #         elif event.type() == QEvent.MouseMove:
    #             index = event.pos()

    #         # Kiểm tra chuột rời khỏi vùng.
    #         elif event.type() == QEvent.Leave:
    #             index = QModelIndex()

    #         # Chuột nhả nút.
    #         elif event.type() == QEvent.MouseButtonRelease:
    #             index = QModelIndex()

    #         # Kéo rời khỏi vùng.
    #         elif event.type() == QEvent.DragLeave:
    #             self.setStyleSheet(
    #                 "QFrame::hover"
    #                 "{"
    #                 "color: #6b6b6b;"
    #                 "background-color: rgba(237, 237, 237, 0.8);"
    #                 "}"
    #                 "QFrame"
    #                 "{"
    #                 "background-color: transparent;"
    #                 "border: none;"
    #                 "}"
    #             )

    #         # Kéo di chuyển bên trong vùng.
    #         elif event.type() == QEvent.DragMove:
    #             pass

    #     except Exception as e:
    #         print(f"Error in eventFilter: {e}")
        
    #     # Không bắt sự kiện, chuyển tiếp đến đối tượng gốc.
    #     return False

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
      
    def dragLeaveEvent(self, event):
      # self.setStyleSheet(
      #   "QFrame::hover"
      #   "{"
      #   "color: #6b6b6b;"
      #   "background-color: rgba(237, 237, 237,0.8);"
      #   "}"
      #   'QFrame'
      #   "{"
      #   'background-color: transparent;'
      #   'border: none;'
      #   "}")
      self.setStyleSheet(
          f"""
              #{self.objectName()} {{
                  background-color: transparent;
              }}
              #{self.objectName()}::hover {{
                  background-color: rgba(237, 237, 237,0.8);
              }}
          """)
      return super().dragLeaveEvent(event)

    def dragMoveEvent(self, event):
      index = event.pos()
      if index != self._last_index:
        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    background-color: transparent;
                }}
                #{self.objectName()}::hover {{
                    background-color: rgba(217, 217, 217,0.6);
                }}
            """)
      return super().dragMoveEvent(event)

    def dropEvent(self, event):
      sender = event.source()
      super().dropEvent(event)

    #   selectedRows = sender.getselectedRowsFast()
      
      # #print('selectedRows_____________')
      
      # model = sender.model()

      # arr_id_profile = []
      # for srow in selectedRows:
      #   id = model.index(srow, 1).data()
      #   arr_id_profile.append(int(id))
      
      print("profile______drop_______", sender, "to group")

      self._onDrop(sender)

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



    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx)
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx)
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx
                
        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {sx_qss}
                }}
            """
        )