############################################################################
# 
#  File: test_appmonitor.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#  USA
#
############################################################################

from time import sleep
import sys
import logging
from pyfldm.appmonitor import AppMonitor
from pyfldm.client import Client
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
        response = self.user_prompt.skip_option("Copy the fldigi program folder into C:\\Users\\Public\\Desktop then continue")
        if response == 'skip':
            return
        new_app = AppMonitor(exe_path="C:\\Users\\Public\\Desktop\\Fldigi-4.1.27\\fldigi.exe")
        new_app.start()
        assert self.user_prompt.verify_yes("Verify that the Fldigi app launched")
        new_app.stop()


    def test_windows_find_multiple_exe(self):
        if sys.platform != 'win32':
            logger.info(f'{self.name}::{PrintColors.YELLOW.value}INFO{PrintColors.ENDC.value}: Not a Windows OS platform, skipping test')
            return
        response = self.user_prompt.skip_option("Find the fldigi program folder in Program Files and copy it into the same location, renaming it to increase the version number then continue")
        if response == 'skip':
            return
        new_app = AppMonitor()
        new_app.start()
        assert self.user_prompt.verify_yes("Verify that the Fldigi app launched")
        new_app.stop()

    def test_get_process_id(self):
        self.app.start()

        id = self.app._get_process_id()
        assert self.user_prompt.verify_yes(f"Use your preferred method on the OS to check the process ID of Fldigi, which should be running. \n Ex. On unix use ps aux | grep fldigi. \nVerify the process id matches: {id}: ")

        self.app.stop(force_if_unsuccessful=True)
    
    def test_repeated_power_cycles(self):
        CYCLES = 20
        for i in range(CYCLES):
            logger.info(f'Starting power cycle {i+1}')
            self.app.start()
            self.app.stop()
