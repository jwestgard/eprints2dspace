#!/usr/bin/env python3

from lxml import etree as etree
import os
import requests
import sys

ROOT  = sys.argv[1]
XPATH = '/dublin_core/dcvalue[@element="description" and @qualifier="uri"]'

class DublinCoreXML():
    def __init__(self, path):
        self.file = os.path.join(path, 'dublin_core.xml')
        self.tree = etree.parse(self.file)
        self.exlinks = self.tree.xpath(XPATH)

    def write(self):
        with open(self.file, 'wb') as handle:
            handle.write(
                etree.tostring(self.tree, xml_declaration=True, encoding="UTF-8")
                )

def main():
    for d in os.listdir(ROOT):
        if not d.startswith('.'):
            print(f'### {d} ###')
            dc = DublinCoreXML(os.path.join(ROOT, d))
            print('  => checking links')
            for node in self.exlinks:
                link = node.text
                try:
                    response = requests.get(link, timeout=10)
                    print(f'  => {link} ... ')
                    status = response.status_code
                    node.text = response.url
                    print(f'  => {node.text} ... ')
                except:
                    print('  => error response')
            dc.write()
            print('  => writing XML')

if __name__ == '__main__':
    main()