import pandas as pd
import numpy as np
import random
import time
import tkinter as tk
from tkinter import simpledialog
import logging

# Load data
# Load data
travel_data = pd.read_csv("travel.csv")
places_data = pd.read_csv("places.csv", index_col="PLACES")
merged_data = pd.merge(
    travel_data, places_data, left_on="Destination", right_index=True, how="left"
)
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )
city_to_railways = {
    "Bhubaneswar": "Bhubaneswar Railway Station(Bhubaneswar)",
    "Cuttack": "Cuttack Junction Railway Station(Cuttack)",
    "Kolkata": "Howrah Junction Railway Station(Kolkata)",
    "Visakhapatnam": "Visakhapatnam Railway Station(Visakhapatnam)",
}


def save_merged_data_to_csv(filename="merged_data.csv"):
    merged_data.to_csv(filename, index=False)
    print(f"Merged data saved to {filename}")


def gui_input():
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


save_merged_data_to_csv()


# Function to extract the city name from place names
def extract_city_name(place):
    """Extracts the city name from a place name formatted as 'Place(City)'"""
    return place.split("(")[-1].strip(")")


# Create initial population consisting of random tours
def create_initial_population(size, starting_city, places):
    """Generates a list of random tours starting and ending in the starting_city."""
    city_places = places
    population = []
    starting_place = city_to_railways[starting_city]
    for _ in range(size):
        tour = random.sample(
            [p for p in city_places if p != starting_place], len(city_places) - 1
        )
        population.append(tour)
    return population


# Calculate the fitness of a tour
def calculate_fitness(tour, max_time, max_cost):
    total_time, total_cost, total_ratings = 0, 0, 0
    for i in range(len(tour) - 1):
        row = merged_data[
            (merged_data["Source"] == tour[i])
            & (merged_data["Destination"] == tour[i + 1])
        ]
        if not row.empty:
            time_inc = (
                row["Time(hrs)"].values[0] + places_data.at[tour[i + 1], "TIME(HOURS)"]
            )
            cost_inc = row["Cost(Rs)"].values[0] + places_data.at[tour[i + 1], "COST"]
            rating_inc = places_data.at[tour[i + 1], "RATINGS"]
            total_time += time_inc
            total_cost += cost_inc
            total_ratings += rating_inc
            # logging.debug(
            #     f"Adding segment from {tour[i]} to {tour[i+1]}: time={time_inc}, cost={cost_inc}, ratings={rating_inc}"
            # )

    penalty = 0
    if total_time > max_time > 0:
        penalty += (total_time - max_time) * 50
        # logging.debug(f"Penalty for time: {(total_time - max_time) * 50}")
    if total_cost > max_cost > 0:
        penalty += (total_cost - max_cost) * 50
        # logging.debug(f"Penalty for cost: {(total_cost - max_cost) * 50}")

    fitness = total_time + total_cost - total_ratings * 10 + penalty
    # logging.info(
    #     f"Calculated fitness: {fitness} (Time: {total_time}, Cost: {total_cost}, Ratings: {total_ratings})"
    # )
    return fitness


# Tournament selection for choosing parents
def select_parents(population, fitness_scores):
    """Selects parents using tournament selection."""
    tournament_size = 5
    tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
    tournament.sort(key=lambda x: x[1])
    return tournament[0][0]


# Ordered crossover to produce offspring
def crossover(parent1, parent2):
    """Perform ordered crossover between two parents."""
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


# Mutation by swapping two cities in the tour
def mutate(tour, mutation_rate=0.1):
    """Mutates a tour by swapping two cities."""
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(tour)), 2)
        tour[idx1], tour[idx2] = tour[idx2], tour[idx1]
    return tour


# Main genetic algorithm
# Main genetic algorithm
def genetic_algorithm(
    starting_city, max_time, max_cost, population_size=10, generations=100
):
    places = list(places_data.index)
    city_places = [p for p in places if extract_city_name(p) == starting_city]
    # print(city_places)
    if not city_places:
        return None

    population = create_initial_population(population_size, starting_city, city_places)
    for _ in range(generations):
        fitness_scores = [
            calculate_fitness(tour, max_time, max_cost) for tour in population
        ]
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = [
                select_parents(population, fitness_scores) for _ in range(2)
            ]
            child1, child2 = crossover(parent1, parent2), crossover(parent2, parent1)
            new_population.extend([mutate(child1), mutate(child2)])
        population = new_population
        # print("  :   ",population)

    final_fitness_scores = [
        calculate_fitness(tour, max_time, max_cost) for tour in population
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
            [city_to_railways[starting_city]]
            + best_tour
            + [city_to_railways[starting_city]]
        )
        best_time, best_cost, best_rating = evaluate_tour(best_tour)
        # print(final_fitness_scores)
        if best_time <= max_time and best_cost <= max_cost:
            return best_tour, best_time, best_cost, best_rating
        
        final_fitness_scores.pop(best_index)
        population.pop(best_index)
        
    return None, None, None, None


def evaluate_tour(tour):
    """Evaluates the specified tour to return its total time, cost, and average rating."""
    # print(" tour : ",tour)
    total_time, total_cost, total_ratings = 0, 0, 0
    for i in range(len(tour) - 1):
        row = merged_data[
            (merged_data["Source"] == tour[i])
            & (merged_data["Destination"] == tour[i + 1])
            | (merged_data["Destination"] == tour[i])
            & (merged_data["Source"] == tour[i + 1])
        ]
        # print(i, " : ", row)
        if not row.empty:
            total_time += (
                row["Time(hrs)"].values[0] + places_data.at[tour[i + 1], "TIME(HOURS)"]
            )
            total_cost += (
                row["Cost(Rs)"].values[0] + places_data.at[tour[i + 1], "COST"]
            )
            # print(places_data.at[tour[i + 1], "RATINGS"], end=" ")
            total_ratings += places_data.at[tour[i + 1], "RATINGS"]
    num_stops = len(tour) - 1
    average_rating = (total_ratings / num_stops) if num_stops > 0 else 0
    return total_time, total_cost, average_rating


# User inputs
starting_city, max_time, max_cost = gui_input()
# Run the algorithm
population_size, generations = 20, 100
start_time = time.time()
optimal_tour, total_time, total_cost, average_rating = genetic_algorithm(
    starting_city, max_time, max_cost, population_size, generations
)
end_time = time.time()
execution_time = end_time - start_time
if optimal_tour:
    for i in range(len(optimal_tour)):
        print(i + 1, optimal_tour[i])
    print("Total Time (in hrs):", total_time)
    print("Total Cost (in rupess):", total_cost)
    print("Rating :", average_rating)
else:
    print("No valid tour could be found or the starting city is not valid.")

print(f"Execution Time: {execution_time} seconds")
