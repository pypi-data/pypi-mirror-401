from typing import Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QFrame



class Controller(QFrame):
    """
    Controller

    Args:
        name                FieldPath	✓	    Unique name of your input.
        control             Control		        control object is from invoking useForm. Optional when using FormProvider.
        render              Function		    This is a render prop. A function that returns a React element and provides the ability to attach events and value into the component. This simplifies integrating with external controlled components with non-standard prop names. Provides onChange, onBlur, name, ref and value to the child component, and also a fieldState object which contains specific input state.
        defaultValue        unknown		        Important: Can not apply undefined to defaultValue or defaultValues at useForm.
                                                    - You need to either set defaultValue at the field-level or useForm's defaultValues. undefined is not a valid value.
                                                    - If your form will invoke reset with default values, you will need to provide useForm with defaultValues.
                                                    - Calling onChange with undefined is not valid. You should use null or the empty string as your default/cleared value instead.
        rules	            Object		        Validation rules in the same format for register options, which includes:
                                                    - required, min, max, minLength, maxLength, pattern, validate
        shouldUnregister	boolean = false`		Input will be unregistered after unmount and defaultValues will be removed as well.
                                                    Note: this prop should be avoided when using with useFieldArray as unregister function gets called after input unmount/remount and reorder.
        disabled	boolean = false`		    disabled prop will be returned from field prop. Controlled input will be disabled and its value will be omitted from the submission data.

    Returns:
        new instance of PySyde6.QtWidgets.QWidget
    """
    def __init__(
            self,
            key: str = None,
            name: str = None,
            value: object = None,
            control: object = None,
            render: Callable = None,
            defaultValue = None,
            rules: object = None,
            shouldUnregister: bool = False
            ):
        super().__init__()

        field = {} # các thuộc tính đi kèm được gán vào khi render
        
        self._key = key
        self._value = value

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        if isinstance(render, Callable):
            self.layout().addWidget(render(field))
        elif isinstance(render, QWidget):
            self.layout().addWidget(render)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)