############################################################################
# 
#  File: flconfig.py
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
import xml.etree.ElementTree as et
import threading
from time import sleep

CONFIG_FILE = 'fldigi_def.xml'
CONFIG_FILE_COPY = 'fldigi_def-orig.xml'
MONITOR_INTERVAL_SECS = 2
    
class FlConfig(threading.Thread):
    ''' TBD
    '''
    def __init__(self, config_location = None, monitor_updates = False) -> None:
        super().__init__(daemon=True)
        self.logger = logging.getLogger(__name__)
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
    
    def _get_config_dir(self, dir_path):
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
    
    def _parse_config_file(self):
        if not os.path.exists(f'{self._config_dir}/{CONFIG_FILE_COPY}'):
            shutil.copy(self._config_file, f'{self._config_dir}/{CONFIG_FILE_COPY}')

        file_buffer = None
        with open(self._config_file, 'rb') as f:
            file_buffer = f.read()

        updated_file_buffer = file_buffer.replace(b'\x07', b'<bell hex sequence>')
        with open(self._config_file, 'wb') as f:
            f.write(updated_file_buffer)

        parser = et.XMLParser(target=et.TreeBuilder(insert_comments=True))
        tree = et.parse(self._config_file, parser)
        root = tree.getroot()
        if not root.tag == 'FLDIGI_DEFS':
            raise Exception('Expected root tag to be \'FLDIGI_DEFS\' but got {!r}'.format(self.root.tag))
        self._timestamp = os.path.getmtime(self._config_file)
        return tree
    
    def get_config(self, tag):
        root = self._config_tree.getroot()
        node = root.find(tag)
        if node is not None:
            return node.text
        return None
    
    def search_config(self, tag_part):
        root = self._config_tree.getroot()
        results = []
        tag_part_up = tag_part.upper()
        for child in root:
            if (type(child.tag) == str) and (tag_part_up in child.tag.upper()):
                results.append(child.tag)
        return results if results else None
    
    def set_config(self, tag, new_value) -> bool:
        '''Returns bool on success'''
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
    
    def _update_tree(self):
        new_tree = self._parse_config_file()
        self._config_tree = new_tree

    def read_changes(self):
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
    
    def run(self):
        while True:
            # check if the timestamp changed
            new_timestamp = os.path.getmtime(self._config_file)
            if new_timestamp != self._timestamp:
                self.read_changes()
                self._update_tree()
            sleep(self._interval)

    #### Gets and Sets for Popular Config items ####
    def get_confirm_exit(self) -> bool:
        return self.get_config('CONFIRMEXIT')
    
    def get_log_file_name(self) -> bool:
        return self.get_config('LOGBOOKFILENAME')
    
    def get_port_in_device(self) -> bool:
        return self.get_config('PORTINDEVICE')
    
    def get_port_out_device(self) -> bool:
        return self.get_config('PORTOUTDEVICE')
    
    def get_full_duplex(self) -> bool:
        return self.get_config('IS_FULL_DUPLEX')
    
    def get_audio_io(self) -> bool:
        ''' Audio subsystem.  Values are as follows:
        0: OSS; 1: PortAudio; 2: PulseAudio; 3: File I/O'''
        return self.get_config('AUDIOIO')
    
    def set_confirm_exit(self, new_val) -> bool:
        return self.set_config('CONFIRMEXIT', new_val)
    
    def set_log_file_name(self, new_val) -> bool:
        return self.set_config('LOGBOOKFILENAME', new_val)
    
    def set_port_in_device(self, new_val) -> bool:
        return self.set_config('PORTINDEVICE', new_val)
    
    def set_port_out_device(self, new_val) -> bool:
        return self.set_config('PORTOUTDEVICE', new_val)
    
    def set_full_duplex(self, new_val) -> bool:
        return self.set_config('IS_FULL_DUPLEX', new_val)
    
    def set_audio_io(self, new_val) -> bool:
        ''' Audio subsystem.  Values are as follows:
        0: OSS; 1: PortAudio; 2: PulseAudio; 3: File I/O'''
        return self.set_config('AUDIOIO', new_val)
