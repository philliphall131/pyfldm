################################################################
# 
#  File: Fldigi.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
################################################################

from xmlrpc.client import ServerProxy

class Log:
    '''Houses the commands in the log group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> import pyfldm
    >>> client = pyfldm.Client()
    >>> client.log.get_az()
    ABCD
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

    def clear(self) -> None:
        '''Clears the contents of the log fields'''
        return self.client.log.clear()
    
    def get_az(self) -> str:
        '''Gets the AZ field contents
        
        @return (str): the AZ field contents
        '''
        return self.client.log.clear()
    
# log.get_band	s:n	Returns the current band name
# log.get_call	s:n	Returns the Call field contents
# log.get_country	s:n	Returns the Country field contents
# log.get_exchange	s:n	Returns the contest exchange field contents
# log.get_frequency	s:n	Returns the Frequency field contents
# log.get_locator	s:n	Returns the Locator field contents
# log.get_name	s:n	Returns the Name field contents
# log.get_notes	s:n	Returns the Notes field contents
# log.get_province	s:n	Returns the Province field contents
# log.get_qth	s:n	Returns the QTH field contents
# log.get_rst_in	s:n	Returns the RST(r) field contents
# log.get_rst_out	s:n	Returns the RST(s) field contents
# log.get_serial_number	s:n	Returns the serial number field contents
# log.get_serial_number_sent	s:n	Returns the serial number (sent) field contents
# log.get_state	s:n	Returns the State field contents
# log.get_time_off	s:n	Returns the Time-Off field contents
# log.get_time_on	s:n	Returns the Time-On field contents
# log.set_call	n:s	Sets the Call field contents
# log.set_exchange	n:s	Sets the contest exchange field contents
# log.set_locator	n:s	Sets the Locator field contents
# log.set_name	n:s	Sets the Name field contents
# log.set_qth	n:s	Sets the QTH field contents
# log.set_rst_in	n:s	Sets the RST(r) field contents
# log.set_rst_out	n:s	Sets the RST(s) field contents
# log.set_serial_number	n:s	Sets the serial number field contents