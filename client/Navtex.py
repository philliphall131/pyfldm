################################################################
# 
#  File: Navtex.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
################################################################

from xmlrpc.client import ServerProxy

class Navtex:
    '''Houses the commands in the navtex group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> import pyfldm
    >>> client = pyfldm.Client()
    >>> client.navtex.get_message()
    ABCD
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

    def get_message(self, max_delay_secs: int) -> str:
        '''Gets the next Navtex/SitorB message
        
        @param max_delay_secs(int): the max delay in seconds
        @return (str): the next Navtex/SitorB message, empty string if max delay reached with no message
        '''
        return self.client.navtex.get_message(max_delay_secs)
    
    def send_message(self, message: str) -> str:
        '''Sends a Navtex/SitorB message
        
        @param message(str): the message to send
        @return (str): empty string if send was good, error message otherwise
        '''
        return self.client.navtex.send_message(message)