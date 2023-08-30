############################################################################
# 
#  File: base_call.py
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

class BaseCall:
    '''Serves as a base class for each of the sub-namespaces of the xmlrpc API
    to house common functionality
    '''
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        pass

    def print_methods(self) -> None:
        '''Prints all the methods available for a specific group'''
        name = self.__str__()
        # name = self.__name__.lower().split(".")[-1]
        print("---------------------")
        print(f"client.{name} methods")
        print("---------------------")

        for method in self.get_methods():
            print(f'{name}.{method}')
        print()

    def get_methods(self) -> list:
        '''Gets all the methods available for a specific group
        
        @return (list): all the xmlrpc methods for a given group
        '''
        return [func for func in dir(self) if 
                    callable(getattr(self, func)) 
                    and not func.startswith("__") 
                    and func not in dir(BaseCall)
                    and func != 'client']