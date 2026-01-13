
from ..material.grips import Grips

class AppGrips:
    def __init__(self, context):
        self._context = context
        self._hide_grips = True

    def setup_gui(self):
        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        self.left_grip = Grips(self._context, "left", self._hide_grips)
        self.right_grip = Grips(self._context, "right", self._hide_grips)
        self.top_grip = Grips(self._context, "top", self._hide_grips)
        self.bottom_grip = Grips(self._context, "bottom", self._hide_grips)
        self.top_left_grip = Grips(self._context, "top_left", self._hide_grips)
        self.top_right_grip = Grips(self._context, "top_right", self._hide_grips)
        self.bottom_left_grip = Grips(self._context, "bottom_left", self._hide_grips)
        self.bottom_right_grip = Grips(self._context, "bottom_right", self._hide_grips)


    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        self.left_grip.setGeometry(0, 10, 10, self._context.height())
        self.right_grip.setGeometry(self._context.width() - 10, 10, 10, self._context.height())
        self.top_grip.setGeometry(5, 0, self._context.width() - 10, 10)
        self.bottom_grip.setGeometry(5, self._context.height() - 10, self._context.width() - 10, 10)
        self.top_right_grip.setGeometry(self._context.width() - 20, 5, 15, 15)
        self.bottom_left_grip.setGeometry(5, self._context.height() - 20, 15, 15)
        self.bottom_right_grip.setGeometry(self._context.width() - 20, self._context.height() - 20, 15, 15)