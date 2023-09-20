from views.stateView import StateView
from errors.errors import EmptyStateException, StateUnreachableException, DuplicateStateIdException
from views.stateView import StateView
from typing import List
from config import config, Config
from api.models import DataExchange, ExchangeRequest, ExchangeType, ExchangeResponse, ConfigDescriptor
import logging

class StateMachineController :
    def __init__(self, connection):
        self.__states = []
        self.__currentState : StateView = None
        self.__next_state_candidate : StateView = None
        self.__config = Config()
        self.__conn = connection
        self.logger = logging.getLogger("fiebooth")

    def add_state(self, state : StateView):
        self.__states.append(state)
        if(len(self.__states) == 1):
            self.__currentState = state
            state.show()

    def next_state(self):
        if self.__currentState is not None:
            current_state_id = self.__currentState.get_state_id()
            target_state_id = self.__currentState.get_next_state_id()
            next_states : List[StateView]= []
            for state in self.__states:
                state : StateView
                if state.get_state_id() == target_state_id:
                    next_states.append(state)
                    
            if len(next_states) > 1:
                raise DuplicateStateIdException
            elif len(next_states) == 0:
                raise StateUnreachableException
            else:
                self.__next_state_candidate = next_states[0]
        else:
            raise EmptyStateException
            

    def setup(self):
        if self.__next_state_candidate is not None:
            self.__currentState.destroy()
            self.__next_state_candidate.set_artifacts(self.__currentState.get_artifacts())
            self.__currentState = self.__next_state_candidate
            self.__currentState.show()
            self.__currentState.clear_artifacts()
            self.__next_state_candidate = None
        self.__currentState.setup()
        self.__process_request()
        pass

    def __process_request(self):
        if self.__conn.poll(0.01):
            message = self.__conn.recv()
            self.logger.info(f"Received message from API : {message}")

                
            if message["type"] == "request":
                if message["value"] == "getConfig":
                    
                if message["value"] == "getConfig":
                    key = message["configKey"]
                    self.__conn.send({
                        "type" : "response",
                        "value" : "getSuccess",
                        "configKey" : key,
                        "configValue" : config[key],
                    })
                    

