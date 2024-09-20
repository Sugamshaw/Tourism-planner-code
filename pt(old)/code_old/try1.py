# Given a set of cities of a state. Provide the optimal tour guidance to the visitors.
# The trip preferences include the distance between the cities and the time taken
# to complete the city, its rating needs to be considered while providing a plan.
# There may be multiple modes available to reach the same destination.
# You need to find the optimal plan which contains the least travel time,
# least cost, least money, but covering highly rated places. This is multiple objective optimization.

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


save_merged_data_to_csv()
# tour = [
#     place
#     for place in merged_data.loc[
#         merged_data["Source"].str.contains("Bhubaneswar"), "Source"
#     ]
# ]
# next_destinations = merged_data.loc[
#     merged_data["Source"] == tour[-1], "Destination"
# ].values
# print(tour)
# print(next_destinations)


def generate_random_tour(starting_city):
    tour = [
        place
        for place in merged_data.loc[
            merged_data["Source"].str.contains(starting_city), "Source"
        ]
    ]
    # print("important tour : ", tour)
    while True:
        next_destinations = merged_data.loc[
            merged_data["Source"] == tour[-1], "Destination"
        ].values
        if len(next_destinations) == 0:
            break  # No destinations available
        next_destination = random.choice(next_destinations)
        # print("next_destination : ", next_destination)
        
        
        if next_destination.split("(")[-1].strip(")") == starting_city:
            # print("next_destination : ", next_destination.split("(")[-1].strip(")"))
            break
        if next_destination not in tour:
            tour.append(next_destination)
    return tour


t = generate_random_tour("Bhubaneswar")
shuffled_indices = merged_data.sample(frac=1).index
l=list(merged_data.loc[shuffled_indices, 'PLACES'])
print(len(set(l)))
for i in set(l):
    print(i)
# tour = generate_random_tour("Bhubaneswar")
# population_size = len(tour)
# population = [
#         tour[:] for _ in range(population_size)
#     ]
# print(population)
