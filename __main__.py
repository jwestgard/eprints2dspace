#!/usr/bin/env python3

import argparse
import csv
from eprints import Eprint
from dspace import SafPackage
import os
import requests
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


class Batch():

    '''Class for managing a particular migration batch'''

    def __init__(self, config):
        self.host           = config.get_property('EPRINTS_HOST')
        self.path           = config.get_property('EPRINTS_QUERY')
        self.query_template = os.path.join(self.host, self.path)
        self.archive_name   = config.get_property('EPRINTS_ARCHIVE')
        self.export_range   = config.get_property('EPRINTS_RANGE')
        self.local_cache    = config.get_property('EPRINTS_LOCAL')
        self.mapfile        = config.get_property('MAPFILE')
        self.errfile        = config.get_property('ERRFILE')
        self.logdir         = config.get_property('LOG_DIR')
        self.ids            = self.get_id_range()
        self.cursor         = 0

    def get_id_range(self):
        begin, end = self.export_range.split('-')
        return [id for id in range(int(begin), int(end)+1)]

    def __iter__(self):
        return self

    def __next__(self):
        if self.cursor < len(self.ids):
            id = self.ids[self.cursor]
            self.cursor += 1
            return id
        else:
            #self.logger.info('Processing complete!')
            raise StopIteration()


def main():

    '''(1) Start from list of eprint ids'''

    config = Config('config.yml')
    batch = Batch(config)
    errfile = os.path.join(batch.logdir, batch.errfile)
    mapfile = os.path.join(batch.logdir, batch.mapfile)
    fieldnames = ['id', 'title', 'creator', 'date', 'relation', 'filename',
                  'subject', 'type', 'format', 'identifier', 'description', 'publisher',
                  'contributor']

    with open(errfile, 'w') as errhandle, open(mapfile, 'w') as maphandle:
        errlog = csv.writer(errhandle)
        maplog = csv.DictWriter(maphandle, fieldnames=fieldnames)
        maplog.writeheader()
        
        '''(2) Pull metadata or read files from data dir'''
        
        for id in batch:
            eprint = Eprint(id)
            local_path = os.path.join(batch.local_cache, eprint.filename)
            
            # check for a cached metadata file, pull from server if not found
            if not os.path.isfile(local_path):
                query = batch.query_template.format(id, batch.archive_name)
                response = requests.get(query)
                if response.status_code == 200:
                    with open(local_path, 'w') as handle:
                        handle.write(response.text)
                else:
                    errlog.writerow([id, response.status_code, query])
                    continue
                
            '''(3) Parse metadata file'''
            
            with open(local_path, 'r') as handle:
                eprint.parse(handle.read())
                maplog.writerow(eprint.to_csv())


    '''(4) Transform metadata'''
    '''(5) Write to SAF package'''



if __name__ == "__main__":
    main()
        


