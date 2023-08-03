from AppMonitor import AppMonitor
from Logger import logger
from time import sleep
from client.Client import Client
from client.Fldigi import Fldigi

a = AppMonitor()
a.start()
client = Client()

# sleep(2)
print(type(client.io.enable_arq()))



# keep_running = True
# while keep_running:
#     print("\n\n\nPyFldigi Automated Base Station")
#     print("\tStation is running. Select an option below:")
#     print("\t(P/p) -- Print last 10 logs")
#     print("\t(X/x) -- Close and exit")
#     choice = input("Please select an option: ")
#     if choice.upper() == 'X':
#         keep_running = False
#     elif choice.upper() == 'P':
#         print('\nHere are all the logs!\n')
#     else:
#         print('\nInvalid selection\n')
