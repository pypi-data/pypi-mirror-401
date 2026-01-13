from typing import Callable, List, Dict, Any
from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal

from .use_state import useState, State
from .use_form import UseForm

@dataclass
class FieldArrayType:
    fields: List[Dict[str, Any]]
    append: Callable[[Dict[str, Any]], None]
    remove: Callable[[int], None]
    update: Callable[[int, Dict[str, Any]], None]

class FieldArray(QObject):
    fieldsChanged = Signal(list)

    def __init__(self, control: UseForm, name: str):
        super().__init__()
        self.control = control
        self.name = name
        self.fields, self.setFields = useState(control.watch().get(name, []))

    def append(self, item: Dict[str, Any]):
        current_fields = self.fields.value.copy()
        current_fields.append(item)
        self.setFields(current_fields)
        self.control.setValue(self.name, current_fields)

    def remove(self, index: int):
        current_fields = self.fields.value.copy()
        if 0 <= index < len(current_fields):
            current_fields.pop(index)
            self.setFields(current_fields)
            self.control.setValue(self.name, current_fields)

    def update(self, index: int, item: Dict[str, Any]):
        current_fields = self.fields.value.copy()
        if 0 <= index < len(current_fields):
            current_fields[index] = item
            self.setFields(current_fields)
            self.control.setValue(self.name, current_fields)

def useFieldArray(control: UseForm, name: str) -> FieldArrayType:
    field_array = FieldArray(control, name)
    return FieldArrayType(
        fields=field_array.fields.value,
        append=field_array.append,
        remove=field_array.remove,
        update=field_array.update,
    )