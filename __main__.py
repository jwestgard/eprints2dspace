#!/usr/bin/env python3

import argparse
import csv
from datetime import datetime as dt
import logging
import os
import requests
import sys

import config as cfg
from extract import Batch
from load import SafPackage
from load import SafResource
from transform import *


def main():

    '''(1) Start from list of eprint ids'''

    logfile = dt.now().strftime("%Y%m%d%H%M%S") + '.txt'
    logpath = os.path.join(cfg.logs['dir'], logfile)
    logging.basicConfig(filename=logpath, level=logging.INFO)

    batch = Batch(cfg.batch, cfg.source)
    logging.info('Batch created with {} resources'.format(len(batch.items)))
    
    for eprint in batch:
        if eprint.reachable:
            print(eprint.title)
        else:
            print('{} not reachable'.format(eprint.id))


    
    """
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
    """



    '''(5) Write to SAF package'''



if __name__ == "__main__":
    main()
