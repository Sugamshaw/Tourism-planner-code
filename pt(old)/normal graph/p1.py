# 26. Tourism Planner
# Given a set of cities of a state. Provide the optimal tour guidance to the visitors.
# The trip preferences include the distance between the cities and the time taken to
# complete the city, its rating needs to be considered while providing a plan. There may
# be multiple modes available to reach the same destination. You need to find the optimal
# plan which contains the least travel time, least cost, least money, but covering highly
# rated places. This is multiple objective optimization.


import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# source, destination, time, cost
filename = "travelf.csv"
source = "Source"
destination = "Destination"
time = "Time(hrs)"
# colour
node_color = "blue"
node_font_color = "black"

edge_color = "skyblue"
edge_font_color = "navy"


df = pd.read_csv(filename)


G2 = nx.DiGraph()

G2 = nx.from_pandas_edgelist(df, source=source, target=destination, edge_attr=time)

pos = nx.spring_layout(G2, k=5)

nx.draw(
    G2,
    pos,
    with_labels=True,
    node_color=node_color,
    node_size=100,
    font_size=10,
    font_weight="bold",
    labels={node: node for node in G2.nodes()},
)
# Change color of edges
nx.draw_networkx_edges(G2, pos, edge_color=edge_color, width=1.0, arrows=True)

# nx.draw_networkx_labels(G2, pos, font_color=node_font_color, font_weight="bold")

# Change color of edge labels
edge_labels = nx.get_edge_attributes(G2, time)
nx.draw_networkx_edge_labels(
    G2, pos, edge_labels=edge_labels, font_size=8, font_color=edge_font_color
)

plt.show()
