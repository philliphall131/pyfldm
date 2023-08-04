################################################################
# 
#  File: Wefax.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
################################################################

from xmlrpc.client import ServerProxy

class Wefax:
    '''Houses the commands in the wefax group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> import pyfldm
    >>> client = pyfldm.Client()
    >>> client.wefax.
    
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

    def get_bandwidth(self) -> str:
        '''Gets the name of the current transceiver bandwidth
        
        @return (str): the bandwidth name
        '''
        return self.client.rig.get_bandwidth()

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