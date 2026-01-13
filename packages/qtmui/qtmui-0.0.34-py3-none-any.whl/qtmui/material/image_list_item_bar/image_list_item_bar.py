# src/qtmui/material/image_list_item_bar.py
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

class ImageListItemBar(QFrame):
    def __init__(
        self,
        title: str = "",
        subtitle: str = None,
        actionIcon=None,           # QWidget (ví dụ IconButton)
        actionPosition: str = "right",  # "left" | "right"
        position: str = "bottom",       # "top" | "bottom" | "below"
        sx: dict = None,
        **kwargs
    ):
        super().__init__()
        self.position = position.lower()
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Layout chính
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        # Action icon (nếu có)
        if actionIcon:
            if actionPosition == "left":
                layout.addWidget(actionIcon)
                layout.addStretch()
            else:
                layout.addStretch()
                layout.addWidget(actionIcon)

        # Text container
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: white; font-weight: 600; font-size: 14px;")
        text_layout.addWidget(self.title_label)

        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 12px;")
            text_layout.addWidget(self.subtitle_label)

        layout.insertLayout(1 if actionPosition == "left" else 0, text_layout)

        # Áp dụng style theo position
        if position in ["top", "bottom"]:
            self.setStyleSheet(f"""
                ImageListItemBar {{
                    background: linear-gradient(to top, 
                        rgba(0,0,0,0.7) 0%, 
                        rgba(0,0,0,0.4) 50%, 
                        transparent 100%);
                    border-radius: {'0 0 8px 8px' if position == 'bottom' else '8px 8px 0 0'};
                }}
            """)
        elif position == "below":
            self.setStyleSheet("""
                ImageListItemBar {
                    background: transparent;
                    padding: 8px 0;
                }
                QLabel { color: rgba(0,0,0,0.87); }
            """)