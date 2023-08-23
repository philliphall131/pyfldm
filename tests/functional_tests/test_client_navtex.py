from time import sleep
from pyfldm.appmonitor import AppMonitor
from pyfldm.client import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt

class TestClientNavtex(BaseTestCase):
    def __init__(self) -> None:
        super().__init__()
        self.user_prompt = UserPrompt()
        self.app = AppMonitor()
        self.client = Client()
    
    def setup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
        self.app.start()
        self.client.modem.set_by_name("CW")
    
    def cleanup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
    
    #TODO: Not sure how to operate NAVTEX well enough to test it yet. The endpoints don't error out though. 
    def test_navtex(self):
        result1 = self.client.navtex.send_message("Hello World")
        assert type(result1) == str

        result2 = self.client.navtex.get_message(5)
        assert type(result2) == str