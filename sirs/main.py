import sirs
from settings import HOST

api = sirs.API(HOST)
nodes = api.tables['infrastructure_nodes']

assert(nodes.get_raw()['data'] == nodes.get(limit=25))
