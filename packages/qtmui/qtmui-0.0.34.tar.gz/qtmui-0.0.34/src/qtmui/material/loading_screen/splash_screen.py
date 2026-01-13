from PySide6.QtWidgets import QFrame, QHBoxLayout

from ..stack import Stack
from ..progress import CircularProgress, LinearProgress

class SplashScreen(QFrame):
    def __init__(
            self,
            variant: str = "circular", # linear
            color: str = "default"
    ):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(
            Stack(
                # hFlexCenter=True,
                # layoutAlignHCenter=True,
                children=[
                    CircularProgress(
                        key="color", 
                        color=color
                    ) if variant == "circular"
                    else LinearProgress(
                        key="color", 
                        color=color    
                    )
                ]
            )
        )

