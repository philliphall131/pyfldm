############################################################################
# 
#  File: run_functional_tests.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#  USA
#
############################################################################

from functional_tests.testing_runner import TestingRunner
from functional_tests import TestAppMonitor, TestClient, TestClientText,\
    TestClientFldigi, TestClientIo, TestClientMain, TestClientModem,\
    TestClientNavtex, TestClientRig, TestClientSpot, TestClientWefax

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
test_client_wefax = TestClientWefax()

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
    test_client_text,
    test_client_wefax
]

tester = TestingRunner(2)
tester.run(tests_to_run)


