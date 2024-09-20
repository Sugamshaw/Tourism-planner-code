import csv
import time

file1 = "travel2.csv"
file2 = "rating2.csv"
destination = None
source = None
city_to_vertex = {}


class Node:
    def __init__(self, city, rating, time):
        self.time = time
        self.rating = rating
        self.city = city


class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = {}

    def add_edge(self, vertex1, vertex2, time):
        if vertex1 in self.graph and vertex2 in self.graph:
            if vertex2 not in self.graph[vertex1]:
                self.graph[vertex1][vertex2] = []
            if vertex1 not in self.graph[vertex2]:
                self.graph[vertex2][vertex1] = []
            self.graph[vertex1][vertex2].append(time)
            self.graph[vertex2][vertex1].append(time)

    def display(self):
        for vertex in self.graph:
            print(vertex, ":", self.graph[vertex])

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

    def calculate_ideal_path(self, paths, limit_time):
        times = []
        shorter_paths = []
        if not paths:
            print("there are no paths to the destination")
            exit()
        for path in paths:
            time = 0
            for vertex in path:
                time = time + vertex.time
            i, j = 0, 1
            while j < len(path):
                time = time + self.graph[path[i]][path[j]][0]
                i = i + 1
                j = j + 1
            if time <= limit_time:
                times.append(time)
                shorter_paths.append(path)

        if not shorter_paths:
            print(f"you have insufficient time to travel to {destination}")
            exit(0)

        i = 0
        highest_rating = 0
        highest_rated_path = 0

        with open("output.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["source", "destination", "time_taken", "average_rating", "path"]
            )
            while i < len(shorter_paths):
                rating = 0
                path = shorter_paths[i]
                for vertex in path:
                    rating = rating + vertex.rating
                average_rating = rating / len(path)

                name = []
                string = []
                name.append(source)
                name.append(destination)
                name.append(times[i])
                name.append(average_rating)
                for vertex in path:
                    string.append(vertex.city)
                name.append("->".join(string))
                writer.writerow(name)
                if average_rating > highest_rating:
                    highest_rating = average_rating
                    highest_rated_path = i
                i = i + 1
            writer.writerow([])
            path = shorter_paths[highest_rated_path]
            name = []
            for vertex in path:
                name.append(vertex.city)
            string = "->".join(name)
            myrow = []
            myrow.append(source)
            myrow.append(destination)
            myrow.append(times[highest_rated_path])
            myrow.append(highest_rating)
            myrow.append(string)
            writer.writerow(myrow)
            return shorter_paths[highest_rated_path]


if __name__ == "__main__":
    graph = Graph()
    with open(file2, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            vertex = Node(row[0], float(row[1]), float(row[2]))
            city_to_vertex[row[0]] = vertex
            graph.add_vertex(vertex)
    with open(file1, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            vertex1 = city_to_vertex[row[0]]
            vertex2 = city_to_vertex[row[1]]
            graph.add_edge(vertex1, vertex2, float(row[2]))
    source = input("Enter starting destination: ")
    destination = input("Enter ending destination: ")
    limit = int(input("How much time do you have?(in Hours): "))
    start_time = time.time()
    vertex1 = city_to_vertex[source]
    vertex2 = city_to_vertex[destination]
    paths = graph.find_all_paths(vertex1, vertex2)
    path = graph.calculate_ideal_path(paths, limit)
    end_time = time.time()

    print("best path: ")
    for cities in path:
        print(cities.city)
    print(f"Time taken to execute: {end_time-start_time} ")
