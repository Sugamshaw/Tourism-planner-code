import pandas as pd
import numpy as np
from deap import creator, base, tools, algorithms


# Load travel data from a CSV file
def load_data(filename):
    return pd.read_csv(filename)


# Extract city names and create a mapping to indices
def prepare_city_index_mapping(df):
    unique_locations = pd.unique(df[["Source", "Destination"]].values.ravel("K"))
    return {city: i for i, city in enumerate(unique_locations)}


# Create matrices for time and cost based on the provided data
def create_distance_matrix(df, cities_index):
    n = len(cities_index)
    time_matrix = np.full((n, n), np.inf)  # Initialize with infinite
    cost_matrix = np.full((n, n), np.inf)

    for _, row in df.iterrows():
        i = cities_index[row["Source"]]
        j = cities_index[row["Destination"]]
        time_matrix[i][j] = row["Time(hrs)"]
        cost_matrix[i][j] = row["Cost(Rs)"]

    return time_matrix, cost_matrix


# Global evaluation function for the GA
def eval_tsp(individual, time_matrix, cost_matrix, max_time, max_cost):
    # Calculate the travel time and cost for the route
    time_total = 0.0
    cost_total = 0.0
    num_cities = len(individual)
    # Loop through each city in the individual route
    for i in range(num_cities):
        next_city = individual[
            (i + 1) % num_cities
        ]  # Wrap around to start for the return trip
        time_total += time_matrix[individual[i]][next_city]
        cost_total += cost_matrix[individual[i]][next_city]

    # If total time or cost exceeds the constraints, apply a very high penalty
    if time_total > max_time or cost_total > max_cost:
        return 1e6, 1e6  # Penalize tours that exceed constraints

    return time_total, cost_total


# Setup the genetic algorithm using DEAP
def setup_ga(
    time_matrix,
    cost_matrix,
    max_time,
    max_cost,
    population_size=50,
    num_generations=100,
):
    creator.create(
        "FitnessMulti", base.Fitness, weights=(-1.0, -1.0)
    )  # Minimize time and cost
    creator.create("Individual", list, fitness=creator.FitnessMulti)

    toolbox = base.Toolbox()
    num_cities = len(time_matrix)
    toolbox.register("indices", np.random.permutation, num_cities)
    toolbox.register(
        "individual", tools.initIterate, creator.Individual, toolbox.indices
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register(
        "evaluate",
        eval_tsp,
        time_matrix=time_matrix,
        cost_matrix=cost_matrix,
        max_time=max_time,
        max_cost=max_cost,
    )
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selNSGA2)

    pop = toolbox.population(n=population_size)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    algorithms.eaSimple(
        pop,
        toolbox,
        cxpb=0.7,
        mutpb=0.2,
        ngen=num_generations,
        stats=stats,
        halloffame=hof,
        verbose=True,
    )

    return pop, stats, hof


# Main function to run the genetic algorithm
def main(city, max_time, max_cost):
    df = load_data("travel.csv")
    cities_index = prepare_city_index_mapping(df)
    time_matrix, cost_matrix = create_distance_matrix(df, cities_index)

    # Run the genetic algorithm
    population, stats, hof = setup_ga(time_matrix, cost_matrix, max_time, max_cost)

    # Extract best routes and their fitness values
    best_routes = []
    for individual in hof:
        route = [list(cities_index.keys())[i] for i in individual]
        total_time, total_cost = eval_tsp(
            individual, time_matrix, cost_matrix, max_time, max_cost
        )
        best_routes.append((route, total_time, total_cost))

    return best_routes


# Example usage
if __name__ == "__main__":
    city = "Bhubaneswar"
    max_time = 5  # hours
    max_cost = 1000  # Rs
    best_routes = main(city, max_time, max_cost)
    print("Best Routes:")
    for route, time, cost in best_routes:
        route_str = " -> ".join(route)
        print(f"Route: {route_str}\nTime: {time:.2f} hours, Cost: {cost:.2f} Rs\n")
