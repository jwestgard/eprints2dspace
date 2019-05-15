#!/usr/bin/env python3

import os
import requests


class Eprint():

    '''Python representation of a single resource from an Eprints repository'''

    def __init__(self, id, config):
        host = config.get_property('eprints_host')
        query_path = config.get_property('dc_export_path')
        archive = config.get_property('eprints_archive')
        self.id = id
        self.filename = f"{self.id}.txt"
        self.local_path = os.path.join(config.get_property('export_dir'), self.filename)
        self.server_path = os.path.join(host, query_path.format(self.id, archive))


    def check_server(self):
        response = requests.get(self.server_path)
        if response.status_code == 200:
            return response.text
        else:
            return None


    def fetch_metadata(self):
        if not os.path.isfile(self.local_path):
            response = self.check_server()
            if response:
                with open(self.local_path, 'w') as handle:
                    handle.write(response)
            else:
                return
        self.parse_metadata_file()


    def parse_metadata_file(self):
    
        '''Parse a textfile of dublin-core keys and values 
           into attributes on the python object'''
           
        with open(self.local_path, 'r') as inputfile:
            contents = inputfile.read().split('\n')
            
        for n, line in enumerate(contents):
            # ignore blank lines and lines with only whitespace
            line = line.strip()
            if line == '':
                continue
            else:
                # split line on first colon
                key, value = tuple(line.split(': ', 1))
                # default to empty list
                attrib_list = getattr(self, key, [])
                # update the existing value list and then the attribute
                attrib_list.append(value)
                setattr(self, key, attrib_list)


    def display_metadata(self):
        for k, v in self.__dict__.items():
            print("{} => {}".format(k, v))

