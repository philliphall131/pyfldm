################################################################
# 
#  File: Text.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
################################################################

from xmlrpc.client import ServerProxy

class Text:
    '''Houses the commands in the text group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> import pyfldm
    >>> client = pyfldm.Client()
    >>> client.text.
    
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

    def get_bandwidth(self) -> str:
        '''Gets the name of the current transceiver bandwidth
        
        @return (str): the bandwidth name
        '''
        return self.client.rig.get_bandwidth()
    
# text.add_tx	n:s	Adds a string to the TX text widget
# text.add_tx_bytes	n:6	Adds a byte string to the TX text widget
# text.clear_rx	n:n	Clears the RX text widget
# text.clear_tx	n:n	Clears the TX text widget
# text.get_rx	6:i	Returns a range of characters (start, length) from the RX text widget
# text.get_rx_length	i:n	Returns the number of characters in the RX widget