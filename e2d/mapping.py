def update_redirect(url):
    '''Follow 301/308 redirects and return new location, else return original'''
    try:
        response = requests.head(url, timeout=30)
        status = response.status_code
        print(f'  => {status} {url}')
        if status in [301, 307]:
            response = requests.get(response.url, timeout=30)
            url = response.url
            print(f'  => Found a redirect to {url}')
        return url
    except:
        return url

fields = [{
    'source':      'title',
    'destination': 'dc.title',
    'required':    True,
    'unique':      True
    },{
    'source':      'creator',
    'destination': 'dc.contributor.author'
    },{
    'source':      'contributor',
    'destination': 'dc.contributor.author'
    },{
    'source':      'publisher',
    'destination': 'dc.publisher',
    'unique':      True
     },{
    'source':      'type',
    'destination': 'dc.type',
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
    'condition':   lambda x: not x.startswith(
                        'http://health-equity.lib.umd.edu'
                        ),
    'replace':     (r'((ISBN|ISSN)\s+[\dX-]+)\s*', '')
    },{
    'source':      'identifier',
    'destination': 'binaries',
    'condition':   lambda x: x.startswith(
                        'http://health-equity.lib.umd.edu'
                        )
    },{
    'source':      'relation',
    'destination': 'dc.identifier.other',
    'required':    True,
    'condition':   lambda x: x.startswith(
                        'http://health-equity.lib.umd.edu'
                        ),
    'replace':     (r'http://health-equity\.lib\.umd\.edu/(\d+)/', 
                        r'Eprint ID \1'
                        )
    },{
    'source':      'relation',
    'destination': 'dc.description.uri',
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
    'condition':   lambda x: not x.startswith(
                        'http://health-equity.lib.umd.edu'
                        ),
    'match':       r'ISBN\s+([\S]+)'
    },{
    'source':      'identifier',
    'destination': 'dc.identifier.issn',
    'condition':   lambda x: not x.startswith(
                        'http://health-equity.lib.umd.edu'
                        ),
    'match':       r'ISSN\s+([\S]+)'
    },{
    'source':      'subject',
    'destination': 'dc.subject'
    },{
    'source':      'description',
    'destination': 'dc.description.abstract'
    }
]

defaults = {
    'dc.contributor.author': 'UNSPECIFIED'
    }

