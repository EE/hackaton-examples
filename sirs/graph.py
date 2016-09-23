import json
import networkx
from collections import Counter

# build graph
graph = networkx.Graph()
with open('data/infrastructure.json') as edges_file:
    graph.add_edges_from(
        (entry['node_A_id'], entry['node_B_id'], entry)
        for entry in json.load(edges_file)
    )

print('nodes:', len(graph.nodes()), 'edges:', len(graph.edges()))
print('connected components count: ', len(list(networkx.connected_components(graph))))
print('connected components sizes: ', Counter(map(len, networkx.connected_components(graph))))
print('nodes degree values:', Counter(networkx.degree(graph).values()))

