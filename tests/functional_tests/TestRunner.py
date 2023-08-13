import logging
from utilities.utilities import PrintColors

class TestRunner:
    def __init__(self) -> None:
        self.logger = self.init_loggers()
        self.total_tests = 0
        self.passing_tests = 0

    def init_loggers(self):
        # init the pyfldm logger
        pyfldm_logger = logging.getLogger('pyfldm')
        pyfldm_logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        pyfldm_logger.addHandler(console_handler)

        testing_logger = logging.getLogger('functional_tests')
        testing_logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        testing_logger.addHandler(console_handler)

        return testing_logger

    def run(self, tests):
        for test in tests:
            self.total_tests += test.count_tests()

        self._init_test_logs()

        for test in tests:
            self.passing_tests += test.run_all_tests()
        
        self._finish_test_logs()

    def _init_test_logs(self):
        self.logger.info(f'\n{PrintColors.GREEN}======================== Starting Test Session ========================{PrintColors.ENDC}')
        self.logger.info(f'Found {self.total_tests} tests\n')
    
    def _finish_test_logs(self):
        self.logger.info(f'\n{PrintColors.YELLOW}========================     Test Results      ========================{PrintColors.ENDC}')
        self.logger.info(f'\t Test Results: Passed: {self.passing_tests}, Failed: {self.total_tests-self.passing_tests}, Total: {self.total_tests}')
        self.logger.info(f'{PrintColors.GREEN}======================== Test Session Finished ========================{PrintColors.ENDC}\n')
    
        
