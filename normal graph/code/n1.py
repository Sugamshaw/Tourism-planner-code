import random
import pandas as pd

# Load data from CSV files
travel_data = pd.read_csv("travel.csv")
place_data = pd.read_csv("places.csv")
travel_data["Source_City"] = travel_data["Source"].str.extract(r"\((.*?)\)")
travel_data["Destination_City"] = travel_data["Destination"].str.extract(r"\((.*?)\)")

# Merge travel data with destination place data
merged_data = pd.merge(
    travel_data, place_data, left_on="Destination", right_on="PLACES"
)



# Define chromosome representation
def generate_random_tour(city, max_time):
    places_within_time = place_data[place_data["TIME(HOURS)"] <= max_time]
    shuffled_indices = (
        travel_data[
            (travel_data["Source_City"] == city)
            & (travel_data["Destination"].isin(places_within_time["PLACES"]))
        ]
        .sample(frac=1)
        .index
    )
    return list(travel_data.loc[shuffled_indices, "Source"])


# Define fitness function
def fitness(tour):
    total_time = 0
    total_cost = 0
    total_rating = 0
    for i in range(len(tour) - 1):
        source = tour[i]
        destination = tour[i + 1]
        try:
            # Calculate total time
            travel_time = merged_data.loc[
                (merged_data["Source"] == source)
                & (merged_data["Destination"] == destination),
                "Time(hrs)",
            ].values[0]
            destination_time = merged_data.loc[
                merged_data["PLACES"] == destination, "TIME(HOURS)"
            ].values[0]
            total_time += travel_time + destination_time
            # Calculate total cost
            travel_cost = merged_data.loc[
                (merged_data["Source"] == source)
                & (merged_data["Destination"] == destination),
                "Cost(Rs)",
            ].values[0]
            destination_cost = merged_data.loc[
                merged_data["PLACES"] == destination, "COST"
            ].values[0]
            total_cost += travel_cost + destination_cost
            # Calculate total rating
            destination_rating = merged_data.loc[
                merged_data["PLACES"] == destination, "RATINGS"
            ].values[0]
            total_rating += destination_rating
        except IndexError:
            # Handle cases where the DataFrame indexing results in an empty DataFrame or missing values
            pass
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
    mutated_tour = tour[:]
    index1, index2 = random.sample(range(len(tour)), 2)
    mutated_tour[index1], mutated_tour[index2] = (
        mutated_tour[index2],
        mutated_tour[index1],
    )
    return mutated_tour


# Genetic algorithm with time constraint
def genetic_algorithm(total_available_time, starting_city):

    tour = generate_random_tour(starting_city, total_available_time)
    population_size = len(
        tour
    )  # Adjust population size based on the length of the tour
    population = [
        tour[:] for _ in range(population_size)
    ]  # Create population with copies of the tour

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
        total_time = 10
        total_time = sum(merged_data.loc[(merged_data["Source"] == best_tour[i])& (merged_data["Destination"] == best_tour[i + 1]),"Time(hrs)",
            ].values[0]
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
            merged_data.loc[
                (merged_data["Source"] == adjusted_tour[i])
                & (merged_data["Destination"] == adjusted_tour[i + 1]),
                "Time(hrs)",
            ].values[0]
            for i in range(len(adjusted_tour) - 1)
        )
        if total_time <= total_available_time:
            break
        # Remove the destination with the highest individual time
        destination_to_remove = max(
            adjusted_tour[1:-1],
            key=lambda x: merged_data.loc[
                merged_data["PLACES"] == x, "TIME(HOURS)"
            ].values[0],
        )
        adjusted_tour.remove(destination_to_remove)
    return adjusted_tour


# Main function
if __name__ == "__main__":
    starting_city = input("Enter the city name: ")
    # print(merged_data.columns)

    while True:
        total_available_time_input = input("Enter total available time (in hours): ")
        try:
            total_available_time = float(total_available_time_input)
            break  # Break the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    optimal_tour, generations = genetic_algorithm(total_available_time, starting_city)
    print("Optimal Tour:", optimal_tour)
    print(
        "Total Time:",
        sum(
            merged_data.loc[
                (merged_data["Source"] == optimal_tour[i])
                & (merged_data["Destination"] == optimal_tour[i + 1]),
                "Time(hrs)",
            ].values[0]
            for i in range(len(optimal_tour) - 1)
        ),
    )
    print(
        "Total Cost:",
        sum(
            merged_data.loc[
                (merged_data["Source"] == optimal_tour[i])
                & (merged_data["Destination"] == optimal_tour[i + 1]),
                "Cost(Rs)",
            ].values[0]
            for i in range(len(optimal_tour) - 1)
        ),
    )
    print(
        "Average Rating:",
        sum(
            merged_data.loc[merged_data["PLACES"] == x, "RATINGS"].values[0]
            for x in optimal_tour
        )
        / len(optimal_tour),
    )
    print("Number of Generations:", generations)
