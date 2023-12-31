############################################################################
# 
#  File: testing_runner.py
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

import os
import sys
import re
import logging
import shutil
from datetime import datetime
from importlib import import_module
from .base_test_case import BaseTestCase
from utilities.utilities import PrintColors, LogOption, PrintColorsRegex

TEST_LOGS_DIR = "./test_logs"

class TestingRunner:
    def __init__(self, log_option = 0) -> None:
        self.total_tests = 0
        self.passing_tests = 0
        self.log_option = LogOption(log_option)
        self.log_file = self.get_file_name()
        self.logger = self._init_loggers()

    def _init_loggers(self):
        testing_logger = logging.getLogger('functional_tests')
        testing_logger.setLevel(logging.DEBUG)
        pyfldm_logger = logging.getLogger('pyfldm')
        pyfldm_logger.setLevel(logging.DEBUG)

        if self.log_option in [LogOption.CONSOLE_ONLY, LogOption.BOTH]:   
            console_handler1 = logging.StreamHandler()
            console_handler1.setLevel(logging.DEBUG)
            console_formatter1 = logging.Formatter('%(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
            console_handler1.setFormatter(console_formatter1)
            pyfldm_logger.addHandler(console_handler1)

            console_handler2 = logging.StreamHandler()
            console_handler2.setLevel(logging.DEBUG)
            console_formatter2 = logging.Formatter('%(message)s')
            console_handler2.setFormatter(console_formatter2)
            testing_logger.addHandler(console_handler2)

        if self.log_option in [LogOption.FILE_ONLY, LogOption.BOTH]:
            if not os.path.isdir(TEST_LOGS_DIR):
                os.mkdir(TEST_LOGS_DIR)
            
            file_handler1 = logging.FileHandler(f'{TEST_LOGS_DIR}/{self.log_file}')
            file_handler1.setLevel(logging.DEBUG)
            file_formatter1 = logging.Formatter('%(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
            file_handler1.setFormatter(file_formatter1)
            pyfldm_logger.addHandler(file_handler1)

            file_handler2 = logging.FileHandler(f'{TEST_LOGS_DIR}/{self.log_file}')
            file_handler2.setLevel(logging.DEBUG)
            file_formatter2 = logging.Formatter('%(message)s')
            file_handler2.setFormatter(file_formatter2)
            testing_logger.addHandler(file_handler2)

        return testing_logger
    
    def get_file_name(self):
        return datetime.now().strftime('%Y%m%d_%H%M%S_functional_test_result.log')

    def run(self, tests):
        if isinstance(tests, list):
            for test in tests:
                self.total_tests += test.count_tests()
            self._init_test_logs()
            for test in tests:
                if not isinstance(test, BaseTestCase):
                    self.logger.error(f"Cannot run {test}, not a child of BaseTestCase")
                try:
                    self.passing_tests += test.run_all_tests()
                except:
                    self.logger.exception(f'Failed while running: {test}')
                    
        elif isinstance(tests, BaseTestCase):
            self.total_tests += tests.count_tests()
            self._init_test_logs()
            try:
                self.passing_tests += tests.run_all_tests()
            except:
                self.logger.exception(f'Failed while running: {tests}')

        elif callable(tests):
            self.total_tests = 1
            self._init_test_logs()
            cls_name = tests.__qualname__.split('.')[0]
            module_name = tests.__module__.split('.')[-1]
            m = import_module('.' + module_name, 'functional_tests')
            cls_impl = getattr(m, cls_name)
            c = cls_impl()
            try:
                self.passing_tests += c.run_one_test(tests)
            except Exception:
                self.logger.exception(f'Failed while running: {tests}')
        
        self._finish_test_logs()

    def _init_test_logs(self):
        self.logger.info(f'\n{PrintColors.GREEN.value}======================== Starting Test Session ========================{PrintColors.ENDC.value}')
        self.logger.info(f'Found {self.total_tests} tests\n')
    
    def _finish_test_logs(self):
        self.logger.info(f'\n{PrintColors.YELLOW.value}========================     Test Results      ========================{PrintColors.ENDC.value}')
        self.logger.info(f'\t Test Results: Passed: {self.passing_tests}, Failed: {self.total_tests-self.passing_tests}, Total: {self.total_tests}')
        self.logger.info(f'{PrintColors.GREEN.value}======================== Test Session Finished ========================{PrintColors.ENDC.value}\n')

        if self.log_option in [LogOption.FILE_ONLY, LogOption.BOTH]:
            self._clean_log_file()
    
    def _clean_log_file(self):
        # windows wont let the script remove the file, so just skip cleaning it
        if sys.platform == "win32":
            return
        if not os.path.isfile(f'{TEST_LOGS_DIR}/{self.log_file}'):
            return
 
        with open(f'{TEST_LOGS_DIR}/{self.log_file}', 'r') as fin:
            with open(f'{TEST_LOGS_DIR}/tmp.log', 'w') as fout:
                for line in fin:
                    for color in PrintColorsRegex:
                        pattern = f'{color.value}'
                        line = re.sub(pattern, "", line)
                    fout.write(line)