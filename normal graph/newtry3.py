import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv('travelprachi.csv')

# Create an undirected graph
G = nx.Graph()

# Add nodes and edges from the CSV file
for index, row in df.iterrows():
    G.add_edge(row['Source'], row['Destination'], time=row['Time(hrs)'], cost=row['Cost(Rs)'])

# Draw the network
pos = nx.spring_layout(G,k=1)  # Positions nodes using Fruchterman-Reingold force-directed algorithm
nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'time')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title('Transportation Network')
plt.show()
