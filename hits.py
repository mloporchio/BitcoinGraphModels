import networkx as nx
import sys
import time

EDGE_LIST_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

start = time.time_ns()

G = nx.read_edgelist(EDGE_LIST_FILE, create_using=nx.DiGraph, nodetype=int, delimiter="\t")

num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()

hubs, authorities = nx.hits(G, max_iter=100, normalized=True)

with open(OUTPUT_FILE, 'w') as f:
    f.write("node_id\thub_score\tauthority_score\n")
    for node in G.nodes():
        f.write(f"{node}\t{hubs[node]}\t{authorities[node]}\n")

end = time.time_ns()
elapsed = end-start

print(f'{num_nodes}\t{num_edges}\t{elapsed}')