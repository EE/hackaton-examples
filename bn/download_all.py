import bn
from settings import HOST

import json
import os
import argparse


parser = argparse.ArgumentParser(description='Download data from BN API.')
parser.add_argument('--host', '-H', default=HOST)
parser.add_argument('--since-id', type=int, default=0)
parser.add_argument('--data-dir', default=os.path.join('data', 'bibs'))
parser.add_argument('--records-per-file', type=int, default=1000)

args = parser.parse_args()

api = bn.Endpoint(args.host)
os.makedirs(args.data_dir, exist_ok=True)

print('downloading data from %s into %s' % (api.url, args.data_dir))

since_id = args.since_id
while True:
    path = os.path.join(args.data_dir, '%012d.json' % since_id)
    print('since %d ... ' % since_id, end='', flush=True)
    data = api.get(since_id=since_id, limit=args.records_per_file)
    with open(path, 'w') as data_file:
        data_file.write(json.dumps(data, indent=2, sort_keys=True))
    max_id = max([e['id'] for e in data])
    print('done %d records, max id: %d' % (len(data), max_id))

    if len(data) < args.records_per_file:
        break
    since_id = max_id + 1

