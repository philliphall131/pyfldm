# PyFLDM

*** v0.0.4 Release Notes: AppMonitor now compatible with Windows OS! ***

*** CAUTION: All versions v0.x.y are very rough and untested. Version 1.0.0 still in development, tentative release date Sep2023. All current functionality being actively developed and tested. ***

## Python Fast Light Digital Modem
A library to be used for interacting with and controlling the Fldigi application. 

Can be used to control the application directly via python library, such as to start, stop, and monitor the running status. But the primary usage is in serving as an api to Fldigi via xmlrpc

## Installation
```
pip install pyfldm
```
To use the headless feature (linux only)
```
sudo apt install xvfb
```


## Using pyfldm

1. Controlling the Application (start, stop, status)
```
>>> from pyfldm.appMonitor import AppMonitor
>>> app = AppMonitor()
>>> app.start()
>>> # wait a few seconds for Fldigi to start up
>>> app.is_running() # checks that Fldigi is a currently running process
True
>>> app.is_functional() # verifies that the xmlrpc interface is responsive
True
>>> result = app.stop() # asks fldigi to gracefully shut down, returns a 0 if successfully stopped, 1 if not
>>> if not result:
...     app.kill()  # forcibly kills the process
>>> app.is_running()
False

```

2. Using the XMLRPC API
```
# * assuming that Fldigi is already running
>>> from pyfldm.client import Client
>>> client = Client()
>>> client.fldigi.version()
4.1.26

```


3. Using pyfldm with fldigi headless

**** Only on linux, must have xvfb installed ****
```
from pyfldm.appmonitor import AppMonitor
app = AppMonitor(headless=True)
```