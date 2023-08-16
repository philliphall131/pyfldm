############################################################################
# 
#  File: Spot.py
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

class Spot(BaseCall):
    '''Houses the commands in the spot group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> from pyfldm.Client import Client
    >>> client = Client()
    >>> client.spot.toggle_auto()
    True
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client
    
    def __str__(self) -> str:
        return __name__.lower().split(".")[-1]

    def get_auto(self) -> bool:
        '''Gets the autospotter state
        
        @return (bool): the autospotter state
        '''
        return self.client.spot.get_auto()
    
    def get_pskrep_count(self) -> int:
        '''Gets the number of callsigns spotted in the current session
        
        @return (int): the number of callsigns
        '''
        return self.client.spot.pskrep.get_count()
    
    def set_auto(self, new_state: bool) -> bool:
        '''Sets the autospotter state
        
        @param new_state(bool): the new autospotter state
        @return (bool): the old state
        '''
        return self.client.spot.set_auto(new_state)
    
    def toggle_auto(self) -> bool:
        '''Toggles the autospotter state
        
        @return (bool): the new state
        '''
        return self.client.spot.toggle_auto()
    
    