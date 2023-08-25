############################################################################
# 
#  File: utilities.py
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

from enum import Enum

class PrintColors(Enum):
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    PINK = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PrintColorsRegex(Enum):
    PURPLE = '\\033\[95m'
    BLUE = '\\033\[94m'
    PINK = '\\033\[96m'
    GREEN = '\\033\[92m'
    YELLOW = '\\033\[93m'
    RED = '\\033\[91m'
    ENDC = '\\033\[0m'
    BOLD = '\\033\[1m'
    UNDERLINE = '\\033\[4m'

class LogOption(Enum):
    CONSOLE_ONLY = 0
    FILE_ONLY = 1
    BOTH = 2

class TestSetupException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class TestCleanupException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)