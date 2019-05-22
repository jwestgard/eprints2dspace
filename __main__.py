#!/usr/bin/env python3

import argparse
import csv
from datetime import datetime as dt
import logging
import os
import requests
import sys
import config as cfg

from extract import EprintsResource
from extract import EprintsServer
from load import SafPackage
from load import SafResource
from transform import *


class Batch():

    '''Class for iterating over a set of resources to be extracted'''

    def __init__(self, batch_config, source_config):
        self.id_range      = batch_config['id_range']
        self.eprints_dir   = batch_config['eprints_dir']
        self.saf_dir       = batch_config['saf_dir']
        self.server        = EprintsServer(**source_config)
        self.cursor        = 0
        self.ids           = self.generate_id_range()
        self.max_id_length = len(str(self.ids[-1]))

        if not os.path.exists(self.eprints_dir):
            os.makedirs(self.eprints_dir)
        if not os.path.exists(self.saf_dir):
            os.makedirs(self.saf_dir)

    def generate_id_range(self):
        limits = self.id_range.split('-')
        first  = int(limits[0])
        last   = int(limits[1]) if len(limits) > 1 else first
        return [id for id in range(first, last + 1)]

    def __iter__(self):
        return self

    def __next__(self):
        try:
            eprint = EprintsResource(self.ids[self.cursor], 
                        self.eprints_dir, self.server.query_pattern)
            self.cursor += 1
            return eprint
        except IndexError:
            raise StopIteration()


def main():

    '''(1) Start from list of eprint ids'''

    # Set up logging
    logdir  = cfg.logs['dir']
    logfile = dt.now().strftime("%Y%m%d%H%M%S") + '.txt'
    logpath = os.path.join(logdir, logfile)
    logging.basicConfig(filename=logpath, level=logging.INFO)

    # Initialize batch
    batch = Batch(cfg.batch, cfg.source)
    saf = SafPackage(batch.saf_dir, batch.max_id_length)
    logging.info('Batch created with {} IDs'.format(len(batch.ids)))

    errfile = os.path.join(logdir, cfg.logs['skipfile'])
    mapfile = os.path.join(logdir, cfg.logs['mapfile'])
    fieldnames = ['id', 'title', 'creator', 'date', 'relation', 'filename',
                  'subject', 'type', 'format', 'identifier', 'description', 
                  'publisher', 'contributor']

    handleErrs = open(os.path.join(logdir, 'errors.csv'), 'w')
    handle400s = open(os.path.join(logdir, '400s.csv'),   'w')
    handle300s = open(os.path.join(logdir, '300s.csv'),   'w')
    handle200s = open(os.path.join(logdir, '200s.csv'),   'w')

    with open(errfile, 'w') as errhandle, open(mapfile, 'w') as maphandle:
        errlog = csv.writer(errhandle)
        maplog = csv.DictWriter(maphandle, fieldnames=fieldnames)
        maplog.writeheader()

        '''(2) Pull metadata or read files from data dir'''

        link_count = 0
        for n, eprint in enumerate(batch, 1):
            msg = 'Total checked: {0} | External links: {1}'
            print(msg.format(n, link_count), end='\r')
            if not eprint.is_cached():
                status = eprint.server_response()
                if status == 200:
                    eprint.cache_locally()
                else:
                    errlog.writerow([eprint.id, status, eprint.query_path])
                    continue

            '''(3) Transform metadata'''
            metadata = parse_metadata(eprint.local_path)

            for rel in metadata['relation']:
                if not rel.startswith(batch.server.host_name):
                    link_count += 1
                    (status, msg, orig, new) = check_ext_link(rel)
                    fields = (eprint.id, status, msg, orig, new)
                    result = [str(field) for field in fields]
                    if status == "error":
                        handleErrs.write(','.join(result) + '\n')
                        handleErrs.flush()
                    elif status >= 400:
                        handle400s.write(','.join(result) + '\n')
                        handle400s.flush()
                    elif status >= 300:
                        handle300s.write(','.join(result) + '\n')
                        handle300s.flush()
                    elif status >= 200:
                        handle200s.write(','.join(result) + '\n')
                        handle200s.flush()

    handleErrs.close()
    handle400s.close()
    handle300s.close()
    handle200s.close()
                

if __name__ == "__main__":
    main()
