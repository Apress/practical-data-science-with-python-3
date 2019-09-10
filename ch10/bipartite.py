# Call usage_matrix.py before executing this script!
from networkx.algorithms import bipartite

# Add two new edges as described in the book.
G.add_edge(0, 10, relation='interact')
G.add_edge(10, 0, relation='interact')

# Select all nodes and edges from G that participate in 'interact' relation and
# create an undirected graph from them.
H = nx.Graph()
H.add_edges_from((u, v) for u, v, r in G.edges(data='relation') if r == 'interact')

# Attach a marker to specify which nodes belong to what group.
for node_id in H.nodes():
    H.node[node_id]['bipartite'] = G.node[node_id]['role'] == 'actor'

nx.relabel_nodes(H, {n: G.node[n]['label'].replace(' ', '\n') for n in H.nodes()}, copy=False)

print("Validating that H is bipartite: ", bipartite.is_bipartite(H))

# This is a graph projection operation. Here, we seek to find out what use cases
# have common actors. The weights represent the commonality factor.
W = bipartite.weighted_projected_graph(H, [n for n, r in H.nodes(data='bipartite') if r == 0])

# Draw the graph using matplotlib under the hood.
pos = nx.shell_layout(W)
nx.draw(W, pos=pos, with_labels=True, node_size=800, font_size=12)
nx.draw_networkx_edge_labels(W, pos=pos, 
                             edge_labels={(u, v): d['weight'] 
                                          for u, v, d in W.edges(data=True)})
