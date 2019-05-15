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



def main():

    config = Config('config.yml')

    for id in range(3080, 3100):
    
        eprint = Eprint(id, config)
        eprint.fetch_metadata()
        eprint.display_metadata()
        
        saf = SafPackage(config)
        saf.write(eprint)



if __name__ == "__main__":
    main()
        

    '''
    (1) Start from list of eprint ids
    (2) Pull metadata or read files from data dir
    (3) Parse metadata file 
    (4) Transform metadata
    (5) Write to SAF package
    '''
