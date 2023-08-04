################################################################
# 
#  File: Spot.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
################################################################

from xmlrpc.client import ServerProxy

class Spot:
    '''Houses the commands in the spot group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> import pyfldm
    >>> client = pyfldm.Client()
    >>> client.spot.
    
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

    def get_bandwidth(self) -> str:
        '''Gets the name of the current transceiver bandwidth
        
        @return (str): the bandwidth name
        '''
        return self.client.rig.get_bandwidth()
    
# spot.get_auto	b:n	Returns the autospotter state
# spot.pskrep.get_count	i:n	Returns the number of callsigns spotted in the current session
# spot.set_auto	n:b	Sets the autospotter state. Returns the old state
# spot.toggle_auto	n:b	Toggles the autospotter state. Returns the new state
    
    