import operator

import networkx as nx
import matplotlib.pyplot as plt

G = nx.karate_club_graph()

node_colors = ['orange' if props['club'] == 'Officer' else 'blue' 
               for _, props in G.nodes(data=True)]
node_sizes = [180 * G.degree(u) for u in G]

plt.figure(figsize=(10, 10))
pos = nx.kamada_kawai_layout(G)
nx.draw_networkx(G, pos, 
                 node_size=node_sizes, 
                 node_color=node_colors, alpha=0.8, 
                 with_labels=False, 
                 edge_color='.6')

# Calculating the absolute edge betweenness centrality.
main_conns = nx.edge_betweenness_centrality(G, normalized=True)
main_conns = sorted(main_conns.items(), key=operator.itemgetter(1), reverse=True)[:5]
main_conns = tuple(map(operator.itemgetter(0), main_conns))
nx.draw_networkx_edges(G, pos, edgelist=main_conns, edge_color='green', alpha=0.5, width=6)

# Estimating the edge betweenness centrality by sampling 40% of nodes.
NUM_SAMPLES = int(0.4 * len(G))

est_main_conns = nx.edge_betweenness_centrality(G, k=NUM_SAMPLES, normalized=True, seed=10)
est_main_conns = sorted(est_main_conns.items(), key=operator.itemgetter(1), reverse=True)[:5]
est_main_conns = tuple(map(operator.itemgetter(0), est_main_conns))
nx.draw_networkx_edges(G, pos, edgelist=est_main_conns,
                       edge_color='red', alpha=0.9, width=6, style='dashed')

nx.draw_networkx_labels(G, pos, 
                        labels={0: G.node[0]['club'], 33: G.node[33]['club']}, 
                        font_size=15, font_color='white')

candidate_edges = ((8, 15), (30, 21), (29, 28), (1, 6))
nx.draw_networkx_edges(G, pos, edgelist=candidate_edges, 
                       edge_color='blue', alpha=0.5, width=2, style='dashed')
nx.draw_networkx_labels(G, pos, 
                        labels={u: u for t in candidate_edges for u in t}, 
                        font_size=13, font_weight='bold', font_color='yellow')

plt.axis('off')
plt.tight_layout();
plt.show()
