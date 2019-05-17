import re

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

    for uri in self.source['relation']:
        if uri.startswith('http://health-equity.lib.umd.edu'):
            pass

    self.metadata['dc.title']                 = self.source['title'][0]
    #self.metadata['dc.contributor.author']    = self.source['author']
    #self.metadata['dc.contributor.publisher'] = self.source['publisher']
    self.metadata['dc.identifier.other']      = self.eprint_id
    self.metadata['dc.citation']              = self.source['identifier']
    self.metadata['dc.date.issued']           = self.source['date'][0]
    self.metadata['dc.description.uri']       = self.source['relation']
    print(self.metadata)


def extract_issn_isbn(self):
    pass
        
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
