from typing import Dict, Any
import logging

class StateView:
    def __init__(self, state_controller, window_context, state_id, next_state_id):
        self._stateMachine = state_controller
        self._window = window_context
        self._id = state_id
        self._next_id = next_state_id
        self.__artifcats : Dict[str, any] = {}
        self._logger = logging.getLogger("fiebooth")
        
    def _get_artifact(self, name : str) -> Any:
        if self._artifact_exists(name):
            return self.__artifcats[name]
        else:
            return None

    def _artifact_exists(self, name : str) -> bool:
        return name in self.__artifcats.keys()
    
    def _add_artifact(self, name: str, value: Any) -> None:
        self.__artifcats[name] = value

    def get_artifacts(self) -> Dict[str, Any]:
        return self.__artifcats.copy()
    
    def set_artifacts(self, artifacts) -> None:
        self.__artifcats = artifacts

    def clear_artifacts(self) -> None:
        self.__artifcats = {}

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
    
    def set_next_state_id(self, next_id) -> None:
        self._next_id = next_id

    def _go_next_state(self) -> None:
        self._stateMachine.next_state()