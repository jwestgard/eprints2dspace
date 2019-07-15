#!/usr/bin/env python3

'''Move objects listed in text file by id from SAF to cellar'''

import os
import shutil
import sys

def main(origdir, destdir, idfile):
    with open(idfile) as handle:
        for id in handle.readlines():
            try:
                id = id.strip()
                path = os.path.join(origdir, f'item_{int(id):04d}')
                print(path)
                shutil.move(path, destdir)
                print(f'moving... {id}')
            except (FileNotFoundError, shutil.Error, ValueError):
                print(f'skipping... {id}')
                continue

if __name__ == '__main__':
    main(*sys.argv[1:])
