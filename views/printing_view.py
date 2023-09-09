from views.stateView import StateView
from assets.assets import get_asset_uri 
from config import config
import time
import pygame


class PrintingView(StateView):
    def __init__(self, state_controller, window_context):
        StateView.__init__(self, state_controller, window_context, "printing", "camera_stream")
        

    def show(self):
        
        pass