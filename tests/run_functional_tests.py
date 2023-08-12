import logging
from time import sleep
from pyfldm.AppMonitor import AppMonitor
from pyfldm.Client import Client

logger = logging.getLogger("pyfldm")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

logger.addHandler(console_handler)

app = AppMonitor()
app.start()
client = Client()

print(client.fldigi.name())
client.text.add_tx("Hello World")
sleep(15)

app.stop()

