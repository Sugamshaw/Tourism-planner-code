import csv
import random
import time
import os
from geopy.geocoders import Nominatim
from geopy import distance
import requests
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Parameters for data generation
# cities = ["Bhubaneswar", "Kolkata", "Delhi", "Mumbai"]
file_name = "final_places1.csv"
# cities = ["Kolkata"]
cities = [
    "Agra", "Jaipur", "Udaipur", "Varanasi", "Amritsar",  # Historic and cultural gems
    "Goa", "Manali", "Leh", "Darjeeling", "Shimla",  # Popular tourist destinations
    "Kochi", "Thiruvananthapuram", "Pondicherry", "Mysore", "Madurai",  # Cultural and coastal attractions
    "Mumbai", "Delhi", "Kolkata", "Chennai", "Bangalore",  # Major metro areas
    "Hyderabad", "Ahmedabad", "Pune", "Chandigarh", "Bhubaneswar",  # Other significant urban centers
    "Srinagar", "Haridwar", "Rishikesh", "Gangtok", "Guwahati",  # Spiritual and scenic spots
    "Dehradun", "Jaisalmer", "Mount Abu", "Lucknow", "Kanpur",  # Blend of history and culture
    "Nagpur", "Indore", "Patna", "Bhopal", "Ludhiana"  # Additional regional hubs
]

num_places_per_city = 127
rating_range = (1, 5)
time_range = (1, 10)
cost_range = (10, 1000)


def safe_geocode(geocoder, query, attempt=1, max_attempts=5):
    try:
        return geocoder.geocode(query)
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        if attempt <= max_attempts:
            time.sleep(2**attempt)  # Exponential backoff
            return safe_geocode(geocoder, query, attempt + 1, max_attempts)
        else:
            print(f"Geocoding failed after {max_attempts} attempts.")
            return None


def get_city_bbox(city_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city_name, exactly_one=True)
    if location:
        return location.raw["boundingbox"]
    else:
        return None


def latlong(location, city):
    geocoder = Nominatim(user_agent="sugamnew")
    full_query = f"{location}, {city}"
    coordinates = safe_geocode(geocoder, full_query)
    if coordinates:
        return coordinates.latitude, coordinates.longitude
    return None, None


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
    a = num_places_per_city
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
            latitude, longitude = latlong(element["tags"]["name"], city_name)
            if latitude != None and longitude != None:
                a -= 1
                attractions.append(
                    [element["tags"]["name"], tag_description, latitude, longitude]
                )
                if a == 0:
                    return len(attractions)
    return len(attractions)

for i in range(len(cities)):
    start=time.time()
    print(cities[i], " : ", get_tourist_attractions(cities[i]))
    end=time.time()
    print(end-start)

