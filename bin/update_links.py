#!/usr/bin/env python3

import os
import requests
import sys
from e2d import load

def main(root):

    '''Check external links and update'''

    for d in os.listdir(root):
        if not d.startswith('.'):
            print(f'### {d} ###')
            dc = load.DublinCoreXML(os.path.join(ROOT, d))
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
            print('  => writing XML')
            dc.write()



if __name__ == '__main__':
    '''Supply root directory of the SAF package to be updated as an argument'''
    main(sys.argv[1])