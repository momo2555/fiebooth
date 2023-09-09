from views.stateView import StateView
from errors.errors import EmptyStateException, StateUnreachableException, DuplicateStateIdException
from views.stateView import StateView


class StateMachineController :
    def __init__(self):
        self.__states = []
        self.__currentState : StateView = None
        pass

    def add_state(self, state : StateView):

        self.__states.append(state)
        if(len(self.__states) == 1):
            self.__currentState = state
            state.show()
        pass

    def next_state(self):
        if self.__currentState is not None:
            current_state_id = self.__currentState.get_state_id()
            target_state_id = self.__currentState.get_next_state_id()

            next_states = []
            for state in self.__states:
                state : StateView
                if state.get_state_id() == target_state_id:
                    next_states.append(state)
                    
            if len(next_states) > 1:
                raise DuplicateStateIdException
            elif len(next_states) == 0:
                raise StateUnreachableException
            else:
                self.__currentState.destroy()
                self.__currentState = next_states[0]
                self.__currentState.show()
        
        else:
            raise EmptyStateException
            


    def setup(self):
        self.__currentState.setup()
        pass
