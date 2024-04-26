import requests
import googlemaps
import json
import dateutil
from datetime import datetime
import os
from dotenv import load_dotenv
import pprint
    
class api(object):
    def __init__(self, api_key):
        self.session = requests.Session()
        self.key = api_key
        self.client = googlemaps.Client(self.key)
    
    """
    uses google maps python api to find address data for a place input as a string,
    returns the address from the response, if an error occurs, prints code and message
    associated with the error type
    """
    
    # build in error handling for invalid locations
    def get_addr(self, location):
        query = f'Closest WMATA Metro Station to {location}'
        response = self.client.find_place(input=query, 
                                          input_type='textquery', 
                                          fields=['formatted_address','name','types'])
        if "error" in response:
            code = response["error"]["code"]
            msg = response["error"]["message"]
            return f'Code:{code}, Error Message: {msg}'
        
        return response['candidates'][0]['formatted_address']
        
    """
    queries a route from the google routes api between point start and point end,
    if an error occurs, prints the code and message associated with the error type
    """
    def compute_route(self, start, end, departure_t):
        routes_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        
        # get addresses of start and end
        origin_addr = self.get_addr(location=start)
        dest_addr = self.get_addr(location=end)
                    
        # format data to pass into request
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.key,
            'X-Goog-FieldMask': 'routes.legs.steps.transitDetails'
        }
        
        # extra parameters for query
        data = {
            "origin" : {
                "address": origin_addr
            },
            "destination": {
                "address": dest_addr
            },
            'travelMode': "TRANSIT",
            'departureTime': departure_t,
            'transitPreferences': {
                'allowedTravelModes': ["SUBWAY", "TRAIN"]
            }
        }
        
        # request
        response = requests.post(routes_url, headers=headers, json=data)
        
        if "error" in response:
            code = response["error"]["code"]
            msg = response["error"]["message"]
            return f'Code:{code}, Error Message:{msg}'
        
        return response

# testing route computation stuff

load_dotenv()
time = datetime.now()
new_hour = 0;
if time.hour + 4 >= 24:
    new_hour = time.hour + 4 - 24
else:
    new_hour = time.hour + 4

if time.minute - 30 < 0:
    new_minute = time.minute - 30 + 60
    new_hour = new_hour - 1
else:
    new_minute = time.minute - 30

zulu_timestr = f'{time.year}-{time.month}-{time.day}T{new_hour:02}:{new_minute:02}:00Z'
print(zulu_timestr)
client = api(os.getenv('GOOG_API_KEY'))
# takes time as HH:MM
resp = client.compute_route("Wiehle Avenue", "University of Maryland College Park", zulu_timestr)
resp_dict = resp.json()

# local json processing stuff
# with open(r"dump.json", "w", encoding="utf-8") as f:
#     json.dump(resp.json(), f, ensure_ascii=False, indent=4)
# with open(r"dump.json", "r") as f:
#     resp = json.load(f)

filtered = filter((lambda x: x), resp_dict['routes'][0]['legs'][0]['steps'])

for x in filtered:
    pprint.pprint(x)
    
# notes about testing:
# need to convert local time to UTC for zulu fmt
# for some reason the departure time calculation has a random 30 minute buffer built in??
