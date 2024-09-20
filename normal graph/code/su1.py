import pandas as pd
import numpy as np
import random
import tkinter as tk
from tkinter import simpledialog
from deap import base, creator, tools, algorithms

# Load and merge data safely
try:
    travel_data = pd.read_csv("travel.csv")
    places_data = pd.read_csv("places.csv", index_col="PLACES")
    merged_data = pd.merge(
        travel_data, places_data, left_on="Destination", right_index=True, how="left"
    )
except FileNotFoundError:
    print("Error: One or more data files are missing.")
    exit()

def extract_city_name(place):
    """Extracts the city name from a place name formatted as 'Place(City)'"""
    return place.split("(")[-1].strip(")")

# Define railway stations for each city
city_to_railways = {
    "Bhubaneswar": "Bhubaneswar Railway Station(Bhubaneswar)",
    "Cuttack": "Cuttack Junction Railway Station(Cuttack)",
    "Kolkata": "Howrah Junction Railway Station(Kolkata)",
    "Visakhapatnam": "Visakhapatnam Railway Station(Visakhapatnam)",
}

# User Interface for input
def gui_input():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    city = simpledialog.askstring("Input", "Enter the city:", parent=root)
    root.destroy()
    return city

city = gui_input()
if city is None or city not in city_to_railways:
    print("Invalid city or city not available.")
    exit()

starting_station = city_to_railways[city]
places_in_city = [place for place in places_data.index if extract_city_name(place) == city]

# Setup for DEAP library
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)
toolbox = base.Toolbox()

# Example mapping of place names to indices
place_to_index = {name: idx for idx, name in enumerate(sorted(set(merged_data['Destination'])))}

# Function to convert an individual's places to indices
def convert_to_indices(individual):
    return [place_to_index[place] for place in individual if place in place_to_index]

# Adjust how individuals are created
def create_individual():
    places_indices = convert_to_indices([starting_station] + places_in_city + [starting_station])
    random.shuffle(places_indices)
    return places_indices

# Register the new individual creation function
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def eval_tour(individual):
    total_time, total_cost, total_ratings = 0, 0, 0
    for i in range(len(individual) - 1):
        row = merged_data[
            (merged_data["Source"] == individual[i]) & 
            (merged_data["Destination"] == individual[i + 1])
        ]
        if not row.empty:
            total_time += row.iloc[0]["Time(hrs)"]
            total_cost += row.iloc[0]["Cost(Rs)"]
            total_ratings += places_data.loc[individual[i + 1], "RATINGS"]
        else:
            total_time += 9999  # Penalty for missing routes
            total_cost += 9999  # Penalty for missing routes

    return total_time, total_cost, total_ratings

toolbox.register("evaluate", eval_tour)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selNSGA2)

def main():
    random.seed(64)
    NGEN = 50
    MU = 50
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    algorithms.eaMuPlusLambda(
        pop, toolbox, mu=MU, lambda_=LAMBDA, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN,
        stats=stats, halloffame=hof, verbose=True
    )

    # Print the best tour and their fitness
    for ind in hof:
        print("Tour:", ind)
        print("Fitness:", ind.fitness.values)

    return pop, stats, hof

if __name__ == "__main__":
    main()
