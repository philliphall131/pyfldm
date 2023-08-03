################################################################
# 
#  File: IoConfig.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
################################################################

from xmlrpc.client import ServerProxy

class IoConfig:
    '''Houses the commands in the io group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.io that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> import pyfldm
    >>> client = pyfldm.Client()
    >>> client.io.in_use()
    1234
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

# io.in_use	s:n	Returns the IO port in use (ARQ/KISS).

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