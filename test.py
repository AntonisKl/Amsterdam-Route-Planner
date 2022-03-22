# import geocoder
# g = geocoder.ip('me')
# print(g.latlng)

# import requests
#
# freegeoip = "http://freegeoip.net/json"
# geo_r = requests.get(freegeoip)
# geo_json = geo_r.json()
#
# user_postition = [geo_json["latitude"], geo_json["longitude"]]
#
# print(user_postition)

from geopy.geocoders import Nominatim

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")

# entering the location name
getLoc = loc.geocode("Amsterdam")

# printing address
print(getLoc.address)

# printing latitude and longitude
print("Latitude = ", getLoc.latitude, "\n")
print("Longitude = ", getLoc.longitude)
