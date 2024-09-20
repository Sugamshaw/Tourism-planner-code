import requests
from geopy.geocoders import Nominatim

def get_city_bbox(city_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city_name, exactly_one=True)
    if location:
        return location.raw['boundingbox']
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

    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    attractions = []
    for element in data['elements']:
        if 'tags' in element and 'name' in element['tags']:
            tag_description = ' or '.join([tag for tag, value in element['tags'].items() if value in [
                'attraction', 'museum', 'monument', 'castle', 'gallery', 'zoo', 'park', 'garden', 'viewpoint', 'beach']])
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
