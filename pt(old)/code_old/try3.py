import random
import pandas as pd

# Load data from CSV files
travel_data = pd.read_csv('travel.csv')
place_data = pd.read_csv('places.csv')

# Extract city names from travel data
travel_data['Source_City'] = travel_data['Source'].str.extract(r'\((.*?)\)')
travel_data['Destination_City'] = travel_data['Destination'].str.extract(r'\((.*?)\)')

# Define chromosome representation
def generate_random_tour(city, max_time):
    places_within_time = place_data[place_data['TIME(HOURS)'] <= max_time]
    shuffled_indices = travel_data[(travel_data['Source_City'] == city) & (travel_data['Destination'].isin(places_within_time['PLACES']))].sample(frac=1).index
    return list(travel_data.loc[shuffled_indices, 'Source'])

# Define fitness function
def fitness(tour, max_time):
    total_time = 0
    total_cost = 0
    total_rating = 0
    
    for i in range(len(tour)-1):
        source = tour[i]
        destination = tour[i+1]
        route = travel_data[(travel_data['Source'] == source) & (travel_data['Destination'] == destination)]
        
        if not route.empty:
            total_time += route['Time(hrs)'].values[0]
            total_cost += route['Cost(Rs)'].values[0]
            total_rating += place_data.loc[place_data['PLACES'] == destination, 'RATINGS'].values[0]
        else:
            print(f"No route found from {source} to {destination}")
    
    # Penalize tours exceeding max_time
    if total_time < max_time:
        total_rating -= (total_time - max_time) * 0.1
            
    average_rating = total_rating / len(tour)
    return -total_time, -total_cost, average_rating

# Define genetic operators
def crossover(parent1, parent2, max_time):
    crossover_point = random.randint(1, len(parent1)-1)
    child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
    return child1, child2

def mutate(tour):
    mutated_tour = tour[:]
    index1, index2 = random.sample(range(len(tour)), 2)
    mutated_tour[index1], mutated_tour[index2] = mutated_tour[index2], mutated_tour[index1]
    return mutated_tour

# Define genetic algorithm
def genetic_algorithm(population_size, generations, city, max_time):
    population = [generate_random_tour(city, max_time) for _ in range(population_size)]
    
    for _ in range(generations):
        next_generation = []
        for _ in range(population_size):
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2, max_time)
            if random.random() < 0.1:
                child1 = mutate(child1)
            if random.random() < 0.1:
                child2 = mutate(child2)
            next_generation.extend([child1, child2])
        print(fitness(next_generation, max_time))
        population = sorted(next_generation, key=lambda x: fitness(x, max_time))[:population_size]
    
    return population[0]

# Define a function to calculate total time and average rating
def calculate_metrics(places):
    total_time = places['TIME(HOURS)'].sum()
    total_rating = places['RATINGS'].sum()
    average_rating = total_rating / len(places)
    return total_time, average_rating

# Define main function
def main():
    city = input("Enter the city you want to visit: ")
    choice = int(input("Enter 1 to find the optimal tour, 2 to view places for a city within a given period of time: "))
    
    if choice == 1:
        population_size = int(input("Enter population size: "))
        generations = int(input("Enter number of generations: "))
        max_time = float(input("Enter the maximum time you have (in hours): "))
        optimal_tour = genetic_algorithm(population_size, generations, city, max_time)
        print("Optimal Tour:", optimal_tour)
        
        # Calculate and print total time and average rating
        total_time, average_rating = calculate_metrics(optimal_tour)
        print("Total Time Taken:", total_time)
        print("Average Rating of Visited Places:", average_rating)
        
    elif choice == 2:
        max_time = float(input("Enter the maximum time you have (in hours): "))
        # Filter places based on city and maximum time
        filtered_places = place_data[(place_data['PLACES'].str.contains(city)) & (place_data['TIME(HOURS)'] <= max_time)]
        
        if filtered_places.empty:
            print("No places to visit within the given time in the specified city.")
        else:
            print("Places to visit within the given time in", city)
            print(filtered_places[['PLACES', 'TIME(HOURS)', 'RATINGS']])
            
            # Calculate and print total time and average rating
            total_time, average_rating = calculate_metrics(filtered_places)
            print("Total Time Taken:", total_time)
            print("Average Rating of Visited Places:", average_rating)
            
    else:
        print("Invalid choice. Please enter either 1 or 2.")

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
