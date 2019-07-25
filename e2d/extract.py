import os
import requests
from urllib.parse import unquote as unquote


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
        self.local_dir = os.path.join(cache_dir, self.id)
        os.makedirs(self.local_dir, exist_ok=True)
        self.local_path = os.path.join(self.local_dir, self.filename)
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

    def parse_source(self):
        result = {}
        with open(self.local_path, 'r') as handle:
            lines = [line.strip() for line in handle.readlines()]
        for line in lines:
            if line is not '':
                key, value = tuple(line.split(': ', 1))
                if not key in result:
                    result[key] = [value.strip()]
                else:
                    result[key].append(value.strip())
        return result

    def fetch_binaries(self):
        '''Download binaries to local cache'''
        fields = self.parse_source()
        for url in [b for b in fields['identifier'] if b.startswith(
                    'http://health-equity.lib.umd.edu')]:
            decoded_filename = unquote(os.path.basename(url))
            binary_path = os.path.join(self.local_dir, decoded_filename)
            if not os.path.isfile(binary_path):
                response = requests.get(url)
                with open(binary_path, 'wb') as handle:  
                    handle.write(response.content)
