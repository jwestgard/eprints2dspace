fields = [{
    'source':      'title',
    'destination': 'dc.title',
    'required':    True,
    'unique':      True,
    'condition':   None,
    'mapping':     None,
    'pattern':     None
    },{
    'source':      'creator',
    'destination': 'dc.contributor.author',
    'required':    False,
    'unique':      False,
    'condition':   None,
    'mapping':     None,
    'pattern':     None
    },{
    'source':      'contributor',
    'destination': 'dc.contributor.author',
    'required':    False,
    'unique':      False,
    'condition':   None,
    'mapping':     None,
    'pattern':     None
    },{
    'source':      'publisher',
    'destination': 'dc.contributor.publisher',
    'required':    False,
    'unique':      True,
    'condition':   None,
    'mapping':     None,
    'pattern':     None
     },{
    'source':      'type',
    'destination': 'dc.type',
    'required':    False,
    'unique':      False,
    'condition':   None,
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
        },
    'pattern':     None
    },{
    'source':      'identifier',
    'destination': 'dc.identifier.citation',
    'required':    False,
    'unique':      False,
    'condition':   lambda x: not x.startswith('http://health-equity.lib.umd.edu'),
    'mapping':     None,
    'pattern':     None
    },{
    'source':      'identifier',
    'destination': 'binaries',
    'required':    False,
    'unique':      False,
    'condition':   lambda x: x.startswith('http://health-equity.lib.umd.edu'),
    'mapping':     None,
    'pattern':     None
    },{
    'source':      'relation',
    'destination': 'dc.identifier.other',
    'required':    True,
    'unique':      False,
    'condition':   lambda x: x.startswith('http://health-equity.lib.umd.edu'),
    'mapping':     None,
    'pattern':     r'http://health-equity\.lib\.umd\.edu/(\d+)'
    },{
    'source':      'relation',
    'destination': 'dc.description.uri',
    'required':    False,
    'unique':      False,
    'condition':   lambda x: not x.startswith('http://health-equity.lib.umd.edu'),
    'mapping':     None,
    'pattern':     None
    },{
    'source':      'date',
    'destination': 'dc.date.issued',
    'required':    True,
    'unique':      True,
    'condition':   None,
    'mapping':     None,
    'pattern':     r'(\d{4})'
    },{
    'source':      'identifier',
    'destination': 'dc.identifier.isbn',
    'required':    False,
    'unique':      False,
    'condition':   lambda x: not x.startswith('http://health-equity.lib.umd.edu'),
    'mapping':     None,
    'pattern':     r'ISBN\s+([\S]+)'
    },{
    'source':      'identifier',
    'destination': 'dc.identifier.issn',
    'required':    False,
    'unique':      False,
    'condition':   lambda x: not x.startswith('http://health-equity.lib.umd.edu'),
    'mapping':     None,
    'pattern':     'ISSN\s+([\S]+)'
    }
]

defaults = {
    'dc.contributor.author': 'UNSPECIFIED'
    }

