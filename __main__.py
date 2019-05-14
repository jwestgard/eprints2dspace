#!/usr/bin/env python3

import argparse
from eprints import Eprint
from dspace import SafPackage
import sys
import yaml


class Config():

    '''Project configuration class'''

    def __init__(self, path):
        with open(path) as configfile:
            self._config = yaml.safe_load(configfile)
    
    def get_property(self, property_name):
        '''Return the value of key in the yaml or None if not found''' 
        return self._config.get(property_name, None)




'''
(1) Start from list of eprint ids
(2) Pull metadata or read files from data dir
(3) Parse metadata file 
(4) Transform metadata
(5) Write to SAF package
'''




if __name__ == "__main__":
    
    e = Eprint(10)
    print(e, e.id)
    e.parse_dc_file('data/export/minorityhealth-archive-3071.txt')
    print(e.__dict__)

    saf = SafPackage('foobar/')
    print(saf.packagedir)

    config = Config('config.yml')
    print(config.get_property('eprints_host'))
