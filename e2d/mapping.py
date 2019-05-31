fields = [{
    'source':      'title',
    'destination': 'dc.title',
    'required':    True,
    'unique':      True
    },{
    'source':      'creator',
    'destination': 'dc.contributor.author',
    'required':    False,
    'unique':      False
    },{
    'source':      'contributor',
    'destination': 'dc.contributor.author',
    'required':    False,
    'unique':      False
    },{
    'source':      'publisher',
    'destination': 'dc.contributor.publisher',
    'required':    False,
    'unique':      True
     },{
    'source':      'type',
    'destination': 'dc.type',
    'required':    False,
    'unique':      False,
    'mapping': {
        'Article':                              'Article',
        'Book':                                 'Book',
        'Book Section':                         'Book Chapter',
        'Image':                                'Image',
        'Audio':                                'Other',
        'Video':                                'Video',
        'Teaching Resource':                    'Learning Object',
        'Thesis or Dissertation':               'Thesis',
        'Report Document or other Monograph':   'Technical Report',
        'Conference or Workshop Item':          'Presentation',
        'Other':                                'Other',
        'PeerReviewed':                         None,
        'NonPeerReviewed':                      None
        }
    },{
    'source':      'identifier',
    'destination': 'dc.identifier.citation',
    'required':    False,
    'unique':      False,
    'condition':   lambda x: not x.startswith(
                        'http://health-equity.lib.umd.edu'
                        )
    'replace':      r'((ISBN|ISSN) *[\dX-]+)\s'
    },{
    'source':      'identifier',
    'destination': 'binaries',
    'required':    False,
    'unique':      False,
    'condition':   lambda x: x.startswith(
                        'http://health-equity.lib.umd.edu'
                        )
    },{
    'source':      'relation',
    'destination': 'dc.identifier.other',
    'required':    True,
    'unique':      False,
    'condition':   lambda x: x.startswith(
                        'http://health-equity.lib.umd.edu'
                        ),
    'match':       r'http://health-equity\.lib\.umd\.edu/(\d+)'
    },{
    'source':      'relation',
    'destination': 'dc.description.uri',
    'required':    False,
    'unique':      False,
    'condition':   lambda x: not x.startswith(
                        'http://health-equity.lib.umd.edu'
                        )
    },{
    'source':      'date',
    'destination': 'dc.date.issued',
    'required':    True,
    'unique':      True,
    'match':       r'(\d{4})'
    },{
    'source':      'identifier',
    'destination': 'dc.identifier.isbn',
    'required':    False,
    'unique':      False,
    'condition':   lambda x: not x.startswith(
                        'http://health-equity.lib.umd.edu'
                        ),
    'match':       r'ISBN\s+([\S]+)'
    },{
    'source':      'identifier',
    'destination': 'dc.identifier.issn',
    'required':    False,
    'unique':      False,
    'condition':   lambda x: not x.startswith(
                        'http://health-equity.lib.umd.edu'
                        ),
    'match':       r'ISSN\s+([\S]+)'
    },{
    'source':      'subject',
    'destination': 'dc.subject',
    'required':    False,
    'unique':      False
    },{
    'source':      'description',
    'destination': 'dc.description.abstract',
    'required':    False,
    'unique':      False
    }
]

defaults = {
    'dc.contributor.author': 'UNSPECIFIED'
    }

