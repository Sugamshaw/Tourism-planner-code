# 26. Tourism Planner
# Given a set of cities of a state. Provide the optimal tour guidance to the visitors.
# The trip preferences include the distance between the cities and the time taken to
# complete the city, its rating needs to be considered while providing a plan. There may
# be multiple modes available to reach the same destination. You need to find the optimal
# plan which contains the least travel time, least cost, least money, but covering highly
# rated places. This is multiple objective optimization.
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Define the colors
node_color = "blue"
node_font_color = "black"
edge_color = "skyblue"
orange_nodes = [
    "Bhubaneswar Railway Station(Bhubaneswar)",
    "Cuttack Junction Railway Station(Cuttack)",
    "Howrah Junction Railway Station(Kolkata)",
    "Visakhapatnam Railway Station(Visakhapatnam)",
]  # List of nodes to be colored orange
orange_edge_nodes = [
    (
        "Bhubaneswar Railway Station(Bhubaneswar)",
        "Cuttack Junction Railway Station(Cuttack)",
    ),
    (
        "Cuttack Junction Railway Station(Cuttack)",
        "Howrah Junction Railway Station(Kolkata)",
    ),
    (
        "Howrah Junction Railway Station(Kolkata)",
        "Visakhapatnam Railway Station(Visakhapatnam)",
    ),
]  # List of edges to be colored orange
orange_edge_color = "orange"  # Color for the specified edges
edge_font_color = "navy"

# Read the data and create the graph
filename = "travel.csv"
source = "Source"
destination = "Destination"
time = "Time(hrs)"
df = pd.read_csv(filename)
G2 = nx.from_pandas_edgelist(df, source=source, target=destination, edge_attr=time)

# Define the positions for the nodes
pos = nx.spring_layout(G2, k=1)

# Draw the graph
nx.draw(
    G2,
    pos,
    with_labels=True,
    node_color=[
        node_color if node not in orange_nodes else "orange" for node in G2.nodes()
    ],
    node_size=[100 if node not in orange_nodes else 300 for node in G2.nodes()],
    font_size=10,
    labels={node: node for node in G2.nodes()},
)

df_paths = []
with open("paths.csv") as f:
    for line in f:
        df_paths.append(pd.DataFrame({"path": [line.strip()]}))

path_colors = ["red", "yellow", "green"]
initial_width = 1
nx.draw_networkx_edges(
    G2,
    pos,
    edgelist=orange_edge_nodes,
    edge_color=orange_edge_color,
    width=1.5,  # You can adjust the width as needed
    arrows=True,
)
# Create separate DiGraph objects for each path and draw edges
for i, df in enumerate(df_paths):
    g = nx.DiGraph()
    for _, row in df.iterrows():
        path = row["path"].split("->")
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
        width=2,  # Decrease width for each subsequent path
    )
# Change color of edges

nx.draw_networkx_edges(G2, pos, edge_color=edge_color, width=0.5, arrows=True)

# Change color of specific edges


# Change color of edge labels
# edge_labels = nx.get_edge_attributes(G2, time)
# nx.draw_networkx_edge_labels(
#     G2, pos, edge_labels=edge_labels, font_size=8, font_color=edge_font_color
# )

plt.show()
