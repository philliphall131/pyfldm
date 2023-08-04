################################################################
# 
#  File: Fldigi.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
################################################################

from xmlrpc.client import ServerProxy

class Fldigi:
    '''Houses the commands in the fldigi group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.fldigi that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> import pyfldm
    >>> client = pyfldm.Client()
    >>> client.fldigi.name()
    fldigi
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

    def name(self) -> str:
        '''Get the program name

        @return (str): the program name
        '''
        return self.client.fldigi.name()
    
    def name_and_version(self) -> str:
        '''Get the program name and version

        @return(str): the program name and version
        '''
        return self.client.fldigi.name_version()
    
    def list(self) -> list:
        '''Gets the list of Fldigi xmlrpc methods

        @return(list[dict]): the list of Fldigi xmlrpc methods expressed as an array of dicts
        '''
        return self.client.fldigi.name_version()
    
    def version(self) -> str:
        '''Gets the program version

        @return (str): the program version
        '''
        return self.client.fldigi.version()
    
    def version_struct(self) -> dict:
        '''Returns the program version as a dict structure

        @return (dict): the program version
        '''
        return self.client.fldigi.version_struct()
    
    def config_dir(self) -> str:
        '''Returns the name of the configuration directory

        @return (str): the config directory
        '''
        return self.client.fldigi.config_dir()
    
    def terminate(self, save_options=True, save_log=True, save_macros=True) -> None:
        '''***CAUTION***
        Terminates fldigi. Only use this if you are sure of what you are doing.
        If using AppMonitor, use care with this method as it may interfere with
        the proper flow intended for AppMonitor
        Arguements are sent as a bitmask specifying data to save: 
        0=options; 1=log; 2=macros

        @param save_options(bool): True to save options; False otherwise
        @param save_log(bool): True to save log; False otherwise
        @param save_macros(bool): True to save macros; False otherwise
        '''
        bitmask = int(f'0b{int(save_macros)}{int(save_log)}{int(save_options)}')
        self.client.fldigi.terminate(bitmask)