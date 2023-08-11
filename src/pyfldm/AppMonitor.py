############################################################################
# 
#  File: AppMonitor.py
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

import sys
import subprocess
import logging
from time import time, sleep
from .Client import Client

logger = logging.getLogger(__name__)

MAX_STARTUP_DELAY_SECS = 5
MAX_SHUTDOWN_DELAY_SECS = 5

class AppMonitor:

    ''' ApplicationMonitor manages the running of Fldigi. 
    Launches, monitors, and terminates the Fldigi process, using python subprocess.Popen

    @param hostname(str): the IP address of the xmlrpc server for Fldigi to establish
    @param port(int): the port number of the xmlrpc server connection

    >>> from pyfldm.AppMonitor import AppMonitor
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
    '''

    def __init__(self, hostname='127.0.0.1', port=7362) -> None:
        self.platform = sys.platform
        self.process = None
        self.hostname = hostname
        self.port = int(port)
        self._client = Client(hostname, port)

        # log platform
        if self.platform == 'darwin':
            logger.debug("Detected MacOS")
        elif self.platform == 'win32':
            logger.debug("Detected Windows")
        else:
            logger.debug("Detected Linux/Other OS")

    def _get_process_id(self) -> int:
        if self.platform == 'win32':
            # check on windows
            pass
        else:
            process1 = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
            try: 
                process2 = subprocess.check_output(['pgrep', '-f', 'fldigi'], stdin=process1.stdout)
            except subprocess.CalledProcessError:
                return 0
            else:
                return int(process2.decode().strip())

    def is_running(self) -> bool:
        return True if self._get_process_id() else False
    
    def is_functional(self) -> bool:
        try:
            if self._client.fldigi.name() == 'fldigi':
                return True
            else:
                logger.warning("Connection made but Fldigi name() not responding with 'fldigi'")
                return False
        except ConnectionRefusedError:
            return False
        
    def _wait_for_startup(self, timeout_secs = MAX_STARTUP_DELAY_SECS, sleep_secs = .5) -> bool:
        start = time()
        while (start + timeout_secs) > time():
            if self.is_functional():
                return True
            sleep(sleep_secs)
        return False
    
    def _wait_for_shutdown(self, timeout_secs = MAX_SHUTDOWN_DELAY_SECS, sleep_secs = .5) -> bool:
        start = time()
        while (start + timeout_secs) > time():
            if not self.is_functional():
                return True
            sleep(sleep_secs)
        return False

    def start(self) -> int:
        # check if application already running
        if self.is_running():
            logger.warning("Fldigi is already running. Shut down all instances of Fldigi before using AppMonitor.start()")
            return 0
        logger.info("Starting Fldigi")

        addl_args = ['--xmlrpc-server-address', 
                     self.hostname, 
                     '--xmlrpc-server-port', 
                     str(self.port)]

        if self.platform == 'darwin':
            # start with MacOS
            # find the application name
            process1 = subprocess.Popen(['ls', '/Applications'], stdout=subprocess.PIPE)
            process2 = subprocess.check_output(['grep', 'fldigi'], stdin=process1.stdout)
            app_name = process2.decode().strip()
            # start the application
            startup_args = ['open', '-a', f'{app_name}', '--args'] + addl_args
            self.process = subprocess.Popen(startup_args)
            sleep(2)

        
        elif self.platform == 'win32':
            # start with windows
            pass

        else:
            # start with linux
            self.process = subprocess.Popen(['fldigi'] + addl_args)

        if self._wait_for_startup():
            logger.debug("Fldigi fully functional")
            return 0
        logger.critical("Fldigi process started but reached max timeout with no connection to xmlrpc. Unconfirmed if Fldigi is functionally running")
        return 1 
    
    def stop(self, save_options=True, save_log=True, save_macros=True,) -> int:
        # first verify its actually running
        if not self.is_running():
            logger.info("No Fldigi instances running, nothing to shut down")
            return 0
        logger.debug("Starting graceful shutdown of Fldigi")
        bitmask = int('0b{}{}{}'.format(int(save_macros), int(save_log), int(save_options)), 0)
        self._client.fldigi.terminate(bitmask)

        # wait and verify that Fldigi has shut down
        if self._wait_for_shutdown():
            logger.info("Fldigi successfully shut down")
            return 0
        logger.critical("Fldigi graceful shutdown unsuccessful")
        return 1
    
    def kill(self) -> int:
        # first verify its actually running
        process_id = self._get_process_id()
        if not self.is_running():
            logger.info("No Fldigi instances running, nothing to shut down")
            return 0
        
        logger.debug("Starting forced shutdown of Fldigi")
        # start with a more graceful system SIGTERM
        if self.platform == 'win32':
            # kill with windows
            pass
        else:
            # kill with macos/linux/other
            subprocess.Popen(['kill', str(process_id)])

        if self._wait_for_shutdown():
            logger.info("Fldigi successfully force killed via SIGTERM")
            return 0
        logger.warn("Fldigi SIGTERM unsuccessful")

        # now try the less graceful SIGKILL
        if self.platform == 'win32':
            # kill with windows
            pass
        else:
            # kill with macos/linux/other
            subprocess.Popen(['kill', '-9', str(process_id)])

        if self._wait_for_shutdown():
            logger.info("Fldigi successfully force killed via SIGKILL")
            return 0
        logger.critical("Fldigi SIGKILL unsuccessful, cannot shut down Fldigi")
        return 1
