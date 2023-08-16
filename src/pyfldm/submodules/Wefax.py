############################################################################
# 
#  File: Wefax.py
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

class Wefax(BaseCall):
    '''Houses the commands in the wefax group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> from pyfldm.Client import Client
    >>> client = Client()
    >>> client.wefax.end_reception()
    "Success"
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client
    
    def __str__(self) -> str:
        return __name__.lower().split(".")[-1]

    def end_reception(self) -> str:
        '''End Wefax image reception
        
        @return (str): success message
        '''
        return self.client.wefax.end_reception()
    
    def get_received_file(self, max_delay_secs: int) -> str:
        '''Waits for next received fax file
        
        @param max_delay_secs(int): the max time in seconds to wait
        @return (str): success message, empty string if timeout
        '''
        return self.client.wefax.get_received_file(max_delay_secs)
    
    def send_file(self, max_delay_secs: int) -> str:
        '''Sends file
        
        @param max_delay_secs(int): the max time in seconds to wait
        @return (str): empty string if successful send, error message otherwise
        '''
        return self.client.wefax.send_file(max_delay_secs)
    
    def set_adif_log(self, reset: bool = False) -> str:
        '''Set/reset logging to received/transmit images to ADIF log file
        
        @param max_delay_secs(int): the max time in seconds to wait
        @return (str): empty string if successful send, error message otherwise
        '''
        return self.client.wefax.set_adif_log()
    
    def set_max_lines(self, max_lines: int) -> str:
        '''Set maximum lines for fax image reception
        
        @param max_lines(int): the max lines to set
        @return (str): empty string if successful send, error message otherwise
        '''
        return self.client.wefax.set_max_lines()
    
    def set_tx_abort_flag(self) -> str:
        '''Cancels Wefax image transmission
        
        @return (str): empty string if successful send, error message otherwise
        '''
        return self.client.wefax.set_tx_abort_flag()
    
    def skip_apt(self) -> str:
        '''Skip APT during Wefax reception
        
        @return (str): empty string if successful send, error message otherwise
        '''
        return self.client.wefax.skip_apt()
    
    def skip_phasing(self) -> str:
        '''Skip phasing during Wefax reception
        
        @return (str): empty string if successful send, error message otherwise
        '''
        return self.client.wefax.skip_phasing()
    
    def state_string(self) -> str:
        '''Gets the Wefax engine state (tx and rx) for information.
        
        @return (str): the engine state information
        '''
        return self.client.wefax.state_string()