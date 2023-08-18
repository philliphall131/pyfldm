from time import sleep
from pyfldm.appmonitor import AppMonitor
from pyfldm.client import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt
from utilities.utilities import TestSetupException

class TestClient(BaseTestCase):
    def __init__(self) -> None:
        super().__init__()
        self.user_prompt = UserPrompt()
        self.app = AppMonitor()
        self.client = Client()
    
    def setup(self) -> None:
        prompt = "Test Case Setup: Ensure there are no instances of Fldigi running. Select Y to continue"
        if not self.user_prompt.verify_yes(prompt):
            raise TestSetupException(f"Exception in setting up test class TestAppMonitor")
    
    def cleanup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
    
    def test_get_all_methods(self):
        self.app.start()

        methods = self.client.get_all_methods()
        assert type(methods) == list

        self.app.stop()
    
    