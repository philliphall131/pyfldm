############################################################################
# 
#  File: Client.py
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

import xmlrpc.client
from .submodules.Fldigi import Fldigi
from .submodules.IoConfig import IoConfig
from .submodules.Main import Main
from .submodules.Modem import Modem
from .submodules.Navtex import Navtex
from .submodules.Rig import Rig
from .submodules.Spot import Spot
from .submodules.Text import Text
from .submodules.Wefax import Wefax

class Client:
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

    @property
    def methods(self):
        '''Returns the list of commands in which can be used to command Fldigi via the xmlrpc interface

        @return (list): the list of pyfldm commands corresponding to fldigi xmlrpc commands
        '''
        # TODO: refine to show actual python methods
        return "List of PyFldm methods"
        #return self.client.fldigi.list()


    