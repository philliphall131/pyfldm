class TestCase:
    def __init__(self) -> None:
        pass

    def setup(self) -> None:
        print("running setup")

    def cleanup(self) -> None:
        print("running cleanup")

    def each_setup(self) -> None:
        print("running individual setup")

    def each_cleanup(self) -> None:
        print("running individual setup")

    def run_all_tests(self) -> None:
        # gather up all the tests and run them
        test_methods = [func for func in dir(self) if 
                        func.startswith("test_")]
        
        self.setup()
        
        for test in test_methods:
            test_func = getattr(self, test)
            self.each_setup()
            test_func()
            self.each_cleanup()

        self.cleanup()

    def run_test(self) -> None:
        # gather up all the tests and run them
        test_methods = [func for func in dir(self) if 
                        func.startswith("test_")]
        # print(test_methods)
        for test in test_methods:
            test_func = getattr(self, test)
            test_func()