#!/usr/bin/env python3

import csv
from lxml import etree as etree
import os
import sys
from e2d.load import DublinCoreXML


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
            dc = DublinCoreXML.from_existing(os.path.join(root, obj))
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

