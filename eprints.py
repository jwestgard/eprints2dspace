#!/usr/bin/env python3

class Eprint():

    '''Python representation of a single resource from an Eprints repository'''

    def __init__(self, id):
        self.id = id

    def parse_dc_file(self, filepath):
        '''Parse a textfile of dublin-core keys and values 
           into attributes on the python object'''
        with open(filepath, 'r') as inputfile:
            contents = inputfile.read().split('\n')
            
        for n, line in enumerate(contents):
            # ignore blank lines and lines with only whitespace
            line = line.strip()
            if line == '':
                continue
            else:
                # split line on first colon
                key, value = tuple(line.split(': ', 1))
                # default to empty list so any attribute can be multivalued
                default = list()
                new = getattr(self, key, default)
                setattr(self, key, new.append(value))
                print('\n', n)
                print(key)
                print(new)
                print(value)
                print(getattr(self, key))
               
