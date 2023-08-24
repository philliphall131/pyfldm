from time import sleep
import sys
import logging
from pyfldm import AppMonitor
from pyfldm import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt
from utilities.utilities import TestSetupException, PrintColors

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
    
    def test_app_launches(self):
        self.app.start()
        prompt = "Verify that the Fldigi app launched"
        assert self.user_prompt.verify_yes(prompt)
        self.app.stop()
    
    def test_app_is_running_and_functional(self):
        assert self.user_prompt.verify_yes("Start Fldigi manually, select Y when complete.")
        sleep(5)

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
        try: 
            assert self.user_prompt.verify_yes("Did Fldigi shut down ok?")
        except:
            self.user_prompt.verify_yes("Looks like pyfldm was not able to gracefully shutdown Fldigi. Manually shut down or force kill pyfldm to continue")
            assert False, "AppMonitor.stop() did not work in shutting down fldigi, user manually shut down"

    def test_app_force_kill(self):
        self.app.start()
        logger.info("Waiting 10 seconds to ensure the app starts up ok")
        sleep(10)

        assert self.app.is_running()
        assert self.app.is_functional()

        successful = self.app.kill()
        if not successful:
            logger.warning(f'{self.name}::{PrintColors.YELLOW.value}WARN{PrintColors.ENDC.value}: Detected AppMonitor did not shut down Fldigi successfully')
        try:
            assert self.user_prompt.verify_yes("Did Fldigi shut down ok?")
        except:
            self.user_prompt.verify_yes("Looks like pyfldm was not able to force kill Fldigi. Manually shut down or force kill pyfldm to continue")
            assert False, "AppMonitor.kill() did not work in killing fldigi, user manually shut down"

    def test_windows_find_exe(self):
        if sys.platform != 'win32':
            logger.info(f'{self.name}::{PrintColors.YELLOW.value}INFO{PrintColors.ENDC.value}: Not a Windows OS platform, skipping test')
            return
        # TODO

    def test_windows_find_multiple_exe(self):
        if sys.platform != 'win32':
            logger.info(f'{self.name}::{PrintColors.YELLOW.value}INFO{PrintColors.ENDC.value}: Not a Windows OS platform, skipping test')
            return
        # TODO

    def test_get_process_id(self):
        self.app.start()

        id = self.app._get_process_id()
        assert self.user_prompt.verify_yes(f"Use your preferred method on the OS to check the process ID of Fldigi, which should be running. \n Ex. On unix use ps aux | grep fldigi. \nVerify the process id matches: {id}: ")

        self.app.stop(force_if_unsuccessful=True)
    
    def test_repeated_power_cycles(self):
        #TODO
        pass
