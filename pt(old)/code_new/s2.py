import pandas as pd
import numpy as np
import random
import time  # Import the time module

# Load data
travel_data = pd.read_csv("travel.csv")
places_data = pd.read_csv("places.csv", index_col="PLACES")
merged_data = pd.merge(
    travel_data, places_data, left_on="Destination", right_index=True, how="left"
)

def save_merged_data_to_csv(filename="merged_data.csv"):
    merged_data.to_csv(filename, index=False)
    print(f"Merged data saved to {filename}")

save_merged_data_to_csv()

def extract_city_name(place):
    """Extracts the city name from a place name formatted as 'Place(City)'"""
    return place.split("(")[-1].strip(")")

def create_initial_population(size, starting_city, places):
    city_places = [place for place in places if extract_city_name(place) == starting_city]
    population = []
    for _ in range(size):
        tour = [starting_city] + random.sample([p for p in city_places if p != starting_city], len(city_places) - 1) + [starting_city]
        population.append(tour)
    return population

def calculate_fitness(tour, max_time, max_cost):
    total_time, total_cost, total_ratings = 0, 0, 0
    for i in range(len(tour) - 1):
        row = merged_data[(merged_data["Source"] == tour[i]) & (merged_data["Destination"] == tour[i + 1])]
        if not row.empty:
            total_time += row["Time(hrs)"].values[0] + places_data.at[tour[i + 1], "TIME(HOURS)"]
            total_cost += row["Cost(Rs)"].values[0] + places_data.at[tour[i + 1], "COST"]
            total_ratings += places_data.at[tour[i + 1], "RATINGS"]
    penalty = 0
    if total_time > max_time:
        penalty += (total_time - max_time) * 50
    if total_cost > max_cost:
        penalty += (total_cost - max_cost) * 50
    return total_time + total_cost - total_ratings * 10 + penalty

def select_parents(population, fitness_scores):
    tournament_size = 5
    tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
    tournament.sort(key=lambda x: x[1])
    return tournament[0][0]

def crossover(parent1, parent2):
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

def mutate(tour, mutation_rate=0.1):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(tour)), 2)
        tour[idx1], tour[idx2] = tour[idx2], tour[idx1]
    return tour

def genetic_algorithm(starting_city, max_time, max_cost, population_size=10, generations=50):
    places = list(places_data.index)
    city_places = [p for p in places if extract_city_name(p) == starting_city]
    if not city_places:
        return None

    population = create_initial_population(population_size, starting_city, city_places)
    start_time = time.time()  # Start timing
    for _ in range(generations):
        fitness_scores = [calculate_fitness(tour, max_time, max_cost) for tour in population]
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = [select_parents(population, fitness_scores) for _ in range(2)]
            child1, child2 = crossover(parent1, parent2), crossover(parent2, parent1)
            new_population.extend([mutate(child1), mutate(child2)])
        population = new_population

    final_fitness_scores = [calculate_fitness(tour, max_time, max_cost) for tour in population]
    best_index = np.argmin(final_fitness_scores)
    best_tour = population[best_index]
    end_time = time.time()  # End timing
    return best_tour, final_fitness_scores[best_index], end_time - start_time  # Return time taken

# User inputs and run the algorithm
starting_city = input("Enter the starting city: ")
max_time = float(input("Enter the maximum allowable time in hours: "))
max_cost = float(input("Enter the maximum allowable cost in Rs: "))

optimal_tour, fitness_score, duration = genetic_algorithm(starting_city, max_time, max_cost)
if optimal_tour:
    print("Optimal Tour:", optimal_tour)
    print("Fitness Score:", fitness_score)
    print("Time Taken to run the algorithm (seconds):", duration)
else:
    print("No valid tour could be found or the starting city is not valid.")
