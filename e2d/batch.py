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
        self.cursor      = 0

        # Parse config file and configure batch
        self.configfile  = configfile
        try:
            with open(self.configfile) as handle:
                config = yaml.safe_load(handle)
                self.__dict__.update(**config)
        except FileNotFoundError:
            print('cannot open configfile')
            sys.exit(1)

        self.mapfile     = Mapfile(mapfile, self.id_range)
        self.contents    = self.mapfile.read()
        self.ids         = [item.id for item in self.contents]
        self.max_width   = len(str(self.contents[-1].id))
        self.source      = EprintsServer(self.host_name, self.query_path)
        self.destination = SafPackage(self.saf_dir, self.max_width)
        if not os.path.exists(self.local_cache):
            os.makedirs(self.local_cache)
        if not os.path.exists(self.saf_dir):
            os.makedirs(self.saf_dir)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            current = self.contents[cursor] 
            self.cursor += 1
            return Resource(current)
        except IndexError:
            raise StopIteration()


class Mapfile():

    def __init__(self, path, id_range):
        self.path = path
        self.id_range = id_range
        
    def read(self):
        try:
            with open(self.path) as handle:
                print("Mapfile exists...reading...", file=sys.stdout)
                reader = csv.DictReader(handle)
                self.data = [dict(row) for row in reader]
                if len(self.data) == 0:
                    raise FileNotFoundError
                return self.data
        except FileNotFoundError:
            print("Mapfile does not exist or is empty...pulling ids from config...",
                  file=sys.stdout)
            limits = self.id_range.split('-')
            first  = int(limits[0])
            last   = int(limits[1]) if len(limits) > 1 else first
            return [Resource(id=id) for id in range(first, last + 1)]

    def write(self, data):
        fieldnames = ['id', 'action', 'special', 
                      'binaries', 'link', 'response', 
                      'newlink']
        rows = sorted(data, key=lambda row: row.id)
        with open(self.path, 'w') as handle:
            writer = csv.DictWriter(handle, 
                                    fieldnames=fieldnames, 
                                    extrasaction='ignore')
            writer.writeheader()
            for row in rows:
                writer.writerow(row.__dict__)


class Resource():
    '''Class that tracks item's progress in ETL process'''
    def __init__(self, **kwargs):
        self.id         = int(kwargs.get('id'))
        self.action     = kwargs.get('action', 'include')
        self.special    = kwargs.get('special', None)
        self.binaries   = kwargs.get('binaries', None)
        self.link       = kwargs.get('link', None)
        self.response   = kwargs.get('response', None)
        self.newlink    = kwargs.get('newlink', None)


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
