from redux.combine_reducers import combine_reducers
from .create_theme.theme_reducer import theme_reducer, ThemeState
from .location_reducer import location_reducer, LocationState

from redux import (
    BaseAction,
    BaseCombineReducerState,
    CombineReducerAction,
    CombineReducerRegisterAction,
    CombineReducerUnregisterAction,
    InitAction,
    InitializationActionError,
    Store,
    combine_reducers,
)
from redux.basic_types import (
    BaseEvent,
    CompleteReducerResult,
    FinishAction,
    ReducerResult,
)

# root_reducer, reducer_id = combine_reducers({
#     "products": product_reducer,
#     "users": user_reducer,
# })

class ProductAction(BaseAction): ...
class UserAction(BaseAction): ...


class StateType(BaseCombineReducerState):
    theme: ThemeState = None
    location: LocationState = None


# ActionType = InitAction | FinishAction | ProductAction | UserAction | CombineReducerAction
ActionType = InitAction | FinishAction | BaseAction | CombineReducerAction


root_reducer, root_reducer_id = combine_reducers(
    state_type=StateType,
    action_type=ActionType,  # pyright: ignore [reportArgumentType]
    theme=theme_reducer,
    location=location_reducer,
)

# store: Store[StateType] = Store(root_reducer)
# store._state.permission
