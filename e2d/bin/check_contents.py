#!/usr/bin/env python3

import os
import sys

ROOT = sys.argv[1]
excludes  = ['dublin_core.xml', 'contents']
to_check  = [dir for dir in os.listdir(ROOT) if not dir.startswith('.')]
total = len(to_check)
errors = 0
successes = 0

print(f'Checking {total} dirs for contents vs. file mismatches...')
for dir in sorted(to_check):
    obj_dir = os.path.join(ROOT, dir)
    obj_list = os.listdir(obj_dir)
    files = [obj for obj in obj_list if obj not in excludes]
    
    if files:
        with open(os.path.join(obj_dir, 'contents')) as handle:
            data = [line.strip('\n') for line in handle.readlines()]

        for listing in data:
            if listing not in files:
                print(f"{dir}: {listing} not in {files}")
                errors += 1
            else:
                successes += 1
                print(f'Analyzing ... {successes} OK', end='\r')

print(f'\nCheck complete! {successes}/{total} verified. {errors} errors.')