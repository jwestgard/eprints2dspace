#!/usr/bin/env python3

import argparse
import csv
import logging
import os
import requests
import sys
import yaml

from extract import EprintServer
from extract import EprintResource
from load import SafPackage
from load import SafResource
from transform import *

class Batch():

    '''Class for managing a particular migration batch'''

    def __init__(self, config):
        self.host           = config['EPRINTS_HOST']
        self.path           = config['EPRINTS_QUERY']
        self.query_template = os.path.join(self.host, self.path)
        self.archive_name   = config['EPRINTS_ARCHIVE']
        self.export_range   = config['EPRINTS_RANGE']
        self.local_cache    = config['EPRINTS_LOCAL']
        self.mapfile        = config['MAPFILE']
        self.errfile        = config['ERRFILE']
        self.logdir         = config['LOG_DIR']
        self.ids            = self.get_id_range()
        self.cursor         = 0
        self.dspace_host    = config['DSPACE_HOST']
        self.dspace_saf     = config['DSPACE_SAF_ROOT']
        self.dspace_handle  = config['DSPACE_HANDLE']

    def get_id_range(self):
        self.first, self.last = self.export_range.split('-')
        return [id for id in range(int(self.first), int(self.last)+1)]

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

    config = yaml.safe_load('config.yml')
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

            package = SafPackage(batch)
            resource = SafResource(eprint, package)
            
            print(resource.path)
            resource.map_source_metadata()



    '''(5) Write to SAF package'''



if __name__ == "__main__":
    main()
        


