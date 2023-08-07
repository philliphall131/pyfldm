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

# a = AppMonitor()
# a.start()
client = Client()
print()
for entry in client.get_all_methods():
    print(entry)

# print(client.fldigi.test_call())

# try:
#     from pyfldm import Client
# except:
#     print('Cannot import pyfldm. Ensure it is installed')
#     sys.exit(1)


