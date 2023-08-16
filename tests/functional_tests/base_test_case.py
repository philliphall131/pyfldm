import logging
from utilities.utilities import PrintColors

logger = logging.getLogger(__name__)

class BaseTestCase:
    def __init__(self) -> None:
        self.passing = 0
        self.name = self.__module__.split('.')[-1]

    def setup(self) -> None: ...

    def cleanup(self) -> None: ...

    def each_setup(self) -> None: ...

    def each_cleanup(self) -> None: ...

    def count_tests(self):
        test_methods = [func for func in self.__dir__() if 
                        func.startswith("test_")]
        return len(test_methods)

    def run_all_tests(self) -> None:
        self.init_logs()
        # gather up all the tests and run them
        test_methods = [func for func in self.__dir__() if 
                        func.startswith("test_")]
        try:
            self.setup()
            
            for test in test_methods:
                test_func = getattr(self, test)
                try:
                    self.run_test(test_func)
                except:
                    logger.error(f"Error in {test_func}, moving on to next test")

            self.cleanup()
        except:
            logger.error("Error in run_all_tests")
        self.finish_logs()
        return self.passing
    
    def run_one_test(self, func):
        self.name += f'.{func.__name__}'
        self.init_logs()
        try:
            self.setup()
            
            self.run_test(func)

            self.cleanup()
        except:
            logger.error("Error in run_one_test")
        self.finish_logs()
        return self.passing
    
    def run_test(self, func):
        try:
            self.each_setup()
        except Exception as e:
            logger.error(f'{self.name}:{func.__name__}   Caught setup error in {func.__name__}. Bypassing this test case')
            return

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

        try:
            self.each_cleanup()
        except Exception as e:
            logger.error(f'{self.name}:{func.__name__}   Caught cleanup error in {func.__name__}.')
            raise e
    
    def init_logs(self):
        logger.info(f'\n{PrintColors.PURPLE.value}======================== {self.name} Starting ========================{PrintColors.ENDC.value}')
    
    def finish_logs(self):
        logger.info(f'\n{PrintColors.PURPLE.value}======================== {self.name} Finished ========================{PrintColors.ENDC.value}')
