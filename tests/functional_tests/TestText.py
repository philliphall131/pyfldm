############################################################################
# 
#  File: TestTextEp.py
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

from .TestCase import TestCase
from pyfldm.AppMonitor import AppMonitor
from pyfldm.Client import Client

class TestText(TestCase):
    def __init__(self) -> None:
        self.app = AppMonitor()
        self.client = Client()

    def setup(self) -> None:
        print("running text setup")

    def cleanup(self) -> None:
        print("running text cleanup")

    def each_setup(self) -> None:
        print("running text individual setup")

    def each_cleanup(self) -> None:
        print("running text individual setup")

    def test_add_tx(self) -> None:
        print('test add text')

    def test_add_rx(self) -> None:
        print('test add rx')
