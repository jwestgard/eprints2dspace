#!/usr/bin/env python3

'''Move objects listed in text file by id from SAF to cellar'''

import os
import shutil
import sys

ROOTDIR  = sys.argv[1]
CELLAR   = sys.argv[2]
SKIPFILE = sys.argv[3]

def main():
    objects = os.listdir(ROOTDIR)
    with open(SKIPFILE) as handle:
        skips = [f'item_{int(id):04d}' for id in handle.readlines()]

    for skip in skips:
        origin = os.path.join(ROOTDIR, skip)
        shutil.move(origin, CELLAR)

if __name__ == '__main__':
    main()