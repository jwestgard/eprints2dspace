#!/usr/bin/env python3

import csv
import logging
import os
import requests

from .batch import *
from .transform import *
from .mapping import *

def main():

    '''(1) Start from list of eprint ids'''

    print_header()
    args = parse_args()
    batch = Batch(args.config, args.mapfile)

    logfile = os.path.join(
        batch.log_dir, 
        dt.now().strftime("%Y%m%d%H%M%S") + '.txt'
        )
    logging.basicConfig(filename=logfile, level=logging.INFO)
    logging.info('Created batch with {} items'.format(len(batch.contents)))
    logging.info('Created source server object at {}'.format(batch.source.host_name))
    logging.info('Caching extracted data at {}'.format(batch.local_cache))
    logging.info('Created destination package at {}'.format(batch.destination.root))

    for n, res in enumerate(batch.contents):

        '''(2) Pull metadata or read files from data dir'''

        eprint = EprintsResource(res.id, batch.local_cache, batch.source.query_pattern)
        
        if not res.extracted:
            if eprint.is_cached():
                logging.info('Found in cache')
                res.extracted = True
            else:
                logging.info('Querying server')
                status = eprint.server_response()
                if status == 200:
                    eprint.cache_locally()
                    res.extracted = True
                else:
                    logging.error(f'Could not reach {eprint.id}, response {status}')
                    res.extracted = False
                    res.extracted_reason = status
                    continue

        '''(3) Transform metadata'''

        if not res.transformed:
            transformed_metadata = transform(eprint.local_path)
            res.transformed = True
            print(n, transformed_metadata['dc.title'][0])

        '''(4) Write SAF'''
        if not res.loaded:
            sr = SafResource(eprint.id, transformed_metadata, batch.destination)
            sr.write_dcxml_file()
            sr.write_contents_file()

    '''(5) Summarize batch processing results'''
    
    batch.write_mapfile()


if __name__ == "__main__":
    main()
