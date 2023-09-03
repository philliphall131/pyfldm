# PyFLDM

## Python Fast Light Digital Modem
A library to be used for interacting with and controlling the Fldigi application. Uses the Fldigi xmlrpc API to give the user programmatic control of Fldigi via python. 

### Contents
- Installation
- Features
- Issues and Contributions
- Logging
- Using pyfldm
- List of all methods

## Installation
```
pip install pyfldm
```
To use the headless feature (linux only)
```
sudo apt install xvfb
```
## Features
- AppMonitor for launching, stopping, and monitoring the running status of the Fldigi application
- Client for exercising all the Fldigi xmlrpc endpoints
- Headless mode for linux to run fldigi purely via script with no Fldigi gui
- See or change Fldigi configuration via AppMonitor.config_manager

## Issues and Contributions
I welcome bringing up any issues you encounter with PyFLDM. Either submit and issue on github (https://github.com/philliphall131/pyfldm/issues) or contact me directly
If you want to contribute, submit a pull request or feel free to contact me via github/email

## Logging
pyfldm uses the built in python logging for all output *(except when print in the method name, like print_methods()). This is to avoid spamming users with unnecessary output unless desired. The user is responsible for setting up logging in whatever fashion they want, here is the example I use for all my sandboxing:
```
import logging

pyfldm_logger = logging.getLogger('pyfldm')
pyfldm_logger.setLevel(logging.DEBUG)
console_handler1 = logging.StreamHandler()
console_handler1.setLevel(logging.DEBUG)
console_formatter1 = logging.Formatter('%(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
console_handler1.setFormatter(console_formatter1)
pyfldm_logger.addHandler(console_handler1)
```

## Using pyfldm
* Below demonstrates some of the main usage with a few examples, but does not cover every possible use case

### 1. Controlling the Application (start, stop, status)
```
>>> from pyfldm.appmonitor import AppMonitor
>>> app = AppMonitor()
>>> app.start()
>>> app.is_running() # checks that Fldigi is a currently running process
True
>>> app.is_functional() # verifies that the xmlrpc interface is responsive
True
>>> result = app.stop() # asks fldigi to gracefully shut down, returns True if successfully stopped, otherwise False
>>> if not result:
...     app.kill()  # forcibly kills the process
>>> # Or use app.stop(force_if_unsuccessful=True) to force close if graceful shutdown not possible
>>> app.is_running()
False

```

### 2. Using the XMLRPC API
- To setup the client for use:
```
# * assuming that Fldigi is already running
>>> from pyfldm.client import Client
>>> client = Client()
```

- For various ways to list available client methods, use the following example:
```
# to get all the methods as a list of dictionaries
>>> methods = client.get_all_methods()
>>> print(methods)
[{'fldigi': ['config_dir', 'list', 'name', 'name_and_version', ...

# to print all the methods to stdout in a readable format:
>>> client.print_all_methods()
---------------------
client.fldigi methods
---------------------
fldigi.config_dir
fldigi.list
fldigi.name
...
 
# to print only the methods of a sub-section of fldigi xmlrpc
>>> client.text.print_methods()
---------------------
client.text methods
---------------------
text.add_tx
text.add_tx_bytes
text.clear_rx
...

# to get the methods of a sub-section of fldigi xmlrpc as a list
>>> client.text.get_methods()
>>> print(methods)
['add_tx', 'add_tx_bytes', 'clear_rx', 'clear_tx', 'get_rx', 'get_rx_data', 'get_rx_length', 'get_rxtx_data', 'get_tx_data']

```

- To use the various xmlrpc endpoint functions:
  - The functions are grouped into sub-categories of related functionality. For example to access text manipulation in Fldigi, use client.text...., to use the high level, generic fldigi info, use client.fldigi..., see some examples below:

```
# * assuming that Fldigi is already running
>>> from pyfldm.client import Client
>>> client = Client()
>>> client.fldigi.version()
4.1.26
>>> client.text.add_tx("some text")
# the fldigi Tx widget should have "some text" populated and ready to send upon triggering transmit

# to trigger transmit
>>> client.main.tx()

# to stop transmitting and revert to receive mode
>>> client.main.rx()

```

### 3. Using pyfldm with fldigi headless

**** Only on linux, must have xvfb installed ****
```
from pyfldm.appmonitor import AppMonitor
app = AppMonitor(headless=True)
```

### 4. Using pyfldm to view and change Fldigi configurations

**** Warning: this does not type check config values, be sure you know the correct value to use if setting values ****

This functionality interacts with the config file that saves all of Fldigi's settings
- To get and set config items:
```
>>> from pyfldm.appmonitor import AppMonitor
>>> app = AppMonitor()

# to search for a particular config item using a part or whole of the config name:
>>> app.config_manager.search_config('tx')
['SHOW_TX_TIMER', 'TX_TIMEOUT', 'RSIDTXMODESEXCLUDE',  ...

# to get the value of a stored config item
>>> app.config_manager.get_config('TX_TIMEOUT')
5

# to set the value of a stored config item (returns True if successful)
>>> app.config_manager.set_config('CONFIRMEXIT', 1)
True
```

- To determine which config item is associated with a specific action in Fldigi, the following functionality will allow you to monitor changes to config as you make the change in the Fldigi GUI and report back the exact config item thats been changed. To use this, you must enable monitoring config updates in the AppMonitor and the python script must be running while making changes in the Fldigi GUI.

Example:
```
>>> from pyfldm.appmonitor import AppMonitor
# Use either this:
>>> app = AppMonitor(monitor_config_updates=True)

# or this:
>>> app = AppMonitor()
>>> app.config_manager.start_listening()

# if running from a script, ensure the script runs long enough for you to make config changes, ie time.sleep()
>>> import time
>>> time.sleep(120)

# Open Fldigi via the GUI and make a change to any config item from Configure > Config Dialog

The TOOLTIPS value has changed from 1 to 0
The CONFIRMEXIT value has changed from 1 to 0

# Now you have the exact names to use for getting/setting config items via app.config_manager.set_config/get_config

```

## Methods List
---------------------
client.fldigi
---------------------
- fldigi.config_dir
- fldigi.list
- fldigi.name
- fldigi.name_and_version
- fldigi.terminate
- fldigi.version
- fldigi.version_struct

---------------------
client.ioconfig
---------------------
- ioconfig.enable_arq
- ioconfig.enable_kiss
- ioconfig.in_use

---------------------
client.main
---------------------
- main.abort
- main.get_afc
- main.get_char_rates
- main.get_char_timing
- main.get_frequency
- main.get_lock
- main.get_max_macro_id
- main.get_reverse
- main.get_rsid
- main.get_squelch
- main.get_squelch_level
- main.get_status1
- main.get_status2
- main.get_trx_state
- main.get_trx_status
- main.get_tx_timing
- main.get_txid
- main.get_wf_sideband
- main.inc_frequency
- main.inc_squelch_level
- main.run_macro
- main.rx
- main.rx_only
- main.rx_tx
- main.set_afc
- main.set_frequency
- main.set_lock
- main.set_reverse
- main.set_rsid
- main.set_squelch
- main.set_squelch_level
- main.set_txid
- main.set_wf_sideband
- main.toggle_afc
- main.toggle_lock
- main.toggle_reverse
- main.toggle_rsid
- main.toggle_squelch
- main.toggle_txid
- main.tune
- main.tx

---------------------
client.modem
---------------------
- modem.get_afc_search_range
- modem.get_bandwidth
- modem.get_carrier
- modem.get_id
- modem.get_max_id
- modem.get_name
- modem.get_names
- modem.get_olivia_bandwidth
- modem.get_olivia_tones
- modem.get_quality
- modem.increment_afc_search_range
- modem.increment_bandwidth
- modem.increment_carrier
- modem.search_down
- modem.search_up
- modem.set_afc_search_range
- modem.set_bandwidth
- modem.set_by_id
- modem.set_by_name
- modem.set_carrier
- modem.set_olivia_bandwidth
- modem.set_olivia_tones

---------------------
client.navtex
---------------------
- navtex.get_message
- navtex.send_message

---------------------
client.rig
---------------------
- rig.get_bandwidth
- rig.get_bandwidths
- rig.get_mode
- rig.get_modes
- rig.get_name
- rig.get_notch
- rig.release_control
- rig.set_bandwidth
- rig.set_bandwidths
- rig.set_frequency
- rig.set_mode
- rig.set_modes
- rig.set_name
- rig.set_pwrmeter
- rig.set_smeter
- rig.take_control

---------------------
client.spot
---------------------
- spot.get_auto
- spot.get_pskrep_count
- spot.set_auto
- spot.toggle_auto

---------------------
client.text
---------------------
- text.add_tx
- text.add_tx_bytes
- text.clear_rx
- text.clear_tx
- text.get_rx
- text.get_rx_data
- text.get_rx_length
- text.get_rxtx_data
- text.get_tx_data

---------------------
client.wefax
---------------------
- wefax.end_reception
- wefax.get_received_file
- wefax.send_file
- wefax.set_adif_log
- wefax.set_max_lines
- wefax.set_tx_abort_flag
- wefax.skip_apt
- wefax.skip_phasing
- wefax.state_string