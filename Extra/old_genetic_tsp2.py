import pandas as pd
import numpy as np
import random
import time
import tkinter as tk
from tkinter import simpledialog


class GeneticAlgorithm:
    def __init__(self, travel_data_path, places_data_path):
        self.travel_data = pd.read_csv(travel_data_path)
        self.places_data = pd.read_csv(places_data_path, index_col="PLACES")
        self.merged_data = pd.merge(
            self.travel_data,
            self.places_data,
            left_on="Destination",
            right_index=True,
            how="left",
        )
        self.city_to_railways = {
            "Bhubaneswar": "Bhubaneswar Railway Station(Bhubaneswar)",
            "Cuttack": "Cuttack Junction Railway Station(Cuttack)",
            "Kolkata": "Howrah Junction Railway Station(Kolkata)",
            "Visakhapatnam": "Visakhapatnam Railway Station(Visakhapatnam)",
        }

    def save_merged_data_to_csv(self, filename="merged_data.csv"):
        self.merged_data.to_csv(filename, index=False)
        print(f"Merged data saved to {filename}")

    def gui_input(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        starting_city = simpledialog.askstring(
            "Input", "Enter the starting city:", parent=root
        )
        max_time = simpledialog.askfloat(
            "Input", "Enter the maximum allowable time in hours:", parent=root
        )
        max_cost = simpledialog.askfloat(
            "Input", "Enter the maximum allowable cost in Rs:", parent=root
        )
        return starting_city, max_time, max_cost

    def create_initial_population(self, size, starting_city, places):
        city_places = places
        population = []
        starting_place = self.city_to_railways[starting_city]
        for _ in range(size):
            tour = random.sample(
                [p for p in city_places if p != starting_place], len(city_places) - 1
            )
            population.append(tour)
        return population

    def calculate_fitness(self, tour, max_time, max_cost):
        total_time, total_cost, total_ratings = 0, 0, 0
        for i in range(len(tour) - 1):
            row = self.merged_data[
                (self.merged_data["Source"] == tour[i])
                & (self.merged_data["Destination"] == tour[i + 1])
            ]
            if not row.empty:
                time_inc = (
                    row["Time(hrs)"].values[0]
                    + self.places_data.at[tour[i + 1], "TIME(HOURS)"]
                )
                cost_inc = (
                    row["Cost(Rs)"].values[0] + self.places_data.at[tour[i + 1], "COST"]
                )
                rating_inc = self.places_data.at[tour[i + 1], "RATINGS"]
                total_time += time_inc
                total_cost += cost_inc
                total_ratings += rating_inc

        penalty = 0
        if total_time > max_time > 0:
            penalty += (total_time - max_time) * 50
        if total_cost > max_cost > 0:
            penalty += (total_cost - max_cost) * 50

        fitness = total_time + total_cost - total_ratings * 10 + penalty
        return fitness

    def select_parents(self, population, fitness_scores):
        tournament_size = 5
        tournament = random.sample(
            list(zip(population, fitness_scores)), tournament_size
        )
        tournament.sort(key=lambda x: x[1])
        return tournament[0][0]

    def crossover(self, parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [None] * len(parent1)
        child[start:end] = parent1[start:end]
        child_pos = end
        for gene in parent2:
            if gene not in child:
                while child[child_pos] is not None:
                    child_pos = (child_pos + 1) % len(child)
                child[child_pos] = gene
        return child

    def mutate(self, tour, mutation_rate=0.1):
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(tour)), 2)
            tour[idx1], tour[idx2] = tour[idx2], tour[idx1]
        return tour

    def run(
        self, starting_city, max_time, max_cost, population_size=10, generations=100
    ):
        places = list(self.places_data.index)
        city_places = [p for p in places if self.extract_city_name(p) == starting_city]
        if not city_places:
            return None

        population = self.create_initial_population(
            population_size, starting_city, city_places
        )
        for _ in range(generations):
            fitness_scores = [
                self.calculate_fitness(tour, max_time, max_cost) for tour in population
            ]
            new_population = []
            while len(new_population) < population_size:
                parent1, parent2 = [
                    self.select_parents(population, fitness_scores) for _ in range(2)
                ]
                child1, child2 = self.crossover(parent1, parent2), self.crossover(
                    parent2, parent1
                )
                new_population.extend([self.mutate(child1), self.mutate(child2)])
            population = new_population

        final_fitness_scores = [
            self.calculate_fitness(tour, max_time, max_cost) for tour in population
        ]
        # best_index = np.argmin(final_fitness_scores)
        # best_tour = population[best_index]
        # best_time, best_cost, best_rating = evaluate_tour(best_tour)
        # return best_tour, best_time, best_cost, best_rating
        checked = 0
        while checked < population_size:
            checked += 1
            best_index = np.argmin(final_fitness_scores)
            best_tour = population[best_index]
            best_tour = (
                [self.city_to_railways[starting_city]]
                + best_tour
                + [self.city_to_railways[starting_city]]
            )
            best_time, best_cost, best_rating = self.evaluate_tour(best_tour)
            # print(final_fitness_scores)
            if best_time <= max_time and best_cost <= max_cost:
                return best_tour, best_time, best_cost, best_rating

            final_fitness_scores.pop(best_index)
            population.pop(best_index)
        return None, None, None, None

    def extract_city_name(self, place):
        return place.split("(")[-1].strip(")")

    def evaluate_tour(self, tour):
        total_time, total_cost, total_ratings = 0, 0, 0
        for i in range(len(tour) - 1):
            row = self.merged_data[
                (self.merged_data["Source"] == tour[i])
                & (self.merged_data["Destination"] == tour[i + 1])
                | (self.merged_data["Destination"] == tour[i])
                & (self.merged_data["Source"] == tour[i + 1])
            ]
            if not row.empty:
                total_time += (
                    row["Time(hrs)"].values[0]
                    + self.places_data.at[tour[i + 1], "TIME(HOURS)"]
                )
                total_cost += (
                    row["Cost(Rs)"].values[0] + self.places_data.at[tour[i + 1], "COST"]
                )
                total_ratings += self.places_data.at[tour[i + 1], "RATINGS"]
        num_stops = len(tour) - 1
        average_rating = (total_ratings / num_stops) if num_stops > 0 else 0
        return total_time, total_cost, average_rating


# Example of how to use the TourOptimizer class
if __name__ == "__main__":

    optimizer = GeneticAlgorithm("travel.csv", "places.csv")
    print("Please enter details for the tour optimization.")
    starting_city, max_time, max_cost = optimizer.gui_input()

    if not starting_city:
        print("No starting city provided. Exiting.")
    population_size, generations = 20, 100
    print(f"Starting optimization for tours starting from {starting_city}.")
    start_time = time.time()
    optimal_tour, total_time, total_cost, average_rating = optimizer.run(
        starting_city, max_time, max_cost, population_size, generations
    )
    end_time = time.time()
    execution_time = end_time - start_time
    if optimal_tour:
        print("Optimal Tour Details:")
        for i in range(len(optimal_tour)):
            print(i + 1, optimal_tour[i])
        print("Total time:", total_time)
        print("Total cost:", total_cost)
        print("Average rating:", average_rating)
    else:
        print("No valid tour could be found or the starting city is not valid.")

print(f"Execution Time: {execution_time} seconds")
