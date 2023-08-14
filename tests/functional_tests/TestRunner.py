import os
import re
import logging
import shutil
from datetime import datetime
from importlib import import_module
from .BaseTestCase import BaseTestCase
from utilities.utilities import PrintColors, LogOption, PrintColorsRegex

TEST_LOGS_DIR = "./test_logs"

class TestRunner:
    def __init__(self, log_option = 0) -> None:
        self.total_tests = 0
        self.passing_tests = 0
        self.log_option = LogOption(log_option)
        self.log_file = self.get_file_name()
        self.logger = self.init_loggers()

    def init_loggers(self):
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
        return datetime.now().strftime('%Y%m%d_%H%M%S_test_result.log')

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
            self.passing_tests += tests.run_all_tests()
        elif callable(tests):
            self.total_tests = 1
            self._init_test_logs()
            cls_name = tests.__qualname__.split('.')[0]
            m = import_module('.' + cls_name, 'functional_tests')
            cls_impl = getattr(m, cls_name)
            c = cls_impl()
            try:
                self.passing_tests += c.run_one_test(tests)
            except:
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
        if not os.path.isfile(f'{TEST_LOGS_DIR}/{self.log_file}'):
            return
        
        with open(f'{TEST_LOGS_DIR}/{self.log_file}', 'r') as fin:
            with open(f'{TEST_LOGS_DIR}/tmp.log', 'w') as fout:
                for line in fin:
                    for color in PrintColorsRegex:
                        pattern = f'{color.value}'
                        line = re.sub(pattern, "", line)
                    fout.write(line)

        
        os.remove(f'{TEST_LOGS_DIR}/{self.log_file}')  
        shutil.move(f'{TEST_LOGS_DIR}/tmp.log', f'{TEST_LOGS_DIR}/{self.log_file}')
    
        
