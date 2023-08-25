############################################################################
# 
#  File: test_client_wefax.py
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

class TestClientWefax(BaseTestCase):
    def __init__(self) -> None:
        super().__init__()
        self.user_prompt = UserPrompt()
        self.app = AppMonitor()
        self.client = Client()
    
    def setup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
        self.app.start()
        self.client.modem.set_by_name("WEFAX576")
    
    def cleanup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
    
    def test_wefax_state_string(self):
        result = self.client.wefax.state_string()
        assert type(result) == str

    def test_wefax_skip_apt(self):
        result = self.client.wefax.skip_apt()
        assert type(result) == str

    def test_wefax_skip_phasing(self):
        result = self.client.wefax.skip_phasing()
        assert type(result) == str

    def test_wefax_set_adif_log(self):
        result = self.client.wefax.set_adif_log(True)
        assert type(result) == str

    def test_wefax_set_max_lines(self):
        result = self.client.wefax.set_max_lines(2000)
        assert type(result) == str

    def test_wefax_set_tx_abort_flag(self):
        result = self.client.wefax.set_tx_abort_flag()
        assert type(result) == str
    
    #TODO: figure out how this call works
    # def test_wefax_send_file(self):
    #     result = self.client.wefax.send_file("")
    #     assert type(result) == str
    
    def test_wefax_get_received_file(self):
        result = self.client.wefax.get_received_file(10)
        assert type(result) == str
    
    def test_wefax_end_reception(self):
        result = self.client.wefax.end_reception()
        assert type(result) == str