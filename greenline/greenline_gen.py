import json
 
with open('greenline_ids.json', 'r') as openfile:
 
    json_object = json.load(openfile)


new_json_object = {}



for i, each in enumerate(json_object):

    
    park_st = -1
    gov_center = -1
    for index, item in enumerate(json_object):
        if item["id"] == 'place-pktrm':
            park_st = index
        if item["id"] == 'place-gover':
            gov_center = index
 

for i, each in enumerate(json_object):


    id = each["id"]

    id = id.replace("place-", "")
    
    direction_id = 0 

    postfix = ""
    if i < park_st:
        postfix = "Inbound"
    elif i == park_st or i == gov_center:
        postfix = "Westbound"
    else:
        postfix = "Outbound"

    key = f'{each["name"]} {postfix}'
    value = f'*{id},{direction_id}&route=Green'

    new_json_object[key] = value


    direction_id = 1

    postfix = ""
    if i < park_st:
        postfix = "Outbound"
    elif i == park_st or i == gov_center:
        postfix = "Eastbound"
    else:
        postfix = "Inbound"

    key = f'{each["name"]} {postfix}'
    value = f'*{id},{direction_id}&route=Green'

    new_json_object[key] = value




        with open("final_green.json", "w") as outfile:

            outfile.write(json.dumps(new_json_object, indent=4))
