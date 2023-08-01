################################################################
# 
# File: Logger.py
# Copyright(c) 2023, Hallway Trails LLC. All rights reserved.
#
################################################################

import logging

logger = logging.getLogger("PyFldm")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

logger.addHandler(console_handler)
