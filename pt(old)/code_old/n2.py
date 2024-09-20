import random
import pandas as pd

# Load data from CSV files
travel_data = pd.read_csv("travel.csv")
place_data = pd.read_csv("places.csv")

# Merge travel data with destination place data
merged_data = pd.merge(
    travel_data, place_data, left_on="Destination", right_on="PLACES"
)
def save_merged_data_to_csv(filename="merged_data.csv"):
    merged_data.to_csv(filename, index=False)
    print(f"Merged data saved to {filename}")

# Pre-process data for efficient lookup
lookup_table = {}
for index, row in merged_data.iterrows():
    key = (row["Source"], row["Destination"])
    value = (row["Time(hrs)"], row["Cost(Rs)"], row["RATINGS"])
    lookup_table[key] = value


# Define chromosome representation
def generate_random_tour(starting_city):
    tour = [place for place in merged_data.loc[merged_data['Source'].str.contains(starting_city), 'Source']]
    while True:
        next_destinations = merged_data.loc[merged_data['Source'] == tour[-1], 'Destination'].values
        if len(next_destinations) == 0:
            break  # No destinations available
        next_destination = random.choice(next_destinations)
        if next_destination.split('(')[-1].strip(')') == starting_city:
            break
        if next_destination not in tour:
            tour.append(next_destination)
    return tour



# Define fitness function
def fitness(tour):
    total_time, total_cost, total_rating = 0, 0, 0
    for i in range(len(tour) - 1):
        source, destination = tour[i], tour[i + 1]
        key = (source, destination)
        if key in lookup_table:
            time, cost, rating = lookup_table[key]
            total_time += time
            total_cost += cost
            total_rating += rating
    average_rating = total_rating / len(tour)
    return -total_time, -total_cost, average_rating


# Define genetic operators
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + [
        gene for gene in parent2 if gene not in parent1[:crossover_point]
    ]
    child2 = parent2[:crossover_point] + [
        gene for gene in parent1 if gene not in parent2[:crossover_point]
    ]
    return child1, child2


def mutate(tour):
    index1, index2 = random.sample(range(len(tour)), 2)
    tour[index1], tour[index2] = tour[index2], tour[index1]
    return tour


# Genetic algorithm with time constraint
def genetic_algorithm(total_available_time, starting_city):
    tour = generate_random_tour(starting_city)
    population_size = len(tour)
    population = [tour[:] for _ in range(population_size)]
    current_generation = 0

    while True:
        current_generation += 1
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

        # Check if the best tour exceeds the time constraint
        best_tour = population[0]
        total_time = sum(
            lookup_table[(best_tour[i], best_tour[i + 1])][0]
            for i in range(len(best_tour) - 1)
        )
        if total_time <= total_available_time:
            break

        # Adjust the tour if it exceeds the time constraint
        adjusted_tour = adjust_tour(best_tour, total_available_time)
        population[0] = adjusted_tour

    return best_tour, current_generation


# Function to adjust the tour to meet the time constraint
def adjust_tour(tour, total_available_time):
    adjusted_tour = tour[:]
    while True:
        total_time = sum(
            lookup_table[(adjusted_tour[i], adjusted_tour[i + 1])][0]
            for i in range(len(adjusted_tour) - 1)
        )
        if total_time <= total_available_time:
            break
        # Remove the destination with the highest individual time
        destination_to_remove = max(
            adjusted_tour[1:-1],
            key=lambda x: lookup_table[(x, adjusted_tour[adjusted_tour.index(x) + 1])][
                0
            ],
        )
        adjusted_tour.remove(destination_to_remove)
    return adjusted_tour


# Main function
if __name__ == "__main__":
    save_merged_data_to_csv()
    starting_city = input("Enter the city name: ")
    
    while True:
        total_available_time_input = input("Enter total available time (in hours): ")
        try:
            total_available_time = float(total_available_time_input)
            break  # Break the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    optimal_tour, generations = genetic_algorithm(total_available_time, starting_city)
    print("Optimal Tour:", optimal_tour)
    print("Number of Generations:", generations)

