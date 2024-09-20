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
        # Compare based on some criteria, e.g., time or rating
        # Here, we compare based on time
        return self.time < other.time


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

    def calculate_ideal_path(self, paths, limit_time, budget):
        if not paths:
            print("there are no paths to the destination")
            exit(1)

        for path in paths:
            total_time = 0
            total_cost = 0
            total_rating = 0
            for place in path:
                total_time = total_time + place.time
                total_cost = total_cost + place.cost
                total_rating = total_rating + place.rating
            i = 0
            while i < len(path) - 1:
                total_cost = total_cost + self.graph[path[i]][path[i + 1]][1]
                total_time = total_time + self.graph[path[i]][path[i + 1]][0]
                i = i + 1

            if total_time <= limit_time and total_cost <= budget:
                times.append(total_time)
                places.append(len(path))
                costs.append(total_cost)
                ratings.append(total_rating)
                priorities.append(total_cost / (total_rating * len(path)))
                shorter_paths.append(path)
                heapq.heappush(
                    priority_queue, (total_cost / (total_rating * len(path)), path)
                )
        if not shorter_paths:
            print(f"No paths found to {destination}")
            exit(0)


if __name__ == "__main__":
    graph = Graph()
    start = time.time()
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
    source = input("start: ")
    destination = input("end: ")
    time_limit = int(input("how much time do you have?: "))
    budget = int(input("what is your budget?: "))
    start_time = time.time()
    vertex1 = city_to_vertex[source]
    vertex2 = city_to_vertex[destination]
    paths = graph.find_all_paths(vertex1, vertex2)
    graph.calculate_ideal_path(paths, time_limit, budget)
    with open("output.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "source",
                "destination",
                "average_rating",
                "cost",
                "time",
                "no of places",
                "path",
            ]
        )
        while priority_queue:
            priority, path = heapq.heappop(priority_queue)
            name = []
            for city in path:
                name.append(city.city)
                name.append("->")
            name.pop()
            pathString = " ".join(name)
            index = shorter_paths.index(path)
            row = []
            row.append(source)
            row.append(destination)
            row.append(ratings[index] / places[index])
            row.append(costs[index])
            row.append(times[index])
            row.append(places[index])
            row.append(pathString)
            writer.writerow(row)
        end = time.time()
        writer.writerow([])
        writer.writerow([f"time taken: {end-start}"])
