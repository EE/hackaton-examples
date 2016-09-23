import siis
from settings import HOST

import gmplot
from pprint import pprint

api = siis.API(HOST)
#pprint(api.schema())

# get users
users = api.years[2015].tables['users_entity_view'].get(filter_string='name:~.*uniwersytet.*')
query = 'usersEntityId:[' + ','.join([str(user['id']) for user in users]) + ']'

# get nodes
nodes = api.years[2015].tables['infrastructure_node_view'].get(filter_string=query)
endpoints = api.years[2015].tables['networkendpoint_view'].get(filter_string=query)

# plot on map
gmap = gmplot.GoogleMapPlotter(52.2556707, 21.0424542, 11.5) # around Warsaw
gmap.coloricon = 'https://raw.githubusercontent.com/vgm64/gmplot/master/gmplot/markers/%s.png'

def safe_marker(lat, lon, title, **kwargs):
    if node['latitude']== None or node['longitude'] == None:
        return
    gmap.marker(lat, lon, title=title.replace('"', '\\"'), **kwargs)

for node in nodes:
    safe_marker(node['latitude'], node['longitude'], color='red', title=(str(node['usersEntityIdName']) + ' | ' + str(node['name'])))
for node in endpoints:
    safe_marker(node['latitude'], node['longitude'], color='green', title=(str(node['usersEntityIdName']) + ' | ' + str(node['nodeIdName'])))
gmap.draw('nodes.html')
