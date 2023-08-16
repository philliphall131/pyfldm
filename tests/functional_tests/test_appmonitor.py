from time import sleep
import logging
from pyfldm import AppMonitor
from pyfldm import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt
from utilities.utilities import TestSetupException, TestCleanupException, PrintColors

logger = logging.getLogger(__name__)

class TestAppMonitor(BaseTestCase):
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
        self.app.stop(force_if_unsuccessful=True)

    def each_cleanup(self) -> None:
        pass
    
    def test_app_launches(self):
        self.app.start()
        prompt = "Verify that the Fldigi app launched"
        assert self.user_prompt.verify_yes(prompt)
        self.app.stop()
    
    def test_app_is_running_and_functional(self):
        assert self.user_prompt.verify_yes("Start Fldigi manually, select Y when complete.")

        assert self.app.is_running()
        assert self.app.is_functional()

        self.app.stop()

    def test_app_graceful_shutdown(self):
        self.app.start()
        logger.info("Waiting 10 seconds to ensure the app starts up ok")
        sleep(10)

        assert self.app.is_running()
        assert self.app.is_functional()

        successful = self.app.stop()
        if not successful:
            logger.warning(f'{self.name}::{PrintColors.YELLOW.value}WARN{PrintColors.ENDC.value}: Detected AppMonitor did not shut down Fldigi successfully')
        assert self.user_prompt.verify_yes("Did Fldigi shut down ok?")

    def test_app_force_kill(self):
        self.app.start()
        logger.info("Waiting 10 seconds to ensure the app starts up ok")
        sleep(10)

        assert self.app.is_running()
        assert self.app.is_functional()

        successful = self.app.kill()
        if not successful:
            logger.warning(f'{self.name}::{PrintColors.YELLOW.value}WARN{PrintColors.ENDC.value}: Detected AppMonitor did not shut down Fldigi successfully')
        assert self.user_prompt.verify_yes("Did Fldigi shut down ok?")

    def test_windows_find_exe(self):
        pass

    def test_windows_find_multiple_exe(self):
        pass

    def test_get_process_id(self):
        pass
