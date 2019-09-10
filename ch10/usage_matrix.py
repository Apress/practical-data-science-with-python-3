import networkx as nx

G = nx.MultiDiGraph()

# Add all nodes with their role and label. You can immediately work with labels, but having
# short node identifiers keeps your code uncluttered.
G.add_node(0, role='use-case', label='Communicate')
G.add_node(1, role='use-case', label='Manage Dev.')
G.add_node(2, role='use-case', label='Exec. Data Analytics')
G.add_node(3, role='use-case', label='Use Bus. Int.')
G.add_node(4, role='use-case', label='Use Op. Int.')
G.add_node(5, role='use-case', label='Send/Receive Data')
G.add_node(6, role='resource', label='Network')
G.add_node(7, role='resource', label='Messaging')
G.add_node(8, role='resource', label='Database')
G.add_node(9, role='actor', label='Device')
G.add_node(10, role='actor', label='Application')
G.add_node(11, role='actor', label='User')

# Add edges for the 'impact' relationship.
G.add_edge(0, 6, weight=600, relation='impact') 
G.add_edge(0, 7, weight=600, relation='impact')
G.add_edge(1, 6, weight=15, relation='impact') 
G.add_edge(2, 7, weight=100, relation='impact') 
G.add_edge(2, 8, weight=900, relation='impact') 
G.add_edge(3, 8, weight=800, relation='impact') 
G.add_edge(4, 8, weight=960, relation='impact')

# Add edges for the 'include' relationship.
G.add_edge(0, 5, relation='include') 
G.add_edge(1, 5, relation='include') 
G.add_edge(2, 5, relation='include') 

# Add edges for the 'extend' relationship.
G.add_edge(3, 2, relation='extend') 
G.add_edge(4, 2, relation='extend') 

# Add edges for the 'interact' relationship.
G.add_edge(9, 0, relation='interact') 
G.add_edge(0, 9, relation='interact') 
G.add_edge(10, 1, relation='interact') 
G.add_edge(1, 10, relation='interact') 
G.add_edge(10, 2, relation='interact') 
G.add_edge(2, 10, relation='interact') 
G.add_edge(11, 3, relation='interact') 
G.add_edge(3, 11, relation='interact') 
G.add_edge(11, 4, relation='interact') 
G.add_edge(4, 11, relation='interact') 

# Visualize the resulting graph using pydot and Graphviz.
from networkx.drawing.nx_pydot import write_dot

# By default NetworkX returns a deep copy of the source graph.
H = G.copy()

# Set some display properties for specific nodes and extract labels.
node_labels = {}
for node_id in H.nodes():
    node_labels[node_id] = H.node[node_id]['label']
    role = H.node[node_id]['role']
    if role == 'resource':
        H.node[node_id]['style'] = 'filled'
        H.node[node_id]['fillcolor'] = 'cyan'
        H.node[node_id]['shape'] = 'component'
        H.node[node_id]['fixedsize'] = 'shape'
    elif role == 'use-case':
        H.node[node_id]['shape'] = 'oval'
    elif role == 'actor':
        H.node[node_id]['style'] = 'rounded'
        H.node[node_id]['shape'] = 'box'
H.node[5]['style'] = 'dashed'

nx.relabel_nodes(H, node_labels, copy=False)
pos = nx.nx_pydot.graphviz_layout(H)
nx.draw(H, pos=pos, with_labels=True, font_weight='bold')
write_dot(H, 'usage_matrix.dot')