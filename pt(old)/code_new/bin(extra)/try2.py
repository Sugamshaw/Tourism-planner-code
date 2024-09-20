import random
import pandas as pd

# Load data from CSV files
travel_data = pd.read_csv('travel.csv')
place_data = pd.read_csv('places.csv')

# Merge travel data and place data based on common attribute
merged_data = pd.merge(
    travel_data, place_data, left_on="Destination", right_on="PLACES"
)


# Define chromosome representation
def generate_random_tour():
    return list(merged_data['PLACES'].sample(frac=1))

# Define fitness function
def fitness(tour):
    total_time = 0
    total_cost = 0
    total_rating = 0
    
    for i in range(len(tour)-1):
        source = tour[i]
        destination = tour[i+1]
        route = merged_data[(merged_data['Source'] == source) & (merged_data['Destination'] == destination)]
        
        if not route.empty:
            total_time += route['Time(hrs)'].values[0]
            total_cost += route['Cost(Rs)'].values[0]
            total_rating += place_data.loc[place_data['PLACES'] == destination, 'RATINGS'].values[0]
        # else:
        #     print(f"No route found from {source} to {destination}")
            
    
    average_rating = total_rating / len(tour)
    return -total_time, -total_cost, average_rating

# Define genetic operators
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1)-1)
    child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
    return child1, child2

def mutate(tour):
    mutated_tour = tour[:]
    index1, index2 = random.sample(range(len(tour)), 2)
    mutated_tour[index1], mutated_tour[index2] = mutated_tour[index2], mutated_tour[index1]
    return mutated_tour

# Genetic algorithm
# Genetic algorithm
def genetic_algorithm(population_size, generations):
    population = [generate_random_tour() for _ in range(population_size)]
    
    for _ in range(generations):
        next_generation = []
        for _ in range(population_size):
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            if random.random() < 0.1:
                child1 = mutate(child1)
            if random.random() < 0.1:
                child2 = mutate(child2)
            next_generation.extend([child1, child2])
        
        population = sorted(next_generation, key=fitness)[:population_size]
    
    return population[0]


# Main function
if __name__ == "__main__":
    optimal_tour = genetic_algorithm(population_size=10, generations=100)
    print("Optimal Tour:", optimal_tour)