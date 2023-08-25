############################################################################
# 
#  File: text.py
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

logger = logging.getLogger(__name__)

class Text(BaseCall):
    '''Houses the commands in the text group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    # * assuming that Fldigi is already running
    >>> from pyfldm.client import Client
    >>> client = Client()
    >>> client.text.get_rx(1,2)
    AB
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client
    
    def __str__(self) -> str:
        return __name__.lower().split(".")[-1]

    def get_rx_data(self) -> bytes:
        '''Gets all RX data received since last query
        
        @return (bytes): the data since last query
        '''
        return self.client.rx.get_data()
    
    def get_rxtx_data(self) -> bytes:
        '''Gets all RXTX combined data since last query
        
        @return (bytes): the data since last query
        '''
        return self.client.rxtx.get_data()
    
    def get_tx_data(self) -> bytes:
        '''Gets all TX data received since last query
        
        @return (bytes): the data since last query
        '''
        return self.client.tx.get_data()
    
    def add_tx(self, text) -> None:
        '''Adds a string to the TX text widget
        
        @param text(str): the text to add to the TX widget
        '''
        self.client.text.add_tx(text)

    def add_tx_bytes(self, byte_str: bytes) -> None:
        '''Adds a byte string to the TX text widget
        
        @param byte_str(str): the byte string to add to the TX widget
        '''
        if type(byte_str) != bytes:
            raise TypeError("Must pass in type bytes")
        self.client.text.add_tx_bytes(byte_str)

    def clear_rx(self) -> None:
        '''Clears the RX text widget'''
        self.client.text.clear_rx()

    def clear_tx(self) -> None:
        '''Clears the TX text widget'''
        self.client.text.clear_tx()

    def get_rx(self, start: int, length: int) -> bytes:
        '''Gets a range of characters (start, length) from the RX text widget
        
        @param start(int): the index of the starting character
        @param length(int): the number of characters to get
        @return (bytes): the requested range of characters in a byte string
        '''
        return self.client.text.get_rx(start, length)

    def get_rx_length(self) -> int:
        '''Gets the number of characters in the RX widget
        
        @return (int): the number of characters in the RX widget
        '''
        return self.client.text.get_rx_length()