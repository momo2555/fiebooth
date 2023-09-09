from .stateView import StateView

class AskPrintView(StateView):
    def __init__(self, state_controller, window_context, buttons_controller):
        StateView.__init__(self, state_controller, window_context, buttons_controller, "ask_print", "home")
    def setup(self):
        pass