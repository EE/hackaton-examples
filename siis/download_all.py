import siis
from settings import HOST

import argparse
import os
import json


parser = argparse.ArgumentParser(description='Download data from SIIS API.')
parser.add_argument('--host', default=HOST)
parser.add_argument('--since-id', type=int, default=0)
parser.add_argument('--data-dir', default='data')
parser.add_argument('--records-per-file', type=int, default=1000)
parser.add_argument('--year', type=int, default=None)
parser.add_argument('--table', default=None)

args = parser.parse_args()

api = siis.API(args.host)

def download_table(year, table):
    directory_path = os.path.join(args.data_dir, str(year), table)
    os.makedirs(directory_path, exist_ok=True)
    print('downloading year %d, table %s into %s' % (year, table, directory_path))

    since_id = args.since_id
    while True:
        path = os.path.join(directory_path, '%012d.json' % since_id)
        print('since %d ... ' % since_id, end='', flush=True)
        data = api.years[year].tables[table].get(offset=since_id, limit=args.records_per_file)
        with open(path, 'w') as data_file:
            data_file.write(json.dumps(data, indent=2, sort_keys=True))
        max_id = max([e['id'] for e in data])
        print('done %d records, max id: %d' % (len(data), max_id))

        if len(data) < args.records_per_file:
            break
        since_id = max_id + 1

def download_year(year):
    print('downloading year %d' % year)
    if args.table == None:
        for table in api.years[year].tables:
            download_table(year, table)
    else:
        download_table(year, args.table)

def download():
    print('downloading data from %s' % api.url)
    if args.year == None:
        for year in api.years:
            download_year(year)
    else:
        download_year(args.year)

download()
