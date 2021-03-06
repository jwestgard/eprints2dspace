from lxml import etree
import os
import requests
from urllib.parse import unquote as unquote


class DublinCoreXML():

    '''Class for the dc XML file in each SAF resource'''
    
    @classmethod
    def from_metadata(cls, dcfile, metadata):
        root = etree.Element("dublin_core")
        for key, value in metadata.items():
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
        return cls(dcfile, etree.ElementTree(root))

    @classmethod
    def from_existing(cls, dcfile):
        tree = etree.parse(dcfile, etree.XMLParser(remove_blank_text=True))
        return cls(path, tree)

    def __init__(self, dcfile, tree):
        self.file = dcfile
        self.tree = tree
        self.root = self.tree.getroot()

    def add_subject(self, keyword):
        child = etree.Element("dcvalue", element="subject")
        child.text = keyword
        self.root.append(child)

    def all_exlinks(self):
        return self.tree.xpath(
            '/dublin_core/dcvalue[@element="description" and @qualifier="uri"]'
            )

    def all_subjects(self):
        subjects = self.root.findall(".//dcvalue[@element='subject']")
        return [subject.text for subject in subjects]

    def write(self):
        with open(self.file, 'wb') as handle:
            handle.write(etree.tostring(self.tree, xml_declaration=True,
                                        encoding="UTF-8", pretty_print=True))


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
        DublinCoreXML.from_metadata(self.dc_file, self.metadata).write()

    def write_contents_file(self):
        '''Write constituent files, one per line, to the contents file'''
        with open(self.cont_file, 'w') as handle:
            handle.write("\n".join(
                [unquote(os.path.basename(f)) for f in self.binaries])
                )

