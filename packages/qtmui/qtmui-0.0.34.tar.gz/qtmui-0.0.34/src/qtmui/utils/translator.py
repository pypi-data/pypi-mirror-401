
from typing import Callable
from qtmui.hooks import State
from qtmui.i18n.use_translation import translate


def getTranslatedText(input):
    if isinstance(input, Callable):
        return translate(input)
    elif isinstance(input, State):
        if isinstance(input.value, Callable):
            return translate(input.value)
        elif isinstance(input.value, str):
            return input.value
    elif isinstance(input, str):
        return input