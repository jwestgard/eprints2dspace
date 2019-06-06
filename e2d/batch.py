import argparse
import csv
import logging
import os
import sys
import yaml

from datetime import datetime as dt

from .extract import EprintsResource
from .extract import EprintsServer
from .load import SafPackage
from .load import SafResource
from .transform import *


class Batch():

    '''Class for iterating over a set of resources to be extracted'''

    def __init__(self, configfile, mapfile):
        self.configfile  = configfile
        self.mapfile     = mapfile
        self.contents    = []
        self.cursor      = 0

        # Parse config file and configure batch
        try:
            with open(self.configfile) as handle:
                self.__dict__.update(**yaml.safe_load(handle))
        except FileNotFoundError:
            print('cannot open configfile')
            sys.exit(1)

        # Read mapfile or setup batch contents
        try:
            with open(self.mapfile) as handle:
                reader = csv.DictReader(handle)
                self.contents = [Resource(**row) for row in reader]
                if len(self.contents) == 0:
                    raise FileNotFoundError
        except FileNotFoundError:
            limits = self.id_range.split('-')
            first  = int(limits[0])
            last   = int(limits[1]) if len(limits) > 1 else first
            self.contents = [Resource(id) for id in range(first, last + 1)]

        last_item = self.contents[-1]
        self.max_width = len(str(last_item.id))
        self.source      = EprintsServer(self.host_name, self.query_path)
        self.destination = SafPackage(self.saf_dir, self.max_width)
        if not os.path.exists(self.local_cache):
            os.makedirs(self.local_cache)
        if not os.path.exists(self.saf_dir):
            os.makedirs(self.saf_dir)

    def write_mapfile(self):
        fieldnames = ['id', 'extracted', 'not_ext_reason', 
                      'transformed', 'not_trans_reason',
                      'link_check', 'orig_uri', 'new_uri',
                      'loaded', 'not_loaded_reason'
                      ]
        handle = open(self.mapfile, 'w')
        writer = csv.DictWriter(handle, 
                                fieldnames=fieldnames,
                                extrasaction='ignore'
                                )
        writer.writeheader()
        for resource in self.contents:
            writer.writerow(resource.__dict__)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            current = self.contents[cursor] 
            self.cursor += 1
            return current
        except IndexError:
            raise StopIteration()


class Resource():
    '''Class that tracks item's progress in ETL process'''
    def __init__(self, id, extracted=False, not_ext_reason=None, 
                 transformed=False, not_trans_reason=None, 
                 link_check=False, status=None, orig_uri=None, new_uri=None,
                 loaded=False, not_loaded_reason=None
                 ):
        self.id                 = int(id)
        self.extracted          = bool(extracted == 'True')
        self.not_ext_reason     = not_ext_reason
        self.transformed        = bool(transformed == 'True')
        self.not_trans_reason   = not_trans_reason
        self.link_check         = bool(link_check == 'True')
        self.status             = status
        self.orig_uri           = orig_uri
        self.new_uri            = new_uri
        self.loaded             = bool(loaded == 'True')
        self.not_loaded_reason  = not_loaded_reason


def print_header():
    '''Format and print a header to the console'''
    title = 'eprints2dspace'
    sys.stderr.write(
        '\n{0}\n{1}\n'.format(title, '=' * len(title))
        )


def parse_args():
    '''Parse args for setting up batch'''
    parser = argparse.ArgumentParser(description='Eprints to Dspace migration.')
    parser.add_argument('-v', '--version', 
                        action='version', 
                        help='print version number and exit',
                        version='%(prog)s 0.1'
                        )
    parser.add_argument('-c', '--config',
                        help='path to configuration file',
                        required='True',
                        action='store'
                        )
    parser.add_argument('-m', '--mapfile',
                        help='path to batch manifest',
                        required='True',
                        action='store'
                        )
    return parser.parse_args()
