import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Load the data from travel1.csv into G2
df_travel = pd.read_csv("travel2.csv")
G2 = nx.from_pandas_edgelist(
    df_travel, source="source", target="destination", edge_attr="travel_time"
)

# Layout for positioning the nodes
pos = nx.spring_layout(G2, k=2)

# Draw the main graph G2 with blue color
nx.draw(
    G2,
    pos,
    with_labels=True,
    node_color="skyblue",
    node_size=500,
    font_size=12,
    font_weight="bold",
)

# Load the data from paths.csv into g3
df_paths = pd.read_csv("paths.csv")

# Create a directed graph for g3
g3 = nx.DiGraph()

# Add edges to g3 from the DataFrame
for _, row in df_paths.iterrows():
    path = row["path"].split("->")
    for i in range(len(path) - 1):
        g3.add_edge(path[i], path[i + 1])

# Draw edges of g3 with arrows to indicate direction
nx.draw_networkx_edges(
    g3, pos, arrows=True, arrowstyle="->", arrowsize=50, edge_color="red", width=4
)

# Highlight nodes of g3 in red color
nx.draw_networkx_nodes(g3, pos, node_color="red", node_size=500)

# Add edge labels for G2
edge_labels = nx.get_edge_attributes(G2, "travel_time")
nx.draw_networkx_edge_labels(G2, pos, edge_labels=edge_labels, font_size=10)

plt.show()
