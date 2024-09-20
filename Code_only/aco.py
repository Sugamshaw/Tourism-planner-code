import re
import random as rn
import numpy as np
from numpy.random import choice as np_choice
import csv
import time

num_name = {}
name_num = {}
budget = 0
time_limit = 0
source = 0
city = None
domain = None
city_to_railways = {
    "bhubaneswar": "Bhubaneswar Railway Station(Bhubaneswar)",
    "cuttack": "Cuttack Junction Railway Station(Cuttack)",
    "kolkata": "Howrah Junction Railway Station(Kolkata)",
    "visakhapatnam": "Visakhapatnam Railway Station(Visakhapatnam)",
}


class AntColony(object):

    def __init__(
        self, times, costs, n_ants, n_best, n_iterations, decay, alpha=1, beta=1
    ):
        self.times = times
        self.costs = costs
        self.pheromone = np.full(self.times.shape, 200) / len(times)
        self.all_inds = range(len(times))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        best_path = None
        all_time_best_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            if len(all_paths) == 0:
                continue
            self.spread_pheromone(all_paths)
            best_path = min(all_paths, key=lambda x: x[1])
            if best_path[1] < all_time_best_path[1]:
                all_time_best_path = best_path
            self.pheromone = self.pheromone * self.decay
        return all_time_best_path

    def spread_pheromone(self, all_paths):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[: self.n_best]:
            for move in path:
                info = num_name[move[0]]
                rating = info[1]
                time = info[2]
                cost = info[3]

                self.pheromone[move] += (rating * 200) / (cost * time)

    def gen_path_cost_time(self, path):
        total_time = num_name[path[0][0]][2]
        total_cost = num_name[path[0][0]][3]
        for ele in path:
            total_time += self.times[ele] + num_name[ele[1]][2]
            total_cost += self.costs[ele] + num_name[ele[1]][3]
        return [total_time, total_cost]

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(source)
            if not path:
                continue
            all_paths.append((path, 200 / len(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.times) - 1):
            move = self.pick_move(
                self.pheromone[prev], self.times[prev], self.costs[prev], visited
            )
            if not move:
                break
            # checking whether the path is going outside the city or not
            place_name = num_name[move][0]
            city_name = re.search(r"\((.*?)\)", place_name).group(1)
            # print(domain)
            # print(city_name)
            # exit()
            if city_name == domain:
                path.append((prev, move))
                prev = move
            else:
                visited.add(move)
                continue
            # checking completed
            visited.add(move)
            # checking whether the path is in bounds of the time limit and budget
            time, cost = self.gen_path_cost_time(path)
            if time <= time_limit and cost <= budget:
                continue
            else:
                path.pop()
                break
        if len(path) == 0:
            return None
        return path

    def pick_move(self, pheromone, time, cost, visited):
        pheromone = np.copy(pheromone)  # it's row
        pheromone[list(visited)] = 0
        time[time == 0] = 0.1
        cost[cost == 0] = 0.1
        row = pheromone * self.alpha * ((200.0 / (time * cost)) * self.beta)
        row[row == np.inf] = 0
        row = np.nan_to_num(row, nan=0)

        if row.sum() == 0:
            return None

        norm_row = row / row.sum()

        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move


if __name__ == "__main__":
    # reading places
    count = 0  # number of places
    with open("places.csv", newline="") as places:
        reader = csv.reader(places)
        next(reader)
        for i, row in enumerate(reader):
            num_name[i] = (row[0], float(row[1]), float(row[2]), float(row[3]))
            name_num[row[0]] = i
            count += 1
    times = np.full((count, count), np.inf, dtype=float)
    costs = np.full((count, count), np.inf, dtype=float)
    with open("travel.csv", newline="") as travel:
        reader = csv.reader(travel)
        next(reader)
        for row in reader:
            times[name_num[row[0].strip()]][name_num[row[1].strip()]] = float(row[2])
            times[name_num[row[1].strip()]][name_num[row[0].strip()]] = float(row[2])
            costs[name_num[row[0].strip()]][name_num[row[1].strip()]] = float(row[3])
            costs[name_num[row[1].strip()]][name_num[row[0].strip()]] = float(row[3])
    start = time.time()
    ant_colony = AntColony(times, costs, 100, 10, 100, 0.3)
    city = city_to_railways[input("which city do you want to travel: ").lower()]
    time_limit = int(input("what is your time limit: "))
    budget = int(input("what is your budget: "))
    domain = re.search(r"\((.*?)\)", city).group(1)
    source = name_num[city]
    best_path = ant_colony.run()
    end = time.time()
    num_places = 1
    start_info = num_name[source]
    total_time, total_cost, total_rating = start_info[2], start_info[3], start_info[1]
    if best_path == ("placeholder", np.inf):
        print("no path exists")
        exit()
    print(city)
    for place in best_path[0]:
        info = num_name[place[1]]
        print(info[0])
        total_time += info[2]
        total_time += times[place]
        total_cost += info[3]
        total_cost += costs[place]
        total_rating += info[1]
        num_places += 1

    print("total_time: ", total_time)
    print("total_cost: ", total_cost)
    print("Average_rating: ", total_rating / num_places)
    print("Execution_time: ", end - start)
