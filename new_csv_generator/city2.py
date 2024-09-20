import requests
from geopy.geocoders import Nominatim


def get_city_bbox(city_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city_name, exactly_one=True)
    if location:
        return location.raw["boundingbox"]
    else:
        return None


def get_tourist_attractions(city_name):
    bbox = get_city_bbox(city_name)
    if not bbox:
        print("City not found.")
        return

    # Convert bounding box to Overpass API format
    south, north, west, east = bbox[0], bbox[1], bbox[2], bbox[3]
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
[out:json][timeout:50];
(
  // Cultural and Historical Sites
  node["tourism"="attraction"]({south},{west},{north},{east});
  way["tourism"="attraction"]({south},{west},{north},{east});
  relation["tourism"="attraction"]({south},{west},{north},{east});
      
  node["historic"="castle"]({south},{west},{north},{east});
  way["historic"="castle"]({south},{west},{north},{east});
  relation["historic"="castle"]({south},{west},{north},{east});

  node["historic"="church"]({south},{west},{north},{east});
  way["historic"="church"]({south},{west},{north},{east});
  relation["historic"="church"]({south},{west},{north},{east});

  node["historic"="ruins"]({south},{west},{north},{east});
  way["historic"="ruins"]({south},{west},{north},{east});
  relation["historic"="ruins"]({south},{west},{north},{east});

  node["historic"="memorial"]({south},{west},{north},{east});
  way["historic"="memorial"]({south},{west},{north},{east});
  relation["historic"="memorial"]({south},{west},{north},{east});

  node["cultural"="theatre"]({south},{west},{north},{east});
  way["cultural"="theatre"]({south},{west},{north},{east});
  relation["cultural"="theatre"]({south},{west},{north},{east});

  node["cultural"="opera_house"]({south},{west},{north},{east});
  way["cultural"="opera_house"]({south},{west},{north},{east});
  relation["cultural"="opera_house"]({south},{west},{north},{east});

  node["cultural"="gallery"]({south},{west},{north},{east});
  way["cultural"="gallery"]({south},{west},{north},{east});
  relation["cultural"="gallery"]({south},{west},{north},{east});

  node["cultural"="museum"]({south},{west},{north},{east});
  way["cultural"="museum"]({south},{west},{north},{east});
  relation["cultural"="museum"]({south},{west},{north},{east});

  node["tourism"="artwork"]({south},{west},{north},{east});
  way["tourism"="artwork"]({south},{west},{north},{east});
  relation["tourism"="artwork"]({south},{west},{north},{east});

  // Leisure and Recreation
  node["leisure"="park"]({south},{west},{north},{east});
  way["leisure"="park"]({south},{west},{north},{east});
  relation["leisure"="park"]({south},{west},{north},{east});

  node["leisure"="garden"]({south},{west},{north},{east});
  way["leisure"="garden"]({south},{west},{north},{east});
  relation["leisure"="garden"]({south},{west},{north},{east});

  node["leisure"="water_park"]({south},{west},{north},{east});
  way["leisure"="water_park"]({south},{west},{north},{east});
  relation["leisure"="water_park"]({south},{west},{north},{east});

  node["leisure"="theme_park"]({south},{west},{north},{east});
  way["leisure"="theme_park"]({south},{west},{north},{east});
  relation["leisure"="theme_park"]({south},{west},{north},{east});

  node["leisure"="marina"]({south},{west},{north},{east});
  way["leisure"="marina"]({south},{west},{north},{east});
  relation["leisure"="marina"]({south},{west},{north},{east});

  node["leisure"="golf_course"]({south},{west},{north},{east});
  way["leisure"="golf_course"]({south},{west},{north},{east});
  relation["leisure"="golf_course"]({south},{west},{north},{east});

  node["leisure"="sports_centre"]({south},{west},{north},{east});
  way["leisure"="sports_centre"]({south},{west},{north},{east});
  relation["leisure"="sports_centre"]({south},{west},{north},{east});

  // Natural Attractions
  node["natural"="peak"]({south},{west},{north},{east});
  way["natural"="peak"]({south},{west},{north},{east});
  relation["natural"="peak"]({south},{west},{north},{east});

  node["natural"="waterfall"]({south},{west},{north},{east});
  way["natural"="waterfall"]({south},{west},{north},{east});
  relation["natural"="waterfall"]({south},{west},{north},{east});

  node["natural"="cave_entrance"]({south},{west},{north},{east});
  way["natural"="cave_entrance"]({south},{west},{north},{east});
  relation["natural"="cave_entrance"]({south},{west},{north},{east});

  node["natural"="spring"]({south},{west},{north},{east});
  way["natural"="spring"]({south},{west},{north},{east});
  relation["natural"="spring"]({south},{west},{north},{east});

  node["natural"="beach"]({south},{west},{north},{east});
  way["natural"="beach"]({south},{west},{north},{east});
  relation["natural"="beach"]({south},{west},{north},{east});

  // Other Points of Interest
  node["tourism"="zoo"]({south},{west},{north},{east});
  way["tourism"="zoo"]({south},{west},{north},{east});
  relation["tourism"="zoo"]({south},{west},{north},{east});

  node["tourism"="aquarium"]({south},{west},{north},{east});
  way["tourism"="aquarium"]({south},{west},{north},{east});
  relation["tourism"="aquarium"]({south},{west},{north},{east});

  node["tourism"="viewpoint"]({south},{west},{north},{east});
  way["tourism"="viewpoint"]({south},{west},{north},{east});
  relation["tourism"="viewpoint"]({south},{west},{north},{east});

  node["tourism"="theme_park"]({south},{west},{north},{east});
  way["tourism"="theme_park"]({south},{west},{north},{east});
  relation["tourism"="theme_park"]({south},{west},{north},{east});
  
  node["historic"="monument"]({south},{west},{north},{east});
  way["historic"="monument"]({south},{west},{north},{east});
  relation["historic"="monument"]({south},{west},{north},{east});
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
                        "castle",
                        "church",
                        "ruins",
                        "memorial",
                        "theatre",
                        "opera_house",
                        "gallery",
                        "museum",
                        "artwork",
                        "park",
                        "garden",
                        "water_park",
                        "theme_park",
                        "marina",
                        "golf_course",
                        "sports_centre",
                        "peak",
                        "waterfall",
                        "cave_entrance",
                        "spring",
                        "beach",
                        "zoo",
                        "aquarium",
                        "viewpoint",
                        "theme_park",
                        "monument"
                    ]
                ]
            )
            attractions.append(f"{element['tags']['name']} ({tag_description})")

    if attractions:
        print(f"Tourist Attractions in {city_name}:")
        for attraction in attractions:
            print(attraction)
    else:
        print("No tourist attractions found.")


# Example usage
city_name = input("Enter a city name: ")
get_tourist_attractions(city_name)
