#!/usr/bin/env python3

import os
import requests


class Eprint():

    '''Python representation of a single resource from an Eprints repository'''

    def __init__(self, id):
        self.id = id


    def parse_dc_file(self, filepath):
    
        '''Parse a textfile of dublin-core keys and values 
           into attributes on the python object'''
           
        with open(filepath, 'r') as inputfile:
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



class Server():

    '''Host Eprints server from which data is to be exported'''
    
    def __init__(self, config):
        self.host_name = config.get_property('eprints_host')
        self.archive_name = config.get_property('eprints_archive')
        self.dc_path = config.get_property('dc_export_path')


    def get(self, id):
        query = os.path.join(self.host_name, self.dc_path.format(id, self.archive_name))
        print(query)