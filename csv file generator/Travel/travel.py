import csv
import random
import time
import os
from collections import defaultdict

def read_places_data(filename):
    city_places = defaultdict(list)
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city_places[row['CITYNAME']].append(int(row['PLACES_ID']))
    return city_places

def generate_travel_data(city_places):
    travel_data = []
    for city, nodes in city_places.items():
        n = len(nodes)
        for i in range(n):
            for j in range(i + 1, n):
                time_hrs = round(random.uniform(1, 8), 2)  # Time between 1 to 8 hours
                cost_rs = random.randint(10, 500)  # Cost between 10 to 500 Rs
                travel_data.append([nodes[i], nodes[j], time_hrs, cost_rs])
    # Fixed routes with specified data
    travel_data.append([1, 129, 0.65, 145])
    travel_data.append([129, 257, 6.5, 800])
    travel_data.append([257, 385, 13, 1240])
    return travel_data

def write_travel_data(folder_path, filename, travel_data):
    # Ensure the directory exists
    os.makedirs(folder_path, exist_ok=True)
    full_path = os.path.join(folder_path, filename)
    with open(full_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Source', 'Destination', 'Time(hrs)', 'Cost(Rs)'])
        writer.writerows(travel_data)

def main():
    start_time = time.time()
    output_folder = 'output_files'
    places_data = read_places_data('places.csv')
    for i in range(1, 101):  # Loop to create 100 CSV files
        travel_data = generate_travel_data(places_data)
        filename = f'travel{i}.csv'
        write_travel_data(output_folder, filename, travel_data)
        print(f"{filename} created in folder '{output_folder}'.")
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds")

if __name__ == '__main__':
    main()
