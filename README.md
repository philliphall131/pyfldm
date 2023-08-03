# PyFLDM
## Python Fast Light Digital Modem
A library to be used for interacting with and controlling the Fldigi application. 

Can be used to control the application directly via python library, such as to start, stop, and monitor the runnin status. But the primary usage is in serving as an api to Fldigi via xmlrpc

Example uses:
1. Controlling the Application (start, stop, status)
```
>>> import pyfldm
>>> app = pyfldm.AppMonitor()
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
>>> import pyfldm
>>> client = pyfldm.Client()
>>> client.fldigi.version()
4.1.26

```