#!/usr/bin/env python3

from csv import DictReader
import json
from lxml import etree
import os
from shutil import copy
import sys
import yaml
from zipfile import ZipFile



class SafPackage():

    '''Class for building Dspace Simple Archive Format packages'''

    def __init__(self, packagedir):
        self.packagedir = packagedir
        self.items = []

    def write(self):
        pass


class SafResource():

    '''Class for an individual resource arranged for inclusion in a SAF package'''

    def __init__(self):
        pass


class DSpaceSAF():

    def __init__(self, metadata, inputpath, outputpath):
        # read metadata
        self.id        = metadata.get('dc.identifier.other')
        self.metadata  = metadata
        self.files_dir = inputpath
        self.saf_dir   = outputpath
        self.contents  = os.path.join(self.saf_dir, 'contents')
        self.dc_file   = os.path.join(self.saf_dir, 'dublin_core.xml')
        self.zip       = os.path.join(self.saf_dir, 'revisions.zip')

        # walk files and generate SAF package
        os.mkdir(self.saf_dir)
        self.walk_files()
        self.create_revisions()
        self.write_contents()
        self.write_dcxml()
        self.copy_files()

    def walk_files(self):
        '''Walk a given directory tree and add absolute paths to all files
        to two lists, one for regular files, one for revisions xml files'''
        self.files = []
        self.revisions = []
        for root, dirs, files in os.walk(self.files_dir):
            for f in files:
                fullpath = os.path.join(root, f)
                if f.startswith('.'):  # skip hidden files
                    continue
                elif root.endswith('revisions'):
                    self.revisions.append(fullpath)
                else:
                    self.files.append(fullpath)

    def write_contents(self):
        '''Write constituent files, one per line, to the contents file'''
        with open(self.contents, 'w') as handle:
            handle.write("\n".join([os.path.basename(f) for f in self.files]))

    def create_revisions(self):
        '''Create a ZIP archive called revisions.zip that contains all xml
        files from the EPrints revisions directory'''
        with ZipFile(self.zip, 'a') as zip:
            [zip.write(f, arcname=os.path.basename(f)) for f in self.files]

    def write_dcxml(self):
        '''Generate an DC XML file from the metadata spreadsheet and 
        serialize it to the file dublin_core.xml'''
        root = etree.Element("dublin_core")
        for key, value in self.metadata.items():
            element = key.split('.')[1]
            try:
                qualifier = key.split('.')[2]
            except IndexError:
                qualifier = None
            if value is not None and value != '':
                for instance in value.split(" || "):
                    child = etree.Element("dcvalue", element=element)
                    if qualifier is not None:
                        child.set('qualifier', qualifier)
                    child.text = instance
                    root.append(child)
        with open(self.dc_file, 'wb') as handle:
            et = etree.ElementTree(root)
            et.write(handle, xml_declaration=True, encoding='UTF-8',
                        pretty_print=True)

    def copy_files(self):
        '''Make a copy of each file in the eprints item directory in the 
        SAF item directory'''
        [copy(f, self.saf_dir) for f in self.files]


"""

def main():
    print_header()
    # load batch configuration
    print('Loading batch configuration...')
    with open(sys.argv[1]) as handle:
        config = yaml.load(handle)
    # load lookup dictionary
    print('Creating files lookup dictionary...')
    lookup = DirLookup(os.path.join(config['ROOT'], 
                                    config['PATH_LOOKUP']))
    # load metadata spreadsheet
    spreadsheet = os.path.join(config['ROOT'], 
                               config['METADATA'])
    # base dir for input
    files_base = os.path.join(config['ROOT'], config['DATA'])
    print('Pulling eprints files from {0}...'.format(files_base))
    # base dir for output
    saf_base = os.path.join(config['ROOT'], config['SAF_DIR'])
    print('Writing SAF packages to {0}...'.format(saf_base))
    try:
        os.mkdir(saf_base)
        print('Creating output dir {0}...'.format(saf_base))
    except FileExistsError:
        print('Output dir exists. Aborting batch.'.format(saf_base))
        sys.exit()
    # walk the data
    print('Reading metadata spreadsheet...')
    with open(spreadsheet) as handle:
        reader = DictReader(handle)
        print('Processing batch items...')
        for n, row in enumerate(reader, 1):
            id = row['dc.identifier.other']
            title = row['dc.title']
            print('  --> ({0}) EPrint #{1}: {2}'.format(n, id, title[:50]))
            # lookup path using eprint id
            relpath = lookup.get(id)
            input_dir = os.path.join(files_base, relpath)
            # generate output path
            output_dir = os.path.join(saf_base, 'Item_{0}'.format(n))
            # create SAF object
            saf = DSpaceSAF(dict(row), input_dir, output_dir)

"""