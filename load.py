#!/usr/bin/env python3

from lxml import etree
import os
from shutil import copy
import sys
import yaml
from zipfile import ZipFile



class SafPackage():

    '''Class for building Dspace Simple Archive Format packages'''

    def __init__(self, batch):
        self.root       = batch.dspace_saf
        self.num_places = len(batch.last)

        os.makedirs(self.root, exist_ok=True)



class SafResource():

    '''Class for an individual resource arranged for inclusion in a SAF package'''

    def __init__(self, eprint, package):
        self.dir        = f'item_{int(eprint.id):0{package.num_places}d}'
        self.path       = os.path.join(package.root, self.dir)
        self.cont_file  = os.path.join(self.dir, 'contents')
        self.dc_file    = os.path.join(self.dir, 'dublin_core.xml')
        self.source     = eprint.__dict__
        self.eprint_id  = eprint.id
        self.metadata   = {}
        self.binaries   = []
        os.makedirs(self.path, exist_ok=True)



    def write_dcxml_file(self):

        '''Generate XML from the eprint metadata and serialize to dublin_core.xml'''

        root = etree.Element("dublin_core")
        for key, value in self.metadata.items():
            schema, element = key.split('.', 1)
            try:
                element, qualifier = element.split('.')
            except IndexError:
                qualifier = None
            if value is not None and value != '':
                for instance in value:
                    child = etree.Element("dcvalue", element=element)
                    if qualifier is not None:
                        child.set('qualifier', qualifier)
                    child.text = instance
                    root.append(child)

        with open(self.dc_file, 'wb') as handle:
            et = etree.ElementTree(root)
            et.write(handle, xml_declaration=True, encoding='UTF-8',
                        pretty_print=True)



    def write_contents_file(self):

        '''Write constituent files, one per line, to the contents file'''

        with open(self.cont_file, 'w') as handle:
            handle.write("\n".join([os.path.basename(f) for f in self.binaries]))


