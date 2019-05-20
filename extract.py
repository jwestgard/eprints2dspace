#!/usr/bin/env python3

import os
import requests

class Batch():

    '''Class for iterating over a set of resources to be extracted'''

    def __init__(self, batch_config, source_config):
        self.__dict__.update(**batch_config)
        self.source = EprintsServer(**source_config)
        self.first_id, self.last_id = self.parse_id_range()
        self.max_id_length = len(str(self.last_id))
        self.items = [EprintsResource(i) for i in range(self.first_id, self.last_id + 1)]
        self.cursor = 0

    def parse_id_range(self):
        try:
            first, last = self.id_range.split('-')
            return (int(first), int(last))
        except IndexError:
            return (int(first), int(first))

    def __iter__(self):
        return self

    def __next__(self):
        try:
            eprint = self.items[self.cursor]
            self.cursor += 1
            eprint.local_cache = os.path.join(self.local_root, "eprints", eprint.filename)
            if not os.path.isfile(eprint.local_cache):
                q = self.source.query.format(eprint.id, self.source.archive)
                response = requests.get(q)
                if not response.status_code == 200:
                    eprint.reachable = False
                    return eprint
                else:
                    with open(eprint.local_cache, 'w') as handle:
                        handle.write(response.text)
            with open(eprint.local_cache) as handle:
                eprint.parse(handle.read())
                eprint.reachable = True
            return eprint
        except IndexError:
            raise StopIteration()


class EprintsServer():

    '''Python representation of a Eprints server'''

    def __init__(self, **config):
        self.__dict__.update(config)
        self.query = os.path.join(self.host_name, self.query_path)


class EprintsResource():

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


