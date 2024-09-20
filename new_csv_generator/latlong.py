from geopy.geocoders import Nominatim
from geopy import distance

# def latlong(location1,location2):
#     geocoder = Nominatim(user_agent = "sugam")
#     coordinates1 =geocoder.geocode(location1)
#     coordinates2 = geocoder.geocode(location2)
#     lat1, long1 = (coordinates1.latitude),(coordinates1.longitude)
#     lat2, long2 = (coordinates2.latitude),(coordinates2.longitude)
#     place1 = (lat1,long1)
#     place2 = (lat2,long2)
#     print(lat1)
#     print(distance.distance(place1,place2))


def latlong(location, city):
    geocoder = Nominatim(user_agent="sugam")
    full_query = f"{location}, {city}"  # Adds city to the query
    coordinates = geocoder.geocode(full_query)
    if coordinates is None:
        return None, None
    lat, long = coordinates.latitude, coordinates.longitude
    return lat, long


print(latlong("Goa Station", "Goa"))


# location1 = "Durgapuja Mandap, Ruchika Market"
# location2 = "Children Park"
# latlong(location1,location2)
