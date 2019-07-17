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

    def all_subjects(self):
        subjects = self.root.findall(".//dcvalue[@element='subject']")
        return [subject.text for subject in subjects]

    def write(self):
        with open(self.file, 'wb') as handle:
            handle.write(etree.tostring(self.tree, xml_declaration=True,
                                        encoding="UTF-8", pretty_print=True))


def create_lookup(path):
    result = dict()
    with open(path) as handle:
        for row in csv.DictReader(handle):
            itemdir = f'item_{int(row["eprintid"]):04d}'
            itemkeywords = []
            keywords = [kw.strip() for kw in row['keywords'].split(';')]
            for kw in keywords:
                if kw is not '':
                    itemkeywords.append(kw)
            if itemkeywords:
                result[itemdir] = itemkeywords
    return result


def main(root, kwfile):
    lookup = create_lookup(kwfile)
    for obj in os.listdir(root):
        try:
            print(f'\nOpening dc file for {obj}:')
            dc = DublinCoreXML(os.path.join(root, obj))
            existing = dc.all_subjects()
            additional = lookup.get(obj, None)
            if not additional:
                print(f'  => no keywords to add.')
            else:
                for kw in additional:
                    if kw not in existing:
                        print(f'  => adding {kw} ... ')
                        dc.add_subject(kw)
                print(f'  => writing dc file. ')
                dc.write()
        except OSError:
            print(f'  => could not write to file!')


if __name__ == '__main__':

    '''pass (1) SAF batch directory 
        and (2) path to CSV (IDs and keywords)
        as arguments'''

    main(sys.argv[1], sys.argv[2])

