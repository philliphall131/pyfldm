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