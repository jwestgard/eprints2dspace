#!/usr/bin/env python3

import csv
from importlib import import_module
import logging
import os
import requests
import shutil
from urllib.parse import unquote as unquote

from .batch import *
from .transform import *
from .mapping import *


def create_lookup(path):

    '''Create a lookup table for adding keywords to the metadata'''
    
    result = dict()
    with open(path) as handle:
        for row in csv.DictReader(handle):
            key = row['eprintid']
            itemkeywords = []
            keywords = [kw.strip() for kw in row['keywords'].split(';')]
            for kw in keywords:
                if kw is not '':
                    itemkeywords.append(kw)
            if itemkeywords:
                result[key] = itemkeywords
    return result


def update_redirect(url):

    '''Follow 301/308 redirects and return new location, else return original'''

    status = None
    try:
        response = requests.head(url, timeout=20)
        status = response.status_code
        if status in [301, 307]:
            response = requests.get(response.url, timeout=20)
            url = response.url
        return (status, url)
    except:
        return (status, url)


def main():

    '''(1) Start from list of eprint ids'''

    print_header()
    args = parse_args()
    batch = Batch(args.config, args.mapfile)
    keyword_lookup = create_lookup(batch.keywords)

    logfile = os.path.join(
        batch.log_dir, dt.now().strftime("%Y%m%d%H%M%S") + '.txt'
        )
    logging.basicConfig(
        filename=logfile, level=logging.INFO
        )
    logging.info(
        'Created batch with {} items'.format(len(batch.contents))
        )
    logging.info(
        'Created source server object at {}'.format(batch.source.host_name)
        )
    logging.info(
        'Caching extracted data at {}'.format(batch.local_cache)
        )
    logging.info(
        'Created destination package at {}'.format(batch.destination.root)
        )


    for n, res in enumerate([i for i in batch.contents], 1):

        '''Skip excluded and complete resources'''
        if res.status == 'complete' or res.action == 'exclude':
            continue

        '''(2) Pull metadata or read files from data dir'''

        eprint = EprintsResource(res.id, batch.local_cache, batch.source.query_pattern)
        print(f'\n({n}) EPRINT {res.id}', file=sys.stdout)
        print(f'  -> Attempting to create item {res.id}', file=sys.stdout)
        if eprint.is_cached():
            print(f'  -> Found in cache', file=sys.stdout)
            res.dcfile = eprint.local_path
        else:
            logging.info('Querying server')
            status = eprint.server_response()
            if status == 200:
                eprint.cache_locally()
                res.dcfile = eprint.local_path
                print(f'  -> Cached to {res.dcfile}', file=sys.stdout)
            else:
                print(f'  -> Could not reach {eprint.id}, response {status}', 
                                                                file=sys.stdout)
                res.action = 'exclude'
                continue
        eprint.fetch_binaries()

        '''(3) Transform metadata'''

        try:
            transformed_metadata = transform(eprint.parse_source())
            title = transformed_metadata['dc.title'][0]
            print(f'  -> Successfully transformed "{title}"')
        except:
            print(f'  -> Could not transform metadata for {eprint.id}')
            continue

        '''(4) Strip External Links from Flagged items'''

        if 'strip_links' in res.special:
            print(f'  -> Removing external links from item {eprint.id}')
            transformed_metadata['dc.description.uri'] = []

        '''(5) Update External Links'''

        external_links = transformed_metadata['dc.description.uri']
        if external_links:
            result = []
            responses = []
            print(f'  -> Checking external links')
            for url in external_links:
                status, updated = update_redirect(url)
                if updated != url:
                    print(f'    * Updated {status}: {updated}')
                    result.append(updated)
                else:
                    print(f'    * Response: {status}')
                    result.append(url)
                responses.append(str(status))
            transformed_metadata['dc.description.uri'] = result
            res.link = ' || '.join(external_links)
            res.response = ' || '.join(responses)
            res.newlink = ' || '.join(result)

        '''(5) Add Keywords'''

        subjects = transformed_metadata['dc.subject']
        keywords = keyword_lookup.get(str(eprint.id))
        if not keywords:
            print(f'  -> no keywords to add')
            res.keywords = None
        else:
            print(f'  -> adding {keywords}')
            additions = [kw for kw in keywords if kw not in subjects]
            subjects.extend(additions)
            res.keywords = ' || '.join(additions)


        '''(6) Write SAF'''
        
        try:
            sr = SafResource(
                eprint.id, transformed_metadata, batch.destination
                )
            print(f'  -> Creating SAF resource at {sr.path}')
            sr.write_dcxml_file()
            print(f'     * Writing DC XML {sr.dc_file}')
            sr.write_contents_file()
            print(f'     * Writing contents file {sr.cont_file}')
            attachments = sr.binaries
            res.binaries = len(attachments)
            if res.binaries:
                print(f'     * Moving binaries:')
                for n, binary in enumerate(attachments, 1):
                    filename = unquote(os.path.basename(binary))
                    path = os.path.join(eprint.local_dir, filename)
                    if os.path.isfile(path):
                        print(f'       ({n}) Moving {filename} to {sr.path}')
                        shutil.copy(path, sr.path)
        except:
            print(f'  FAILED TO CREATE SAF RESOURCE')
            continue

        '''(7) Move Aside Excluded Items'''
        if 'move_aside' in res.special:
            shutil.move(sr.path, os.path.join(batch.cellar, sr.dir))
        
        '''(8) Set item status to complete'''
        res.status = 'complete'

    print('\nBatch complete!', file=sys.stdout)

    '''(6) Summarize batch processing results''' 
    
    batch.mapfile.write(batch.contents)


if __name__ == "__main__":
    main()
