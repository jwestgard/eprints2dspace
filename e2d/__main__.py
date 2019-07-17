#!/usr/bin/env python3

import csv
from importlib import import_module
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
        batch.log_dir, dt.now().strftime("%Y%m%d%H%M%S") + '.txt'
        )
    logging.basicConfig(
        filename=logfile, level=logging.INFO
        )
    logging.info(
        'Created batch with {} items'.format(len(batch.contents))
        )
    logging.info(
        'Created source server object at {}'.format(batch.source.host_name)
        )
    logging.info(
        'Caching extracted data at {}'.format(batch.local_cache)
        )
    logging.info(
        'Created destination package at {}'.format(batch.destination.root)
        )


    for n, res in enumerate(batch.contents):

        '''(2) Pull metadata or read files from data dir'''

        eprint = EprintsResource(
            res.id, batch.local_cache, batch.source.query_pattern
            )
        
        print(f'Creating item {res.id}', end='\r', file=sys.stdout)
        
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
                    logging.error(
                        f'Could not reach {eprint.id}, response {status}'
                        )
                    res.extracted = False
                    res.not_ext_reason = status
                    continue

        '''(3) Transform metadata'''

        if not res.transformed:
            try:
                transformed_metadata = transform(eprint.local_path)
                res.transformed = True
                title = transformed_metadata['dc.title'][0]
                logging.info(f'Successfully transformed {title[:20]}')
            except:
                res.transformed = False
                res.not_trans_reason = 'transformation error'
                logging.error(f'Could not transform metadata for {eprint.id}')
                continue

        '''(4) Write SAF'''

        if not res.loaded:
            try:
                sr = SafResource(
                    eprint.id, transformed_metadata, batch.destination
                    )
                sr.write_dcxml_file()
                sr.write_contents_file()
                sr.fetch_binaries()
                res.loaded = True
            except:
                res.loaded = False
                res.not_loaded_reason = 'could not create SAF'
                continue

    print('\nBatch complete!', file=sys.stdout)

    '''(5) Do any specified extra actions'''
    '''print('Applying extra actions', file=sys.stdout)
    for n, action in enumerate(batch.extra, 1):
        modpath = action['module']
        params = [p for p in action['parameters']]
        print(f'  {n}. Calling {modpath.rstrip(".")} with {params}', 
                file=sys.stdout)
        module = import_module(modpath, package='e2d.extra')
        module.main(*params)'''

    '''(5) Summarize batch processing results''' 
    
    batch.write_mapfile()


if __name__ == "__main__":
    main()
