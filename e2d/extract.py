import os
import requests


class EprintsServer():

    '''Python representation of a Eprints server'''

    def __init__(self, host_name=None, query_path=None):
        self.host_name     = host_name
        self.query_pattern = os.path.join(self.host_name, query_path)


class EprintsResource():

    '''Python representation of a single resource from an Eprints repository'''

    def __init__(self, id, cache_dir, query_pattern):
        self.id = str(id)
        self.filename = "{}.txt".format(self.id)
        self.local_path = os.path.join(cache_dir, self.filename)
        self.query_path = query_pattern.format(id)

    def server_response(self):
        return requests.head(self.query_path).status_code

    def is_cached(self):
        return os.path.isfile(self.local_path)

    def cache_locally(self):
        response = requests.get(self.query_path)
        if response.status_code == 200:
            with open(self.local_path, 'w') as handle:
                handle.write(response.text)

