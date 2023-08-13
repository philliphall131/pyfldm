import logging
from utilities.utilities import PrintColors

logger = logging.getLogger(__name__)

class BaseTestCase:
    def __init__(self) -> None:
        self.passing = 0
        self.name = self.__module__.split('.')[-1]

    def setup(self) -> None:
        pass

    def cleanup(self) -> None:
        pass

    def each_setup(self) -> None:
        pass

    def each_cleanup(self) -> None:
        pass

    def count_tests(self):
        test_methods = [func for func in self.__dir__() if 
                        func.startswith("test_")]
        return len(test_methods)

    def run_all_tests(self) -> None:
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
        self.name += f'.{func.__name__}'
        self.init_logs()
        self.setup()
        
        self.run_test(func)

        self.cleanup()
        self.finish_logs()
        return self.passing
    
    def run_test(self, func):
        self.each_setup()
        try:
            func()
            self.passing += 1
            logger.info(f'{self.name}:{func.__name__}   {PrintColors.GREEN.value}PASS{PrintColors.ENDC.value}')
        except AssertionError:
            logger.exception(f'{self.name}:{func.__name__}   {PrintColors.RED.value}FAIL{PrintColors.ENDC.value}')
            logger.info("")
        except:
            logger.exception(f'{self.name}:{func.__name__}   {PrintColors.RED.value}ERROR{PrintColors.ENDC.value}')
            logger.info("")
        self.each_cleanup()

    
    def init_logs(self):
        logger.info(f'\n{PrintColors.PURPLE.value}======================== {self.name} Starting ========================{PrintColors.ENDC.value}')
    
    def finish_logs(self):
        logger.info(f'\n{PrintColors.PURPLE.value}======================== {self.name} Finished ========================{PrintColors.ENDC.value}')
