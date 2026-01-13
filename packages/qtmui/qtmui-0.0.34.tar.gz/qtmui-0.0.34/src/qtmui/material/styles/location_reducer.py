from dataclasses import dataclass, field
from typing import Literal, Optional, Dict, Any, Callable, Union, List

from dataclasses import field, replace
from typing import Callable, Sequence, Optional

from immutable import Immutable
from redux import ReducerResult, CompleteReducerResult, BaseAction, BaseEvent, Store


# Cập nhật ThemeState để sử dụng Palette thay vì Dict
# @dataclass(frozen=True)
class LocationState(Immutable):
    currentUrl: Optional[str] = None
    prevUrl: Optional[List] = field(default_factory=dict)
    mextUrl: Optional[List] = field(default_factory=dict)


class UpdateCurrentUrlAction(BaseAction):
    url: Optional[str]


def location_reducer(
    state: LocationState | None,
    action: BaseAction,
) -> ReducerResult[LocationState, BaseAction, BaseEvent]:
    if state is None:
        return LocationState()

    if isinstance(action, UpdateCurrentUrlAction):
        return replace(state, components=action.url)
    
    return state
