############################################################################
# 
#  File: test_client_text.py
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

class TestClientText(BaseTestCase):
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

    def test_text_add_tx(self):
        self.client.text.add_tx("Hello World")
        assert self.user_prompt.verify_yes("Verify the Tx Text Widget in Fldigi has the words 'Hello World'.")

        self.client.text.clear_tx()
        assert self.user_prompt.verify_yes("Verify the Tx Text Widget is now cleared")

        string1 = "Hello World2"
        byte_str = bytes(string1.encode())
        self.client.text.add_tx_bytes(byte_str)

        assert self.user_prompt.verify_yes("Verify the Tx Text Widget in Fldigi has the words 'Hello World2'.")
        self.client.text.clear_tx()
    
    def test_text_get_tx_data(self):
        assert self.user_prompt.verify_yes("Set your computer sound volume low, between 10-25% and ensure there is no radio connected to the computer")
        assert self.user_prompt.verify_yes("Manually set Fldigi configuration to use computer speakers/mic as the audio in/out devices.")
        self.client.modem.set_by_name("BPSK31")
        self.client.text.add_tx("Hello World")
        self.client.main.tx()
        sleep(10)
        self.client.main.rx()
        sleep(2)
        result1 = self.client.text.get_tx_data()
        result1_str = str(result1)
        assert "Hello World" in result1_str

        self.client.text.add_tx("Hello World2")
        self.client.main.tx()
        sleep(10)
        self.client.main.rx()
        sleep(2)
        result2 = self.client.text.get_rxtx_data()
        result2_str = str(result2)
        assert "Hello World2" in result2_str
    
    def test_text_get_rx_data(self):
        self.client.modem.set_by_name("THOR8")
        assert self.user_prompt.verify_yes("Manually set Fldigi configuration to use computer speakers/mic as the audio in/out devices.")
        assert self.user_prompt.verify_yes("Make some external noise, like playing a song from a phone, near the computer. ")
        sleep(10)
        result1 = self.client.text.get_rx_data()
        assert len(str(result1)) > 0

        result2 = self.client.text.get_rx_length()
        assert type(result2) == int
        if result2 > 0:
            result2 = self.client.text.get_rx(0, 1)
            assert len(str(result2)) == 1
        else:
            assert False, "Not recieving data"
        
        assert self.user_prompt.verify_yes("Stop playing external sounds")
        sleep(1)
        self.client.text.clear_rx()
        assert self.user_prompt.verify_yes("Verify the Rx text widget in Fldigi is empty")