from functional_tests.testing_runner import TestingRunner
from functional_tests import TestAppMonitor, TestClient, TestText,\
    TestClientFldigi

test_app_monitor = TestAppMonitor()
test_client = TestClient()
test_client_fldigi = TestClientFldigi()
test_text = TestText()


tests_to_run = [
    test_app_monitor,
    test_client,
    test_client_fldigi,
    test_text
]

tester = TestingRunner(0)
# tester.run(tests_to_run)

tester.run(test_client_fldigi)


