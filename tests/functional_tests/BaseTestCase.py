import logging
from utilities.utilities import PrintColors

logger = logging.getLogger(__name__)

class BaseTestCase:
    def __init__(self) -> None:
        self.passing = 0

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
        name = self.__module__.split('.')[-1]
        self.init_logs(name)
        # gather up all the tests and run them
        test_methods = [func for func in self.__dir__() if 
                        func.startswith("test_")]

        self.setup()
        
        for test in test_methods:
            test_func = getattr(self, test)
            self.each_setup()
            try:
                test_func()
                self.passing += 1
                logger.info(f'{name}:{test}   {PrintColors.GREEN}PASS{PrintColors.ENDC}')
            except AssertionError:
                logger.exception(f'{name}:{test}   {PrintColors.RED}FAIL{PrintColors.ENDC}')
                logger.info("")
            except:
                logger.exception(f'{name}:{test}   {PrintColors.RED}ERROR{PrintColors.ENDC}')
                logger.info("")
            self.each_cleanup()

        self.cleanup()
        self.finish_logs(name)
        return self.passing
    
    def init_logs(self, name):
        logger.info(f'\n{PrintColors.PURPLE}======================== {name} Starting ========================{PrintColors.ENDC}')
    
    def finish_logs(self, name):
        logger.info(f'\n{PrintColors.PURPLE}======================== {name} Finished ========================{PrintColors.ENDC}')
