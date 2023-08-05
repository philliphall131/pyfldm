############################################################################
# 
#  File: Main.py
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

from xmlrpc.client import ServerProxy

class Main:
    '''Houses the commands in the main group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> import pyfldm
    >>> client = pyfldm.Client()
    >>> client.main.get_frequency()
    14070.000
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

    def abort(self) -> None:
        '''Aborts a transmit or tune'''
        self.client.main.abort()
    
    def get_afc(self) -> bool:
        '''Gets the AFC state

        @return (bool): the AFC state
        '''
        return self.client.main.get_afc()
    
    def get_char_rates(self) -> str:
        '''Gets the table of char rates

        @return (str): the char rates
        '''
        return self.client.main.get_char_rates()
    
    def get_char_timing(self, char_bytes: bytes) -> str:
        '''Gets transmit duration for the specified character

        @param char_bytes(bytes): the bitmask to send for the character (samples:sample rate)
        @return (bytes): the value of the character
        '''
        return self.client.main.get_char_timing(char_bytes)
    
    def get_frequency(self) -> float:
        '''Gets the RF carrier frequency

        @return (float): the RF carrier frequency
        '''
        return self.client.main.get_frequency()
    
    def get_local(self) -> bool:
        '''Gets the Transmit Lock state

        @return (bool): the Transmit Lock state
        '''
        return self.client.main.get_local()
    
    def get_max_macro_id(self) -> int:
        '''Gets the maximum macro ID number

        @return (int): the maximum macro ID number
        '''
        return self.client.main.get_max_macro_id()
    
    def get_rsid(self) -> bool:
        '''Gets the RSID state

        @return (bool): the RSID state
        '''
        return self.client.main.get_rsid()
    
    def get_txid(self) -> bool:
        '''Gets the TxRSID state

        @return (bool): the TxRSID state
        '''
        return self.client.main.get_txid()
    
    def get_squelch(self) -> bool:
        '''Gets the squelch state

        @return (bool): the squelch state
        '''
        return self.client.main.get_squelch()
    
    def get_squelch_level(self) -> float:
        '''Gets the squelch level

        @return (float): the squelch level
        '''
        return self.client.main.get_squelch_level()
    
    def get_status1(self) -> str:
        '''Gets the contents of the first status field (typically s/n)

        @return (str): the contents of the first status field
        '''
        return self.client.main.get_status1()
    
    def get_status2(self) -> str:
        '''Gets the contents of the second status field

        @return (str): the contents of the second status field
        '''
        return self.client.main.get_status2()
    
    def get_trx_state(self) -> str:
        '''Gets the T/R state

        @return (str): the T/R state
        '''
        return self.client.main.get_trx_state()
    
    def get_trx_status(self) -> str:
        '''Gets the transmit/tune/receive status

        @return (str): the transmit/tune/receive status
        '''
        return self.client.main.get_trx_status()
    
    def get_trx_timing(self, bitmask: bytes) -> str:
        '''Gets the transmit duration for test string (samples:sample rate:secs)

        @param bitmask(bytes): the bytes to specify the test string (samples:sample rate:secs)
        @return (str): the transmit/tune/receive status
        '''
        return self.client.main.get_trx_timing(bitmask)

    def get_wf_sideband(self) -> str:
        '''Gets the current waterfall sideband

        @return (str): the current waterfall sideband
        '''
        return self.client.main.get_wf_sideband()
    
    def inc_frequency(self, amount: float) -> float:
        '''Increments the RF carrier frequency

        @param amount(float): the amount to increment the frequency
        @return (float): the new frequency
        '''
        return self.client.main.inc_frequency(amount)
    
    def inc_squelch_level(self, amount: float) -> float:
        '''Increments the squelch level

        @param amount(float): the amount to increment the squelch
        @return (float): the new squelch level
        '''
        return self.client.main.inc_squelch_level(amount)
    
    def run_macro(self, macro_num: int) -> None:
        '''Runs a macro

        @param macro_num(float): the macro number to run
        @return (float): the new frequency
        '''
        self.client.main.run_macro(macro_num)
    
    def rx(self) -> None:
        '''Puts Fldigi into recieve mode'''
        self.client.main.rx()
    
    def rx_only(self) -> None:
        '''Puts Fldigi into recieve mode, disables Tx'''
        self.client.main.rx_only()

    def rx_tx(self) -> None:
        '''Sets normal Rx/Tx switching'''
        self.client.main.rx_tx()

    def set_afc(self, new_state: bool) -> bool:
        '''Sets the AFC state

        @param new_state(bool): the new AFC state
        @return (bool): the old state
        '''
        return self.client.main.set_afc(new_state)

    def set_frequency(self, new_frequency: float) -> float:
        '''Sets the RF carrier frequency

        @param new_state(float): the new frequency
        @return (bool): the old frequency
        '''
        return self.client.main.set_frequency(new_frequency)

    def set_lock(self, new_state: bool) -> bool:
        '''Sets the Transmit Lock state

        @param new_state(bool): the new Transmit lock state
        @return (bool): the old state
        '''
        return self.client.main.set_lock(new_state)
    
    def set_reverse(self, new_state: bool) -> bool:
        '''Sets the reverse sideband state

        @param new_state(bool): the new reverse sideband
        @return (bool): the old state
        '''
        return self.client.main.set_reverse(new_state)
    
    def set_rsid(self, new_state: bool) -> bool:
        '''Sets the RSID state

        @param new_state(bool): the new RSID state
        @return (bool): the old state
        '''
        return self.client.main.set_rsid(new_state)
    
    def set_txid(self, new_state: bool) -> bool:
        '''Sets the TxRSID state

        @param new_state(bool): the new TxRSID state
        @return (bool): the old state
        '''
        return self.client.main.set_txid(new_state)
    
    def set_squelch(self, new_state: bool) -> bool:
        '''Sets the Squelch state

        @param new_state(bool): the new squelch state
        @return (bool): the old state
        '''
        return self.client.main.set_squelch(new_state)
    
    def set_squelch_level(self, new_level: float) -> float:
        '''Sets the Squelch level

        @param new_level(float): the new squelch level
        @return (float): the old level
        '''
        return self.client.main.set_squelch_level(new_level)
    
    def set_wf_sideband(self, new_sideband: str) -> None:
        '''Sets the waterfall sideband to USB or LSB

        @param new_sideband(float): the new squelch level
        '''
        self.client.main.set_wf_sideband(new_sideband)

    def toggle_afc(self) -> bool:
        '''Toggles the AFC state

        @return (bool): the new state
        '''
        return self.client.main.toggle_afc()
    
    def toggle_lock(self) -> bool:
        '''Toggles the Transmit Lock state

        @return (bool): the new state
        '''
        return self.client.main.toggle_lock()
    
    def toggle_reverse(self) -> bool:
        '''Toggles the Reverse Sideband state

        @return (bool): the new state
        '''
        return self.client.main.toggle_reverse()
    
    def toggle_rsid(self) -> bool:
        '''Toggles the RSID state

        @return (bool): the new state
        '''
        return self.client.main.toggle_rsid()
    
    def toggle_txid(self) -> bool:
        '''Toggles the TxRSID state

        @return (bool): the new state
        '''
        return self.client.main.toggle_txid()
    
    def toggle_squelch(self) -> bool:
        '''Toggles the squelch state

        @return (bool): the new state
        '''
        return self.client.main.toggle_squelch()
    
    def tune(self) -> None:
        '''Tunes'''
        self.client.main.tune()

    def tx(self) -> None:
        '''Puts the Fldigi into transmit mode'''
        self.client.main.tx()