
source = {
    'host_name': 'http://health-equity.lib.umd.edu',
    'query_path': 'cgi/export/{0}/DC/minorityhealth-archive-{0}.txt'
    }

batch = {
    'id_range': '1-4500',
    'eprints_dir': 'data/eprints',
    'saf_dir': 'data/saf'
    }

transformations = {}

destination = {  
    'host_name': 'http://drum.lib.umd.edu',
    'handle': ""
    }

logs = {
    'dir': 'logs',
    'mapfile': 'mapfile.csv',
    'skipfile': 'skipfile.csv'
    }
