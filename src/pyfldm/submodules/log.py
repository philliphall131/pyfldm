############################################################################
# 
#  File: Log.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#  USA
#
############################################################################

import logging
from xmlrpc.client import ServerProxy
from .base_call import BaseCall

logger = logging.getLogger(__name__)

class Log(BaseCall):
    '''Houses the commands in the log group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> from pyfldm.Client import Client
    >>> client = Client()
    >>> client.log.get_az()
    ABCD
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client
    
    def __str__(self) -> str:
        return f'log'

    def clear(self) -> None:
        '''Clears the contents of the log fields'''
        self.client.log.clear()
    
    def get_az(self) -> str:
        '''Gets the AZ field contents
        
        @return (str): the AZ field contents
        '''
        return self.client.log.get_az()
    
    def get_band(self) -> str:
        '''Gets the current band name
        
        @return (str): the current band name
        '''
        return self.client.log.get_band()
    
    def get_call(self) -> str:
        '''Gets the call field contents
        
        @return (str): the call field contents
        '''
        return self.client.log.get_call()
    
    def get_country(self) -> str:
        '''Gets the country field contents
        
        @return (str): the country field contents
        '''
        return self.client.log.get_country()
    
    def get_exchange(self) -> str:
        '''Gets the contest exchange field contents
        
        @return (str): the contest exchange field contents
        '''
        return self.client.log.get_exchange()
    
    def get_frequency(self) -> str:
        '''Gets the frequency field contents
        
        @return (str): the frequency field contents
        '''
        return self.client.log.get_frequency()
    
    def get_locator(self) -> str:
        '''Gets the locator field contents
        
        @return (str): the locator field contents
        '''
        return self.client.log.get_locator()
    
    def get_name(self) -> str:
        '''Gets the name field contents
        
        @return (str): the name field contents
        '''
        return self.client.log.get_name()
    
    def get_notes(self) -> str:
        '''Gets the notes field contents
        
        @return (str): the notes field contents
        '''
        return self.client.log.get_notes()
    
    def get_providence(self) -> str:
        '''Gets the providence field contents
        
        @return (str): the providence field contents
        '''
        return self.client.log.get_providence()
    
    def get_qth(self) -> str:
        '''Gets the Qth field contents
        
        @return (str): the Qth field contents
        '''
        return self.client.log.get_qth()
    
    def get_rst_in(self) -> str:
        '''Gets the RST(r) field contents
        
        @return (str): the RST(r) field contents
        '''
        return self.client.log.get_rst_in()
    
    def get_rst_out(self) -> str:
        '''Gets the RST(s) field contents
        
        @return (str): the RST(s) field contents
        '''
        return self.client.log.get_rst_out()
    
    def get_serial_number(self) -> str:
        '''Gets the serial number field contents
        
        @return (str): the serial number field contents
        '''
        return self.client.log.get_serial_number()
    
    def get_serial_number_sent(self) -> str:
        '''Gets the serial number (sent) field contents
        
        @return (str): the serial number (sent) field contents
        '''
        return self.client.log.get_serial_number_sent()
    
    def get_state(self) -> str:
        '''Gets the state field contents
        
        @return (str): the state field contents
        '''
        return self.client.log.get_state()

    def get_time_off(self) -> str:
        '''Gets the Time-off field contents
        
        @return (str): the time-off field contents
        '''
        return self.client.log.get_time_off()
    
    def get_time_on(self) -> str:
        '''Gets the Time-on field contents
        
        @return (str): the time-on field contents
        '''
        return self.client.log.get_time_on()
    
    def set_call(self, call_str: str) -> None:
        '''Sets the call field contents
        
        @param call_str(str): the string to populate in the call field
        '''
        self.client.log.set_call(call_str)
    
    def set_exchange(self, exchange_str: str) -> None:
        '''Sets the contest exchange field contents
        
        @param exchange_str(str): the string to populate in the contest exchange field
        '''
        self.client.log.set_exchange(exchange_str)

    def set_locator(self, locator_str: str) -> None:
        '''Sets the locator field contents
        
        @param locator_str(str): the string to populate in the locator field
        '''
        self.client.log.set_locator(locator_str)
    
    def set_name(self, name_str: str) -> None:
        '''Sets the name field contents
        
        @param name_str(str): the string to populate in the name field
        '''
        self.client.log.set_name(name_str)

    def set_name(self, name_str: str) -> None:
        '''Sets the name field contents
        
        @param name_str(str): the string to populate in the name field
        '''
        self.client.log.set_name(name_str)
    
    def set_qth(self, qth_str) -> None:
        '''Sets the Qth field contents
        
        @param qth_str(str): the string to populate in the Qth field
        '''
        self.client.log.set_qth(qth_str)

    def set_rst_in(self, rst_in_str) -> None:
        '''Sets the RST(r) field contents
        
        @param rst_in_str(str): the string to populate in the RST(r) field
        '''
        self.client.log.set_rst_in(rst_in_str)
    
    def set_rst_out(self, rst_out_str: str) -> None:
        '''Sets the RST(s) field contents
        
        @param rst_out_str(str): the string to populate in the RST(s) field
        '''
        self.client.log.set_rst_out(rst_out_str)

    def set_serial_number(self, serial_number_str: str) -> None:
        '''Sets the serial number field contents
        
        @param serial_number_str(str): the string to populate in the serial number field
        '''
        self.client.log.set_serial_number(serial_number_str)
