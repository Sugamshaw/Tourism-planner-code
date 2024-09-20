from collections import defaultdict, deque
import csv
import time
import heapq

file1 = "travel.csv"
file2 = "places.csv"
destination = None
source = None
city_to_vertex = {}
times = []
places = []
costs = []
priorities = []
ratings = []
shorter_paths = []
priority_queue = []


class Node:
    def __init__(self, city, rating, time, cost):
        self.time = time
        self.rating = rating
        self.city = city
        self.cost = cost

    def __lt__(self, other):
        return self.time < other.time


class Edge:
    def __init__(self, source, destination, time, cost):
        self.source = source
        self.destination = destination
        self.time = time
        self.cost = cost

    def solve(self, source, destination):
        print("hii")
        print(self.source)
        if self.source == source and self.destination == destination:
            return self.time, self.cost


class Graph:
    def __init__(self, is_directed=False):
        self.graph = defaultdict(list)
        self.is_directed = is_directed
        self.node_to_index = {}

    def get_edge(self, source, destination):
        for edge in self.graph[source]:
            if edge.destination == destination:
                return edge
        return None

    def add_vertex(self, vertex):
        if vertex not in self.node_to_index:
            index = len(self.node_to_index)
            self.node_to_index[vertex] = index

    def add_edge(self, vertex1, vertex2, time, cost):
        self.graph[vertex1].append(Edge(vertex1, vertex2, time, cost))
        if not self.is_directed:
            self.graph[vertex2].append(
                Edge(vertex2, vertex1, time, cost)
            )  # For undirected graphs, add reverse edge

    def heuristic(self, current, goal):
        return (
            (current.time - goal.time) ** 2 + (current.rating - goal.rating) ** 2
        ) ** 0.5

    def find_path_astar(self, start, goal, limit_time, budget):
        start_index = self.node_to_index[start]
        goal_index = self.node_to_index[goal]

        open_list = [(0, start_index)]
        closed_set = [False] * len(self.node_to_index)
        came_from = [-1] * len(self.node_to_index)
        g_score = [float("inf")] * len(self.node_to_index)
        g_score[start_index] = 0
        f_score = [float("inf")] * len(self.node_to_index)
        f_score[start_index] = self.heuristic(start, goal)

        while open_list:
            current_f, current_index = heapq.heappop(open_list)

            if current_index == goal_index:
                path = deque()
                while current_index != -1:
                    path.appendleft(list(self.node_to_index.keys())[current_index])
                    current_index = came_from[current_index]
                # print("nn: ",self.graph)
                return path

            closed_set[current_index] = True

            for edge in self.graph[list(self.node_to_index.keys())[current_index]]:
                neighbor_index = self.node_to_index[edge.destination]
                if closed_set[neighbor_index]:
                    continue

                tentative_g_score = g_score[current_index] + edge.time
                if tentative_g_score >= g_score[neighbor_index]:
                    continue

                came_from[neighbor_index] = current_index
                g_score[neighbor_index] = tentative_g_score
                f_score[neighbor_index] = g_score[neighbor_index] + self.heuristic(
                    edge.destination, goal
                )
                heapq.heappush(open_list, (f_score[neighbor_index], neighbor_index))

        return deque()


def load_graph_from_csv(graph, file1, file2):
    with open(file2, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            vertex = Node(row[0].strip(), float(row[1]), float(row[2]), float(row[3]))
            city_to_vertex[row[0].strip()] = vertex
            graph.add_vertex(vertex)

    with open(file1, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            vertex1 = city_to_vertex.get(row[0].strip())
            vertex2 = city_to_vertex.get(row[1].strip())
            if vertex1 and vertex2:
                graph.add_edge(vertex1, vertex2, float(row[2]), float(row[3]))


def get_user_input():
    source = input("Enter your starting city: ").strip()
    destination = input("Enter your destination city: ").strip()
    try:
        time_limit = int(input("Enter the maximum time you have (in hours): "))
        budget = int(input("Enter your budget: "))
        return source, destination, time_limit, budget
    except ValueError:
        print("Invalid input! Please enter a valid integer for time and budget.")
        return None, None, None, None


# def print_path_info(path, start, end, total_time, total_cost, avg_rating):
#     print("\nOptimal Path:")
#     print("-------------")
#     print(f"Source: {start}")
#     print(f"Destination: {end}")
#     print(f"Average Rating: {avg_rating:.2f}")
#     print(f"Total Cost: {total_cost:.2f}")
#     print(f"Total Time: {total_time:.2f} hours")
#     print("Number of Places: ", len(path))
#     print("Path: ", " -> ".join(path))

def API(source,destination,time_limit,budget):
    graph = Graph()
    load_graph_from_csv(graph, file1, file2)

    if source and destination and time_limit is not None and budget is not None:
        if source not in city_to_vertex or destination not in city_to_vertex:
            return None
        else:
            vertex1 = city_to_vertex[source]
            vertex2 = city_to_vertex[destination]
            path = graph.find_path_astar(vertex1, vertex2, time_limit, budget)
            if path:
                l = []
                for node in path:
                    l.append(node.city)
                tt, tc = 0, 0
                for i in range(len(l) - 1):
                    vertex1 = city_to_vertex.get(l[i].strip())
                    vertex2 = city_to_vertex.get(l[i + 1].strip())
                    edge = graph.get_edge(vertex1, vertex2)
                    tt += edge.time
                    tc += edge.cost
                total_time = sum(node.time for node in path) + tt
                total_cost = sum(node.cost for node in path) + tc
                total_rating = sum(node.rating for node in path)
                avg_rating = total_rating / len(path)
                path_info = (
                    [node.city for node in path],
                    total_time,
                    total_cost,
                    avg_rating,
                )
                return path_info
            else:
                return None
    else:
        return None
