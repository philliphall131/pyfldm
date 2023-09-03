############################################################################
# 
#  File: test_radio1.py
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
from .messages import MESSAGE1

class TestRadioOne(BaseTestCase):
    def __init__(self) -> None:
        super().__init__()
        self.user_prompt = UserPrompt()
        self.app = AppMonitor()
        self.client = Client()
    
    def setup(self) -> None:
        assert self.user_prompt.verify_yes("To Perform these tests, ensure entire radio setup is complete to allow normal transmission using Fldigi. It is operator responsibilty to ensure the radio is set up to transmit legally and within the locally acceptable bounds. This test defaults to using PSK31. Select Y when hardware setup is complete (fldigi should not be running). ")
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
        self.app.start()
        self.client.modem.set_by_name("BPSK31")
    
    def cleanup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True) 
    
    def test_basic_send(self) -> None:
        # clear off the widgets
        self.client.text.clear_rx()
        self.client.text.clear_tx()
        self.client.main.rx_tx()

        # add message1 to the Tx
        self.client.text.add_tx(MESSAGE1)

        # Transmit it
        self.client.main.tx()

        # Wait for transmission to complete and check that all transmitted
        sleep(20)
        self.client.text.get_tx_data()

        # Verify recieving end shows all recieved



    
    # abort
    # run macro
    # get trx state, status
    # tx, rx, rx_only, rx_tx

    # modem search up/down
    # navtex?

    # spot 
    # spot.get_auto
    # set_auto
    # toggle_auto
    # get_pskrep_count()

    # text addtx, cleartx addtxbytes
    # gettxdata, get rx tx data
    # getrxdata, getrxlength, get_rx, clear rx

      # wefax state_string, skip_apt, skip_phasing, set_adif_log
    # set_max_lines, set_tx_abort_flag
    # get_received_file, end_reception, send_file