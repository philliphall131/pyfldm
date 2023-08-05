############################################################################
# 
#  File: Rig.py
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

from xmlrpc.client import ServerProxy

class Rig:
    '''Houses the commands in the rig group in the XML-RPC spec for fldigi.
    Reference: http://www.w1hkj.com/FldigiHelp/xmlrpc_control_page.html

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference Client.py which has an attribute self.log that interfaces these methods.

    @param client(xmlrpc.client.ServerProxy): a ServerProxy client object used to make http requests via the fldigi xmlrpc api
    
    Example use:
    >>> import pyfldm
    >>> client = pyfldm.Client()
    >>> client.rig.get_bandwidth()
    12345
    '''
    def __init__(self, client: ServerProxy) -> None:
        self.client = client

    def get_bandwidth(self) -> str:
        '''Gets the name of the current transceiver bandwidth
        
        @return (str): the bandwidth name
        '''
        return self.client.rig.get_bandwidth()
    
    def get_bandwidths(self) -> list:
        '''Gets the list of available rig bandwidths
        
        @return (list): the list of available rig bandwidths
        '''
        return self.client.rig.get_bandwidths()
    
    def get_mode(self) -> str:
        '''Gets the name of the current transceiver mode
        
        @return (str): the name of the current transceiver mode
        '''
        return self.client.rig.get_mode()
    
    def get_modes(self) -> list:
        '''Gets the list of available rig modes
        
        @return (list): the list of available rig modes
        '''
        return self.client.rig.get_modes()
    
    def get_name(self) -> str:
        '''Gets the rig name previously set via rig.set_name
        
        @return (str): the rig name previously set via rig.set_name
        '''
        return self.client.rig.get_name()
    
    def get_notch(self) -> str:
        '''Reports a notch filter frequency based on WF action
        
        @return (str): the report
        '''
        return self.client.rig.get_notch()
    
    def release_control(self) -> None:
        '''Switches rig control to previous setting'''
        self.client.rig.release_control()

    def set_bandwidth(self, new_bandwidth: str) -> None:
        '''Selects a bandwidth previously added by rig.set_bandwidths
        
        @param new_bandwidth(str): the new bandwidth to select
        '''
        self.client.rig.set_bandwidth(new_bandwidth)

    def set_bandwidths(self, bandwidths: list) -> None:
        '''Sets the list of available rig bandwidths
        
        @param bandwidths(list): a list of bandwidths
        '''
        self.client.rig.set_bandwidths(bandwidths)

    def set_frequency(self, new_frequency: float) -> float:
        '''Sets the RF carrier frequency
        
        @param new_frequency(float): the new carrier frequency
        @return (float): the old frequency
        '''
        self.client.rig.set_frequency(new_frequency)

    def set_mode(self, new_mode: str) -> None:
        '''Selects a mode previously added by rig.set_modes
        
        @param new_mode(str): the new mode to set
        '''
        self.client.rig.set_mode(new_mode)

    def set_modes(self, new_modes: list) -> None:
        '''Sets the list of available rig modes
        
        @param new_modes(list): the list of rig modes
        '''
        self.client.rig.set_modes(new_modes)

    def set_name(self, new_name: str) -> None:
        '''Sets the rig name for xmlrpc rig
        
        @param new_name(str): the name to set
        '''
        self.client.rig.set_name(new_name)

    def set_pwrmeter(self, new_value: int) -> None:
        '''Sets the power meter
        
        @param new_value(int): the value to set
        '''
        self.client.rig.set_pwrmeter(new_value)

    def set_smeter(self, new_value: int) -> None:
        '''Sets the smeter
        
        @param new_value(int): the value to set
        '''
        self.client.rig.set_smeter(new_value)

    def take_control(self) -> None:
        '''Switches rig control to XML-RPC'''
        self.client.rig.take_control()