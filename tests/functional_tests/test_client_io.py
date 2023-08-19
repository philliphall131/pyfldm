from time import sleep
from pyfldm.appmonitor import AppMonitor
from pyfldm.client import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt

class TestClientIo(BaseTestCase):
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
    
    def restart(self) -> None:
        self.app.stop()
        sleep(2)
        self.app.start()

    
    def test_io_config(self):
        ARQ_MODE = "ARQ"
        KISS_MODE = "KISS"

        self.client.io.enable_kiss()
        self.restart()

        mode = self.client.io.in_use()
        assert mode == KISS_MODE

        self.client.io.enable_arq()
        self.restart()

        mode = self.client.io.in_use()
        assert mode == ARQ_MODE

        self.client.io.enable_kiss()
        self.restart()

        mode = self.client.io.in_use()
        assert mode == KISS_MODE

        self.client.io.enable_arq()
        self.restart()

        mode = self.client.io.in_use()
        assert mode == ARQ_MODE