#!/usr/bin/env python3

class SafPackage():

    '''Class for building Dspace Simple Archive Format packages'''

    def __init__(self, packagedir):
        self.packagedir = packagedir
        self.items = []

    def write(self):
        pass


class SafItem():

    '''Class for an individual resource arranged for inclusion in a SAF package'''

    def __init__(self):
        pass