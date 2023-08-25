############################################################################
# 
#  File: test_client_spot.py
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
        self.client.modem.set_by_name("CW")
    
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
    