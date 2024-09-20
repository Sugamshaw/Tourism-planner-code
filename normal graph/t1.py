import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import community
import numpy as np

filename = "travel.csv"

# Correcting column names
source = "Source"
destination = "Destination"
time = "Time(hrs)"

# Reading CSV file properly
df = pd.read_csv(filename)

# Removing unnecessary spaces in city names
df['Source'] = df['Source'].str.strip()
df['Destination'] = df['Destination'].str.strip()

G = nx.DiGraph()
G = nx.from_pandas_edgelist(df, source=source, target=destination, edge_attr=time)

# Detect communities (clusters) using Girvan-Newman algorithm
communities_generator = community.girvan_newman(G)
top_level_communities = next(communities_generator)
next_level_communities = next(communities_generator)
communities = sorted(map(sorted, next_level_communities))

# Create node colors based on community
node_colors = {}
for i, comm in enumerate(communities):
    for city in comm:
        node_colors[city] = f"C{i}"

# Separate the graph into subgraphs based on communities
subgraphs = [G.subgraph(comm) for comm in communities]

# Compute layouts for each subgraph
layouts = [nx.spring_layout(subgraph, weight='Time(hrs)', iterations=50, scale=10) for subgraph in subgraphs]

# Determine the number of clusters and total number of nodes
num_clusters = len(communities)
num_nodes = sum(len(subgraph.nodes) for subgraph in subgraphs)

# Set the space between clusters
space_between_clusters =5

# Calculate the total width of the layout
total_width = space_between_clusters * (num_clusters - 1)

# Initialize the x-coordinate for the clusters
x_coordinates = np.linspace(-total_width / 2, total_width / 2, num_clusters)

# Combine layouts into a single layout with proper spacing between clusters
combined_layout = {}
for i, comm in enumerate(communities):
    x_offset = x_coordinates[i]
    for j, city in enumerate(comm):
        layout_x, layout_y = layouts[i][city]
        combined_layout[city] = np.array([layout_x + x_offset, layout_y])

# Draw nodes with community-based colors and custom layout
nx.draw(
    G,
    combined_layout,
    with_labels=True,
    node_size=100,
    font_size=10,
    font_weight="bold",
    node_color=[node_colors[node] for node in G.nodes()],
    font_color="black"
)

# Draw edges with labels
edge_labels = nx.get_edge_attributes(G, time)
nx.draw_networkx_edge_labels(
    G,
    combined_layout,
    edge_labels=edge_labels,
    font_size=8,
    font_color="navy"
)

plt.show()
