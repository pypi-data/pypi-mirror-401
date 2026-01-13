from PySide6.QtWidgets import QLayout, QHBoxLayout, QVBoxLayout, QWidget

def clear_layout(layout: QLayout | QHBoxLayout | QVBoxLayout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        
        if widget is not None:
            widget.deleteLater()
            
