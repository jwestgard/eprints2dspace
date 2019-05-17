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


    def map_source_metadata(self):

        '''Clean and map DC export from Eprints to DC metadata fields for Dspace'''

        REQUIRED      = ['title', 'date']
        SINGLE_VALUED = ['title', 'date']

        # Check for required fields:
        for field in REQUIRED:
            if field not in self.source:
                print(f'ERROR: {self.eprint_id} has no field "{field}"')
                return

        for field in SINGLE_VALUED:
            if len(self.source[field]) > 1:
                print(f'ERROR: {self.eprint_id} has multiple fields {field}')
                return

        self.metadata['dc.title']                 = self.source['title']
        #self.metadata['dc.contributor.author']    = self.source['author']
        #self.metadata['dc.contributor.publisher'] = self.source['publisher']
        self.metadata['dc.identifier.other']      = self.eprint_id
        self.metadata['dc.citation']              = self.source['identifier']
        self.metadata['dc.date.issued']           = self.source['date']
        self.metadata['dc.description.uri']       = self.source['relation']
        print(self.metadata)


    def extract_issn_isbn(self):

        self.metadata['dc.identifier.issn']       = self.source['citation']
        self.metadata['dc.identifier.isbn']       = self.source['citation']
        
        '''
        creator = dc.contributor.author (UNSPECIFIED added to entries without an author; see below)
        contributor = dc.contributor.author
        publisher = dc.contributor.publisher
        type = dc.type
        id = dc.identifier.other (this is the EPrints ID)
        identifier = dc.citation
        date = dc.date.issued
        title = dc.title
        relation = dc.description.uri (links to outside document)
        ISSN = dc.identifier.issn (extracted from Identifier field/dc.citation)
        ISBN = dc.identifier.isbn (extracted from Identifier field/dc.citation)
        Add UNSPECIFIED to dc.contributor.author entries that are blank (both creator and contributor fields in MHHEA get mapped to dc.contributor.author so both need to be blank)
        Map the following document types from MHHEA (type) to DRUM (dc.type); need to verify that all MHHEA document types are accounted for in DRUM
            audio = other
            teaching resource = learning object
            thesis or dissertation = thesis
            report document or other monograph = technical report
            conference or workshop item = presentation
            book section = book chapter
        Remove unnecessary URLs from the Identifier (dc.citation) field 
        Remove ISSN and ISBN from the Identifier (dc.citation) field
        Remove MHHEA URL from the Relation (dc.description.uri) field leaving only the external URL
        In the Type (dc.type) field, remove PeerReviewed NonPeerReviewed (only one entry is allowed for DOI)
        Date (dc.date) field must conform to format YYYY
        Delete the Format column
        Remove the following files from records: revisions.zip, preview.jpg, and indexcodes.txt
        '''



    def write_dcxml(self):

        '''Generate XML from the eprint metadata and serialize to dublin_core.xml'''

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


    def write_contents(self):

        '''Write constituent files, one per line, to the contents file'''

        with open(self.cont_file, 'w') as handle:
            handle.write("\n".join([os.path.basename(f) for f in self.binaries]))


