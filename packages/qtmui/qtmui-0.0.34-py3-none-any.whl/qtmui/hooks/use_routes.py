


import uuid
from typing import Optional, Callable, Dict, Any

from dataclasses import dataclass, field
from functools import wraps
import uuid
from dataclasses import replace
from .use_state import useState



from ..immutable import Immutable

from redux import (
    BaseAction,
    BaseEvent,
    CompleteReducerResult,
    FinishAction,
    ReducerResult,
)
from redux.main import Store


class InitialState(Immutable):
  currentLocation: Optional[str] = ""
  params: Optional[dict] = field(default_factory=dict)



class UpdateCurrentLocationAction(BaseAction):
    currentLocation: Optional[str] = ""

class UpdatePushParamsAction(BaseAction):
    params: Optional[dict]
    

# reducer:
def reducer(
    state: InitialState | None,
    action: BaseAction,
) -> ReducerResult[InitialState, BaseAction, BaseEvent]:
    if state is None:
        return InitialState()
    

    if isinstance(action, UpdateCurrentLocationAction):
        return replace(
            state,
            currentLocation=action.currentLocation,
        )
    
    if isinstance(action, UpdatePushParamsAction):
        return replace(
            state,
            params=action.params,
        )
    
    return state


router_store = Store(reducer)
router_store.dispatch(UpdateCurrentLocationAction(currentLocation=""))
router_store.dispatch(UpdatePushParamsAction(params={}))

location, setLocation = useState(router_store._state.currentLocation)
params, setParams = useState(router_store._state.params)

def useRouter():
    global location
    class Route():
        def __init__(self):
            self.location = None
        def push(self, location):
            # router_store.dispatch(UpdateCurrentLocationAction(currentLocation=f"push//:{location}"))
            params = location.split('?')[1]
            params_list = params.split("&&")
            params_dict = {}
            for param in params_list:
                params_dict.update({param.split("=")[0]: param.split("=")[1]})
            router_store.dispatch(UpdatePushParamsAction(params=params_dict))
        def replace(self, location):
            router_store.dispatch(UpdateCurrentLocationAction(currentLocation=f"replace//:{location}"))
        def to(self, location):
            router_store.dispatch(UpdateCurrentLocationAction(currentLocation=location))
    route = Route()
    route.location = location
    return route



def useSearchParams():
    global params
    return params

def useLocation():
    global location, setLocation
    # setLocation(router_store._state.currentLocation)
    return location

@router_store.autorun(lambda state: state.currentLocation)
def update_location(currentLocation):
    setLocation(currentLocation)

@router_store.autorun(lambda state: state.params)
def update_params(params):
    setParams(params)


