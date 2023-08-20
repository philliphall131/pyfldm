from functional_tests.testing_runner import TestingRunner
from functional_tests import TestAppMonitor, TestClient, TestText,\
    TestClientFldigi, TestClientIo, TestClientMain

test_app_monitor = TestAppMonitor()
test_client = TestClient()
test_client_fldigi = TestClientFldigi()
test_text = TestText()
test_client_io = TestClientIo()
test_client_main = TestClientMain()

tests_to_run = [
    test_app_monitor,
    test_client,
    test_client_fldigi,
    test_client_io,
    test_client_main,
    test_text
]

tester = TestingRunner(0)
# tester.run(tests_to_run)

tester.run(test_client_main)

#TODO: add config setting to set computer speakers to audio output


