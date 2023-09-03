############################################################################
# 
#  File: flconfig_manager.py
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

import logging
import os
import shutil
from pathlib import Path
from xml.etree import ElementTree
import threading
from time import sleep
from typing import Any

CONFIG_FILE = 'fldigi_def.xml'
CONFIG_FILE_COPY = 'fldigi_def-orig.xml'
MONITOR_INTERVAL_SECS = 2
    
class FlConfigManager(threading.Thread):
    '''Used to view and update Fldigi configuratin settings. Can be used to monitor updates to the Fldigi config file as a daemon thread that will die upon the script/caller ending

    This class is not intended to be created or used directly, but rather utilized under the pyfldm client object. Reference appmonitor.py which has an attribute self.config_manager that interfaces these methods.

    @param config_location(str): the path to the fldigi config directory (leave blank if default installed, only needed if a unique config directory has been set up)
    @param monitor_updates(bool): set to True to automatically begin the daemon thread to listen for config updates
    
    Example use:
    >>> from pyfldm.appmonitor import AppMonitor
    >>> app = AppMonitor()
    >>> app.config_manager.get_config('TX_TIMEOUT')
    5
    '''
    def __init__(self, config_location:str = None, monitor_updates:bool = False) -> None:
        super().__init__(daemon=True)
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._config_dir = self._get_config_dir(config_location)
        self._config_file = f'{self._config_dir}/{CONFIG_FILE}'
        self._config_tree = None
        self._config_monitor = None
        self._timestamp = None
        self._interval = MONITOR_INTERVAL_SECS
        self._update_tree()
        if monitor_updates:
            self.start()
    
    def __str__(self) -> str:
        return __name__.lower().split(".")[-1]
    
    def _get_config_dir(self, dir_path:str = None) -> str:
        '''Finds the fldigi config directory. If specified, ensures it exists and is valid. If not valid or not supplied, uses the default fldigi config directory location

        @param dir_path(str): the path to the fldigi config directory
        @return (str): the validated path to the config directory
        '''
        # check that config directory exists
        make_default_path = False
        if dir_path:
            # check that fldigi_def.xml exists
            if not os.path.exists(f'{dir_path}/{CONFIG_FILE}'):
                make_default_path = True
                self.logger.warning(f"Did not find {CONFIG_FILE} in the specified directory: ({dir_path}). Attempting to find configs in the default Fldigi location")

        # set the config directory as specified or default to user home directory
        config_dir = dir_path
        if make_default_path or not dir_path:
            config_dir = f'{Path.home()}/.fldigi'
            # check that fldigi_def.xml exists
            if not os.path.exists(f'{config_dir}/{CONFIG_FILE}'):
                self.logger.exception(f"Did not find {CONFIG_FILE} in the default Fldigi config directory: ({dir_path}). Ensure Fldigi is correctly installed and references a configuration directory. If the configuation directory is in a custom location, make sure to specify this when setting up FlConfig()")
        return f'{config_dir}'
    
    def _parse_config_file(self) -> ElementTree:
        '''Reads in the config file from xml format into a python xml tree object. Notes timestamp of the file as well

        @return (ElementTree): the xml tree object of all the fldigi config items
        '''
        if not os.path.exists(f'{self._config_dir}/{CONFIG_FILE_COPY}'):
            shutil.copy(self._config_file, f'{self._config_dir}/{CONFIG_FILE_COPY}')

        file_buffer = None
        with open(self._config_file, 'rb') as f:
            file_buffer = f.read()

        updated_file_buffer = file_buffer.replace(b'\x07', b'<bell hex sequence>')
        with open(self._config_file, 'wb') as f:
            f.write(updated_file_buffer)

        parser = ElementTree.XMLParser(target=ElementTree.TreeBuilder(insert_comments=True))
        tree = ElementTree.parse(self._config_file, parser)
        root = tree.getroot()
        if not root.tag == 'FLDIGI_DEFS':
            raise Exception('Expected root tag to be \'FLDIGI_DEFS\' but got {!r}'.format(self.root.tag))
        self._timestamp = os.path.getmtime(self._config_file)
        return tree
    
    def get_config(self, tag: str) -> str:
        '''Gets the value specified by the input tag or key

        @param tag(str): The exact name (case-sensitive) of the config item
        @return (str): the value of the config item
        '''
        root = self._config_tree.getroot()
        node = root.find(tag)
        if node is not None:
            return node.text
        return None
    
    def search_config(self, tag_part: str) -> list:
        '''Searches all the config items for a tag/key that has even a partial match to the input tag_part

        @param tag_part(str): the entire tag, or a portion of the tag to search for
        @return (list): a list of the tag names (as str) that match or partial match the tag_part
        '''
        root = self._config_tree.getroot()
        results = []
        tag_part_up = tag_part.upper()
        for child in root:
            if (type(child.tag) == str) and (tag_part_up in child.tag.upper()):
                results.append(child.tag)
        return results if results else None
    
    def set_config(self, tag: str, new_value: Any) -> bool:
        '''Sets a config item and updates the config file. Careful, there is no type checking and some values may not work in Fldigi. The user should understand what are valid values to update config items (reference the config file for type descriptions)

        @param tag(str): the config item to update (case sensitive)
        @param new_value(Any): the value to update the config item to
        @return (bool): True if the value successfully set
        '''
        root = self._config_tree.getroot()
        # first verify that the tag exists and is a single tag
        nodes = root.findall(tag)
        if not nodes:
            self.logger.warn(f"No nodes found with the given tag: {tag}")
            return False
        if len(nodes) > 1:
            self.logger.warn(f"Multiple tags found for the given tag: {tag}")
            return False
        # we know we have a matching single tag
        node = root.find(tag)
        node.text = str(new_value)
        self._config_tree.write(self._config_file)
        return True
    
    def _update_tree(self) -> None:
        '''Private method to update the config object'''
        new_tree = self._parse_config_file()
        self._config_tree = new_tree

    def read_changes(self) -> None:
        '''Re-reads the config file and compares against the currently stored config items to determine what differences there might be and logs/prints out the difference with the config item name'''
        new_tree = self._parse_config_file()
        new_root = new_tree.getroot()
        root = self._config_tree.getroot()
        for child in root:
            if type(child.tag) == str:
                original_val = child.text
                new_node = new_root.find(child.tag)
                new_val = new_node.text
                if original_val != new_val:
                    self.logger.info(f"The {child.tag} value has changed from {original_val} to {new_val}")
                    print(f"The {child.tag} value has changed from {original_val} to {new_val}")
    
    def start_listening(self) -> None:
        '''Starts the thread to listen for config file changes'''
        if not self._running:
            self.start()

    def run(self) -> None:
        '''Overrides the Thread object run. Listens for updates to the config file for as long as the parent python script/caller is alive'''
        self._running = True
        while True:
            # check if the timestamp changed
            new_timestamp = os.path.getmtime(self._config_file)
            if new_timestamp != self._timestamp:
                self.read_changes()
                self._update_tree()
            sleep(self._interval)

    #### Gets and Sets for Popular Config items ####
    def get_confirm_exit(self):
        return self.get_config('CONFIRMEXIT')
    
    def get_log_file_name(self):
        return self.get_config('LOGBOOKFILENAME')
    
    def get_port_in_device(self):
        return self.get_config('PORTINDEVICE')
    
    def get_port_out_device(self):
        return self.get_config('PORTOUTDEVICE')
    
    def get_full_duplex(self):
        return self.get_config('IS_FULL_DUPLEX')
    
    def get_audio_io(self):
        ''' Audio subsystem.  Values are as follows:
        0: OSS; 1: PortAudio; 2: PulseAudio; 3: File I/O'''
        return self.get_config('AUDIOIO')
    
    def set_confirm_exit(self, new_val):
        return self.set_config('CONFIRMEXIT', new_val)
    
    def set_log_file_name(self, new_val):
        return self.set_config('LOGBOOKFILENAME', new_val)
    
    def set_port_in_device(self, new_val):
        return self.set_config('PORTINDEVICE', new_val)
    
    def set_port_out_device(self, new_val):
        return self.set_config('PORTOUTDEVICE', new_val)
    
    def set_full_duplex(self, new_val):
        return self.set_config('IS_FULL_DUPLEX', new_val)
    
    def set_audio_io(self, new_val):
        ''' Audio subsystem.  Values are as follows:
        0: OSS; 1: PortAudio; 2: PulseAudio; 3: File I/O'''
        return self.set_config('AUDIOIO', new_val)
