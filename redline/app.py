import json

from datetime import datetime, timedelta

import urllib3

http = urllib3.PoolManager()

# import requests

 
with open('name_to_id.json', 'r') as openfile:
    stops = json.load(openfile)
    stops = stops.items()

for i, each in enumerate(stops):
    park_st = -1
    downtown_crossing = -1
    for index, item in enumerate(stops):
        if item[1] == 'place-pktrm':
            park_st = index
        if item[1] == 'place-dwnxg':
            downtown_crossing = index


def getNextTimes(stop_info, route):
    filtered = [x for x in stop_info if x["attributes"]["arrival_time"]]
    
    filtered = [x for x in filtered if route in x["relationships"]["route"]["data"]["id"]]

    
    res = []
    for each in filtered[:4]:
        
        try :
            
            arrival_string = each["attributes"]["arrival_time"]
                
                
            i = len(arrival_string) - 6
            
            timezone = arrival_string[i:]
    
            arrival_string = arrival_string[:i]
    
            arrival_date = datetime.strptime(arrival_string, '%Y-%m-%dT%H:%M:%S')
            
            h = int(timezone[2])
            now = datetime.now() - timedelta(hours=5)
            
            delta = arrival_date - now 
                
                
            route_id = ""
            if not route == "Red":
                route_id = each["relationships"]["route"]["data"]["id"]
            
           
            
            if delta.days < 0:
                res.append(f'0 min')
            
            else:
                seconds = delta.total_seconds()
                minutes = int((seconds % 3600) // 60)
                
                res.append(f'{minutes} min {route_id}')
        except:
            
            print(f'An Error occurred parsing: {each}')
            continue

    
    if len(res) > 0:
        return f'Arrives in {", ".join(res)}'
    else:
        return "No predictions available at this time"



def getPrefix(stop_id):

    res = {
        0: "",
        1: ""
    }


    index = 0

    for i, each in enumerate(stops):
        if each[1] == stop_id:
            index = i

    prefix = ""
    if index < park_st:
        prefix = "Inbound"
    elif index == park_st or index == downtown_crossing:
        prefix = "Southbound"
    else:
        prefix = "Outbound"
    
    res[0] = prefix

    prefix = ""
    if index < park_st:
        prefix = "Outbound"
    elif index == park_st or index == downtown_crossing:
        prefix = "Northbound"
    else:
        prefix = "Inbound"
    
    res[1] = prefix

    
    return res



def lambda_handler(event, context):
    
    stop = event["queryStringParameters"]["stop"]
    
    prefixes = getPrefix(stop)
        
    route = "Red"
    
    if "route" in event["queryStringParameters"]:
        route = event["queryStringParameters"]["route"]


    direction_id = 0
    url = f'https://api-v3.mbta.com/predictions?filter%5Bstop%5D={stop}&filter%5Bdirection_id%5D={direction_id}&include=stop'

    
    # r = http.request('GET', url)
    # stop_info = json.loads(r.data)["data"]

    r = requests.get(url)
    stop_info = json.loads(r.text)["data"]

    

    first = f'{prefixes[0]}: {getNextTimes(stop_info, route)}'

    direction_id = 1
    url = f'https://api-v3.mbta.com/predictions?filter%5Bstop%5D={stop}&filter%5Bdirection_id%5D={direction_id}&include=stop'

    
    # r = http.request('GET', url)
    # stop_info = json.loads(r.data)["data"]

    r = requests.get(url)
    stop_info = json.loads(r.text)["data"]

    second = f'{prefixes[1]}: {getNextTimes(stop_info, route)}'



    return {
            'statusCode': 200,
            'body': first + second
        } 
    
    
    

res = lambda_handler({"queryStringParameters": {"stop": "place-cntsq", "direction_id": "0"}},None)

print(res)
