import csv
from collections import Counter


def print_frequencies(my_list):
    frequencies = Counter(my_list)
    for key, value in frequencies.items():
        print(f"{key}: {value}")


def read_places_data(filename):
    city_places = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            city_places.append(int(row["Source"]))
            city_places.append(int(row["Destination"]))
    print_frequencies(city_places)


# Assuming the filename is 'travel.csv' and it is in the correct format as described.
places_data = read_places_data("travel.csv")
