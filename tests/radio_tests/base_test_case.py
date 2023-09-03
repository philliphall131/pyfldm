############################################################################
# 
#  File: base_test_case.py
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
from utilities.utilities import PrintColors

logger = logging.getLogger(__name__)

class BaseTestCase:
    '''Base Test Case for all other functional test cases to inherit from. Provides some built in logic
    to run tests of various input kinds, such as running all the tests in a module or just a single
    test function.
    '''

    def __init__(self) -> None:
        self.passing = 0
        self.name = self.__module__.split('.')[-1]

    def setup(self) -> None: ...
    def cleanup(self) -> None: ...
    def each_setup(self) -> None: ...
    def each_cleanup(self) -> None: ...

    def count_tests(self):
        '''Used to count up how many test functions there are in a module by counting how many
        functions begin wih 'test_'

        @return (int): number of test methods found
        '''
        test_methods = [func for func in self.__dir__() if 
                        func.startswith("test_")]
        return len(test_methods)

    def run_all_tests(self) -> None:
        '''Runs all the tests in the inherited module

        @return (int): the number of tests that passed
        '''
        self.init_logs()
        # gather up all the tests and run them
        test_methods = [func for func in self.__dir__() if 
                        func.startswith("test_")]
        self.setup()
            
        for test in test_methods:
            test_func = getattr(self, test)
            self.run_test(test_func)

        self.cleanup()
        self.finish_logs()
        return self.passing
    
    def run_one_test(self, func):
        '''Runs a single specified test within the module, with module levelsetup and cleanup. Assumes the user knows this function does actually exist in the module
        
        @param func(fn): the actual function to call
        @return (int): the number of passing tests (should be 1 or 0)
        '''
        self.name += f'.{func.__name__}'
        self.init_logs()
        self.setup()
        self.run_test(func)
        self.cleanup()
        self.finish_logs()
        return self.passing
    
    def run_test(self, func):
        '''Runs a single specified test within the module. Assumes the user knows this function does actually exist in the module
        
        @param func(fn): the actual function to call
        '''
        try:
            self.each_setup()
        except Exception:
            logger.error(f'{self.name}:{func.__name__}   Caught setup error in {func.__name__}. Bypassing this test case')
            return

        try:
            func()
            self.passing += 1
            logger.info(f'{self.name}:{func.__name__}   {PrintColors.GREEN.value}PASS{PrintColors.ENDC.value}')
        except AssertionError:
            logger.exception(f'{self.name}:{func.__name__}   {PrintColors.RED.value}FAIL{PrintColors.ENDC.value}')
            logger.info("")
        except Exception:
            logger.exception(f'{self.name}:{func.__name__}   {PrintColors.RED.value}ERROR{PrintColors.ENDC.value}')
            logger.info("")

        try:
            self.each_cleanup()
        except Exception as e:
            logger.error(f'{self.name}:{func.__name__}   Caught cleanup error in {func.__name__}.')
            raise e
    
    def init_logs(self):
        '''Initializes the testing logs'''
        logger.info(f'\n{PrintColors.PURPLE.value}======================== {self.name} Starting ========================{PrintColors.ENDC.value}')
    
    def finish_logs(self):
        '''Closes out the testing logs'''
        logger.info(f'\n{PrintColors.PURPLE.value}======================== {self.name} Finished ========================{PrintColors.ENDC.value}')
