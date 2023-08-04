################################################################
# 
#  File: Main.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
################################################################

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
    
    def get_char_timing(self, char_bytes) -> str:
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
    
    def get_trx_timing(self, bitmask) -> str:
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

# main.set_afc	b:b	Sets the AFC state. Returns the old state
# main.set_frequency	d:d	Sets the RF carrier frequency. Returns the old value
# main.set_lock	b:b	Sets the Transmit Lock state. Returns the old state
# main.set_reverse	b:b	Sets the Reverse Sideband state. Returns the old state
# main.set_rsid	b:b	Sets the RSID state. Returns the old state
# mmain.set_txid	b:b	Sets the TxRSID state. Returns the old state
# main.set_squelch	b:b	Sets the squelch state. Returns the old state
# main.set_squelch_level	d:d	Sets the squelch level. Returns the old level
# main.set_wf_sideband	n:s	Sets the waterfall sideband to USB or LSB
# main.toggle_afc	b:n	Toggles the AFC state. Returns the new state
# main.toggle_lock	b:n	Toggles the Transmit Lock state. Returns the new state
# main.toggle_reverse	b:n	Toggles the Reverse Sideband state. Returns the new state
# main.toggle_rsid	b:n	Toggles the RSID state. Returns the new state
# main.toggle_txid	b:n	Toggles the TxRSID state. Returns the new state
# main.toggle_squelch	b:n	Toggles the squelch state. Returns the new state
# main.tune	n:n	Tunes
# main.tx	n:n	Transmits
