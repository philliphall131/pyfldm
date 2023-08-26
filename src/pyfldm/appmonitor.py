############################################################################
# 
#  File: appmonitor.py
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

import os, sys
import psutil
import subprocess
import logging
from time import time, sleep
from xvfbwrapper import Xvfb
from .client import Client

logger = logging.getLogger(__name__)

MAX_STARTUP_DELAY_SECS = 10
MAX_SHUTDOWN_DELAY_SECS = 10

class AppMonitor:

    ''' ApplicationMonitor manages the running of Fldigi. 
    Launches, monitors, and terminates the Fldigi process, using python subprocess.Popen

    @param hostname(str): the IP address of the xmlrpc server for Fldigi to establish
    @param port(int): the port number of the xmlrpc server connection
    @param exe_path(str): [OPTIONAL, ONLY USE IF NEEDED] the path to the executable fldigi app, to be used when Fldigi installed in an other than default location. 
    Example for windows: exe_path = "C:\\\\\\Users\\\\\\Me\\\\\\Desktop\\\\\\fldigi-folder\\\\\\fldigi.exe ***must use double slash for python to understand the windows path as a string***, 
    Example for linux: exe_path = "/home/myself/Desktop/fldigi-folder/fldigi-4.1.26

    Example use:
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
    '''

    def __init__(self, 
                 hostname:str='127.0.0.1', 
                 port:int=7362, 
                 exe_path:str=None, 
                 headless:bool=False,
                 multi:bool=False) -> None:
        self.platform = sys.platform
        self.process_id = None
        self.hostname = hostname
        self.port = int(port)
        self._client = Client(hostname, port)
        self.exe_path = exe_path
        self.headless = headless
        self.multi = multi
        self.vdisplay = None

        # log warning on using multi feature
        if self.multi:
            logger.warning("Use caution with the multi feature. If you do not maintain a consistent object to\
                            start and stop the application, you may experience erratic results when starting\
                            and stopping multiple instances of fldigi.")

        # log platform
        if self.platform == 'darwin':
            logger.debug("Detected MacOS")
        elif self.platform == 'win32':
            logger.debug("Detected Windows")
        else:
            logger.debug("Detected Linux/Other OS")

    def _get_process_id(self) -> int:
        if self.process_id:
            # check that the process id is still valid and return it, otherwise
            # set it to none and continue
            try:
                process = psutil.Process(self.process_id)
                if process.status() not in ['dead', 'zombie']:
                    return self.process_id
            except psutil.NoSuchProcess:
                pass
            # if we got here, the process is either non-existant (NoSuchProcess), dead,
            # or zombied so just continue on to see if theres any other fldigi processes
            self.process_id = None

        # filter processes to find fldigi, if it exists
        fldigi_processes = [proc for proc in psutil.process_iter(['pid', 'name']) if 'fldigi' in proc.name()]
        if not fldigi_processes:
            # no fldigi processes found
            return 0
        # filter out any zombie processes (occurs on linux)
        valid_processes = []
        for proc in fldigi_processes:
            if proc.status() != 'zombie':
                valid_processes.append(proc)
        if not valid_processes:
            # no fldigi processes found
            return 0
        elif len(valid_processes) > 1:
            logger.warning("Multiple valid Fldigi instances running, choosing most recently started instance.")
            valid_processes.sort(key=lambda x: x.create_time(), reverse=True)
        return valid_processes[0].pid


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
            if not self.is_running():
                return True
            sleep(sleep_secs)
        return False

    def start(self) -> int:
        # check if application already running
        if (not self.multi) and (self.is_running()):
            logger.warning("Fldigi is already running. Shut down all instances of Fldigi before using AppMonitor.start()")
            return 0
        logger.info("Starting Fldigi")

        addl_args = ['--xmlrpc-server-address', 
                     self.hostname, 
                     '--xmlrpc-server-port', 
                     str(self.port)]
        startup_args = ['fldigi']

        if self.platform == 'darwin':
            # start with MacOS
            # find the application name with bash commands
            process1 = subprocess.Popen(['ls', '/Applications'], stdout=subprocess.PIPE)
            process2 = subprocess.check_output(['grep', 'fldigi'], stdin=process1.stdout)
            app_name = process2.decode().strip()
            # start the application
            startup_args = ['open', '-a', f'{app_name}', '--args']

        elif self.platform == 'win32':
            # start with windows
            # use the path given
            if self.exe_path:
                exe_file_name = os.path.basename(self.exe_path)
                if ((not os.path.isfile(self.exe_path)) 
                    or (not self.exe_path.endswith('.exe')) 
                    or ('fldigi' not in exe_file_name.lower())):
                    raise FileNotFoundError('The given fldigi .exe file not found')
                startup_args = [self.exe_path]

            # otherwise need to look for the path
            else:
                startup_args = [self._find_fldigi_exe()]

        else:
            # start with linux
            if self.headless:
                self.vdisplay = Xvfb()
                self.vdisplay.start()
        
        # start the process with the gathered command line arguments
        process = subprocess.Popen(startup_args + addl_args)
        self.process_id = process.pid

        if self._wait_for_startup():
            logger.debug("Fldigi fully functional")
            return 0
        logger.critical("Fldigi process started but reached max timeout with no connection to xmlrpc. Unconfirmed if Fldigi is functionally running")
        return 1 
    
    def stop(self, save_options=False, save_log=False, save_macros=False, force_if_unsuccessful=False) -> bool:
        # first verify its actually running
        if not self.is_running():
            logger.info("No Fldigi instances running, nothing to shut down")
            return True
        logger.debug("Starting graceful shutdown of Fldigi")
        self._client.fldigi.terminate(save_options, save_log, save_macros)
        if self.headless:
            self.vdisplay.stop()

        # wait and verify that Fldigi has shut down
        if self._wait_for_shutdown():
            logger.info("Fldigi successfully shut down")
            return True
        logger.critical("Fldigi graceful shutdown unsuccessful")
        if force_if_unsuccessful:
            return self.kill()
        return False
    
    def kill(self) -> bool:
        # first verify its actually running
        if not self.is_running():
            logger.info("No Fldigi instances running, nothing to shut down")
            return True
        process_id = self._get_process_id()
        process = psutil.Process(process_id)
        logger.debug("Starting forced shutdown of Fldigi")

        # start with a more graceful system SIGTERM
        process.terminate()

        if self._wait_for_shutdown():
            logger.info("Fldigi successfully force killed via SIGTERM")
            return True
        logger.warn("Fldigi SIGTERM unsuccessful")

        # now try the less graceful SIGKILL
        process.kill()

        if self._wait_for_shutdown():
            logger.info("Fldigi successfully force killed via SIGKILL")
            return True
        logger.critical("Fldigi SIGKILL unsuccessful, cannot shut down Fldigi")
        return False

    def _find_fldigi_exe(self):
        # first look in Program Files (x86)
        prog_files = os.environ["ProgramFiles(x86)"]
        fldigi_dir = [dir for dir in os.listdir(prog_files) if 'fldigi' in dir.lower()]
        if not fldigi_dir:
            # Not there, look in Program Files
            prog_files = os.environ["ProgramFiles"]
            fldigi_dir = [dir for dir in os.listdir(prog_files) if 'fldigi' in dir.lower()]
        # No Fldigi folders found in any Program Files directories
        if not fldigi_dir:
            logger.critical("Cannot find FLDigi in either Program Files or Program Files (x86). Check that FLDigi is installed or pass in the path to the fldigi .exe")
            raise ModuleNotFoundError("Cannot find FLDigi. Ensure it's installed or pass in path to .exe")

        if len(fldigi_dir) > 1:
            logger.warning("Found multiple versions or installs of Fldigi. Defaulting to the latest version, as best as can be determined. If another version or install is preferred, pass in the .exe path to AppMonitor")
            # get the latest version number, sort so the latest is first
            fldigi_dir.sort(reverse=True)
            # ensure there is an exe in the folder we want, if not iterate through th fldigi folders to find one
            for dir in fldigi_dir:
                current_dir = os.path.join(prog_files, dir)
                files_in_dir = os.listdir(current_dir)
                for file in files_in_dir:
                    if  (('fldigi' in file) and ('.exe' in file)):
                        logger.info(f"The latest usable version found is {current_dir}, attempting to start with this installation")
                        return os.path.join(current_dir, file)
                logger.warn(f"No fldigi exe found in {current_dir}. This may be a corrupted installation. Attempting the next installed version, if any")
            
            return
        path_to_exe = os.path.join(prog_files, fldigi_dir[0])
        fldigi_exe = [f for f in os.listdir(path_to_exe) if (('fldigi' in f) and ('.exe' in f))]
        if fldigi_exe:
            return os.path.join(path_to_exe, fldigi_exe[0])
        else:
            logger.critical(f"No fldigi exe found in {path_to_exe}. Check your installation of Fldigi, it may be incomplete or corrupted.")
            raise ModuleNotFoundError('No fldigi exe found')
