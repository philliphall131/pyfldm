from time import sleep
from pyfldm.appmonitor import AppMonitor
from pyfldm.client import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt

class TestClientSpot(BaseTestCase):
    def __init__(self) -> None:
        super().__init__()
        self.user_prompt = UserPrompt()
        self.app = AppMonitor()
        self.client = Client()
    
    def setup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
        self.app.start()
    
    def cleanup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
    
    def get_set_toggle(self, set_func:str, get_func:str, tog_func:str) -> bool:
        state1 = set_func(True)
        if not (type(state1) == bool):
            return False, "state1 not of type bool"
        sleep(1)

        state2 = get_func()
        if not (type(state2) == bool):
            return False, "state2 not of type bool"
        if not state2:
            return False, "state2 should be True, was False"

        state3 = set_func(False)
        if not state3:
            return False, "state3 should be True, was False"
        sleep(1)

        state4 = get_func()
        if state4:
            return False, "state4 should be False, was True"

        state5 = tog_func()
        if not state5:
            return False, "state5 should be True, was False"
        sleep(1)

        state6 = get_func()
        if not state6:
            return False, "state6 should be True, was False"
        return True, ""
    
    def test_spot_get_set_toggle_auto(self):
        get_auto = self.client.spot.get_auto
        set_auto = self.client.spot.set_auto
        tog_auto = self.client.spot.toggle_auto
        result, msg = self.get_set_toggle(set_auto, get_auto, tog_auto)
        assert result, msg
    
    def test_spot_get_pskrep_count(self):
        result1 = self.client.spot.get_pskrep_count()
        assert type(result1) == int
    