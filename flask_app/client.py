import requests
import googlemaps
import re
import datetime
import calendar
    
    
class api(object):
    def __init__(self, api_key):
        self.session = requests.Session()
        self.key = api_key
        self.client = googlemaps.Client(self.key)
        self.routes_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        self.routes_header = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.key,
            'X-Goog-FieldMask': 'routes.legs.steps.transitDetails'
        }
    
    """
    desc: uses google maps python api to find address data for a place input as a string,
        returns the address from the response, if an error occurs, prints code and message
        associated with the error type
    params:
        location: location to search around <string>
    """
    
    # build in error handling for invalid locations
    def get_addr(self, location):
        query = f'WMATA Metro near {location}'
        response = self.client.find_place(input=query, 
                                          input_type='textquery', 
                                          fields=['formatted_address','name','types'])
        if "error" in response:
            code = response["error"]["code"]
            msg = response["error"]["message"]
            return f'Code:{code}, Error Message: {msg}'
                
        # if candidates is empty it couldn't find the location
        if not response['candidates']:
            return "Error: Could not find location, please try again."
        
        return response['candidates'][0]['formatted_address']
        
    """
    desc: 
        queries a route from the google routes api between point start and point end,
        if an error occurs, prints the code and message associated with the error type,
        otherwise, returns a list of transit directions
    params:
        start: desired origin <string>
        end: desired destination <string>
        departure_t: time to depart <datetime.datetime>
    """
    def compute_route(self, start, end, departure_dt):
        
        # get addresses of start and end
        origin_addr = self.get_addr(location=start)
        dest_addr = self.get_addr(location=end)
        
        # convert datetime to ZULU UTC format
        # for some reason it has a 30 minute buffer, remove that buffer, rectify new time
        # there are some edge cases here lol but we don't talk about that
        query_yr = int(departure_dt.year)
        query_mnt = int(departure_dt.month)
        query_day = int(departure_dt.day)
        query_hr = int(departure_dt.hour) + 4
        query_min = int(departure_dt.minute)
        
        # fixes underflowed/overflowed times and returns a corrected datetime
        def rectify_time(year, month, day, hour, minute):
            # minute underflow/overflow
            if minute < 0:
                minute += 60
                hour -= 1
            elif minute > 60:
                minute -= 60
                hour += 1
            
            # hour underflow/overflow
            if hour < 0:
                hour += 24
                day -= 1
            elif hour >= 24:
                hour -= 24
                day += 1
            
            # day underflow/overflow
            _, max = calendar.monthrange(year, month)

            if day < 1:
                month -= 1
                _, max_new = calendar.monthrange(year, month)
                day = max_new
            elif day > max:
                month += 1
                day = 1
            
            # month underflow/overflow
            if month < 1:
                year -= 1
                month = 12
            if month > 12:
                year += 1
                month = 1
            
            return datetime.datetime(year, month, day, hour, minute)
        
        UTC = rectify_time(query_yr, query_mnt, query_day, query_hr, query_min)
            
        zulu_timestr = f'{UTC.year:04}-{UTC.month:02}-{UTC.day:02}T{UTC.hour:02}:{UTC.minute:02}:00Z'
        
        # extra parameters for query
        data = {
            "origin" : {
                "address": origin_addr
            },
            "destination": {
                "address": dest_addr
            },
            'travelMode': "TRANSIT",
            'departureTime': zulu_timestr,
            'transitPreferences': {
                'allowedTravelModes': ["SUBWAY"]
            }
        }
        
        # request
        response = requests.post(url=self.routes_url, headers=self.routes_header, json=data)
                
        if "error" in response:
            code = response["error"]["code"]
            msg = response["error"]["message"]
            return f'Code:{code}, Error Message:{msg}'
    
        # converts json to dictionary, filters for transit steps
        resp_as_dict = response.json()
        
        # if the route is empty that just means you have to walk
        if not resp_as_dict:
            return None
            
        filtered = filter((lambda x: x), resp_as_dict['routes'][0]['legs'][0]['steps'])
        
        # list of information about each step of transit route, list is in step order
        route_info = []
        
        # pattern to extract date data
        time_pattern = re.compile("([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):[0-9]{2}Z")
        
        for step in filtered:
            matched_dpt = re.fullmatch(time_pattern, 
                                       step['transitDetails']['stopDetails']['departureTime'])
            matched_arr = re.fullmatch(time_pattern,
                                       step['transitDetails']['stopDetails']['arrivalTime'])
            
            # get matched groups
            dpt_yr, dpt_mnt, dpt_day, dpt_hr, dpt_min = matched_dpt.group(1, 2, 3, 4, 5)
            arr_yr, arr_mnt, arr_day, arr_hr, arr_min = matched_arr.group(1, 2, 3, 4, 5)
            
            rectified_dpt = rectify_time(int(dpt_yr), int(dpt_mnt), int(dpt_day), int(dpt_hr) - 4, int(dpt_min))
            rectified_arr = rectify_time(int(arr_yr), int(arr_mnt), int(arr_day), int(arr_hr) - 4, int(arr_min))
            
            route_info.append({
                'line_info': {
                    "line": step['transitDetails']['transitLine']['name'],
                    'hex_color': step['transitDetails']['transitLine']['color'],
                    "headsign": step['transitDetails']['headsign']
                },
                "from": {
                    "name": step['transitDetails']['stopDetails']['departureStop']['name'],
                    'est_dept_t': rectified_dpt       
                },
                "to": {
                    "name": step['transitDetails']['stopDetails']['arrivalStop']['name'],
                    'est_arr_t': rectified_arr
                }
            })
        
        # returns a list of the filtered non-empty transit steps with necessary information
        return route_info
