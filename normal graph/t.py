import csv
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Parse the CSV data and extract unique city names
cities = set()
with open('travel.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        source_city = row[0].split('(')[1][:-1]  # Extract city name from source
        dest_city = row[1].split('(')[1][:-1]    # Extract city name from destination
        cities.add(source_city)
        cities.add(dest_city)

# Step 2: Create a graph using NetworkX
G = nx.Graph()

# Step 3: Add nodes for places within each city
for city in cities:
    places = [row[0].split('(')[0] for row in reader if row[0].split('(')[1][:-1] == city]
    for place in places:
        G.add_node(place)

# Step 4: Add edges representing connections between places within each city
for row in reader:
    source_city = row[0].split('(')[1][:-1]
    dest_city = row[1].split('(')[1][:-1]
    if source_city == dest_city:  # Check if both places belong to the same city
        source = row[0].split('(')[0]
        destination = row[1].split('(')[0]
        time = float(row[2])
        G.add_edge(source, destination, weight=time)  # Add time as edge length

# Step 5: Visualize the graph with matplotlib
pos = nx.spring_layout(G, k=2.5, iterations=100)  # Adjust k and iterations for better layout
nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=10)

# Draw edge labels
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Network of Cities and Places of Interest")
plt.show()
