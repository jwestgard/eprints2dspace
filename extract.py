#!/usr/bin/env python3

import os
import requests

class Batch:

    '''Class for iterating over a set of resources to be extracted'''

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


class EprintServer():
    

class EprintResource():

    '''Python representation of a single resource from an Eprints repository'''

    def __init__(self, id):
        self.id = str(id)
        self.filename = "{}.txt".format(self.id)


    def parse(self, txt):
        '''Parse dublin-core keys and values into attributes on the python object'''
        lines = [line.strip() for line in txt.split('\n') if line.strip() is not '']
        for n, line in enumerate(lines):
            # split line on first colon
            key, value = tuple(line.split(': ', 1))
            # default to empty list
            attrib_list = getattr(self, key, [])
            # update the existing value list and then the attribute
            attrib_list.append(value)
            setattr(self, key, attrib_list)


    def check_links(self, host):
        if hasattr(self, 'relation'):
            for link in self.relation:
                if link.startswith(host):
                    self.link_loc = link
                else:
                    self.link_ext = link
        if self.link_ext is not None:
            requests.get(self.link_ext)


    def fetch_binaries(self, host):
        for rel in self.relation:
            if rel.startswith(host):
                print(rel)


    def display_metadata(self):
        for k, v in self.__dict__.items():
            print("{} => {}".format(k, v))


    def to_csv(self):
        return {k: ' || '.join(v) for k, v in self.__dict__.items()}


