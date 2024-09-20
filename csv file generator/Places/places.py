import csv
import random
import time
import os

# Parameters for data generation
cities = ["Bhubaneswar", "Cuttack", "Kolkata", "Visakhapatnam"]
num_places_per_city = 5
rating_range = (1, 5)
time_range = (1, 10)
cost_range = (10, 1000)


# Function to generate random data for one city
def generate_city_data(city, s):
    data = []
    for i in range(s, s + num_places_per_city):
        place_id = i
        rating = random.uniform(*rating_range)
        time_hours = random.uniform(*time_range)
        cost = random.randint(*cost_range)
        data.append([city, place_id, round(rating, 1), round(time_hours, 1), cost])
    return data


def main():
    output_folder = "output_files"  # Specify the folder to store CSV files
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create folder if it does not exist

    start_time = time.time()  # Start timing the process
    for file_number in range(1, 101):  # Generate 100 files
        start = 1  # Reset start for each file
        all_data = []
        for city in cities:
            all_data.extend(generate_city_data(city, start))
            start += num_places_per_city  # Increment start for each city

        # Generate file name dynamically and include the folder path
        file_name = f"{output_folder}/place{file_number}.csv"
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["CITYNAME", "PLACES_ID", "RATINGS", "TIME(HOURS)", "COST"])
            writer.writerows(all_data)
        print(f"{file_name} has been created with random data.")

    end_time = time.time()  # End timing the process
    print(
        f"Total execution time: {end_time - start_time:.2f} seconds"
    )  # Print total execution time


if __name__ == "__main__":
    main()
