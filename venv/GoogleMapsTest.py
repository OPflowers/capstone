import urllib.request
import requests
import json
import googlemaps
import math
from geopy.geocoders import Nominatim
from googlegeocoder import GoogleGeocoder

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'AIzaSyABFLTbVUwK1gJvs5rweaBM1bU-fBtXXSI'
geocoder = GoogleGeocoder(api_key)

origin = input('Where are you?: ').replace(' ','+')

geolocator = Nominatim(user_agent= "capstone")
location = geolocator.geocode("1600 amphitheatre parkway")
print(location.address)
print((location.latitude, location.longitude))
#gmaps = googlemaps.Client(api_key)
#geocode_result = gmaps.geocode(origin)
#local = gmaps.local_search('hospital near ' + origin)
#lat = geocode_result[0].geometry.location.lat()
#print(geocode_result)

#destination = input('Where do you want to go?: ').replace(' ','+')

#nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
#request = endpoint + nav_request
#response = urllib.request.urlopen(request).read()

#directions = json.loads(response)
#print(directions)
def getDistance(lat1, lng1, lat2, lng2):
   earth_radius = 6371 # this is in km
   delta_lat = change_to_radians(lat2 - lat1)
   delta_lng = change_to_radians(lng2 - lng1)

   #Haversine formula
   a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + \
      math.cos(change_to_radians(lat1)) * math.cos(change_to_radians(lat2)) * \
      math.sin(delta_lng/2) * math.sin(delta_lng/2)
   c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
   d = earth_radius * c
   return d

def change_to_radians(degree):
   return degree * (math.pi/180)

def findPlaces(latitude, longitude,radius, origin_lat, origin_lng, pagetoken = None):
   lat = latitude
   lng = longitude
   type = "hospital"
   url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type}&key={APIKEY}{pagetoken}".format(lat = lat, lng = lng, radius = radius, type = type,APIKEY = api_key, pagetoken = "&pagetoken="+pagetoken if pagetoken else "")
   #print(url)
   response = requests.get(url)
   res = json.loads(response.text)
   # print(res)
   print("here results ---->>> ", len(res["results"]))
   final_destination = [math.inf, math.inf]
   for result in res["results"]:
      #info = ";".join(map(str,result["geometry"]["location"]["lat"],result["geometry"]["location"]["lng"],))
      #print(info)
      if getDistance(origin_lat, origin_lng, result["lat"], result["lng"]) < getDistance(origin_lat, origin_lng, final_destination[0], final_destination[1]):
         final_destination[0] = result["lat"]
         final_destination[1] = result['lng']
      print((result["lat"]),result['lng'])
   pagetoken = res.get("next_page_token",None)

   if final_destination[0] == math.inf and final_destination[1] == math.inf:
      return None
   return final_destination

pagetoken = None
radius = 200
destination = None
while destination == None:
     destination = findPlaces(location.latitude, location.longitude, radius, location.latitude, location.longitude, pagetoken=pagetoken)
     if destination != None:
        break
     else:
        radius = radius + 200