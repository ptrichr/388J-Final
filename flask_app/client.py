import requests
import googlemaps
import json
import dateutil
import datetime
import os
from dotenv import load_dotenv
    
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
    def get_addr(self, location):
        query = f'Closest Metro Station to {location} Washington DC'
        response = json.load(self.client.find_place(input=query, 
                                                  input_type='textquery', 
                                                  fields=['formatted_address','name']))
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

# testing

# load_dotenv()
# time = datetime.datetime.today()
# zulu_timestr = f'{time.year}-{time.month}-{time.day}T{time.hour}:{time.minute}:00Z'
# client = api(os.getenv('GOOG_API_KEY'))
# # takes time as HH:MM
# resp = client.compute_route("L'enfant Plaza",
#                      "University Of Maryland",
#                      zulu_timestr)
# print(resp)
