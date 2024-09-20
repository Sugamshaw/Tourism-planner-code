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

df = pd.read_csv("network.csv")

G2 = nx.DiGraph()

G2 = nx.from_pandas_edgelist(
    df, source="source", target="destination", edge_attr="Length"
)

pos = nx.spring_layout(G2, k=2)
weights = list(nx.get_edge_attributes(G2, "Length").values())
weights = list(i / 5 for i in weights)


nx.draw(
        G2,
        pos,
        with_labels=True,
        node_color="skyblue",
        node_size=500,
        font_size=12,
        font_weight="bold",
        
    )
edge_labels = nx.get_edge_attributes(G2, "Length")
nx.draw_networkx_edge_labels(G2, pos, edge_labels=edge_labels, font_size=10)
plt.show()