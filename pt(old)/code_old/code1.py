import pandas as pd
import numpy as np
from deap import base, creator, tools, algorithms
import random

def load_data(filename):
    df = pd.read_csv(filename)
    df[['Source', 'Source City']] = df['Source'].str.extract(r'(.+)\((.+)\)')
    df[['Destination', 'Destination City']] = df['Destination'].str.extract(r'(.+)\((.+)\)')
    return df

def create_city_graphs(df):
    cities = df['Source City'].unique()
    city_graphs = {}
    for city in cities:
        # Ensure all unique attractions are included, both as sources and destinations
        attractions = np.unique(df[df['Source City'] == city][['Source', 'Destination']].values)
        size = len(attractions)
        cost_matrix = np.full((size, size), np.inf)
        time_matrix = np.full((size, size), np.inf)
        attraction_index = {attraction: idx for idx, attraction in enumerate(attractions)}

        # Filter rows relevant to the current city
        subset = df[(df['Source City'] == city) & (df['Destination City'] == city)]
        for _, row in subset.iterrows():
            src_idx = attraction_index[row['Source']]
            dest_idx = attraction_index[row['Destination']]
            time_matrix[src_idx][dest_idx] = row['Time(hrs)']
            cost_matrix[src_idx][dest_idx] = row['Cost(Rs)']

        city_graphs[city] = (attractions, time_matrix, cost_matrix, attraction_index)
    return city_graphs

# Define the DEAP fitness and individual classes
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

def create_individual(city_graph):
    attractions = city_graph[0]
    individual = list(attractions)
    random.shuffle(individual)
    return creator.Individual(individual)

def evaluate(individual, city_graph):
    index_map = city_graph[3]
    time_matrix = city_graph[1]
    cost_matrix = city_graph[2]
    
    total_time = 0
    total_cost = 0
    for i in range(len(individual) - 1):
        src = index_map[individual[i]]
        dest = index_map[individual[i + 1]]
        total_time += time_matrix[src][dest]
        total_cost += cost_matrix[src][dest]
    return total_time, total_cost

def setup_toolbox(city_graph):
    toolbox = base.Toolbox()
    toolbox.register("individual", create_individual, city_graph)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=50)
    toolbox.register("evaluate", evaluate, city_graph)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selNSGA2)
    return toolbox

# Assuming the main section of the code handles setup and running the GA as previously described
# Genetic Algorithm Run Function
def run_ga(toolbox, max_generations=100, population_size=50, cxpb=0.7, mutpb=0.2):
    population = toolbox.population(n=population_size)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + stats.fields

    for gen in range(max_generations):
        offspring = algorithms.varAnd(population, toolbox, cxpb=cxpb, mutpb=mutpb)
        fits = map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        record = stats.compile(population)
        logbook.record(gen=gen, nevals=len(offspring), **record)
        print(logbook.stream)

    return tools.sortNondominated(population, len(population), first_front_only=True)

# Main program allowing user input for customization
if __name__ == "__main__":
    df = load_data('travel.csv')
    city_graphs = create_city_graphs(df)

    # User input for city, time, and cost constraints
    city = input("Enter the city for the tour: ")
    max_time = float(input("Enter maximum allowable total time for the tour (in hours): "))
    max_cost = float(input("Enter maximum allowable total cost for the tour (in Rs): "))

    if city in city_graphs:
        toolbox = setup_toolbox(city_graphs[city])
        result = run_ga(toolbox)
        print("Optimal Tours Found:")
        for ind in result[0]:
            time, cost = ind.fitness.values
            if time <= max_time and cost <= max_cost:
                print("Tour: {}, Time: {:.2f}h, Cost: Rs{:.2f}".format(ind, time, cost))
            else:
                print("No tours found within the specified constraints.")
    else:
        print(f"No data available for the city: {city}")
