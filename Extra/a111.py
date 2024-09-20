import csv
from collections import defaultdict, deque
class Edge:
    def __init__(self, source, destination, time, cost):
        self.source = source
        self.destination = destination
        self.time = time
        self.cost = cost
    def solve(self,source,destination):
        print("hii")
        print(self.source)
        if(self.source == source and self.destination == destination):
            return self.time
        
class Graph:
    def __init__(self, is_directed=False):
        self.node_to_index = {}
        self.graph = defaultdict(list)

    def get_edge(self, source, destination):
        for edge in self.graph[source]:
            print(edge)
            if edge.destination == destination:
                return edge
        return None
    
    def add_edge(self, vertex1, vertex2, time, cost):
        self.graph[vertex1].append(Edge(vertex1, vertex2, time, cost))
def load_graph_from_csv(graph, file1, file2):
    with open(file1, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            vertex1 = row[0].strip()
            vertex2 = row[1].strip()
            if vertex1 and vertex2:
                graph.add_edge(vertex1, vertex2, float(row[2]), float(row[3])) 
if __name__ == "__main__":
    graph=Graph()
    load_graph_from_csv(graph, "travel.csv", "places.csv")
    print(graph.get_edge("Bhubaneswar Railway Station(Bhubaneswar)","Lingaraj Temple(Bhubaneswar)"))