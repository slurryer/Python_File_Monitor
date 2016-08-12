
# coding: utf-8

# In[ ]:

import configparser
from glob import glob
import os
import shutil
import tempfile

class File_Monitor:
    """Monitor and movement and triggers of files in the restructured Triage folder"""
    
    def __init__(self, config_file):
        self.monitor_sources = dict()
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
    
    def __getitem__(self,monitor):
        return self.config[monitor]
        
    def __len__(self):
        return(len(self.monitors()))
    
    def monitors(self):
        monitors = [monitor_name for monitor_name in self.config]
        return monitors[2:]
    
    def conditions(self, monitor):
        conditions = list()
        monitor_actions = self.config[monitor]
        for item, value in monitor_actions.items():
            if 'condition' in item:
                conditions.append(value)
        return conditions
            
    def execute_monitor(self, monitor):
        home = self.config['HOME']['PATH']
        monitor_source_folder = self.config[monitor]['SOURCE']
        monitor_destination_folder = self.config[monitor]['DESTINATION']
        
        source_folder = os.path.join(home, monitor_source_folder)
        destination_folder = os.path.join(home, monitor_destination_folder)
        conditions = self.conditions(monitor)
        
        # Generate a list of all files in source matching conditions
        source_targeted_files = list()
        for condition in conditions:
            
            source_filter = os.path.join(source_folder, condition)
            source_targeted_files.extend(glob(source_filter))
        print(monitor)
        if len(source_targeted_files) > 0:
            for s in source_targeted_files:
                path, source_filename = os.path.split(s)
                source_path = os.path.join(source_folder, source_filename)
                dest_path = os.path.join(destination_folder, source_filename)

                shutil.move(source_path, dest_path)
         

