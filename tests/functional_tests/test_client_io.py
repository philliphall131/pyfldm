############################################################################
# 
#  File: test_client_io.py
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
        self.client.modem.set_by_name("CW")
    
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