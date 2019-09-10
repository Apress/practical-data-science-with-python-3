import networkx as nx

G = nx.Graph()

G.add_node(0, role='quality-attribute', label='Maintainability')
G.add_node(1, role='quality-attribute', label='Reliability')
G.add_node(2, role='quality-attribute', label='Performance')

G.add_edge(0, 1, sign='+')
G.add_edge(0, 2, sign='-')
G.add_edge(1, 2, sign='-')
