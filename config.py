
source = {
    'host_name': 'http://health-equity.lib.umd.edu',
    'query_path': 'cgi/export/{0}/DC/{1}-{0}.txt',
    'archive': 'minorityhealth-archive'
    }

batch = {
    'id_range': '1-4500',
    'local_root': 'data'
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
