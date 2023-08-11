############################################################################
# 
#  File: IoConfig.py
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
from .BaseCall import BaseCall

logger = logging.getLogger(__name__)

class IoConfig(BaseCall):
    '''Houses the commands in the io group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.io that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> from pyfldm.Client import Client
    >>> client = Client()
    >>> client.io.in_use()
    1234
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

    def __str__(self) -> str:
        return __name__.lower().split(".")[-1]

    def enable_arq(self) -> None:
        '''Switch to ARQ I/O'''
        self.client.io.enable_arq()
    
    def enable_kiss(self) -> None:
        '''Switch to KISS I/O'''
        self.client.io.enable_kiss()
    
    def in_use(self) -> str:
        '''Gets the IO port in use (ARQ/KISS)

        @return (str): the IO port in use
        '''
        return self.client.io.in_use()