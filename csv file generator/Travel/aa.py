from geopy.geocoders import Nominatim
from geopy import distance

geocoder = Nominatim(user_agent="sarang")
location1 = "lingaraj temple"
location2 = "bhubaneswar station"
coor1 = geocoder.geocode(location1)
coor2 = geocoder.geocode(location2)
lat1, long1 = (coor1.latitude), (coor1.longitude)
lat2, long2 = (coor2.latitude), (coor2.longitude)
place1 = (lat1, long1)
place2 = (lat2, long2)
print(distance.distance(place1, place2))
