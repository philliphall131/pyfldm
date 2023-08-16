from functional_tests.testing_runner import TestingRunner
from functional_tests.test_appmonitor import TestAppMonitor
from functional_tests.test_text import TestText

case_app_monitor = TestAppMonitor()
text_case = TestText()

tests_to_run = [
    case_app_monitor
]

tester = TestingRunner(2)
tester.run(tests_to_run)


