

class StateView:
    def __init__(self, state_controller, window_context, buttons_controller, state_id, next_state_id):
        self._stateMachine = state_controller
        self._window = window_context
        self.__buttons_controller = buttons_controller
        self._id = state_id
        self._next_id = next_state_id
        pass

    def show(self):
        pass

    def setup(self):
        pass

    def destroy(self):
        pass
    
    def get_state_id(self):
        return self._id

    def get_next_state_id(self):
        return self._next_id

    def _go_next_state(self):
        self._stateMachine.next_state()