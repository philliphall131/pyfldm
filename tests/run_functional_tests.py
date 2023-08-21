from functional_tests.testing_runner import TestingRunner
from functional_tests import TestAppMonitor, TestClient, TestClientText,\
    TestClientFldigi, TestClientIo, TestClientMain, TestClientModem,\
    TestClientNavtex, TestClientRig, TestClientSpot

test_app_monitor = TestAppMonitor()
test_client = TestClient()
test_client_fldigi = TestClientFldigi()
test_client_io = TestClientIo()
test_client_main = TestClientMain()
test_client_modem = TestClientModem()
test_client_navtex = TestClientNavtex()
test_client_rig = TestClientRig()
test_client_spot = TestClientSpot()
test_client_text = TestClientText()

tests_to_run = [
    test_app_monitor,
    test_client,
    test_client_fldigi,
    test_client_io,
    test_client_main,
    test_client_modem,
    test_client_navtex,
    test_client_rig,
    test_client_spot,
    test_client_text
]

tester = TestingRunner(0)
# tester.run(tests_to_run)

tester.run(test_client_text)

#TODO: add config setting to set computer speakers to audio output


