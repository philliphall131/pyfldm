############################################################################
# 
#  File: client.py
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
import xmlrpc.client
from .submodules.fldigi import Fldigi
from .submodules.ioconfig import IoConfig
from .submodules.main import Main
from .submodules.modem import Modem
from .submodules.navtex import Navtex
from .submodules.rig import Rig
from .submodules.spot import Spot
from .submodules.text import Text
from .submodules.wefax import Wefax

logger = logging.getLogger(__name__)

class Client:

    ''' Client serves as the client side connection to Fldigi via the xmlrpc API. 
    This is the main worker for the pyfldm library and facilitates all the xmlrpx 
    calls available to Fldigi

    @param hostname(str): the IP address of the xmlrpc server to connect to
    @param port(int): the port number of the xmlrpc server connection
    
    Example use:
    # * assuming that Fldigi is already running
    >>> from pyfldm.client import Client
    >>> c = Client()
    >>> methods = c.get_all_methods()
    >>> print(methods[0])
    {'fldigi': ['config_dir', 'list', 'name', 'name_and_version', 'terminate', 'version', 'version_struct']}
    >>> c.print_all_methods()
    ---------------------
    client.fldigi methods
    ---------------------
    fldigi.config_dir
    fldigi.list
    ...
    '''

    def __init__(self, hostname='127.0.0.1', port=7362) -> None:
        self.hostname = hostname
        self.port = port
        self.client = xmlrpc.client.ServerProxy(f'http://{self.hostname}:{self.port}/', allow_none=True)

        self.fldigi = Fldigi(self.client)
        self.io = IoConfig(self.client)
        self.main = Main(self.client)
        self.modem = Modem(self.client)
        self.navtex = Navtex(self.client)
        self.rig = Rig(self.client)
        self.spot = Spot(self.client)
        self.text = Text(self.client)
        self.wefax = Wefax(self.client)
        self._sub_clients = [
            self.fldigi,
            self.io,
            self.main,
            self.modem,
            self.navtex,
            self.rig,
            self.spot,
            self.text,
            self.wefax
        ]

        logger.info(f"Setup Fldigi client on {hostname}:{port}")

    def get_all_methods(self) -> list:
        '''Returns the list of commands in which can be used to command Fldigi via the xmlrpc interface
        Formatted as a list containing a dict entry for each client namespace, for example:
        
        [ {'fldigi': [<fldigi methods>]}, ... ]

        @return (list): the list of pyfldm commands corresponding to fldigi xmlrpc commands
        '''
        methods_list = []
        for sub in self._sub_clients:
            methods_list.append({
                sub.__str__(): sub.get_methods()
            })
        return methods_list
    
    def print_all_methods(self) -> None:
        '''Prints the list of commands in which can be used to command Fldigi via the xmlrpc interface'''
        
        for sub in self._sub_clients:
            sub.print_methods()


    