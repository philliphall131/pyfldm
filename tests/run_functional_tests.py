import logging
from pyfldm.AppMonitor import AppMonitor
from pyfldm.Client import Client

# logger = logging.getLogger("pyfldm")
# logger.setLevel(logging.DEBUG)

# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)

# console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# console_handler.setFormatter(console_formatter)

# logger.addHandler(console_handler)

from functional_tests.TestText import TestText

test_case1 = TestText()
test_case1.run_all_tests()


