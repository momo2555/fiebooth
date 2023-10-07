from views.stateView import StateView
from errors.errors import EmptyStateException, StateUnreachableException, DuplicateStateIdException
from views.stateView import StateView
from typing import List
from config import config, Config
from api.models import DataExchange, ExchangeRequest, ExchangeType, ExchangeResponse, ConfigDescriptor
from utils.image_utils import ImageUtils
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

    def next_state(self, force_state = None):
        if self.__currentState is not None:
            #current_state_id = self.__currentState.get_state_id()
            if force_state is None:
                target_state_id = self.__currentState.get_next_state_id()
            else:
                target_state_id = force_state
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
                if message["value"] == "setConfig":
                    key = message["configKey"]
                    config[key] = message["configValue"]
                    self.__conn.send({
                        "type" : "response",
                        "value" : "setSuccess",
                        "configKey" : key,
                        "configValue" : config[key],
                    })
                if message["value"] == "getConfig":
                    key = message["configKey"]
                    self.__conn.send({
                        "type" : "response",
                        "value" : "getSuccess",
                        "configKey" : key,
                        "configValue" : config[key],
                    })
                if message["value"] == "print":
                    image_id = message["imageId"]
                    image_path = ImageUtils.get_image_path_from_id(image_id)
                    self.__currentState._add_artifact("photo_name", image_path)
                    self.next_state("printing")
                    self.__conn.send({
                        "type" : "response",
                        "value" : "printSent",
                    })
                if message["value"] == "createUser":
                    config["user_name"] = message["userName"]
                    config["user_password"] = message["userPassword"]
                    config["user_text"] = ""
                    config["user_prints_len"] = 0
                    config["user_photos_len"] = 0
                    self.logger.info(f"user created {config.user_name}")
                    
                    self.__conn.send({
                        "type" : "response",
                        "value" : "userCreated",
                    })

                    

