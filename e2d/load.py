from lxml import etree
import os
import requests


class SafPackage():

    '''Class for building Dspace Simple Archive Format packages'''

    def __init__(self, root, max_width):
        self.root      = root
        self.max_width = max_width
        os.makedirs(self.root, exist_ok=True)


class SafResource():

    '''Class for individual resources arranged in a SAF package'''

    def __init__(self, id, metadata, package):
        self.dir        = f'item_{int(id):0{package.max_width}d}'
        self.path       = os.path.join(package.root, self.dir)
        self.cont_file  = os.path.join(self.path, 'contents')
        self.dc_file    = os.path.join(self.path, 'dublin_core.xml')
        self.binaries   = metadata.pop('binaries')
        self.metadata   = metadata
        os.makedirs(self.path, exist_ok=True)

    def write_dcxml_file(self):
        '''Generate XML from eprint metadata & write to dublin_core.xml'''
        root = etree.Element("dublin_core")
        for key, value in self.metadata.items():
            schema, element = key.split('.', 1)
            if len(element.split('.')) == 2:
                element, qualifier = element.split('.')
            else:
                qualifier = None
            if value is not None and value != '':
                for instance in value:
                    child = etree.Element("dcvalue", element=element)
                    if qualifier is not None:
                        child.set('qualifier', qualifier)
                    child.text = instance
                    root.append(child)
        with open(self.dc_file, 'wb') as handle:
            et = etree.ElementTree(root)
            et.write(handle, xml_declaration=True, encoding='UTF-8',
                        pretty_print=True)

    def write_contents_file(self):
        '''Write constituent files, one per line, to the contents file'''
        with open(self.cont_file, 'w') as handle:
            handle.write("\n".join(
                [os.path.basename(f) for f in self.binaries])
                )

    def fetch_binaries(self):
        '''Download attached binaries for inclusion in import package'''
        for url in self.binaries:
            local_path = os.path.join(self.path, os.path.basename(url))
            if not os.path.isfile(local_path):
                response = requests.get(url)
                with open(local_path, 'wb') as handle:  
                    handle.write(response.content)
            logging.info('  • Download: {0} -> {1}'.format(url, local_path))
