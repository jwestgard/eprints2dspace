#!/usr/bin/env python3

import logging
import os
import sys
sys.path.append(os.path.join(sys.path[0], '..'))
from load import DublinCoreXML

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def create_paths(root, objlist):
    with open(objlist) as handle:
        objs = [f'item_{int(id):04d}' for id in handle.readlines()]
        return [os.path.join(root, obj) for obj in objs]

def strip_link(dcfile):
    logging.info(f'Stripping external link from {dcfile}')
    dc = DublinCoreXML.from_existing(dcfile)    
    for node in dc.all_exlinks():
        node.getparent().remove(node)
    dc.write()

def main(root, list):
    for item in create_paths(root, list):
        strip_link(item)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
