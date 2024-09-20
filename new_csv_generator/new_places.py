import csv
import random
import time
import os
from geopy.geocoders import Nominatim
from geopy import distance
import requests


# Parameters for data generation
# cities = ["Bhubaneswar", "Kolkata", "Delhi", "Mumbai"]
file_name="final_places1.csv"
cities = ["Kolkata"]
num_places_per_city = 50
rating_range = (1, 5)
time_range = (1, 10)
cost_range = (10, 1000)


def get_city_bbox(city_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city_name, exactly_one=True)
    if location:
        return location.raw["boundingbox"]
    else:
        return None

def latlong(location, city):
    geocoder = Nominatim(user_agent="sugam")
    full_query = f"{location}, {city}"  # Adds city to the query
    coordinates = geocoder.geocode(full_query)
    if coordinates is None:
        return None, None
    lat, long = coordinates.latitude, coordinates.longitude
    return lat, long

def get_tourist_attractions(city_name):
    bbox = get_city_bbox(city_name)
    if not bbox:
        print("City not found.")
        return

    # Convert bounding box to Overpass API format
    south, north, west, east = bbox[0], bbox[1], bbox[2], bbox[3]
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["tourism"="attraction"]({south},{west},{north},{east});
      way["tourism"="attraction"]({south},{west},{north},{east});
      relation["tourism"="attraction"]({south},{west},{north},{east});

      node["tourism"="museum"]({south},{west},{north},{east});
      way["tourism"="museum"]({south},{west},{north},{east});
      relation["tourism"="museum"]({south},{west},{north},{east});

      node["historic"="monument"]({south},{west},{north},{east});
      way["historic"="monument"]({south},{west},{north},{east});
      relation["historic"="monument"]({south},{west},{north},{east});

      node["historic"="castle"]({south},{west},{north},{east});
      way["historic"="castle"]({south},{west},{north},{east});
      relation["historic"="castle"]({south},{west},{north},{east});

      node["tourism"="gallery"]({south},{west},{north},{east});
      way["tourism"="gallery"]({south},{west},{north},{east});
      relation["tourism"="gallery"]({south},{west},{north},{east});

      node["tourism"="zoo"]({south},{west},{north},{east});
      way["tourism"="zoo"]({south},{west},{north},{east});
      relation["tourism"="zoo"]({south},{west},{north},{east});

      node["leisure"="park"]({south},{west},{north},{east});
      way["leisure"="park"]({south},{west},{north},{east});
      relation["leisure"="park"]({south},{west},{north},{east});

      node["leisure"="garden"]({south},{west},{north},{east});
      way["leisure"="garden"]({south},{west},{north},{east});
      relation["leisure"="garden"]({south},{west},{north},{east});

      node["tourism"="viewpoint"]({south},{west},{north},{east});
      way["tourism"="viewpoint"]({south},{west},{north},{east});
      relation["tourism"="viewpoint"]({south},{west},{north},{east});

      node["natural"="beach"]({south},{west},{north},{east});
      way["natural"="beach"]({south},{west},{north},{east});
      relation["natural"="beach"]({south},{west},{north},{east});
    );
    out body;
    >;
    out skel qt;
    """

    response = requests.get(overpass_url, params={"data": overpass_query})
    data = response.json()

    attractions = []
    for element in data["elements"]:
        if "tags" in element and "name" in element["tags"]:
            tag_description = " or ".join(
                [
                    tag
                    for tag, value in element["tags"].items()
                    if value
                    in [
                        "attraction",
                        "museum",
                        "monument",
                        "castle",
                        "gallery",
                        "zoo",
                        "park",
                        "garden",
                        "viewpoint",
                        "beach",
                    ]
                ]
            )
            
            attractions.append([element["tags"]["name"], tag_description])
    return attractions





# Function to generate random data for one city
def generate_city_data(city, s):
    data = []
    places_data = get_tourist_attractions(city)
    a=0
    e=num_places_per_city
    for i in range(0, e):
        print(i," ",places_data[i][0])
        latitude, longitude = latlong(places_data[i][0], city)
        if latitude == None:
            e+=1
            continue
        a+=1
        place_id = a + s
        #    ["PLACES_ID","CITYNAME","PLACE_NAME","TAG","latitude","longitude", "RATINGS", "TIME(HOURS)", "COST"])
        data.append(
            [
                place_id,
                city,
                places_data[i][0],
                places_data[i][1],
                latitude,
                longitude,
                round(random.uniform(*rating_range), 1),
                round(random.uniform(*time_range), 1),
                random.randint(*cost_range)
            ]
        )
    print("dd")
    return data


def main():
    # output_folder = "output_files"  # Specify the folder to store CSV files
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)  # Create folder if it does not exist

    start_time = time.time()
    start = 1
    all_data = []
    for city in cities:
        lat,long=latlong(city+" Station", city)
        all_data.append([
                start,
                city,
                city+" Station",
                "Station",
                lat,
                long,
                round(random.uniform(*rating_range), 1),
                round(random.uniform(*time_range), 1),
                random.randint(*cost_range)
            ]
            )
        start+=1
        all_data.extend(generate_city_data(city, start))
        start += num_places_per_city
    
    with open(file_name, "w", newline="", encoding='utf-8') as file:
        file.flush()
        writer = csv.writer(file)
        writer.writerow(
            [
                "PLACES_ID",
                "CITYNAME",
                "PLACE_NAME",
                "TAG",
                "latitude",
                "longitude",
                "RATINGS",
                "TIME(HOURS)",
                "COST",
            ]
        )

        writer.writerows(all_data)
        file.flush()
    print(f"{file_name} has been created.")

    end_time = time.time()  # End timing the process
    print(
        f"Total execution time: {end_time - start_time:.2f} seconds"
    )  # Print total execution time


if __name__ == "__main__":
    main()
