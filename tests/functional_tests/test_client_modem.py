############################################################################
# 
#  File: test_client_modem.py
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

class TestClientModem(BaseTestCase):
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

    def test_modem_get_set_modem(self):
        result1 = self.client.modem.set_by_name("CW")
        assert type(result1) == str

        result2 = self.client.modem.get_name()
        assert type(result2) == str
        assert result2 == 'CW'

        result3 = self.client.modem.get_id()
        assert type(result3) == int
        assert result3 == 1

        result4 = self.client.modem.set_by_name("DOMEX8")
        assert result4 == 'CW'

        result5 = self.client.modem.get_name()
        assert result5 == 'DOMEX8'

        result6 = self.client.modem.get_id()
        assert result6 == 25

        result7 = self.client.modem.set_by_id(2)
        assert type(result7) == int
        assert result7 == 25

        result5 = self.client.modem.get_name()
        assert result5 == 'CONTESTIA'

        result6 = self.client.modem.get_id()
        assert result6 == 2

    def test_modem_get_names(self):
        result = self.client.modem.get_names()
        assert type(result) == list
        assert type(result[1]) == str
    
    def test_modem_get_max_id(self):
        result = self.client.modem.get_max_id()
        assert type(result) == int

    def test_modem_get_set_inc_carrier(self):
        result1 = self.client.modem.set_carrier(1500)
        assert type(result1) == int

        result2 = self.client.modem.get_carrier()
        assert type(result2) == int
        assert result2 == 1500

        result3 = self.client.modem.set_carrier(2000)
        assert result3 == 1500

        result4 = self.client.modem.get_carrier()
        assert result4 == 2000

        result5 = self.client.modem.increment_carrier(500)
        assert type(result5) == int
        assert result5 == 2500

        result6 = self.client.modem.get_carrier()
        assert result6 == 2500
    
    def test_modem_get_set_inc_bandwidth(self):
        self.client.modem.set_by_name("CW")
        sleep(2)

        result1 = self.client.modem.set_bandwidth(150)
        assert type(result1) == int
        sleep(1)

        result2 = self.client.modem.get_bandwidth()
        assert type(result2) == int
        assert result2 == 150

        result3 = self.client.modem.set_bandwidth(50)
        assert result3 == 150
        sleep(1)

        result4 = self.client.modem.get_bandwidth()
        assert result4 == 50

        result5 = self.client.modem.increment_bandwidth(50)
        assert type(result5) == int
        assert result5 == 100
        sleep(1)

        result6 = self.client.modem.get_bandwidth()
        assert result6 == 100

    def test_modem_get_set_inc_afc_search_range(self):
        self.client.modem.set_by_name('BPSK31')
        sleep(2)

        result1 = self.client.modem.set_afc_search_range(150)
        assert type(result1) == int
        sleep(1)

        result2 = self.client.modem.get_afc_search_range()
        assert type(result2) == int
        assert result2 == 150

        result3 = self.client.modem.set_afc_search_range(50)
        assert result3 == 150
        sleep(1)

        result4 = self.client.modem.get_afc_search_range()
        assert result4 == 50

        result5 = self.client.modem.increment_afc_search_range(50)
        assert type(result5) == int
        assert result5 == 100
        sleep(1)

        result6 = self.client.modem.get_afc_search_range()
        assert result6 == 100

    def test_modem_get_quality(self):
        result = self.client.modem.get_quality()
        assert type(result) == float

    #TODO: cant get this to work. the call to fldigi works fine, but not sure how
    #TODO: to set it up so that it has a measurable effect
    def test_modem_search(self):
        self.client.modem.set_by_name('DOMEX8')
        sleep(2)
        # assert self.user_prompt.verify_yes("Manually set Fldigi configuration to use computer speakers/mic as the audio in/out devices.")
        # assert self.user_prompt.verify_yes("Make some external noise, like playing a song from a phone, near the computer. ")

        result1 = self.client.modem.get_carrier()
        self.client.modem.search_down()
        self.client.modem.search_up()
        sleep(1)
        result2 = self.client.modem.get_carrier()
        # assert result1 != result2
        # assert self.user_prompt.verify_yes("Stop playing external sounds")
    
    def test_modem_olivia_bandwidth(self):
        self.client.modem.set_olivia_bandwidth(125)
        result1 = self.client.modem.get_olivia_bandwidth()
        assert type(result1) == int
        assert result1 == (125*2)

        self.client.modem.set_olivia_bandwidth(500)
        result2 = self.client.modem.get_olivia_bandwidth()
        assert type(result2) == int
        assert result2 == (500*2)

    def test_modem_olivia_tones(self):
        self.client.modem.set_olivia_tones(2)
        result1 = self.client.modem.get_olivia_tones()
        assert type(result1) == int
        assert result1 == 2

        self.client.modem.set_olivia_tones(8)
        result2 = self.client.modem.get_olivia_tones()
        assert type(result2) == int
        assert result2 == 8