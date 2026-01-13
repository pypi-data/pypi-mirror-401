from typing import Callable
from PySide6.QtWidgets import QToolButton, QColorDialog, QDialogButtonBox, QGridLayout, QSpinBox
from PySide6.QtCore import Slot, Qt

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n

class ColorPicker(QToolButton):

    def __init__(
            self,
            tooltip: str = None,
            onChange: Callable = None
    ):
        super().__init__()

        self._tooltip = tooltip
        self._onChange = onChange
        self._dialog_color = QColorDialog(self)

        self.initUI()
        i18n.langChanged.connect(self.reTranslation)
        self.reTranslation()
    
    def initUI(self):
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self.on_click)
        self._set_color()

        theme = useTheme()
        theme.state.valueChanged.connect(self._set_theme)
        self._set_theme()

    def reTranslation(self):
        if self._tooltip:
            if isinstance(self._tooltip, Callable):
                self.setToolTip(translate(self._tooltip))
            else:
                self.setToolTip(self._tooltip)

    def _set_color(self, color=None):
        theme = useTheme()
        self.setStyleSheet(f"margin-left: 8px;border: 0px solid transparent;border-radius: 2px;background-color: {color or theme.palette.grey._500};")

    def _set_theme(self):
        theme = useTheme()

        # self._dialog_color.setOption(QColorDialog.ShowAlphaChannel)

        grid = self._dialog_color.findChild(QGridLayout)
        # print('grid____________________', grid)
        names = iter(('hue', 'sat', 'val', 'red', 'green', 'blue', 'alpha'))
        for i in range(grid.count()):
            item = grid.itemAt(i)
            widget = item.widget()
            if isinstance(widget, QSpinBox):
                widget.setStyleSheet('background: red;')
                widget.setObjectName(next(names))

        # alternatively:
        #spins = dialog.findChildren(QtWidgets.QSpinBox)
        #names = 'hue', 'sat', 'val', 'red', 'green', 'blue', 'alpha'
        #for name, spin in zip(names, spins):
        #    spin.setObjectName(name)

        buttonBox = self._dialog_color.findChild(QDialogButtonBox)
        buttonBox.button(QDialogButtonBox.Ok).setObjectName('ok')
        buttonBox.button(QDialogButtonBox.Cancel).setObjectName('cancel')

        self._dialog_color.setStyleSheet(f'''
            /* the HTML color line edit */
            QColorDialog {{
                background: yellow;
            }}
            QLineEdit {{
                background: yellow;
            }}

            /* the spin boxes */
            QSpinBox#hue {{
                background: coral;
            }}
            QSpinBox#sat {{
                background: orange;
            }}
            QSpinBox#val {{
                background: lightgray;
            }}
            QSpinBox#red {{
                background: orangered;
            }}
            QSpinBox#green {{
                background: lime;
            }}
            QSpinBox#blue {{
                background: aqua;
            }}
            QSpinBox#alpha {{
                background: pink;
            }}

            /* buttons that are children of QDialogButtonBox */
            QDialogButtonBox QAbstractButton#ok {{
                background: green;
            }}
            QDialogButtonBox QAbstractButton#cancel {{
                background: red;
            }}
            ''')

        # self._dialog_color.setStyleSheet(
        #     f"""
        #         QColorPicker {{
        #             background-color: rgb(6, 6, 14);
        #         }}
        #         QPushButton {{
        #             color: rgb(211, 213, 201); 
        #             background-color: rgb(36, 36, 44);
        #         }}
        #         QLabel {{
        #             color: rgb(211, 213, 201); 
        #             background-color: rgb(6, 6, 14);
        #         }}
        #         QLineEdit {{
        #             color: rgb(211, 213, 201); 
        #             background-color: rgb(36, 36, 44);
        #         }}
        #         QSpinBox {{
        #             color: rgb(211, 213, 201); 
        #             background-color: rgb(36, 36, 44);
        #         }}
        #     """
        # )

    @Slot()
    def on_click(self):
        self.openColorDialog()
        self._set_theme()

    def openColorDialog(self):
        color = self._dialog_color.getColor()

        if color.isValid():
            print(color.name())
            self._onChange(color.name())
            self._set_color(color.name())


