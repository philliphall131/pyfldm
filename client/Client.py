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
from client.Modem import Modem
from client.Navtex import Navtex
from client.Rig import Rig
from client.Spot import Spot
from client.Text import Text
from client.Wefax import Wefax

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


# wefax.end_reception	s:n	End Wefax image reception
# wefax.get_received_file	s:i	Waits for next received fax file, returns its name with
# a delay. Empty string if timeout.
# wefax.send_file	s:i	Send file. returns an empty string if OK otherwise an error message.
# wefax.set_adif_log	s:b	Set/reset logging to received/transmit images to ADIF log file
# wefax.set_max_lines	s:i	Set maximum lines for fax image reception
# wefax.set_tx_abort_flag	s:n	Cancels Wefax image transmission
# wefax.skip_apt	s:n	Skip APT during Wefax reception
# wefax.skip_phasing	s:n	Skip phasing during Wefax reception
# wefax.state_string	s:n	Returns Wefax engine state (tx and rx) for information.

    