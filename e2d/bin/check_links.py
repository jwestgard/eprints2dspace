#!/usr/bin/env python3

import os
import requests
import sys
sys.path.append(os.path.join(sys.path[0], '..'))
from load import DublinCoreXML


def update_link(url):
    '''Follow 301/308 redirects and return new location, else return original'''
    try:
        response = requests.head(url, timeout=30)
        status = response.status_code
        print(f'  => {status} {url}')
        if status in [301, 308]:
            response = requests.get(response.url, timeout=30)
            url = response.url
            print(f'  => Found a redirect to {url}')
        return url
    except:
        return url


def main(root):
    '''Walk a directory tree and update external links found in the 
        object's metadata file'''
    for d in [d for d in os.listdir(root) if not d.startswith('.')]:
        print(f'\n{d.upper()}')
        dc = DublinCoreXML.from_existing(os.path.join(root, d))
        print('  => checking links')
        exlinks = dc.all_exlinks()
        if len(exlinks) == 0:
            print('  => no external links')
        else:
            for node in exlinks:
                original = node.text
                new = update_link(original)
                if new != original:
                    node.text = new
                    dc.write()
                    print('  => writing new XML')
                else:
                    print('  => keeping same URL')


if __name__ == '__main__':
    main(sys.argv[1])
