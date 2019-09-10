import networkx as nx
import pandas as pd

G = nx.read_edgelist('edges.edgelist', 
                     create_using=nx.MultiDiGraph,
                     nodetype=int,
                     data=(('weight', int), ('relation', str)))

df = pd.read_csv('nodes.csv', index_col=0)
for row in df.itertuples():
    G.node[row.Index]['role'] = row.Role
    G.node[row.Index]['label'] = row.Label

# Make a small report.
print("Nodes: \n", G.nodes(data=True), sep='')
print("-" * 20, "\nEdges: \n", G.edges(data=True), sep='')
