import logging

class ComponentBase():
    def __init__(self, window_context):
        self._window = window_context
        self._logger = logging.getLogger("fiebooth")

    def setup(self) -> None:
        pass
    