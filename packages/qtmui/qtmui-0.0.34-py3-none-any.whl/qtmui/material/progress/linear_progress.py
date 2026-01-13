from typing import Optional, Union, Callable, Dict

from PySide6.QtWidgets import QFrame, QHBoxLayout

from .linear_indeterminate import LinearIndeterminate
from .linear_query import LinearQuery
from .linear_determinate import LinearDeterminate
from .linear_buffer import LinearBuffer

class LinearProgress(QFrame):
    """
        /**
        * Override or extend the styles applied to the component.
        */
        classes?: Partial<LinearProgressClasses>;
        /**
        * The color of the component.
        * It supports both default and custom theme colors, which can be added as shown in the
        * [palette customization guide](https://mui.com/material-ui/customization/palette/#adding-new-colors).
        * @default 'primary'
        */
        color?: OverridableStringUnion<
            'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning' | 'inherit',
            LinearProgressPropsColorOverrides
        >;
        /**
        * The system prop that allows defining system overrides as well as additional CSS styles.
        */
        sx?: SxProps<Theme>;
        /**
        * The value of the progress indicator for the determinate and buffer variants.
        * Value between 0 and 100.
        */
        value?: number;
        /**
        * The value for the buffer variant.
        * Value between 0 and 100.
        */
        valueBuffer?: number;
        /**
        * The variant to use.
        * Use indeterminate or query when there is no progress value.
        * @default 'indeterminate'
        */
        variant?: 'determinate' | 'indeterminate' | 'buffer' | 'query';
    """
    def __init__(self, 
                key: str = None, 
                value: int = None, 
                variant: str = None,
                color: str = None,
                sx: Optional[Union[Callable, str, Dict]]= None
        ):
        super().__init__()

        self._key = key
        self._value = value
        self._variant = variant
        self._color = color
        self._sx = sx
        self._buffer = 10

        self._init_ui()

    def _init_ui(self):
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        if self._variant == "determinate":
            self.layout().addWidget(LinearDeterminate(value=self._value, key=self._key, color=self._color))
        elif self._variant == "indeterminate":
            self.layout().addWidget(LinearIndeterminate(key=self._key, color=self._color))
        elif self._variant == "buffer":
            self.layout().addWidget(LinearBuffer(key=self._key, color=self._color, value=self._value, buffer=self._buffer))
        elif self._variant == "query":
            self.layout().addWidget(LinearQuery(key=self._key, color=self._color))
        else:
            self.layout().addWidget(LinearProgressIndeterminateNomal(key=self._key, color=self._color))
    
         
