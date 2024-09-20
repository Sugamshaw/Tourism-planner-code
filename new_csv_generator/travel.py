import csv
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from collections import defaultdict

# Initializing the geocoder and dictionary to store location data
geocoder = Nominatim(user_agent="sarang")
idtoinfo = defaultdict(list)

# Reading location data
with open("final_places.csv", 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header
    count = 0
    for row in reader:
        count += 1
        place_id, city_name, place_name, tag, latitude, longitude, rating, time, cost = row
        place_id = int(place_id)  # Assuming place_id is integer and sequentially ordered
        latitude, longitude = float(latitude), float(longitude)
        idtoinfo[place_id] = (latitude, longitude)  # Storing as a tuple for easy access

# Constants for calculation
cost_multiplier = 30
time_multiplier = 1.5

# Writing the travel information to a new CSV
with open("travel.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    header = ["source", "destination", "cost", "time"]
    writer.writerow(header)
    
    for i in range(1, count + 1):
        if i not in idtoinfo:
            continue
        source_latitude, source_longitude = idtoinfo[i]
        
        for j in range(i + 1, count + 1):
            if j not in idtoinfo:
                continue
            dest_latitude, dest_longitude = idtoinfo[j]
            
            distance_km = geodesic((source_latitude, source_longitude), (dest_latitude, dest_longitude)).kilometers
            travel_cost = int(distance_km * cost_multiplier)
            travel_time = distance_km * time_multiplier
            
            writer.writerow([i, j, travel_cost, travel_time])
