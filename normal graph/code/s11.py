import pandas as pd
import numpy as np
import random

# Load data
travel_data = pd.read_csv("travel.csv")
places_data = pd.read_csv("places.csv", index_col="PLACES")
merged_data = pd.merge(travel_data, places_data, left_on="Destination", right_index=True, how="left")

def save_merged_data_to_csv(filename="merged_data.csv"):
    merged_data.to_csv(filename, index=False)
    print(f"Merged data saved to {filename}")

save_merged_data_to_csv()

def extract_city_name(place):
    return place.split("(")[-1].strip(")")

def create_initial_population(size, starting_city, places):
    valid_tours = []
    remaining_places = [place for place in places if place != starting_city and not merged_data[(merged_data['Source'] == starting_city) & (merged_data['Destination'] == place)].empty]
    if len(remaining_places) < 1:  # Check if there are enough places to visit
        return []
    for _ in range(size):
        valid_tour = [starting_city]
        random.shuffle(remaining_places)
        for place in remaining_places:
            if not merged_data[(merged_data['Source'] == valid_tour[-1]) & (merged_data['Destination'] == place)].empty:
                valid_tour.append(place)
        valid_tour.append(starting_city)
        valid_tours.append(valid_tour)
    return valid_tours



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
    if len(population) < 2:  # Ensure there are at least two individuals to perform a tournament
        return random.choice(population) if population else None
    tournament_size = min(5, len(population))
    tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
    tournament.sort(key=lambda x: x[1])
    return tournament[0][0]



def crossover(parent1, parent2):
    # Check if either parent is None
    if parent1 is None or parent2 is None or len(parent1) < 3 or len(parent2) < 3:
        # If there's an issue with the parents, return the non-None parent or an empty list
        return parent1 if parent1 is not None else parent2 if parent2 is not None else []
    
    start, end = sorted(random.sample(range(1, len(parent1) - 1), 2))
    child = [None] * len(parent1)
    child[start:end] = parent1[start:end]
    child_pos = end
    for gene in parent2:
        if gene not in child:
            while child[child_pos] is not None:
                child_pos = (child_pos + 1) % len(child)
            child[child_pos] = gene
    return repair_tour(child)


def repair_tour(tour):
    # Repair tour to ensure all paths are valid (simple and naive implementation)
    repaired_tour = [tour[0]]
    for i in range(1, len(tour)):
        if not merged_data[(merged_data['Source'] == repaired_tour[-1]) & (merged_data['Destination'] == tour[i])].empty:
            repaired_tour.append(tour[i])
    return repaired_tour

def mutate(tour, mutation_rate=0.1):
    if random.random() < mutation_rate:
        idx1 = random.randint(0, len(tour) - 2)
        idx2 = idx1 + 1
        tour[idx1], tour[idx2] = tour[idx2], tour[idx1]
    return tour

def genetic_algorithm(starting_city, max_time, max_cost, population_size=10, generations=50):
    places = list(places_data.index)
    city_places = [p for p in places if extract_city_name(p) == starting_city]
    if not city_places:
        return None
    population = create_initial_population(population_size, starting_city, city_places)
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
    return best_tour, calculate_fitness(best_tour, max_time, max_cost)

starting_city = input("Enter the starting city: ")
max_time = float(input("Enter the maximum allowable time in hours: "))
max_cost = float(input("Enter the maximum allowable cost in Rs: "))
optimal_tour, fitness_score = genetic_algorithm(starting_city, max_time, max_cost)
if optimal_tour:
    print("Optimal Tour:", optimal_tour)
    print("Fitness Score:", fitness_score)
else:
    print("No valid tour could be found or the starting city is not valid.")
