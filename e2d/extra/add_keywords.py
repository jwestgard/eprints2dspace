#!/usr/bin/env python3

import csv
from lxml import etree as etree
import os
import sys

class DublinCoreXML():
    def __init__(self, path):
        self.file = os.path.join(path, 'dublin_core.xml')
        self.tree = etree.parse(self.file, etree.XMLParser(remove_blank_text=True))
        self.root = self.tree.getroot()

    def add_subject(self, keyword):
        child = etree.Element("dcvalue", element="subject")
        child.text = keyword
        self.root.append(child)

    def write(self):
        with open(self.file, 'wb') as handle:
            handle.write(etree.tostring(self.tree, xml_declaration=True,
                                        encoding="UTF-8", pretty_print=True))

def main(kwfile):
    with open(kwfile) as handle:
        for row in csv.DictReader(handle):
            itemdir = f'item_{int(row["eprintid"]):04d}'
            print(f'Processing {itemdir}:')
            keywords = [kw.strip() for kw in row['keywords'].split(';') \
                            if kw.strip() is not '']
            if len(keywords) > 0:
                try:
                    print(f'  => opening dc file ... ')
                    dc = DublinCoreXML(os.path.join(ROOT, itemdir))
                    for kw in keywords:
                        dc.add_subject(kw)
                        print(f'  => adding {kw} ... ')
                    dc.write()
                    print(f'  => writing dc file. ')
                except OSError:
                    print(f'  => could not write to file!')
            else:
                print(f'  => no keywords to add.')


if __name__ == '__main__':
    
    #ROOT = sys.argv[1]
    #kwfile = sys.argv[2]
    main(kwfile)

