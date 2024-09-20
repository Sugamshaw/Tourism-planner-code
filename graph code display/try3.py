import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Load the data from travel1.csv into G2
df_travel = pd.read_csv("input1.csv")
G2 = nx.from_pandas_edgelist(
    df_travel, source="Source", target="Destination", edge_attr="Time(hrs)"
)

# Layout for positioning the nodes
pos = nx.spring_layout(G2, k=2)

# Draw the main graph G2 with blue color
nx.draw(
    G2,
    pos,
    with_labels=True,
    node_color="blue",
    node_size=100,
    font_size=10,
    font_weight="bold",
    labels={node: node for node in G2.nodes()},
)

# Load the data from paths.csv into separate DataFrames for each path
df_paths = []
with open("paths1.csv") as f:
    for line in f:
        df_paths.append(pd.DataFrame({"path": [line.strip()]}))

# Define colors and initial width for each path
path_colors = ["green", "yellow", "red"]
initial_width = 1

# Create separate DiGraph objects for each path and draw edges
for i, df in enumerate(df_paths):
    g = nx.DiGraph()
    for _, row in df.iterrows():
        path = row["path"].split(" -> ")
        for j in range(len(path) - 1):
            g.add_edge(path[j], path[j + 1])
    nx.draw_networkx_edges(
        g,
        pos,
        arrows=True,
        arrowstyle="->",
        arrowsize=50,
        edge_color=path_colors[
            i % len(path_colors) - 1
        ],  # Use modulo to cycle through colors
        width=initial_width + i,  # Decrease width for each subsequent path
    )

# Add edge labels for G2
edge_labels = nx.get_edge_attributes(G2, "Time(hrs)")
nx.draw_networkx_edge_labels(
    G2, pos, edge_labels=edge_labels, font_size=8, font_color="navy"
)

plt.show()
