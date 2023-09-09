from typing import Dict, Any

class StateView:
    def __init__(self, state_controller, window_context, buttons_controller, state_id, next_state_id):
        self._stateMachine = state_controller
        self._window = window_context
        self.__buttons_controller = buttons_controller
        self._id = state_id
        self._next_id = next_state_id
        self._artifcats : Dict[str, any] = {}
        
    def _get_artifact(self, name : str) -> Any:
        if self._artifact_exists(name):
            return self._artifcats[name]
        else:
            return None

    def _artifact_exists(self, name : str) -> bool:
        return name in self._artifcats.keys()
    
    def get_artifacts(self) -> Dict[str, Any]:
        return self._artifcats
    
    def set_artifacts(self, artifacts) -> None:
        self._artifcats = artifacts

    def show(self) -> None:
        pass

    def setup(self) -> None:
        pass

    def destroy(self) -> None:
        pass
    
    def get_state_id(self) -> str:
        return self._id

    def get_next_state_id(self) -> str:
        return self._next_id

    def _go_next_state(self) -> None:
        self._stateMachine.next_state()