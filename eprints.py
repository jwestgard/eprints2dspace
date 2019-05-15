#!/usr/bin/env python3

import os
import requests

class Eprint():

    '''Python representation of a single resource from an Eprints repository'''

    def __init__(self, id):
        self.id = str(id)
        self.filename = "{}.txt".format(self.id)
        self.title = None
        self.creator = [] 
        self.subject = []
        self.description = None
        self.date = None
        self.type = []
        self.format = None
        self.identifier = []
        self.relation = []

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

    def check_links(self, sitehost):
        if hasattr(self, 'relation'):
            for link in self.relation:
                if link.startswith(sitehost):
                    self.link_loc = link
                else:
                    self.link_ext = link
        if self.link_ext is not None:
            requests.get(self.link_ext)

    def fetch_binaries(self):
        for relation in self.

    def display_metadata(self):
        for k, v in self.__dict__.items():
            print("{} => {}".format(k, v))

