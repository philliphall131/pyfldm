############################################################################
# 
#  File: Navtex.py
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

class Navtex(BaseCall):
    '''Houses the commands in the navtex group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> from pyfldm.Client import Client
    >>> client = Client()
    >>> client.navtex.get_message()
    ABCD
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

    def __str__(self) -> str:
        return __name__.lower().split(".")[-1]

    def get_message(self, max_delay_secs: int) -> str:
        '''Gets the next Navtex/SitorB message
        
        @param max_delay_secs(int): the max delay in seconds
        @return (str): the next Navtex/SitorB message, empty string if max delay reached with no message
        '''
        return self.client.navtex.get_message(max_delay_secs)
    
    def send_message(self, message: str) -> str:
        '''Sends a Navtex/SitorB message
        
        @param message(str): the message to send
        @return (str): empty string if send was good, error message otherwise
        '''
        return self.client.navtex.send_message(message)