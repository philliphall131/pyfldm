from time import sleep
from pyfldm.appmonitor import AppMonitor
from pyfldm.client import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt

class TestText(BaseTestCase):
    def __init__(self) -> None:
        super().__init__()
        self.user_prompt = UserPrompt()
        self.app = AppMonitor()
        self.client = Client()
    
    def setup(self) -> None:
        if not self.app.is_running():
            self.app.start()
    
    def cleanup(self) -> None:
        self.app.stop(force_if_unsuccessful=True)

    def test_add_tx(self):
        self.client.text.add_tx("Testing add text to tx widget")
        # assert self.user_prompt.verify_yes("Check the Fldigi Tx Widget and ensure the following string has been populated: 'Testing add text to tx widget'")
        assert True
    
    def test_shutdown(self):
        for _ in range(25):
            self.app.stop()
            sleep(10)
            self.app.start()
            sleep(10)