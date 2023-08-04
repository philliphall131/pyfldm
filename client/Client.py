################################################################
# 
# File: Client.py
# Copyright(c) 2023, Phillip Hall. All rights reserved.
#
################################################################

import xmlrpc.client
from client.Fldigi import Fldigi
from client.IoConfig import IoConfig
from client.Main import Main

class Client:
    def __init__(self, hostname='127.0.0.1', port=7362) -> None:
        self.hostname = hostname
        self.port = port
        self.client = xmlrpc.client.ServerProxy(f'http://{self.hostname}:{self.port}/', allow_none=True)

        self.fldigi = Fldigi(self.client)
        self.io = IoConfig(self.client)
        self.main = Main(self.client)

    @property
    def methods(self):
        '''Returns the list of commands in which can be used to command Fldigi via the xmlrpc interface

        @return (list): the list of pyfldm commands corresponding to fldigi xmlrpc commands
        '''
        # TODO: refine to show actual python methods
        return "List of PyFldm methods"
        #return self.client.fldigi.list()

    