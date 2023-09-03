############################################################################
# 
#  File: modem.py
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

import logging
from xmlrpc.client import ServerProxy
from .base_call import BaseCall

class Modem(BaseCall):
    '''Houses the commands in the Modem group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference client.py which has an attribute self.modem that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    # * assuming that Fldigi is already running
    >>> from pyfldm.client import Client
    >>> client = Client()
    >>> client.modem.get_carrier()
    1234
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client
        self.logger = logging.getLogger(__name__)
    
    def __str__(self) -> str:
        return __name__.lower().split(".")[-1]

    def get_afc_search_range(self) -> int:
        '''Gets the modem AFC search range
        
        @return (int): the modem AFC search range
        '''
        return self.client.modem.get_afc_search_range()

    def get_bandwidth(self) -> int:
        '''Gets the modem bandwidth
        
        @return (int): the modem bandwidth
        '''
        return self.client.modem.get_bandwidth()

    def get_carrier(self) -> int:
        '''Gets the modem carrier frequency
        
        @return (int): the modem carrier frequency
        '''
        return self.client.modem.get_carrier()

    def get_id(self) -> int:
        '''Gets the ID of the current modem
        
        @return (int): the ID of the current modem
        '''
        return self.client.modem.get_id()

    def get_max_id(self) -> int:
        '''Gets the maximum modem ID number
        
        @return (int): the maximum modem ID number
        '''
        return self.client.modem.get_max_id()
    
    def get_name(self) -> list:
        '''Gets the current modem name
        
        @return (str): the current modem name
        '''
        return self.client.modem.get_name()

    def get_names(self) -> list:
        '''Gets the modem names
        
        @return (list): a list of all modem names
        '''
        return self.client.modem.get_names()

    def get_quality(self) -> float:
        '''Gets the modem signal quality in the range [0:100]
        
        @return (float): the modem signal quality
        '''
        return self.client.modem.get_quality()

    def increment_afc_search_range(self, amount:int ) -> int:
        '''Increments the modem AFC search range
        
        @param amount(int): the amount to increase the afc search range
        @return (int): the new value
        '''
        return self.client.modem.inc_afc_search_range(int(amount))

    def increment_bandwidth(self, amount: int) -> int:
        '''Increments the modem bandwidth
        
        @param amount(int): the amount to increase the bandwidth
        @return (int): the new value
        '''
        return self.client.modem.inc_bandwidth(int(amount))
    
    def increment_carrier(self, amount: int) -> int:
        '''Increments the modem carrier frequency
        
        @param amount(int): the amount to increase the frequency
        @return (int): the new carrier frequency
        '''
        return self.client.modem.inc_carrier(int(amount))
    
    def get_olivia_bandwidth(self) -> int:
        '''Gets the Olivia bandwidth
        
        @return (int): the Olivia bandwidth
        '''
        return self.client.modem.olivia.get_bandwidth()
    
    def get_olivia_tones(self) -> int:
        '''Gets the Olivia tones
        
        @return (int): the Olivia tones
        '''
        return self.client.modem.olivia.get_tones()
    
    def set_olivia_tones(self, new_tone: int) -> None:
        '''Sets the Olivia tones. Available values [2, 4, 8, 16, 32, 64, 128, 256]
        
        @param new_tone(int): the new Olivia tones value
        '''
        tone = int(new_tone)
        if tone not in [2, 4, 8, 16, 32, 64, 128, 256]:
            raise ValueError("Must be one of these values: 2, 4, 8, 16, 32, 64, 128, 256")
        self.client.modem.olivia.set_tones(tone)

    def set_olivia_bandwidth(self, new_bandwidth: int) -> None:
        '''Sets the Olivia bandwidth. Available values [125, 250, 500, 1000, 2000]
        
        @param new_bandwidth(int): the new Olivia bandwidth value
        '''
        bandwidth = int(new_bandwidth)
        if bandwidth not in [125, 250, 500, 1000, 2000]:
            raise ValueError("Must be one of these values: 125, 250, 500, 1000, 2000")
        self.client.modem.olivia.set_bandwidth(bandwidth)

    def search_down(self) -> None:
        '''Searches downward in frequency'''
        self.client.modem.search_down()

    def search_up(self) -> None:
        '''Searches upward in frequency'''
        self.client.modem.search_up()

    def set_afc_search_range(self, new_value: int) -> int:
        '''Sets the modem AFC search range
        
        @param new_value (int): the modem AFC search range value
        @return (int): the old value
        '''
        return self.client.modem.set_afc_search_range(new_value)
    
    def set_bandwidth(self, new_value: int) -> int:
        '''Sets the modem bandwidth
        
        @param new_value (int): the modem bandwidth value
        @return (int): the old value
        '''
        return self.client.modem.set_bandwidth(new_value)
    
    def set_by_id(self, new_modem: int) -> int:
        '''Sets the current modem
        
        @param new_modem (int): the new modem id
        @return (int): the old modem id
        '''
        return self.client.modem.set_by_id(new_modem)
    
    def set_by_name(self, new_modem: str) -> str:
        '''Sets the current modem
        
        @param new_modem (str): the new modem name
        @return (str): the old modem name
        '''
        return self.client.modem.set_by_name(new_modem)
    
    def set_carrier(self, new_carrier: int) -> int:
        '''Sets the modem carrier
        
        @param new_carrier (int): the new modem carrier
        @return (int): the old carrier
        '''
        return self.client.modem.set_carrier(new_carrier)