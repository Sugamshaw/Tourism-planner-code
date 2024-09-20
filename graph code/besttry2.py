import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# Load data from the CSV file
df = pd.read_csv("travel.csv")

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph from the DataFrame
for _, row in df.iterrows():
    G.add_edge(
        row["Source"], row["Destination"], time=row["Time(hrs)"], cost=row["Cost(Rs)"]
    )

# Define positions for nodes using a layout algorithm
pos = nx.spring_layout(G, k=0.5)  # Adjust the value of k to increase or decrease the distance between nodes

# Create edge traces
edge_x = []
edge_y = []
edge_text = []  # Text to display on hover for edges
for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    edge_text.append(f"Time: {edge[2]['time']} hrs<br>Cost: Rs {edge[2]['cost']}")

    # Scale the length of the edges based on time (time multiplied by some factor for visualization)
    time_scale_factor = 0.3  # You can adjust this factor as needed
    scaled_length = edge[2]["time"] * time_scale_factor
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    edge_text.append(f"Time: {edge[2]['time']} hrs<br>Cost: Rs {edge[2]['cost']}")
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(
            width=scaled_length, color="#888"
        ),  # Adjust the width based on scaled length
        hoverinfo="text",  # Update hoverinfo to display text
        text=edge_text,  # Set the text to be displayed on hover
        mode="lines",
    )

# Create node traces
node_x = []
node_y = []
node_names = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_names.append(node)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers",
    hoverinfo="text",
    text=node_names,
    marker=dict(
        showscale=True,
        colorscale="YlGnBu",
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15, title="Node Connections", xanchor="left", titleside="right"
        ),
        line_width=2,
    ),
)

# Update the figure layout
fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        title="<br>Network graph made with Python",
        titlefont_size=16,
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        annotations=[
            dict(
                text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.005,
                y=-0.002,
            )
        ],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    ),
)

# Show the figure
fig.show()
