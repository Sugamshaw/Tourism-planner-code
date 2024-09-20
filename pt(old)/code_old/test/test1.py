import csv
import time
import heapq

file1 = "travel.csv"
file2 = "places.csv"
destination = None
source = None
city_to_vertex = {}
max_time = 0
max_cost = 0


class Node:
    def __init__(self, city, rating, time, cost):
        self.time = time
        self.rating = rating
        self.city = city
        self.cost = cost


class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = {}

    def add_edge(self, vertex1, vertex2, time, cost):

        if vertex1 in self.graph and vertex2 in self.graph:
            if vertex2 not in self.graph[vertex1]:
                self.graph[vertex1][vertex2] = []
            if vertex1 not in self.graph[vertex2]:
                self.graph[vertex2][vertex1] = []
            self.graph[vertex1][vertex2].append(time)
            self.graph[vertex1][vertex2].append(cost)
            self.graph[vertex2][vertex1].append(time)
            self.graph[vertex2][vertex1].append(cost)

    def find_all_paths(self, start, end, path=[], time=0):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.graph:
            return []
        paths = []
        for neighbor in self.graph[start]:
            if neighbor not in path:
                new_paths = self.find_all_paths(neighbor, end, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths


if __name__ == "__main__":
    graph = Graph()
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
            vertex1 = city_to_vertex[row[0].strip()]
            vertex2 = city_to_vertex[row[1].strip()]
            graph.add_edge(vertex1, vertex2, float(row[2]), float(row[3]))
    source = city_to_vertex[input("start: ")]
    destination = city_to_vertex[input("end: ")]

    paths = graph.find_all_paths(source, destination)

    for path in paths:
        i = 1
        temp_time = 0
        temp_cost = 0
        while i < len(path) - 1:
            temp_time += path[i - 1].time + graph.graph[path[i - 1]][path[i]][0]
            temp_cost += path[i - 1].cost + graph.graph[path[i - 1]][path[i]][1]
            i += 1
        temp_time += path[i - 1].time
        temp_cost += path[i - 1].cost
        if temp_time > max_time:
            max_time = temp_time
        if temp_cost > max_cost:
            max_cost = temp_cost
    print("max time: ", max_time)
    print("max_cost: ", max_cost)
    print("Total paths :", len(paths))
