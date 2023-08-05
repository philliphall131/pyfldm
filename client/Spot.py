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
    >>> client.spot.toggle_auto()
    True
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

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
    
    