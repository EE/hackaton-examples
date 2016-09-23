import sirs
from settings import HOST

import json
import os

DATA_DIRECTORY = 'data'

api = sirs.API(HOST)
os.makedirs(DATA_DIRECTORY, exist_ok=True)

print('downloading data from %s' % api.url)
for name, table in api.tables.items():
    path = os.path.join(DATA_DIRECTORY, name + '.json')
    print(
        'writing contents of table %s (at %s) to file %s ... ' % (name, table.url, path),
        end='', flush=True
    )
    data = table.get()
    print('writing %d records ... ' % len(data), end='', flush=True)
    with open(path, 'w') as data_file:
        data_file.write(json.dumps(data, indent=2, sort_keys=True))
    print('done')
