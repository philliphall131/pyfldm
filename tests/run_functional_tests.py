from functional_tests.TestRunner import TestRunner
from functional_tests.TestText import TestText

text_case = TestText()

tester = TestRunner(2)
tester.run([text_case])


