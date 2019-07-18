#!/usr/bin/env python3

import os
import requests
import sys
sys.path.append(os.path.join(sys.path[0], '..'))
from load import DublinCoreXML

def main(root):

    '''Check external links and update'''

    for d in os.listdir(root):
        updated = False
        if not d.startswith('.'):
            print(f'### {d} ###')
            dc = DublinCoreXML.from_existing(os.path.join(root, d))
            print('  => checking links')
            for node in dc.all_exlinks():
                link = node.text
                try:
                    response = requests.head(link, timeout=10)
                    status = response.status_code
                    print(f'  => {link} ... {status}')
                    if status in [301, 308]:
                        response = requests.get(link, timeout=10)
                        if response.status_code == 200:
                            node.text = response.url
                            print(f'  => updating to {node.text}')
                            updated = True
                    else:
                        continue
                except:
                    print('  => error response')
        if updated:
            print('  => writing XML')
            dc.write()


if __name__ == '__main__':
    '''Supply root directory of the SAF package to be updated as an argument'''
    main(sys.argv[1])
