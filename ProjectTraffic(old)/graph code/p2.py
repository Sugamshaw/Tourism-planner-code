import networkx as nx
import matplotlib.pyplot as plt
import csv


def show():
    G = nx.Graph()
    with open("rating2.csv", "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            G.add_node(row[0])
    with open("travel2.csv", "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            G.add_edge(row[0], row[1], weight=float(row[2]))
    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="skyblue",
        node_size=500,
        font_size=12,
        font_weight="bold",
        
    )
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    plt.show()


if __name__ == "__main__":
    show()
